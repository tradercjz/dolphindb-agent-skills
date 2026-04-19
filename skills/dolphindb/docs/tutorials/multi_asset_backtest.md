<!-- Auto-mirrored from upstream `documentation-main/tutorials/multi_asset_backtest.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 多资产回测使用说明及示例

在金融市场中，涵盖多种资产的投资策略早已成为主流实践。无论是跨市场套利、大类资产配置，还是套期保值与波动率管理，投资组合往往需要同时运用股票、期货、期权等多种工具。相比单一资产，联合回测能够更真实地反映资金使用、风险暴露和执行路径，从而更贴近实盘表现。基于这一需求，DolphinDB
推出了多资产混合回测，使用户能够在同一框架下实现多品种协同回测，并通过单一账户或多账户灵活管理现金和持仓。本文将以两个典型案例——股票与股指期货对冲策略，以及期货与期权套利策略，来展示
DolphinDB 多资产回测引擎的使用方法以及其在实际应用中的优势。

## 1. 背景介绍

本文将展示两个多资产回测案例：其一是在多个账户下结合技术分析指标投资股票，并同时持有股指期货以对冲系统性风险；其二是在单一账户下利用期货与期权的认购–认沽平价关系进行跨市场套利。

在介绍策略的具体实现过程之前，本章将简要阐述这两类策略的核心思路，并概述 DolphinDB 提供的多资产回测解决方案，以帮助读者更清晰地理解应用背景与场景。

### 1.1 股票期货对冲策略背景介绍

在股票投资中，由于个股与市场整体高度相关，投资组合不可避免地暴露于系统性风险。为了削弱这一类无法通过分散化规避的风险，投资者通常借助股指期货进行 β 对冲。β
系数衡量了组合相对于市场的敏感度，通过卖出与组合 β
相匹配的股指期货合约，可以将组合整体的市场风险敞口降至目标水平，从而在保留选股所带来的超额收益能力的同时，削弱市场波动对组合表现的干扰。这一策略广泛应用于主动管理基金、量化市场中性策略以及风险管理实践，是股票与衍生品结合的典型场景。

在本文的案例中，我们将基于多个技术分析指标，从沪深 300 成分股中择股投资，并通过沪深 300 股指期货实现 β 对冲，以展示 DolphinDB
多资产回测框架在实际策略中的应用。

### 1.2 期货期权跨市场套利策略背景介绍

在衍生品市场中，期货与期权同属于基础资产的衍生工具，但定价机制与风险特征存在显著差异。两者之间的定价关系不仅受标的资产价格影响，还与无风险利率、股息率、波动率预期等因素密切相关。在理论框架下，认购–认沽平价关系（Put–Call
Parity）为期货与期权之间的定价提供了严格约束，若市场价格偏离该平价关系，便会出现无风险或低风险套利机会。投资者可以通过构建“买入低估资产 +
卖出高估资产”的组合，锁定确定性价差收益。

在接下来的案例中，我们将基于期货与期权的认购–认沽平价关系设计跨市场套利策略，借此展示 DolphinDB
多资产混合回调在统一资金管理、风险控制与跨品种交易方面的优势。

### 1.3 DolphinDB 多资产回测解决方案概述

DolphinDB
回测插件现已全面支持多资产策略回测。在统一的回测框架下，用户可以同时加载股票、期货、期权等多类资产的行情与交易规则，并在同一引擎中实现资金、保证金与风险控制的统一管理，从而获得更贴近实盘的模拟效果。与传统的单资产回测相比，多资产回测在引擎配置、账户管理以及行情数据输入方式等方面均有所扩展，构成了一套更加完整的解决方案。

**与单一资产回测的主要差异：**

* **账户管理：**多资产回测可以在同一引擎中可同时管理多个账户，或以字典形式配置单一账户覆盖多个资产；
* **接口调用方式：**在回测插件接口中新增参数 *assetType*（账户类型），用于区分股票、期货、期权等不同资产；
* **引擎相关配置：**

  + 账户配置：初始资金 cash 必须是字典结构，以支持不同账户或多资产共享账户的管理;
  + 行情配置： 配置项 multiAssetQuoteUnifiedInput
    决定输入的行情是多个资产合成的表，还是不同资产单独输入；
  + 回调机制配置：配置项 msgAs​PiecesOnSnapshot 决定是每条数据依次触发
    `onSnapshot` 回调函数，还是同一时间戳的所有数据同时触发；
* **行情数据输入：**

  + 通过 `appendQuotationMsg` 接口插入数据时，*msg*
    必须为字典；
  + 当 multiAssetQuoteUnifiedInput 为 true 时，可通过 *multiAsset*
    字段一次性输入多类资产行情，并用 *assetType* 字段区分。
  + 当 multiAssetQuoteUnifiedInput = false 时，则需分别输入
    stock、futures、options 表;

引擎配置、行情输入输出、基本信息表等详细信息可参考多资产。

## 2. 基于 DolphinDB 的股票期货对冲策略实现

本案例基于沪深 300
成分股的分钟级行情数据，构建了一个结合趋势与动量的多资产对冲策略。策略核心思路是通过双均线、RSI（相对强弱指数）与波动率指标捕捉趋势信号，并利用沪深 300
股指期货主力合约进行 β 对冲，以降低市场系统性风险。整体逻辑如下：

* **指标计算**：

  + 使用 5 分钟与 20 分钟窗口计算短期和长期移动平均线，同时保留前一时刻的数值以判断均线交叉；
  + 以过去 10 分钟的收益率标准差衡量短期波动率；
  + 基于 14 分钟收盘价序列计算 RSI 指标，用于识别超买超卖状态。
* **开仓逻辑**：

  当短期均线上穿长期均线（形成金叉），且 RSI 超过 70 时，买入开仓，捕捉强势趋势的延续。
* **止损逻辑**：

  当持有多仓期间，若价格跌破短期均线、显示短期趋势转弱，并且波动率超过 5%，则卖出平仓，以规避潜在回撤。
* **期货对冲**：

  在股票组合持仓的基础上，计算加权后的组合 β 值，并据此确定所需卖出的股指期货合约数量，从而对冲系统性风险，保留选股带来的超额收益。

### 2.1 编写自定义策略

**首先，基于分钟频行情数据定义技术分析指标：**

* **移动均线**：计算个股的短期均线 (shortMA) 与长期均线 (longMA) 以识别趋势信号，同时利用 prev
  函数获取前一期均线值 (prevShortMA、prevLongMA)，用于判断均线交叉。
* **相对强弱指数（RSI）**：衡量个股的超买或超卖状态，辅助控制建仓与平仓时的情绪风险。
* **波动率（volatility）**：通过收益率的标准差度量价格波动幅度，为风险管理提供依据，避免高波动资产对组合产生不利影响。

为了满足使用中高频行情数据计算类似量价因子的需求，DolphinDB
回测引擎采用了状态响应式引擎。这一引擎能够实现流批统一计算，并有效处理带有状态的高频因子，具体也可以参考状态响应式引擎用户手册定义相应的指标。以下是定义技术指标长短期均线、波动率的代码示例：

```
@state
def myMA(close,period){
    ma=sma(close,period)
    return ma, prev(ma)
}
@state
def getVolatility(close, period=10){
    returns = DIFF(close) / REF(close, 1)
    return STD(returns, period)
}
```

中高频回测中，策略通常是事件驱动的，而一个策略逻辑通常需要涉及多种事件，比如新的行情到来、新的订单成交等等。DolphinDB
回测引擎采用事件驱动机制，提供了全面的事件函数如策略初始化函数、盘前回调函数、行情回调函数、每日盘后回调函数等，用户可以在相应的回调函数中编写策略逻辑实现相应的策略。此外，自定义回调函数支持
JIT 技术，可以有效提升策略执行效率。后续本案例将会展示不同的事件函数是如何实现的。

**在策略初始化函数中，首先订阅基于行情数据计算的移动均线指标、 RSI 指标和波动率指标。**这里
`subscribeIndicator` 接口传入回测引擎句柄、需要计算的数据类型、需要计算的指标字典（key
为指标名，用于之后访问；value 为指标计算的元代码），之后计算结果将传入`onBar` 等策略回调函数。

```
def initialize(mutable contextDict){
    d = dict(STRING, ANY)
    d["shortMA"] = <myMA(close, 5)[0]>
    d["prevShortMA"] = <myMA(close, 5)[1]>
    d["longMA"] = <myMA(close, 20)[0]>
    d["prevLongMA"] = <myMA(close, 20)[1]>
    d["rsi"] = <RSI(close, 14)>
    d["volatility"] = <getVolatility(close, 10)>
    Backtest::subscribeIndicator(contextDict["engine"], "kline", d,"stocks")
}
```

**在 K 线行情回调函数**
`onBar`
**中，系统会基于订阅的技术指标生成股票买入或卖出信号，并结合当前股票持仓和预先计算好的 β
值确定需要买入或卖出的期货合约数量，以实现动态对冲。**`onBar` 函数的 *msg*
参数，为回测引擎传来的最新分钟频行情， *msg* 是一个字典，字典的 key 为期货标的名，而 value
为这支期货标的对应的行情信息，在本例中个股的 β 值作为扩展字段随行情一并传入。以下代码示例展示了：

* 股票买入开仓与卖出平仓的判断逻辑；
* 基于加权平均 β 值计算期货对冲仓位的实现方式。

```
def onBar( mutable contextDict, msg, indicator){
    stockPosDict = contextDict["stockPos"]
    stockBetaDict = contextDict["beta"]
    keysAll=msg.keys()
	keys1 = keysAll[!(like(keysAll,"IF%"))]
    for(i in keys1 ){
            istock = msg[i].symbol
            close = msg[i].close
            symbolSource = msg[i].symbolSource
            shortMA = indicator[i].shortMA
            prevShortMA = indicator[i].prevShortMA
            longMA = indicator[i].longMA
            prevLongMA = indicator[i].prevLongMA
            rsi = indicator[i].rsi
            volatility = indicator[i].volatility
            &position = Backtest::getPosition(contextDict.engine,istock,"stock")
            longPos = position.longPosition
            beta = msg[i].beta

        //股票买开:没有持仓且短均线穿过长均线且RSI >80
        if (longPos<=0 && shortMA>longMA && prevShortMA<=prevLongMA && rsi>70){
           Backtest::submitOrder(contextDict["engine"], (istock, symbolSource,contextDict["tradeTime"], 5, close, ,,100,1,,,), "stock buyOpen",0)
        }

        // 股票卖平
        else if (longPos>0 && close<shortMA && volatility>0.05){
            Backtest::submitOrder(contextDict["engine"], (istock,symbolSource, contextDict["tradeTime"], 5,close, ,,longPos,3,,,), "stock sellClose",0)
        }
        //记录持仓以及对应的beta值
        stockBetaDict[istock]=beta
        &position = Backtest::getPosition(contextDict.engine,istock,"stock")
        longPos = position.longPosition
        stockPosDict[istock]= longPos*close
        contextDict["stockPos"]=stockPosDict
        contextDict["beta"]=stockBetaDict
        }
     // 股指期货beta对冲
    longPos = Backtest::getPosition(contextDict.engine, contextDict["futuresCode"], "futures").longPosition
    shortPos = Backtest::getPosition(contextDict.engine, contextDict["futuresCode"], "futures").shortPosition
    if(shortPos<1 and contextDict["futuresCode"] in msg.keys()){
        futuresPrice = msg[contextDict["futuresCode"]].close
		symbolSource = msg[contextDict["futuresCode"]].symbolSource
        vt = table(stockPosDict.keys() as symbol, stockPosDict.values() as value)
        bt = table(stockBetaDict.keys() as symbol, stockBetaDict.values() as beta)
        temp = lj(vt, bt, `symbol)
        comBeta = exec sum(value * beta) from temp
        if (comBeta==0){return}
        qty = round(comBeta/futuresPrice)
        combo_position = sum(stockPosDict.values())
        qty=qty*300
       //股票复合beta>0 卖开期货进行对冲
        if (combo_position>0 && qty>0){
            orderMsg=(contextDict["futuresCode"],msg[contextDict["futuresCode"]].symbolSource , contextDict.tradeTime, 5, futuresPrice, ,,qty,2,,,)
            Backtest::submitOrder(contextDict.engine, orderMsg,"future sellopen",0,"futures")
        }
        //股票复合beta<0 买开期货进行对冲
        else if (combo_position>0 && qty<0){
            m=-qty
            orderMsg=(contextDict["futuresCode"],msg[contextDict["futuresCode"]].symbolSource , contextDict.tradeTime, 5, futuresPrice, ,,m,1,,,)
            Backtest::submitOrder(contextDict.engine, orderMsg,"future buyopen",0,"futures")
        }
    }
}
```

这里的 `Backtest::submitOrder`是回测引擎提供的下单接口：

```
Backtest::submitOrder(engine, msg, label="", orderType=0,contractType)
//engine 引擎实例
//msg:订单信息
//label:可选参数，方便用于对订单进行分类
//orderType: 订单类型，支持普通订单、算法订单和组合订单的不同种订单
//contractType: STRING 类型标量，表示订阅的行情品种类型
```

除了根据行情到来编写相应策略外，中高频回测引擎还支持针对委托订单发生订单状态变化、成交、每日盘后进行账户信息统计、策略结束之前处理相应的业务逻辑等编写相应策略。要了解所有中高频回测引擎支持的事件回调函数，请参阅回测插件接口说明文档。

### 2.2 根据策略设置相应的配置参数

回测的开始与结束日期、初始资金、手续费和印花税、行情类型、订单延时等均可以通过参数进行配置。这些参数允许用户灵活地调整回测条件，以模拟不同的市场环境和交易策略的效果。此外策略逻辑上下文
context 也可以通过参数设置策略中的全局变量，此案例中我们在 context 中设置了策略中需要储存的股票持仓以及对应的 β
值。具体的初始参数配置代码示例如下：

```
startDate=2024.01.01
endDate=2024.12.31
userConfig = dict(STRING,ANY)
userConfig["startDate"] =  startDate
userConfig["endDate"] = endDate
userConfig["strategyGroup"] = "multiAsset"
cashDict = dict(STRING,DOUBLE)
cashDict["stocks"] = 100000000.
cashDict["futures"] = 100000000.
userConfig["cash"] = cashDict
userConfig["dataType"] = 3
userConfig["matchingMode"] = 3
userConfig["frequency"] = 0
userConfig["outputOrderInfo"] = true
userConfig["multiAssetQuoteUnifiedInput"] = false
userConfig["depth"]= 5
userConfig["outputOrderInfo"] = true
userConfig["commission"]= 0.00
userConfig["tax"]= 0.00
Context = dict(STRING, ANY)
//股票持仓
Context["stockPos"] = dict(STRING, ANY)
//股票beta
Context["beta"] = dict(STRING, ANY)
userConfig["context"] = Context
```

在本案例中，我们设置多个账户分别管理不同资产的资金，通过 cashDict 这个字典设置股票和期货账户的初始资金。

### 2.3 创建回测引擎

设置引擎名称、引擎配置项、真实行情表的结构和字段映射字典、委托订单的结构和字段映射字典，以及订单详情输出表和合成快照输出表等相应参数之后，通过接口
`createBacktester` 创建模拟撮合引擎实例。其中，接口
`createBacktester` 的第四个参数为表示是否开启 JIT 优化。默认值为
false，表示不开启，若需要开启 JIT 优化，只需要设置此参数为 true 即可。

```
engineName="test01"
callbacks=dict(STRING,ANY)
callbacks["initialize"] = initialize
callbacks["beforeTrading"] = beforeTrading
callbacks["onBar"] = onBar
engine= Backtest::createBacktester(engineName, userConfig, callbacks,false,futuSecurityReference)
```

### 2.4 执行回测引擎

通过 `Backtest::createBacktester` 创建回测引擎之后，可以通过以下方式执行回测。dict\_msg
为储存相应的股票、期货分钟频率行情数据的字典，行情数据字段和类型说明参考回测插件的接口文档。

```
dict_msg=dict(STRING,ANY)
dict_msg["futures"] =select* from  futuresData order by tradeTime
dict_msg["stocks"] = select * from stocksData order by tradeTime
Backtest::appendQuotationMsg(engine,dict_msg)
```

### 2.5 获取回测结果

回测运行结束之后，可以通过相应的接口获取每日持仓、每日权益、收益概述、成交明细和策略中用户自定义的逻辑上下文。回测插件提供的完整回测结果接口可以参阅回测插件的接口说明文档。下图为本例获得的账户每日权益结果：

![](images/multi_asset_backtest.png)

## 3. 基于 DolphinDB 的期货期权套利策略实现

本案例基于沪深 300
股指期货主力合约的分钟级行情数据，以及其对应的认购、认沽期权的分钟级行情数据，构建了一个基于认购–认沽平价关系的多资产套利策略。策略核心是基于下述平价关系：

![](images/multi_asset_backtest_formula.png)

通过比较市场价格与该平价关系，当出现明显偏离时，构建“买入低估资产 + 卖出高估资产”的组合，获取套利机会，整体逻辑如下：

**指标计算：**

* 期货理论价差：期货价格 − 执行价贴现值；
* 期权实际价差：认购期权价格 − 认沽期权价格；
* 通过两者的比值来衡量偏离程度。

**套利逻辑：**

* 当价差偏大（超过上限阈值）：

  + 买入期货；
  + 卖出虚一档认购期权；
  + 买入虚一档认沽期权。
* 当价差偏小（低于下限阈值）：

  + 卖出期货；
  + 买入虚一档认购期权；
  + 卖出虚一档认沽期权。

### 3.1 编写自定义策略

在策略初始化函数 `initialize` 中设置折溢价上下限阈值、无风险利率等全局参数。

```
def initialize(mutable context){
    context["upper"] = 0.005
    context["down"] = 0.007
    context["futuresCode"] = 'IF2306'
    context["callOption"] ="IO2306C4750"
    context["putOption"] ="IO2306P4750"
    context["strikePrice"] = 4750.
    context["rf"] = 0.02
    context["maturity"] = 0.67
}
```

在 `onBar` 策略回调函数中，根据上述指标计算逻辑计算相应的价差指标，并通过套利逻辑进行开平仓逻辑处理。

```
def onBar(mutable context, msg,indicator){
    futureSpread = msg[context["futuresCode"]]["close"] - context["strikePrice"]*exp(-context["rf"]*context["maturity"])
    optionSpread = msg[context["callOption"]]["close"] -msg[context["putOption"]]["close"]
    futPos = Backtest::getPosition(context.engine, context["futuresCode"], "futures")
    calloptPos = Backtest::getPosition(context.engine, context["callOption"], "option")
    putoptPos = Backtest::getPosition(context.engine, context["putOption"], "option")

    if(double(optionSpread)\double(futureSpread)-1 > context["upper"]){
        if(futPos.longPosition<1 && context["futuresCode"] in msg.keys()){
            futuresPrice = msg[context["futuresCode"]]["close"]
            symbolSource = msg[context["futuresCode"]]["symbolSource"]
            orderMsg=(context["futuresCode"],symbolSource, context.tradeTime, 5, futuresPrice,0. ,,5,1,,0,)
            Backtest::submitOrder(context.engine, orderMsg,"buyOpen future",0,"futures")
        }

        if( calloptPos.shortPosition<1){
            futuresPrice = msg[context["futuresCode"]]["close"]
            level = msg[context["callOption"]]["level"]
            optType = msg[context["callOption"]]["optType"]
            strikePrice = msg[context["callOption"]]["strikePrice"]
            if(int(level)==1 and optType==1 and strikePrice > futuresPrice){
                symbolSource = msg[context["callOption"]]["symbolSource"]
                price = msg[context["callOption"]]["close"]
                orderMsg=(context["callOption"], symbolSource , context.tradeTime, 5, price,0. ,,5,2,,0,)
                Backtest::submitOrder(context["engine"], orderMsg,"sellOpen call option",0,"option")
            }
        }
        if( putoptPos.longPosition<1){
            level = msg[context["putOption"]]["level"]
            optType = msg[context["putOption"]]["optType"]
            strikePrice = msg[context["putOption"]]["strikePrice"]
            price=msg[context["putOption"]]["close"]
            if(int(level)==1 and optType==2 ){
                symbolSource = msg[context["putOption"]]["symbolSource"]
                price = msg[context["putOption"]]["close"]
                orderMsg=(context["putOption"],symbolSource , context.tradeTime, 5, price,0. ,,5,1,,0,)
                Backtest::submitOrder(context["engine"], orderMsg,"buyOpen put option",0,"option")
            }
        }
    }
    ...
}
```

### 3.2 根据策略设置相应的配置参数

在本案例中，我们采用统一账户管理模式，即所有期货与期权头寸均归属于同一个账户进行资金核算与风险控制。在参数配置中通过 cashDict
字典来配置账户的初始资金。这样不仅保证了不同资产之间能够共享和动态调配保证金，还能更真实地模拟实盘中多资产共用账户的风险管理机制。

```
startDate=2023.01.01
endDate=2023.02.03
userConfig=dict(STRING,ANY)
userConfig["startDate"]= startDate
userConfig["endDate"]= endDate
userConfig["strategyGroup"]= "multiAsset"
cashDict=dict(STRING,DOUBLE)
cashDict["futures, options"]=100000000.
userConfig["cash"]= cashDict
userConfig["dataType"]=3
userConfig["msgAsTable"]= false
userConfig["frequency"]= 0
userConfig["outputOrderInfo"]= true
userConfig["multiAssetQuoteUnifiedInput"]= false
userConfig["depth"]= 5
userConfig["commission"]= 0.00015
userConfig["tax"]= 0.001
```

## 4. 性能测试

为了更直观地评估 DolphinDB 高频回测引擎在典型场景下的执行性能，我们基于上述两个案例进行了测试：

**股票–期货对冲策略：**选取沪深 300 成分股的两天分钟 K 线数据（共 144,000 条），以及沪深 300 股指期货主力合约的两天分钟K线数据（394
条）。在单线程、非 JIT 模式下运行该策略示例，共生成 156 笔订单，整体回测耗时约 5.2 秒。

**期货–期权套利策略：**选取沪深 300 股指期货主力合约及其对应的一只认购期权和一只认沽期权，两天的分钟 K 线数据，共约 4,000
条行情数据。回测过程中共生成 40 笔成交订单，整体回测耗时仅 0.012 秒。

## 5. 总结

在量化研究中，跨资产策略往往涉及股票、期货、期权等多类工具，单一资产的回测框架难以全面反映组合层面的资金占用、风险暴露与执行路径。本文通过股票与股指期货 β
对冲策略、期货与期权平价套利策略两个典型案例，展示了 DolphinDB
多资产回测框架在复杂策略场景下的表现。用户可以在统一的回测引擎中同时管理多个账户、灵活配置资金与保证金，并通过混合回调机制实现不同资产类别的协同模拟。相比传统的分资产回测，DolphinDB
不仅大幅降低了跨市场策略的实现复杂度，还在中高频行情驱动下保持了高效的计算性能与完整的交易细节还原，为多资产策略的验证与落地提供了坚实支撑。

## 6. 附录

股票期货对冲策略的 demo 及需要的数据样例：

[股票+期货2.dos](https://cdn.dolphindb.cn/zh/tutorials/script/multi_asset_backtest/stocks_futures2.dos)

[futureTest.csv](https://cdn.dolphindb.cn/zh/tutorials/script/multi_asset_backtest/futureTest.csv)

[stockTestData.csv](https://cdn.dolphindb.cn/zh/tutorials/script/multi_asset_backtest/stockTestData.csv)

期货期权套利策略的 demo 及需要的数据样例：

[optionIOdata.csv](https://cdn.dolphindb.cn/zh/tutorials/script/multi_asset_backtest/optionIOdata.csv)

[futureDataIF.csv](https://cdn.dolphindb.cn/zh/tutorials/script/multi_asset_backtest/futureDataIF.csv)

[期货+期权.dos](https://cdn.dolphindb.cn/zh/tutorials/script/multi_asset_backtest/futures_options.dos)
