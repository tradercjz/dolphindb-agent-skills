<!-- Auto-mirrored from upstream `documentation-main/plugins/backtest/stock.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 股票回测配置

回测平台支持的股票资产行情数据类型包括：逐笔或逐笔+快照，快照，快照+逐笔成交明细，分钟频率，日频，逐笔（宽表），逐笔+快照（宽表），快照+分钟频率等。

## 引擎配置说明

接口 `createBacktester` 的参数 *config* 和接口
`createBacktestEngine` 的参数 *userConfig*
的配置可参考下表（注意股票回测的策略类型需要设置为“stock”）：

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "startDate" | 开始日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "endDate" | 结束日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "strategyGroup" | 策略类型 | 必须配置，“stock” |
| "cash" | 初始资金 | 必须配置，DOUBLE 类型 |
| "commission" | 手续费 | DOUBLE 类型，默认为 0.0 |
| "tax" | 印花税 | DOUBLE 类型，默认为 0.0 |
| "dataType" | 行情类型 | 必须配置，INT 类型，可选值为： 0：股票逐笔（逐笔委托和逐笔成交明细）+快照  1：快照  2：快照+逐笔成交明细  3：分钟频率  4：日频  5：股票逐笔（逐笔委托和逐笔成交明细合并为宽表）  6：股票逐笔+快照（逐笔委托、逐笔成交明细和快照合并为宽表）  7：快照+分钟频率（该模式仅由接口 `createBacktester` 创建的引擎支持，且不支持 JIT） |
| “frequency” | 逐笔数据以指定频率合成快照  或快照数据以指定频率合成 bar | INT 类型，默认为 0  * 当 dataType=0（逐笔）或 dataType = 5   时必须配置frequency>0，系统将逐笔数据合成 *frequency*   频率的快照，并以此触发onSnapshot 回调函数 * dataType=1 或 2 时，若配置 frequency>0，系统将快照数据合成   *frequency* 频率的 bar 数据，并以此触发onBar 回调函数 |
| "msgAsTable" | 行情的数据格式 | BOOL 类型，默认 false false：字典  true：表 （只能通过接口createBacktestEngine 创建引擎） |
| “matchingMode“ | 订单撮合模式 | INT 类型，可选值为： 1：   * 日频：以收盘价撮合订单 * 分钟频：行情时间大于订单时间时撮合订单   2：   * 日频：以开盘价撮合订单 * 分钟频：行情时间等于订单时间时以当前行情的收盘价撮合订单，后续未完成订单撮合订单同 1   3：以委托价格成交。  注： * 当 dataType=3 或 4 时，默认为 1 撮合模式。 * 当 dataType 不为 3 或 4 时（基于高频行情进行策略回测），该参数设置为 1 或 2   时都会使用模拟撮合引擎按照价格优先、时间优先逻辑撮合订单。 |
| “benchmark” | 基准标的 | STRING 或 SYMBOL 类型 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾  例如 ”000300.XSHG“ |
| "latency" | 订单延时 | INT 类型，单位为毫秒，用来模拟用户订单从发出到被处理的时延。默认为0，表示无延迟。 |
| “stockDividend” | 分红除权基本信息表 | TABLE 类型，字段说明见下文；或 DICT 类型，如包含可转债必须使用 DICT 类型：   ``` dividend=dict(STRING,ANY) dividend["stocks"]=tb1           //股票和基金 dividend["convertibleBonds"]=tb2 //可转债 ``` |
| ”enableAlgoOrder” | 是否开启算法订单 | BOOL 类型： true：开启  false：不开启 |
| “enableIndicatorOptimize” | 是否开启指标优化 | BOOL 类型，默认为 false true：开启  false：不开启 |
| “isBacktestMode“ | 是否为回测模式 | BOOL 类型，默认为 true true：回测模式  false：模拟交易模式 |
| ”dataRetentionWindow“ | 开始指标优化时数据保留的窗口 | STRING 类型或 INT 类型。 当 enableIndicatorOptimize = true 时，该参数生效。  * isBacktestMode = true 时，默认值为“None” ，可选值为：    + “None”：不保留数据   + “ALL“：全部数据保留   + “20d”：支持按天保留数据，即交易日天数，如 “20d” 代表 20 个交易日   + 20：支持按条数保留数据，如 20 代表每个 symbol 保留最新的 20 条 * isBacktestMode = false 时，无需设置 |
| ”addTimeColumnInIndicator“ | 指标订阅时是否给指标数表增加时间列 | BOOL 类型，默认为 false true：增加  false：不增加 |
| "context" | 行情逻辑上下文类结构 | DICT 类型，行情全局变量构成的字典，如：  ``` context=dict(STRING,ANY) context["buySignalRSI"]=70. userConfig["context"]=context ``` |
| ”callbackForSnapshot “ | 快照行情触发回调模式 | dataType = 1 时仅有。 INT 类型，默认为 0 ，可选值为：  0：表示只触发 onSnapshot  1 ：表示既触发 onSnpshot 又触发 onBar  2 ：表示只触发 onBar  当 frequency >0 时，必须触发 onBar 回调函数，即 callbackForSnapshot =1 或者 2 |
| “enableSubscriptionToTickQuotes” | 是否订阅逐笔行情 | dataType = 0 、5、6 时仅有。 BOOL 类型，默认为 false。当 dataType = 0 或 5，并且使用行情回调函数 onTick 时，必须配置为 true  true：订阅  false：不订阅 |
| “outputQueuePosition” | 是否需要获取订单在行情中的位置  如果输出该信息，则在成交明细和未成交订单接口中会增加以下 5 个指标：   * 优于委托价格的行情未成交委托单总量 * 次于委托价格的行情未成交委托单总量 * 等于委托价格的行情未成交委托单总量 * 等于委托价格且早于用户订单时间的行情未成交委托单总量 * 优于委托价格的行情档位数 | dataType = 0 、5、6 且enableSubscriptionToTickQuotes = true 时仅有。 INT 类型，可选值为：  0：默认值，表示不输出  1：表示订单撮合成交计算上述指标的时候，把最新的一条行情纳入订单薄  2：表示订单撮合成交计算上述指标的时候，把最新的一条行情不纳入订单薄，即统计的是撮合计算前的位置信息 |
| “prevClosePrice” | 前收盘价数据表 | dataType = 0 、5、6 时仅有。 TABLE 类型，为以下三列的表：  [symbol, tradeDate, prevClose]  在深交所的逐笔行情时，创业板股票的前收盘价必须设置，否则订单撮合结果可能不符合预期 |
| “orderBookMatchingRatio” | 与行情订单薄的成交百分比 | dataType = 0 、1、2、 5、6 时仅有 DOUBLE 类型，默认 1.0，取值 0~1.0 之间 |
| “matchingRatio” | 区间撮合比例 | dataType = 0 、1、2、 5、6 时仅有 DOUBLE 类型，默认 1.0，取值 0~1.0 之间。默认和成交百分比 orderBookMatchingRatio 相等 |
| “setLastDayPosition” | 设置底仓 | TABLE 类型，对于每一支选池内的股票进行底仓设置 |
| "enableMinimumPerTransactionFee" | 是否开启股票每笔交易的最低交易费用 | * true：当单笔交易费用低于 5 元时，系统会自动按5元计费。 * false：成交金额\*commission |
| "enableSellCloseRestrict" | 是否限制当日新开仓位的平仓操作 | * false（默认）：不限制 * true，当日买开的持仓不可卖平，只能平掉此前已持有的仓位。 |
| "msgAs​PiecesOnSnapshot" | 回测时，是每条数据依次触发 `onSnapshot` 回调函数，还是同一时间戳的所有数据同时触发。 | BOOL 类型，默认值为 false，此时每条数据依次触发`onSnapshot` |
| "mutualTrigger" | 设置委托确认和撤单触发方式 | * false（默认）：基于模拟撮合引擎接收到的该标的的最新行情时间触发； * true：基于模拟撮合引擎接收到的最新行情时间触发；   仅支持 dataType = 1，2，5，6 |

