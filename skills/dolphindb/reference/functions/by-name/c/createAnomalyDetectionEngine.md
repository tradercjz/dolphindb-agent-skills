# createAnomalyDetectionEngine

## 语法

`createAnomalyDetectionEngine(name, metrics, dummyTable,
outputTable, timeColumn, [keyColumn], [windowSize], [step], [garbageSize],
[roundTime=true], [snapshotDir], [snapshotIntervalInMsgCount],
[raftGroup],[anomalyDescription])`

## 详情

创建异常检测引擎，返回一个表对象，向该表写入数据意味着将数据注入异常检测引擎进行计算。异常检测引擎会根据异常指标，对每条记录进行检测。

异常检测引擎不支持在 *metrics* 中使用以下函数：`next`,
`talibNull`, `linearTimeTrend`,
`iterate`；亦不支持在序列相关函数内部嵌套聚合函数，如：`tmsum(sum())`。

为了便于观察和对比计算结果，系统会对第一个数据窗口的起始时间进行调整。调整规则与 createTimeSeriesEngine 相同。

更多流数据引擎的应用场景说明可以参考 流计算引擎。

## 计算规则

异常检测引擎会根据不同类型的异常指标采用不同的计算规则。异常指标一般有以下三种类型：

* 某个列与常量对比、列与列之间对比或非聚合函数中没有嵌套聚合函数，例如 qty < 4, qty > price, lt(qty,
  prev(qty)), isNull(qty) == false
  等。对于这类指标，异常检测引擎会对每一条数据进行计算，判断是否符合条件并决定输出。
* 聚合函数的结果与某个常量值对比、聚合函数结果之间的对比、非聚合函数中仅嵌套聚合函数和常量，例如 avg(qty - price) > 10,
  percentile(qty, 90) < 100, max(qty) < avg(qty) \* 2, le(sum(qty), 5)
  等。对于这类指标，异常检测引擎会在每个窗口计算时判断计算结果是否符合条件并决定输出。
* 聚合函数的结果与列对比、非聚合函数中同时嵌套聚合函数和列，例如 avg(qty) > qty, le(med(qty), price)
  等。对于这类指标，每当数据到达时，异常检测引擎会将数据与上一个计算窗口的聚合结果对比，判断计算结果是否符合条件并决定输出，直到触发下一次聚合计算。

注：

* 当指标中包含聚合函数，则必须指定窗口长度（由参数 *windowSize* 设置）和计算的时间间隔（由参数 *step*
  设置）。每隔一段时间，在固定长度的移动窗口中计算指标。为了便于观察和对比计算结果，系统会对第一个数据窗口的起始时间进行调整，起始窗口的规整规则同时间序列引擎。
* 乱序数据处理规则：
  + 如果需要聚合计算，输入流数据表中时间列（*timeColumn*）所指示的时间戳必须为非递减序列；如果同时指定了分组列（*keyColumn*），则按照分组分别进行计算，组内数据的时间戳必须为非递减序列。否则，乱序数据将被直接丢弃，不参与计算。
  + 如果不需要聚合计算，引擎可以接收乱序数据。

## 引擎的其它功能

* 支持数据/状态清理：若 *metrics*
  参数指定的指标中使用了聚合函数或序列相关函数，异常检测引擎会保留历史数据，可通过配置 *garbageSize*
  参数，使系统清理本次计算不需要的历史数据。若指定了 *keyColumn*，则各分组独立进行数据清理。
* 快照机制：启用快照机制之后，系统若出现异常，可及时将流数据引擎恢复到最新的快照状态。（详情请参考
  *snapshotDir* 和 *snapshotIntervalInMsgCount* 的参数说明）

## 参数

**name** 字符串标量，表示异常检测引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics** 以元代码或元组的格式表示异常指标，每个异常指标必须是布尔表达式，如<[sum(qty) >
5, avg(qty) > qty, qty < 4]>。有关元代码的更多信息可参考 元编程。

注：

*metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或分布式表。在调用
`createAnomalyDetectionEngine`
函数之前，需要预先设立输出表。异常检测引擎会将计算结果注入该表。

输出表的各列的顺序如下：

(1) 时间列。其数据类型与 *dummyTable* 的时间列一致，用于存放检测到异常的时间戳。

(2) 分组列。如果 *keyColumn* 不为空，则其后几列和 *keyColumn* 设置的列及其顺序保持一致。

