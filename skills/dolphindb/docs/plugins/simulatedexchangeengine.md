<!-- Auto-mirrored from upstream `documentation-main/plugins/simulatedexchangeengine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SimulatedExchangeEngine

DolphinDB 的 SimulatedExchangeEngine
插件实现了一个完整的模拟交易所系统，支持接收行情快照数据与交易员委托订单，实时构建订单簿，支持将不同的订单委托撮合成交。该插件可输出交易明细与订单明细，为量化策略回测提供真实的交易环境模拟。

## 安装插件

### 版本要求

DolphinDB Server 2.00.16 和 3.00.4，支持 Linux x86-64。

**注**：该插件仅支持 DolphinDB 商业版。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   **注**：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("SimulatedExchangeEngine")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("SimulatedExchangeEngine")
   ```

## 接口说明

### createSimulatedExchangeEngine

**语法**

```
SEEPlugin::createSimulatedExchangeEngine(name, config, quoteColMap)
```

**详情**

创建一个模拟交易所。返回一个句柄，可以用于其他接口。

**参数**

* **name** 字符串标量，交易所唯一标识，不能为空字符串。
* **config** 键为 STRING 类型的字典，表示模拟交易所引擎的配置项。目前支持的配置如下表：

  | 配置项 | 类型/形式 | 说明 |
  | --- | --- | --- |
  | marketType | STRING | 必填，市场类型，目前仅支持 “CFETS\_XBOND”。 |
  | outputInterval | INT | 选填，表示输出快照的最小间隔，单位为毫秒，默认值为 3000。可选值：  + 小于等于 0：表示不输出快照； + 大于等于 1000：当快照发生变化时，按此间隔输出快照。 |
  | forceTriggerInterval | INT | 选填，表示输出快照的最大间隔，单位为毫秒。默认值为 60000。可选值：  + 小于等于 0：表示不强制输出快照； + 大于等于 1000：当快照长时间无变化时，超过 *forceTriggerInterval*也会强制输出一次快照。 **注：**当 *forceTriggerInterval* 生效时（≥ 1000），其值必须大于 *outputInterval*。 |
  | sessionBegin | SECOND 向量 | 选填，表示快照输出时间区间的起止时刻。传入的时间区间必须按顺序从早到晚递增，且不能重叠。 |
  | sessionEnd | SECOND 向量 |
  | quotePriority | INT | 必填，表示行情撮合的优先级：  + 0：表示用户订单优先与用户订单撮合； + 1：表示用户订单优先与行情虚拟订单撮合。 |
  | checkQuote | INT | 选填，表示是否会校验债券报价数据的合理性，即 bidYTM, bidYTC, askClean, askDirty 为严格递增，bidDirty, askTYM, askYTC 为严格递减；dirtyPrice, cleanPrice 的买一价小于卖一价，YTM, YTC 的买一价大于卖一价。可选值：  + 1：默认值，校验； + 0：不校验上述内容，由用户自行保证。 |
  | user | 表 | 选填，表示用户信息表。表结构如下：  + userName，STRING，用户名称； + userId，INT，用户 ID； + password，STRING，用户密码； + isValid，BOOL，用户是否有效。 |
  | userGroup | 表 | 选填，表示用户组信息表。表结构如下：  + groupName，STRING，用户组名称； + groupId，INT，用户组 ID； + groupType，STRING，用户组类型； + priority，INT，用户组优先级； + userId，INT[]，该用户组包含的用户 ID。 |
  | riskControl | 表 | 选填，表示风控配置表。表结构如下：  + userId，INT，用户 ID； + maxDailyOrderCount，INT/LONG，每日最大订单数量限制； + maxDailyTradeAmount，LONG/DOUBLE，每日最大交易金额限制； + orderSubmissionRate，INT，订单提交速率限制； + priceDeviationLimit，DOUBLE，价格偏差限制； + yieldDeviationBP，DOUBLE，收益率偏差限制（基点）。 |
  | blackWhiteList | 表 | 选填，表示黑白名单配置表。表结构如下：  + groupId，INT，用户组 ID； + black，INT[]，黑名单用户 ID； + white，INT[]，白名单用户 ID。 |
  | bondDetail | 表 | 选填，表示债券详细信息表。表结构如下：  + symbol，STRING，债券代码； + symbolSource，STRING，债券来源； + bondType，STRING，债券类型； + maturity，DOUBLE，到期期限； + duration，DOUBLE，久期； + prevCleanPrice，DOUBLE，前一日净价； + prevDirtyPrice，DOUBLE，前一日全价； + prevYTM，DOUBLE，前一日到期收益率； + prevYTC，DOUBLE，前一日赎回收益率； + internalRating，STRING，内部评级； + externalRating，STRING，外部评级； + issuanceMethod，STRING，发行方式。 |

  **注：**上述表中，STRING 类型的列也可以支持 SYMBOL 类型。

