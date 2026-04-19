<!-- Auto-mirrored from upstream `documentation-main/plugins/order_management_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 订单管理引擎（Order Management Engine）

OrderManagementEngine 用于创建订单管理引擎，该引擎支持插入行情和委托下单，实现订单撮合、持仓管理和资金计算， 并返回可用现金、持仓结明细等功能。

## 安装插件

### 版本要求

DolphinDB Server 2.00.17/3.00.4 及更高版本，支持 Linux X86。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("OrderManagementEngine")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("OrderManagementEngine")
   ```

## 接口说明

### createOrderManagementEngine

**语法**

```
createOrderManagementEngine(name,config,dummyQuoteTable,
quoteColMap,dummyOrderTable,orderColMap,securityReferenceData,orderDetailsOutput)
```

**详情**

创建一个订单管理引擎。

**参数**

**name** 字符串标量，表示引擎名称，可包含字母，数字和下划线，但必须以字母开头。

**config** 一个字典， 用于配置引擎的行为。每个 Key 对应一个功能参数。可配置 Key 的说明如下：

| 字典 Key | 含义 |
| --- | --- |
| cash | 初始资金，可选，默认 0 |
| commission | 手续费，可选，默认 0 |
| tax | 印花税，可选，默认 0 |
| dataType | 行情类别：  * 1：股票快照 * 6：期货快照 |
| latency | 模拟时延（毫秒），用于模拟用户订单从发出到被处理的延迟。  * latency=-1   ，订单会即时撮合。目前仅股票逐笔、股票快照、银行间现券/上交所债券快照支持 * latency > 0 ， 当最新行情时间 >订单时间+ latency   时，开始撮合该用户订单 * latency = 0 ，当最新行情时间>=订单时间+ latency 时，开始撮合用户订单 |
| orderBookMatchingRatio | 与盘口撮合的成交百分比，不能小于0 |
| matchingMode | 根据快照行情是否带有区间成交明细信息，可以有两种撮合模式，可设置为 1 或者 2：   * 1：与最新成交价以及对手方盘口按配置的比例撮合（快照行情无区间成交明细信息时） * 2：与区间的成交列表以及对手方盘口撮合成交（快照行情带有区间成交明细信息时） |
| matchingRatio | 快照模式下，快照的区间成交百分比，默认和成交百分比 *orderBookMatchingRatio* 相等 |
| outputRejectDetails | 是否输出用户订单或撤单被拒绝的具体原因，默认 false |
| userDefinedOrderId | 该参数为 true 时，insertMsg 的 orderId 为用户设置的外部订单号，订单明细表新增一列 userOrderId，为此订单号。默认为 false。 |
| mutualTrigger | 设置委托确认和撤单触发方式   * false（默认）：基于模拟撮合引擎接收到的该标的的最新行情时间触发； * true：基于模拟撮合引擎接收到的最新行情时间触发；   目前仅支持 dataType = 1 |

**dummyQuoteTable** 插入行情数据表的结构。引擎实际使用的字段通过 *quoteColMap*
与行情表中的列名进行映射。

**quoteColMap** 一个字典，类型为 (STRING, STRING) ，用于指定行情数据表中各列与引擎内部字段之间的映射关系。

**dummyOrderTable** 用于插入订单明细数据的表结构。引擎实际使用的字段通过参数 *orderColMap*
与该表中的实际列名进行映射。

**orderColMap** 一个字典标量，类型为 (STRING, STRING)，用于定义订单明细数据表中各列与引擎内部字段之间的映射关系。

其中，订单表必须提供的列如下：

| 名称 | 类型 | 含义 |
| --- | --- | --- |
| symbol | SYMBOL 或 STRING | 股票标的 |
| sendTime | TIMESTAMP | 订单发送时间 |
| orderType | INT | 订单类型 |
| direction | INT | 订单方向  1：买开，2卖开，3：卖平，4：买平 |
| orderPrice | DOUBLE | 订单价格 |
| orderQty | INT | 订单数量 |
| effectiveTime | TIMESTAMP | 交易开始时间 |
| expireTime | TIMESTAMP | 交易过期时间 |
| label | STRING | 订单标签信息 |
| symbolSource | STRING | 交易所信息 |
| stopPrice | DOUBLE | 止损价 |
| timeInForce | INT | 委托订单有效性：  0：当日有效（默认）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK） |

**securityReferenceData** 基本信息表，*config* 中设置 dataType 为1（股票）时置为空。