(3) 之后两列分别为 INT类型列 type 和 STRING / SYMBOL 类型列 metric，分别用于记录异常的类型（在 *metrics*
中的下标）和异常条件的内容。

**timeColumn** 字符串标量，该参数用于指定订阅的流数据表中时间列的名称。

**keyColumn** 可选参数，字符串标量或向量，表示分组列名。异常检测引擎会按照 *keyColumn*
对输入的数据分组，计算将在各分组分别进行。

**windowSize** 可选参数，正整数。如果 *metrics* 中包含聚合函数，必须指定
*windowSize*，它表示计算的数据窗口的长度，数据窗口只包含上边界不包含下边界。如果 *metrics*
中不包含聚合函数，该参数无效。

**step** 可选参数，正整数。如果 *metrics* 中包含聚合函数，必须指定 *step*，并且必须能够被
*windowSize* 整除，它表示计算的时间间隔。如果 *metrics* 中不包含聚合函数，该参数无效。

**garbageSize** 可选参数，正整数。它是可选参数，默认值是 2,000（单位为行）。如果没有指定
*keyColumn*，当内存中历史数据的数量超过 *garbageSize* 时，系统会清理本次计算不需要的历史数据。如果指定了
*keyColumn*，意味着需要分组计算时，内存清理是各分组独立进行的。当一个组的历史数据记录数超出 *garbageSize*
时，会清理该组不再需要的历史数据。若一个组的历史数据记录数未超出 *garbageSize*，则该组数据不会被清理。如果 *metrics*
中没有聚合函数，这个参数不起作用。

**roundTime** 可选参数，布尔值，表示若数据时间精度为毫秒或者秒且 *step* > 一分钟，如何对窗口边界值进行规整处理。默认值为
true，表示按照既定的多分钟规则（见以上表格）进行规整。若为 false，则按一分钟规则（见以上表格）进行窗口规整（详情参考
`规整规则表`）。

若要开启快照机制 (snapshot)，必须指定 *snapshotDir* 与 *snapshotIntervalInMsgCount*。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
* 临时存储快照信息：文件名为 <engineName>.tmp；
* 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
* 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount** 可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**raftGroup** 是流数据高可用订阅端 raft 组的 ID (大于1的整数，由流数据高可用相关的配置项
*streamingRaftGroups* 指定)。设置该参数表示开启计算引擎高可用。在 leader 节点创建流数据引擎后，会同步在
follower 节点创建该引擎。每次保存的 snapshot 也会同步到 follower。当 raft 组的 leader 节点宕机时，会自动切换新 leader
节点重新订阅流数据表。请注意，若要指定 *raftGroup*，必须同时指定 *snapshotDir*。

注意，自 3.00.5
版本起，流计算引擎暂不支持高可用功能，*raftGroup* 参数将不生效。

**anomalyDescription** 可选参数，字符串向量，长度和 *metrics*
中定义的指标数量相同。指定该参数后，输出表的最后一列将显示异常条件对应的字符串。

## 返回值

一个表。

## 例子

例1. 下面的例子使用 `createAnomalyDetectionEngine` 函数创建了一个表
engine，然后通过订阅流数据表 trades 把数据写入到 engine 中，按照 sym 列进行分组聚合运算，并把结果保存在表 outputTable
中。

```
share streamTable(1000:0, `time`sym`qty, [TIMESTAMP, SYMBOL, INT]) as trades
share table(1000:0, `time`sym`type`metric, [TIMESTAMP, SYMBOL, INT, STRING]) as outputTable
engine = createAnomalyDetectionEngine(name="anomalyDetection1", metrics=<[sum(qty) > 5, avg(qty) > qty, qty < 4]>, dummyTable=trades, outputTable=outputTable, timeColumn=`time, keyColumn=`sym, windowSize=3, step=3)
subscribeTable(tableName="trades", actionName="anomalyDetectionSub1", offset=0, handler=append!{engine}, msgAsTable=true)

def writeData(n){
     timev = 2018.10.08T01:01:01.001 + 1..n
     symv =take(`A`B, n)
     qtyv = n..1
     insert into trades values(timev, symv, qtyv)
}

writeData(6);