* **quoteColMap** 一个字典，类型为 (string, string)，用于映射行情表中的列名。映射规则为“必须的列名 →
  实际表中的列名”。必须的列名如下表所示：

  | 名称 | 表中对应列的类型 | 说明 |
  | --- | --- | --- |
  | symbol | STRING | 标的 |
  | symbolSource | STRING | 交易所 |
  | settlType | INT | 清算速度，可选值包括：  + 0：T0，当日清算； + 1：T1，交易日后一个工作日清算； + 2：T2，交易日后两个工作日清算。 |
  | bidQty | LONG[] | 买数量 |
  | bidYTM | DOUBLE[] | 买到期收益率 |
  | bidYTC | DOUBLE[] | 买行权收益率（可选） |
  | bidCleanPrice | DOUBLE[] | 买委托净价 |
  | bidDirtyPrice | DOUBLE[] | 买委托全价（可选） |
  | askQty | LONG[] | 卖数量 |
  | askYTM | DOUBLE[] | 卖到期收益率 |
  | askYTC | DOUBLE[] | 卖行权收益率（可选） |
  | askCleanPrice | DOUBLE[] | 卖委托净价 |
  | askDirtyPrice | DOUBLE[] | 卖委托净价（可选） |
  | YTM | DOUBLE | 最新到期收益率 |
  | YTC | DOUBLE | 最新行权收益率（可选） |
  | cleanPrice | DOUBLE | 最新净价 |
  | dirtyPrice | DOUBLE | 最新全价（可选） |

### insertMsg

**语法**

```
SEEPlugin::insertMsg(engine, msg)
```

**详情**

插入深度行情表。

**参数**

* **engine** 交易所句柄。
* **msg** 行情表。表结构在首次调用接口后将被锁定，不可修改。表中必须包含在创建交易所时，由 *quoteColMap*
  指定的列。

**注：**

1. 行情中 askYield 必须是递减排序，bidYield 必须是递增排序，否则交易所行为未定义。
2. askYield、askQty、askSettlType 长度相同；bidYield、bidQty、bidSettlType 长度相同。

### submitOrder

**语法**

```
SEEPlugin::submitOrder(engine, msg)
```

**详情**

插入用户订单。撤单请使用 `cancelOrder`。

**参数**

* **engine** 交易所句柄。
* **msg** 一个元组，表示用户订单信息。按顺序包含如下信息：

  + symbol：STRING 类型标量，表示标的。
  + symbolSource：STRING 类型标量，表示市场。
  + orderType：整型标量，目前只支持 1，表示限价单。
  + settlType：整型标量，表示清算速度，可选值包括：0-当日清算，1-交易日后一个工作日清算，2-交易日后两个工作日清算。
  + matchPrice：字符串标量。表示价格类型。
  + direction：整型标量。可选值包括：1-买，2-卖。
  + price：浮点型标量，表示价格。
  + qty：整型标量，表示数量。
  + userOrderId：字符串标量，表示用户自定义编号。
  + traderId：整型标量，表示交易员编号。
  + timeInForce：整型标量，表示委托订单有效性。可选值包括：0-默认，1-FOK，2-FAK。
  + expirationTime：TIME 类型标量，表示委托订单的到期时间，可填空值。非空时要求时间晚于当前时间，否则无效。
  + label：字符串标量，表示标签。

### dropSimulatedExchangeEngine

**语法**

```
SEEPlugin::dropSimulatedExchangeEngine(engine)
```

**详情**

删除该交易所。

**参数**

* **engine** 交易所句柄。

### getOutputSchema

**语法**

```
SEEPlugin::getOutputSchema(engine, outputType)
```

**详情**

获取输出表的结构。

**参数**

* **engine** 交易所句柄。
* **outputType** 字符串标量，支持 orderDetails、tradeDetails 以及 snapshot。

