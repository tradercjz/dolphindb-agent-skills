<!-- Auto-mirrored from upstream `documentation-main/plugins/xtp.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# XTP

通过 DolphinDB 的 XTP 插件，用户可以接收上交所、深交所以及北交所的实时行情，并将数据存储于 DolphinDB 的共享表中。可接收的数据如下表所示：

|  | 指数 | 股票 | 基金 | 债券 | 期权 |
| --- | --- | --- | --- | --- | --- |
| 快照 | 有 | 有 | 有 | 有 | 有 |
| 逐笔 | 无 | 有 | 有 | 有 | 无 |
| 订单簿 | 无 | 有 | 有 | 有 | 无 |

本插件依赖中泰证券提供的第三方库 *libxtpquoteapi.so*，可参见文档链接 [xtp-中泰证券](https://xtp.zts.com.cn/doc/api/xtpDoc) 。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("XTP")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("XTP")
   ```

## 接口说明

### setGlobalConfig

**语法**

```
XTP::setGlobalConfig(clientId, saveFilePath, [logLevel=3])
```

**详情**

设置一些全局配置项。在创建句柄前必须调用至少一次。无返回值。

**参数**

**clientId** INT 类型标量，1-99 之间取值，表示账户 ID。如果需要在多个 DolphinDB 进程中使用同一个账户去连接，则需要使用不同的 *clientId*。

**saveFilePath** STRING 类型标量，表示存储日志文件的目录，要求必须存在且有可写权限。

**logLevel** INT 类型标量，表示 xtp 记录日志的级别，0-5 之间取值，分别对应 FATAL ERROR WARNING INFO DEBUG TRACE 级别，默认是 3。

### createXTPConnection

**语法**

```
XTP::createXTPConnection(name, [config])
```

**详情**

返回一个连接句柄，可用于登录，订阅数据。

**参数**

**name** STRING 类型标量，连接句柄的唯一标识符，不能为空，也不能重复。

**config** 一个 key 类型为 STRING 的字典，包含如下所示的配置项：

| **配置项** | **值类型** | **说明** |
| --- | --- | --- |
| receiveTime | 整型 | 可选参数，用于设定是否将接收到数据的时间并为表的最后一列，类型为 NANOTIMESTAMP。1：增加该列；其它不增加；默认不增加。 |
| OutputElapsed | BOOL | 可选参数，用于设定是否为行情表增加最后一列。该列数据类型为 LONG，表示插件从收到行情开始到准备插入流表为止的延时，单位为纳秒。true 表示增加该列；默认为 false，表示不增加。 |
| ciphertext | INT | 可选参数，用于设定在登陆时是否密码使用密文传输和传递 IV 值。（加密采用 AES-256-CFB 算法）默认为 1，表示开启；若为其他值，则为关闭。 |

### login

**语法**

```
XTP::login(conn, config)
```

**详情**

连接 XTP 服务器并登录。无返回值。

注意事项（摘自 XTP 官方文档）：

* 测试环境使用 TCP 的方式推送行情。由于带宽的限制，建议客户只订阅少量股票，否则会出现推送延时、断线等问题。
* XPT 提供的 API 的默认日志级别是 DEBUG，需要调整到 INFO（或 ERROR），否则可能会导致丢包。本插件已将默认级别调整到 INFO，在调试时可以设置为 DEBUG。

**参数**

**conn** 由 `createXTPConnection` 接口返回的句柄。

**config** 一个 key 类型为 STRING 的字典，包含一些配置项：