设置底仓 “setLastDayPosition”，引擎配置中 “setLastDayPosition” 的具体字段说明如下：

| 字段名称 | 类型 | 名称 |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 |
| longPosition | LONG | 买入持仓量 |
| costPrice | DOUBLE | 持仓均价 |
| closePrice | DOUBLE | 昨日收盘价 |

注：

不同的股票行情类型（dataType）的引擎配置参数有所差异：

* 快照行情触发回调模式“callbackForSnapshot” 参数只有在快照行情时设置；
* 是否订阅逐笔行情 “enableSubscriptionToTickQuotes” 、是否需要获取订单在行情中的位置
  “outputQueuePosition” 以及前收盘价数据表 “prevClosePrice” 只有在含逐笔的行情类型中可以设置，即
  dataType = 0 、5、6；
* 与行情订单薄的成交百分比 “orderBookMatchingRatio” 以及区间撮合比例 “matchingRatio”
  只有在含快照的行情类型中可以设置，即 dataType = 0 、1、2、 5、6。

### 分红除权基本信息表说明

股票或基金的分红除权基本信息表 “stockDividend” 字段说明如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 股票代码 |
| endDate | 分红年度 |
| annDate | 预案公告日 |
| recordDate | 股权登记日 |
| exDate | 除权除息日 |
| payDate | 派息日 |
| divListDate | 红股上市日 |
| bonusRatio | 每股送股比例 |
| capitalConversion | 每股转增比例 |
| afterTaxCashDiv | 每股分红（税后） |
| allotPrice | 配股价格 |
| allotRatio | 每股配股比例 |

可转债分红除权基本信息表 “stockDividend” 的字段说明如下：

