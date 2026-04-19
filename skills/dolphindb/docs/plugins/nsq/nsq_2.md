<!-- Auto-mirrored from upstream `documentation-main/plugins/nsq/nsq_2.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# NSQ

为对接恒生 NSQ 极速行情服务软件，DolphinDB 基于恒生 HSNsqApi 开发了 NSQ 插件。通过该插件能够获取上海和深圳市场的行情。主要获得以下三种行情：

1. 主推-现货深度行情主推回调（OnRtnSecuDepthMarketData->snapshot）
2. 主推-现货逐笔成交行情主推回调（OnRtnSecuTransactionTradeData->trade）
3. 主推-现货逐笔委托行情主推回调（OnRtnSecuTransactionEntrustData->orders）

请注意，DolphinDB NSQ 插件仅提供行情对接服务。数据源和接入服务可咨询数据服务商或证券公司。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x86-64, Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456");
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("nsq");
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("nsq");
   ```

注意：如果在高版本 glibc 的机器上（比如 RockyLinux8）使用该插件，需要安装 libnsl 库。

## 接口函数

### connect

**语法**

```
nsq::connect(configFilePath, [option], [username], [password], [dataVersion])
```

**详情**

该函数将根据 NSQ 配置文件 *sdk\_config.ini* 、传入的用户名和密码，与行情服务器建立连接。连接成功后，将在日志文件 *dolphindb.log* 中会打印 “OnFrontConnected”。

注意：

1. 部分 NSQ 的行情服务器会强制要求用户传入用户名密码，请注意填写。
2. 再次执行 `connect` 进行重新连接前，需要先执行 `nsq::close()` 断开连接，否则会抛出异常。
3. 配置文件中 sailfish 源必须指定 service\_addr 和 service\_port 两项，否则会直接报错。
4. 如果配置文件的编码格式有误，也可能会导致无法找到上一条中所说的必备项，建议使用 UTF-8 格式编码的配置文件。
5. 目前插件支持连接 sailfish，DS 解码，目前不支持其他源如 FPGA 解码。如果填写了不支持的源则会在连接时宕机，需要谨慎处理。
6. 连接 Windows 版本的 NSQ 时，配置文件需要使用 CRLF 换行符；直接使用 UNIX 风格的换行方式可能会导致系统卡住。

**参数**

**configFilePath** 字符串标量，表示 *sdk\_config.ini* 的绝对路径；若拷贝 sdk\_config.ini 至 dolphindb server，则可以是相对于 DolphinDB Server 的一个相对路径。

**option** 字典类型，可选参数，表示扩展参数。当前键只支持 receivedTime 和 getAllFieldNames。

* receivedTime 表示是否显示接收时间，对应值为布尔值。
* getAllFieldNames 表示是否接受所有字段数据，对应值为布尔值。详见后文示例。

**username** 字符串类型，可选参数，表示登录的用户名。

**password** 字符串类型，可选参数，表示登录用户名对应的密码。

**dataVersion** 字符串标量，可选参数，表示接收数据时字段内容所基于的 NSQ SDK 版本，可以填写 ‘ORIGIN’ 或者 ‘v220105’，默认为 ‘ORIGIN’。‘v220105’ 与 NSQ SDK 202201.05.000 版本对齐，其中 orders 类型会比 'ORIGIN' 版本多两个字段；当参数 *option* 中 getAllFieldNames 为 true 时，snapshot 类型也会增加深圳债券现券交易等字段。注意：指定该参数后，`getSchema` 和 `subscribe` 函数都会基于所指定的版本改变行为。

### getSchema

**语法**

```
nsq::getSchema(dataType)
```

**详情**

该函数需要在 `connect` 函数之后调用。后续根据 `getSchema` 返回的表结构创建流表。

返回一个表，包含两列：name，type，分别表示该行情表各个字段的名称、类型名。可通过该表来创建具有相同结构的共享流表。

**参数**

**dataType** 一个字符串，表示所要获取的表结构的类型，支持填写 snapshot, trade, orders, orderTrade。

### subscribe

**语法**

```
nsq::subscribe(dataType, market, outputTable, [queueDepth=1000000], [codes])
```