| 名称代码 | 类型 | 名称 |
| --- | --- | --- |
| symbol | SYMBOL 或 STRING | 合约代码 |
| multiplier | DOUBLE | 合约乘数 |
| marginRatio | DOUBLE | 保证金比率 |
| tradeUnit | DOUBLE | 合约单位 |
| priceUnit | DOUBLE | 报价单位 |
| priceTick | DOUBLE | 价格最小变动单位 |
| commission | DOUBLE | 费用 |
| deliveryCommissionMode | INT | 计费方式：  1：费用\*手数  2：费用\*金额 |

**orderDetailsOutput**
订单详情结果输出表(包括用户订单委托回报，成交、拒单以及撤单状态)，设置该参数时可以把成交明细表数据实时推送到该表中。

* 在配置项 *outputRejectDetails* 为 true 时（详见本接口的 *config* 参数说明），启用
  outputRejectDetails 列。
* 在配置项 *userDefinedOrderId* 为 true 时，输出 userOrderId 列。

  | 名称 | 类型 | 含义 |
  | --- | --- | --- |
  | orderId | LONG | 成交的用户订单 ID |
  | symbol | STRING | 股票标的 |
  | direction | INT | 订单方向 |
  | sendTime | TIMESTAMP | 订单发送时间 |
  | orderPrice | DOUBLE | 委托价格 |
  | orderQty | LONG | 订单委托数量 |
  | tradeTime | TIMESTAMP | 成交时间 |
  | tradePrice | DOUBLE | 成交价格 |
  | tradeQty | LONG | 成交量 |
  | orderStatus | INT | 用户订单是否完全成交 + 4：已报 + -2：表示撤单被拒绝 + -1：表示订单被拒绝 + 0：表示订单部分成交 + 1：表示订单完全成交 + 2：表示订单被撤单 |
  | orderReceiveTime | NANOTIMESTAMP | 订单收到时的时间（系统时间） |
  | effectiveTime | TIMESTAMP | 交易开始时间 |
  | expireTime | TIMESTAMP | 交易过期时间 |
  | cumTradeQty | LONG | 累计成交量 |
  | tradeAvgPrice | DOUBLE | 成交平均价 |
  | label | STRING | 订单标记 |
  | userOrderId | LONG | 用户设置的外部订单号 |
  | rejectDetails | STRING | 用户订单、用户撤单的具体拒单原因 |
  | openVolumeWithBetterPrice | LONG | 优于委托价格的行情未成交委托单总量 |
  | openVolumeWithWorsePrice | LONG | 次于委托价格的行情未成交委托单总量 |
  | openVolumeAtOrderPrice | LONG | 等于委托价格行情未成交委托单总量 |
  | priorOpenVolumeAtOrderPrice | LONG | 等于委托价格行情且比自己早的行情未成交委托单总量 |
  | depthWithBetterPrice | INT | 优于委托价格的行情档位数 |

**返回值**

一个引擎句柄

### getEngineList

**语法**

```
getEngineList()
```

**详情**

查询所有的订单管理引擎。

**参数**

无

**返回值**

返回一个字典，键是引擎名称，值是引擎句柄。

### dropEngine

**语法**

```
dropEngine(engine)
```

**详情**

删除指定的订单管理引擎。

**参数**

**engine** 通过 `createOrderManagementEngine` 接口创建或从
`getEngineList`返回值中得到的引擎句柄。

**返回值**

无

### insertMsg

**语法**

```
insertMsg(engine, msgBody, msgType)
```

**详情**

向引擎中插入行情和订单数据。

**参数**

**engine** 通过 `createOrderManagementEngine` 接口创建或从
`getEngineList`返回值中得到的引擎句柄。

**msgBody** 行情或订单数据。行情数据仅支持表格形式，而订单数据支持表格或元组形式。

**msgType** 数据类型标识，1 表示行情，2 表示订单。

**返回值**

* 当 msgType 为 1 时无返回值。
* 当 msgType 为 2 时，返回一个由订单 id 组成的 LONG 类型向量。

### getAvailableCash

**语法**

```
getAvailableCash(engine)
```

**详情**

查询账户可用现金。

**参数**

**engine** 通过 `createOrderManagementEngine` 接口创建或从
`getEngineList`返回值中得到的引擎句柄。

**返回值**

DOUBLE 类型标量。

### getPosition

**语法**

```
getPosition(engine,symbol="")
```

**详情**

获取持仓信息。

**参数**

**engine** 通过 `createOrderManagementEngine` 接口创建或从
`getEngineList`返回值中得到的引擎句柄。

**symbol** 可选参数，字符串类型，表示股票代码。

**返回值**

返回一个包含持仓信息的表，包含如下字段：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨买持仓量 |
| lastDayShortPosition | 昨卖持仓量 |
| longPosition | 买持仓量 |
| longPositionAvgPrice | 买成交均价 |
| shortPosition | 卖持仓量 |
| shortPositionAvgPrice | 卖成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todayBuyValue | 当日买成交金额 |
| todaySellVolume | 当日卖成交数量 |
| todaySellValue | 当日卖成交金额 |