| **字段** | **说明** |
| --- | --- |
| symbol | 可转债代码 |
| recordDate | 登记日 |
| payDate | 可转债付息日 |
| afterTaxCashDiv | 可转债票面利率 |

### 可转债付息表

“stockDividend” 支持使用字典形式配置，其中可通过 "convertibleBonds"
指定可转债付息表，例如：

```
dividend=dict(STRING,ANY)
dividend["convertibleBonds"]=tb2  // 可转债付息表
```

可转债付息表的字段说明如下：

| **字段** | **含义** |
| --- | --- |
| symbol | 可转债代码 |
| recordDate | 登记日 |
| payDate | 可转债付息日 |
| afterTaxCashDiv | 可转债票面利率 |

### 融资融券

#### 引擎配置说明

关于接口 `createBacktester` 的参数 *config* 和接口
`createBacktestEngine` 的参数 *userConfig*
的配置，除上述所需的基本参数配置，用户可以根据下表添加两融行情所需的参数配置，其中策略类型需要更改为“securityCreditAccount”，行情类型仅支持快照、分钟频以及日频。此外，融资融券策略的行情数据以及行情回调函数说明与股票的保持一致，融资融券策略支持分红除权的设置，具体的结构请参考股票中分红除权表的说明。

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "strategyGroup" | 策略类型 | 必须配置，“securityCreditAccount” |
| "dataType" | 行情类型 | 必须配置，INT 类型，可选值为： 1：快照  3：分钟频率  4：日频  7：快照+分钟频率（该模式仅由接口 `createBacktester` 创建的引擎支持，且不支持 JIT） |
| “lineOfCredit” | 授信额度 | 必须配置，DOUBLE 类型，最大可融额度(融资+融券) |
| “marginTradingInterestRate” | 融资利率 | 必须配置，DOUBLE 类型，如 0.15 |
| “secuLendingInterestRate” | 融券利率 | 必须配置，DOUBLE 类型，可设置与融资利率不同的值，如 0.15 |
| “maintenanceMargin” | 维持担保比例 | 必须配置，DOUBLE 数组类型，如[1.45,1.3,1.2]，三个元素分别为警戒线、追保线、最低线 |
| “longConcentration” | 净多头集中度  集中度计算公式为：  stock\_i 持仓市值/总持仓市值 | 可选配置，DOUBLE 数组类型，控制多头买入金额，如 [1.0, 0.85, 0.6], 三个元素分别控制三条警戒线。注意，最后一个元素是最高线，第一个元素是底线。 |
| “shortConcentration“ | 净空头负债集中度  集中度计算公式为：  stock\_i 持仓市值/总持仓市值 | 可选配置，DOUBLE 数组类型，控制融券卖出金额，如 [1.0, 0.85, 0.6]。集中度越小，说明风险被组合降低。 |
| “outputOrderInfo” | 是否输出风控日志（在订单明细表中） | BOOL 类型 true：输出  false（默认）：不输出 |
| “repayWithoutMarginBuy“ | 控制是否可以用融资买入的券抵消融券卖出的券 | BOOL 类型 true：可以抵消  false（默认）：不允许抵消 |
| “setLastDayPosition” | 设置底仓 | TABLE 类型，对于每一支选池内的股票进行底仓设置 |

* 设置底仓 ”setLastDayPosition”，引擎配置中 “setLastDayPosition” 的具体字段说明如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| marginSecuPosition | LONG | 担保品买入持仓量 |
| marginSecuAvgPrice | DOUBLE | 买成交均价 |
| marginPosition | LONG | 融资买入持仓量 |
| marginBuyValue | DOUBLE | 融资买入金额 |
| secuLendingPosition | LONG | 融券卖出持仓量 |
| secuLendingSellValue | DOUBLE | 融券卖出金额 |
| closePrice | DOUBLE | 收盘价 |
| conversionRatio | DOUBLE | 保证金折算率 |
| tradingMargin | DOUBLE | 融资保证金比例 |
| lendingMargin | DOUBLE | 融券保证金比例 |

#### 基本信息表说明

接口 `createBacktester` 的参数 `securityReference`
和接口 `createBacktestEngine` 的参数
`securityReference` 基本信息表：每日可买入卖出标的基本信息表字段说明如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| tradeDate | DATE | 交易日 |
| symbolSource | SYMBOL | 交易所 |
| securityRating | SYMBOL | 标的分类 |
| marginable | BOOL | 是否是可充抵保证金证券 true：可以担保品买入  false：无法担保品买入 |
| conversionRatio | DOUBLE | 保证金折算率 （影响可用保证金可用余额） |
| tradingMargin | DOUBLE | 融资保证金比例 （影响可用保证金可用余额） |
| lendingMargin | DOUBLE | 融券保证金比例 （影响可用保证金可用余额） |
| eligibleForMarginTrading | BOOL | 是否是可融资状态 true：可以融资买入  false：无法融资买入 |
| eligibleForLending | BOOL | 是否是可融券状态 true：可以融券卖出  false：无法融券卖出 |