**详情**

表示对上海证券交易所或深圳证券交易所发布的某种行情数据进行订阅，并将结果保存到由参数 *outputTable* 指定的流表中。

订阅成功后，在日志（*dolphindb.log*）中会有打印如下信息（若出现 successfully，表则示订阅成功）：

```
OnRspSecuTransactionSubscribe: nRequestID[0], ErrorID[0], ErrorMsg[subscribe all transaction trans type[1] of exchange_id [1] successfully]
```

请注意，若需要将已经订阅的同一个(dataType, market) 的行情数据输出到另一个 outputTable，需要通过 `unscribeTable` 命令取消订阅，否则会抛出异常。

outputTable（流表）是一种特殊的内存表，用于存储及发布流数据。更多流表的使用方法可参考文档：DolphinDB-流数据介绍。

**参数**

**dataType** 一个字符串，表示行情的类型，可以指定为以下值：

* "snapshot" 表示回调函数 `OnRtnSecuDepthMarketData` （主推 - 现货深度行情）获取的行情数据。
* "trade" 表示回调函数 `OnRtnSecuTransactionTradeData` （主推 - 现货逐笔成交行情主）获取的行情数据。
* "orders" 表示回调函数 `OnRtnSecuTransactionEntrustData` （主推 - 现货逐笔委托行情）获取的行情数据。
* "orderTrade" 表示由 orders 和 trade 合并的行情数据，适配 `orderbookSnapshotEngine` 的输入。

**market** 一个字符串，表示上海证券交易所或深圳证券交易所。上海证券交易所用 `sh` 表示，深圳证券交易所用 `sz` 表示。

**outputTable**

* 如果 *dataType* 为普通行情类型（snapshot/trade/orders）：表示一个共享流表对象，需在订阅前创建。该流表结构需与行情数据结构一致，可通过 `getSchema` 函数获取表结构。
* 如果 *dataType* 为合并类型（orderTrade）：表示一个字典对象，需在订阅前创建，其键值对定义如下：
  + key：INT 类型标量，表示行情数据的通道编号，需大于 0。
  + value：共享流表对象，流表结构需与行情数据结构一致，可通过 `getSchema(dataType=orderTrade)` 获取表结构。

**queueDepth** 整型标量，可选参数，默认为 1000000，表示后台接收数据的队列深度。

**codes** 字符串向量，可选参数，表示要订阅的标的。如果不指定或者指定为空则订阅全部标的，指定了则会根据它进行过滤。

**注** ：subscribe 函数执行时，同一个 dataType 和 market 组合只能订阅一次，即使订阅时指定的 codes 不同也会被视为同一种订阅。

### unsubscribe

**语法**

```
nsq::unsubscribe(dataType, market)
```

**详情**

