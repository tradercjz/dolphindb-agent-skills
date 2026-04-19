<!-- Auto-mirrored from upstream `documentation-main/stream/time_bucket_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 时间桶引擎

时间桶引擎与时间序列引擎相似，可以将数据基于指定时间窗口进行划分，并在窗口内进行聚合计算。它们的不同之处在于，时间序列引擎只能按照固定的窗口长度来进行聚合计算，且计算由第一条时间戳大于窗口结束边界的数据触发；而时间桶引擎允许自定义时间窗口的划分方式，并在时间窗口闭合的同时触发聚合计算。该引擎适用于需要对不定长窗口即时计算的场景，通过与时序聚合引擎级联使用，可以对高频聚合计算结果进行进一步处理，如

* 基于已有的 1 分钟 K 线合成 5 分钟、15 分钟、30 分钟的 K 线。
* 基于已有的 1 分钟频率因子，根据用户自定义的计算逻辑得到 5 分钟、15 分钟、30 分钟频率的因子。

例如，在 1 分钟 K 线合成 5 分钟 K 线的场景中，先通过时序聚合引擎处理原始行情数据，计算 1 分钟 K 线数据，再将1 分钟 K 线数据输入时间桶引擎。在 5 分钟窗口
[09:00,09:05) 内，当一条 1 分钟 K 线数据被输入引擎时，如果它的时间戳已经达到或超过当前窗口的右边界
09:04，时间桶引擎就会立即关闭该窗口并执行计算。如果再次使用时序聚合引擎合成 5 分钟 K 线，则需要等待 09:05 或之后的数据注入引擎才能输出计算结果。

![](images/time_bucket_engine.png)

时间桶引擎由 `createTimeBucketEngine` 函数创建。语法如下：

`createTimeBucketEngine(name,timeCutPoints,metrics,dummyTable,outputTable,timeColumn,[keyColumn],[useWindowStartTime],[closed='left'],[fill='none'],[keyPurgeFreqInSec=-1],[outputElapsedMicroseconds=false],[parallelism=1],[outputHandler=NULL],[msgAsTable=false],[snapshotDir],[snapshotIntervalInMsgCount])`

参数的详细含义可以参考：createTimeBucketEngine。

## 应用示例

下面以 1 分钟 K 线合成 5 分钟 K 线的计算来说明时间桶引擎如何进行窗口边界的规整以及窗口计算。

首先创建流数据表 trades，包含 time、sym、price 和 volume 四列，模拟股票行情数据源。创建时间序列引擎 timeSeries1，根据
trades 中的数据计算1分钟 K 线，并将计算结果写入流数据表 output1。

```
share streamTable(1000:0, `time`sym`price`volume, [TIMESTAMP, SYMBOL, DOUBLE, INT]) as trades
share streamTable(1000:0, `time`sym`firstPrice`maxPrice`minPrice`lastPrice`sumVolume, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT]) as output1
timeSeries1 = createTimeSeriesEngine(name="timeSeries1", windowSize=60000, step=60000, metrics=<[first(price), max(price), min(price), last(price), sum(volume)]>, dummyTable=trades, outputTable=output1, timeColumn=`time, useSystemTime=false, keyColumn=`sym, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="timeSeries1", offset=0, handler=append!{timeSeries1}, msgAsTable=true)
```

创建时间桶引擎 timeBucket1，通过订阅流数据表 output1，将 1 分钟 K 线输入时间桶引擎 timeBucket1，进而合成 5 分钟 K
线，最后将结果写入 output2 表。其中，*timeCutPoints* 中的任意两个相邻元素确定了窗口的左、右边界，并且
*timeCutPoints* 中元素的时间精度决定了关闭窗口右边界的时间精度。

```
output2 = table(1000:0, `time`sym`firstPrice`maxPrice`minPrice`lastPrice`sumVolume, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT])
timeCutPoints=[10:00m, 10:05m, 10:10m, 10:15m]
timeBucket1 = createTimeBucketEngine(name="timeBucket1", timeCutPoints=timeCutPoints, metrics=<[first(firstPrice), max(maxPrice), min(minPrice), last(lastPrice), sum(sumVolume)]>, dummyTable=output1, outputTable=output2, timeColumn=`time, keyColumn=`sym)
subscribeTable(tableName="output1", actionName="timeBucket1", offset=0, handler=append!{timeBucket1}, msgAsTable=true);
```

向流数据表 trades 插入数据，代码如下：

```
insert into trades values(2024.10.08T10:01:01.785,`A, 10.83, 2110)
insert into trades values(2024.10.08T10:01:02.125,`B,21.73, 1600)
insert into trades values(2024.10.08T10:01:12.457,`A,10.79, 2850)
insert into trades values(2024.10.08T10:03:10.789,`A,11.81, 2250)
insert into trades values(2024.10.08T10:03:12.005,`B, 22.96, 1980)
insert into trades values(2024.10.08T10:08:02.236,`A, 11.25, 2400)
insert into trades values(2024.10.08T10:08:04.412,`B, 23.03, 2130)
insert into trades values(2024.10.08T10:08:05.152,`B, 23.18, 1900)
insert into trades values(2024.10.08T10:08:30.021,`A, 11.04, 2300)
insert into trades values(2024.10.08T10:09:20.123,`A, 11.85, 2200)
insert into trades values(2024.10.08T10:10:02.236,`A, 11.06, 2200)
insert into trades values(2024.10.08T10:11:04.412,`B, 23.15, 1880)
```

查看时间序列引擎 timeSeries1 的计算结果：

```
select * from output1
```

| time | sym | firstPrice | maxPrice | minPrice | lastPrice | sumVolume |
| --- | --- | --- | --- | --- | --- | --- |
| 2024.10.08 10:02:00.000 | A | 10.83 | 10.83 | 10.79 | 10.79 | 4,960 |
| 2024.10.08 10:02:00.000 | B | 21.73 | 21.73 | 21.73 | 21.73 | 1,600 |
| 2024.10.08 10:04:00.000 | A | 11.81 | 11.81 | 11.81 | 11.81 | 2,250 |
| 2024.10.08 10:04:00.000 | B | 22.96 | 22.96 | 22.96 | 22.96 | 1,980 |
| 2024.10.08 10:09:00.000 | A | 11.25 | 11.25 | 11.04 | 11.04 | 4,700 |
| 2024.10.08 10:09:00.000 | B | 23.03 | 23.18 | 23.03 | 23.18 | 4,030 |
| 2024.10.08 10:10:00.000 | A | 11.85 | 11.85 | 11.85 | 11.85 | 2,200 |

查看时间桶引擎 timeBucket1 的计算结果：

```
select * from output2
```

| time | sym | firstPrice | maxPrice | minPrice | lastPrice | sumVolume |
| --- | --- | --- | --- | --- | --- | --- |
| 2024.10.08 10:05:00.000 | A | 10.83 | 11.81 | 10.79 | 11.81 | 7,210 |
| 2024.10.08 10:05:00.000 | B | 21.73 | 22.96 | 21.73 | 22.96 | 3,580 |
| 2024.10.08 10:10:00.000 | A | 11.25 | 11.25 | 11.04 | 11.04 | 4,700 |
| 2024.10.08 10:10:00.000 | B | 23.03 | 23.18 | 23.03 | 23.18 | 4,030 |

时间桶引擎通过 *timeCutPoints*的第一个元素和最后一个元素来确定计算的时间范围。在一个时间窗口内，当收到第一条时间戳大于等于窗口右边界的数据时触发窗口关闭，窗口内的数据根据
*metrics* 参数中定义的计算规则进行计算。引擎计算的时间精度也由 *timeCutPoints* 参数的时间精度决定。当
*timeCutPoints*参数的时间向量精度为分钟时，引擎以分钟级精度划分时间窗口并进行计算；当时间向量精度为秒时，引擎以秒级精度划分时间窗口并进行计算。

在本例中，时间桶引擎根据 *keyColumn* 参数指定的分组列 *sym* 进行分组计算。由于 A、B 两组数据的计算逻辑一致，因此我们仅对 A
组数据进行说明。 A 组的首条数据的时间戳为 10:02:00.000（后面简称为 10:02m ），在第一个时间窗口 [10:00m, 10:05m)
中。在窗口边界为左闭右开的情况下，收到时间戳大于等于右边界时间戳减去 1 个单位的数据时窗口关闭，因此当时间大于等于 10:04m 的数据输入引擎时窗口关闭，引擎根据
*metrics* 中的计算规则对窗口区间内 10:02m 和 10:04m 的数据进行计算，并输出结果。当 10:09m 的数据输入引擎时，由于
[10:05m, 10:10m) 区间到 10:09m 截至，因此窗口关闭，该窗口内只有一条数据。10:10m 的 A 组数据输入引擎后，由于时间大于等于 10:14m
的数据尚未到来，窗口还未关闭，因此不进行聚合计算。

接下来，展示窗口边界为左开右闭情况下的计算结果。创建时间桶引擎 timeBucket2，通过 closed 参数指定窗口边界为左开右闭，订阅流数据表
output1，并将结果写入 output3 表。

```
output3 = table(1000:0, `time`sym`firstPrice`maxPrice`minPrice`lastPrice`sumVolume, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT])
timeBucket2 = createTimeBucketEngine(name="timeBucket2", timeCutPoints=timeCutPoints, metrics=<[first(firstPrice), max(maxPrice), min(minPrice), last(lastPrice), sum(sumVolume)]>, dummyTable=output1, outputTable=output3, timeColumn=`time, keyColumn=`sym, closed='right')
subscribeTable(tableName="output1", actionName="timeBucket2", offset=0, handler=append!{timeBucket2}, msgAsTable=true);
```

查看时间桶引擎 timeBucket2 的计算结果：

```
select * from output3
```

| time | sym | firstPrice | maxPrice | minPrice | lastPrice | sumVolume |
| --- | --- | --- | --- | --- | --- | --- |
| 2024.10.08 10:05:00.000 | A | 10.83 | 11.81 | 10.79 | 11.81 | 7,210 |
| 2024.10.08 10:05:00.000 | B | 21.73 | 22.96 | 21.73 | 22.96 | 3,580 |
| 2024.10.08 10:10:00.000 | A | 11.25 | 11.85 | 11.04 | 11.85 | 6,900 |

在窗口边界为左开右闭的情况下，当第一条时间戳大于等于右边界时间戳的数据输入引擎时，触发窗口关闭。在本例中，收到第一条时间大于等于 (10:00m, 10:05m]
区间右边界的数据（10:09m 的数据）时，窗口关闭，引擎对 10:02m 和 10:04m 的数据进行计算，并输出结果。10:10m 的 A
组数据输入引擎后，(10:05m, 10:10m] 区间的窗口关闭，并对 10:09m 和 10:10m 的数据进行计算。

**相关信息**

createTimeBucketEngine

streamTable

createTimeSeriesEngine

subscribeTable