| **配置项** | **值类型** | **说明** |
| --- | --- | --- |
| ip | 字符串 | 服务器 IP 地址 |
| port | 整型 | 服务器端口号 |
| localIP | 字符串 | 可选参数，本地网卡地址，不能为空字符串 |
| user | 字符串 | 登录用户名 |
| password | 字符串 | 登录密码 |
| protocalType | 整型 | 1: TCP；2: UDP |
| heartBeatInterval | 整型 | 可选参数，设置心跳检测时间间隔，单位为秒。默认填 30 |
| udpBufferSize | 整型 | 可选参数，UDP 方式连接时的缓冲区大小，可填 64，128，256，512，单位 MB，默认填 512 |
| udpRecvCPUId | 整型数组 | 可选参数，UDP 方式接收行情时，接受行情的线程绑定的 CPU 集合。绑核时，将从数组前面的核开始使用。不超过 10 个 |
| udpParseCPUId | 整型数组 | 可选参数，UDP 方式接收行情时，解析行情的线程绑定的 CPU 集合。绑核时，将从数组前面的核开始使用。不超过 10 个 |
| udpOutputFlag | 整型 | 可选参数，设定 UDP 方式接收行情时，是否输出异步日志。1：输出；其它不输出；默认不输出 |

注意：如果在 `createXTPConnection` 中开启了配置项 ciphertext，则在登陆时传递的密码和 IV 值的类型也要求是 INT 类型数组。

### subscribe

**语法**

```
XTP::subscribe(conn, quoteType, marketType, codeList, tableDict)
```

**详情**

订阅行情数据，收到数据后存储到目标表中。无返回值。

注意事项：

* 订阅同一个行情类型时，在多次订阅上证、深证市场时，要求传入的 *tableDict* 相同，如果不同，则以第一次订阅传入的 *tableDict* 为准。
* 订阅同一个行情类型时，在多次订阅新三板市场时，要求传入的 *tableDict* 相同，如果不同，则以第一次订阅传入的 *tableDict* 为准。
* 订阅同一个行情类型时，市场类型如果已订阅了 4（上证+深证）则不能再次订阅 1（上证）或 2（深证）。
* 订阅同一个行情类型时，市场类型如果已订阅了 1（上证）或 2（深证）则不能再次订阅 4（上证+深证）。
* 如果 *marketType* 填为 4，则不能填 *codeList*。
* 各目标表的 schema 可以通过 `getSchema` 接口获取。
* 目标表要求是共享表。
* 公网测试环境仅供客户调试 API 接口，没有订单薄 OB 行情。

**参数**

**conn** 由 `createXTPConnection` 接口返回的句柄。

**quoteType** INT 类型标量，表示行情类型。1：快照，2：逐笔，3：订单簿。

**marketType** INT 类型标量，表示市场类型。1：上证， 2：深证，3：新三板，4：上证+深证。

**codeList** STRING 类型向量，表示合约 ID 数组。如果不填或者填空，则订阅全市场数据。

**tableDict** 一个字典，key 类型是 STRING，value 必须是共享表，用来指定输出表。根据行情类型的不同，输出表的数量也不同。如果空缺其中若干表，则相对应的行情会被丢弃，详情如下表所示：

| **行情类型** | **key** | **说明** |
| --- | --- | --- |
| 快照 | indexTable、optionTable、actualTable、bondTable | 指数快照表、期权快照表、现货快照表（股票/基金等）、债券快照表 |
| 逐笔 | entrustTable、tradeTable、statusTable、TickByTickTable | 逐笔委托表、逐笔成交表、逐笔状态表、逐笔合并表 |
| 订单簿 | orderBookTable | 订单簿表 |

注意：自 3.00.0.2/2.00.12.5 版本起，支持 TickByTickTable 即逐笔合并表，其包含收到的三种逐笔数据（委托、成交、状态），该表可以做为 orderbookSnapshotEngine 的输入表。在订阅逐笔数据时，*tableDict* 如果指定了 “TickByTickTable”，就会忽略其它的表。当 key 为 ”TickByTickTable” 时，value 分成两种情况：

* value 为一个表，即包含收到的所有数据。
* value 为一个字典，该字典的键为整形，表示channelNo，值是共享表，会将收到数据按照 channelNo 进行分类，放到不同的表中。

### unsubscribe

**语法**

```
XTP::unsubscribe(conn, quoteType)
```

**详情**

取消订阅某个类型的行情数据。无返回值。

**参数**

**conn** 由 `createXTPConnection` 接口返回的句柄。

**quoteType** INT 类型标量，表示行情类型。1：快照；2：逐笔；3：订单簿。

