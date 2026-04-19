<!-- Auto-mirrored from upstream `documentation-main/tutorials/daily_stock_portfolio_backtest.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 股票组合管理日频回测案例

在量化投资中，组合回测是评估投资策略稳定性与收益风险特征的核心环节。无论是指数增强策略、基金定投组合，还是机构资产管理中的模型组合，策略绩效都取决于在不同市场阶段下的投资组合权重调整与执行效率。投资组合权重通常由外部策略模块或研究团队生成，可能基于机器学习模型、风险预算框架、行业配置方案或因子评分体系。权重数据一般按日或按既定周期输出并存档，用于驱动组合构建和再平衡过程。如何高效地将这些比重文件与行情数据结合，构建一个按固定周期自动调仓的回测系统，是组合策略研究的重要基础。

本文将通过 DolphinDB
回测插件，展示一个基于给定权重文件的按日调仓进行组合投资的回测案例。该案例通过解析每日目标权重文件，模拟实际投资组合在不同时间点的持仓调整过程，帮助研究者系统地评估组合策略的历史表现与稳定性。

## 1. 背景介绍

本文将展示如何基于外部持仓权重文件，构建一个股票组合按日自动再平衡的被动投资策略。该策略以预先定义的资产权重为核心输入，在回测过程中根据每日（或指定周期）的目标权重文件动态调整组合持仓，从而模拟真实投资组合在不同市场环境下的再平衡过程。

本章将简要介绍股票投资组合管理的基本思路、基于权重文件的被动型再平衡机制，以及 DolphinDB 提供的高性能回测框架在组合策略研究中的应用。

### 1.1 股票组合管理策略背景介绍

该策略旨在模拟实际投资组合在特定周期（如每日、每周、每月或每季度）进行权重调整的过程，用以评估不同权重配置方案在历史市场环境下的收益与风险表现。策略核心思想是：在每个再平衡周期起始日，按照预先设定或外部生成的目标权重文件，对各股票的持仓比例进行调整，使投资组合持仓与目标权重对齐，从而实现系统化的资产配置与风险控制。

在股票投资组合管理和指数增强策略中，基于固定频率的组合再平衡是一种常见且关键的投资管理手段。相较于基于实时信号的主动交易策略，这类被动型组合再平衡策略不依赖即时市场预测，而侧重于验证权重配置本身的长期稳定性与分散化效果。研究者可以借此独立评估不同因子打分、行业轮动、或优化算法生成的权重方案在历史区间内的表现差异，从而为资产配置模型或量化选股模型提供经验验证。

为实现上述目标，本文采用 DolphinDB
的高性能回测引擎构建组合回测系统。系统能够高效加载多标的历史行情数据，解析外部权重文件，并在指定频率上自动执行再平衡操作。通过引擎的事件驱动框架，策略可在每日或指定周期内对比当前持仓与目标权重差异，自动生成买卖指令并记录交易执行过程。结合回测结果，用户可进一步分析组合的净值变化、波动率、最大回撤、夏普比率等绩效指标，为不同再平衡策略的有效性与稳定性提供定量评估依据。

### 1.2 DolphinDB 中高频回测解决方案概述

中高频量化交易策略回测平台的实现主要包括三个重要环节：行情数据按顺序回放，委托订单撮合，以及策略开发与策略回测绩效评估。而在实现时往往面临以下几个挑战：

首先，海量中高频交易数据对回测引擎的查询与计算性能提出了极高的要求。

其次，为确保策略评估和优化的有效性，回测过程中应尽可能模拟实际的交易过程，例如考虑订单能否成交、成交价格、成交量以及市场冲击等因素。

最后，回测引擎还应具有灵活的架构，能够支持多种交易策略和技术指标的实现，并且易于扩展，以适应不同的市场和交易需求。

针对上述挑战，DolphinDB
基于其高性能的分布式存储和计算架构，为用户提供了一个易扩展、性能优的中高频量化交易策略回测解决方案。该方案实现了库内行情回放、模拟撮合、中高频回测三大功能，支持通过
DLang、Python 或 C++ 语言完成中高频策略的研发和测试。具体来说，该方案涵盖以下三个模块：

* 回放功能：支持将一个或多个不同结构的分布式表中的数据严格按照时间或者按指定多列排序顺序**回放**到流表中，因此可以方便地解决因子计算和量化策略研发中研发和生产一体化的问题。
* 模拟撮合：支持沪深交易所 Level-2 逐笔行情和快照行情，实现与交易所一致的 **“价格优先，时间优先”**的高精度的撮合、具备基于多种行情数据的撮合模式、提供丰富的可用于模拟实盘环境的撮合配置。
* 回测：支持基于逐笔、快照、分钟和日频行情进行策略回测，可自定义指标，获取回测的收益、持仓、交易明细等信息。其中逐笔和快照行情支持高精度策略回测，可实现仿真和回测一体化的策略验证。

值得一提的是，这三个模块与外部解决方案兼容性良好。即使用户已经实现了某个环节的解决方案，DolphinDB
提供的解决方案也可以与其融合成一个完整的回测方案。

## 2. 基于 DolphinDB 的股票组合管理日频策略回测实现

本章节基于股票日频数据，利用 DolphinDB
回测插件实现了一个按目标权重进行每日动态调仓的组合回测示例。策略在指定调仓日根据预设权重调整持仓，以模拟实际投资组合的再平衡过程。

### 2.1 编写自定义策略

**首先，通过自定义函数检查标的是否具备交易条件**（当日是否停牌、是否触及涨停或跌停、成交量与价格是否有效）；随后，依据市场规则进行数量合规校验，将目标股数按交易所最小成交单位与整手规则进行取整与修正；最后，在给定资金约束下，将可用资金换算为可执行的买卖数量，得到实际下单数量。

```
def isBuyAble(data){
    if(data.volume <= 0.001 or (data.upLimitPrice == data.close)){
        return false
    }
    return true
}
def isSellAble(data){
    if(data.volume <= 0.001 or (data.downLimitPrice == data.close)){
        return false
    }
    return true
}
def checkBuyVolume(istock, num){
    if(num <= 0) {return 0 }
    if(istock.substr(0,2) == "68" and num >= 200){
        return num
    }
    else if(istock.substr(0,2) == "68"){ return 0}
    return floor(int(num)/100)*100
}
def getBuyAbleVolume(istock, cash, price){
    if(price <= 0. ) {return 0 }
    if(istock.substr(0,2) == "68" and floor(cash/price) >= 200){
        return floor(cash/price)
    }
    else if(istock.substr(0,2) == "68"){ return 0}
    return floor(floor(cash/price)/100)*100
}
```

**其次在 K 线回调函数** `onBar`
**中实现策略主体逻辑。**`onBar` 函数的 *msg* 参数，为回测引擎传入 K
线行情，*msg* 是一个字典，字典的 key 为标的名，而 value 为这只标的对应的行情信息。策略首先通过
`getTotalPortfolios` 接口获取当前账户的总权益，以及
`getPosition`
接口获取当前持仓。根据权益和持仓结合目标权重与当期价格，将权重换算为目标头寸，随后按照“**先卖出、再买入**”的顺序执行调仓操作，从而使组合持仓重新对齐至目标权重结构。以下代码展示了具体的的计算和调仓逻辑：（计算权重和买入卖出可以分开）

```
def onBar(mutable context, msg, indicator){
	weightsToday = context["targetWeight"][date(context["tradeDate"])]
	idate = date(context["tradeDate"])
	if(typestr(weightsToday) == "VOID"){ return }
	totalEquity = Backtest::getTotalPortfolios(context["engine"]).totalEquity[0]
	pos = select symbol, longPosition from Backtest::getPosition(context["engine"])
	pos = dict(pos.symbol,pos.longPosition)
	update weightsToday set targetMv = totalEquity*(1- 2*context["commission"]-context["tax"])*weight
	update weightsToday set open = each(getOpenPrice{msg},symbol)
	update weightsToday set targetPos = iif(open <= 0.,0,iif(symbol.substr(0,2) == "68"and floor(targetMv/open) >= 200,
	floor(targetMv/open),iif(symbol.substr(0,2) == "68",0,floor(floor(targetMv/open)/100)*100)))
	update weightsToday set Pos = nullFill(pos[symbol],0)

	sell = select symbol,Pos-targetPos as num from weightsToday where targetPos-Pos < 0
	sell = dict(sell.symbol,sell.num)
	for(istock in sell.keys()){
		data = msg[istock]
		num = sell[istock]
		if(isSellAble(data) and num > 0){
			Backtest::submitOrder(context["engine"], (istock, context["tradeTime"], 5, msg[istock].open, num, 3), "卖出平仓")
		}
	}

	buy = select symbol,targetPos-Pos as num from weightsToday where targetPos-Pos>0
	buy = dict(buy.symbol,buy.num)
	for(istock in buy.keys()){
		data = msg[istock]
		num = buy[istock]
		cash = Backtest::getAvailableCash(context["engine"])
		price = data.open
		qty = getBuyAbleVolume(istock, cash*(1- context["commission"]), price)
		num = min(checkBuyVolume(istock, num), qty)
		if(isBuyAble(data) and num > 0){
			Backtest::submitOrder(context["engine"], (istock, context["tradeTime"], 5, price, int(num), 1), "开仓买入")
		}
	}
}
```

### 2.2 根据策略设置相应的配置参数

回测的开始与结束日期、初始资金、手续费与印花税、行情类型及订单延时等均可通过参数灵活配置，用于模拟不同的市场环境和交易策略表现。此外，策略逻辑上下文
context 也可以通过配置参数设置策略中的全局变量，例如在本案例中，可通过 context
设置每日的目标权重数据，以及计算目标头寸时所需的手续费与税率参数。这样，策略在运行过程中即可直接引用这些全局变量完成资金分配与持仓调整。具体的初始参数配置代码示例如下：

```
config = dict(STRING,ANY)
config["startDate"] = 2012.02.01
config["endDate"] = 2022.04.28
config["strategyGroup"] = "stock"
config["cash"] = 100000000
config["commission"] = 0.0005
config["tax"] = 0.001
config["dataType"]  = 4
config["matchingMode"] = 3
config["outputOrderInfo"] = true
w = select * from loadTable("dfs://dbweight",`dt) where weight >0. order by tradeDay
dailyWeight = dict(DATE,ANY,true)
for (idate in sort(distinct(w.tradeDay))){
	s = select symbol, weight from w where tradeDay = idate
	dailyWeight[idate] = s
}
context = dict(STRING,ANY)
context["targetWeight"] = dailyWeight
context["commission"] = config["commission"]
context["tax"] = config["tax"]
config["context"] = context
```

### 2.3 创建回测引擎

设置引擎名称、引擎配置项、相应的回调函数、合约基本信息表等相应参数之后，通过接口 `createBacktester`
创建模拟撮合引擎实例。其中，接口 `createBacktester` 的第四个参数为表示是否开启 JIT 优化。默认值为
false，表示不开启，若需要开启 JIT 优化，只需要设置此参数为 true 即可。

```
strategyName = "Backtest_portfolio"
callbacks = dict(STRING,ANY)
callbacks["onBar"] = onBar
try{Backtest::dropBacktestEngine(strategyName)}catch(ex){print ex}
engine = Backtest::createBacktester(strategyName, config, callbacks,, )
timer Backtest::appendQuotationMsg(engine,  dailyData  );
```

### 2.4 执行回测引擎

通过 `Backtest::createBacktester` 创建回测引擎之后，可以通过以下方式执行回测，其中 dailyData
为相应的日频行情数据，行情数据字段和类型说明可参考回测插件的接口文档。

```
name=["symbol","tradeTime","open","low","high","close","volume","amount","upLimitPrice","downLimitPrice","prevClosePrice","signal"]
type=["STRING","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","DOUBLE","LONG","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE[]"]
dailyData= loadText("./portfolioData.csv",schema = table(name as name,type as type))
timer Backtest::appendQuotationMsg(engine,  dailyData );
```

### 2.5 获取回测结果

回测运行结束之后，可以通过相应的接口获取每日持仓、每日权益、收益概述、成交明细和策略中用户自定义的逻辑上下文。回测插件提供的完整回测结果接口可以参阅回测插件的接口说明文档。下图为本例获得的交易明细结果：

![](images/daily_stock_portfolio_backtest.png)

## 3. 性能测试

为了更直观地展示 DolphinDB 回测引擎在实际场景下的执行性能，我们选取了上交所 2000 只股票标的从 2025.01.02 到 2025.06.30
期间的历史日频数据作为测试样本。在单线程、非 JIT 模式下运行该策略示例，共处理了 232196 条行情数据，生成 28021 笔订单，整体回测耗时约为 0.9
秒。

## 4. 总结

在量化研究中，组合管理策略的回测不仅关注单一标的的交易收益，更强调多标的之间的动态权重调整与整体风险控制。为在计算效率与策略复杂度之间取得平衡，本文展示了一种基于
DolphinDB
回测插件的股票日频组合再平衡实现方案：策略通过读取外部权重文件或预设权重矩阵，在指定调仓日按“先卖出、再买入”的顺序对各标的头寸进行再平衡，以保持组合与目标权重的一致性。该方案既保留了日频回测的高效性，又能灵活扩展至不同权重生成逻辑与再平衡周期，从而为资产配置、指数增强及量化选股策略提供统一的验证框架。通过本案例，可以直观体现
DolphinDB 在多标的回测、资金约束管理与调仓执行方面的高性能表现，以及其在组合类量化策略研究中的应用潜力。

## 5. 附录

股票组合管理策略 demo 以及所需要的数据

[portfolioStrategy.dos](https://cdn.dolphindb.cn/zh/tutorials/script/daily_stock_portfolio_backtest/portfolioStrategy.dos)

[portfolioData.csv](https://cdn.dolphindb.cn/zh/tutorials/data/daily_stock_portfolio_backtest/portfolioData.csv)

[weight.csv](https://cdn.dolphindb.cn/zh/tutorials/data/daily_stock_portfolio_backtest/weight.csv)
