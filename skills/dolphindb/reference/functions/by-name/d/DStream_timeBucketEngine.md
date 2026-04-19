# DStream::timeBucketEngine

首发版本：3.00.3

## 语法

`DStream::timeBucketEngine(timeCutPoints, metrics, timeColumn, [keyColumn],
[useWindowStartTime], [closed='left'], [fill='none'], [keyPurgeFreqInSecond=-1],
[parallelism=1])`

## 详情

创建流计算自定义窗口长度（长度相同或不同）的时间序列聚合引擎，支持基于该引擎定义后续处理逻辑。

## 参数

**timeCutPoints** MINUTE 或 SECOND 类型向量，且不能包含空值。由
*timeCutPoints* 向量的任意两个相邻元素确定窗口的左、右边界。注意：

* *timeCutPoints* 指定的时间精度必须不高于 *timeColumn* 列的精度。
* *timeCutPoints* 指定的时间精度决定关闭窗口右边界的时间精度。如果 *timeCutPoints* 是
  MINUTE 类型，则窗口右边界的时间精度是分；如果 *timeCutPoints* 是 SECOND
  类型，则窗口右边界的时间精度是秒。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 元编程。

* 计算指标可以是一个或多个系统内置或用户自定义的聚合函数（使用 defg 关键字定义），如
  <[sum(volume), avg(price)]>；可以对聚合结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可对列与列的计算结果进行聚合计算，如
  <[std(price1-price2)]>。
* *metrics* 内支持调用具有多个返回值的函数，例如 <func(price) as
  `col1`col2>（可不指定列名）。
* 支持指定为一个常量标量或向量，例如 <1>，<[1, 2, 3]> 。当指定为常量向量时，对应的输出列必须设置为数组向量类型。
* 若 *windowSize* 为向量， *windowSize* 每个值可对应
  *metrics* 中多个计算指标。例如，*windowSize* 为[10,20]时，metrics可为
  (<[min(volume), max(volume)]>, <sum(volume)>)。
  *metrics* 也可以嵌套输入元组向量。例如：[[<[min(volume), max(volume)]>,
  <sum(volume)>], [<avg(volume)>]]

  注：

  + *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。
  + *metrics* 中不可使用嵌套聚合函数。

**timeColumn** 字符串标量或长度为2的向量，用于输入表中时间列的名称。

**keyColumn**
可选参数，字符串标量或向量，表示分组列名。若设置，则分组进行聚合计算，例如以每支股票为一组进行聚合计算。

**useWindowStartTime** 可选参数。布尔值，表示输出表中的时间是否为数据窗口起始时间。默认值为
false，表示输出表中的时间为窗口结束时间。

**closed** 字符串，用于确定滑动窗口边界的开闭情况。可选值为 'left' 或 'right'，默认值为
'left'。

* closed = 'left'： 窗口左闭右开。
* closed = 'right'： 窗口左开右闭。

**fill** 可选参数，一个标量或向量，指定某个分组的某个窗口无数据时的处理方法。可取以下值：

* 'none': 不输出结果。
* 'null': 输出结果为 NULL。
* 'ffill': 输出上一个有数据的窗口的结果。
* '具体数值'：该值的数据类型需要和对应的 *metrics* 计算结果的类型保持一致。

*fill* 可以输入向量，长度与 *metrics* 元素个数保持一致，表示为每个 *metrics* 指定不同的 *fill*
方式。若为向量，向量中各项只能是 'null', 'ffill' 或一个数值，不能是 'none'。

**keyPurgeFreqInSec**
正整数，表示清理窗口数据为空的分组的时间间隔，单位为秒。指定该参数后，若当前数据注入时间与上一次清理时间的间隔大于等于
*keyPurgeFreqInSec*，则触发对当前窗口数据为空的分组信息的清理。若指定该参数，则必须指定 *keyColumn*，且不能指定
*fill。*

**parallelism** 为不超过 63 的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。建议小于机器核数，推荐值为 4 到 8 。

## 返回值

返回一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')
g = createStreamGraph('engine')

g.source("trades", `time`sym`price`volume, [TIMESTAMP, SYMBOL, DOUBLE, INT])
.timeSeriesEngine(windowSize=60000, step=60000, metrics=<[first(price), max(price), min(price), last(price), sum(volume)]>, timeColumn=`time, useSystemTime=false, keyColumn=`sym, useWindowStartTime=false)
.timeBucketEngine(timeCutPoints=[10:00m, 10:05m, 10:10m, 10:15m], metrics=<[first(first_price), max(max_price), min(min_price), last(last_price), sum(sum_volume)]>, timeColumn=`time,  keyColumn=`sym)
.sink("output")
g.submit()
go

times = [2024.10.08T10:01:01.785, 2024.10.08T10:01:02.125, 2024.10.08T10:01:12.457, 2024.10.08T10:03:10.789, 2024.10.08T10:03:12.005, 2024.10.08T10:08:02.236, 2024.10.08T10:08:04.412, 2024.10.08T10:08:05.152, 2024.10.08T10:08:30.021, 2024.10.08T10:10:20.123, 2024.10.08T10:11:02.236, 2024.10.08T10:13:04.412, 2024.10.08T10:15:12.005]
syms = [`A, `B, `A, `A, `B, `A, `B, `B, `A, `A, `A, `B, `B]
prices = [10.83, 21.73, 10.79, 11.81, 22.96, 11.25, 23.03, 23.18, 11.04, 11.85, 11.06, 23.15, 22.06]
volumes = [2110, 1600, 2850, 2250, 1980, 2400, 2130, 1900, 2300, 2200, 2200, 1880, 2100]
tmp = table(times as time, syms as sym, prices as price, volumes as volume)
appendOrcaStreamTable("trades", tmp)

select * from orca_table.output
```

| time | sym | first\_first\_price | max\_max\_price | min\_min\_price | last\_last\_price | sum\_sum\_volume |
| --- | --- | --- | --- | --- | --- | --- |
| 2024.10.08 10:05:00.000 | A | 10.83 | 11.81 | 10.79 | 11.81 | 7,210 |
| 2024.10.08 10:05:00.000 | B | 21.73 | 22.96 | 21.73 | 22.96 | 3,580 |
| 2024.10.08 10:10:00.000 | A | 11.25 | 11.25 | 11.04 | 11.04 | 4,700 |
| 2024.10.08 10:10:00.000 | B | 23.03 | 23.18 | 23.03 | 23.18 | 4,030 |
| 2024.10.08 10:15:00.000 | B | 23.15 | 23.15 | 23.15 | 23.15 | 1,880 |
