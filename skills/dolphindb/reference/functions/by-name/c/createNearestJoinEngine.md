# createNearestJoinEngine

首发版本：3.00.4，3.00.3.1

## 语法

`createNearestJoinEngine(name, leftTable, rightTable, outputTable, kNearest,
metrics, matchingColumn, [timeColumn], [useSystemTime=false], [garbageSize =
5000], [maxDelayedTime], [nullFill], [cachedTableCapacity=1024], [snapshotDir],
[snapshotIntervalInMsgCount])`

## 详情

创建流计算最近邻关联引擎。引擎接收的左表和右表以 *matchingColumn*
指定的连接列分组，并在每个组内进行匹配。对于每个分组中每条左表数据，实时关联右表中时间戳不晚于该记录的最近 k 条记录，并基于这些记录计算并输出结果。

注：

不支持乱序处理机制，用户需要自行保证输入的数据有序。

## 参数

**name**
表示引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**leftTable** 表对象。可以不包含数据，但结构必须与输入的流数据表相同。

**rightTable** 表对象。可以不包含数据，但结构必须与输入的流数据表相同。

**outputTable** 计算结果的输出表。引擎会将计算结果注入该表。输出表的各列的顺序如下：

1. 时间列。其中：

   * 若 *useSystemTime* = true，为 TIMESTAMP
     类型；
   * 若 *useSystemTime* = false，数据类型与
     *timeColumn* 列一致。
2. 连接列。与 *matchingColumn* 中的列以及其顺序一致，可为多列。
3. 计算结果列。可为多列。

**kNearest** 一个正整数，表示记录的条数。对于每条左表记录，关联右表中时间戳不大于该记录时间戳的最近 k
条记录。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 元编程。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如
  <func(price) as `col1`col2>。

  若在 *metrics* 指定了 *leftTable* 和
  *rightTable* 中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName"
  指定该列来自哪个表。
* 在需要输出 array vector
  类型结果时，需要显式指定`toArray`函数转换类型，例如：`<toArray(price)>`，其中
  price 为右表中的普通列。
* 支持使用 `toColumnarTuple` 函数，将非聚合计算结果转换为列式元组（columnar
  tuple）。

**注意：**

* *metrics* 中使用的列名大小写不敏感，不要求与输入表的列名大小写保持一致。
* 当以下函数只计算 *rightTable* 中的数据列时，最近邻关联引擎对它们进行了优化：sum,
  sum2, avg, std, var, corr, covar, wavg, wsum, beta, max, min, last,
  first, med, percentile。

**matchingColumn** 表示连接列的字符串标量/向量/tuple，支持 Integral, Temporal 或
Literal（UUID 除外）类型。*matchingColumn* 指定规则为：

1. 只有一个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串标量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 sym，右表连接列名为 sym1，则 *matchingColumn* =
   [[`sym],[`sym1]]。
2. 有多个连接列：当左表和右表的连接列名相同时，*matchingColumn* 是一个字符串向量，否则是一个长度为 2 的
   tuple，例如：左表连接列名为 timestamp, sym，右表连接列名为 timestamp, sym1，则
   *matchingColumn* = [[`timestamp, `sym], [`timestamp,`sym1]]。

**timeColumn** 可选参数，当 *useSystemTime* = false
时，指定要连接的两个表中时间列的名称。*leftTable* 和 *rightTable* 时间列名称可以不同，但数据类型需保持一致。当
*leftTable* 和 *rightTable* 时间列名称不同时，*timeColumn*
为一个长度为2的字符串向量。

**useSystemTime**
可选参数，表示 *outputTable* 中第一列（时间列）为系统当前时间（*useSystemTime* =
true）或左表的时间列（*useSystemTime* = false）。

**garbageSize** 可选参数，是正整数，默认值是5,000（单位为行）。随着订阅的流数据不断积累进入 window
join 引擎，存放在内存中的数据会越来越多，这时需要清理不再需要的历史数据。当左/右两表各个分组内的数据行数超过 *garbageSize*
值时，系统会清理本次计算不需要的历史数据。

**maxDelayedTime** 可选参数，是正整数，用于触发引擎中长时间未输出的分组数据进行计算。 具体来说，若`(某个分组中的左表数据时间戳)
+ (maxDelayedTime) < (右表最新收到的任意一个分组数据的时间戳)`，则这条数据会触发关联计算。

注：

指定该参数时，必须同时指定 *timeColumn*，且两者的单位需一致。默认值为3秒，根据 *timeColumn* 的精度换算。例如，若
*timeColumn* 的精度是毫秒，则默认值为3000毫秒。

注：