## 逐笔或逐笔+快照

### 行情数据结构说明

通过接口 `appendQuotationMsg` 向引擎中插入数据时，*msg* 结构

```
colName=`msgTime`msgType`msgBody`symbol`channelNo`seqNum
colType= [TIMESTAMP, SYMBOL, BLOB,STRING,INT,LONG]
messageTable=streamTable(10000000:0, colName, colType)
```

带有逐笔行情时，msgType 有 "entrust", "trade", "snapshot", "END"
四种类型，当使用逐笔数据合成指定频率的快照数据时，可以不使用 msgType 为 "snapshot"
的行情数据。在这种情况下，系统将根据逐笔交易数据和委托单数据生成对应频率的快照数据。不同 msgType 类型的逐笔数据表通过回放函数
`replayDS` 以及
replay输出得到回测所需的表`messageTable`。下面为各类逐笔数据表的结构说明：

逐笔数据 entrust 和 trade 表结构：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者 "XSHE" （深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0 代表委托数据 entrust；1 代表成交数据 trade |
| orderType | INT | entrust：1 市价；2 限价；3 本方最优；10 撤单（仅上交所，即上交所撤单记录在 entrust 中） trade：0 成交；1 撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据； entrust 中的委托单号填充 |
| sellNo | LONG | trade 对应其原始数据； entrust 中的委托单号填充 |
| direction | INT | 1（买 ）or 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |

snapshot 表结构：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者 "XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| signal | DOUBLE[] | 指标列表 |
| seqNum | LONG | 逐笔数据序号 |
| prevClosePrice | DOUBLE | 前收盘价 |

回测行情回放结束时，增加一条 msgType 为”END“的消息。如下示例：

```
messageTable=select top 1* from messageTable where msgTime=max(msgTime)
update messageTable set msgType="END"
update messageTable set msgTime=concatDateTime(msgTime.date(),16:00:00)
Backtest::appendQuotationMsg(engine,messageTable)
```

### 行情回调函数说明

逐笔行情回调函数 `onTick` ：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 tick 数据字典。其中 value 为这支股票对应的行情信息以及 initialize
中定义的指标计算结果。每个 tick 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0 代表委托数据entrust；1 代表成交表 trade |
| orderType | INT | entrust：1 市价；2 限价；3 本方最优；10 撤单（仅上交所，即上交所撤单记录在 entrust 中） trade：0 成交；1 撤单（仅深交所，即深交所撤单记录在 trade 中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据，entrust 中的委托单号填充。 |
| sellNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充。 |
| direction | INT | 1 （买 ）or 2 （卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |

快照行情回调函数 `onSnapshot` ：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 snapShot 数据字典。其中 value 为这支股票对应的行情信息以及initialize
中定义的指标计算结果。每个 snapShot 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | SYMBOL | 股票市场 ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停板价 |
| downLimitPrice | DOUBLE | 跌停板价 |
| totalBidQty | LONG | 买单成交数量总和 |
| totalOfferQty | LONG | 卖单成交数量总和 |
| bidPrice | DOUBLE[] | 买单价格列表 |
| bidQty | LONG[] | 买单数量列表 |
| offerPrice | DOUBLE[] | 卖单价格列表 |
| offerQty | LONG[] | 卖单数量列表 |
| signal | DOUBLE[] | 指标列表 |

## 快照

### 行情数据结构说明

通过 Backtest::appendQuotationMsg
写入的行情表结构如下：

```
colName=["symbol","symbolSource","timestamp","lastPrice","upLimitPrice","downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty",
"offerPrice","offerQty","prevClosePrice"]
colType= ["SYMBOL","SYMBOL","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","LONG",
"LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]", "DOUBLE"]
messageTable=table(10000:0, colName, colType)
```

注：

* 标的代码 symbol 必须带有交易所标识（".XSHG",".XSHE"）结尾，如 600000.XSHG，不然报错。
* 上述为快照行情（frequency=0，callbackForSnapshot=0），即非快照合成 bar 行情的输入表结构。
* 字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING
  类型的列，或名为 signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

快照行情数据表必需字段如下所示：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者"XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| signal | DOUBLE[] | 指标列表 |
| prevClosePrice | DOUBLE | 前收盘价 |

快照行情（frequency>0，callbackForSnapshot=1或者2）表结构：

```
colName=["symbol","symbolSource","timestamp","lastPrice","upLimitPrice",
"downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty",
"offerPrice","offerQty","prevClosePrice","open", "close","low","high","volume"]
colType= ["STRING","STRING","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","LONG",
"LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE",DOUBLE, DOUBLE,DOUBLE,DOUBLE,LONG]
messageTable=table(10000000:0, colName, colType)
```

注：

* 快照合成 bar 行情时（frequency>0 且 callbackForSnapshot=1 或者 2）,
  还需要增加五个字段："open", "close", "low", "high", "volume"。
* 字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING
  类型的列，或名为 signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