### getStatus

**语法**

```
XTP::getStatus([conn])
```

**详情**

获取订阅的状态信息。返回一个表，表结构如下所示：

| **列名** | **含义** | **类型** |
| --- | --- | --- |
| conn | 连接名称 | STRING |
| quoteType | 订阅类型 | STRING |
| startTime | 订阅开始的时间 | NANOTIMESTAMP |
| endTime | 订阅结束的时间 | NANOTIMESTAMP |
| lastMsgTime | 最后一条消息收到的时间 | NANOTIMESTAMP |
| processedMsgCount | 已经处理的消息数 | LONG |
| lastErrMsg | 最后一条错误信息 | STRING |
| failedMsgCount | 处理失败的消息数 | LONG |
| lastFailedTimestamp | 最后一条错误消息发生的时间 | NANOTIMESTAMP |

**参数**

**conn** 由 `createXTPConnection` 接口返回的句柄，可选参数。如果不填，则返回当前所有连接的状态信息。

### getHandle

**语法**

```
XTP::getHandle(name)
```

**详情**

返回由 *name* 指定的连接句柄。

**参数**

**name** STRING 类型标量，表示连接句柄的唯一标识符 。

### closeXTPConnection

**语法**

```
XTP::closeXTPConnection(conn)
```

**详情**

断开连接，销毁句柄。

**参数**

**conn** 由 `createXTPConnection` 接口返回的句柄。

### getSchema

**语法**

```
XTP::getSchema(type, [outputRecvTime], [outputElapsed])
```

**详情**

返回可存储相应行情类型数据的表的结构。

**参数**

**type** STRING 类型标量，表示类型。可选的 type 如下表所示：

| **type** | **含义** |
| --- | --- |
| indexMarketData | 指数快照表 |
| optionMarketData | 期权快照表 |
| actualMarketData | 现货快照表 |
| bondMarketData | 债券快照表 |
| BSEMarketData | 北交所数据表 |
| entrust | 逐笔委托表 |
| trade | 逐笔成交表 |
| state | 逐笔状态表 |
| orderBook | 订单簿表 |
| TickByTickTable | 逐笔合并表 |

**outputRecvTime** BOOL 类型标量，可选参数，默认为 false,，表示是否需要包含 receiveTime 列。如果在 `createXTPConnection` 时指定了 receiveTime 配置，那么该参数须设置为 true。

**outputElapsed** BOOL 类型标量，可选参数，表示返回的 shcmea 是否包含 elapsedTime 列。默认为 false，表示不包含。

**返回值** 一个表结构。表结构因 type 参数设置值不同而有所变化，具体说明如下。

指数快照表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所 ID |
| ticker | SYMBOL | 指数代码，6位 |
| lastPrice | DOUBLE | 最新价 |
| preClosePrice | DOUBLE | 昨日收盘 |
| openPrice | DOUBLE | 今日开盘 |
| highPrice | DOUBLE | 最高 |
| lowPrice | DOUBLE | 最低 |
| closePrice | DOUBLE | 今收 |
| dataTime | TIMESTAMP | 时间戳 |
| qty | LONG | 成交量，单位：上交所是手，深交所是股 |
| turnover | DOUBLE | 成交金额，单位元 |
| tradesCount | LONG | 成交笔数 注意，该字段对上交所无意义（填0） |
| bid1Qty | LONG[] | 买一队列 |
| bid1Count | INT | 买一队列的有效委托笔数 |
| maxBid1Count | INT | 买一队列总委托笔数 |
| ask1Qty | LONG[] | 卖一队列 |
| ask1Count | INT | 卖一队列的有效委托笔数 |
| maxAsk1Count | INT | 卖一队列总委托笔数 |

