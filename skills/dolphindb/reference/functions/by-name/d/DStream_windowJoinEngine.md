# DStream::windowJoinEngine

首发版本：3.00.3

## 语法

`DStream::windowJoinEngine(rightStream, window, metrics, matchingColumn,
[timeColumn], [useSystemTime=false], [garbageSize], [maxDelayedTime],
[nullFill], [sortByTime], [closed])`

## 详情

创建流计算窗口连接引擎。参考：createWindowJoinEngine 。

**注意：**Orca 中的输出表会自动推断列类型：

* window = 0:0（特殊窗口）：对于非聚合结果，默认推断为 array vector；若结果类型不支持 array
  vector，则自动转换为列式元组（columnar tuple）。
* window ≠ 0:0（普通窗口）：必须显式指定 `toArray`，结果才会输出为 array vector。

## 参数

**rightStream** DStream 对象，表示输入的右表数据源。

**window** 必选参数，表示滑动窗口区间的整型或 DURATION 数据对，其中左右边界都包含在内。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 元编程。

* 计算指标可以是一个或多个表达式、系统内置或用户自定义函数。
* *metrics* 内支持调用具有多个返回值的函数，且必须指定列名，例如 <func(price) as
  `col1`col2>。

  若在 *metrics* 指定了 *leftTable* 和
  *rightTable* 中具有相同名称的列，默认取左表的列，可以通过 "tableName.colName"
  指定该列来自哪个表。

  注：

  + *metrics* 中使用的列名大小写不敏感，不要求与输入表的列名大小写保持一致。
  + 在需要输出 array vector 类型结果时，需要显式指定 `toArray`
    函数转换类型。
  + 支持使用 `toColumnarTuple`
    函数，将非聚合计算结果转换为列式元组（columnar tuple）。
  + 当以下函数只计算 *rightTable* 中的数据列时，window join 引擎对它们进行了优化：sum,
    sum2, avg, std, var, corr, covar, wavg, wsum, beta, max, min,
    last, first, med, percentile。

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

**maxDelayedTime** 可选参数，是正整数，用于触发引擎中长时间未输出的分组数据进行计算。
具体来说，若`(某个分组中未发生计算的窗口右边界) + (maxDelayedTime) <
(右表最新收到的任意一个分组数据的时间戳)`，则这条数据会触发该窗口计算输出。

**nullFill**
和输出表列字段等长且类型一一对应的元组，用于填充以下列中的空值：输出表中包含的左表列、右表列、右表列被聚合计算后的计算结果列。

**sortByTime** 布尔值，表示是否按全局时间顺序输出数据。默认值为
false，表示不按全局时间输出数据，仅在组内按时间顺序输出数据。注意：当设置 sortByTime=true 时，必须保证输入的左表和右表的数据全局有序，且不可设置
*maxDelayedTime*。

**closed** 字符串，用于确定窗口边界的开闭情况，仅当 *window*为 0:0 时有效 。可选值为 ‘left’ 或 ‘right’，默认值为 ‘left’。

* closed = ‘left’： 窗口左闭右开。
* closed = ‘right’： 窗口左开右闭。此时必须设置 useSystemTime=false 。

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

r = g.source("right", `time`sym`val, [TIMESTAMP, SYMBOL, DOUBLE])
g.source("left", `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE])
    .windowJoinEngine(r, window=-2:2, metrics=<[price,val,sum(val)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false,nullFill=[2012.01.01T00:00:00.000, `NONE, 0.0, 0.0, 0.0])
    .sink("output")
g.submit()

go

n=10
tp1=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(NULL join rand(10.0, n-1),2*n) as price)
tp1.sortBy!(`time)
appendOrcaStreamTable("left", tp1)

tp2=table(take(2012.01.01T00:00:00.000+0..10, 2*n) as time, take(`A, n) join take(`B, n) as sym, take(double(1..n),2*n) as val)
tp2.sortBy!(`time)
appendOrcaStreamTable("right", tp2)

select * from orca_table.output
```