快照行情数据表（使用快照合成 bar 行情）必需字段如下所示：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者 "XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| signal | DOUBLE[] | 指标列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| open | DOUBLE | 合成 bar 行情的开盘价 |
| close | DOUBLE | 合成 bar 行情的收盘价 |
| low | DOUBLE | 合成 bar 行情的最低价 |
| high | DOUBLE | 合成 bar 行情的最高价 |
| volume | LONG | 合成 bar 行情的成交量 |

回测行情回放结束时，发送一条 symbol 为 “END” 的消息:

```
messageTable=select top 1 * from messageTable
update messageTable set symbol="END"
Backtest::appendQuotationMsg(engine,messageTable)
```

### 行情回调函数说明

快照行情回调函数 `onSnapshot` ：输入参数 msg

msg 为字典时，是以 symbol为 key 的 snapShot 数据字典。其中 value 为这支股票对应的行情信息。每个 snapShot
对象包含字段如下：

| **名称** | **类型** | **含义** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停板价 |
| downLimitPrice | DOUBLE | 跌停板价 |
| totalBidQty | LONG | 买单成交数量总和 |
| totalOfferQty | LONG | 卖单成交数量总和 |
| bidPrice | DOUBLE[] | 买单价格列表 |
| bidQty | LONG[] | 买单数量列表 |
| offerPrice | DOUBLE[] | 卖单价格列表 |
| offerQty | LONG[] | 卖单数量列表 |
| signal | DOUBLE[] | 其他 |
| open | DOUBLE | 合成 bar 行情的开盘价 （dataType = 1 或者 2，callbackForSnapshot = 1或者2时才有） |
| close | DOUBLE | 合成 bar 行情的收盘价 （dataType = 1或者 2，callbackForSnapshot = 1或者 2 时才有） |
| low | DOUBLE | 合成 bar 行情的最低价 （dataType = 1 或者 2，callbackForSnapshot = 1或者 2 时才有） |
| high | DOUBLE | 合成 bar 行情的最高价 （dataType = 1 或者 2，callbackForSnapshot = 1或者 2 时才有） |
| volume | LONG | 合成 bar 行情的成交量 （dataType = 1 或者 2，callbackForSnapshot = 1 或者 2 时才有） |

注：

* 快照合成 bar 行情时（frequency > 0 且 callbackForSnapshot = 1 或者 2）, 输入参数
  msg 还需要增加五个字段："open", "close","low","high","volume"。
* 当 callbackForSnapshot = 1 或 2 时，还需回调 onBar 函数，输入参数 msg 的数据结构如下。

k线行情回调函数 `onBar`：输入参数 msg

msg 为字典时，是以 symbol 为 key 的分钟频率的 K 线数据字典。每个 K 线包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| tradeTime | TIMESTAMP | 交易日 |
| open | DOUBLE | 开盘价 |
| low | DOUBLE | 最低价 |
| high | DOUBLE | 最高价 |
| close | DOUBLE | 收盘价 |
| volume | LONG | 成交量 |
| amount | DOUBLE | 成交额 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| prevClosePrice | DOUBLE | 前收盘价 |
| signal | DOUBLE[] | 其他 |

## 快照+逐笔成交明细

### 行情数据结构说明

快照+逐笔成交明细行情（frequency=0，callbackForSnapshot=0）时的表结构：

```
colName=["symbol","symbolSource","timestamp","lastPrice","upLimitPrice",
                "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty",
                "offerPrice","offerQty","tradePrice","tradeQty","prevClosePrice"]
colType= ["STRING","STRING","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","LONG",
                "LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE"]
messageTable=table(10000000:0, colName, colType)
```

注：

* 标的代码symbol必须带有交易所标识（".XSHG",".XSHE"）结尾,如 600000.XSHG，不然报错。
* 上述为快照+逐笔成交明细行情（frequency=0，callbackForSnapshot=0），即非快照合成bar行情的输入表结构。

具体字段说明如下：（与快照行情比增加tradePrice 和 tradeQty 两个字段）

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者"XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| tradePrice | DOUBLE[] | 成交价格 |
| tradeQty | LONG[] | 成交数量 |
| signal | DOUBLE[] | 指标列表 |
| prevClosePrice | DOUBLE | 前收盘价 |

快照+逐笔成交明细行情（frequency>0，callbackForSnapshot=1或者2）时的表结构：

```
colName=["symbol","symbolSource","timestamp","lastPrice","upLimitPrice",
                "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty",
                "offerPrice","offerQty","tradePrice","tradeQty","prevClosePrice","open", "close","low","high","volume"]
colType= ["STRING","STRING","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","LONG",
                "LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE","DOUBLE", "DOUBLE","DOUBLE","DOUBLE","LONG"]
messageTable=table(10000000:0, colName, colType)
```

注：

快照合成bar行情时（frequency>0且callbackForSnapshot=1或者2）, 还需要增加五个字段："open",
"close","low","high","volume"。