期权快照表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所 ID |
| ticker | SYMBOL | 期权代码，8位 |
| lastPrice | DOUBLE | 最新成交价 |
| preClosePrice | DOUBLE | 昨日收盘价 |
| openPrice | DOUBLE | 今日开盘 |
| highPrice | DOUBLE | 当日最高价 |
| lowPrice | DOUBLE | 当日最低价 |
| closePrice | DOUBLE | 今收价 |
| preTotalLongPosition | LONG | 昨持仓量 |
| totalLongPosition | LONG | 未平仓合约数量（张或股） |
| preSettlPrice | DOUBLE | 昨日结算价 |
| settlPrice | DOUBLE | 今日结算价 |
| upperLimitPrice | DOUBLE | 涨停价 |
| lowerLimitPrice | DOUBLE | 跌停价 |
| dataTime | TIMESTAMP | 时间戳 |
| qty | LONG | 当日累计成交量 |
| turnover | DOUBLE | 当日累计成交金额 |
| avgPrice | DOUBLE | 均价 |
| bids | DOUBLE[] | 10档买价 |
| asks | DOUBLE[] | 10档卖价 |
| bidQty | LONG[] | 10档买量 |
| askQty | LONG[] | 10档卖量 |
| tradesCount | LONG | 成交笔数 |
| tickerStatus | SYMBOL | 当前交易状态及标志 |
| auctionPrice | DOUBLE | 波段性中断参考价 |
| auctionQty | LONG | 波段性中断集合竞价虚拟匹配量 |
| lastEnquiryTime | TIMESTAMP | 最近询价时间 |
| bid1Qty | LONG[] | 买一队列 |
| bid1Count | INT | 买一队列的有效委托笔数 |
| maxBid1Count | INT | 买一队列总委托笔数 |
| ask1Qty | LONG[] | 卖一队列 |
| ask1Count | INT | 卖一队列的有效委托笔数 |
| maxAsk1Count | INT | 卖一队列总委托笔数 |

现货快照表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所ID |
| ticker | SYMBOL | 期权代码 |
| lastPrice | DOUBLE | 最新成交价 |
| preClosePrice | DOUBLE | 昨日收盘价 |
| openPrice | DOUBLE | 今日开盘 |
| highPrice | DOUBLE | 当日最高价 |
| lowPrice | DOUBLE | 当日最低价 |
| closePrice | DOUBLE | 今收价 |
| upperLimitPrice | DOUBLE | 涨停价 |
| lowerLimitPrice | DOUBLE | 跌停价 |
| dataTime | TIMESTAMP | 时间戳 |
| qty | LONG | 当日累计成交量 |
| turnover | DOUBLE | 当日累计成交金额 |
| bids | DOUBLE[] | 10档买价 |
| asks | DOUBLE[] | 10档卖价 |
| bidQty | LONG[] | 10档买量 |
| askQty | LONG[] | 10档卖量 |
| tradesCount | LONG | 成交笔数 |
| tickerStatus | SYMBOL | 当前交易状态及标志 |
| totalBidQty | LONG | 委托买入总量，SHL2/SZ有值 |
| totalAskQty | LONG | 委托卖出总量，SHL2/SZ有值 |
| maBidPrice | DOUBLE | 加权平均委买价格，SHL2/SZ有值 |
| maAskPrice | DOUBLE | 加权平均委卖价格，SHL2/SZ有值 |
| maBondBidPrice | DOUBLE | 债券加权平均委买价格，SHL2有值 |
| maBondAskPrice | DOUBLE | 债券加权平均委卖价格，SHL2有值 |
| yieldToMaturity | DOUBLE | 债券到期收益率，SHL2有值 |
| iopv | DOUBLE | 基金实时参考净值，SH/SZ有值 |
| etfBuyCount | INT | ETF申购笔数，SHL2有值 |
| etfSellCount | INT | ETF赎回笔数，SHL2有值 |
| etfBuyQty | DOUBLE | ETF申购数量，SHL2有值 |
| etfBuyMoney | DOUBLE | ETF申购金额，SHL2有值 |
| etfSellQty | DOUBLE | ETF赎回数量，SHL2有值 |
| etfSellMoney | DOUBLE | ETF赎回金额，SHL2有值 |
| totalWarrantExecQty | DOUBLE | 权证执行的总数量，SHL2有值 |
| warrantLowerPrice | DOUBLE | 权证跌停价格，SHL2有值 |
| warrantUpperPrice | DOUBLE | 权证涨停价格，SHL2有值 |
| cancelBuyCount | INT | 买入撤单笔数，SHL2有值 |
| cancelSellCount | INT | 卖出撤单笔数，SHL2有值 |
| cancelBuyQty | DOUBLE | 买入撤单数量，SHL2有值 |
| cancelSellQty | DOUBLE | 卖出撤单数量，SHL2有值 |
| cancelBuyMoney | DOUBLE | 买入撤单金额，SHL2有值 |
| cancelSellMoney | DOUBLE | 卖出撤单金额，SHL2有值 |
| totalBuyCount | LONG | 买入总笔数，SHL2有值 |
| totalSellCount | LONG | 卖出总笔数，SHL2有值 |
| durationAfterBuy | INT | 买入委托成交最大等待时间，SHL2有值 |
| durationAfterSell | INT | 卖出委托成交最大等待时间，SHL2有值 |
| numBidOrders | INT | 买方委托价位数，SHL2有值 |
| numAskORders | INT | 卖方委托价位数，SHL2有值 |
| preIopv | DOUBLE | 基金T-1日净值。SZ有值 |
| bid1Qty | LONG[] | 买一队列 |
| bid1Count | INT | 买一队列的有效委托笔数 |
| maxBid1Count | INT | 买一队列总委托笔数 |
| ask1Qty | LONG[] | 卖一队列 |
| ask1Count | INT | 卖一队列的有效委托笔数 |
| maxAsk1Count | INT | 卖一队列总委托笔数 |

