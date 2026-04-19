<!-- Auto-mirrored from upstream `documentation-main/plugins/datafeed.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DataFeed

DolphinDB DataFeed 插件通过集成中金所提供的 SDK 来接收非展示型行情源数据，并将数据存入 DolphinDB 的数据表。该插件支持通过 TCP 和 UDB 组播两种方式接收数据。

插件依赖第三方库 libdatafeed\_multi\_api.so。

## 安装插件

### 版本要求

DolphinDB Server：2.00.10 及更高版本，支持 Linux x64。TCP 连接要求 server 版本号不低于 2.00.13。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("DataFeed")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("DataFeed")
   ```

## 接口说明

### createHandle

**语法**

```
createHandle(addr, username, password, logLevel, logFileName, [option])
```

**详情**

创建一个句柄，用于后续操作，例如订阅，取消订阅等。注意：只能创建一个。

**参数**

**addr** STRING 类型向量，表示后台服务器地址。服务器地址的格式为："protocol://ipaddress:port"，如："tcp://127.0.0.1:17001"。 "tcp" 代表传输协议，"127.0.0.1" 代表服务器地址，"17001" 代表服务器端口号。

**username** STRING 类型标量，表示用户名。

**password** STRING 类型标量，表示密码。

**logLevel** 整型标量，表示日志级别，在[0, 5]中取值，分别表示 FATAL, ERROR, WARNING, INFO, DEBUG, TRACE。

**logFileName** STRING 类型标量，用于指定存储 DataFeed 日志的文件。

**option**：一个字典, 类型为 (STRING, BOOL)，可选参数。其键支持 "receiveTime"，"OutputElapsed"。其中：

* "receiveTime" 表示是否获取插件收到行情数据的时间戳。其指定为 dict(["receiveTime"], [true]) ，且 `getSchema` 指定 *needReceiveTime*=true 时，获取的表结构中将包含插件收到行情数据的时间戳列。
* "OutputElapsed" 表示是否获取插件从收到行情到准备插入流表的时延，单位是纳秒。其指定为 dict(["OutputElapsed"], [true])，且 `getSchema` 指定 *needElapsedTime*=true 时，获取的表结构中将包含时延列。
* "concatTime" 表示是否获取 tradeTime，即 UpdateTime 和 UpdateMsec 合并后的时间。其指定为 dict(["concatTime"], [true]) ，且 `getSchema` 指定 *concatTime*=true 时，获取的表结构中将包含 tradeTime 列。

### subscribe

**语法**

```
DataFeed::subscribe(handle, localIP, table)
```

**详情**

开始订阅行情数据，将数据存到 *table* 中。

**参数**

**handle** 由 `createHandle` 返回的句柄。

**localIP** STRING 类型标量，表示用户本地 IP 地址，用来校验地址以及指定组播接收网卡。注意：请保证传入的 IP 地址合法，且相应网卡已使能组播，否则无法收到数据。

**table** 共享内存表或共享流表，表结构可由 `getSchema` 接口获取。

### unsubscribe

**语法**