具体字段说明如下：（与快照行情比增加tradePrice 和 tradeQty 两个字段）

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | STRING | "XSHG"（上交所）或者 "XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| tradePrice | DOUBLE[] | 成交价格 |
| tradeQty | LONG[] | 成交数量 |
| signal | DOUBLE[] | 指标列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| open | DOUBLE | 合成bar行情的开盘价 |
| close | DOUBLE | 合成bar行情的收盘价 |
| low | DOUBLE | 合成bar行情的最低价 |
| high | DOUBLE | 合成bar行情的最高价 |
| volume | LONG | 合成bar行情的成交量 |

回测行情回放结束时，发送一条symbol为“END”的消息:

```
messageTable=select top 1 * from messageTable
update messageTable set symbol="END"
Backtest::appendQuotationMsg(engine, messageTable)
```

### 行情回调函数说明

快照行情回调函数 `onSnapshot`：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 snapShot数据字典。其中 value 为这支股票对应的行情信息。每个 snapShot
对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停板价 |
| downLimitPrice | DOUBLE | 跌停板价 |
| totalBidQty | LONG | 买单成交数量总和 |
| totalOfferQty | LONG | 卖单成交数量总和 |
| bidPrice | DOUBLE[] | 买单价格列表 |
| bidQty | LONG[] | 买单数量列表 |
| offerPrice | DOUBLE[] | 卖单价格列表 |
| offerQty | LONG[] | 卖单数量列表 |
| signal | DOUBLE[] | 其他 |
| open | DOUBLE | 合成 bar 行情的开盘价 （dataType = 1 或者 2，callbackForSnapshot = 1 或者 2 时才有） |
| close | DOUBLE | 合成 bar 行情的收盘价 （dataType = 1 或者 2，callbackForSnapshot = 1 或者 2 时 才有） |
| low | DOUBLE | 合成 bar 行情的最低价 （dataType = 1 或者 2，callbackForSnapshot = 1 或者 2 时才有） |
| high | DOUBLE | 合成 bar 行情的最高价 （dataType = 1 或者 2，callbackForSnapshot = 1 或者 2 时才有） |
| volume | LONG | 合成 bar 行情的成交量 （dataType = 1 或者 2，callbackForSnapshot = 1 或者 2 时才有） |

注：

* 快照合成 bar 行情时（frequency > 0 且 callbackForSnapshot = 1 或者 2）, 输入参数
  msg 还需要增加五个字段："open", "close","low","high","volume"。
* 当 callbackForSnapshot = 1 或 2 时，还需回调 onBar 函数，输入参数 msg 的数据结构如下。

k线行情回调函数 `onBar`：输入参数 msg

msg 为字典时，是以 symbol 为 key 的分钟频率的 K 线数据字典。每个 K 线包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| tradeTime | TIMESTAMP | 交易日 |
| open | DOUBLE | 开盘价 |
| low | DOUBLE | 最低价 |
| high | DOUBLE | 最高价 |
| close | DOUBLE | 收盘价 |
| volume | LONG | 成交量 |
| amount | DOUBLE | 成交额 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| prevClosePrice | DOUBLE | 前收盘价 |
| signal | DOUBLE[] | 其他 |

## 分钟频或日频

### 行情数据结构说明

通过 Backtest::appendQuotationMsg
写入的行情表结构如下：

