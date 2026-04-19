<!-- Auto-mirrored from upstream `documentation-main/plugins/backtest/digital_currency.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 数字货币回测配置

回测平台支持的数字货币行情数据类型包括：快照，分钟频率，日频等。

数字货币引擎支持单个引擎中同时管理现货和期货的多个账户，其使用方式与单账户引擎有所不同。多账户设计遵循以下原则：

1. 数字货币行情中可以存在不同的合约类型，onBar 回调会一次性提供对应时间段内所有合约类型的数据，便于用户根据不同合约的行情设计策略。
2. 数字货币接口支持可选的 *accountType*
   参数，用于指定需要操作的账户。在省略该参数时，原则上策略中使用的接口(下单撤单、获取未成交订单、获取持仓等)默认为现货账户，回测结束后调用的接口(成交明细、每日持仓等)默认返回所有账户的结果。

## 引擎配置说明

接口 `createBacktester` 的参数 *config* 和接口
`createBacktestEngine` 的参数 *userConfig* 的配置可参考下表：

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "startDate" | 开始日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "endDate" | 结束日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "strategyGroup" | 策略类型 | 必须配置，“cryptocurrency” |
| "cash" | 初始资金 字典类型  {  “spot”：100000.  “futures“:100000.  “option“:100000.  } | 必须配置，DOUBLE 类型，不同的品种在不同的账户 spot：现货账户  futures：期货和永续账户  option：期权账户 |
| "dataType" | 行情类型 | 必须配置，INT 类型，可选值为： 1：快照  3：分钟频  4：日频 |
| "msgAsTable" | 行情的数据格式 | BOOL 类型，默认为 false false：字典  true：表（只能通过接口createBacktestEngine 创建引擎） |
| “matchingMode“ | 订单撮合模式 | INT 类型，根据行情类型模式不同，可选值为： 1：   * 日频：以收盘价撮合订单 * 分钟频：行情时间大于订单时间时撮合订单   2：   * 日频：以开盘价撮合订单 * 分钟频：行情时间等于订单时间时以当前行情的收盘价撮合订单，后续未完成订单撮合订单同 1   3：以委托价格成交  当 dataType=1 时，该参数设置为 1 或 2 时无效，默认按模拟撮合引擎撮合订单 |
| “benchmark” | 基准标的 | STRING 或 SYMBOL 类型，例如 ”BTCUSDT\_0“ 。在接口`getReturnSummary` 中使用 |
| "latency" | 订单延时 | DOUBLE 类型，单位为毫秒，用来模拟用户订单从发出到被处理的时延。默认为0，表示无延迟。 |
| fundingRate | 永续合约资金费率 | TABLE 类型，字段说明见下文 |
| “enableIndicatorOptimize” | 是否开启指标优化 | BOOL 类型，默认为 false true：开启  false：不开启 |
| ”addTimeColumnInIndicator“ | 指标订阅时是否给指标数表增加时间列 | BOOL 类型，默认为 false true：增加  false：不增加 |
| “isBacktestMode“ | 是否为回测模式 | BOOL 类型，默认为 true true：回测模式  false：模拟交易模式 |
| ”dataRetentionWindow“ | 开始指标优化时数据保留的窗口 | STRING 类型或 INT 类型。 当 enableIndicatorOptimize = true 时，该参数生效。  * isBacktestMode = true 时，默认 “None” ，可设置为：    + “ALL“：全部数据保留   + “20d”：支持按天保留数据，即交易日天数，如 “20d” 代表 20 个交易日   + “None”：不保留数据   + 20：支持按条数保留数据，如 20 代表每个 symbol 保留最新的 20 条 * isBacktestMode = false 时，无需设置 |
| "context" | 策略逻辑上下文类结构 | DICT 类型，策略全局变量构成的字典，如：  ``` context=dict(STRING,ANY) context["buySignalRSI"]=70. context["buySignalRSI"]=30.  userConfig["context"]=context ``` |
| “orderBookMatchingRatio” | 与行情订单薄的成交百分比 | dataType = 1 或 2 仅有。 DOUBLE 类型，默认 1.0，取值0~1.0 之间 |
| “matchingRatio” | 区间撮合比例 | dataType = 1 或 2 仅有。 DOUBLE 类型，默认 1.0，取值0~1.0 之间。默认和成交百分比 orderBookMatchingRatio 相等 |
| "msgAs​PiecesOnSnapshot" | 回测时，是每条数据依次触发 `onSnapshot` 回调函数，还是同一时间戳的所有数据同时触发。 | BOOL 类型，默认值为 false，此时每条数据依次触发`onSnapshot` |

注意：不同的数字货币行情类型（dataType）的引擎配置参数有所差异：

* 与行情订单薄的成交百分比 “orderBookMatchingRatio” 以及区间撮合比例 “matchingRatio”
  只有在含快照的行情类型中可以设置，即 dataType = 1 或 2。

永续合约资金费率表 “fundingRate”：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | STRING 或 SYMBOL | 合约 |
| settlementTime | TIMESTAMP | 结算时间 |
| lastFundingRate | DECIMAL128(8) | 结算费率 |
| markPrice | DECIMAL128(8) | 结算时的标记价格，用于计算资金费率应付金额：  * 字段存在且大于 0 时，按该价格结算费率； * 字段为空或小于等于 0 时，按最新行情价格结算费率。 |

### 基本信息表说明

接口 `createBacktester` 的参数 `securityReference` 和接口
`createBacktestEngine` 的参数 `securityReference`
的基本信息表字段可参考下表：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL 或 STRING | 品种代码 |
| contractType | INT | 品种类型 0：现货  1：交割合约  2：永续合约  3：期权 |
| optType | INT | 期权类型 1：看涨（call）  2：看跌（put） |
| strikePrice | DECIMAL128(8) | 行权价 |
| contractSize | DECIMAL128(8) | 合约乘数 |
| marginRatio | DECIMAL128(8) | 保证金比例 |
| tradeUnit | DECIMAL128(8) | 合约单位 |
| priceUnit | DECIMAL128(8) | 报价单位 |
| priceTick | DECIMAL128(8) | 价格最小变动单位 |
| takerRate | DECIMAL128(8) | 吃单手续费 |
| makerRate | DECIMAL128(8) | 挂单手续费 |
| deliveryCommissionMode | INT | 1：makerRate（或者takerRate）/ 手 2：成交额 \*makerRate（或者takerRate） |
| fundingSettlementMode | INT | 1：lastFundingRate/手（永续合约） 2：价值 \*lastFundingRate（永续合约） |
| lastTradeTime | TIMESTAMP | 最后交易时间 |

注：

* 费用计算，每个品种相应的保证金、费用等不一致
* 若品种类型为永续合约时，持仓费用计算还需参考配置的永续合约资金费率表

## 快照

### 行情数据结构说明

通过接口 `appendQuotationMsg` 向引擎中插入数据时，*msg* 结构：

```
colName=["symbol","symbolSource","timestamp","tradingDay","lastPrice","upLimitPrice",
        "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty","offerPrice",
        "offerQty","highPrice","lowPrice","prevClosePrice","settlementPrice",
        "prevSettlementPrice","contractType"]
