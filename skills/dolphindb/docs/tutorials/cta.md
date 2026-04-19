<!-- Auto-mirrored from upstream `documentation-main/tutorials/cta.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 外汇中高频 CTA 风控策略回测案例

在汇率波动日益频繁、企业与机构对风险管理要求不断提高的背景下，外汇交易策略已成为资产配置与对冲操作的重要工具。其中，CTA
策略在外汇交易中具有非常重要的实际应用价值，在风险控制、趋势捕捉、资金效率与交易实用性之间取得了良好平衡。

在投入实盘交易之前，利用市场的历史数据对量化中高频策略进行测试和评估是确保交易策略有效性和可行性的重要步骤。DolphinDB
凭借其高性能计算引擎和强大的数据处理能力，成为交易策略回测的理想选择。本文将通过一个结合中高频 CTA 逻辑与实时风控的外汇远期交易策略案例，展示 DolphinDB
回测引擎的使用，以及其在实际应用中的应用优势。

## 1. 背景介绍

本文将详细展示如何结合多个技术分析指标，如 RSI （相对强弱指数），Bollinger Bands（布林带），构建一个涵盖买卖开仓逻辑的外汇 CTA
策略，并通过算法订单实现具备实时止盈止损功能的风险控制机制。

在介绍该策略的实现过程之前，为帮助读者更清晰地理解背景与应用场景，本章将简要介绍外汇交易的基本特点、CTA 策略的核心思路，以及 DolphinDB
提供的回测解决方案。

### 1.1 外汇交易背景介绍

中国的外汇市场以银行间外汇市场为核心，由中国外汇交易中心（CFETS）组织交易。交易品种主要包括即期外汇、远期外汇、外汇掉期、期权等。不同于国际市场，中国尚未开放外汇期货交易，远期合约成为企业管理汇率风险的主要工具之一。外汇远期合约（Forward
FX）是指买卖双方约定在未来某一时间以固定汇率交换一定数量货币的合约。它广泛用于锁定结汇成本、规避汇率波动。相比现货交易，远期合约具有非标准化、定制化、无交易所挂牌等特点。其价格通常基于即期汇率与利率平价理论计算而来，受利差、期限结构、市场预期等因素影响。尽管远期交易以对冲为主，但在利差套利、汇率择时、资金流动管理等领域也广泛应用于策略化操作。通过历史数据进行回测，可以系统评估策略的收益风险特征、参数稳定性以及对汇率变动的敏感性。

### 1.2 CTA 策略背景介绍

CTA 投资策略主要通过技术分析和系统化交易方法，对期货、外汇、利率等衍生品进行交易。随着全球金融市场的发展，CTA
策略已被广泛应用于外汇市场，成为机构和量化交易者应对汇率波动、实现趋势跟踪与风险控制的重要工具之一。CTA 策略通常分为主观 CTA 和量化 CTA
两大类型。前者依赖交易员对宏观经济、政策事件等基本面的判断进行主观决策；而后者则基于量化模型，按照预设规则自动生成买卖信号并执行交易。尤其在量化 CTA
策略中，交易决策往往依托一系列技术指标，RSI、Bollinger Bands、平均真实范围（ATR）等，来识别市场趋势和交易机会。同时， CTA
策略高度重视风险管理。通过设置止盈止损、限制头寸规模、控制最大浮亏等方式，量化 CTA
策略在追求趋势收益的同时，也注重保护资金安全，提高策略在不同市场环境下的稳健性。

### 1.3 DolphinDB 中高频回测解决方案概述

中高频量化交易策略回测平台的实现主要包括三个重要环节：行情数据按顺序回放，委托订单撮合，以及策略开发与策略回测绩效评估。而在实现中高频策略回测时往往面临以下几个挑战：

首先，海量中高频交易数据对回测引擎的查询与计算性能提出了极高的要求。

其次，为确保策略评估和优化的有效性，回测过程中应尽可能模拟实际的交易过程，例如考虑订单能否成交、成交价格、成交量以及市场冲击等因素。

此外，回测引擎还应具有灵活的架构，能够支持多种交易策略和技术指标的实现，并且易于扩展，以适应不同的市场和交易需求。

针对上述挑战，DolphinDB
基于其高性能的分布式存储和计算架构，为用户提供了一个易扩展、性能优的中高频量化交易策略回测解决方案。该方案实现了库内行情回放、模拟撮合引擎和事件型中高频回测引擎三大核心组件，支持通过
DLang、Python 或 C++语言完成中高频策略的研发和测试。具体来说，该方案涵盖以下三个模块：

* 回放功能：支持将一个或多个不同结构的分布式表中的数据严格按照时间或者按指定多列排序顺序**回放**到流表中，因此可以方便地解决因子计算和量化策略研发中研发和生产一体化的问题。
* 模拟撮合引擎插件：支持沪深交易所 Level-2 逐笔行情和快照行情，实现与交易所一致的 **“价格优先，时间优先”**的高精度的撮合、基于多种行情数据的撮合模式、丰富的可用于模拟实盘环境的撮合配置。
* 回测插件：用户可以在其中自定义指标，支持基于逐笔、快照、分钟和日频行情进行策略回测，获取回测的收益、持仓、交易明细等信息。其中基于逐笔和快照行情进行高精度策略回测，用户可以实现仿真和回测一体化的策略验证。

值得一提的是，这三个模块化解决方案与外部解决方案兼容性良好。即使用户已经实现了某个环节的解决方案，DolphinDB
提供的解决方案也可以与其融合成一个完整的回测方案。

## 2. 基于 DolphinDB 的外汇 CTA 策略：中低频交易与高频风控融合实践

在大部分的 CTA 策略中，高精度的订单模拟撮合和实时风险控制是确保策略成功和有效执行的关键因素。策略的主要逻辑可能是基于分钟等聚合的 K
线行情，订单的成交依赖高精度的订单撮合引擎或者策略止盈止损依赖实时的 tick 级高频行情。DolphinDB 可以实现回测引擎以实时的 tick
行情作为回测引擎行情输入，同时按配置的指定频率触发 onBar 行情回调方式回测。本案例基于 tick 级高频行情数据，通过配置项
callbackForSnapshot 实时合成 1 小时 K 线，以实现一个基于布林带突破与 RSI 指标的外汇 CTA 趋势策略。具体的策略逻辑如下：

* 做多开仓：当前 RSI 大于 70 且布林带正在上移并打破上轨
* 做空开仓：当前 RSI 小于 30 且布林带正在下移并打破下轨
* 如果存在多头或空头委托订单，在算法订单中根据 tick 行情判断是否撤单、止盈止损

### 2.1 编写自定义策略

**首先，基于 tick 行情数据定义重要的技术分析指标：RSI 和**
**Bollinger Bands。**RSI 用来评估市场的超买或超卖状态，Bollinger Bands
则用来判断价格波动是否突破区间。为了满足使用中高频行情数据计算类似量价因子的需求，DolphinDB
回测引擎采用了响应式状态引擎。这一引擎能够实现流批统一计算，并有效处理带有状态的高频因子，具体也可以参考响应式状态引擎用户手册定义相应的指标。以下是定义技术指标 RSI 和 Bollinger Bands 的代码示例：

```
@state
defg RSI(close, timePeriod=14) {
     deltaClose = deltas(close)
     up = iif(nullCompare(>, deltaClose, 0), deltaClose, 0)
     down = iif(nullCompare(>, deltaClose, 0), 0, -deltaClose)
     upAvg = wilder(up, timePeriod)
     downAvg = wilder(down, timePeriod)
     return 100.0 * upAvg / (upAvg + downAvg)
}
@state
def stddev(close, timePeriod=5, nbdev=1){
    return sqrt(var(close, timePeriod, nbdev)) * nbdev
}
@state
def bBands_(close, timePeriod=5, nbdevUp=2, nbdevDn=2, maType=0){
    mid =sma(close, timePeriod)
    md = stddev(close, timePeriod, 1)
    return ((mid + nbdevUp * md), mid, (mid - nbdevDn * md))
}
```

中高频回测中，策略通常是事件驱动的，而一个策略逻辑通常需要涉及多种事件，比如新的行情到来、新的订单成交等等。DolphinDB
回测引擎采用事件驱动机制，提供了全面的事件函数如策略初始化函数、盘前回调函数、行情回调函数、每日盘后回调函数等，用户可以在相应的回调函数中编写策略逻辑实现相应的策略。此外，自定义回调函数支持
JIT 技术，可以有效提升策略执行效率。后续本案例将会展示不同的事件函数是如何实现的。

**在策略初始化函数中，首先订阅指标 RSI 、Bollinger Bands**。subscribeIndicator
接口获取回测引擎名、需要计算的数据类型、需要计算的指标字典（key 为指标名，用于之后访问；value 为指标计算的元代码），之后计算结果将传入
`onBar` 策略回调函数。

```
def initialize(mutable context){
    print("initialize")
    d=dict(STRING,ANY)
    d["rsi"]=<ta::rsi(lastPrice, 11)>
    d["bhigh"]=<ta::bBands(lastPrice, 20, 2, 2, 0)[0]>
    d["bmid"]=<ta::bBands(lastPrice, 20, 2, 2, 0)[1]>
    d["blow"]=<ta::bBands(lastPrice, 20, 2, 2, 0)[2]>
    Backtest::subscribeIndicator(context["engine"], "snapshot_kline", d)

}
```

**在 K 线回调函数**
`onBar`
**中，系统通过获取订阅的 RSI 和 布林带 指标生成开仓信号。并通过算法订单来实现止盈止损。**`onBar` 函数的
*msg* 参数，为回测引擎传来的合成的 K 线行情，以及在 `initialize`
中定义的指标计算结果。*msg* 是一个字典，字典的 key 为期货标的名，而 value
为这支期货标的对应的行情信息以及指标计算结果。以下代码展示了买入开仓与卖出开仓的判断逻辑：

```
def onBar(mutable context, msg,indicator){
	istock=msg.keys()[0]
	msg_=msg[istock]
	askPrice0=msg_.offerPrice[0]
	bidPrice0=msg_.bidPrice[0]
	spread=askPrice0-bidPrice0
	indicator_=indicator[istock]
	blow=indicator_.blow
	bhigh=indicator_.bhigh

	if(spread>context["maxSpread"]){
		return
	}
	rsi_=indicator_.rsi
	if(isNull(rsi_)){return}
	close=msg_.lastPrice
	bmid=indicator_.bmid
	open=msg_.open
	istock=msg_.symbol
	position=Backtest::getPosition(context["engine"],istock)
	longpos = position.longPosition
	shortpos = position.shortPosition
	if(rsi_>70. and askPrice0>bhigh and close>open and longpos <1){
	            Backtest::submitOrder(context["engine"], (istock,msg_.symbolSource ,
	            context["barTime"],5, round(askPrice0,5),
	            askPrice0 -context["sl"]+context['Slippage'] , askPrice0+ context["tp"]+context['Slippage'],
	            2, 1,context['Slippage'], 0, context["barTime"]+36000000),"openBuy", 5)
	        	return

    	}
	if(rsi_<30. and bidPrice0<blow and close<open and shortpos <1){
		    Backtest::submitOrder(context["engine"], (istock,msg_.symbolSource,
		    context["barTime"],5, round(bidPrice0,5),
		    bidPrice0+context["sl"]-context['Slippage'],
		    bidPrice0 - context["tp"]-context['Slippage'], 2, 2, context['Slippage'] , 0,
		    context["barTime"]+36000000),"openSell", 5)
			return

	}
}
```

这里的 `Backtest::submitOrder` 是回测引擎提供的下单接口，回测引擎内置了实时止盈止损的算法订单，配置项
enableAlgoOrder 设置为 true 时，可以开启算法订单：

```
Backtest::submitOrder(engine, orderMsg, label="", orderType = 5)
```

orderMsg
为元组类型，包含的成员变量分别是标的代码、交易所代码、时间、订单类型、委托订单价格、止损价、止盈价、委托订单数量、买卖方向、滑点、委托订单有效性，以及委托订单到期时间。算法订单的类型
orderType
的取值包括限价止盈订单（1），市价止盈订单（2），限价止损订单（3），市价止损订单（4），限价止盈止损订单（5），和市价止盈止损订单（6）。

### 2.2 根据策略设置相应的配置参数

回测的开始与结束日期、初始资金、手续费和印花税、行情类型、订单延时等均可以通过参数进行配置。这些参数允许用户灵活地调整回测条件，以模拟不同的市场环境和交易策略的效果。此外策略逻辑上下文
context 也可以通过参数设置策略中的全局变量，此案例中我们在 context
中设置了策略中需要的滑点、点差以及止盈止损价。具体的初始参数配置代码示例如下：

```
startDate=2018.12.31
endDate=2019.12.31
userConfig=dict(STRING,ANY)
userConfig["startDate"]=startDate
userConfig["endDate"]=endDate
userConfig["strategyGroup"]="universal"
userConfig["frequency"]= 3600000
userConfig["cash"]= 10000000
userConfig["dataType"]=1
userConfig["depth"] = 1;
userConfig["enableAlgoOrder"]= true
userConfig["latency"]= 1
userConfig["callbackForSnapshot"]=2
userConfig["matchingMode"]=3
Context=dict(STRING,ANY)
Context["opens"]=false
Context["Slippage"]=0.00002
Context["tp"]=0.01
Context["sl"]=0.001
Context["orderId"]=0
Context["maxSpread"]=2.
userConfig["context"]=Context
```

我们通过配置项 callbackForSnapshot 和 frequency，按指定频率触发 `onBar`
行情回调，从而驱动回测策略执行。以下是对这两个配置项的具体说明：

| 配置项 | 配置项说明 |
| --- | --- |
| callbackForSnapshot = 0 | 表示 tick 行情：tick 行情触发 onSnapshot 行情回调 |
| callbackForSnapshot = 1，frequency > 0 | 表示 tick 行情：tick 行情触发 onSnapshot 行情回调；tick 行情按指定 frequency 频率合成的 K 线行情触发 onBar 行情回调 |
| callbackForSnapshot = 2，frequency > 0 | 表示 tick 行情：tick 行情按指定 frequency 频率合成的 K 线行情触发 onBar 行情回调 |

### 2.3 创建回测引擎

设置引擎名称、引擎配置项、相应的回调函数、合约基本信息表等相应参数之后，通过接口 `createBacktester`
创建模拟撮合引擎实例。其中，接口 `createBacktester` 的第四个参数为表示是否开启 JIT 优化。默认值为
false，表示不开启，若需要开启 JIT 优化，只需要设置此参数为 true 即可。

```
callbacks=dict(STRING,ANY)
callbacks["initialize"]=initialize
callbacks["beforeTrading"]=beforeTrading
callbacks["onBar"]=onBar
callbacks["onOrder"]=onOrder
callbacks["onTrade"]=onTrade
callbacks["afterTrading"]=afterTrading
callbacks["finalize"]=finalize
strategyName="ftxdemoStrategydemo333"
try{Backtest::dropBacktestEngine(strategyName)}catch(ex){print ex}
engine = Backtest::createBacktester(strategyName, userConfig, callbacks,false,basicInfo)
```

### 2.4 执行回测引擎

通过 `Backtest::createBacktester`
创建回测引擎之后，可以通过以下方式执行回测。backtestdata\_ 为相应的分钟频率行情数据，行情数据字段和类型说明参考 回测插件的接口文档。

```
Backtest::appendQuotationMsg(engine, backtestdata_ )
```

### 2.5 获取回测结果

回测运行结束之后，可以通过相应的接口获取每日持仓、每日权益、收益概述、成交明细和策略中用户自定义的逻辑上下文。回测插件提供的完整回测结果接口可以参阅 回测插件的接口文档。下图为本例获得的交易明细结果：

![](images/cta.png)

## 3. 性能测试

为了更直观地展示 DolphinDB 高频回测引擎在实际场景下的执行性能，我们选取了一只外汇远期合约的一年历史数据作为测试样本。在单线程、非 JIT
模式下运行该策略示例，共处理了 29,317,091 条行情数据，生成 168 笔订单，整体回测耗时约为 8.2 秒。

## 4. 总结

在量化回测中，全面采用 tick
数据会带来较高的计算成本，而纯粹依赖中低频策略又容易忽略实盘中的滑点影响与风控响应延迟问题。为兼顾回测性能与交易精度，本文展示了一种将中低频决策逻辑与高频风控机制相结合的策略架构：策略核心逻辑基于分钟或小时级别的
K 线进行信号判断与下单操作，关键的止盈止损则通过 tick 行情回调实时监控并触发，从而更真实地还原实盘交易过程中的风控行为。展现了 DolphinDB
回测引擎优异的性能、丰富的策略触发机制以及全面的回测结果信息。

## 5. 附录

外汇 CTA 策略 demo 以及所需要的数据

* [FXDemo.dos](https://cdn.dolphindb.cn/zh/tutorials/script/cta/FXDemo.dos)
* [backtestdata\_.zip](https://cdn.dolphindb.cn/zh/tutorials/script/cta/backtestdata_.zip)
