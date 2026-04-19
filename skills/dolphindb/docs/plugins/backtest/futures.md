<!-- Auto-mirrored from upstream `documentation-main/plugins/backtest/futures.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 期货回测配置

回测平台支持的期货资产行情数据类型包括：快照，分钟频率，日频。

## 引擎配置说明：

接口 `createBacktester` 的参数 *config* 和接口
`createBacktestEngine` 的参数 *userConfig* 的配置可参考下表：userConfig
参数的配置：

```
userConfig = dict(STRING, ANY)
```

| **key** | **说明** | **备注** |
| --- | --- | --- |
| "startDate" | 开始日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "endDate" | 结束日期 | 必须配置，DATE 类型 例如 “2020.01.01” |
| "strategyGroup" | 策略类型 | 必须配置，“futures” |
| "cash" | 初始资金 | 必须配置，DOUBLE 类型 |
| "dataType" | 行情类型 | 必须配置，INT 类型，可选值为： 1：快照  3：分钟频  4：日频  7：快照+分钟频率（该模式仅由接口 `createBacktester` 创建的引擎支持，且不支持 JIT） |
| “frequency” | 快照数据以指定频率合成 bar | dataType = 1 仅有。 INT 类型， 默认为 0   * 当 frequency = 0 时，该参数无效。 * 当 dataType=1 且 frequency > 0 时，引擎内部合成 frequency 频率的   bar 行情触发 `onBar` 回调函数 |
| "msgAsTable" | 行情的数据格式 | BOOL 类型，默认为 false false：字典  true：表（只能通过接口createBacktestEngine 创建引擎） |
| “matchingMode“ | 订单撮合模式 | INT 类型，根据行情类型模式不同，可选值为： 1：   * 日频：以收盘价撮合订单 * 分钟频：行情时间大于订单时间时撮合订单   2：   * 日频：以开盘价撮合订单 * 分钟频：行情时间等于订单时间时以当前行情的收盘价撮合订单，后续未完成订单撮合订单同 1   3：以委托价格成交  当 dataType=1 时，该参数设置为 1 或 2 时无效，默认按模拟撮合引擎撮合订单 |
| “benchmark” | 基准标的 | STRING 或 SYMBOL 类型 例如 ”A2305“ ，在接口`getReturnSummary` 中使用 |
| "latency" | 订单延时 | INT 类型，单位为毫秒，用来模拟用户订单从发出到被处理的时延。默认为0，表示无延迟。 |
| “maintenanceMargin” | 维保比例 | DOUBLE 类型，默认 1.0，取值0~1.0 之间 |
| ”enableAlgoOrder” | 是否开启算法订单 | BOOL 类型： true：开启  false：不开启 |
| ”futuresType“ | 期货品种类型，如股指期货，商品期货等 | STRING 或 SYMBOL 类型 目前只支持期货 |
| “enableIndicatorOptimize” | 是否开启指标优化 | BOOL 类型，默认为 false true：开启  false：不开启 |
| “isBacktestMode“ | 是否为回测模式 | BOOL 类型，默认为 true true：回测模式  false：模拟交易模式 |
| ”dataRetentionWindow“ | 开始指标优化时数据保留的窗口 | STRING 类型或 INT 类型。 当 enableIndicatorOptimize = true 时，该参数生效。  * isBacktestMode = true 时，默认 “None” ，可设置为：    + “ALL“：全部数据保留   + “20d”：支持按天保留数据，即交易日天数，如 “20d” 代表 20 个交易日   + “None”：不保留数据   + 20：支持按条数保留数据，如 20 代表每个 symbol 保留最新的 20 条 * isBacktestMode = false 时，无需设置 |
| ”addTimeColumnInIndicator“ | 指标订阅时是否给指标数表增加时间列 | BOOL 类型，默认 false true：增加  false：不增加 |
| "context" | 策略逻辑上下文类结构 | DICT 类型，策略全局变量构成的字典，如：  ``` context=dict(STRING,ANY) context["buySignalRSI"]=70. userConfig["context"]=context ``` |
| ”callbackForSnapshot “ | 快照行情触发回调模式 | dataType = 1 仅有。 INT 类型，可选值为：  0：表示只触发 `onSnapshot`  1 ：表示既触发 `onSnpshot` 又触发 `onBar`  2 ：表示只触发 `onBar`  默认为 0，当 frequency > 0 时，必须触发 `onBar` 回调函数，即 callbackForSnapshot = 1 或者 2 |
| “orderBookMatchingRatio” | 与行情订单薄的成交百分比 | dataType = 1 仅有。 DOUBLE 类型，默认 1.0，取值 0~1.0 之间 |
| “matchingRatio” | 区间撮合比例 | dataType = 1 仅有。 DOUBLE 类型，默认 1.0，取值0~1.0 之间。默认和成交百分比 orderBookMatchingRatio 相等 |
| "msgAs​PiecesOnSnapshot" | 回测时，是每条数据依次触发 `onSnapshot` 回调函数，还是同一时间戳的所有数据同时触发。 | BOOL 类型，默认值为 false，此时每条数据依次触发`onSnapshot` |

注：

不同的期货行情类型（dataType）的引擎配置参数有所差异：

快照行情触发回调模式“callbackForSnapshot” 、与行情订单薄的成交百分比 “orderBookMatchingRatio” 以及区间撮合比例
“matchingRatio” 只有在快照的行情类型中可以设置，即 dataType = 1。

### 基本信息表说明

接口 `createBacktester` 的参数 `securityReference` 和接口
`createBacktestEngine` 的参数 `securityReference`
的基本信息表字段可参考下表：

| **字段** | **类型** | **说明** |
| --- | --- | --- |
| symbol | SYMBOL或STRING | 期货合约代码 |
| multiplier | DOUBLE | 合约乘数 |
| marginRatio | DOUBLE | 保证金比率 |
| tradeUnit | DOUBLE | 合约单位 |
| priceUnit | DOUBLE | 报价单位 |
| priceTick | DOUBLE | 价格最小变动单位 |
| commission | DOUBLE | 费用 |
| deliveryCommissionMode | INT | 计费方式： 1：费用\*手数  2：费用\*金额 |
| lastTradingDay | DATE | 合约最后交易日，在该日期收盘时会自动平仓。  自动平仓时不触发 `onOrder` 和 `onTrade`，在交易明细表中orderStatus 为 1 且 label 为 \_\_auto\_close\_position\_on\_last\_trading\_day 的记录代表自动平仓。 |
| deliveryPrice | DOUBLE | 交割价。  最后交易日执行自动平仓时，系统将按照以下价格优先级成交。若高优先级价格未设置或不可用，则依次采用下一级价格：  1. 交割价  2. 结算价（settlement）  3. 最新成交价（lastPrice） |
| intradayClosingFee | DOUBLE | 日内平仓费用 |

## 快照

### 行情数据结构说明

通过 `Backtest::appendQuotationMsg`
写入的行情表结构如下：

```
colName=["symbol","symbolSource","timestamp","tradingDay","lastPrice","upLimitPrice",
        "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty","offerPrice",
        "offerQty","highPrice","lowPrice","prevClosePrice","settlementPrice",
        "prevSettlementPrice"]