债券快照表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所ID |
| ticker | SYMBOL | 期权代码 |
| lastPrice | DOUBLE | 最新成交价 |
| preClosePrice | DOUBLE | 昨日收盘价 |
| openPrice | DOUBLE | 今日开盘 |
| highPrice | DOUBLE | 当日最高价 |
| lowPrice | DOUBLE | 当日最低价 |
| closePrice | DOUBLE | 今收价 |
| upperLimitPrice | DOUBLE | 涨停价 |
| lowerLimitPrice | DOUBLE | 跌停价 |
| dataTime | TIMESTAMP | 时间戳 |
| qty | LONG | 当日累计成交量 |
| turnover | DOUBLE | 当日累计成交金额 |
| bids | DOUBLE[] | 10档买价 |
| asks | DOUBLE[] | 10档卖价 |
| bidQty | LONG[] | 10档买量 |
| askQty | LONG[] | 10档卖量 |
| tradesCount | LONG | 成交笔数 |
| tickerStatus | SYMBOL | 当前交易状态及标志 |
| totalBidQty | LONG | 委托买入总量(SH,SZ) |
| totalAskQty | LONG | 委托卖出总量(SH,SZ) |
| maBidPrice | DOUBLE | 加权平均委买价格(SZ) |
| maAskPrice | DOUBLE | 加权平均委卖价格(SZ) |
| maBondBidPrice | DOUBLE | 债券加权平均委买价格(SH) |
| maBondAskPrice | DOUBLE | 债券加权平均委卖价格(SH) |
| yieldToMaturity | DOUBLE | 债券到期收益率(SH) |
| matchLastpx | DOUBLE | 匹配成交最近价(SZ) |
| maBondPrice | DOUBLE | 债券加权平均价格(SH) |
| matchQty | LONG | 匹配成交成交量(SZ) |
| matchTurnover | DOUBLE | 匹配成交成交金额(SZ) |
| cancelBuyCount | INT | 买入撤单笔数(SH) |
| cancelSellCount | INT | 卖出撤单笔数(SH) |
| cancelBuyQty | DOUBLE | 买入撤单数量(SH) |
| cancelSellQty | DOUBLE | 卖出撤单数量(SH) |
| cancelBuyMoney | DOUBLE | 买入撤单金额(SH) |
| cancelSellMoney | DOUBLE | 卖出撤单金额(SH) |
| totalBuyCount | LONG | 买入总笔数(SH) |
| totalSellCount | LONG | 卖出总笔数(SH) |
| durationAfterBuy | INT | 买入委托成交最大等待时间(SH) |
| durationAfterSell | INT | 卖出委托成交最大等待时间(SH) |
| numBidOrders | INT[] | 买方委托价位数(SH) |
| numAskOrders | INT | 卖方委托价位数(SH) |
| instrumentStatus | SYMBOL | 状态 |
| bid1Qty | LONG[] | 买一队列 |
| bid1Count | INT | 买一队列的有效委托笔数 |
| maxBid1Count | INT | 买一队列总委托笔数 |
| ask1Qty | LONG[] | 卖一队列 |
| ask1Count | INT | 卖一队列的有效委托笔数 |
| maxAsk1Count | INT | 卖一队列总委托笔数 |

