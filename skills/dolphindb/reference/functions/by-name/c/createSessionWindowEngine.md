# createSessionWindowEngine

## 语法

`createSessionWindowEngine(name, sessionGap, metrics,
dummyTable, outputTable, [timeColumn], [useSystemTime=false], [keyColumn],
[updateTime], [useSessionStartTime=true], [snapshotDir],
[snapshotIntervalInMsgCount], [raftGroup], [forceTriggerTime])`

## 详情

创建流数据会话窗口引擎。

`createSessionWindowEngine` 的参数绝大多数与
`createTimeSeriesEngine` 一样，只有 *sessionGap* 和
*useSessionStartTime* 是它独有的参数。*sessionGap*
决定了一个会话窗口何时结束，*useSessionStartTime* 决定了输出表时间列的时间为各个窗口的起始时刻还是结束时刻。

更多流数据引擎的应用场景说明可以参考 流计算引擎。

自 2.00.11 版本开始，*dummyTable* 和 *outputTable* 支持 array
vector，但不支持在计算中使用 array vector，即 *metrics* 中不能包含 array vector 列。

## 计算规则

若某条数据之后，经过 *sessionGap*
指定的时间长度内，没有新数据到来，就进行一次窗口截断（以截断前最后一条数据的时间戳 + *sessionGap*
作为窗口的结束时刻）。窗口结束后新到来的一条数据将触发该窗口的计算。

注：

如果不使用数据输入引擎时的系统时间作为时间列进行计算，输入流数据表中时间列（*timeColumn*）所指示的时间戳必须为非递减序列；如果同时指定了分组列（*keyColumn*），则按照分组分别进行计算，组内数据的时间戳必须为非递减序列。否则，乱序数据将被直接丢弃，不参与计算。

## 参数

由于会话窗口引擎的绝大多数参数与时间序列引擎重合，请参照 createTimeSeriesEngine 中参数介绍。这里仅介绍与时间序列引擎不同的参数：

**sessionGap**
必选参数，正整数标量，是判断窗口结束的时间指标，表示某条数据到来后若等待该时间仍无更新的数据到来，就终止当前窗口。此参数的时间精度取决于
*useSystemTime* 参数。

**useSessionStartTime**: 可选参数，布尔值，默认值为
true，表示输出表中的时刻为数据窗口起始时刻，即每个窗口中第一条数据的时间戳。若设置为
false，则表示输出表中的时刻为数据窗口结束时刻，即每个窗口中最后一条数据的时刻+ *sessionGap*。如果指定 *updateTime*
，*useSessionStartTime* 必须为 true。

**forceTriggerTime** 可选参数，非负整数，单位与 *timeColumn*
的时间精度一致。该参数仅在设置 *useSystemTime* = false 时起效。当系统收到最后一条数据后，经过
*forceTriggerTime* 时间，将强制触发未计算的窗口进行计算。

注：

若设置了 *keyColumn*，则各分组内进行上述操作。

## 返回值

返回一个表对象。

## 例子

**例1.** 下例通过 `createSessionWindowEngine` 函数创建了一个会话窗口引擎，设置
*sessionGap*=5 ms，基于连续交易活动时间段而非固定时间段（区别于时间序列引擎）进行窗口划分。

会话窗口引擎识别每只股票的交易活跃期：当某股票在 5ms 内没有新交易数据时，窗口结束并输出该活动期内的成交量总和。

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
share table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT]) as output1
engine_sw = createSessionWindowEngine(name = "engine_sw", sessionGap = 5, metrics = <sum(volume)>, dummyTable = trades, outputTable = output1, timeColumn = `time, keyColumn=`sym)
subscribeTable(tableName="trades", actionName="append_engine_sw", offset=0, handler=append!{engine_sw}, msgAsTable=true)