colType= ["STRING","STRING","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE","LONG","LONG",
        "DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE","DOUBLE","DOUBLE",
        "DOUBLE","DOUBLE"]
messageTable=table(10000000:0, colName, colType)
```

注：

* 上述为快照行情（callbackForSnapshot = 0），即非快照合成 bar 行情的输入表结构。
* 字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING
  类型的列，或名为 signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

快照行情数据表必需字段如下所示：

|  |  |  |
| --- | --- | --- |
| **字段** | **类型** | **备注** |
| symbol | SYMBOL | 期货代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委托买价 |
| bidQty | LONG[] | 委托买量 |
| offerPrice | DOUBLE[] | 委托卖价 |
| offerQty | LONG[] | 委托卖价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| settlementPrice | DOUBLE | 结算价 |
| prevSettlementPrice | DOUBLE | 前结算价 |

快照行情（frequency > 0，callbackForSnapshot = 1 或者 2）表结构：

```
colName=["symbol","symbolSource","timestamp","tradingDay","lastPrice","upLimitPrice",
        "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty","offerPrice",
        "offerQty","highPrice","lowPrice","signal","prevClosePrice","settlementPrice",
        "prevSettlementPrice","open", "close","low","high","volume"]
colType= ["STRING","STRING","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE","LONG","LONG",
        "DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE","DOUBLE","DOUBLE","DOUBLE",
        "DOUBLE","DOUBLE","DOUBLE","DOUBLE",
        "DOUBLE","DOUBLE","LONG"]