```
DataFeed::unsubscribe(handle)`
```

**详情**

取消订阅。

**参数**

**handle** 由 `createHandle` 返回的句柄。

### close

**语法**

```
DataFeed::close(handle)
```

**详情**

断开连接，销毁该 *handle*。

**参数**

**handle** 由 `createHandle` 返回的句柄。

### getHandle

**语法**

```
DataFeed::getHandle()
```

**详情**

返回可用的句柄。如果没有可用句柄，则抛出异常。

### getStatus

**语法**

```
DataFeed::getStatus()
```

**详情**

获取订阅数据的状态信息。返回一个表格，结构为：

| **列名** | **含义** | **类型** |
| --- | --- | --- |
| startTime | 订阅开始的时间 | NANOTIMESTAMP |
| endTime | 订阅结束的时间 | NANOTIMESTAMP |
| lastMsgTime | 最后一条消息收到的时间 | NANOTIMESTAMP |
| processedMsgCount | 已经处理的消息数 | LONG |
| lastErrMsg | 最后一条错误信息 | STRING |
| failedMsgCount | 处理失败的消息数 | LONG |
| lastFailedTimestamp | 最后一条错误消息发生的时间 | NANOTIMESTAMP |

### getSchema

**语法**

```
DataFeed::getSchema([needReceiveTime], [needElapsedTime], [concatTime])
```

**详情**

返回存放行情的表的结构信息。返回一个表，包含三列：name，typeString 和 typeInt，分别表示该行情表中字段的名字，字段类型的名称和类型的枚举值。

|  | name | typeString | typeInt |
| --- | --- | --- | --- |
| 1 | TradingDay | DATE | 17 |
| 2 | InstrumentID | SYMBOL | 17 |
| 3 | SettlementGroupID | SYMBOL | 17 |
| 4 | SettlementID | INT | 4 |
| 5 | LastPrice | DOUBLE | 16 |
| 6 | PreSettlementPrice | DOUBLE | 16 |
| 7 | PreClosePrice | DOUBLE | 16 |
| 8 | PreOpenInterest | DOUBLE | 16 |
| 9 | OpenPrice | DOUBLE | 16 |
| 10 | HighPrice | DOUBLE | 16 |
| 11 | LowPrice | DOUBLE | 16 |
| 12 | Volume | INT | 4 |
| 13 | Turnover | DOUBLE | 16 |
| 14 | OpenInterest | DOUBLE | 16 |
| 15 | ClosePrice | DOUBLE | 16 |
| 16 | SettlementPrice | DOUBLE | 16 |
| 17 | UpperLimitPrice | DOUBLE | 16 |
| 18 | LowerLimitPrice | DOUBLE | 16 |
| 19 | PreDelta | DOUBLE | 16 |
| 20 | CurrDelta | DOUBLE | 16 |
| 21 | UpdateTime | SECOND | 17 |
| 22 | UpdateMsec | INT | 4 |
| 23 | BidPrice | DOUBLE[] | 80 |
| 24 | BidVolume | INT[] | 68 |
| 25 | AskPrice | DOUBLE[] | 80 |
| 26 | AskVolume | INT[] | 68 |
| 27 | BandingUpperPrice | DOUBLE | 16 |
| 28 | BandingLowerPrice | DOUBLE | 16 |
| 29 | receiveTime(可选） | NANOTIMESTAMP | 14 |
| 30 | OutputElapsed (可选） | NANOTIMESTAMP | 14 |
| 31 | concatTime(可选) | TIME | 8 |

**参数**

**needReceiveTime** 可选参数，BOOL 类型标量， 表示是否需要包含 receiveTime 列，默认为 false。如果在 `createHandle` 时，指定了 *receiveTime*，则需要将该参数设置为 true。

**needElapsedTime** 可选参数，BOOL 类型标量， 表示是否需要包含 OutputElapsed 列，默认为 false。如果在 `createHandle` 时，指定了 *OutputElapsed*，则需要将该参数设置为 true。

**concatTime** 可选参数，BOOL 类型标量， 表示是否需要包含 UpdateTime 和 UpdateMsec 合并后的列，默认为 false。如果在 `createHandle` 时，指定了 *concatTime*，则需要将该参数设置为 true。

## 完整示例

```
handle = DataFeed::createHandle(["tcp://10.15.14.15:9001"], "user", "password", 3, "/home/logPath/log.log")

share  table(1:0, `TradingDay`InstrumentID`SettlementGroupID`SettlementID`LastPrice`PreSettlementPrice`PreClosePrice`PreOpenInterest`OpenPrice`HighPrice`LowPrice`Volume`Turnover`OpenInterest`ClosePrice`SettlementPrice`UpperLimitPrice`LowerLimitPrice`PreDelta`CurrDelta`UpdateTime`UpdateMsec`BidPrice`BidVolume`AskPrice`AskVolume`BandingUpperPrice`BandingLowerPrice, [SYMBOL, SYMBOL, SYMBOL, INT, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, SYMBOL, INT, DOUBLE[], INT[], DOUBLE[], INT[], DOUBLE, DOUBLE]) as depthMDTable

DataFeed::subscribe(handle, "10.115.11.114", depthMDTable)

DataFeed::getStatus()
DataFeed::close(handle)
```