colType= ["STRING","STRING","TIMESTAMP","DATE","DECIMAL128(8)","DECIMAL128(8)","DECIMAL128(8)","DECIMAL128(8)","DECIMAL128(8)",
        "DECIMAL128(8)[]","DECIMAL128(8)[]","DECIMAL128(8)[]","DECIMAL128(8)[]","DECIMAL128(8)","DECIMAL128(8)",
        "DECIMAL128(8)","DECIMAL128(8)","DECIMAL128(8)","INT"]
messageTable=table(10000000:0, colName, colType)
```

快照行情数据表结构：

|  |  |  |
| --- | --- | --- |
| **字段** | **类型** | **备注** |
| symbol | STRING | 品种代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DECIMAL128(8) | 最新成交价 |
| upLimitPrice | DECIMAL128(8) | 涨停价 |
| downLimitPrice | DECIMAL128(8) | 跌停价 |
| totalBidQty | DECIMAL128(8) | 区间成交买数量 |
| totalOfferQty | DECIMAL128(8) | 区间成交卖数量 |
| bidPrice | DECIMAL128(8)[] | 委托买价 |
| bidQty | DECIMAL128(8)[] | 委托买量 |
| offerPrice | DECIMAL128(8)[] | 委托卖价 |
| offerQty | DECIMAL128(8)[] | 委托卖价 |
| highPrice | DECIMAL128(8) | 最高价 |
| lowPrice | DECIMAL128(8) | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DECIMAL128(8) | 前收盘价 |
| settlementPrice | DECIMAL128(8) | 结算价 |
| prevSettlementPrice | DECIMAL128(8) | 前结算价 |
| contractType | INT | 品种类型 0：现货  1：交割合约  2：永续合约  3：期权 |

注：不同品种类型对应的基本信息表说明见本节最后一栏。

回测行情回放结束时，发送一条 symbol 为 “END” 的消息：

```
messageTable=select top 1* from messageTable where tradeTime=max(tradeTime)
update messageTable set symbol="END"
update messageTable set tradeTime=concatDateTime(tradeTime.date(),16:00:00)
Backtest::appendQuotationMsg(engine,messageTable)
```

### 策略回调函数说明

快照行情回调函数 `onSnapshot`：输入参数 msg

msg 为字典时，是 symbol 为 key 值的 snapShot 数据字典，每个 snapShot 对象包含字段如下：

|  |  |  |
| --- | --- | --- |
| **字段** | **类型** | **备注** |
| symbol | STRING | 品种代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DECIMAL128(8) | 最新成交价 |
| upLimitPrice | DECIMAL128(8) | 涨停价 |
| downLimitPrice | DECIMAL128(8) | 跌停价 |
| totalBidQty | DECIMAL128(8) | 区间成交买数量 |
| totalOfferQty | DECIMAL128(8) | 区间成交卖数量 |
| bidPrice | DECIMAL128(8)[] | 委托买价 |
| bidQty | DECIMAL128(8)[] | 委托买量 |
| offerPrice | DECIMAL128(8)[] | 委托卖价 |
| offerQty | DECIMAL128(8)[] | 委托卖价 |
| highPrice | DECIMAL128(8) | 最高价 |
| lowPrice | DECIMAL128(8) | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DECIMAL128(8) | 前收盘价 |
| settlementPrice | DECIMAL128(8) | 结算价 |
| prevSettlementPrice | DECIMAL128(8) | 前结算价 |
| contractType | INT | 品种类型 0：现货  1：交割合约  2：永续合约  3：期权 |

## 分钟频率或日频

### 行情数据结构说明

通过接口 `appendQuotationMsg` 向引擎中插入数据时，*msg* 结构：

```
colName=[`symbol,`symbolSource,`tradeTime,`tradingDay,`open,`low,`high,`close,`volume,`amount,`upLimitPrice,
        `downLimitPrice,`prevClosePrice,`settlementPrice,`prevSettlementPrice,`contractType]
