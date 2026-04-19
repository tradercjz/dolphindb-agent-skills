# createThresholdEngine

首发版本：3.00.3

## 语法

`createThresholdEngine(name, threshold, metrics, dummyTable, outputTable,
thresholdColumn, [keyColumn], [timeColumn], [sessionBegin], [sessionEnd],
[keyPurgeDaily=false], [forceTriggerSessionEndTime=0], [snapshotDir],
[snapshotIntervalInMsgCount], [outputElapsedMicroseconds=false],
[outputThreshold=false])`

## 详情

创建阈值引擎，以实现基于累计值阈值触发的聚合计算，每当阈值列（*thresholdColumn*）的累计值达到特定阈值（*threshold\**n）时，进行一次聚合计算：

* 若指定 *keyColumn* 进行分组，则聚合计算将在各分组内独立进行。
* 若指定 *sessionBegin* 和 *sessionEnd*，则仅有 [sessionBegin, sessionEnd]
  范围内的数据会参与计算。

## 参数

**name** 字符串标量，表示阈值引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**threshold** 正整数标量，表示阈值步长。

**metrics** 以元代码的格式表示计算指标，支持输入元组。有关元代码的更多信息可参考 元编程。

* 计算指标可以是一个或多个系统内置或用户自定义的聚合函数（使用 defg 关键字定义），如
  <[sum(volume), avg(price)]>；可以对聚合结果使用表达式，如
  <[avg(price1)-avg(price2)]>；也可对列与列的计算结果进行聚合计算，如
  <[std(price1-price2)]>。
* *metrics* 内支持调用具有多个返回值的函数，例如 <func(price) as
  `col1`col2>（可不指定列名）。
* 支持指定为一个常量标量或向量，例如 <1>，<[1, 2, 3]> 。当指定为常量向量时，对应的输出列必须设置为数组向量类型。
* 若 *windowSize* 为向量， *windowSize* 每个值可对应
  *metrics* 中多个计算指标。例如，*windowSize* 为[10,20]时，metrics可为
  (<[min(volume), max(volume)]>, <sum(volume)>)。
  *metrics* 也可以嵌套输入元组向量。例如：[[<[min(volume), max(volume)]>,
  <sum(volume)>], [<avg(volume)>]]

  注：

  + *metrics* 中使用的列名大小写不敏感，不需要与输入表的列名大小写保持一致。
  + *metrics* 中不可使用嵌套聚合函数。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable**计算结果的输出表，可以是内存表或分布式表。在使用`createThresholdEngine`函数之前，需要将输出表预先设立为一个空表，并指定各列列名以及数据类型。阈值引擎会将计算结果插入该表。

输出表的列顺序如下：

1. 时间列。如果指定了 *timeColumn*，则输出表中时间列与 *timeColumn*
   数据类型一致，用于记录触发引擎计算的数据时间。
2. 分组列。如果指定了 *keyColumn*，则输出表中分组列和 *keyColumn* 设置的列的类型和顺序保持一致。
3. 阈值窗口值列。如果指定 *outputThreshold*=true，则指定一个 LONG 类型的列用于记录触发计算的阈值窗口右边界的值。
4. thresholdColumn 累计和列。如果指定*outputThreshold*=true，则指定一个 DOUBLE
   类型的列记录触发计算时，*thresholdColumn* 的累计和。
5. 耗时列。如果指定 *outputElapsedMicroseconds*=true，则指定一个 LONG
   类型的列用于存储耗时（单位：微秒）。
6. 计算结果列。可为多列。

**keyColumn** 可选参数，字符串标量或向量，表示分组列名。若设置，则分组进行聚合计算。

**timeColumn** 可选参数，字符串标量或向量，用于指定订阅的流数据表中时间列的名称。

* 注：字符串向量必须是 date 和 time 组成的向量，date 类型为 DATE，time 类型为 TIME, SECOND 或
  NANOTIME。此时，输出表第一列的时间类型必须与 concatDateTime(date, time) 的类型一致。

