# DStream::asofJoinEngine

首发版本：3.00.3

## 语法

`DStream::asofJoinEngine(rightStream, metrics, matchingColumn, [timeColumn],
[useSystemTime=false], [delayedTime], [garbageSize], [sortByTime])`

## 详情

创建流计算 asof join 引擎。参考：createAsofJoinEngine。

## 参数

**rightStream** DStream 对象，表示输入的右表数据源。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 Metaprogramming。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量，但不能是聚合函数。当指定为常量向量时，对应的输出列必须设置为数组向量类型，例子参见
  createReactiveStateEngine 中的例4。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。若在 *metrics* 指定了 *leftTable* 和 *rightTable*
  中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName" 指定该列来自哪个表。

  注：

  *metrics*
  中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn** 表示连接列的字符串标量/向量/字符串组成的 tuple，支持 Integral,
Temporal 或 Literal（UUID 除外）类型。*matchingColumn* 指定规则为：

1. 只有一个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 orderNo, sym，右表连接列名为 orderNo, sym1，则 *matchingColumn* =
   [[`orderNo, `sym], [`orderNo,`sym1]]。

**timeColumn** 可选参数，字符串标量或向量。当 *useSystemTime* = false
时，指定要连接的两个表中时间列的名称。 *leftTable* 和 *rightTable* 时间列名称可以不同，但数据类型需保持一致。当
*leftTable* 和 *rightTable* 时间列名称不同时，*timeColumn*
为一个长度为2的字符串向量。

**useSystemTime** 可选参数，布尔值。表示是否使用数据注入引擎时的系统时间作为时间列进行计算。

* 当 *useSystemTime* = true
  时，按照数据进入引擎的时刻（毫秒精度的本地系统时间，与数据中的时间列无关）进行计算。
* 当 *useSystemTime* = false（缺省值）时，按照数据中的时间列进行计算。

**delayedTime** 可选参数，正整数，单位同 timeColumn
精度一致。表示左表中未联结数据被触发联结并计算输出的最大等待时间。要设置 *delayedTime*， 必须指定
*timeColumn*，更多介绍见详情。

**garbageSize** 可选参数，正整数，默认值是 5,000（单位为行）。随着订阅的流数据不断注入 asof
join 引擎，存放在内存中的数据会越来越多，当各分组对应的缓存表（左表或右表）中数据行数超过 *garbageSize*
值时，系统会清理该表中已经触发计算的历史数据。

**sortByTime** 布尔值，表示是否按全局时间顺序输出数据。默认值为
false，表示不按全局时间输出数据，仅在组内按时间顺序输出数据。

注：

当设置
*sortByTime* = true 时，必须保证输入的左表和右表的数据分别全局有序，且不可设置
*delayedTime*。

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
// dropStreamGraph('asofJoin')

g = createStreamGraph('asofJoin')
r = g.source("right", `time`sym`bid`ask, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE])
g.source("left", `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
    .asofJoinEngine(r, <[price, bid, ask, abs(price-(bid+ask)/2)]>, `sym, `time)
    .sink("output")
g.submit()
go

tmp1=table(2024.08.27T09:30:00.000+2 8 20 22 23 24 as time, take(`A`B, 6) as sym, 20.01 20.04 20.07 20.08 20.4 20.5 as price)
tmp1.sortBy!(`time)
appendOrcaStreamTable("left", tmp1)

tmp2=table(2024.08.27T09:30:00.000+1 5 6 11 19 20 21 as time, take(`A`B, 7) as sym, 20 20.02 20.03 20.05 20.06 20.6 20.4 as bid,  20.01 20.03 20.04 20.06 20.07 20.5 20.6 as ask)
appendOrcaStreamTable("right", tmp2)

select * from orca_table.output
```

| time | sym | price | bid | ask | abs |
| --- | --- | --- | --- | --- | --- |
| 2024.08.27 09:30:00.002 | A | 20.01 | 20.00 | 20.01 | 0.004999999999999005 |
| 2024.08.27 09:30:00.020 | A | 20.07 | 20.06 | 20.07 | 0.005000000000002558 |
| 2024.08.27 09:30:00.008 | B | 20.04 | 20.02 | 20.03 | 0.015000000000000568 |
