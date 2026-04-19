# DStream::lookupJoinEngine

首发版本：3.00.3

## 语法

`DStream::lookupJoinEngine(rightStream, metrics, matchingColumn,
[rightTimeColumn], [checkTimes], [keepDuplicates=false])`

## 详情

创建流计算 lookup join 引擎。参考：createLookupJoinEngine。

## 参数

**rightStream** DStream 对象，表示输入的右表数据源。

**metrics** 可选参数，以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 Metaprogramming。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量，但不能是聚合函数。当指定为常量向量时，对应的输出列必须设置为数组向量类型，例子参见
  createReactiveStateEngine 中的例4。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。
* 若在 *metrics* 指定了 *leftTable* 和 *rightTable*
  中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName" 指定该列来自哪个表。

  注：

  *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn** 可选参数，表示连接列的字符串标量/向量或字符串向量组成的 tuple，支持
Integral, Temporal 或 Literal(UUID 除外)类型。*matchingColumn* 指定规则：

1. 只有一个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym], [`timestamp,`sym1]]。

**rightTimeColumn**
可选参数，是字符串标量，表示右表的时间列名称。若设置该参数，右表会根据指定的时间列的时间戳保留最新的数据（若有多行，则取其中最后一行）。若不指定该参数，则根据数据注入系统的时间保留最新数据。

**checkTimes** 可选参数，是一个时间类型向量或 DURATION 的标量。设置后，系统会定时更新
*rightTable* 的数据（只保留 *rightTable* 的最新数据），并将更新后的数据追加到引擎中。当无需更新
*rightTable* 时，则不用设置该参数，但需要在引擎创建后，手动将 *rightTable* 注入到引擎中。

* *checkTimes* 是时间类型向量时，只能为SECOND、TIME 或 NANOTIME 类型。 lookup join
  引擎每天根据向量内各元素指定的时间定时更新右表。
* *checkTimes* 是 DURATION 标量时，表示更新右表的时间间隔。

**keepDuplicates** 可选参数，布尔值，表示是否保留右表各分组内的所有数据。默认值为
false，即在关联时只取右表各分组内的最新一条数据。当设置为 true
时，在关联时则使用右表各分组内的所有数据，此时的连接类型为内连接，即只有左右两表匹配的记录被计算输出。

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

r = g.source("right", `timestamps`sym`val`id, [TIMESTAMP, SYMBOL, DOUBLE, INT])
g.source("left", `timestamps`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
    .lookupJoinEngine(r, metrics=<[price,val,price*val]>, matchingColumn=`sym)
    .sink("output")
g.submit()

go
n  = 15
tmp1 = table( (2018.10.08T01:01:01.001 + 1..12) join (2018.10.08T01:01:01.001 + 1..3)as timestamps,take(`A`B`C, n) as sym,take(1..15,n) as val,1..15 as id)
appendOrcaStreamTable("right", tmp1)

n = 10
tmp2 = table( 2019.10.08T01:01:01.001 + 1..n as timestamps,take(`A`B`C, n) as sym,take(0.1+10..20,n) as price)
appendOrcaStreamTable("left", tmp2)

select * from orca_table.output
```

| sym | price | val | price\_mul |
| --- | --- | --- | --- |
| A | 10.1 | 13 | 131.30 |
| B | 11.1 | 14 | 155.40 |
| C | 12.1 | 15 | 181.50 |
| A | 13.1 | 13 | 170.30 |
| B | 14.1 | 14 | 197.40 |
| C | 15.1 | 15 | 226.50 |
| A | 16.1 | 13 | 209.30 |
| B | 17.1 | 14 | 239.40 |
| C | 18.1 | 15 | 271.50 |
| A | 19.1 | 13 | 248.30 |
