# DStream::snapshotJoinEngine

首发版本：3.00.3

## 语法

`DStream::snapshotJoinEngine(rightStream, metrics, matchingColumn,
[timeColumn], [keepLeftDuplicates=false], [keepRightDuplicates=false],
[isInnerJoin=true])`

## 详情

创建流计算快照连接引擎。参考：createSnapshotJoinEngine。

## 参数

**rightStream** DStream 对象，表示输入的右表数据源。

**metrics**：以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 Metaprogramming。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数，但不能是聚合函数。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。
* 若在 *metrics* 指定了 *leftTable* 和 *rightTable*
  中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName" 指定该列来自哪个表。

  **注：**
  *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**matchingColumn：**表示连接列的字符串标量/向量或字符串向量组成的 tuple，支持 Integral,
Temporal 或 Literal(UUID 除外)类型。*matchingColumn* 指定规则：

1. 只有一个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列。当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple。例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym],
   [`timestamp,`sym1]]。

**timeColumn:** 字符串标量或向量，可选参数。用于指定 leftTable 和 rightTable
中时间列的名称。两表的时间列名称可以不同，但数据类型需保持一致。当 leftTable 和 rightTable 时间列名称相同时，timeColumn
是字符串标量，否则，timeColumn 是长度为2的字符串向量。

**keepLeftDuplicates**：布尔值，可选参数，表示在进行右连接时，是否匹配左表各分组内的所有数据。

* 若设置为 false（默认值）：仅匹配左表各分组内的最新一条数据。
* 若设置为 true：匹配左表各分组内的所有数据。

**keepRightDuplicates**：布尔值，可选参数，表示在进行左连接时，是否保留右表各分组内的所有数据。

* 若设置为 false（默认值）：仅匹配右表各分组内的最新一条数据。
* 若设置为 true：匹配右表各分组内的所有数据。

**isInnerJoin：**布尔值，可选参数，表示是否进行内连接。

* 若设置为 true（默认值）：进行内连接，只有左右两表匹配的记录被计算输出。
* 若设置为 false：进行左连接或右连接，保留两个表中的所有记录。对于左右两表中匹配的记录进行计算，而未匹配的记录输出空值。

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
r = g.source("right", `timestamp`sym2`id`price`qty, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE])
g.source("left", `timestamp`sym1`id`price`val, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE])
    .snapshotJoinEngine(r, metrics=[<val*10>, <qty>], matchingColumn = [["id","sym1"],["id","sym2"]],
timeColumn = `timestamp, isInnerJoin=true, keepLeftDuplicates=true,keepRightDuplicates=true)
    .sink("output")
g.submit()
go

timestamp = 2024.10.10T15:12:01.507+1..10
sym = take(["a","b","c","d"],10)
id = [1,1,2,1,5,2,4,4,1,4]
price = [2.53,7.61,8.07,7.87,7.29,9.39,5.98,9.49,9.20,9.17]
val = [101,108,101,109,104,100,108,100,107,104]
tmp1 = table(timestamp as timestamp,sym as sym1,id as id,price as price,val as val)
appendOrcaStreamTable("left", tmp1)

id = [1,2,4,3,5,5,4,2,5,5]
price =  [1.08,9.08,9.97,7.60,1.91,6.77,7.81,8.81,0.61,5.92]
qty =  [208,200,203,202,204,201,206,207,205,205]
tmp2 = table(timestamp as timestamp,sym as sym2,id as id,price as price,qty as qty)
appendOrcaStreamTable("right", tmp2)

select * from orca_table.output
```

| id | sym1 | timestamp | right\_timestamp | val\_mul | qty |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 2024.10.10 15:12:01.508 | 2024.10.10 15:12:01.508 | 1,010 | 208 |
| 1 | a | 2024.10.10 15:12:01.512 | 2024.10.10 15:12:01.512 | 1,040 | 204 |
| 2 | a | 2024.10.10 15:12:01.512 | 2024.10.10 15:12:01.516 | 1,040 | 205 |
| 3 | b | 2024.10.10 15:12:01.513 | 2024.10.10 15:12:01.509 | 1,000 | 200 |
| 4 | c | 2024.10.10 15:12:01.514 | 2024.10.10 15:12:01.510 | 1,080 | 203 |
| 5 | c | 2024.10.10 15:12:01.514 | 2024.10.10 15:12:01.514 | 1,080 | 206 |
| 6 | a | 2024.10.10 15:12:01.516 | 2024.10.10 15:12:01.508 | 1,070 | 208 |
