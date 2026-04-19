# DStream::leftSemiJoinEngine

首发版本：3.00.3

## 语法

`DStream::leftSemiJoinEngine(rightStream, metrics, matchingColumn,
[garbageSize=5000], [updateRightTable=false])`

## 详情

创建流计算左半等值连接引擎。参考：createLeftSemiJoinEngine。

## 参数

**rightStream** DStream 对象，表示输入的右表数据源。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 Metaprogramming。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量。当指定为常量向量时，对应的输出列必须设置为数组向量类型，例子参见
  createReactiveStateEngine 中的例4。
* **metrics** 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。

  若在 *metrics* 指定了 *leftTable* 和
  *rightTable* 中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName"
  指定该列来自哪个表。

  注：

  *metrics*
  中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn** 表示连接列的字符串标量/向量或字符串向量组成的 tuple，支持 Integral,
Temporal 或 Literal(UUID 除外)类型。

1. 只有一个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym], [`timestamp,`sym1]]。

**garbageSize** 可选参数，正整数，默认值是 5,000（单位为行）。和其他连接引擎不同，该函数的
*garbageSize* 参数只用于清理左表的历史数据。当左表发生过 join 的记录数超过 *garbageSize*
时，系统会触发清理。

**updateRightTable** 可选参数，布尔值，默认为 false，表示右表存在多条相同
*matchingColumn* 的记录时，是保留第一条（false）还是最新一条记录（true）。

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

r = g.source("right", `time`sym1`vol, [TIMESTAMP, SYMBOL, INT])
g.source("left", `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
    .leftSemiJoinEngine(r, metrics=<[price, vol,price*vol]>, matchingColumn=[[`time,`sym], [`time,`sym1]], updateRightTable=true)
    .sink("output")
g.submit()

go

v = [1, 5, 10, 15]
tmp1=table(2012.01.01T00:00:00.000+v as time, take(`AAPL, 4) as sym, rand(100,4) as price)
appendOrcaStreamTable("left", tmp1)

v = [1, 1, 3, 4, 5, 5, 5, 15]
tmp2=table(2012.01.01T00:00:00.000+v as time, take(`AAPL, 8) as sym, rand(100,8) as vol)
appendOrcaStreamTable("right", tmp2)

select * from orca_table.output
```

| time | sym | price | vol | price\_mul |
| --- | --- | --- | --- | --- |
| 2012.01.01 00:00:00.001 | AAPL | 36 | 62 | 2,232 |
| 2012.01.01 00:00:00.005 | AAPL | 82 | 35 | 2,870 |
| 2012.01.01 00:00:00.015 | AAPL | 60 | 23 | 1,380 |