**sessionBegin** 可选参数，可以是与时间列的数据类型对应的 SECOND、TIME 或 NANOTIME
类型的标量或向量，表示每个时间段的起始时刻。如果 *sessionBegin* 是一个向量，它必须是递增的。

**sessionEnd** 可选参数，可以是与时间列的数据类型对应的 SECOND、TIME 或 NANOTIME
类型的标量或向量，表示每个时间段的结束时刻。可在 *sessionEnd* 中指定 00:00:00 表示的次日的零点（即当日的 24:00:00）。

**keyPurgeDaily** 可选参数，是一个布尔值。默认值为
true，表示引擎在收到第一批包含新日期的数据时，先清空之前保存的所有分组，再对这批新数据进行处理。若设置为 false，则引擎不会清理前一天的分组。

**forceTriggerSessionEndTime** 可选参数，非负整数，单位与 timeColumn 的时间精度一致，默认值为 0。若
sessionEnd
时刻对应的窗口数据长时间未发生计算，通过该参数可以设置系统经过多少时间后触发计算并输出。若设置为0，表示不会通过这种方式触发计算。

注：

**注：**
当系统时间达到 sessionEnd + forceTriggerSessionEndTime 时触发计算，因此该参数在回放场景下不适用。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：
  + 临时存储快照信息：文件名为 <engineName>.tmp；
  + 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
  + 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount** 可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**outputElapsedMicroseconds** 可选参数，布尔标量，表示是否输出每个窗口从触发计算到计算完成输出结果的耗时（若指定了
*keyColumn* 则包含数据分组的耗时），默认为 false。指定参数 *outputElapsedMicroseconds*
后，在定义 *outputTable* 时需要在时间列和分组列后增加一个 LONG 类型的列，详见 *outputTable* 参数说明。

**outputThreshold** 可选参数，布尔标量，表示是否输出阈值窗口值和 *thresholdColumn* 累计和。

## 返回值

一个表对象，通过向该表对象写入，将数据注入阈值引擎进行计算。

## 例子

**例1** 通过时序聚合引擎计算1分钟 K 线，然后通过 createThresholdEngine 将 1 分钟 K 线聚合为 5
分钟。在窗口左闭右开的情况下，可以提前一分钟结束窗口并计算输出，从而比使用 createTimeSeriesEngine 减少延时。

```
// 准备数据
n = 1000000;
sampleDate = 2019.11.07;
symbols = `600519`000001`600000`601766;
trade = table(take(sampleDate, n) as date,
	(09:30:00.000 + rand(7200000, n/2)).sort!() join (13:00:00.000 + rand(7200000, n/2)).sort!() as time,
	rand(symbols, n) as symbol,
	100+cumsum(rand(0.02, n)-0.01) as price,
	rand(1000, n) as volume)

// 创建dummyTable, outputTable
share(streamTable(10:0,`date`time`symbol`price`volumn,[DATE, TIME, SYMBOL, DOUBLE, DOUBLE]), `trades);
share(table(1:0, `timestamp`symbol`open`high`low`close, [TIMESTAMP,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE]), `outputTable);
go
// 创建阈值引擎
thresholdEngine = createThresholdEngine(name="demo", threshold=1000000, metrics=<[first(price), max(price), min(price), last(price)]>, dummyTable=trades, outputTable=outputTable, thresholdColumn=`volumn, keyColumn=`symbol, timeColumn=[`date, `time]);

// 插入数据
thresholdEngine.append!(trade);