n = 5
timev = 2018.10.12T10:01:00.000 + (1..n)
symv=take(`A`B`C,n)
volumev = (1..n)%1000
insert into trades values(timev, symv, volumev)

n = 5
timev = 2018.10.12T10:01:00.010 + (1..n)
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

n = 6
timev = 2018.10.12T10:01:00.020 + 1 2 3 8 14 20
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

select * from output1;
```

输出返回：

| time | sym | volume |
| --- | --- | --- |
| 2018.10.12T10:01:00.001 | A | 5 |
| 2018.10.12T10:01:00.002 | B | 7 |
| 2018.10.12T10:01:00.003 | C | 3 |
| 2018.10.12T10:01:00.011 | A | 5 |
| 2018.10.12T10:01:00.012 | B | 7 |
| 2018.10.12T10:01:00.013 | C | 3 |
| 2018.10.12T10:01:00.021 | A | 1 |
| 2018.10.12T10:01:00.022 | B | 2 |
| 2018.10.12T10:01:00.023 | C | 3 |

**例2.** 通过指定 *forceTriggerTime*，可以强制触发尚未计算的窗口计算。

清理环境：

```
dropStreamEngine(`engine_sw)
unsubscribeTable(, tableName="trades", actionName="append_engine_sw")
```

重新创建会话引擎，此时指定 *forceTriggerTime* 为 1000ms，意味着在引擎收到最后一条消息后，经过
1000ms，将会触发所有分组数据的计算和输出：

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
share table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT]) as output1
engine_sw = createSessionWindowEngine(name = "engine_sw", sessionGap = 5, metrics = <sum(volume)>, dummyTable = trades, outputTable = output1, timeColumn = `time, keyColumn=`sym, forceTriggerTime=1000)
subscribeTable(tableName="trades", actionName="append_engine_sw", offset=0, handler=append!{engine_sw}, msgAsTable=true)

n = 5
timev = 2018.10.12T10:01:00.000 + (1..n)
symv=take(`A`B`C,n)
volumev = (1..n)%1000
insert into trades values(timev, symv, volumev)

n = 5
timev = 2018.10.12T10:01:00.010 + (1..n)
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

n = 6
timev = 2018.10.12T10:01:00.020 + 1 2 3 8 14 20
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

sleep(1100)
select * from output1;
```

再次查询输出表，可以得到以下结果。可见 *forceTriggerTime* 成功强制触发了最后 3
个已结束但未计算的窗口。而在例 1 中，由于未设置 *forceTriggerTime*，且没有后续数据触发计算，这些窗口未能输出结果。

| time | sym | volume |
| --- | --- | --- |
| 2018.10.12T10:01:00.001 | A | 5 |
| 2018.10.12T10:01:00.002 | B | 7 |
| 2018.10.12T10:01:00.003 | C | 3 |
| 2018.10.12T10:01:00.011 | A | 5 |
| 2018.10.12T10:01:00.012 | B | 7 |
| 2018.10.12T10:01:00.013 | C | 3 |
| 2018.10.12T10:01:00.021 | A | 1 |
| 2018.10.12T10:01:00.022 | B | 2 |
| 2018.10.12T10:01:00.023 | C | 3 |
| 2018.10.12T10:01:00.028 | A | 4 |
| 2018.10.12T10:01:00.034 | B | 5 |
| 2018.10.12T10:01:00.040 | C | 6 |

**例3.** 设置 *useSessionStartTime* 为 false， 输出窗口结束时刻。

清理环境：

```
dropStreamEngine(`engine_sw)
unsubscribeTable(, tableName="trades", actionName="append_engine_sw")
```

重新创建会话引擎，此时设置 *useSessionStartTime* 为
false，使输出表中的时间列显示每个会话窗口的结束时刻（即最后一条数据时间+*sessionGap*），而不是默认的窗口开始时刻。

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
share table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT]) as output1
engine_sw = createSessionWindowEngine(name = "engine_sw", sessionGap = 5, metrics = <sum(volume)>, dummyTable = trades, outputTable = output1, timeColumn = `time, keyColumn=`sym, useSessionStartTime=false, forceTriggerTime=1000)
subscribeTable(tableName="trades", actionName="append_engine_sw", offset=0, handler=append!{engine_sw}, msgAsTable=true)

n = 5
timev = 2018.10.12T10:01:00.000 + (1..n)
symv=take(`A`B`C,n)
volumev = (1..n)%1000
insert into trades values(timev, symv, volumev)

n = 5
timev = 2018.10.12T10:01:00.010 + (1..n)
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

n = 6
timev = 2018.10.12T10:01:00.020 + 1 2 3 8 14 20
volumev = (1..n)%1000
symv=take(`A`B`C,n)
insert into trades values(timev, symv, volumev)

sleep(1100)
select * from output1;
```

| time | sym | sumVolume |
| --- | --- | --- |
| 2018.10.12 10:01:00.008 | C | 3 |
| 2018.10.12 10:01:00.009 | A | 5 |
| 2018.10.12 10:01:00.010 | B | 7 |
| 2018.10.12 10:01:00.018 | C | 3 |
| 2018.10.12 10:01:00.019 | A | 5 |
| 2018.10.12 10:01:00.020 | B | 7 |
| 2018.10.12 10:01:00.026 | A | 1 |
| 2018.10.12 10:01:00.027 | B | 2 |
| 2018.10.12 10:01:00.028 | C | 3 |
| 2018.10.12 10:01:00.033 | A | 4 |
| 2018.10.12 10:01:00.039 | B | 5 |
| 2018.10.12 10:01:00.045 | C | 6 |