messageTable=table(10000000:0, colName, colType)
```

注：

* 快照合成 bar 行情时（callbackForSnapshot = 1 或者 2），还需要增加五个字段："open",
  "close","low","high","volume"。
* 字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING
  类型的列，或名为 signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

快照行情数据表（使用快照合成 bar 行情）必需字段如下所示：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 期货代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委托买价 |
| bidQty | LONG[] | 委托买量 |
| offerPrice | DOUBLE[] | 委托卖价 |
| offerQty | LONG[] | 委托卖价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| settlementPrice | DOUBLE | 结算价 |
| prevSettlementPrice | DOUBLE | 前结算价 |
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

### 策略回调函数说明

快照行情回调函数 `onSnapshot`：输入参数 msg

msg 为字典时，是 symbol 为 key 值的 snapShot 数据字典，每个 snapShot 对象包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 期货代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委托买价 |
| bidQty | LONG[] | 委托买量 |
| offerPrice | DOUBLE[] | 委托卖价 |
| offerQty | LONG[] | 委托卖价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| settlementPrice | DOUBLE | 结算价 |
| prevSettlementPrice | DOUBLE | 前结算价 |
| open | DOUBLE | 合成 bar 行情的开盘价 （dataType = 1 或者 2 ，callbackForSnapshot = 1 或者 2 时才有） |
| close | DOUBLE | 合成 bar 行情的收盘价 （dataType = 1 或者 2 ，callbackForSnapshot = 1 或者 2 时才有） |
| low | DOUBLE | 合成 bar 行情的最低价 （dataType = 1 或者 2 ，callbackForSnapshot = 1 或者 2 时才有） |
| high | DOUBLE | 合成 bar 行情的最高价 （dataType = 1 或者 2 ，callbackForSnapshot = 1 或者 2 时才有） |
| volume | LONG | 合成 bar 行情的成交量 （dataType = 1 或者 2 ，callbackForSnapshot = 1 或者 2 时才有） |

注：

* 快照合成 bar 行情时（frequency > 0 且 callbackForSnapshot = 1 或者 2）, 输入参数
  msg 还需要增加五个字段："open", "close","low","high","volume"。
* 当 callbackForSnapshot = 1 时，还需回调 onBar 函数，输入参数 msg 的数据结构如下。

k 线行情回调函数 `onBar`：输入参数 msg

msg 是字典时，是 以 symbol 为 key 值的分钟频率的 K 线数据字典，每个 K 线包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 期货代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委托买价 |
| bidQty | LONG[] | 委托买量 |
| offerPrice | DOUBLE[] | 委托卖价 |
| offerQty | LONG[] | 委托卖价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| settlementPrice | DOUBLE | 结算价 |
| prevSettlementPrice | DOUBLE | 前结算价 |

## 分钟频或日频

### 行情数据结构说明

通过 `Backtest::appendQuotationMsg`
写入的行情表结构如下：

```
colName=["symbol","symbolSource","tradeTime","tradingDay","open","low","high","close",
"volume","amount","upLimitPrice","downLimitPrice","prevClosePrice",
"settlementPrice","prevSettlementPrice"]
colType=["SYMBOL","SYMBOL","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","LONG","DOUBLE",
"DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE"]
messageTable=table(10000000:0, colName, colType)
```

注：

字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING 类型的列，或名为
signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

分钟频行情数据表必需字段如下所示：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 期货代码 |
| symbolSource | STRING | 交易所 |
| tradeTime | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| open | DOUBLE | 开盘价 |
| low | DOUBLE | 最低价 |
| high | DOUBLE | 最高价 |
| close | DOUBLE | 收盘价 |
| volume | LONG | 成交量 |
| amount | DOUBLE | 成交金额 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| settlementPrice | DOUBLE | 结算价 |
| prevSettlementPrice | DOUBLE | 前结算价 |

回测行情回放结束时，发送一条 symbol 为 “END” 的消息:

```
messageTable=select top 1 * from messageTable
update messageTable set symbol="END"
Backtest::appendQuotationMsg(engine,messageTable)
```

### 策略回调函数说明

k 线行情回调函数 `onBar`：输入参数 msg

msg 是字典时，是 以 symbol 为 key 值的分钟频率的 K 线数据字典，每个 K 线包含字段如下：

| **字段** | **类型** | **备注** |
| --- | --- | --- |
| symbol | SYMBOL | 期货代码 |
| symbolSource | STRING | 交易所 |
| timestamp | TIMESTAMP | 时间戳 |
| tradingDay | DATE | 交易日/结算日期 |
| lastPrice | DOUBLE | 最新成交价 |
| upLimitPrice | DOUBLE | 涨停价 |
| downLimitPrice | DOUBLE | 跌停价 |
| totalBidQty | LONG | 区间成交买数量 |
| totalOfferQty | LONG | 区间成交卖数量 |
| bidPrice | DOUBLE[] | 委托买价 |
| bidQty | LONG[] | 委托买量 |
| offerPrice | DOUBLE[] | 委托卖价 |
| offerQty | LONG[] | 委托卖价 |
| highPrice | DOUBLE | 最高价 |
| lowPrice | DOUBLE | 最低价 |
| signal | DOUBLE[] | 其他字段列表 |
| prevClosePrice | DOUBLE | 前收盘价 |
| settlementPrice | DOUBLE | 结算价 |
| prevSettlementPrice | DOUBLE | 前结算价 |

## 快照+分钟频率

### 行情数据结构说明

通过接口 `appendQuotationMsg` 向引擎中插入数据时，*msg* 为一个字典，key 支持
'ohlc'，'snapshot' 或 'indicator' 三种：

* 'ohlc'
  为分钟频行情表，结构如下：

  ```
  colName=["symbol","symbolSource","tradeTime","tradingDay","open","low","high","close",
  "volume","amount","upLimitPrice","downLimitPrice","prevClosePrice",
  "settlementPrice","prevSettlementPrice"]
  colType=["SYMBOL","SYMBOL","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","LONG","DOUBLE",
  "DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE"]
  messageTable=table(10000000:0, colName, colType)
  ```

  注：

  字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING 类型的列，或名为
  signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

  分钟频行情数据表必需字段如下所示：

  | **字段** | **类型** | **备注** |
  | --- | --- | --- |
  | symbol | SYMBOL | 期货代码 |
  | symbolSource | STRING | 交易所 |
  | tradeTime | TIMESTAMP | 时间戳 |
  | tradingDay | DATE | 交易日/结算日期 |
  | open | DOUBLE | 开盘价 |
  | low | DOUBLE | 最低价 |
  | high | DOUBLE | 最高价 |
  | close | DOUBLE | 收盘价 |
  | volume | LONG | 成交量 |
  | amount | DOUBLE | 成交金额 |
  | upLimitPrice | DOUBLE | 涨停价 |
  | downLimitPrice | DOUBLE | 跌停价 |
  | signal | DOUBLE[] | 其他字段列表 |
  | prevClosePrice | DOUBLE | 前收盘价 |
  | settlementPrice | DOUBLE | 结算价 |
  | prevSettlementPrice | DOUBLE | 前结算价 |
* 'snapshot'
  为快照行情表，结构如下：

  ```
  colName=["symbol","symbolSource","timestamp","tradingDay","lastPrice","upLimitPrice",
          "downLimitPrice","totalBidQty","totalOfferQty","bidPrice","bidQty","offerPrice",
          "offerQty","highPrice","lowPrice","prevClosePrice","settlementPrice",
          "prevSettlementPrice"]
  colType= ["STRING","STRING","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE","LONG","LONG",
          "DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE","DOUBLE","DOUBLE",
          "DOUBLE","DOUBLE"]
  messageTable=table(10000000:0, colName, colType)
  ```

  注：

  + 上述为快照行情（callbackForSnapshot = 0），即非快照合成 bar 行情的输入表结构。
  + 字段名须严格与下表一致，字段顺序除首列必须为 symbol 列外，无其它要求，此外还支持 INT，DOUBLE，STRING
    类型的列，或名为 signal 的 DOUBLE ARRAY VECTOR 类型的列作为扩展字段。

  快照行情数据表必需字段如下所示：

  |  |  |  |
  | --- | --- | --- |
  | **字段** | **类型** | **备注** |
  | symbol | SYMBOL | 期货代码 |
  | symbolSource | STRING | 交易所 |
  | timestamp | TIMESTAMP | 时间戳 |
  | tradingDay | DATE | 交易日/结算日期 |
  | lastPrice | DOUBLE | 最新成交价 |
  | upLimitPrice | DOUBLE | 涨停价 |
  | downLimitPrice | DOUBLE | 跌停价 |
  | totalBidQty | LONG | 区间成交买数量 |
  | totalOfferQty | LONG | 区间成交卖数量 |
  | bidPrice | DOUBLE[] | 委托买价 |
  | bidQty | LONG[] | 委托买量 |
  | offerPrice | DOUBLE[] | 委托卖价 |
  | offerQty | LONG[] | 委托卖价 |
  | highPrice | DOUBLE | 最高价 |
  | lowPrice | DOUBLE | 最低价 |
  | signal | DOUBLE[] | 其他字段列表 |
  | prevClosePrice | DOUBLE | 前收盘价 |
  | settlementPrice | DOUBLE | 结算价 |
  | prevSettlementPrice | DOUBLE | 前结算价 |
* 'indicator' 为对应 onBar 回调的历史指标数据表。设置该表时，不能同时使用
  `subscribeIndicator` 订阅 ohlc/kline 类型的指标。该表的字段必须包含
  symbol 和 timestamp，其后可以是 INT、DOUBLE 或 STRING 类型的扩展字段。