### cancelOrder

**语法**

```
cancelOrder(engine, orderId)
```

**详情**

清空内部缓存的所有订单信息以及行情信息。

**参数**

**engine** 通过 `createOrderManagementEngine` 接口创建或从
`getEngineList`返回值中得到的引擎句柄。

**orderId** 字符串标量，表示订单 ID。

**返回值**

无

## 示例

创建一个订单管理引擎并插入行情和订单，最后查看交易明显和持仓明显。

数据文件：<data/order_management_engine/data.csv>

```
try{loadPlugin("path/PluginMatchingEngineSimulator.txt")}catch(ex){print ex}
try{loadPlugin("path/PluginOrderManagementEngine.txt")}catch(ex){print ex}
go

// 行情订单输入表和交易明细输出表结构
dummyQuoteTable = table(1:0, `symbol`symbolSource`timestamp`lastPrice`upLimitPrice`downLimitPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty, [STRING,STRING,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE[],LONG[],DOUBLE[],LONG[]])
quoteColMap = dict( `symbol`symbolSource`timestamp`lastPrice`upLimitPrice`downLimitPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty, `symbol`symbolSource`timestamp`lastPrice`upLimitPrice`downLimitPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty)
dummyOrderTable = table(1:0, `symbol`sendTime`orderType`direction`orderPrice`orderQty`effectiveTime`expireTime`label`orderId, [STRING,TIMESTAMP,INT,INT,DOUBLE,LONG,TIMESTAMP,TIMESTAMP,STRING,LONG])
orderColMap = dict(`symbol`sendTime`orderType`direction`orderPrice`orderQty`effectiveTime`expireTime`label`orderId, `symbol`sendTime`orderType`direction`orderPrice`orderQty`effectiveTime`expireTime`label`orderId)
orderDetailsOutput = table(1:0, `orderId`symbol`direction`sendTime`orderPrice`orderQty`tradeTime`tradePrice`tradeQty`orderStatus`orderReceiveTime`effectiveTime`expireTime`cumTradeQty`tradeAvgPrice`label`userOrderId`rejectDetails`openVolumeWithBetterPrice`openVolumeWithWorsePrice`openVolumeAtOrderPrice`priorOpenVolumeAtOrderPrice`depthWithBetterPrice`receiveTime`startMatchTime`endMatchTime, [LONG, STRING, INT, TIMESTAMP, DOUBLE, LONG, TIMESTAMP, DOUBLE, LONG, INT, NANOTIMESTAMP, TIMESTAMP, TIMESTAMP, LONG, DOUBLE, STRING,LONG,STRING,LONG,LONG,LONG,LONG,INT,TIMESTAMP, NANOTIMESTAMP, NANOTIMESTAMP])

// 配置项
config = dict(STRING, DOUBLE);
config["cash"] = 100000;
config["dataType"] = 1;
config["latency"] = 0;
config["orderBookMatchingRatio"] = 0.1;
config["matchingMode"] = 1;
config["matchingRatio"] = 0.1;
config["outputRejectDetails"] = true;
config["userDefinedOrderId"] = true;
config["outputQueuePosition"]= 1
config["outputTimeInfo"]= 1
config["commission"]= 0
config["tax"]= 0

// 创建引擎
engineName = "engine_stock"
try{OrderManagementEngine::dropEngine(engineName)}catch(ex){};go // 如果已存在同名引擎则先删除
engine = OrderManagementEngine::createOrderManagementEngine(engineName,config,dummyQuoteTable,quoteColMap,dummyOrderTable,orderColMap,,orderDetailsOutput)

// 加载数据
schema = extractTextSchema("path/data.csv")
update schema set type = "STRING" where name = "symbol" or name = "symbolSource"
update schema set type = "LONG" where name = "totalBidQty" or name = "totalOfferQty"
update schema set type = "DOUBLE[]" where name = "bidPrice" or name = "offerPrice"
update schema set type = "LONG[]" where  name = "bidQty" or name = "offerQty"
data = loadText("path/OrderManagementEngine/data.csv",,schema)

// 插入行情和订单
OrderManagementEngine::insertMsg(engine, data, 1)
OrderManagementEngine::insertMsg(engine,("688171.XSHG", 2022.04.11 09:30:38.000, 1, 1, 0.0, 200l,,, "buy open", 1l),2)
OrderManagementEngine::insertMsg(engine,("688171.XSHG", 2022.04.11 09:30:38.000, 1, 2, 0.0, 200l,,, "sell open", 2l),2)

// 查看结果
orderDetailsOutput // 交易明细
OrderManagementEngine::getPosition(engine) // 持仓明细
```
