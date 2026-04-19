# DStream::sessionWindowEngine

首发版本：3.00.3

## 语法

`DStream::sessionWindowEngine(sessionGap, metrics, [timeColumn],
[useSystemTime=false], [keyColumn], [updateTime], [useSessionStartTime=true],
[forceTriggerTime])`

## 详情

创建流计算会话窗口引擎。参考：createSessionWindowEngine。

## 参数

**sessionGap**
必选参数，正整数标量，是判断窗口结束的时间指标，表示某条数据到来后若等待该时间仍无更新的数据到来，就终止当前窗口。此参数的时间精度取决于
*useSystemTime* 参数。

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

**timeColumn** 可选参数，字符串标量或向量。当 *useSystemTime* = false
时，必须指定该参数。 该参数用于指定订阅的流数据表中时间列的名称。

注：

字符串向量必须是 date 和 time
组成的向量，date 类型为 DATE，time 类型为 TIME, SECOND 或 NANOTIME。此时，输出表第一列的时间类型必须与 concatDateTime(date, time)
的类型一致。

**useSystemTime** 可选参数，布尔值，表示是否使用数据注入引擎时的系统时间作为时间列进行计算。

* 当 *useSystemTime* =
  true时，时间序列引擎会按照数据注入时间序列引擎的时刻（毫秒精度的本地系统时间，与数据中的时间列无关），每隔固定时间截取固定长度窗口的流数据进行计算。只要一个数据窗口中含有数据，数据窗口结束后就会自动进行计算。结果中的第一列为计算发生的时间戳，与数据中的时间无关。
* 当 *useSystemTime* = false（缺省值）时，时间序列引擎根据流数据中的 *timeColumn*
  列来截取数据窗口。一个数据窗口结束后的第一条新数据才会触发该数据窗口的计算。请注意，触发计算的数据并不会参与该次计算。

  例如，一个数据窗口从 10:10:10 到 10:10:19。若 *useSystemTime*
  = true，则只要该窗口中至少有一条数据，该窗口的计算会在窗口结束后的 10:10:20 触发。若 *useSystemTime*
  = false，且 10:10:19 后的第一条数据为 10:10:25，则该窗口的计算会在 10:10:25 触发。

**keyColumn**
可选参数，字符串标量或向量，表示分组列名。若设置，则分组进行聚合计算，例如以每支股票为一组进行聚合计算。

**updateTime** 可选参数，非负整数，单位与 timeColumn 的时间精度一致。用于指定比
*step* 更短的计算时间间隔。*step* 必须是 *updateTime* 的整数倍。要设置
*updateTime*， *useSystemTime* 必须设为 false。

* updateTime 指定为正整数值时：

  + 从当前窗口的左边界开始，每隔 *updateTime*
    时间，若有新的数据到来，则对当前窗口内该数据之前的所有数据进行计算。
  + 如果系统经过 2 \* *updateTime* （至少2秒）后仍有未被处理的数据，则触发对当前窗口内所有数据的计算。
  + 若分组计算，则每组内进行上述操作。
* updateTime 指定为 0 时：在新的数据到来后，立即对当前窗口的最新数据计算并输出。

**useSessionStartTime**: 可选参数，布尔值，默认值为
true，表示输出表中的时刻为数据窗口起始时刻，即每个窗口中第一条数据的时间戳。若设置为
false，则表示输出表中的时刻为数据窗口结束时刻，即每个窗口中最后一条数据的时刻+ *sessionGap*。如果指定 *updateTime*
，*useSessionStartTime* 必须为 true。

**forceTriggerTime** 可选参数，非负整数，单位与 *timeColumn*
的时间精度一致。该参数仅在设置 *useSystemTime* = false 时起效。当系统收到最后一条数据后，经过
*forceTriggerTime* 时间，将强制触发未计算的窗口进行计算。

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

g.source("trades", `time`sym`volume, [TIMESTAMP, SYMBOL, INT])
.sessionWindowEngine(sessionGap = 5, metrics = <sum(volume)>, timeColumn = `time, keyColumn=`sym)
.sink("output")
g.submit()
go

n = 5
time = 2018.10.12T10:01:00.000 + (1..n)
sym = take(`A`B`C, n)
volume = (1..n) % 1000
tmp = table(time as time, sym as sym, volume as volume)
appendOrcaStreamTable("trades", tmp)

n = 5
time = 2018.10.12T10:01:00.010 + (1..n)
sym = take(`A`B`C, n)
volume = (1..n) % 1000
tmp = table(time as time, sym as sym, volume as volume)
appendOrcaStreamTable("trades", tmp)

n = 6
time = 2018.10.12T10:01:00.020 + 1 2 3 8 14 20
sym = take(`A`B`C, n)
volume = (1..n) % 1000
tmp = table(time as time, sym as sym, volume as volume)
appendOrcaStreamTable("trades", tmp)

select * from orca_table.output
```

| time | sym | volume |
| --- | --- | --- |
| 2018.10.12 10:01:00.001 | A | 5 |
| 2018.10.12 10:01:00.002 | B | 7 |
| 2018.10.12 10:01:00.003 | C | 3 |
| 2018.10.12 10:01:00.011 | A | 5 |
| 2018.10.12 10:01:00.012 | B | 7 |
| 2018.10.12 10:01:00.013 | C | 3 |
| 2018.10.12 10:01:00.021 | A | 1 |
| 2018.10.12 10:01:00.022 | B | 2 |
| 2018.10.12 10:01:00.023 | C | 3 |