北交所数据表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所ID |
| ticker | SYMBOL | 股票 ID |
| lastPrice | DOUBLE | 最新成交价 |
| preClosePrice | DOUBLE | 昨日收盘价 |
| openPrice | DOUBLE | 今日开盘 |
| highPrice | DOUBLE | 当日最高价 |
| lowPrice | DOUBLE | 当日最低价 |
| closePrice | DOUBLE | 今收价 |
| totalLongPosition | LONG | 未平仓合约数量（张或股） |
| dataTime | TIMESTAMP | 时间戳 |
| qty | LONG | 当日累计成交量 |
| turnover | DOUBLE | 当日累计成交金额 |
| upperLimitPrice | DOUBLE | 涨停价 |
| lowerLimitPrice | DOUBLE | 跌停价 |
| tradesCount | LONG | 成交笔数 |
| tickerStatus | SYMBOL | 当前交易状态及标志 |
| bids | DOUBLE[] | 10档买价 |
| asks | DOUBLE[] | 10档卖价 |
| bidQty | LONG[] | 10档买量 |
| askQty | LONG[] | 10档卖量 |
| bid1Qty | LONG[] | 买一队列 |
| maxBid1Count | INT | 买一队列总委托笔数 |
| bid1Count | INT | 买一队列的有效委托笔数 |
| ask1Qty | LONG[] | 卖一队列 |
| ask1Count | INT | 卖一队列的有效委托笔数 |
| receiveTime | NANOTIMESTAMP | 接收数据时间 |

逐笔委托表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所 ID |
| ticker | SYMBOL | 代码，6位 |
| seq | LONG | 上交所表示业务序号；深交所无意义 |
| dataTime | TIMESTAMP | 时间戳 |
| channelNo | INT | 频道代码 |
| entrustSeq | LONG | 委托序号 |
| price | DOUBLE | 委托价格 |
| qty | LONG | 上交所表示剩余委托数量；深交所表示委托数量 |
| side | CHAR | 上交所：'B'（买）；'S'（卖） 深交所：'1'（买）；'2'（卖）；'G'（借入）；'F'（出借） |
| ordType | CHAR | 上交所：'A'（增加）；'D':（删除） 深交所表示订单类别：'1'（市价）； '2'（限价）；'U'（本方最优） |
| orderNo | LONG | 上交所表示原始订单号；深交所无意义 |

逐笔成交表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所 ID |
| ticker | SYMBOL | 代码，6位 |
| seq | LONG | 上交所表示业务序号；深交所无意义 |
| dataTime | TIMESTAMP | 时间戳 |
| channelNo | INT | 频道代码 |
| tradeSeq | LONG | 成交序号 |
| price | DOUBLE | 成交价格 |
| qty | LONG | 成交量 |
| money | DOUBLE | 成交金额（仅适用上交所） |
| bidNo | LONG | 买方订单号 |
| askNo | LONG | 卖方订单号 |
| tradeFlag | CHAR | 上交所表示内外盘标识（'B'：主动买；'S'：主动卖；'N'：未知） 深交所表示成交标识（'4'：撤；'F'：成交） |