表示取消对上海证券交易所或深圳证券交易所发布的某种行情数据的订阅，例如：unsubscribe(`snapshot, \`sz) 表示取消对深圳证券交易所的 snapshot 行情数据的订阅。

取消订阅成功后，在日志 (*dolphindb.log*) 中会有打印如下信息（若出现 successfully，表示取消订阅成功）：

```
OnRspSecuTransactionCancel: nRequestID[0], ErrorID[0], ErrorMsg[unsubscribe all transaction trans type [2] of exchange_id [2] successfully]
```

**参数**

同 `subscribe` 一致。

### close

**语法**

```
nsq::close()
```

**详情**

表示断开当前连接。

### getStatus

**语法**

```
nsq::getStatus()
```

**详情**

`getStatus` 是一个运维命令，用于获取当前连接状态，以及每个订阅的状态。在 3.00.0.2/2.00.12.5 之前版本，该函数名为 `getSubscriptionStatus` ，现已兼容。

该函数会返回一个表：

| 列名 | 类型 | 含义 |
| --- | --- | --- |
| topicType | STRING | 订阅的类型和市场 |
| startTime | NANOTIMESTAMP | 订阅开始的时间 |
| endTime | NANOTIMESTAMP | 订阅结束的时间 |
| firstMsgTime | NANOTIMESTAMP | 第一条消息收到的时间 |
| lastMsgTime | NANOTIMESTAMP | 最后一条消息收到的时间 |
| processedMsgCount | LONG | 已经处理的消息数 |
| lastErrMsg | STRING | 最后一条错误信息 |
| failedMsgCount | LONG | 处理失败的消息数 |
| lastFailedTimestamp | NANOTIMESTAMP | 最后一条错误消息发生的时间 |
| queueDepthLimit | LONG | 异步队列深度的上限 |
| queueDepth | LONG | 当前异步队列的深度 |

## 完整示例

```
// 登录
login("admin", "123456")

// 加载插件
loadPlugin("Your_plugin_path/PluginNsq.txt");

// 连接行情服务器，第二个参数为可选
nsq::connect(your_config_path，dict(["ReceivedTime"， "getAllFieldNames"], [true, true]));

// 获取行情数据的表结构
snapshotSchema = nsq::getSchema(`snapshot);
tradeSchema = nsq::getSchema(`trade);

// 根据表结构创建流表
streamTable(1000:0, snapshotSchema[`name], snapshotSchema[`type]) as t1;
streamTable(1000:0, tradeSchema[`name], tradeSchema[`type]) as t2;
go

// 流表持久化
enableTableShareAndPersistence(table=t1, tableName=`snapshot_sh, cacheSize=100000)
enableTableShareAndPersistence(table=t2, tableName=`trade_sh, cacheSize=100000)

// 订阅上海证券交易所的深度行情s
nsq::subscribe(`snapshot, `sh, snapshot_sh);

// 取消订阅
nsq::unsubscribe(`snapshot, `sh)

// 订阅上海证券交易所的逐笔成交行情
nsq::subscribe(`trade`, `sh`, trade_sh);

// 用这个表对象进行操作
select * from snapshot_sh limit 100;

// 取消订阅
nsq::unsubscribe(`trade`, `sh`)

// 获取每个订阅的状态
status = nsq::getSubscriptionStatus();
select * from status;

// 关闭连接
nsq::close();
```

## 附录

### 报错信息

插件正常运行的信息会打印在日志文件中（*dolphindb.log*），若运行中出现错误，则会抛出异常。具体异常信息及解决办法如下：

1. 重复连接异常。若当前已连接，则需要先通过 `close` 关闭连接，再 `connect` 重连。

   You are already connected. To reconnect, please execute close() and try again.
2. API 初始化错误，需要确认 `connect` 传入的配置文件路径和配置信息是否正确。

   Initialization failed. Please check the config file path and the configuration.
3. API 连接服务器失败，需要确认 `connect` 传入的配置文件路径和配置信息是否正确。

   Failed to connect to server. Please check the config file path and the configuration.
4. 登录错误，用户名，密码错误。

   login failed: iRet [iRet], error: [errorMsg]
5. API 未初始化错误，需要检查是否 `connect()` 成功。

   API is not initialized. Please check whether the connection is set up via connect().
6. subscribe 的 `outputTable` 参数错误，需要是一个 shared streamTable（共享流表）。

   The third parameter "outputTable" must be a shared stream table.
7. subscribe 的 `market` 参数错误，需要是 `sh` 或 `sz`。

   The second parameter "market" must be `sh` or `sz`.
8. subscribe 的 `dataType` 参数错误，应该是 `snapshot` or `trade` or `orders`。

   The first parameter "dataType" must be `snapshot`, `trade` or `orders`.
9. subscribe `outputTable` 参数的 *schema* 错误，schema 需和 SDK 一致。

   Subscription failed. Please check if the schema of “outputTable” is correct.
10. 重复订阅错误，想要更换同一类订阅 (如 `snapshot`, `sh` 两个字段唯一标识一类订阅) 订阅的流表，需要先执行 `unsubscribe`，然后再更新订阅。

    Subscription already exists. To update subscription, call unsubscribe() and try again.
11. `unsubscribe` 时 API 未初始化错误。

    API is not initialized. Please check whether the connection is set up via connect().
12. `close()` 错误，在未初始化（未调用 `connect`）的 API 上进行了 `close`。

    Failed to close(). There is no connection to close.