// 查询计算结果
select * from outputTable
```

部分结果如下：

| timestamp | symbol | open | high | low | close |
| --- | --- | --- | --- | --- | --- |
| 2019.11.07 09:31:54.986 | 000001 | 99.98404977017083 | 100.52950904161203 | 99.56823161885143 | 100.5279260600172 |
| 2019.11.07 09:33:51.890 | 000001 | 100.51835866520182 | 100.92578917419537 | 100.49741881850642 | 100.70077057819347 |
| 2019.11.07 09:35:48.298 | 000001 | 100.71148486480116 | 100.787968895277 | 99.84565304366406 | 100.61527177638374 |
| 2019.11.07 09:37:49.058 | 000001 | 100.61627630640287 | 101.55438607632183 | 100.48305282644462 | 101.33690219670534 |
| 2019.11.07 09:39:44.562 | 000001 | 101.32348716112786 | 101.55176323080435 | 100.74830873960164 | 100.77029377058614 |
| 2019.11.07 09:41:38.118 | 000001 | 100.78262700690422 | 101.24037498458289 | 100.67253582042176 | 100.7765302780131 |

**例2** 通过 *sessionBegin* 和 *sessionEnd* 限定只处理交易时段内的数据。

```
// 准备数据
t = table(
    2024.01.02 2024.01.02 2024.01.02 2024.01.02 2024.01.02 as date,
    09:20:00.000 09:31:00.000 10:15:00.000 11:35:00.000 13:05:00.000 as time,
    `A`A`A`A`A as sym,
    10.1 10.2 10.3 10.4 10.5 as price,
    200 500 600 700 800 as volume
)
```

| date | time | sym | price | volume |
| --- | --- | --- | --- | --- |
| 2024.01.02 | 09:20:00.000 | A | 10.1 | 200 |
| 2024.01.02 | 09:31:00.000 | A | 10.2 | 500 |
| 2024.01.02 | 10:15:00.000 | A | 10.3 | 600 |
| 2024.01.02 | 11:35:00.000 | A | 10.4 | 700 |
| 2024.01.02 | 13:05:00.000 | A | 10.5 | 800 |

```
// 创建 dummyTable, outputTable
share(streamTable(10:0, `date`time`sym`price`volume, [DATE, TIME, SYMBOL, DOUBLE, DOUBLE]), `trades1)
share(table(10:0, `timestamp`sym`sumVol, [TIMESTAMP, SYMBOL, DOUBLE]), `outputTable1)
go
// 创建阈值引擎
engine = createThresholdEngine(
    name="thresholdDemo1",
    threshold=1000,
    metrics=<[sum(volume)]>,
    dummyTable=trades1,
    outputTable=outputTable1,
    thresholdColumn=`volume,
    keyColumn=`sym,
    timeColumn=[`date, `time],
    sessionBegin=09:30:00.000 13:00:00.000,
    sessionEnd=11:30:00.000 15:00:00.000
)

// 插入数据
engine.append!(t)

// 查询结果
select * from outputTable1
```

| timestamp | sym | sumVol |
| --- | --- | --- |
| 2024.01.02 10:15:00.000 | A | 1,100 |

09:20:00.000 和 11:35:00.000 的数据不在 [sessionBegin, sessionEnd] 指定的交易时段内，不参与阈值累计。

**例3** 通过 *keyPurgeDaily* 控制跨日后是否清空前一日分组状态

```
// 创建 dummyTable, outputTable
share(streamTable(10:0, `date`time`sym`price`volume, [DATE, TIME, SYMBOL, DOUBLE, DOUBLE]), `trades)
share(table(10:0, `timestamp`sym`sumVol, [TIMESTAMP, SYMBOL, DOUBLE]), `output1)
share(table(10:0, `timestamp`sym`sumVol, [TIMESTAMP, SYMBOL, DOUBLE]), `output2)
go
// keyPurgeDaily=true：跨日后清空前一日分组状态
engine1 = createThresholdEngine(
    name="thresholdDemo2_true",
    threshold=1000,
    metrics=<[sum(volume)]>,
    dummyTable=trades,
    outputTable=output1,
    thresholdColumn=`volume,
    keyColumn=`sym,
    timeColumn=[`date, `time],
    keyPurgeDaily=true
)

// keyPurgeDaily=false：跨日后保留前一日分组状态
engine2 = createThresholdEngine(
    name="thresholdDemo2_false",
    threshold=1000,
    metrics=<[sum(volume)]>,
    dummyTable=trades,
    outputTable=output2,
    thresholdColumn=`volume,
    keyColumn=`sym,
    timeColumn=[`date, `time],
    keyPurgeDaily=false
)

// 准备数据
t = table(
    2024.01.02 2024.01.03 2024.01.03 as date,
    14:59:00.000 09:31:00.000 09:31:01.000 as time,
    `A`A`A as sym,
    10.1 10.2 10.3 as price,
    600 500 700 as volume
)

