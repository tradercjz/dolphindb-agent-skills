<!-- Auto-mirrored from upstream `documentation-main/plugins/amdquote/amdquote.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# amdQuote

华锐高速行情平台（Archforce Market Data）简称 AMD，是华锐提供的超高可用、超低时延的优质行情服务。DolphinDB 提供了 amdQuote 系列插件用于接收华锐 AMD 的极速行情数据，将实时行情数据便捷地接入 DolphinDB。

amdQuote 系列插件基于华锐提供的 AMD SDK 进行开发，通过实现行情的回调接口获取数据。目前支持实时获取逐笔成交委托、股票债券基金以及期货期权快照等多种品类的数据。目前，DolphinDB 根据 AMD SDK 的不同版本，分别提供以下插件：amdQuote396，amdQuote398，amdQuote401，amdQuote420，amdQuote430，amdQuote455，amdQuote457。

## 安装插件

### 版本要求

DolphinDB Server：2.00.10 及更高版本，支持 Linux x86-64, Linux JIT, Linux ABI。其中，分别支持的 AMD SDK 版本为：

* Linux X86-64：3.9.6、3.9.8、4.0.1、4.2.0、4.3.0、4.5.5、4.5.7
* Linux X86-64 ABI=1：3.9.8

在使用插件时请选择低于行情源版本的插件，否则将无法接收数据。比如行情源版本为 4.0.1，则需选择 DolphinDB amdQuote401、amdQuote398 或者 amdQuote396 插件。

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   amdQuote 插件目前支持多个版本的华锐 AMD SDK，需要选择适用于 AMD SDK 版本的插件。

   以适配华锐 AMD SDK 4.0.1 版本的 amdQuote 插件为例：

   ```
   installPlugin("amdQuote401")
   ```
3. 使用 `loadPlugin` 命令加载插件。此处的插件名为 amdQuote+版本号，例如 amdQuote401：

   ```
   loadPlugin("amdQuote401")
   ```

## 接口说明

### connect

**语法**

```
amdQuote::connect(username, password, host, port, [option], [dataVersion='ORIGIN'])
```

**详情**

创建一个和 AMD 行情服务器之间的连接，返回一个句柄。

注意：如果当前已有一个 amdQuote 连接并且尚未调用 `close` 进行关闭，如果再次以完全相同的参数进行调用，则不会重新进行连接，而会直接返回已有连接的 handle。如果参数指定不同，则会报错，无法新建连接。此时如果需要获取已有的 AMD 行情连接句柄需要调用 `getHandle` 函数。

**参数**

**username** STRING 类型标量，AMD 行情服务器的用户名。

**password** STRING 类型标量，AMD 行情服务器的密码。

**host** STRING 类型向量，AMD 行情服务器 IP 列表，需要和端口列表数量相同。

**port** 为整型向量，AMD 行情服务器端口列表，需要和 IP 列表数量相同。

**option** 可选参数。是字典类型，表示扩展参数。当前支持 ReceivedTime, OutputElapsed, DailyIndex, StartTime。
其中：

* ReceivedTime 表示是否获取插件收到行情数据的时间戳。其指定为 dict(["ReceivedTime"], [true]) 时，getSchema 获取的表结构中将包含插件收到行情数据的时间戳列。
* OutputElapsed 表示是否获取 amdQuote 插件接收数据处理的时延。其指定为 dict(["OutputElapsed"], [true]) 时，`getSchema` 获取的表结构中将包含插件收到行情数据的时延列。

  时延的定义：'amd 回调函数返回数据' 到 '准备开始 transform' 处理，或准备 append 到共享流表前’ 这段时间。
* DailyIndex 表示是否添加每天按 channel\_no 递增的数据列，仅对 order 和 execution 类型的行情数据有效，其他类型该列均为空值。其指定为 dict(["DailyIndex"], [true]) 时，getSchema 获取的表结构中将包含插件收到行情数据的按 channel\_no 递增的列。如果订阅的时间超过了 StartTime（默认为 `8:40:00.0000`），则置为空值。具体 StartTime 的含义见 StartTime 条目。
* StartTime 表示每天计算的 dailyIndex 起始的时间，默认为 8:40:00.0000 。其指定为 dict(["StartTime"], [true]) 时，如果执行 `amdQuote::subscribe` 的服务器时间小于 StartTime，则当日的 dailyIndex 都为空值，进入第二天则从头计数，不置为空值。

**dataVersion** 可选参数，为 STRING 类型标量，默认为 "ORIGIN"。还可以指定为 "4.0.1"，此时，接收数据表的 schema 对齐于华锐 4.0.1 版本 SDK 的字段。当接收 order、bondOrder 或 bondSnapshot 类型数据时，如果指定 dataVersion 为 "4.0.1" 而非 "ORIGIN"，在 schema 中会多出一些字段。

```
注意，版本号不低于 4.0.1 的插件，即 amdQuote401 及以上版本才能 dataVersion="4.0.1"。
```

### query

**语法**

```
amdQuote::query(handle, dataType, market, channelNo, beginSeqNum, endSeqNum, [option])
```

**详情**

查询当天数据，返回一个表，表的字段类型和 amdQuote::getSchema 一致。由于 AMD SDK 有限制，查询条数不能超过 1000 条，既 endSeqNum - beginSeqNum 必须少于 1000。仅 amdQuote455 和 amdQuote457 插件支持该接口。

**参数**

**handle** `connect` 接口返回的句柄。

**dataType** STRING 类型标量，表示行情的类型。目前只支持 “orderExecution”，基金股票逐笔成交合并。

**market** 整型标量。表示市场类型。上交所 是 101，深交所是 102。

**channelNo** 整型标量。表示需要查询的逐笔数据的通道号。

**beginSeqNum** 整型标量，表示需要查询的逐笔数据的起始序号。必须大于等于 1。

**endSeqNum** 整型标量，表示需要查询的逐笔数据的结束序号。必须大于等于 beginSeqNum 。

**option** 可选参数，一个字典，表示扩展参数，类型为<STRING, ANY>。支持如下参数：

* "Timeout" 表示超时时间，单位为分钟。其值为整型，取值范围为 1- 60，默认值为 1。

### subscribe

**语法**

```
amdQuote::subscribe(handle, dataType, outputTable, market, [codeList], [transform], [seqCheckMode=1], [queueDepth=100000])
```

**详情**

订阅指定市场、行情数据类型和股票列表的行情数据到目标表中。

**参数**

**handle** `connect` 接口返回的句柄。

**dataType** STRING 类型标量，表示行情的类型。可取值详见附录的行情类型对照表。

注意，由于上交所部分债券申购数据会被当作现货交易，所以如果订阅了上交所基金，对应的输出表会有部分债券数据混入。因此如果需要将股债基明确落入不同的库表，建议订阅时将股票基金债券的订阅写入一张表中，下游通过流订阅进行分派写入。

**outputTable** 如果 *dataType* 的类型不是合并类型 'bondOrderExecution'，'orderExecution'，则表示一个 共享流表 或者 IPC 表对象， 需要在订阅前创建。该表的 schema 需要和获取的行情数据结构一致。可以通过插件提供的 `getSchema` 函数来获取行情数据的 schema。

如果 *dataType* 的类型是合并类型 'bondOrderExecution'，'orderExecution'。则该参数需要传入一个字典。字典的 key 为整型标量，指代特定的 channel，需要大于 0。字典的 value 为 共享流表、流数据引擎 或 IPC 表。流表的 schema 需要和获取的行情数据结构一致。

**market** 整型标量。表示市场类型。需要和 AMD 中定义的市场类型一致。**amdQuote 插件不支持订阅全部市场，因此必须填写具体的市场代码如 101。**

**codeList** 字符串向量，可选。表示股票列表。不传该参数表示订阅所有股票。

**transform**: 一元函数（其参数是一个表），可选。插入到 DolphinDB 表前对表进行转换，例如替换列。请注意，传入的一元函数中不能存在对 DFS 表的操作，例如：读取或写入 DFS 表，获取 DFS 表的 schema 等。

**seqCheckMode** 可选，可以为整型标量，也可以为STRING 类型标量，用于控制在数据不连续时插件接收数据的行为。在合并类型 orderExecution, bondOrderExecution 的订阅中生效。

* seqCheckMode 为 0 或者 'check'：代表在数据不连续时，停止接收数据。
* seqCheckMode 为 1 或者 'ignoreWithLog'（默认值）：代表在数据不连续时，继续接收数据，但是会输出序号跳变情况到 info 级别的 log。该选项为默认选项。
* seqCheckMode 为 2 或者 'ignore'：代表在数据不连续时，继续接收数据，且不输出任何 log。

判断是否连续的方式（随着交易所规则改变，该规则也可能发生改变）：

* 上交所：不同标的 order 和 trade 数据的 nBizIndex 共同连续递增。
* 深交所：不同标的 order 和 trade 数据的 nBizIndex 共同连续递增。

**注意**

1. 收到的数据可能已经乘了一定的倍率，插件中未作更多处理。具体字段对应倍率请查询华锐提供的官方文档。
2. 如果未取消订阅就重新订阅某种类型的行情，该种类前一次订阅的内容会被取消，即只有最后一次订阅生效。

**queueDepth** 可选参数，非负整数，表示该订阅对应的队列深度，默认值为 100000。

### unsubscribe

**语法**

```
amdQuote::unsubscribe(handle, dataType, [market], [codeList])
```

**详情**

取消对行情数据的订阅。

* 如果 *dataType* 指定为 'all'，表示取消所有订阅，此时无需指定 *market* 和 *codeList*。
* 如果 *dataType* 指定非 'all' 的值：
  + 只指定 *market*，表示取消 *market* 下的所有订阅。
  + 同时指定 *market* 和 *codeList*，表示只取消对 *codeList* 的订阅。

**参数**

**handle** `connect` 接口返回的句柄。

**dataType** STRING 类型标量，表示行情的类型。可取值详见附录的行情类型对照表。

**market** 整型标量，表示市场类型，需要和 AMD 中定义的市场类型一致。

**codeList** 字符串向量，可选，表示股票列表。

### close

**语法**

```
amdQuote::close(handle)
```

**详情**

关闭当前连接。通过 `connect` 创建连接时，插件会创建线程在内的一些资源。当用户确定不使用行情数据之后需要手动调用 `close` 接口释放资源。

注意：

* AMD 提供的 SDK 在连接时会创建一些全局变量，它们在 DolphinDB 插件内无法析构，因此用户需要尽量避免频繁连接，以免内存占用过高导致 DolphinDB 不可用。
* 请勿使用 DolphinDB server 的 close) 函数关闭 amdQuote 插件的句柄（handle），需使用插件提供的关闭接口，否则不会断开与服务器的连接，资源也无法释放。

**参数**

**handle** `connect` 接口返回的句柄。

### getSchema

**语法**

```
amdQuote::getSchema(dataType)
```

**详情**

该函数应该在 `connect` 函数之后调用。获取行情数据的表结构。返回一个表，包含三列：name，type 和 typeInt，分别表示该行情表中字段的名字，字段类型的名称和类型的枚举值。通过该表来创建具有相同结构的共享流表。

如果在 `connect` 中指定了 *option*，在返回的 schema 中会增加对应的列。

* 如果指定了 ReceivedTime 为 true，则会增加 receivedTime 列，表示数据进入插件的时间，类型为 NANOTIMESTAMP。
* 如果指定了 DailyIndex 为 true，则会增加 dailyIndex 列，表示插件收到的行情数据在每个 channel\_no 下按日内递增的序列号，类型为 LONG。
* 如果指定了 OutputElapsed 为 true，则会增加 perPenetrationTime 列，表示从插件接收到数据，到写入流表前的时间间隔。类型为 LONG，单位为微秒。

目前 `getSchema` 函数返回的个别字段的命名与行情数据中的字段名不同，使用中需要注意：

* execution、bondExecution 类型对应行情数据的第 9 列字段名为 bidApplSeqNum，而该函数返回的字段名为 bidAppSeqNum。

**参数**

**dataType** STRING 类型标量，表示行情的类型。可取值详见附录的行情类型对照表。

注意 orderExecution 同时包含基金和股票数据。

### getStatus

**语法**

```
amdQuote::getStatus(handle)
```

**详情**

返回一个表格，包含各种已订阅数据的状态信息，不包含未订阅过的数据类型

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| **topicType** | 订阅的类型 | STRING |
| **market** | 订阅的市场 | INT |
| **channel** | 若订阅了逐笔合并，为该订阅所对应的通道号 | INT |
| **startTime** | 订阅开始的时间 | NANOTIMESTAMP |
| **endTime** | 订阅结束的时间 | NANOTIMESTAMP |
| **firstMsgTime** | 第一条消息收到的时间 | NANOTIMESTAMP |
| **lastMsgTime** | 最后一条消息收到的时间 | NANOTIMESTAMP |
| **processedMsgCount** | 已经处理的消息数 | LONG |
| **lastErrMsg** | 最后一条错误信息 | STRING |
| **failedMsgCount** | 处理失败的消息数 | LONG |
| **lastFailedTimestamp** | 最后一条错误消息发生的时间 | NANOTIMESTAMP |
| **queueDepthLimit** | 异步队列深度的上限 | LONG |
| **queueDepth** | 当前异步队列的深度 | LONG |

**参数**

**handle** `connect` 接口返回的句柄。

### getHandle

**语法**

```
amdQuote::getHandle()
```

**详情**

获取当前已有的 AMD 连接句柄。如果尚未连接则抛出异常。

### getCodeList

**语法**

```
amdQuote::getCodeList([market])
```

**详情**

获取当前连接下的代码表结构。

AMD SDK 版本为 3.9.6 的 amdQuote396 插件不支持该函数。

**参数**

**market** 可选，整型向量，表示需要查询的市场代码所组成的向量。如果不填写将会默认查询上交所与深交所。支持传入 0 即华锐定义的 kNone 市场类型，可以查询所有市场。

### getETFCodeList

**语法**

```
amdQuote::getETFCodeList([market])
```

**详情**

获取当前连接下指定交易所的 ETF 代码表结构。

AMD SDK 版本为 3.9.6 的插件不支持该函数。

**参数**

**market** 可选，整型向量，表示需要查询的市场代码。默认值为 market=[101, 102]，即上交所与深交所。注意：指定单个市场代码，也必须传入向量，例如：market=[103]。

### setLogLevel

**语法**

```
amdQuote::setLogLevel(logLevel)
```

**详情**

设置插件的日志等级，系统将打印当前日志等级及以上级别的插件日志，默认为 INFO。注意，该函数仅设置插件的日志等级，不会改变 DolphinDB server 的日志等级。

**参数**

**logLevel** 日志等级，从低到高可选值为：DEBUG, INFO, WARNING, ERROR。

**示例**

设置 amdQuote 插件的 log level 为 WARNING，此时只输出 WARNING 和 ERROR 级别的 log。

```
amdQuote::setLogLevel(WARNING)
```

### getLogLevel

**语法**

```
amdQuote::getLogLevel()
```

**详情**

获取当前当前的日志等级。返回值为一个字符串。

## 使用示例

1. 使用 `loadPlugin` 加载插件

   ```
   loadPlugin("amdQuote401")
   ```
2. 连接 AMD 服务器

   ```
   handle = amdQuote::connect(`admin, `123456, [`119.29.65.231], [8031], dict(["ReceivedTime"], [true]))
   ```
3. 获取对应的表结构

   ```
   snapshotSchema = getSchema(`snapshot);

   executionSchema = getSchema(`execution);

   orderSchema = getSchema(`order);
   ```
4. 创建流数据表

   ```
   snapshotTable = streamTable(10000:0, snapshotSchema[`name], snapshotSchema[`type]);

   executionTable = streamTable(10000:0, executionSchema[`name], executionSchema[`type]);

   orderTable = streamTable(10000:0, orderSchema[`name], orderSchema[`type]);
   ```
5. 共享并持久化流数据表

   ```
   enableTableShareAndPersistence(table=snapshotTable, tableName=`snapshot1, cacheSize=10000)

   enableTableShareAndPersistence(table=executionTable, tableName=`execution1, cacheSize=10000)

   enableTableShareAndPersistence(table=orderTable, tableName=`order1, cacheSize=10000)
   ```
6. 订阅深圳市场全部股票代码

   因为 AMD API 文档中深圳市场的枚举值为 102，所以 `subscribe` 的 *market* 参数指定为102。

   对应的订阅快照，逐笔成交和逐笔委托的示例为：

   ```
   amdQuote::subscribe(handle, `snapshot, snapshot1, 102)

   amdQuote::subscribe(handle, `execution, execution1, 102)

   amdQuote::subscribe(handle, `order, order1, 102)
   ```
7. 取消深圳市场的快照订阅

   ```
   amdQuote::unsubscribe(handle， `snapshot, 102)
   ```

   取消逐笔成交，逐笔委托，取消全部数据的订阅分别是：

   ```
   amdQuote::unsubscribe(handle, `execution, 102)

   amdQuote::unsubscribe(handle, `order, 102)

   amdQuote::unsubscribe(handle, `all, 102)
   ```
8. 使用完成后，调用接口释放资源

   ```
   amdQuote::close(handle)
   ```

## 附录

* 行情类型对照表

| 交易所 | 行情类型取值 | 行情类型 | 备注 |
| --- | --- | --- | --- |
| 上交所(101)/深交所(102) | index | 指数 |  |
| orderQueue | 委托队列 |  |
| snapshot | 股票快照 |  |
| execution | 股票逐笔成交 |  |
| order | 股票逐笔委托 |  |
| fundSnapshot | 基金快照 | 上交所基金会混入部分债券申购的快照数据 |
| fundExecution | 基金逐笔成交 | 上交所基金会混入部分债券的成交数据 |
| fundOrder | 基金逐笔委托 | 上交所基金会混入部分债券的委托数据 |
| bondSnapshot | 债券快照 |  |
| bondExecution | 债券逐笔成交 |  |
| bondOrder | 债券逐笔委托 |  |
| orderExecution | 基金股票逐笔成交合并 | 包括股票和基金数据 |
| bondOrderExecution | 债券逐笔成交合并 |  |
| option | 期权 |  |
| IOPV | ETF 基金份参考净值 | 需 amdQuote 版本 >= 3.9.8 |
| 北交所（2） | NEEQSnapshot | 股转快照 |  |
| 上期所（3）/中金所（4） | future | 期货/期货期权 |  |
| 港交所（103） | HKExMergeSnapshot | 商业港股股票快照和委托挂单 | 需 amdQuote 版本 >= 4.5.7 |
| HKExIndexSnapshot | 商业港股指数行情快照 | 需 amdQuote 版本 >= 4.5.7 |
| HKTSnapshot | 商业港股快照行情 |  |