逐笔状态表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所 ID |
| ticker | SYMBOL | 代码，6位 |
| seq | LONG | 上交所表示业务序号；深交所无意义 |
| dataTime | TIMESTAMP | 时间戳 |
| channelNo | INT | 频道代码 |
| statusSeq | LONG | 状态序号 |
| flag | SYMBOL | 状态信息 |

订单簿表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| exchangeID | INT | 交易所 ID |
| ticker | SYMBOL | 代码，6位 |
| lastPrice | DOUBLE | 最近成交价 |
| qty | LONG | 成交总量 |
| turnover | DOUBLE | 成交总金额 |
| tradesCount | LONG | 成交笔数 |
| bids | DOUBLE[] | 十档买价 |
| asks | DOUBLE[] | 十档卖价 |
| bidQty | LONG[] | 十档买量 |
| askQty | LONG[] | 十档卖量 |
| dataTime | TIMESTAMP | 最近成交时间 |

逐笔合并表

| 列名 | 列类型 | 说明 |
| --- | --- | --- |
| SecurityID | SYMBOL | 标的字符串 |
| MDDate | DATE | 日期 |
| MDTime | TIME | 时间 |
| ExchangeType | INT | 1 上证 2 深证 3 新三板 |
| SourceType | INT | 0表示逐笔委托 1表示逐笔成交 -1表示产品状态 |
| Type | INT | 交易类型： 如果是逐笔委托单，则：1表示市价；2表示限价；3表示本方最优；10表示撤单（仅上交所）；11市场状态（仅上交所） 如果是逐笔成交单，则：0表示成交；1表示撤单（仅深交所） |
| Price | LONG | 价格，真实价格\*10000 |
| Qty | LONG | 数量 |
| BSFlag | INT | 买卖方向：1表示买单；2表示卖单 在逐笔成交时，通过买卖订单号判断，如果买单订单号大，就是买单，如果卖单订单号大，就是卖单 |
| BuyNo | LONG | 买方委托序号 |
| SellNo | LONG | 卖方委托序号 |
| ApplSeqNum | LONG | 一个通道内从 1 开始递增的逐笔数据序号 |
| ChannelNo | INT | channel 序号 |

### generateCiphertextAndIV

**语法**

```
XTP::generateCiphertextAndIV(password)
```

**详情**

对传入的明文密码进行加密，并返回加密后的密码和 IV 值，可用于登录。加密算法为 AES-256-CFB。返回一个元组，第一个元素是密文密码，第二个元素是 IV 值，这两个元素的类型都是 INT 类型数组。

**参数**

**password** STRING类型标量，表示明文密码。

## 使用示例

```
XTP::setGlobalConfig(11, "/path/to/log", 5)

stockConn = XTP::createXTPConnection("stockConn")

stockConfig = dict(STRING, ANY);
stockConfig["ip"] = "1.2.3.4";
stockConfig["port"] = 6002;
stockConfig["user"] = "3225";
stockConfig["password"] = "225";
stockConfig["protocalType"] = 1;    //1 是 TCP 2 是 UDP, 测试环境只有TCP
stockConfig["heartBeatInterval"] = 60;

XTP::login(stockConn, stockConfig)

tableDict = dict(STRING, ANY);
share  table(1:0, `exchangeID`ticker`lastPrice`qty`turnover`tradesCount`bids`asks`bidQty`askQty`dataTime, [INT, SYMBOL,DOUBLE, LONG,DOUBLE, LONG, DOUBLE[],DOUBLE[],LONG[],LONG[],TIMESTAMP]) as orderBookTable
tableDict["orderBookTable"] = orderBookTable

XTP::subscribe(stockConn, 3, 1, ["600250", "010504"], tableDict)
XTP::getStatus()
XTP::unsubscribe(stockConn, 3)
```

## 附录

在使用 `createXTPConnection` 接口时，可参考如下使用建议（请以 XTP 官方文档描述为准）：

* 如果需要连接多个 XTP 服务器，则需要创建多个句柄，用每个句柄连接不同的服务器。
* 在登录任一个 XTP 服务器之前，必须创建完毕所有句柄，即在登录后就不允许创建新的句柄，否则会抛出异常。