```
colName=`symbol`tradeTime`open`low`high`close`volume`amount`upLimitPrice`downLimitPrice`prevClosePrice
colType=[SYMBOL,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE]
messageTable=table(10000000:0, colName, colType)
```

注：

字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING 类型的列，或名为
signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

分钟频行情数据表必需字段如下所示：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 |
| tradeTime | TIMESTAMP | 时间戳 |
| open | DOUBLE | 开盘价 |
| low | DOUBLE | 最低价 |
| high | DOUBLE | 最高价 |
| close | DOUBLE | 收盘价 |
| volume | LONG | 成交量 |
| amount | DOUBLE | 成交金额 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| prevClosePrice | DOUBLE | 前收盘价 |
| signal | DOUBLE[] | 其他字段列表 |

回测行情回放结束时，发送一条 symbol 为“END”的消息:

```
messageTable=select top 1 * from messageTable
update messageTable set symbol="END"
Backtest::appendQuotationMsg(engine,messageTable)
```

### 行情回调函数说明

K 线行情回调函数 `onBar`：输入参数 msg

msg 为字典时，是以 symbol 为 key 的分钟频率的 K 线数据字典。每个 K 线包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| tradeTime | TIMESTAMP | 交易日 |
| open | DOUBLE | 开盘价 |
| low | DOUBLE | 最低价 |
| high | DOUBLE | 最高价 |
| close | DOUBLE | 收盘价 |
| volume | LONG | 成交量 |
| amount | DOUBLE | 成交额 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| prevClosePrice | DOUBLE | 前收盘价 |
| signal | DOUBLE[] | 其他 |

## 逐笔（宽表）

### 行情数据结构说明

执行回测时输入表 messageTable 结构:
`Backtest::appendQuotationMsg(engine,messageTable)`

```
colName=[`symbol,`symbolSource,`timestamp,`sourceType,`orderType,`price,`qty,`buyNo,
    `sellNo,`direction,`channelNo,`seqNum,`reserve1]
colType=["SYMBOL","INT","TIMESTAMP","INT","INT","DOUBLE","LONG","LONG",
    "LONG","INT","INT","LONG","DOUBLE"]
messageTable=table(1000:0,colName,colType)
```

逐笔（宽表）行情数据表结构：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以 ".XSHG" 结尾  深交所以 ".XSHE" 结尾 |
| symbolSource | INT | 0（上交所）或者1（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0 代表委托数据`entrust`；1 代表成交表 trade |
| orderType | INT | `entrust`：1 市价；2 限价；3 本方最优；10 撤单（仅上交所，即上交所撤单记录在`entrust`中）  trade：0 成交；1 撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| sellNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| direction | INT | 1（买 ）or 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |
| reserve1 | DOUBLE | 预留字段1（宽表） |

与逐笔数据相比，逐笔（宽表）增加了”reserve1“ 这个预留字段。

回测行情回放结束时，增加一条 symbol 为”END“的消息。如下示例：

```
messageTable=select top 1 * from messageTable
update messageTable set symbol="END"
Backtest::appendQuotationMsg(engine,messageTable)
```

### 行情回调函数说明

逐笔行情回调函数 `onTick` ：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 tick 数据字典。其中 value 为这支股票对应的行情信息以及initialize
中定义的指标计算结果。每个 tick 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0代表委托数据`entrust`；1代表成交表 trade |
| orderType | INT | `entrust`：1市价；2限价；3本方最优；10撤单（仅上交所，即上交所撤单记录在`entrust`中） trade：0成交；1撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| sellNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| direction | INT | 1（买 ）or 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |
| reserve1 | DOUBLE | 预留字段1（宽表） |

快照行情回调函数 `onSnapshot` ：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 snapShot 数据字典。其中 value 为这支股票对应的行情信息以及initialize
中定义的指标计算结果。每个 snapShot 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0代表委托数据`entrust`；1代表成交表 trade |
| orderType | INT | `entrust`：1市价；2限价；3本方最优；10撤单（仅上交所，即上交所撤单记录在`entrust`中） trade：0成交；1撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| sellNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| direction | INT | 1（买 ）or 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |
| reserve1 | DOUBLE | 预留字段1（宽表） |

## 逐笔+快照（宽表）

### 行情数据结构说明

执行回测时输入表`messageTable`的数据结构：`Backtest::appendQuotationMsg(engine,messageTable)`

```
colName=[`symbol,`symbolSource,`timestamp,`sourceType,`orderType,`price,`qty,`buyNo,
`sellNo,`direction,`channelNo,`seqNum,"lastPrice","upLimitPrice",
"downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty",
"offerPrice","offerQty","prevClosePrice"]
colType=["SYMBOL","STRING","TIMESTAMP","INT","INT","DOUBLE","LONG","LONG",
"LONG","INT","INT","LONG","DOUBLE","DOUBLE","DOUBLE","LONG",
"LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE"]
messageTable=table(1000:0,colName,colType)
```

逐笔+快照（宽表）行情数据表结构：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | INT | 0（上交所）或者1（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0 代表委托数据 entrust；1 代表成交数据 trade；2 代表快照数据snapshot |
| orderType | INT | entrust：1 市价；2 限价；3 本方最优；10 撤单（仅上交所，即上交所撤单记录在 entrust 中） trade：0 成交；1 撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据； entrust 中的委托单号填充 |
| sellNo | LONG | trade 对应其原始数据； entrust 中的委托单号填充 |
| direction | INT | 1（买 ）或者 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| reserve1 | DOUBLE | 预留字段1（宽表） |
| reserve2 | DOUBLE | 预留字段2（宽表） |

回测行情回放结束时，发送一条 symbol 为 “END” 的消息:

```
messageTable=select top 1* from messageTable
update messageTable set symbol="END"
Backtest::appendQuotationMsg(engine,messageTable)
```

### 行情回调函数说明

逐笔行情回调函数 `onTick` ：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 tick 数据字典。其中 value 为这支股票对应的行情信息以及initialize
中定义的指标计算结果。每个 tick 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0代表委托数据`entrust`；1代表成交表 trade,2代码snapshot |
| orderType | INT | `entrust`：1 市价；2 限价；3 本方最优；10 撤单（仅上交所，即上交所撤单记录在`entrust`中） trade：0 成交；1 撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| sellNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| direction | INT | 1（买 ）or 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| reserve1 | DOUBLE | 预留字段 1（宽表） |
| reserve2 | DOUBLE | 预留字段 2（宽表） |

快照行情回调函数 `onSnapshot` ：输入参数 msg

msg 为字典时，是以 symbol 为 key 的 snapShot 数据字典。其中 value 为这支股票对应的行情信息以及initialize
中定义的指标计算结果。每个 snapShot 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
| symbolSource | STRING | ".XSHG"（上交所）或者".XSHE"（深交所） |
| timestamp | TIMESTAMP | 时间戳 |
| sourceType | INT | 0代表委托数据`entrust`；1代表成交表 trade,2代码snapshot |
| orderType | INT | `entrust`：1 市价；2 限价；3 本方最优；10 撤单（仅上交所，即上交所撤单记录在`entrust`中） trade：0 成交；1 撤单（仅深交所，即深交所撤单记录在 trade中） |
| price | DOUBLE | 订单价格 |
| qty | LONG | 订单数量 |
| buyNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| sellNo | LONG | trade 对应其原始数据；entrust 中的委托单号填充， |
| direction | INT | 1（买 ）or 2（卖） |
| channelNo | INT | 通道号 |
| seqNum | LONG | 逐笔数据序号 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间买量 |
| totalOfferQty | LONG | 区间卖量 |
| bidPrice | DOUBLE[] | 委买价格列表 |
| bidQty | LONG[] | 委买量列表 |
| offerPrice | DOUBLE[] | 委卖价格列表 |
| offerQty | LONG[] | 委卖量列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| reserve1 | DOUBLE | 预留字段 1（宽表） |
| reserve2 | DOUBLE | 预留字段 2（宽表） |

## 快照+分钟频率

### 行情数据结构说明

通过接口 `appendQuotationMsg` 向引擎中插入数据时，*msg* 为一个字典，key 支持
'ohlc'，'snapshot' 或 'indicator' 三种：

* 'ohlc'
  为分钟频行情表，结构如下：

  ```
  colName=`symbol`tradeTime`open`low`high`close`volume`amount`upLimitPrice`downLimitPrice`prevClosePrice
  colType=[SYMBOL,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE]
  messageTable=table(10000000:0, colName, colType)
  ```

  注：

  字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING 类型的列，或名为
  signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。
* 'snapshot'
  为快照行情表，结构如下：

  ```
  colName=["symbol","symbolSource","timestamp","lastPrice","upLimitPrice","downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty",
  "offerPrice","offerQty","prevClosePrice"]
  colType= ["SYMBOL","SYMBOL","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","LONG",
  "LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]", "DOUBLE"]
  messageTable=table(10000:0, colName, colType)
  ```

  注：

  + 标的代码 symbol 必须带有交易所标识（".XSHG",".XSHE"）结尾，如 600000.XSHG，不然报错。
  + 上述为快照行情（frequency=0，callbackForSnapshot=0），即非快照合成 bar 行情的输入表结构。
  + 字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING
    类型的列，或名为 signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

  快照行情数据表必需字段如下所示：

  | **字段** | **类型** | **备注** |
  | --- | --- | --- |
  | symbol | SYMBOL | 股票代码 上交所以".XSHG"结尾  深交所以".XSHE"结尾 |
  | symbolSource | STRING | "XSHG"（上交所）或者"XSHE"（深交所） |
  | timestamp | TIMESTAMP | 时间戳 |
  | lastPrice | DOUBLE | 最新成交价 |
  | upLimitPrice | DOUBLE | 涨停价 |
  | downLimitPrice | DOUBLE | 跌停价 |
  | totalBidQty | LONG | 区间买量 |
  | totalOfferQty | LONG | 区间卖量 |
  | bidPrice | DOUBLE[] | 委买价格列表 |
  | bidQty | LONG[] | 委买量列表 |
  | offerPrice | DOUBLE[] | 委卖价格列表 |
  | offerQty | LONG[] | 委卖量列表 |
  | signal | DOUBLE[] | 指标列表 |
  | prevClosePrice | DOUBLE | 前收盘价 |

  分钟频行情数据表必需字段如下所示：

  | **字段** | **类型** | **备注** |
  | --- | --- | --- |
  | symbol | SYMBOL | 股票代码 |
  | tradeTime | TIMESTAMP | 时间戳 |
  | open | DOUBLE | 开盘价 |
  | low | DOUBLE | 最低价 |
  | high | DOUBLE | 最高价 |
  | close | DOUBLE | 收盘价 |
  | volume | LONG | 成交量 |
  | amount | DOUBLE | 成交金额 |
  | upLimitPrice | DOUBLE | 涨停价 |
  | downLimitPrice | DOUBLE | 跌停价 |
  | prevClosePrice | DOUBLE | 前收盘价 |
  | signal | DOUBLE[] | 其他字段列表 |
* 'indicator' 为对应 onBar 回调的历史指标数据表。设置该表时，不能同时使用
  `subscribeIndicator` 订阅 ohlc/kline 类型的指标。该表的字段必须包含
  symbol 和 timestamp，其后可以是 INT、DOUBLE 或 STRING 类型的扩展字段。
