# DStream::anomalyDetectionEngine

首发版本：3.00.3

## 语法

`DStream::anomalyDetectionEngine(metrics, timeColumn, [keyColumn],
[windowSize], [step], [garbageSize], [roundTime=true],
[anomalyDescription])`

## 详情

创建一个流计算异常检测引擎。参考 createAnomalyDetectionEngine。

## 参数

**metrics** 以元代码或元组的格式表示异常指标，每个异常指标必须是布尔表达式，如<[sum(qty) >
5, avg(qty) > qty, qty < 4]>。有关元代码的更多信息可参考 元编程。

注：

*metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**timeColumn** 字符串标量，该参数用于指定订阅的流数据表中时间列的名称。

**keyColumn** 可选参数，字符串标量或向量，表示分组列名。异常检测引擎会按照 *keyColumn*
对输入的数据分组，计算将在各分组分别进行。

**windowSize** 可选参数，正整数。如果 *metrics* 中包含聚合函数，必须指定
*windowSize*，它表示计算的数据窗口的长度，数据窗口只包含上边界不包含下边界。如果 *metrics*
中不包含聚合函数，该参数无效。

**step** 可选参数，正整数。如果 *metrics* 中包含聚合函数，必须指定 *step*，并且必须能够被
*windowSize* 整除，它表示计算的时间间隔。如果 *metrics* 中不包含聚合函数，该参数无效。

**garbageSize** 可选参数，正整数。它是可选参数，默认值是 2,000（单位为行）。如果没有指定
*keyColumn*，当内存中历史数据的数量超过 *garbageSize* 时，系统会清理本次计算不需要的历史数据。如果指定了
*keyColumn*，意味着需要分组计算时，内存清理是各分组独立进行的。当一个组的历史数据记录数超出 *garbageSize*
时，会清理该组不再需要的历史数据。若一个组的历史数据记录数未超出 *garbageSize*，则该组数据不会被清理。如果 *metrics*
中没有聚合函数，这个参数不起作用。

**roundTime** 可选参数，布尔值，表示若数据时间精度为毫秒或者秒且 *step* > 一分钟，如何对窗口边界值进行规整处理。默认值为
true，表示按照既定的多分钟规则（见以上表格）进行规整。若为 false，则按一分钟规则（见以上表格）进行窗口规整（详情参考
`规整规则表`）。

若要开启快照机制 (snapshot)，必须指定 *snapshotDir* 与 *snapshotIntervalInMsgCount*。

**anomalyDescription** 可选参数，字符串向量，长度和 *metrics*
中定义的指标数量相同。指定该参数后，输出表的最后一列将显示异常条件对应的字符串。

## 返回值

一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

adGraph = createStreamGraph("anomalyDetection")
adGraph.source("trade",`time`sym`qty, [TIMESTAMP, SYMBOL, INT])
  .anomalyDetectionEngine(metrics=<[sum(qty) > 5, avg(qty) > qty, qty < 4]>, timeColumn=`time, keyColumn=`sym, windowSize=3, step=3)
  .sink("anomal_output")
adGraph.submit()
go

times=2024.10.08T01:01:01.001 + 1..6
syms=["A", "B", "A", "B", "A", "B"]
qtys=[6, 5, 4, 3, 2, 1]
tmp=table(times as timestamp, syms as sym, qtys as qty)

appendOrcaStreamTable("trade", tmp)

select * from orca_table.anomal_output
```

| time | sym | type | metric |
| --- | --- | --- | --- |
| 2024.10.08T01:01:01.003 | A | 0 | sum(qty) > 5 |
| 2024.10.08T01:01:01.004 | A | 1 | avg(qty) > qty |
| 2024.10.08T01:01:01.005 | B | 2 | qty < 4 |
| 2024.10.08T01:01:01.006 | A | 1 | avg(qty) > qty |
| 2024.10.08T01:01:01.006 | A | 2 | qty < 4 |
| 2024.10.08T01:01:01.006 | B | 0 | sum(qty) > 5 |
| 2024.10.08T01:01:01.007 | B | 1 | avg(qty) > qty |
| 2024.10.08T01:01:01.007 | B | 2 | qty < 4 |
