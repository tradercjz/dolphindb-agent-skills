# DStream::equalJoinEngine

首发版本：3.00.3

## 语法

`DStream::equalJoinEngine(rightStream, metrics, matchingColumn, timeColumn,
[garbageSize=5000], [maxDelayedTime])`

## 详情

创建流计算等值连接引擎。参考：createEquiJoinEngine。

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

**timeColumn** 字符串标量或向量。用于指定 *leftTable* 和
*rightTable* 中时间列的名称。两表的时间列名称可以不同，但数据类型需保持一致。当 *leftTable* 和
*rightTable* 时间列名称相同时，*timeColumn* 是字符串标量，否则，*timeColumn*
是长度为2的字符串向量。

**garbageSize** 可选参数，正整数，默认值是 5,000（单位为行）。当内存中历史数据行数超过
*garbageSize* 时，会清理本次计算不需要的历史数据。

1. 历史数据中已经 join 并输出的数据；
2. 历史数据未发生 join 的数据，但其时间戳与 *leftTable* 或 *rightTable* 收到的最新数据的时间戳的差值大于
   *maxDelayedTime*。

**maxDelayedTime** 可选参数，正整数，单位同 *timeColumn* 精度一致，默认值为 3
秒。该参数仅在达到 *garbageSize* 清理条件时才会起效，表示引擎内能够保留最新多长时间的数据。详情参考上述清理条件 2。不建议设置
*maxDelayedTime* 值设置过小，否则可能导致一些需关联却没及时关联的数据被清理。

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
// dropStreamGraph('joinEngine')
g = createStreamGraph('joinEngine')
r = g.source("right", `time`sym`val, [SECOND, SYMBOL, DOUBLE])
g.source("left", `time`sym`price, [SECOND, SYMBOL, DOUBLE])
    .equalJoinEngine(r, [<price>, <val>, <price*val>], `sym, `time)
    .sink("output")
g.submit()

go

tmp1=table(13:30:10+1..20 as time, take(`AAPL, 10) join take(`IBM, 10) as sym, double(1..20) as price)
appendOrcaStreamTable("left", tmp1)

tmp2=table(13:30:10+1..20 as time, take(`AAPL, 10) join take(`IBM, 10) as sym, double(50..31) as val)
appendOrcaStreamTable("right", tmp2)

select * from orca_table.output
```