colType=[SYMBOL,SYMBOL,TIMESTAMP,DATE,DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),
DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),DECIMAL128(8),INT]
messageTable=table(10000000:0, colName, colType)
```

分钟频行情数据表结构：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 品种代码 |
| symbolSource | SYMBOL | 交易所 |
| tradeTime | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| open | DECIMAL128(8) | 开盘价 |
| low | DECIMAL128(8) | 最低价 |
| high | DECIMAL128(8) | 最高价 |
| close | DECIMAL128(8) | 收盘价 |
| volume | DECIMAL128(8) | 成交量 |
| amount | DECIMAL128(8) | 成交金额 |
| upLimitPrice | DECIMAL128(8) | 涨停价 |
| downLimitPrice | DECIMAL128(8) | 跌停价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DECIMAL128(8) | 前收盘价 |
| settlementPrice | DECIMAL128(8) | 结算价 |
| prevSettlementPrice | DECIMAL128(8) | 前结算价 |
| contractType | INT | 品种类型 0：现货  1：交割合约  2：永续合约  3：期权 |

注：不同品种类型对应的基本信息表说明见本节最后一栏。

回测行情回放结束时，发送一条 symbol 为 “END” 的消息:

```
messageTable=select top 1* from messageTable where tradeTime=max(tradeTime)
update messageTable set symbol="END"
update messageTable set tradeTime=concatDateTime(tradeTime.date(),16:00:00)
Backtest::appendQuotationMsg(engine,messageTable)
```

### 策略回调函数说明

k 线行情回调函数 `onBar`：输入参数 msg

msg 是字典时，是 以 symbol 为 key 值的分钟频率的 K 线数据字典，每个 K 线包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 品种代码 |
| symbolSource | SYMBOL | 交易所 |
| tradeTime | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| open | DECIMAL128(8) | 开盘价 |
| low | DECIMAL128(8) | 最低价 |
| high | DECIMAL128(8) | 最高价 |
| close | DECIMAL128(8) | 收盘价 |
| volume | DECIMAL128(8) | 成交量 |
| amount | DECIMAL128(8) | 成交金额 |
| upLimitPrice | DECIMAL128(8) | 涨停价 |
| downLimitPrice | DECIMAL128(8) | 跌停价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DECIMAL128(8) | 前收盘价 |
| settlementPrice | DECIMAL128(8) | 结算价 |
| prevSettlementPrice | DECIMAL128(8) | 前结算价 |
| contractType | INT | 品种类型 0：现货  1：交割合约  2：永续合约  3：期权 |
