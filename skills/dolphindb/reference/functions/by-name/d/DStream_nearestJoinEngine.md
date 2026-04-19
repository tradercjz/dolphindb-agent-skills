# DStream::nearestJoinEngine

首发版本：3.00.4，3.00.3.1

## 语法

`DStream::nearestJoinEngine(rightStream, kNearest, metrics, matchingColumn,
[timeColumn], [useSystemTime=false], [garbageSize = 5000], [maxDelayedTime],
[nullFill], [cachedTableCapacity=1024])`

## 详情

创建流计算最近邻关联引擎。参考：createNearestJoinEngine。

## 参数

**rightStream** DStream 对象，表示输入的右表数据源。

**kNearest** 一个正整数，表示记录的条数。对于每条左表记录，关联右表中时间戳不大于该记录时间戳的最近 k
条记录。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 元编程。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as `col1`col2>。

  若在 *metrics* 指定了 *leftTable* 和 *rightTable*
  中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName" 指定该列来自哪个表。
* 支持使用 `toArray` 函数将右表字段聚合为 array vector
  类型，例如：`<toArray(price)>`，其中 price 为右表中的普通列。

**注意：**

* *metrics* 中使用的列名大小写不敏感，不要求与输入表的列名大小写保持一致。
* 当以下函数只计算 *rightTable* 中的数据列时，最近邻关联引擎对它们进行了优化：sum, sum2, avg, std, var,
  corr, covar, wavg, wsum, beta, max, min, last, first, med, percentile。

**matchingColumn** 表示连接列的字符串标量/向量/tuple，支持 Integral, Temporal 或 Literal（UUID
除外）类型。*matchingColumn* 指定规则为：

1. 只有一个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则 *matchingColumn*
   = [[`timestamp, `sym], [`timestamp,`sym1]]。

**timeColumn** 可选参数，当 *useSystemTime* =
false时，指定要连接的两个表中时间列的名称。*leftTable* 和 *rightTable*
时间列名称可以不同，但数据类型需保持一致。当 *leftTable* 和 *rightTable*
时间列名称不同时，*timeColumn* 为一个长度为2的字符串向量。

**useSystemTime** 可选参数，表示 *outputTable* 中第一列（时间列）为系统当前时间（*useSystemTime*
= true）或左表的时间列（*useSystemTime* = false）。

**garbageSize** 可选参数，是正整数，默认值是5,000（单位为行）。随着订阅的流数据不断积累进入 window join
引擎，存放在内存中的数据会越来越多，这时需要清理不再需要的历史数据。当左/右两表各个分组内的数据行数超过 *garbageSize*
值时，系统会清理本次计算不需要的历史数据。

**maxDelayedTime** 可选参数，是正整数，用于触发引擎中长时间未输出的分组数据进行计算。
具体来说，若`(某个分组中未发生计算的窗口右边界) + (maxDelayedTime) <
(右表最新收到的任意一个分组数据的时间戳)`，则这条数据会触发该窗口计算输出。

**注：** 请合理设置 *maxDelayedTime* 参数。当左表数据较少而右表数据频率较高时，若 *maxDelayedTime*
设置过小，系统可能在未触发某些分组计算之前，就清理掉右表中过早的数据。

**nullFill** 和输出表列字段等长且类型一一对应的元组，用于填充以下列中的空值：输出表中包含的左表列、右表列、右表列被聚合计算后的计算结果列。

**cachedTableCapacity** 可选参数，为正整数，表示引擎为每个不同的分组分别创建的左缓存表和右缓存表的初始容量（以数据条数计）。默认值为
1024。

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
// dropStreamGraph('nearestEngine')
g = createStreamGraph('nearestEngine')

leftStream = g.source("leftTable", `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
rightStream  = g.source("rightTable", `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE])
leftStream.nearestJoinEngine(rightStream=rightStream,kNearest=8, metrics=<[price,toArray(val),sum(val)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=NULL)
		.sink("output")
g.submit()
go

n=10
tp2=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(double(1..10),2*n) as val)
tp2.sortBy!(`time)
appendOrcaStreamTable(`rightTable, tp2)
tp1=table(take(2012.01.01T00:00:00.003+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(NULL join rand(10.0, n-1),2*n) as price)
tp1.sortBy!(`time)

appendOrcaStreamTable(`leftTable, tp1)

select * from orca_table.output
```

| time | sym | price | toArray\_val | sum\_val |
| --- | --- | --- | --- | --- |
| 2012.01.01 00:00:00.003 | A |  | [1, 2, 3, 4] | 10 |
| 2012.01.01 00:00:00.004 | A | 3.4822947595856824 | [1, 2, 3, 4, 5] | 15 |
| 2012.01.01 00:00:00.005 | A | 7.86139521284484 | [1, 2, 3, 4, 5, 6] | 21 |
| 2012.01.01 00:00:00.006 | A | 3.1722617468716185 | [1, 2, 3, 4, 5, 6, 7] | 28 |
| 2012.01.01 00:00:00.007 | A | 5.3532539582956415 | [1, 2, 3, 4, 5, 6, 7, 8] | 36 |
| 2012.01.01 00:00:00.008 | A | 6.732663744145904 | [2, 3, 4, 5, 6, 7, 8, 9] | 44 |
| 2012.01.01 00:00:00.003 | B | 3.4822947595856824 | [2, 3, 4, 5] | 14 |
| 2012.01.01 00:00:00.004 | B | 7.86139521284484 | [2, 3, 4, 5, 6] | 20 |
| 2012.01.01 00:00:00.005 | B | 3.1722617468716185 | [2, 3, 4, 5, 6, 7] | 27 |
| 2012.01.01 00:00:00.006 | B | 5.3532539582956415 | [2, 3, 4, 5, 6, 7, 8] | 35 |