select * from trades;
```

| time | sym | qty |
| --- | --- | --- |
| 2018.10.08T01:01:01.002 | A | 6 |
| 2018.10.08T01:01:01.003 | B | 5 |
| 2018.10.08T01:01:01.004 | A | 4 |
| 2018.10.08T01:01:01.005 | B | 3 |
| 2018.10.08T01:01:01.006 | A | 2 |
| 2018.10.08T01:01:01.007 | B | 1 |

```
select * from outputTable;
```

| time | sym | type | metric |
| --- | --- | --- | --- |
| 2018.10.08T01:01:01.003 | A | 0 | sum(qty) > 5 |
| 2018.10.08T01:01:01.004 | A | 1 | avg(qty) > qty |
| 2018.10.08T01:01:01.005 | B | 2 | qty < 4 |
| 2018.10.08T01:01:01.006 | A | 1 | avg(qty) > qty |
| 2018.10.08T01:01:01.006 | A | 2 | qty < 4 |
| 2018.10.08T01:01:01.006 | B | 0 | sum(qty) > 5 |
| 2018.10.08T01:01:01.007 | B | 1 | avg(qty) > qty |
| 2018.10.08T01:01:01.007 | B | 2 | qty < 4 |

下面详细解释异常检测引擎的计算过程：

(1) 指标 sum(qty) > 5 是聚合函数的结果与常量的对比，因此异常检测引擎会在每个窗口计算时进行检测。第一个数据窗口是
2018.10.08T01:01:01.000 到 2018.10.08T01:01:01.002，分别计算 A, B 的 sum(qty)，在
2018.10.08T01:01:01.003 时判断是否符合条件 sum(qty)>5，第二个数据窗口是 2018.10.08T01:01:01.003 到
2018.10.08T01:01:01.005，在 2018.10.08T01:01:01.006 时判断是否符合条件 sum(qty)>5，如此类推。

(2) 指标 avg(qty) > qty
是聚合函数的结果与某列对比，因此每当数据到达时，异常检测引擎会将数据与上一个计算窗口的聚合结果对比，判断计算结果是否符合条件并决定输出，直到触发下一次聚合计算。第一个数据窗口是
2018.10.08T01:01:01.000 到 2018.10.08T01:01:01.002，分别计算 A, B 的
avg(qty)，2018.10.08T01:01:01.003 到 2018.10.08T01:01:01.005 之间的 qty 会与上一个窗口的 avg(qty)
比较，2018.10.08T01:01:01.005 时窗口发生移动，第二个数据窗口为 2018.10.08T01:01:01.003 到
2018.10.08T01:01:01.005，此时计算 A, B 的 avg(qty)，2018.10.08T01:01:01.006 到
2018.10.08T01:01:01.008 之间的 qty 会与上一个窗口的 avg(qty) 比较，如此类推。

(3) 指标 qty < 4 是列与常量对比，因此每次数据进入时，异常检测引擎都会进行判断。

例2. 下例通过 *anomalyDescription* 参数指定输出的异常指标对应的文字信息

```
share streamTable(1000:0, `time`temp, [TIMESTAMP, DOUBLE]) as sensordata

share streamTable(1000:0, `time`anomalyType`anomalyString, [TIMESTAMP, INT, SYMBOL]) as outputTable
engine = createAnomalyDetectionEngine(name = "engineB", metrics=<[temp > 65, temp > percentile(temp, 75)]>, dummyTable = sensordata, outputTable = outputTable, timeColumn = `time, windowSize = 6, step = 3, anomalyDescription=["The temperature is higher than 65°C", "The temperature is larger than 75% values of the last window"])
subscribeTable(,tableName = "sensordata", actionName = "sensorAnomalyDetection", offset = 0, handler = append!{engine}, msgAsTable = true)

timev = 2018.10.08T01:01:01.001 + 1..10
tempv = 59 66 57 60 63 51 53 52 56 55
insert into sensordata values(timev, tempv)

sleep(10)
select * from outputTable
```

| time | anomalyType | anomalyString |
| --- | --- | --- |
| 2018.10.08T01:01:01.003 | 0 | The temperature is higher than 65°C |
| 2018.10.08T01:01:01.003 | 1 | The temperature is larger than 75% values of the last window |
| 2018.10.08T01:01:01.005 | 1 | The temperature is larger than 75% values of the last window |
| 2018.10.08T01:01:01.006 | 1 | The temperature is larger than 75% values of the last window |