// 插入数据
engine1.append!(t)
engine2.append!(t)

// 查询结果
select * from output1
```

| timestamp | sym | sumVol |
| --- | --- | --- |
| 2024.01.02 14:59:00.000 | A | 600 |
| 2024.01.03 09:31:01.000 | A | 1,200 |

```
select * from output2
```

| timestamp | sym | sumVol |
| --- | --- | --- |
| 2024.01.03 09:31:00.000 | A | 1,100 |

**例4** 通过 outputElapsedMicroseconds 输出每次触发计算的耗时

```
// 创建 dummyTable, outputTable
share(streamTable(10:0, `date`time`sym`price`volume, [DATE, TIME, SYMBOL, DOUBLE, DOUBLE]), `trades)
share(table(10:0, `timestamp`sym`elapsed`avgPrice`sumVol, [TIMESTAMP, SYMBOL, LONG, DOUBLE, DOUBLE]), `outputTable)
go
// 创建阈值引擎
engine = createThresholdEngine(
    name="thresholdDemo4",
    threshold=1000,
    metrics=<[avg(price), sum(volume)]>,
    dummyTable=trades,
    outputTable=outputTable,
    thresholdColumn=`volume,
    keyColumn=`sym,
    timeColumn=[`date, `time],
    outputElapsedMicroseconds=true
)

// 准备数据
t = table(
    2024.01.02 2024.01.02 2024.01.02 as date,
    09:31:00.000 09:32:00.000 09:33:00.000 as time,
    `A`A`A as sym,
    10.1 10.2 10.3 as price,
    300 400 500 as volume
)

// 插入数据
engine.append!(t)

// 查询结果
select * from outputTable
```

| timestamp | sym | elapsed | avgPrice | sumVol |
| --- | --- | --- | --- | --- |
| 2024.01.02 09:33:00.000 | A | 1 | 10.2 | 1,200 |

**例5** 通过 *outputThreshold* 输出阈值窗口值和 *thresholdColumn* 累计和

```
// 创建 dummyTable, outputTable
share(streamTable(10:0, `date`time`sym`price`volume, [DATE, TIME, SYMBOL, DOUBLE, DOUBLE]), `trades)
share(table(10:0, `timestamp`sym`thresholdValue`cumThreshold`lastPrice, [TIMESTAMP, SYMBOL, LONG, DOUBLE, DOUBLE]), `outputTable)
go
// 创建阈值引擎
engine = createThresholdEngine(
    name="thresholdDemo5",
    threshold=1000,
    metrics=<[last(price)]>,
    dummyTable=trades,
    outputTable=outputTable,
    thresholdColumn=`volume,
    keyColumn=`sym,
    timeColumn=[`date, `time],
    outputThreshold=true
)

// 准备数据
t = table(
    2024.01.02 2024.01.02 2024.01.02 as date,
    09:31:00.000 09:32:00.000 09:33:00.000 as time,
    `A`A`A as sym,
    10.1 10.2 10.3 as price,
    300 400 500 as volume
)

// 插入数据
engine.append!(t)

// 查询结果
select * from outputTable
```

| timestamp | sym | thresholdValue | cumThreshold | lastPrice |
| --- | --- | --- | --- | --- |
| 2024.01.02 09:33:00.000 | A | 1,000 | 1,200 | 10.3 |
