# createAsofJoinEngine

## 语法

`createAsofJoinEngine(name, leftTable, rightTable,
outputTable, metrics, matchingColumn, [timeColumn], [useSystemTime=false],
[delayedTime], [garbageSize], [sortByTime], [outputElapsedMicroseconds=false], [snapshotDir],
[snapshotIntervalInMsgCount])`

## 详情

创建流数据 asof join 引擎。返回一个左、右两表 asof join 后的表对象。注入 asof join
引擎的左、右两表将以 `matchingColumn` + `timeColumn` (或系统时间)
作为连接列，在右表中选取与连接列匹配的，在给定的左表时间戳前且最接近的记录。该引擎适用于两个数据源没有完全匹配的记录，需要按时间段作连接，以获取最新信息的场景。

注：

asof join 左表和右表的数据必须按照时间顺序排序。

* 如果没有指定
  `delayedTime`，则当右表数据的最新时间大于左表数据的最新时间，才会触发 join,
  计算输出。
* 如果指定了
  `delayedTime`，则当左表中数据最新时间与上一条未计算的时间差大于
  *delayedTime* 设置值，或者左表中数据在经过 2 \* *delayedTime*
  （小于2秒按2秒计算）后还没有 join 输出，就直接触发左右两表 join。

更多流数据引擎的应用场景说明可以参考 流计算引擎。

## 参数

**name** 字符串标量，表示 asof join 引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**leftTable** 和 **rightTable** 表对象。结构必须与输入的的流数据表相同。从
2.00.11 版本开始左、右表支持 array vector 类型。

**outputTable** 计算结果的输出表，可以是内存表或分布式表。从 2.00.11 版本开始输出表支持
array vector 类型。在使用 `createAsofJoinEngine`
函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。asof join 引擎会将计算结果注入该表。输出表的各列的顺序如下：

1. 时间列。其中：
   * 若 *useSystemTime* = true，为 TIMESTAMP 类型；
   * 若 *useSystemTime* = false，数据类型与 *timeColumn* 列一致。
2. 连接列。与 *matchingColumn* 中的列以及其顺序一致，可为多列。
3. 计算结果列。可为多列。
4. 耗时列。如果指定 *outputElapsedMicroseconds* = true，则指定一个 LONG
   类型的列用于记录单次响应计算耗时（单位：微秒）。
5. batchSize 列。如果指定 *outputElapsedMicroseconds* = true, 则指定一个 INT
   类型的列，记录单次响应的数据条数。

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

**outputElapsedMicroseconds** 布尔值，表示是否输出数据的单次响应计算耗时（从触发计算的数据注入引擎到计算完成的耗时），默认为
false。指定参数 *outputElapsedMicroseconds* 后，在定义 *outputTable* 时需要在计算结果列后增加一个
LONG 类型的列和 INT 类型的列，详见 *outputTable* 参数说明。

若要开启快照机制 (snapshot)，必须指定 *snapshotDir* 与
*snapshotIntervalInMsgCount*。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
* 临时存储快照信息：文件名为 <engineName>.tmp；
* 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
* 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount**
可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

## 返回值

一个表。

## 例子

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades
share streamTable(1:0, `time`sym`bid`ask, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE]) as quotes
share table(100:0, `time`sym`price`bid`ask`spread, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE]) as prevailingQuotes

ajEngine=createAsofJoinEngine(name="aj1", leftTable=trades, rightTable=quotes, outputTable=prevailingQuotes, metrics=<[price, bid, ask, abs(price-(bid+ask)/2)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false)
tmp1=table(2020.08.27T09:30:00.000+2 8 20 22 23 24 as time, take(`A`B, 6) as sym, 20.01 20.04 20.07 20.08 20.4 20.5 as price)
tmp2=table(2020.08.27T09:30:00.000+1 5 6 11 19 20 21 as time, take(`A`B, 7) as sym, 20 20.02 20.03 20.05 20.06 20.6 20.4 as bid,  20.01 20.03 20.04 20.06 20.07 20.5 20.6 as ask)
tmp1.sortBy!(`time)
tmp2.sortBy!(`time)

subscribeTable(tableName="trades", actionName="joinLeft", offset=0, handler=appendForJoin{ajEngine, true}, msgAsTable=true)
subscribeTable(tableName="quotes", actionName="joinRight", offset=0, handler=appendForJoin{ajEngine, false}, msgAsTable=true)

trades.append!(tmp1)
quotes.append!(tmp2)

sleep(100)
select time, sym, bid from prevailingQuotes
```

| time | sym | bid |
| --- | --- | --- |
| 2020.08.27T09:30:00.002 | A | 20 |
| 2020.08.27T09:30:00.020 | A | 20.06 |
| 2020.08.27T09:30:00.008 | B | 20.02 |

```
// 清理引擎及变量
unsubscribeTable(tableName="trades", actionName="joinLeft")
unsubscribeTable(tableName="quotes", actionName="joinRight")
undef(`trades,SHARED)
undef(`quotes,SHARED)
dropAggregator(name="aj1")

// 定义引擎，设置 sortByTime=true
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades
share streamTable(1:0, `time`sym`bid`ask, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE]) as quotes
share table(100:0, `time`sym`price`bid`ask`spread, [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE]) as prevailingQuotes
ajEngine=createAsofJoinEngine(name="aj1", leftTable=trades, rightTable=quotes, outputTable=prevailingQuotes, metrics=<[price, bid, ask, abs(price-(bid+ask)/2)]>, matchingColumn=`sym, timeColumn=`time, useSystemTime=false, sortByTime=true)

tmp1=table(2020.08.27T09:30:00.000+2 8 20 22 23 24 as time, take(`A`B, 6) as sym, 20.01 20.04 20.07 20.08 20.4 20.5 as price)
tmp2=table(2020.08.27T09:30:00.000+1 5 6 11 19 20 21 as time, take(`A`B, 7) as sym, 20 20.02 20.03 20.05 20.06 20.6 20.4 as bid,  20.01 20.03 20.04 20.06 20.07 20.5 20.6 as ask)
tmp1.sortBy!(`time)
tmp2.sortBy!(`time)
// 只能使用 appendForJoin 插入数据
subscribeTable(tableName="trades", actionName="joinLeft", offset=0, handler=appendForJoin{ajEngine, true}, msgAsTable=true)
subscribeTable(tableName="quotes", actionName="joinRight", offset=0, handler=appendForJoin{ajEngine, false}, msgAsTable=true)

trades.append!(tmp1)
quotes.append!(tmp2)

sleep(100)
// 查看结果表，数据按照全局时间顺序输出
select time, sym, bid from prevailingQuotes
```

| time | sym | bid |
| --- | --- | --- |
| 2020.08.27T09:30:00.002 | A | 20 |
| 2020.08.27T09:30:00.008 | B | 20.02 |
| 2020.08.27T09:30:00.020 | A | 20.06 |
