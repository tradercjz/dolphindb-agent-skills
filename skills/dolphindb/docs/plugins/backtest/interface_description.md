<!-- Auto-mirrored from upstream `documentation-main/plugins/backtest/interface_description.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 接口说明

本节将介绍 DolphinDB 的回测引擎接口。用户可以基于自定义的策略创建回测引擎并执行回测，获取每日持仓、每日权益、收益概述、成交明细等回测结果。

## appendEndMarker

**语法**

```
Backtest::appendEndMarker​(engine)
```

**详情**

结束回测，触发事件函数 `afterTrading` 和 `finalize`。相当于通过
`appendQuotationMsg` 追加一条 END 类型数据。

**参数**

**engine** 回测引擎句柄。

## appendQuotationMsg

**语法**

```
Backtest::appendQuotationMsg(engine, msg)
```

**详情**

插入行情执行策略回测。

**参数**

**engine** 回测引擎句柄。

**msg** 行情输入表，表结构请参考行情数据结构说明。

## cancelOrder

**语法**

```
Backtest::cancelOrder(engine, symbol="", orders=NULL, label="")
```

**详情**

取消订单。

* 若 *symbol* 不为空，其他字段为空，则取消该标的的所有订单。
* 若 *symbol* 为空，*orders* 不为空，则取消 *orders* 中的订单。
* 若 *symbol* 为空，orders 为空，则取消 *label* 指定的订单。
* 若 *symbol*，*orders，*
  *label* 都为空，则取消 *engine* 中的所有订单。

**参数**

**engine** 回测引擎句柄，在回调函数中可通过 `contextDict["engine"]` 获取。

**symbol** STRING 类型标量，要取消的订单的证券代码，可选参数。

**orders** INTEGRAL 类型向量，要取消的订单 ID 列表，可选参数。

**label** STRING 类型标量，要取消的订单的备注信息。

## createBacktestEngine

注：

此接口为 createBacktester 的旧版本接口。

**语法**

```
Backtest::createBacktestEngine(name, config, [securityReference], initialize, beforeTrading, onTick/onBar, onSnapshot, onOrder, onTrade, afterTrading, finalize)
```

**详情**

创建回测引擎，同时设置所有的回调函数。此接口为 `createBacktester` 的旧版本接口，适用于所有资产。

返回创建的回测引擎句柄。

**参数**

**name** STRING 类型标量，表示回测引擎名称。

**config** 一个字典，表示回测引擎的配置项。key 是 STRING 类型，代表配置项的名称，value 是该配置项的具体配置。详情请参考股票回测配置，期权回测配置，期货回测配置，债券回测配置，数字货币回测配置。

**securityReference** 基础信息表，仅当资产为股票时是可选参数，其他资产均为必选参数。

**initialize** 初始化回调函数，回测开始时触发调用。

**beforeTrading** 每日盘前回调函数，每日开盘前触发调用。

**onTick/onBar** 逐笔/分钟或者日线行情回调函数，可选参数，订阅快照行情时触发调用。

**onSnapshot** 快照行情回调函数，订阅快照行情时触发调用。

**onOrder** 委托回报通知函数，订单变更时触发调用。

**onTrade** 成交回报通知函数，订单交易时触发调用。

**afterTrading** 每日盘后回调函数，每日收盘时触发调用。

**finalize** 策略结束回调函数，回测结束时会触发调用。

上述回调函数中，onTick, onBar, onSnapshot 的触发条件如下，使用时应根据 *config*参数的配置，指定对应的回调函数，无需全部指定：

| **输入数据类型** | **frequency 参数设置** | **可触发的函数** |
| --- | --- | --- |
| dataType=0 | frequency=0 | onTick |
| frequency>0 | onTick, onSnapshot |
| dataType=1 或 2 | frequency=0 | onSnapshot |
| frequency>0 | onSnapshot, onBar |

## createBacktester

**语法**

```
Backtest::createBacktester(name, config, eventCallbacks, [jit=false], [securityReference])
```

**详情**

创建回测引擎，同时设置所有的回调函数。

返回创建的回测引擎句柄。

**参数**

**name** STRING 类型标量，表示回测引擎名称。

**config** 一个字典，表示回测引擎的配置项。字典的 key 是 STRING 类型，代表配置项的名称，value
是该配置项的具体配置，详情请参考股票回测配置，期权回测配置，期货回测配置。

**eventCallbacks** 一个字典，表示策略回调函数。字典的 key 是 STRING 类型，代表回调函数，value 为对应函数的定义。key 的可选值为：

* "initialize" 策略初始化回调函数，回测开始时触发调用。
* "beforeTrading" 每日盘前回调函数，每日开盘前触发调用。
* "onTick" 逐笔行情回调函数，可选参数。订阅逐笔行情时触发调用。
* "onSnapshot" 快照行情回调函数，订阅快照行情时触发调用。
* "onBar" 分钟或者日线行情回调函数，可选参数，订阅快照行情时触发调用。
* "onOrder" 委托回报通知函数，订单变更时触发调用。
* "onTrade" 成交回报通知函数，订单交易时触发调用。
* "afterTrading" 每日盘后回调函数，每日收盘时触发调用。
* "finalize" 策略结束回调函数，回测结束时会触发调用。
* "onTimer" 定时回调函数，value 为一个字典：
  + dataType=1，2，3，5，6 时字典的键是 SECOND 类型，代表触发时间，其值是定时回调函数。
  + dataType=4 时字典的键是 STRING 类型，可选值为：

    - “dateList”，其值为 DATE 类型的标量或向量，表示触发日期；
    - “onTimeCallback”，其值为定时回调函数。

上述回调函数中，onTick, onBar, onSnapshot 的触发条件如下，使用时应根据 *config*参数的配置，指定对应的回调函数，无需全部指定：

| **输入数据类型** | **frequency 参数设置** | **可触发的函数** |
| --- | --- | --- |
| dataType=0 | frequency=0 | onTick |
| frequency>0 | onTick, onSnapshot |
| dataType=1或2 | frequency=0 | onSnapshot |
| frequency>0 | onSnapshot, onBar |

**jit** BOOL 类型标量，表示是否开启 JIT 优化。默认值为 false，表示不开启。当前版本暂不支持数字货币回测开启 JIT
优化，暂不支持模拟交易模式（isBacktestMode=false）开启 JIT 优化。

**securityReference** 合约的基本信息表。仅当资产为股票时是可选参数，其他资产均为必选参数。

## dropBacktestEngine

**语法**

```
Backtest::dropBacktestEngine(engine)
```

**详情**

删除回测引擎。仅限管理员用户和引擎创建者调用。

**参数**

**engine** 回测引擎句柄。

## enableEnginePersistence

**语法**

```
Backtest::enableEnginePersistence(engine, snapshotDir, [freq], [udf])
```

**详情**

启用引擎持久化。目前支持股票和两融的快照、分钟频和日频回测；暂不支持回调函数 `onTimer`；暂不支持 JIT 模式。

快照保存时机如下：

* 调用该接口时，立即保存一次快照。
* 每当 `appendQuotationMsg` 完成一批行情回测时：

  + 如果订单状态发生变化，会立即保存一次当前快照；
  + 如果订单状态未改变，若当前行情时间距离上次快照的行情时间超过 *freq*，则保存一次当前快照。
* 每当触发 `beforeTrading`、`afterTrading`
  和回测结束时，保存一次快照。

**参数**

**engine** 回测引擎句柄。

**snapshotDir** STRING 类型标量，表示快照文件的存储目录。

**freq** 可选参数，INT 类型标量，表示订单状态未改变后触发持久化的最小间隔，单位为秒。默认值为 0，表示行情回调一次都自动触发持久化。若小于
0，代表不会自动触发持久化。

**udf** 可选参数，一个字典，如果回调函数中调用了用户自定义的函数，则需要在此指定，以确保后续恢复后正常使用。字典的 key 是 STRING
类型，表示函数名；value 是 ANY 类型，代表对应函数。

## extractSnapshotInfo

**语法**

```
Backtest::extractSnapshotInfo(snapshotDir, engineName, [needContext=true])
```

**详情**

提取快照文件保存的回测引擎的基础信息。仅支持 admin 用户和创建者调用。

返回一个字典，包含以下字段：

| 字段名 | 含义 |
| --- | --- |
| engineName | 引擎名 |
| strategyGroup | 策略类型 |
| dataType | 行情类型 |
| createdUser | 创建者 |
| createdTime | 快照创建时间 |
| pluginVersion | 插件版本 |
| isBacktestMode | 是否是回测模式 |
| context | 该引擎的上下文字典 |

**参数**

**snapshotDir** STRING 类型标量，表示快照文件的存储目录。

**engineName** STRING 类型标量，表示快照回测引擎的名字，必须与创建快照的引擎名字一致。

**needContext** 可选参数，BOOL 类型，表示是否返回上下文字典。默认值为 true，此时返回结果中包含回测引擎的上下文字典，对应 key 为
“context“。注意：上下文字典 context 中的 resource 的值将不会被获取。

## forceTriggerEngineSnapshot

**语法**

```
Backtest::forceTriggerEngineSnapshot(engine, force=false)
```

**详情**

立即触发保存快照。该引擎必须已通过 `enableEnginePersistence` 已经开启持久化功能。

此函数不可在回调函数内调用。

**参数**

**engine** 回测引擎句柄。

**force** BOOL 类型，表示是否强制出发保存快照。默认值为 false，仅当上次持久化后调用过
`appendQuotationMsg`、`submitOrder` 和
`cancelOrder` 接口时才触发，否则不触发。

## getAvailableCash

**语法**

```
Backtest::getAvailableCash(engine)
```

**详情**

查询账户可用现金。

**参数**

**engine** 回测引擎句柄。

## getBacktestEngineList

**语法**

```
Backtest::getBacktestEngineList()
```

**详情**

获取所有的回测引擎。

## getBacktestEngineStat

**语法**

```
Backtest::getBacktestEngineStat(engine, [block=true])
```

**详情**

查看回测引擎状态。

返回一个表，包含以下字段：

* name：回测引擎名称
* user：回测引擎的创建者
* status：回测引擎的状态，可能的值包括 OK（可用），END（正常结束），FATAL（不可用）。对于状态为 FATAL 的引擎：
  + 如果是插入数据的格式错误导致的 FATAL，则后续插入正确格式数据，即可恢复正常；
  + 如果是回调函数抛出异常导致的 FATAL，则使用 `updateEventCallbacks`
    修复回调函数，即可继续正常使用。
* lastErrMsg：最后一条错误信息
* numIndicators：订阅的指标数量
* snapshotTimestamp：回测引擎当前处理过的最新数据的时间戳
* isBacktestMode：当前是回测还是模拟交易模式

**参数**

**engine** 回测引擎句柄。

**block** 可选参数，BOOL 类型，表示当其它线程正在使用该回测引擎时，是否阻塞当前线程。默认为 true，阻塞等待直到获取状态结果返回；若设置为
false，会立即抛出异常。

## getConfig

**语法**

```
Backtest::getConfig(engine)
```

**详情**

获取回测引擎的配置。

**参数**

**engine** 回测引擎句柄。

## getContextDict

**语法**

```
Backtest::getContextDict(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

返回逻辑上下文。

## getDailyPosition

**语法**

```
Backtest::getDailyPosition(engine, [symbol])
```

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，可选参数，表示要获取的标的。默认为空，此时获取所有标的的持仓数据。

**详情**

通常在回测结束调用，返回每日盘后的持仓数据详情。盘中调用会丢失当日信息，返回前一天的持仓数据。

当资产为股票、期货、期权时，持仓数据详情表结构如下：

| 字段 | 含义 |
| --- | --- |
| symbol | 标的代码 |
| tradeDate | 交易日 |
| lastDayLongPosition | 昨日买持仓 |
| lastDayShortPosition | 昨日卖持仓 |
| longPosition | 买持仓量 |
| longPositionAvgPrice | 买成交均价 |
| shortPosition | 卖持仓量 |
| shortPositionAvgPrice | 卖成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todayBuyValue | 当日买成交金额 |
| todaySellVolume | 当日卖成交数量 |
| todaySellValue | 当日卖成交金额 |
| strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |

当为融资融券模式时，持仓数据详情表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| tradeDate | 交易日 |
| lastDayMarginSecuPosition | 昨日担保品买入持仓量 |
| lastDayMarginDebt | 昨日收盘融资负债 |
| lastDaySecuLendingDebt | 昨日收盘融券负债 |
| marginSecuPosition | 担保品买入持仓量 |
| marginSecuAvgPrice | 买持仓均价 |
| marginBuyPosition | 融资买入持仓量 |
| marginBuyValue | 融资买入金额 |
| secuLendingPosition | 融券卖出持仓量 |
| secuLendingSellValue | 融券卖出金额 |
| closePrice | 收盘价 |
| longPositionConcentration | 多头集中度 |
| shortPositionConcentration | 净空头集中度 |
| marginBuyProfit | 融资盈亏 |
| financialFee | 融资利息 |
| secuLendingProfit | 融券盈亏 |
| secuLendingFee | 融券费用 |
| strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |

当资产为债券时，持仓数据详情表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨买持仓数量 |
| lastDayShortPosition | 昨卖持仓数量 |
| longPosition | 买持仓量 |
| shortPosition | 卖持仓量 |
| longPositionAvgPrice | 买成交均价 |
| shortPositionAvgPrice | 卖成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todaySellVolume | 当日卖成交数量 |
| totalValue | 持仓总额 |
| accruedInterest | 应计利息 |
| fullBondPrice | 债券全价 |
| lastPrice | 债券净价 |
| yield | 收益率 |
| interestIncome | 利息收入 |
| floatingProfit | 浮动损益 |
| realizedProfit | 实际损益 |
| totalProfit | 总损益 |
| duration | 久期 |
| convexity | 凸性 |
| DV01 | DV01 |

## getDailyTotalPortfolios

**语法**

```
Backtest::getDailyTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

通常在回测结束调用，获取策略每日权益指标表。回测的资产不同，返回表的结构也有所差异：

* 股票：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | frozenFunds | 冻结资金 |
  | totalFee | 总费用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现盈亏 |
  | totalPnl | 总盈亏 |
  | benchmarkClosePrice | 基准每日收盘价，仅当设置 *benchmark* 时返回 |
  | benchmarkNetValue | 基准每日净值，仅当设置 *benchmark* 时返回 |
  | bottomNetValue | 底仓净值，仅当设置底仓时返回 |
  | strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |
* 融资融券：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | lineOfCredit | 授信额度 |
  | availableCash | 可用资金 |
  | lastDayMarginDebt | 昨日收盘融资负债 |
  | lastDaySecuLendingDebt | 昨日收盘融券负债 |
  | marginSecuMarketValue | 担保品买入市值 |
  | marginDebt | 融资负债 |
  | secuLendingSellValue | 融券卖出金额（融券负债） |
  | marginBalance | 融资融券余额 |
  | secuLendingDebt | 融券负债 |
  | financialFee | 融资利息 |
  | secuLendingFee | 融券费用 |
  | maintenanceMargin | 维保比例 |
  | availableMarginBalance | 保证金可用余额 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | yield | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | benchmarkClosePrice | 基准每日收盘价，仅当设置 *benchmark* 时返回 |
  | benchmarkNetValue | 基准每日净值，仅当设置 *benchmark* 时返回 |
  | strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |
* 期货/期权：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | margin | 保证金占用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现累计盈亏 |
  | totalPnl | 累计盈亏 |
  | totalMarketValue | 总市值（仅期权） |
  | cash | 可用资金 |
  | totalEquity | 账户总权益 |
  | marginRatio | 保证金占用比例 |
  | pnl | 账户当日盈亏 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | benchmarkClosePrice | 基准每日收盘价，仅当设置 *benchmark* 时返回 |
  | benchmarkNetValue | 基准每日净值，仅当设置 *benchmark* 时返回 |
* 债券

  | **字段名称** | **字段说明** |
  | --- | --- |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | totalFee | 总费用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现盈亏 |
  | totalPnl | 总盈亏 |

## getDailyTradingStatistics

**语法**

```
Backtest::getDailyTradingStatistics(engine, [symbol])
```

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，可选参数，表示要获取的合约。默认为空，此时获取所有合约的持仓数据。

**详情**

仅支持股票、期权、期货，获取每日交易统计信息。

指定 *symbol* 时返回字典，否则返回表，包含以下字段：

| **字段** | **含义** |
| --- | --- |
| symbol | 标的代码 |
| assetType | 资产类型（仅多资产回测时包含该字段） |
| tradeDate | 交易日期 |
| todayBuyOpenTradeVolume | 当日买开成交交易量 |
| todayBuyOpenTradeValue | 当日买开成交交易额 |
| todayBuyOpenAvgPrice | 当日买开成交平均价 |
| todaySellOpenTradeVolume | 当日卖开成交交易量 |
| todaySellOpenTradeValue | 当日卖开成交交易额 |
| todaySellOpenAvgPrice | 当日卖开成交平均价 |
| todaySellCloseTradeVolume | 当日卖平仓交易量 |
| todaySellCloseTradeValue | 当日卖平仓交易额 |
| todaySellCloseAvgPrice | 当日卖平成交均价 |
| todayBuyCloseTradeVolume | 当日买平仓交易量 |
| todayBuyCloseTradeValue | 当日买平仓交易额 |
| todayBuyCloseAvgPrice | 当日买平成交均价 |

## getEventCallbacks

**语法**

```
Backtest::getEventCallbacks(engine)
```

**详情**

获取回测引擎使用的策略回调函数。仅支持引擎创建者调用。

返回一个字典。

**参数**

**engine** 回测引擎句柄。

## getFuturesTotalPortfolios

**语法**

```
Backtest::getFuturesTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

查询每日期货盈亏情况，返回表结构如下：

| **字段名称** | **字段说明** |
| --- | --- |
| tradeDate | 日期 |
| margin | 保证金占用 |
| floatingPnl | 浮动盈亏 |
| realizedPnl | 已实现累计盈亏 |
| totalPnl | 累计盈亏 |
| cash | 可用资金 |
| totalEquity | 账户总权益 |
| marginRatio | 保证金占用比例 |
| pnl | 账户当日盈亏 |
| netValue | 账户单位净值 |
| totalReturn | 截至当日的累计收益率 |
| ratio | 账户每日收益率 |
| totalFee | 总费用 |

## getIndicatorSchema

**语法**

```
Backtest::getIndicatorSchema(engine,[marketDataType])
```

**参数**

**engine** 回测引擎句柄。

**marketDataType** STRING
类型标量，表示订阅指标的行情类型，如果该引擎只订阅了一种行情类型指标，则该参数可省略，否则必须指定该参数。

**详情**

返回一张策略指标空表，表结构如下：

| **列名** | **数据类型** | **说明** |
| --- | --- | --- |
| symbol | SYMBOL | 标的代码 |
| timestamp | TIMESTAMP | 时间戳 |
| 订阅的指标名称 | DOUBLE | 订阅的指标 |
| … | … | … |

## getMarginSecuPosition

**语法**

```
Backtest::getMarginSecuPosition(engine,[symbolList])
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbolList** 可选参数，STRING 类型向量，表示股票代码列表。省略时默认返回所有股票担保品买入持仓信息。

**详情**

查询担保品买入持仓信息。

若 *engine* 由接口 `createBacktester` 创建，则

* *symbolList* 的长度为 1 时返回字典
* *symbolList* 的长度不为 1 时报错
* *symbolList* 省略时返回表

若 *engine* 由接口 `createBacktester` 创建，则返回表。

返回表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨日收盘时担保品买入持仓量 |
| lastDayBuyValue | 昨日收盘时担保品买入金额 |
| longPosition | 担保品买入持仓量 |
| buyValue | 担保品买入金额 |
| todayBuyVolume | 当日担保品买入成交数量 |
| todayBuyValue | 当日担保品买入成交金额 |
| strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |

## getMarginTradingPosition

**语法**

```
Backtest::getMarginTradingPosition(engine,symbolList)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbolList**可选参数，STRING 类型向量，表示股票代码列表。省略时默认返回所有股票融资买入持仓信息。

**详情**

查询融资买入持仓信息。

若 *engine* 由接口 `createBacktester` 创建，则

* *symbolList* 的长度为 1 时返回字典
* *symbolList* 的长度不为 1 时报错
* *symbolList* 省略时返回表

若 *engine* 由接口 `createBacktester` 创建，则返回表。

返回表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨日收盘时融资买入持仓量 |
| lastDayBuyValue | 昨日收盘时融资买入金额 |
| lastDayMarginDebt | 昨日收盘时融资买入负债 |
| longPosition | 融资买入持仓量 |
| buyValue | 融资买入金额 |
| todayBuyVolume | 当日融资买入成交数量 |
| todayBuyValue | 当日融资买入金额 |
| marginBuyProfit | 融资盈亏 |
| financialFee | 融资利息 |
| strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |

## getOpenOrders

**语法**

```
Backtest::getOpenOrders(engine, symbol=NULL, orders=NULL, label="", outputQueuePosition=false)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过 `contextDict["engine"]` 获取。

**symbol** STRING 类型标量，证券代码，可选参数。

**orders** INTEGRAL 类型向量，订单 ID 列表，可选参数。

**label** STRING 类型标量，用作备注，可选参数。

**outputQueuePosition** BOOL 类型标量，是否输出详细信息（包括 openVolumeWithBetterPrice,
openVolumeWithWorsePrice, openVolumeAtOrderPrice, priorOpenVolumeAtOrderPrice,
depthWithBetterPrice）。可选参数，默认为 false，表示不输出。仅支持股票和期货品种设置此参数。

**详情**

查询未成交订单。

* 若 *symbol* 不为空，则查询该标的的未成交订单。
* 若 *symbol* 为空，*orders* 不为空，则查询 *orders* 中未成交的订单。
* 若 *symbol* 为空，orders 为空，则查询 *label* 指定的未成交订单。

查询未成交订单信息。返回一个元素全为字典的元组，或一张表。

对于除债券外的其它资产，结构如下：

| key | value 类型 | value 说明 |
| --- | --- | --- |
| orderId | LONG | 订单 ID |
| timestamp | TIMESTAMP | 时间 |
| symbol | STRING | 标的代码 |
| price | DOUBLE | 委托价格 |
| totalQty | LONG | 用户订单数量 |
| openQty | LONG | 用户订单余量 |
| direction | INT | 1（买开 ），2（卖开），3（卖平），4（买平） |
| isMacthing | INT | 订单是否到达撮合时间 |
| openVolumeWithBetterPrice | LONG | 优于委托价格的行情未成交委托单总量（仅当 *outputQueuePosition=true* 时返回） |
| openVolumeWithWorsePrice | LONG | 次于委托价格的行情未成交委托单总量（仅当 *outputQueuePosition=true* 时返回） |
| openVolumeAtOrderPrice | LONG | 等于委托价格行情未成交委托单总量（仅当 *outputQueuePosition=true* 时返回） |
| priorOpenVolumeAtOrderPrice | LONG | 等于委托价格行情且比自己早的行情未成交委托单总量（仅当 *outputQueuePosition=true*时返回） |
| depthVolumeWithBetterPrice | INT | 优于委托价格的行情未成交价格档位深度（仅当 *outputQueuePosition=true*时返回） |
| updateTime | TIMESTAMP | 最新更新时间 |

对于债券，结构如下：

| **名称** | **类型** | **含义** |
| --- | --- | --- |
| orderId | LONG | 订单id |
| time | TIMESTAMP | 时间 |
| symbol | STRING | 股票标的 |
| bidPrice | DOUBLE | 委买价格 |
| bidTotalQty | LONG | 用户订单委买数量 |
| bidRemainQty | LONG | 用户订单委买余量 |
| askPrice | DOUBLE | 委卖委托价格 |
| askTotalQty | LONG | 用户订单委卖数量 |
| askRemainQty | LONG | 用户订单委卖余量 |
| direction | INT | 1：买 2：卖  3：双边 |
| label | STRING | 备注 |

## getOptionTotalPortfolios

**语法**

```
Backtest::getOptionTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

查询每日期权盈亏情况，返回表结构如下：

| **字段名称** | **字段说明** |
| --- | --- |
| tradeDate | 日期 |
| margin | 保证金占用 |
| floatingPnl | 浮动盈亏 |
| realizedPnl | 已实现累计盈亏 |
| totalPnl | 累计盈亏 |
| totalMarketValue | 账户总市值 |
| cash | 可用资金 |
| totalEquity | 账户总权益 |
| marginRatio | 保证金占用比例 |
| pnl | 账户当日盈亏 |
| netValue | 账户单位净值 |
| totalReturn | 截至当日的累计收益率 |
| ratio | 账户每日收益率 |
| totalFee | 总费用 |

## getPosition

**语法**

```
Backtest::getPosition(engine, symbol="")
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbol** STRING 类型标量，证券代码，可选参数。

**详情**

获取持仓信息。

* 若不指定 *symbol*，返回表；
* 若指定 *symbol*，返回字典；
* 开启 JIT 优化时必须指定 *symbol*。

返回结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayLongPosition | 昨买持仓数量 |
| lastDayShortPosition | 昨卖持仓数量 |
| longPosition | 买持仓量 |
| shortPosition | 卖持仓量 |
| longPositionAvgPrice | 买成交均价 |
| shortPositionAvgPrice | 卖成交均价 |
| todayBuyVolume | 当日买成交数量 |
| todaySellVolume | 当日卖成交数量 |
| totalValue | 持仓总额 |
| accruedInterest | 应计利息 |
| fullBondPrice | 债券全价 |
| lastPrice | 债券净价 |
| yield | 收益率 |
| interestIncome | 利息收入 |
| floatingProfit | 浮动损益 |
| realizedProfit | 实际损益 |
| totalProfit | 总损益 |
| duration | 久期 |
| convexity | 凸性 |
| DV01 | DV01 |

## getReturnSummary

**语法**

```
Backtest::getReturnSummary(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

用于回测结束时计算策略的收益概述，返回一张收益概述表。收益表结构如下：

* **股票/期货/期权/债券：**

  | **字段名称** | **字段说明** |
  | --- | --- |
  | totalReturn | 总收益 |
  | annualReturn | 年化收益率 |
  | annualVolatility | 年化波动率 |
  | annualSkew | 收益率偏度 |
  | annualKur | 收益率峰度 |
  | sharpeRatio | 夏普率 |
  | maxDrawdown | 最大回撤 |
  | drawdownRatio | 收益回撤比 |
  | beta | beta系数 |
  | alpha | a系数 |
  | benchmarkReturn | 基准收益 |
  | annualExcessReturn | 年化超额收益 |
  | turnoverRate | 换手率 |
  | dailyWinningRate | 日胜率 |
  | maxMarginRatio | 策略最大保证金占用比例（期货期权独有字段） |
  | strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |
* 融资融券模式，返回的收益表除上述字段外 ，还包含以下字段：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | totalFee | 佣金与手续费之和 |
  | financialFee | 融资利息 |
  | secuLendingFee | 融券费用 |
  | bottomRet | 底仓收益 |
  | bottomExcessRet | 底仓超额收益 |

## getSecuLendingPosition

**语法**

```
Backtest::getSecuLendingPosition(engine,symbolList)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbolList** 可选参数，STRING 类型向量，表示股票代码列表。省略时默认返回所有股票融券卖出信息。

**详情**

查询融券卖出信息。

若 *engine* 由接口 `createBacktester` 创建，则

* *symbolList* 的长度为 1 时返回字典
* *symbolList* 的长度不为 1 时报错
* *symbolList* 省略时返回表

若 *engine* 由接口 `createBacktester` 创建，则返回表。

返回表结构如下：

| **字段** | **名称** |
| --- | --- |
| symbol | 标的代码 |
| lastDayShortPosition | 昨日融券卖出持仓量 |
| lastDayShortValue | 昨日融券卖出金额 |
| lastDaySecuLendingDebt | 昨日收盘时融券卖出负债 |
| shortPosition | 融券卖出持仓量 |
| shortValue | 融券卖出金额 |
| todayShortVolume | 当日融券卖出成交量 |
| todayShortValue | 当日融券卖出金额 |
| secuLendingProfit | 融券盈亏 |
| secuLendingFee | 融券费用 |
| strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |

## getStockTotalPortfolios

**语法**

```
Backtest::getStockTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

获取当前的股票策略权益指标，返回一个字典，结构如下：

| **key** | **value** |
| --- | --- |
| tradeDate | 日期 |
| cash | 可用资金 |
| floatingPnl | 浮动盈亏 |
| realizedPnl | 已实现盈亏 |
| totalPnl | 总盈亏 |
| totalMarketValue | 账户总市值 |
| totalEquity | 账户总权益 |
| netValue | 账户单位净值 |
| totalReturn | 截至当日的累计收益率 |
| ratio | 账户每日收益率 |
| pnl | 账户当日盈亏 |
| totalFee | 总费用 |
| frozenFunds | 冻结资金 |

## getTodayPnl

**语法**

```
Backtest::getTodayPnl(engine, symbol)
```

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，表示股票标的。

**详情**

该接口仅可用于股票，获取账户盈亏。

返回一个字典，结构如下：

| **key** | **value** |
| --- | --- |
| symbol | 标的代码 |
| pnl | 当前账户中该标的的盈亏金额 |
| todayPnl | 当日账户中该标的的盈亏金额 |

## getTodayTradingStatistics

**语法**

```
Backtest::getTodayTradingStatistics(engine, [symbol])
```

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，可选参数，表示要获取的合约。默认为空，此时获取所有合约的持仓数据。

**详情**

仅支持股票、期权、期货，获取当日交易统计信息。

指定 *symbol* 时返回字典，否则返回表，包含以下字段：

| **字段** | **含义** |
| --- | --- |
| symbol | 标的代码 |
| assetType | 资产类型（仅多资产回测时包含该字段） |
| tradeDate | 交易日期 |
| todayBuyOpenTradeVolume | 当日买开成交交易量 |
| todayBuyOpenTradeValue | 当日买开成交交易额 |
| todayBuyOpenAvgPrice | 当日买开成交平均价 |
| todaySellOpenTradeVolume | 当日卖开成交交易量 |
| todaySellOpenTradeValue | 当日卖开成交交易额 |
| todaySellOpenAvgPrice | 当日卖开成交平均价 |
| todaySellCloseTradeVolume | 当日卖平仓交易量 |
| todaySellCloseTradeValue | 当日卖平仓交易额 |
| todaySellCloseAvgPrice | 当日卖平成交均价 |
| todayBuyCloseTradeVolume | 当日买平仓交易量 |
| todayBuyCloseTradeValue | 当日买平仓交易额 |
| todayBuyCloseAvgPrice | 当日买平成交均价 |

## getTotalPortfolios

**语法**

```
Backtest::getTotalPortfolios(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

获取当前策略权益指标。

若 *engine* 通过 `createBacktestEngine` 创建，则返回一张表；若通过
`createBacktester` 创建，则返回一个字典。结构如下：

* 股票：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | frozenFunds | 冻结资金 |
  | totalFee | 总费用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现盈亏 |
  | totalPnl | 总盈亏 |
  | benchmarkClosePrice | 基准每日收盘价，仅当设置 *benchmark* 时返回 |
  | benchmarkNetValue | 基准每日净值，仅当设置 *benchmark* 时返回 |
  | bottomNetValue | 底仓净值，仅当设置底仓时返回 |
  | strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |
* 融资融券：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | lineOfCredit | 授信额度 |
  | availableCash | 可用资金 |
  | lastDayMarginDebt | 昨日收盘融资负债 |
  | lastDaySecuLendingDebt | 昨日收盘融券负债 |
  | marginSecuMarketValue | 担保品买入市值 |
  | marginDebt | 融资负债 |
  | secuLendingSellValue | 融券卖出金额（融券负债） |
  | marginBalance | 融资融券余额 |
  | secuLendingDebt | 融券负债 |
  | financialFee | 融资利息 |
  | secuLendingFee | 融券费用 |
  | maintenanceMargin | 维保比例 |
  | availableMarginBalance | 保证金可用余额 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | yield | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | benchmarkClosePrice | 基准每日收盘价，仅当设置 *benchmark* 时返回 |
  | benchmarkNetValue | 基准每日净值，仅当设置 *benchmark* 时返回 |
  | strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |
* 期货/期权：

  | **字段名称** | **字段说明** |
  | --- | --- |
  | tradeDate | 日期 |
  | margin | 保证金占用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现累计盈亏 |
  | totalPnl | 累计盈亏 |
  | totalMarketValue | 总市值（仅期权） |
  | cash | 可用资金 |
  | totalEquity | 账户总权益 |
  | marginRatio | 保证金占用比例 |
  | pnl | 账户当日盈亏 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | benchmarkClosePrice | 基准每日收盘价，仅当设置 *benchmark* 时返回 |
  | benchmarkNetValue | 基准每日净值，仅当设置 *benchmark* 时返回 |
* 债券

  | **字段名称** | **字段说明** |
  | --- | --- |
  | cash | 可用资金 |
  | totalMarketValue | 账户总市值 |
  | totalEquity | 账户总权益 |
  | netValue | 账户单位净值 |
  | totalReturn | 截至当日的累计收益率 |
  | ratio | 账户每日收益率 |
  | pnl | 账户当日盈亏 |
  | totalFee | 总费用 |
  | floatingPnl | 浮动盈亏 |
  | realizedPnl | 已实现盈亏 |
  | totalPnl | 总盈亏 |

## getTradeDetails

**语法**

```
Backtest::getTradeDetails(engine)
```

**参数**

**engine** 回测引擎句柄。

**详情**

获取订单交易明细，表结构如下：

| 字段 | 含义 |
| --- | --- |
| orderId | 订单号 |
| symbol | 证券代码 |
| direction | 订单委托买卖标志 1：买开；2：卖开；3：卖平；4：买平 |
| sendTime | 订单委托时间 |
| orderPrice | 订单委托价格 |
| orderQty | 订单委托数量 |
| tradeTime | 订单成交时间 |
| tradePrice | 成交价格 |
| tradeQty | 成交数量 |
| orderStatus | 表示订单状态： 4：已报  2：撤单成功  1：已成  0：部成  -1：审批拒绝  -2：撤单拒绝  -3：未成交的订单 |
| label | 标签 |
| outputOrderInfo | 风控日志，仅当引擎配置参数 *outputOrderInfo*=true 时包含此列 |
| seqNum | 序号列，仅当引擎配置参数 *outputSeqNum*=true 时包含此列 |
| strategyName | 策略名称，即该回测引擎的名字。 仅股票、两融的模拟交易模式包含该字段。 |

## restoreFromSnapshot

**语法**

```
Backtest::restoreFromSnapshot(snapshotDir, engineName, [output], [resource], [functions])
```

**详情**

根据快照文件恢复回测引擎，返回一个回测引擎句柄。仅支持 admin 用户和创建者调用。

**注意：**若回测引擎订阅了行情指标，那么恢复后引擎状态将为 FATAL。

**参数**

**snapshotDir** STRING 类型标量，表示快照文件的存储目录。

**engineName** STRING 类型标量，表示快照回测引擎的名字，必须与创建快照的引擎名字一致。

**output** 可选参数，一个字典，为该引擎设置实时输出表，相当于调用 `setTradingOutput`。

**resource** 可选参数，一个 STRING->ANY 字典，将作为恢复后引擎的 context 上下文字典的键 resource 对应的值。

**functions** 可选参数，一个 STRING->ANY 字典，将作为恢复后引擎的 context 上下文字典的键 functions 对应的值。

## setPosition

**语法**

```
Backtest::set​​Position(engine, symbol, qty, orderPrice, [lastPrice], [assetType])
```

**详情**

设置初始仓位，必须在 `appendQuotationMsg` 插入行情之前调用。通常在回调函数
`initialize` 中调用。暂不支持数字货币。

与配置项 *setLastDayPosition* 不同，*setLastDayPosition* 设置的底仓不占用初始资金，而
`setPosition` 设置的初始仓位，其成本会占用初始资金。

**参数**

**engine** 回测引擎句柄。

**symbol** STRING 类型标量，表示标的代码。

**qty** LONG 类型标量，表示持仓量：

* qty>0：代表买开持仓；
* qty<0：代表卖开持仓，股票、债券不支持卖开。

**orderPrice** DOUBLE 类型标量，表示持仓成本价。

**lastPrice** 可选参数，DOUBLE 类型标量，该标的的最新价，即前收盘价。省略该参数或设置为 0 时，默认值为
*orderPrice*。

**assetType** STRING 类型标量，表示资产类型，仅需在多资产回测时指定，可选值为 stocks，futures, options。

## setSecurityReference

**语法**

```
Backtest::setSecurityReference(engine, securityReferenceData)
```

**参数**

**engine** 回测引擎句柄。

**securityReferenceData** 该品种对应的基础信息表。

**详情**

设置基本信息表。

## setStockDividend

**语法**

```
Backtest::setStockDividend(engine, stockDividend)
```

**详情**

设置分红除权信息表，作用等价于 *stockDividend* 配置项。仅支持股票、融资融券品种。

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**stockDividend** 分红除权基本信息表，TABLE 类型，字段同配置项 *stockDividend*。

## setTradingOutput

**语法**

```
Backtest::setTradingOutput(engine, ouput)
```

**详情**

为回测引擎设置实时输出表，信息将实时写入对应的表。

**参数**

**engine** 回测引擎句柄。

**output** 一个字典，每个键值对代表一个输出表，key 的可选值包括：

* snapshot，对应的 value 为订阅的快照指标输出表，其表结构可通过 `getIndicatorSchema`
  获取。
* tick，对应的 value 为订阅的逐笔指标输出表，其表结构可通过 `getIndicatorSchema`
  获取。
* ohlc（或 kline），对应的 value 为订阅的 K 线指标输出表，其表结构可通过
  `getIndicatorSchema` 获取。
* transaction（或 trade），对应的 value 为订阅的逐笔成交指标输出表，其表结构可通过
  `getIndicatorSchema` 获取。
* snapshot\_kline（或 snapshot\_ohlc），对应的 value 为订阅的快照合成的 K 线的指标输出表，其表结构可通过
  `getIndicatorSchema` 获取。
* position，对应的 value 为实时更新持仓信息的表，可以通过 `getPosition`
  获取相应引擎指标表结构。
* totalPortfolios，对应的 value 为实时获取账户权益的表，可以通过
  `getTotalPortfolios` 获取相应引擎指标表结构。
* tradeDetails，对应的 value 为实时更新成交明细的表，可以通过 `getTradeDetails`
  获取相应引擎指标表结构。
* dailyPosition，对应的 value 为获取每日持仓的表，可以通过 `getDailyPosition`
  获取相应引擎指标表结构。
* dailyTotalPortfolios，对应的 value 为更新账户每日权益的表，可以通过
  `getDailyTotalPortfolios` 获取相应引擎指标表结构。
* returnSummary，对应的 value 为更新账户实时收益概述表，可以通过 getReturnSummary
  获取相应引擎指标表结构。支持股票和两融回测。

## setTradingVolumeDist

**语法**

```
setTradingVolumeDist(engine, volume)
```

**详情**

设置 VWAP 成交量分布表，用于 VWAP 算法单计算每个间隔的理论委托数量。

**参数**

**engine** 回测引擎句柄。

**volume** 一个表对象，表示成交量分布。包含以下字段：

| **字段名** | **数据类型** | **备注** |
| --- | --- | --- |
| symbol | STRING/SYMBOL | 标的代码 |
| time | SECOND | 时间 |
| value | INT/DOUBLE | 成交量或权重 |

## setUniverse

**语法**

```
Backtest::setUniverse(engine, symbolList)
```

**详情**

为引擎设置标的池。

**参数**

**engine** 回测引擎句柄。

**symbolList** STRING 类型向量，表示标的。

## stopBacktestEngine

**语法**

```
Backtest::stopBacktestEngine(engine)
```

**详情**

* 若引擎当前处于回测执行过程中（即正在调用
  `appendQuotationMsg`），将立即终止该引擎。被终止的引擎无法再次运行。
* 若引擎处于非运行状态，则不执行任何操作，后续仍可通过调用 `appendQuotationMsg` 启动回测。

返回该引擎的状态表，包含以下字段：

* name：回测引擎名称
* user：回测引擎的创建者
* status：回测引擎的状态，可能的值包括 OK（可用），END（正常结束），FATAL（不可用）。对于状态为 FATAL 的引擎：
  + 如果是插入数据的格式错误导致的 FATAL，则后续插入正确格式数据，即可恢复正常；
  + 如果是回调函数抛出异常导致的 FATAL，则使用 `updateEventCallbacks`
    修复回调函数，即可继续正常使用。
* lastErrMsg：最后一条错误信息
* numIndicators：订阅的指标数量
* snapshotTimestamp：回测引擎当前处理过的最新数据的时间戳
* isBacktestMode：当前是回测还是模拟交易模式

**参数**

**engine** 回测引擎句柄。

## submitOrder

**语法**

```
Backtest::submitOrder(engine, msg, [label=""], [orderType=0], [accountType="stock"], [algoOrderParam])
```

**详情**

可在回调函数中调用此函数提交订单，返回订单号。

**参数**

**engine** 回测引擎句柄，在回调函数中可通过 `contextDict["engine"]` 获取。

**msg** 一个元组或表，表示订单信息。

* *orderType*=0 时，格式如下：

  | **品种** | **格式** | **说明** |
  | --- | --- | --- |
  | 股票（包括股票、可转债、基金） | (股票代码, 下单时间, 订单类型, 订单价格, 订单数量, 买卖方向) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平 **订单类型：**  上交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中最优五档即时成交剩余转限价委托订单  2：市价单中本方最优价格委托订单  3：市价单中对手方最优价格委托订单  5：限价单  深交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中即时成交剩余撤销委托订单  2：市价单中本方最优价格委托订单  3: 市价单中对手方最优价格委托订单  4：市价单中全额成交或撤销委托订单  5：限价单 |
  | 期货/期权 | (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价/止盈价，委托订单数量，买卖方向，委托订单有效性) | **买卖方向：**  1：买开  2：卖开  3：卖平  4：买平  5：期权行权（仅支持多资产回测模式的期权品种，且基本信息表的 underlyingCode 项必须配置）  6：卖平今仓（仅支持期货、期权品种，且基本信息表的 intradayClosingFee 项必须配置）  7：买平今仓（仅支持期货、期权品种，且基本信息表的 intradayClosingFee 项必须配置）  **订单类型：**  0：市价单，以涨跌停价委托，并遵循时间优先原则  1：市价止损单  2：市价止盈单  3：限价止损单  4：限价止盈单  5：限价单（默认值）  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK）  止损价/止盈价暂不支持，默认 0. |
  | 融资融券 | (股票代码、下单时间、订单类型、订单价格、订单数量、买卖标志) | **订单类型：**  0：市价单  5：限价单  **买卖标志：**  1：担保品买入  2：担保品卖出  3：融资买入  4：融券卖出  5：直接还款  6：卖券还款  7：直接还券  8：买券还券 |
  | 债券 | （标的代码，下单时间，订单类型，清算速度，买价，买量，卖价，卖量，买卖方向，用户指定的订单号，渠道，价格类型） | 买卖方向： 1：买开  2：卖平  3：双边报价  4：借券买入（基础信息表中必须设置 bondLendingRate）  5：借券平仓（基础信息表中必须设置 bondLendingRate）  订单类型：  1：限价单  3：市价单转撤单  4：市价单转限单  5：弹性  7: FAK：按用户指定的价格立即撮合，不能成交的部分马上撤单  8：FOK：按用户指定的价格立即完全成交撮合，不能完全成交就撤单  价格类型：  1 或省略：净价  2：全价  3：收益率 |
  | 数字货币/多资产 | (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价，止盈价，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平  **订单类型：**  5：限价单（默认值）  0：市价单，以涨跌停价委托，并遵循时间优先原则  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK） |
* orderType = 5 或 6 时，格式为 `(期货代码, 交易所代码, 时间, 订单类型, 委托订单价格,
  止损价，止盈价，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间)`。
* orderType=8 时，格式为如下：

  |  |  |  |
  | --- | --- | --- |
  | 期货/期权 | (期货/合约代码, 交易所代码, 时间, 订单类型,买开平标志, 买单价格，买单数量，卖开平标志，卖单价格，卖单数量，bidDifftolerance, askDifftolerance, quantityAllowed) 其中：bidDifftolerance,askDifftolerance,quantityAllowed 为保留字段 | **买卖方向：**1：买开；2卖开；3：卖平；4：买平；5：期权行权（仅支持多资产回测模式的期权品种，且基本信息表的 underlyingCode 项必须配置） **订单类型：**  0：市价单，以涨跌停价委托，并遵循时间优先原则  1：市价止损单  2：市价止盈单  3：限价止损单  4：限价止盈单  5：限价单（默认值）  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK）  止损价/止盈价暂不支持，默认 0. |
* orderType=9 时，格式为如下：

  | **品种** | **格式** | **说明** |
  | --- | --- | --- |
  | 期货/期权 | (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价/止盈价，委托订单数量，买卖方向，委托订单有效性) | + 买卖方向为 1 时   - 若委托数量大于当前买开持仓量（longPosition），则提交一笔买开订单；   - 若委托数量小于等于 longPosition，则提交一笔卖平（买卖方向为     3）订单。 + 买卖方向为 2 时：   - 若委托数量大于当前卖开持仓量（shortPosition），则提交一笔卖开订单；   - 若委托数量小于等于 shortPosition，则提交一笔买平（买卖方向为     4）订单。 **订单类型：**  0：市价单，以涨跌停价委托，并遵循时间优先原则  1：市价止损单  2：市价止盈单  3：限价止损单  4：限价止盈单  5：限价单（默认值）  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交否则自动撤销（FOK）  2：立即成交剩余自动撤销（FAK）  止损价/止盈价暂不支持，默认 0. |
* *orderType*=10 时，格式如下：

  | **品种** | **格式** | **说明** |
  | --- | --- | --- |
  | 股票、融资融券 | (股票代码, 下单时间, 订单类型, 订单价格, 订单数量, 买卖方向) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平  **订单类型：**  上交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中最优五档即时成交剩余转限价委托订单  2：市价单中本方最优价格委托订单  3：市价单中对手方最优价格委托订单  5：限价单  深交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中即时成交剩余撤销委托订单  2：市价单中本方最优价格委托订单  3: 市价单中对手方最优价格委托订单  4：市价单中全额成交或撤销委托订单  5：限价单 |
* *orderType*=11 时，格式如下：

  | **品种** | **格式** | **说明** |
  | --- | --- | --- |
  | 股票、融资融券 | (股票代码, 下单时间, 订单类型, 订单价格, 订单数量, 买卖方向) | **买卖方向：**1：买开；2卖开；3：卖平；4：买平  **订单类型：**  上交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中最优五档即时成交剩余转限价委托订单  2：市价单中本方最优价格委托订单  3：市价单中对手方最优价格委托订单  5：限价单  深交所：  0：市价单中最优五档即时成交剩余撤销委托订单  1：市价单中即时成交剩余撤销委托订单  2：市价单中本方最优价格委托订单  3: 市价单中对手方最优价格委托订单  4：市价单中全额成交或撤销委托订单  5：限价单 |
* *orderType*=12 时，格式如下：

  | **品种** | **格式** | **说明** |
  | --- | --- | --- |
  | 股票 | (股票代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价，止盈价，最高价/最低价回落百分比，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间) | **买卖方向：**1：买开；2卖开  **委托订单有效性：**  0：当日有效（默认值）  1：立即全部成交，否则自动撤销（FOK）  2：立即成交，剩余自动撤销（FAK） |

**label** STRING 类型标量，对该订单设置标签，对该订单分类。

**orderType** INT 类型标量，可选值如下：

* 0 ：默认值，表示一般订单
* 5：限价止盈止损订单
* 6：市价止盈止损订单
* 8：双边报价订单（仅期货、期权支持）
* 9：自动下单，此时买卖方向只支持设置为 1 或 2
* 10：TWAP(Time-Weighted Average Price) 算法单，将大额订单按照时间间隔均匀拆分成多个小订单执行
* 11：VWAP(Volume-Weighted Average Price) 算法单，将大额订单按照成交量分布比例拆分成多个小订单执行
* 12：移动止盈止损订单

其中 5、6 和 8 为算法订单，5 和 6 仅支持股票、期货、期权，8 仅支持期货和期权，可通过配置项 enableAlgoOrder 开启。10 和 11
仅支持股票和两融的快照模式。

**accountType** 可选参数，多资产回测和数字货币回测专用。

**algoOrderParam** 可选参数，TWAP 和 VWAP 算法单专用，一个字典，包含以下字段：

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| startTime | SECOND | 可选字段，拆单开始时间，不设置时默认为引擎的最新行情时间；设置时开始时间为 `startTime = max(startTime, second(引擎的最新行情时间))` |
| endTime | SECOND | 必填字段，结束时间，用于计算拆单次数。  `拆单次数 = floor((endTime - startTime) / interval) + 1` |
| interval | INT | 可选字段，切分时间间隔，单位为秒，默认为 20 秒。 |
| maxSingleOrderVolume | LONG | 可选字段，每笔订单最大下单手数。 |
| orderPriceType | INT | 可选字段，算法订单的委托价格类型：   * 0（默认）：最新价； * 1：本方第一档价格； * 2：对手方第一档价格。 |

## subscribeIndicator

**语法**

```
Backtest::subscribeIndicator(engine, marketDataType, metrics)
```

**详情**

设置订阅的行情指标。

**参数**

**engine** 回测引擎句柄。

**marketDataType** STRING 类型标量，表示要订阅指标的行情类型，可选值为：

* "snapshot" 快照。
* "entrust" 逐笔委托。
* "kline"或"ohlc" K 线。
* "trade"或"transaction" 逐笔成交明细。
* "snapshot\_kline"或"snapshot\_ohlc" 快照合成的 K 线。

**metrics** 一个字典，key 是 STRING 类型，代表指标名；value 是以元代码的形式表示计算公式，代表如何计算指标。状态因子的编写请参考
DolphinDB
响应式状态引擎介绍教程。

**示例**

```
d=dict(STRING,ANY)
d["mavg"]=<mavg(lastPrice,20)>
Backtest::subscribeIndicator(contextDict["engine"], "snapshot", d)
Backtest::subscribeIndicator(contextDict["engine"], "tick", d)
d=dict(STRING,ANY)
d["mavg"]=<mavg(trade,20)>
Backtest::subscribeIndicator(contextDict["engine"], "trade", d)
d=dict(STRING,ANY)
d["mavg"]=<mavg(close,20)>
Backtest::subscribeIndicator(contextDict["engine"], "kline", d)
```

## subscribeQuote

**语法**

```
subscribeQuote(engine, symbolList, [symbolSource=""], [quoteType='snapshot'])
```

**详情**

订阅行情。订阅后，仅指定的行情会触发回调。

目前支持期货、债券、多资产品种的快照模式。

**参数**

**engine** 回测引擎句柄。

**symbolList** STRING 类型向量，表示要订阅的标的。

**symbolSource** 可选参数，STRING 类型标量，表示要订阅的交易所（ symbolSource
字段的值）。默认为空，表示不指定，此时会订阅上交所和深交所的数据。

**quoteType** 可选参数，STRING 类型标量，表示要订阅行情的类型。可选值为：

* “snapshot”：默认值，快照行情。
* “ohlc”：分钟频或日频。

## triggerDailySettlement

**语法**

```
Backtest::triggerDailySettlement(engine)
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**详情**

该接口仅支持仿真模式（isBacktestMode=false）调用，开启手动每日收盘结算，包括计算每日持仓，计算每日权益，重置模拟撮合引擎，触发
afterTrading 回调等相关处理逻辑。

* 在首次调用该接口之前，系统通过跨日结算机制完成结算，即根据接收到的行情时间戳日期发生变化来触发结算。
* 首次调用该接口之后，将关闭跨日自动结算机制，改为仅通过该接口触发结算。

## unsubscribeQuote

**语法**

```
unsubscribeQuote(engine, symbolList, [symbolSource=""], [quoteType='snapshot'])
```

**详情**

取消回测引擎订阅的行情。

**参数**

**engine** 回测引擎句柄。

**symbolList** STRING 类型向量，表示要订阅的标的。

**symbolSource** 可选参数，STRING 类型标量，表示要取消订阅的交易所（ symbolSource
字段的值）。默认为空，表示不指定，此时取消订阅所有交易所。

**quoteType** 可选参数，STRING 类型标量，表示要订阅行情的类型。可选值为：

* “snapshot”：默认值，快照行情。
* “ohlc”：分钟频或日频。

## updateEventCallbacks

**语法**

```
Backtest::updateEventCallbacks(engine, callbacks)
```

**详情**

更新回调函数。该函数仅支持股票和两融品种的仿真模式（isBacktestMode=false）。

**参数**

**engine** 回测引擎句柄。

**callbacks** 为 STRING->ANY 类型的字典，键是要修改的回调函数，支持 “initialize”, “beforeTrading”,
“onTick”, “onBar”, “onSnapshot”, “onOrder”, “onTrade”, “afterTrading” 和
“finalize”，值是修改后的函数。

## updatePosition

**语法**

```
Backtest::updatePosition (engine, symbol, qty, [price])
```

**参数**

**engine** 回测引擎句柄，在回调函数中可通过逻辑上下文 `context["engine"]` 获取。

**symbol** STRING 类型标量，表示标的。

**qty** INT 类型标量，正数代表增加持仓，负数代表减少持仓。

**price** DOUBLE 类型标量，表示成交价格。当参数为 0 或为空时，取行情的最新价。

**详情**

更新持仓，返回订单号。该接口仅支持在模拟交易模式下调用。

## 多资产接口

多资产回测支持在一个引擎中，同时管理股票、期货、期权的多个账户。

多资产回测接口与一致。用户仍可通过这些接口创建引擎、执行回测、获取回测结果。这里仅介绍有所变动的接口。

部分接口增加了参数：

**contractType** STRING 类型标量，表示订阅的行情品种类型。可选值为 "stock", "futures", "option",
"bonds"，分别代表股票、期货、期权、债券。

**assetType** STRING 类型标量，表示账户类型。可选值为 "stock", "futures", "option",
"bonds"，分别代表股票、期货、期权、债券账户。接口
getDailyPosition，getDailyTotalPortfolios，getReturnSummary，getTradeDetails
中该参数默认为空，此时返回所有账户的对应信息（getDailyPosition 返回除债券外的所有账户信息），其他接口默认值为 "stock"。

| 接口 | 语法详情 |
| --- | --- |
| subscribeIndicator | 订阅指标：  ``` Backtest::subscribeIndicator(engine, marketDataType, metrics, [contractType="stock"]) ``` |
| submitOrder | 下单接口：  ``` Backtest::submitOrder(engine, msg, [label=""], [orderType=0], [assetType="stock"]) ```   *msg* 的格式为 (标的代码, 交易所代码, 时间, 订单类型, 委托订单价格, 止损价，止盈价，委托订单数量，买卖方向，滑点，委托订单有效性，委托订单到期时间)  注：债券账户下单的 *msg* 和单品种债券格式一致。 |
| cancelOrder | 取消订单：  ``` cancelOrder(engine, [symbol=""], [orders], [label=""], [assetType=""]) ``` |
| getAvailableCash | 查询账户可用资金：  ``` Backtest::getAvailableCash(engine, [assetType="stock"]) ``` |
| getTodayPnl | 获取股票盈亏：  ``` getTodayPnl(engine, symbol, [assetType=""]) ``` |
| getPosition | 获取当前持仓：  ``` Backtest::getPosition(engine, [symbol], [assetType="stock"]) ``` |
| getDailyPosition | 获取每日持仓：  ``` Backtest::getDailyPosition(engine, [symbol], [assetType]) ``` |
| getDailyTotalPortfolios | 获取策略每日权益指标：  ``` Backtest::getDailyTotalPortfolios(engine, [assetType]) ```   * assetType 的可选值除 "stock", "futures", "option" 外，还允许指定   “strategy” 代表整个策略的权益表。 * assetType 省略时，会将所有资产类型（包括 strategy）的权益表拼接成一张表后返回。 |
| getTotalPortfolios | 获取权益指标表：  ``` Backtest::getTotalPortfolios(engine, assetType="") ```   assetType 的可选值除 "stock", "futures", "option" 外，还允许指定 “strategy” 代表整个策略的权益表。 |
| getReturnSummary | 获取策略的收益概述：  ``` Backtest::getReturnSummary(engine, [assetType]) ``` |
| getTradeDetails | 获取订单交易明细：  ``` Backtest::getTradeDetails(engine, [assetType]) ``` |
| getOpenOrders | 获取未成交订单：  ``` Backtest::getOpenOrders(engine, [symbol=""], [orders], [label=""], [outputQueuePosition=false], [assetType="stock"]) ``` |
| getIndicatorSchema | 获取策略指标表：  ``` backtest::getIndicatorSchema(engine,marketDataType,assetType="stock") ```   *marketDataType* 可为 “snapshot”，“ohlc”，“kline”，“trade” 或 “transaction” |
| setTradingOutput | 设置实时输出表：  ``` backtest::setTradingOutput(engine, ouput) ```   output 是一个嵌套字典，key 是账户类型，value 为字典。子字典 value 的键是输出表名， 对应的值为表对象。 |
| setSecurityReference | 设置基本信息表：  ``` setSecurityReference(engine, securityReference, [assetType=""]) ``` |
| getTodayTradingStatistics | 获取当日交易统计信息：  ``` Backtest::getTodayTradingStatistics(engine, [symbol], assetType) ```   assetType 为必填参数，当前仅支持“stock” ，“futures”，“option”，默认值为 “stock”。 |
| getDailyTradingStatistics | 获取每日交易统计信息：  ``` Backtest::getDailyTradingStatistics(engine, [symbol], [assetType]) ```   assetType 当前仅支持 “stock”，“futures”，“option”，默认返回所有品种的结果。 |

## 数字货币接口

数字货币引擎支持单个引擎中同时管理现货和期货的多个账户，其使用方式与单账户引擎有所不同。多资产设计遵循以下原则：

1. 数字货币行情中可以存在不同的合约类型，onBar 回调会一次性提供对应时间段内所有合约类型的数据，便于用户根据不同合约的行情设计策略。
2. 数字货币接口支持可选的 *accountType*
   参数，用于指定需要操作的账户。在省略该参数时，原则上策略中使用的接口(下单撤单、获取未成交订单、获取持仓等)默认为现货账户，回测结束后调用的接口(成交明细、每日持仓等)默认返回所有账户的结果。

在数字货币回测中，多数引擎接口与其他资产一致。用户仍可通过这些接口创建引擎、执行回测、获取回测结果。需要注意，部分接口增加了相关参数：

**contractType** STRING 类型标量，表示订阅行情品种类型。可选值为 "spot", "futures",
"option"，分别代表现货、期货和永续合约、期权。

**accountType** STRING 类型标量，表示账户类型。可选值为 "spot", "futures",
"option"，分别代表现货账户、期货和永续合约账户、期权账户。

相关接口如下表所示：

| **接口** | **语法详情** |
| --- | --- |
| subscribeIndicator | 订阅指标：   ``` Backtest::subscribeIndicator(contextDict["engine"], "snapshot", d,contractType) ``` |
| submitOrder | 下单接口：   ``` Backtest::submitOrder(engine, msg,label="",orderType=0,accountType) ``` |
| cancelOrder | 取消订单：  ``` Backtest::cancelOrder(engine, symbol="", orders=NULL, label="", contractType) ``` |
| getAvailableCash | 查询账户可用资金：   ``` Backtest::getAvailableCash(long(engine),accountType) ``` |
| getTotalPortfolios | 获取策略当前权益指标：   ``` Backtest::getTotalPortfolios(engine, accountType) ``` |
| getPosition | 获取当前持仓：   ``` Backtest::getPosition(engine,symbol="",accountType) ``` |
| getDailyPosition | 获取每日持仓：   ``` Backtest::getDailyPosition(engine，accountType) ``` |
| getDailyTotalPortfolios | 获取策略每日权益指标：   ``` Backtest::getDailyTotalPortfolios(engine,accountType) ``` |
| getReturnSummary | 获取策略的收益概述：   ``` Backtest::getReturnSummary(engine,accountType) ``` |
| getTradeDetails | 获取订单交易明细：   ``` Backtest::getTradeDetails(engine,accountType) ``` |
| getOpenOrders | 获取未成交订单：   ``` Backtest::getOpenOrders(engine, symbol=NULL, orders=NULL, label="", accountType) ``` |