请合理设置 *maxDelayedTime* 参数。当左表数据较少而右表数据频率较高时，若
*maxDelayedTime* 设置过小，系统可能在未触发某些分组计算之前，就清理掉右表中过早的数据。

**nullFill**
和输出表列字段等长且类型一一对应的元组，用于填充以下列中的空值：输出表中包含的左表列、右表列、右表列被聚合计算后的计算结果列。

**cachedTableCapacity**可选参数，为正整数，表示引擎为每个不同的分组分别创建的左缓存表和右缓存表的初始容量（以数据条数计）。默认值为 1024。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了
  *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
* 临时存储快照信息：文件名为 <engineName>.tmp；
* 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
* 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount**
可选参数，正整数，表示每隔多少条数据保存一次流数据引擎快照。

## 返回值

一个表。

## 例子

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE]) as rightTable
share table(100:0, `time`sym`factor1`factor2`factor3, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE[], DOUBLE]) as output

nullFill= [2012.01.01T00:00:00.000, `NONE, 0.0, [], 0.0]

njEngine=createNearestJoinEngine(name="test1", leftTable=leftTable, rightTable=rightTable, outputTable=output,  kNearest=8, metrics=<[price,toArray(val),sum(val)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false,nullFill=nullFill)

subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{njEngine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{njEngine, false}, msgAsTable=true)

n=10

tp2=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(double(1..n),2*n) as val)
tp2.sortBy!(`time)
rightTable.append!(tp2)

tp1=table(take(2012.01.01T00:00:00.003+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(NULL join rand(10.0, n-1),2*n) as price)
tp1.sortBy!(`time)
leftTable.append!(tp1)

tp2=table(take(2012.01.01T00:00:00.010+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(double(1..n),2*n) as val)
tp2.sortBy!(`time)
rightTable.append!(tp2)

select * from output
```

| time | sym | factor1 | factor2 | factor3 |
| --- | --- | --- | --- | --- |
| 2012.01.01 00:00:00.003 | A | 0 | [1, 2, 3, 4] | 10 |
| 2012.01.01 00:00:00.004 | A | 8.049739237951693 | [1, 2, 3, 4, 5] | 15 |
| 2012.01.01 00:00:00.005 | A | 6.31845193685475 | [1, 2, 3, 4, 5, 6] | 21 |
| 2012.01.01 00:00:00.006 | A | 0.01247286192106635 | [1, 2, 3, 4, 5, 6, 7] | 28 |
| 2012.01.01 00:00:00.007 | A | 8.373015887228414 | [1, 2, 3, 4, 5, 6, 7, 8] | 36 |
| 2012.01.01 00:00:00.008 | A | 4.636610761119452 | [2, 3, 4, 5, 6, 7, 8, 9] | 44 |
| 2012.01.01 00:00:00.003 | B | 8.049739237951693 | [2, 3, 4, 5] | 14 |
| 2012.01.01 00:00:00.004 | B | 6.31845193685475 | [2, 3, 4, 5, 6] | 20 |
| 2012.01.01 00:00:00.005 | B | 0.01247286192106635 | [2, 3, 4, 5, 6, 7] | 27 |
| 2012.01.01 00:00:00.006 | B | 8.373015887228414 | [2, 3, 4, 5, 6, 7, 8] | 35 |
| 2012.01.01 00:00:00.007 | B | 4.636610761119452 | [2, 3, 4, 5, 6, 7, 8, 9] | 44 |
| 2012.01.01 00:00:00.008 | B | 7.700075873220435 | [3, 4, 5, 6, 7, 8, 9, 10] | 52 |
| 2012.01.01 00:00:00.009 | B | 0.5831421500989946 | [3, 4, 5, 6, 7, 8, 9, 10] | 52 |
| 2012.01.01 00:00:00.009 | A | 7.700075873220435 | [3, 4, 5, 6, 7, 8, 9, 10] | 52 |
| 2012.01.01 00:00:00.010 | A | 0.5831421500989946 | [4, 5, 6, 7, 8, 9, 10, 1] | 50 |
| 2012.01.01 00:00:00.011 | A | 5.117162734418752 | [5, 6, 7, 8, 9, 10, 1, 2] | 48 |
| 2012.01.01 00:00:00.012 | A | 8.823084861596655 | [6, 7, 8, 9, 10, 1, 2, 3] | 46 |
| 2012.01.01 00:00:00.010 | B | 5.117162734418752 | [5, 6, 7, 8, 9, 10, 1, 2] | 48 |
| 2012.01.01 00:00:00.011 | B | 8.823084861596655 | [6, 7, 8, 9, 10, 1, 2, 3] | 46 |
| 2012.01.01 00:00:00.013 | B | 0 | [8, 9, 10, 1, 2, 3, 4, 5] | 42 |