snapshot 表结构参见 [getSnapshot](#topic_xcx_gnl_qhc) 章节。

orderDetails 表结构如下：

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| symbol | STRING | 标的 |
| submitTime | TIMESTAMP | 下单时间 |
| writeTime | TIMESTAMP | 写入表时间 |
| symbolSource | STRING | 市场 |
| orderType | INT | 委托类型 |
| settlType | INT | 清算速度 |
| matchPrice | STRING | 价格类型 |
| direction | INT | 方向 |
| price | DOUBLE | 价格 |
| qty | LONG | 量 |
| userOrderId | STRING | 客户自定义编号 |
| traderId | INT | 交易员号 |
| timeInForce | INT | 委托订单有效性 |
| label | STRING | 标签 |
| orderId | LONG | 订单号 |
| status | INT | 委托状态。其中：  0：未成交，2：部分成交，4：已成交，5：全部撤单，6：部分撤单，7：拒单 |
| remainedQty | LONG | 未成交量 |
| turnover | DOUBLE | 成交总额 |
| orderInfo | STRING | 订单拒单等时的详细信息（正常订单该字段为空） |

tradeDetails 表结构如下：

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| symbol | STRING | 标的 |
| settlType | INT | 清算速度 |
| tradeTime | TIMESTAMP | 成交时间 |
| tradeId | LONG | 成交编号 |
| bidUserOrderId | STRING | 客户自定义买编号 |
| askUserOrderId | STRING | 客户自定义卖编号 |
| symbolSource | STRING | 市场 |
| direction | INT | 方向 |
| tradePrice | DOUBLE | 成交价格 |
| matchPrice | STRING | 价格类型 |
| tradeQty | LONG | 成交数量 |
| bidOrderId | LONG | 买委托订单号 |
| askOrderId | LONG | 卖委托订单号 |
| bidTraderId | INT | 买交易员 |
| askTraderId | INT | 卖交易员 |

### setOutput

**语法**

```
SEEPlugin::setOutput(engine, output)
```

**详情**

设置输出表。如果设置了快照表，满足快照输出条件时，将当前快照输出到该表中。

**参数**

* **engine** 交易所句柄。
* **output** 键为 STRING 类型的字典，用于设置输出表。字典的 key 支持
  orderDetails、tradeDetails 以及 snapshot。

### getSnapshot

**语法**

```
SEEPlugin::getSnapshot(engine, symbolSource, symbol, settlType, matchPrice)
```

**详情**

获取快照。

**参数**

* **engine** 交易所句柄。
* **symbolSource** 字符串标量，表示市场。
* **symbol** 字符串标量，用于指定标的。
* **settlType** 整型标量，表示清算速度，支持 0 (T0)、1 (T1)、2 (T2)。
* **matchPrice** 字符串标量，表示价格类型。

返回的表结构如下：

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| symbol | STRING | 标的代码 |
| symbolSource | STRING | 市场 |
| timestamp | TIMESTAMP | 时间 |
| settlType | INT | 清算速度 |
| matchPrice | STRING | 价格类型 |
| bidQty | LONG[] | 报买量（元） |
| bidPrice | DOUBLE[] | 报买到期收益率、行情收益率、净价或者全价 |
| bidParty | INT[] | 买报价方，traderId 数组 |
| askQty | LONG[] | 卖单数量列表 |
| askPrice | DOUBLE[] | 报买到期收益率、行情收益率、净价或者全价 |
| askParty | INT[] | 卖报价方，traderId 数组 |
| lastPrice | DOUBLE | 最新成交价 |
| tradeQty | LONG | 总成交数量 |

### cancelOrder

**语法**

```
SEEPlugin::cancelOrder(engine, orderId, [traderId], [label=""])
```

**详情**

根据订单 ID 取消订单，或者根据 *traderID* 和 *label* 取消订单。

当 *orderID* 不为空值时，系统根据指定的订单 ID 执行撤单操作。

当 *orderID* 为空值时，系统根据 *traderID* 和 *label* 撤单。

**参数**

* **engine** 交易所句柄。
* **orderID** 整型标量，订单 ID。
* **traderID** 可选参数，字符串标量，交易员号。
* **label** 可选参数，字符串标量，订单标签。

### getOrderStatus

**语法**

```
SEEPlugin::getOrderStatus(engine, orderId, [traderId])
```

**详情**

根据订单 ID *orderId* 或者交易员号 *traderId* 获取订单信息。当 *orderId* 非空时，按照订单 ID
获取信息，当 *orderId* 为空时，按照 *traderId* 获取信息。

返回的表的结构与 orderDetails 表相似，仅缺少 writeTime 列。

**参数**

* **engine** 交易所句柄。
* **orderId** 整型数值，表示订单 ID。
* **traderId** 整型数值。

### resetSimulatedExchangeEngine

**语法**

```
SEEPlugin::resetSimulatedExchangeEngine(engine)
```

**详情**

重置交易所。取消所有尚未成交的用户订单，清空内部的所有行情。

**参数**

* **engine** 交易所句柄。

### getEngineList

**语法**

```
SEEPlugin::getEngineList()
```

**详情**

获取当前存在的所有交易所引擎。返回一个 key 为 name、value 为 engine 的字典对象。

### setSecurityReference

**语法**

```
SEEPlugin::setSecurityReference(engine, securityReferenceData)
```

**详情**

设置基本信息表，用于追加或修改 *config* 中的基础信息。

**参数**

* **engine** 交易所句柄。
* **securityReferenceData** 一个字典，表示可以动态增加相应的基本表数据。其 key 为 user,
  userGroup, riskControl, blackWhiteList, bondDetail。

## 使用示例

下例展示 SimulatedExchangeEngine 插件各接口的基本使用方法。

1. 加载/安装插件

   ```
   // 安装插件
   login("admin", "123456")
   listRemotePlugins()
   installPlugin("SimulatedExchangeEngine")
   loadPlugin("SimulatedExchangeEngine")
   ```
2. 准备数据

   ```
   // 创建用户表
   user = table(1:0, `userName`userId`password`isValid, [STRING,INT,STRING,BOOL])
   for(userId in 1..22){
       insert into user values("user"+string(userId), userId, "123456", true)
   }

   // 创建用户组表
   userGroup = table(1:0, `groupName`groupId`groupType`priority`userId, [STRING,INT,STRING,INT,INT[]])
   insert into userGroup values("group1", 1, "做市", 1, [[1,2,3,4,5,6,7,8,9,10]])
   insert into userGroup values("group2", 2, "经营", 31, [[13,14]])
   insert into userGroup values("group3", 3, "经营", 32, [[15,16]])
   insert into userGroup values("group4", 4, "经营", 33, [[17,18]])
   insert into userGroup values("group5", 5, "经营", 34, [[19,20]])
   insert into userGroup values("group6", 6, "做市", 3, [[11,12]])
   insert into userGroup values("group7", 7, "经营", 36, [[21,22]])

   // 定义价格转换函数
   def convert(matchType, value){
       if(matchType == 'YTM'){
           t = (5 - value) \ 4.5
       }else if(matchType == 'YTC'){
           t = sqrt((5 - value) \ 4.5)
       }else if(matchType == 'CleanPrice'){
           t = (value - 20) \ 20
       }else{
           t = sqrt((value - 20) \ 20)
       }
       YTM = 5 - 4.5 * t
       YTC = 5 - 4.5 * pow(t, 2)
       CleanPrice = 20 + 20 * t
       DirtyPrice = 20 + 20 * pow(t, 2)
       return {'YTM': YTM, 'YTC': YTC, 'CleanPrice': CleanPrice, 'DirtyPrice': DirtyPrice}
   }

   // 创建债券详细信息表
   symbol = lpad(string(0..30), 5, "0")
   bondType = take("国债", size(symbol))
   maturity = take(1.0, size(symbol))
   duration = take(1.0, size(symbol))
   price1 = convert("CleanPrice", 25.58735610)
   price2 = convert("CleanPrice", 25.387)
   prevCleanPrice = take([25.58735610, 25.387], size(symbol))
   prevDirtyPrice = take([price1.DirtyPrice, price2.DirtyPrice], size(symbol))
   prevYTM = take([price1.YTM, price2.YTM], size(symbol))
   prevYTC = take([price1.YTC, price2.YTC], size(symbol))
   internalRating = take("AAA", size(symbol))
   externalRating = take("AAA", size(symbol))
   issuanceMethod = take("YEAR", size(symbol))
   bondDetail = table(symbol, take("ESP", size(symbol)) as symbolSource, bondType, maturity, duration,
       prevCleanPrice, prevDirtyPrice, prevYTM, prevYTC, internalRating, externalRating, issuanceMethod)
   ```
3. 插件各接口的基本使用方法

   ```
   // 创建模拟交易所引擎
   config = dict(STRING, ANY)
   config["marketType"] = "CFETS_XBOND"
   config["quotePriority"] = 0
   config["user"] = user
   config["userGroup"] = userGroup
   config["bondDetail"] = bondDetail
   quoteColMap = dict(
       `symbol`symbolSource`settlType`bidQty`bidYTM`bidYTC`bidCleanPrice`bidDirtyPrice`askQty`askYTM`askYTC`askCleanPrice`askDirtyPrice`YTM`YTC`cleanPrice`dirtyPrice,
       `symbol`symbolSource`settlType`bidQty`bidYTM`bidYTC`bidCleanPrice`bidDirtyPrice`askQty`askYTM`askYTC`askCleanPrice`askDirtyPrice`YTM`YTC`cleanPrice`dirtyPrice
   )
   engine = SEEPlugin::createSimulatedExchangeEngine("simulatedTest", config, quoteColMap)

   // 创建输出表
   // 获取订单明细表结构
   orderSchema = SEEPlugin::getOutputSchema(engine, "orderDetails")
   // 获取成交明细表结构
   tradeSchema = SEEPlugin::getOutputSchema(engine, "tradeDetails")
   // 获取快照表结构
   snapshotSchema = SEEPlugin::getOutputSchema(engine, "snapshot")
   // 创建输出表
   tradeTable = table(1:0, `symbol`settlType`tradeTime`traderID`bidUserOrderID`askUserOrderID`symbolSource`direction`tradePrice`matchPrice`tradeQty`bidOrderID`askOrderID`bidtraderID`asktraderID, [STRING,INT,TIMESTAMP,LONG,STRING,STRING,STRING,INT,DOUBLE,STRING,LONG,LONG,LONG,INT,INT])
   // 设置输出表
   outputDict = dict(STRING, ANY)
   outputDict = dict(STRING, ANY)
   outputDict["tradeDetails"] = tradeTable
   SEEPlugin::setOutput(engine, outputDict)

   // 提交用户订单
   // 卖单
   SEEPlugin::submitOrder(engine, ("00001", "ESP", 1, 2, "YTM", ORDER_SEL, 3.9, 300000, "1", 1, DEFAULT, NULL, ""))
   // 买单
   SEEPlugin::submitOrder(engine, ("00001", "ESP", 1, 2, "YTM", ORDER_BUY, 3.78, 350000, "1", 2, DEFAULT, time(), ""))

   // 插入行情数据
   price1 = each(convert{"CleanPrice"}, [23.67, 23.78, 23.8, 23.9, 24.0, 24.1])
   price2 = each(convert{"CleanPrice"}, [23.65, 23.4, 23.3, 23.2, 23.1, 23.0])
   price3 = convert("CleanPrice", 23.66)
   SEEPlugin::insertMsg(engine, ("00001", "ESP", 2,
       [100000, 100000, 100000, 100000, 100000, 100000],
       price2.YTM, price2.YTC, price2.CleanPrice, price2.DirtyPrice,
       [100000, 100000, 100000, 100000, 100000, 100000],
       price1.YTM, price1.YTC, price1.CleanPrice, price1.DirtyPrice,
       price3.YTM, price3.YTC, price3.CleanPrice, price3.DirtyPrice))

   // 查询订单状态
   // 根据交易员 ID 查询
   res = SEEPlugin::getOrderStatus(engine, , 1)
   select * from res
   // 根据订单 ID 查询
   res = SEEPlugin::getOrderStatus(engine, 1, )
   select * from res

   // 获取指定标的快照
   snapshot = SEEPlugin::getSnapshot(engine, "ESP", "00001", 2, "YTM")
   select * from snapshot

   // 根据订单 ID 撤单
   SEEPlugin::cancelOrder(engine, 1)

   // 修改基本信息
   // 设置黑白名单
   blackwhite = table(
       [1, 3] as groupId,
       arrayVector([3, 5], [1, 3, 6, 1, 6]) as black,
       arrayVector([1, 2], [int(), int()]) as white
   )
   SEEPlugin::setSecurityReference(engine, {"blackWhiteList":blackwhite})
   // 设置风控配置
   userId = user.userId
   n = size(userId)
   maxDailyOrderCount = long(100 + rand(10000, n))
   maxDailyTradeAmount = long(200000000 + rand(10000, n))
   orderSubmissionRate = take(200, n)
   priceDeviationLimit = take(200.0, n)
   yieldDeviationBP = take(200.03, n)
   riskTb = table(userId, maxDailyOrderCount, maxDailyTradeAmount, orderSubmissionRate, priceDeviationLimit, yieldDeviationBP)
   SEEPlugin::setSecurityReference(engine, {"riskControl":riskTb})

   // 获取交易所列表
   // 获取所有交易所引擎
   engineList = SEEPlugin::getEngineList()
   engineList.keys()
   // 通过名称获取引擎句柄
   myEngine = engineList["simulatedTest"]

   // 重置交易所
   SEEPlugin::resetSimulatedExchangeEngine(engine)

   // 删除交易所引擎
   SEEPlugin::dropSimulatedExchangeEngine(engine)
   ```
