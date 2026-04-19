<!-- Auto-mirrored from upstream `documentation-main/tutorials/data_replay.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 数据回放

一个量化策略在用于实际交易时，处理实时数据的程序通常为事件驱动。而研发量化策略时，需要使用历史数据进行回测，这时的程序通常不是事件驱动。因此同一个策略需要编写两套代码，不仅耗时而且容易出错。在 DolphinDB 中，用户可将历史数据按照时间顺序以“实时数据”的方式导入流数据表中，这样就可以使用同一套代码进行回测和实盘交易。

DolphinDB 的流数据处理框架采用发布 - 订阅 - 消费的模式，数据持续地以流的形式发布给数据订阅者。订阅者收到消息以后，可使用自定义函数或者 DolphinDB 内置的流数据引擎来处理消息。DolphinDB 流数据接口支持多种语言的 API，包括 C++, C#, Java, 和 Python 等。用户可以使用这些 API 来编写更加复杂的处理逻辑，更好地与实际生产环境相结合。详细情况请参考DolphinDB 流数据教程。

## 1. 函数介绍

### 1.1. `replay`

```
replay(inputTables, outputTables, [dateColumn], [timeColumn], [replayRate], [absoluteRate=true], [parallelLevel=1])
```

`replay`函数的作用是将若干表或数据源同时回放到相应的输出表中。用户需要指定输入的数据表或数据源、输出表、日期列、时间列、回放速度以及并行度。

* inputTables: 单个表或包含若干表或数据源（见`replayDS`介绍）的元组。
* outputTables: 可以是单个表或包含若干个表的元组，表示共享的流数据表对象，也可以是字符或字符串，表示共享流数据表的名称。
* dateColumn 与 timeColumn: 字符串，表示输入表的日期和时间列，若均不指定则默认第一列为 dateColumn。若有 dateColumn，则该列必须为分区列之一；若无 dateColumn，则必须指定 timeColumn，且其必须为分区列之一。若输入表中时间列同时包含日期和时间，需要将 dateColumn 和 timeColumn 设为同一列。回放时，系统将根据 dateColumn 和 timeColumn 的设定，决定回放的最小时间精度。在此时间精度下，同一时刻的数据将在相同批次输出。举例来说，若 timeColumn 最小时间精度为秒，则每一秒的数据在统一批次输出；若只设置了 dateColumn，那么同一天的所有数据会在一个批次输出。
* replayRate: 整数，表示数据回放速度。若 absoluteRate 为 true，replayRate 表示每秒钟回放的数据条数。由于回放时同一个时刻数据在同一批次输出，因此当 replayRate 小于一个批次的行数时，实际输出的速率会大于 replayRate。若 absoluteRate 为 false，依照数据中的时间戳加速 replayRate 倍回放。若 replayRate 未指定或为负，以最大速度回放。
* absoluteRate 是一个布尔值。默认值为 true，表示 replayRate 为每秒回放的记录数。若为 false，表示依照数据中的时间戳加速 replayRate 倍回放。
* parallelLevel: 整数，表示读取数据的并行度。当源数据单个分区相对内存较大，或者超过内存时，需要使用`replayDS`函数将源数据划分为若干个小的数据源，依次从磁盘中读取数据并回放。参数 parallelLevel 指定同时读取这些经过划分之后的小数据源的线程数，可提升数据读取速度。

### 1.2. `replayDS`

```
replayDS(sqlObj, [dateColumn], [timeColumn], [timeRepartitionSchema])
```

`replayDS`函数可以将输入的 SQL 查询转化为数据源，结合`replay`函数使用。其作用是根据输入表的分区以及 timeRepartitionSchema，将原始的 SQL 查询按照时间顺序拆分成若干小的 SQL 查询。

* sqlObj: SQL 查询元代码，表示回放的数据，如 `select * from loadTable("dfs://source", "source")`。SQL 查询的表对象是 DFS 表，且至少有一个分区列为 DATE 类型。
* dateColumn: 字符串，表示日期列。若不指定，默认第一列为日期列。`replayDS`函数默认日期列是数据源的一个分区列，并根据分区信息将原始 SQL 查询拆分为多个查询。
* timeColumn: 字符串，表示时间列，配合 timeRepartitionSchema 使用。
* timeRepartitionSchema: TIME 或 NANOTIME 类型向量，如 08:00:00 .. 18:00:00。对 sqlObj 在每一个 dateColumn 分区中，在 timeColumn 维度上进一步拆分。

### 1.3. 单个内存表回放

单内存表回放只需要设置输入表、输出表、日期列、时间列和回放速度即可。

```
replay(inputTable, outputTable, `date, `time, 10)
```

### 1.4. 使用 data source 的单表回放

若数据表的行数过多，可使用`replayDS`函数将其划分为若干个小的数据源，再使用`replay`函数从磁盘中读取数据并回放，`replayDS`函数的返回值是一个向量，记录了划分出的多个 SQL 查询语句。`replay`内部实现使用了 pipeline 框架，取数据与输出分开执行。当`replayDS`函数的输出作为数据源时，多块数据可以并行读取，以避免输出线程等待的情况。此例中并行度设置为 2，表示有两个线程同时执行取数据的操作。

```
inputTable = loadTable("dfs://source", "source")
inputDS = replayDS(<select * from inputTable>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
replay(inputDS, outputTable, `date, `time, 1000, true, 2)
```

### 1.5. 多表回放

#### 1.5.1. N 对 N 多表回放

`replay`也支持多张表的同时回放，只需将多张输入表以元组的方式传入`replay`，并且分别指定输出表即可。这里输出表和输入表应当一一对应，每一对都必须有相同的表结构。如果指定了日期列或时间列，那么所有表中都应当存在相应的列。

```
ds1 = replayDS(<select * from input1>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
ds2 = replayDS(<select * from input2>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
ds3 = replayDS(<select * from input3>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
replay([ds1, ds2, ds3], [out1, out2, out3], `date, `time, 1000, true, 2)
```

#### 1.5.2. N 对一异构多表回放

1.30.17/2.00.5 及以上版本，`replay`增加了 N 对一异构模式的多表回放。它将多个具有不同表结构的数据源回放到同一个输出表中，这里的输出表必须为异构流数据表。N 对一异构模式的多表回放能够保证多表之间严格按照时间顺序进行回放，且后续对输出表进行订阅和处理时，也能够保证多个表数据之间严格按照时间顺序被消费。更详细的异构多表回放的功能介绍与应用案例见异构回放功能应用：股票行情回放教程。

```
ds1 = replayDS(<select * from input1>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
ds2 = replayDS(<select * from input2>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
ds3 = replayDS(<select * from input3>, `date, `time, 08:00:00.000 + (1..10) * 3600000)
replay([ds1, ds2, ds3], outputTable, `date, `time, 1000, true, 2)
```

### 1.6. 取消回放

如果`replay`函数是通过`submitJob`调用，可以使用`getRecentJobs`获取 jobId，然后用`cancelJob`取消回放。

```
getRecentJobs()
cancelJob(jobid)
```

如果`replay`函数是直接调用，可在另外一个 GUI session 中使用`getConsoleJobs`获取 jobId，然后使用`cancelConsoleJob`取消回放任务。

```
getConsoleJobs()
cancelConsoleJob(jobId)
```

## 2. 如何使用回放的数据

回放的数据以流数据形式存在，我们可以使用以下三种方式来订阅与消费这些数据：

* 在 DolphinDB 中订阅，使用 DolphinDB 脚本自定义回调函数来消费流数据。
* 在 DolphinDB 中订阅，使用内置的流计算引擎来处理流数据，譬如时间序列聚合引擎、横截面聚合引擎、异常检测引擎等。DolphinDB 内置的聚合引擎可以对流数据进行实时聚合计算，使用简便且性能优异。在 3.2 中，我们使用横截面聚合引擎来处理回放的数据，并计算 ETF 的内在价值。
* 第三方客户端通过 DolphinDB 的流数据 API 来订阅和消费数据。

## 3. 金融示例

### 3.1. 回放 level1 报价数据并计算 ETF 内在价值

本例中使用美国股市 2007 年 8 月 17 日的 level1 报价数据，执行`replayDS`函数进行数据回放，并通过 DolphinDB 内置的横截面聚合引擎计算 ETF 内在价值。数据存放在分布式数据库"dfs://TAQ"的 quotes 表，以下是 quotes 表的结构以及数据预览。

```
quotes = loadTable("dfs://TAQ", "quotes")
quotes.schema().colDefs;
```

| name | typeString | typeInt |
| --- | --- | --- |
| time | SECOND | 10 |
| symbol | SYMBOL | 17 |
| ofrsiz | INT | 4 |
| ofr | DOUBLE | 16 |
| mode | INT | 4 |
| mmid | SYMBOL | 17 |
| ex | CHAR | 2 |
| date | DATE | 6 |
| bidsize | INT | 4 |
| bid | DOUBLE | 16 |

```
select top 10 * from quotes where date=2007.08.17;
```

| symbol | date | time | bid | ofr | bidsiz | ofrsiz | mode | ex | mmid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 2007.08.17 | 04:15:06 | 0.01 | 0 | 10 | 0 | 12 | 80 |  |
| A | 2007.08.17 | 06:21:16 | 1 | 0 | 1 | 0 | 12 | 80 |  |
| A | 2007.08.17 | 06:21:44 | 0.01 | 0 | 10 | 0 | 12 | 80 |  |
| A | 2007.08.17 | 06:49:02 | 32.03 | 0 | 1 | 0 | 12 | 80 |  |
| A | 2007.08.17 | 06:49:02 | 32.03 | 32.78 | 1 | 1 | 12 | 80 |  |
| A | 2007.08.17 | 07:02:01 | 18.5 | 0 | 1 | 0 | 12 | 84 |  |
| A | 2007.08.17 | 07:02:01 | 18.5 | 45.25 | 1 | 1 | 12 | 84 |  |
| A | 2007.08.17 | 07:54:55 | 31.9 | 45.25 | 3 | 1 | 12 | 84 |  |
| A | 2007.08.17 | 08:00:00 | 31.9 | 40 | 3 | 2 | 12 | 84 |  |
| A | 2007.08.17 | 08:00:00 | 31.9 | 35.5 | 3 | 2 | 12 | 84 |  |

(1) 对要进行回放的数据进行划分。回放大量数据时，若将数据全部导入内存后再回放，可能导致内存不足。可先使用`replayDS`函数并指定参数 timeRepartitionSchema，将数据按照时间戳分为 60 个部分。

```
trs = cutPoints(09:30:00.000..16:00:00.000, 60)
rds = replayDS(<select * from quotes where date=2007.08.17>, `date, `time,  trs);
```

(2) 定义输出表 outQuotes 为流数据表。

```
sch = quotes.schema().colDefs
share streamTable(100:0, sch.name, sch.typeString) as outQuotes
```

(3) 定义 ETF 成分股票权重字典 weights 以及聚合函数 etfVal，用于计算 ETF 内在价值。为简化起见，本例使用了一个虚构的由 AAPL、IBM、MSFT、NTES、AMZN、GOOG 这 6 只股票组成的的 ETF。

```
defg etfVal(weights,sym, price) {
    return wsum(price, weights[sym])
}
weights = dict(STRING, DOUBLE)
weights[`AAPL] = 0.1
weights[`IBM] = 0.1
weights[`MSFT] = 0.1
weights[`NTES] = 0.1
weights[`AMZN] = 0.1
weights[`GOOG] = 0.5
```

(4) 创建流聚合引擎，并订阅数据回放的输出表 outQuotes。订阅 outQuotes 表时，我们指定过滤条件，只有 symbol 为 AAPL、IBM、MSFT、NTES、AMZN、GOOG 的数据才会发布到横截面聚合引擎，减少不必要的网络开销和数据传输。

```
setStreamTableFilterColumn(outQuotes, `symbol)
outputTable = table(1:0, `time`etf, [TIMESTAMP,DOUBLE])
tradesCrossAggregator=createCrossSectionalAggregator("etfvalue", <[etfVal{weights}(symbol, ofr)]>, outQuotes, outputTable, `symbol, `perBatch)
subscribeTable(tableName="outQuotes", actionName="tradesCrossAggregator", offset=-1, handler=append!{tradesCrossAggregator}, msgAsTable=true, filter=`AAPL`IBM`MSFT`NTES`AMZN`GOOG)
```

(5) 开始回放，设定每秒回放 10 万条数据，聚合引擎则会实时地对回放的数据进行消费。

```
submitJob("replay_quotes", "replay_quotes_stream", replay, rds, outQuotes, `date, `time, 100000, true, 4)
```

(6) 查看 ETF 内在价值。

```
//查看outputTable表内前15行的数据,其中第一列时间为聚合计算发生的时间
select top 15 * from outputTable;
```

| time | etf |
| --- | --- |
| 2019.06.04T16:40:18.476 | 14.749 |
| 2019.06.04T16:40:19.476 | 14.749 |
| 2019.06.04T16:40:20.477 | 14.749 |
| 2019.06.04T16:40:21.477 | 22.059 |
| 2019.06.04T16:40:22.477 | 22.059 |
| 2019.06.04T16:40:23.477 | 34.049 |
| 2019.06.04T16:40:24.477 | 34.049 |
| 2019.06.04T16:40:25.477 | 284.214 |
| 2019.06.04T16:40:26.477 | 284.214 |
| 2019.06.04T16:40:27.477 | 285.68 |
| 2019.06.04T16:40:28.477 | 285.68 |
| 2019.06.04T16:40:29.478 | 285.51 |
| 2019.06.04T16:40:30.478 | 285.51 |
| 2019.06.04T16:40:31.478 | 285.51 |
| 2019.06.04T16:40:32.478 | 285.51 |

## 4. 性能测试

以下对 DolphinDB database 的数据回放功能进行性能测试。测试服务器配置如下：

* 主机：DELL PowerEdge R730xd
* CPU：Intel Xeon(R) CPU E5-2650 v4（24 核 48 线程 2.20GHz）
* 内存：512 GB（32GB × 16, 2666 MHz）
* 硬盘：17T HDD（1.7T × 10, 读取速度 222 MB/s，写入速度210 MB/s）
* 网络：万兆以太网

测试脚本如下：

```
sch = quotes.schema().colDefs
trs = cutPoints(09:30:00.000..16:00:00.001,60)
rds = replayDS(<select * from quotes where date=2007.08.17>, `date, `time,  trs);
share streamTable(100:0, sch.name, sch.typeString) as outQuotes1
jobid = submitJob("replay_quotes","replay_quotes_stream",  replay,  [rds],  [`outQuotes1], `date, `time, , ,4)
```

在不设定回放速率（即以最快的速率回放），并且输出表没有任何订阅时，回放 331,204,031 条数据耗时仅需要 90~110 秒。
