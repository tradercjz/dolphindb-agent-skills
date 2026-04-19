# DStream::crossSectionalEngine

首发版本：3.00.3

## 语法

`DStream::crossSectionalEngine(metrics, keyColumn,
[triggeringPattern='perBatch'], [triggeringInterval=1000], [useSystemTime=true],
[timeColumn], [lastBatchOnly=false], [contextByColumn], [roundTime=true],
[keyFilter])`

## 详情

创建流计算横截面引擎。参考：createCrossSectionalEngine。

## 参数

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考元编程。

* 计算指标可以是系统内置或用户自定义的函数，如 <[sum(qty), avg(price)]>；可以对计算结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可以对多列进行运算，如 <[std(price1-price2)]>。
* *metrics* 内支持调用具有多个返回值的函数，例如 <func(price) as `col1`col2>（可不指定列名）。
* *metrics* 中使用的列名大小写不敏感，不要求与输入表的列名大小写保持一致。

**keyColumn**
字符串标量或向量，指定流数据表中某列的值为横截面引擎的键值。横截面引擎的计算时，仅使用每个键值对应的最新一行记录。

**triggeringPattern**
字符串标量，表示触发计算的方式，每触发一次计算，输出一条结果到输出表。该字符串可选值如下：

* 'perBatch'：*triggeringPattern* 的默认值。每插入一次数据触发一次计算。
* 'perRow'：插入的每一行数据都会触发一次计算。
* 'interval'：基于系统时间间隔触发计算。
* 'keyCount'：若相同时间戳的数据分批次到达，则只有在当前时间戳的记录数达到
  *triggeringInterval*，或有更新时间戳的数据到达时，才会触发计算。使用该参数值时，必须指定
  *timeColumn*，且 *useSystemTime* = false。若设置
  *triggeringPattern* = 'keyCount'，收到的数据中出现的乱序数据会被丢弃，不参与计算。
* 'dataInterval'：基于数据时间间隔触发计算。使用该参数值时，必须指定 *timeColumn*，且指定
  *useSystemTime* = false。

**triggeringInterval** 整数或元组，触发计算规则如下：

* *triggeringPattern* 取值为 'interval' 时，*triggeringInterval*
  是一个正整数，表示触发计算的时间间隔，单位为毫秒，默认值为 1000。每经过 *triggeringInterval*
  指定的时间间隔，检查引擎中的数据是否被计算。若存在未被计算的数据，则触发一次计算。
* *triggeringPattern* 取值为 'keyCount' 时：
  + *triggeringInterval* 可以是一个整数。设置后，在更新的时间戳的数据到来前，当前时间戳的记录数需要累积到
    *triggeringInterval* 才会触发计算。
  + *triggeringInterval* 也可以是一个长度为 2 的
    元组。元组的第一个元素是整数，表示触发计算的最新时间戳的记录数量。元组的第二个值可以是整数或者 duration 类型数据。假设设置
    *triggeringInterval* = (c1, c2):
    - 当 c2 为整数时，若收到的最新时间戳 t1 的数据数量小于 c1，这批数据不会触发计算，系统可以继续缓存更新时间戳
      t2(t2>t1) 的数据，当 t2 的数据量达到 c2 或者收到更新的时间戳 t3(t3>t2)
      的数据时，会触发时间戳 t1 对应数据的计算。注意必须满足 c2 < c1。
    - 当 c2 为 duration 时，若收到的最新时间戳 t1 的数据数量小于
      c1，这批数据不会触发计算，系统收到更新的时间戳 t2(t2>t1) 的数据后，会等待 duration
      指定的时间，若在此期间继续收到了 t1 的数据且满足 t1 时间戳的数据总量达到 c1，或者在此期间又收到了更新的时间戳
      t3(t3>t2) 的数据，则直接触发 t1 对应数据的计算，等待时间结束后不再触发计算。否则，等待
      duration 设置的时间后才会触发 t1 数据的计算。
* *triggeringPattern* 取值为 'dataInterval' 时，*triggeringInterval*
  是一个正整数，单位和数据时间的单位一致，默认值为 1000。从第一条数据的时间戳开始一个窗口，窗口长度为
  *triggeringInterval*。一个窗口结束后到达的第一条数据会触发当前窗口内数据的计算输出。输出表的时间为窗口结束的时间戳。

**useSystemTime** 可选参数，布尔值，表示是否使用数据注入引擎时的系统时间作为计算参照的时间列。

* 若 *useSystemTime* = true，*outputTable* 中第一列（时间列）为系统时间；
* 若 *useSystemTime* = false，必须指定 *timeColumn*，*outputTable*
  中第一列（时间列）为数据的时间戳。

**timeColumn** 是一个字符串。当 *useSystemTime* = false
时，指定订阅的流数据表中时间列的名称。仅支持 TIMESTAMP 类型。

**lastBatchOnly** 可选参数。横截面引擎是否只保留最新时间戳上的数据。当
*lastBatchOnly* = true 时，只能指定 *triggeringPattern* =
'keyCount'，此时横截面引擎维护的键值表只保存最新时间戳的键值数据；否则，更新并保留所有时间戳上的键值数据。

**contextByColumn**
可选参数，字符串标量或向量。设置后，将对横截面引擎中数据按照指定的字段或字段组合分组，并在组内进行指定计算。

* 设置该参数，必须指定 *metrics* 和 *outputTable*.
* 如果 *metrics* 全为聚合函数，则分组计算结果和 groupby 分组计算结果一致，否则和 contextby
  分组计算结果一致。

**roundTime** 可选参数，布尔值。用于对第一个数据窗口的起始时间进行规整，仅在
*triggeringPattern*=dataInterval 时有效。系统将根据该参数、triggeringInterval
和时间精度来确定规整尺度（alignmentSize）。窗口规整规则同时序引擎。

**keyFilter** 可选参数，以元代码形式表示的过滤条件。过滤条件是一个表达式或者函数调用，应用于截面数据中的列（列值为
key），返回一个布尔向量。引擎会从截面数据中过滤出 key 满足条件的数据进行计算。

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
// dropStreamGraph('cs')

csGraph = createStreamGraph("cs")
csGraph.source("trade1", `time`sym`price`volume,[TIMESTAMP,SYMBOL,DOUBLE,INT])
  .crossSectionalEngine(metrics=<[avg(price), sum(volume), sum(price*volume), count(price)]>, keyColumn=`sym)
  .sink("cs_output")
csGraph.submit()
go

times=2020.08.12T09:30:00.000 + 123 234 456 678 890 901
syms=`A`B`A`B`B`A
prices=10 20 10.1 20.1 20.2 10.2
volumes=20 10 20 30 40 20
tmp=table(times as time, syms as sym, prices as price, volumes as volume)

appendOrcaStreamTable("trade1", tmp)

select * from orca_table.cs_output;
```
