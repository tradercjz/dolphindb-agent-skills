<!-- Auto-mirrored from upstream `documentation-main/plugins/backtest/quick_start.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB 回测插件快速上手

使用 DolphinDB 脚本来编写回测策略，通常包含以下步骤：

* 在策略初始化函数中定义所需的指标；
* 在其他相应的回调函数（如 `onBar`、`onSnapshot` 等）中实现自定义交易逻辑；
* 配置策略相关参数，如行情源、初始资金、订单延时、成交比例等；
* 基于策略和配置创建回测引擎；
* 回放数据源并执行回测；
* 获取并分析回测结果。

本文将通过示例演示如何使用 DolphinDB 回测插件完成策略编写与回测执行。示例适用于 DolphinDB Server 2.00.14.1、3.00.2.1
及以上版本。在执行本文示例前，请参照“插件安装”小节完成插件安装。

## 1. 回测快速上手：构建一个基础策略回测

DolphinDB 回测框架基于 DolphinDB
Server，通过插件形式提供适用于多种资产的回测引擎。本章将通过一个简单的中高频交易策略，演示如何使用回测引擎进行策略回测。

### 1.1 实现一个简单策略

基于分钟 K 线行情，对于每一只标的，当持仓为空时，执行买入操作。本示例使用的数据见附件。

```
//step 1：编写策略逻辑
def onBar(mutable context, msg, indicator){
	for(istock in msg.keys()){
		&pos=Backtest::getPosition(context.engine,istock)
		price=msg[istock].close
		//没有持仓时，买入
		if(pos.longPosition<1){
			Backtest::submitOrder(context.engine, (istock,
			context.tradeTime,5, price+0.02,100, 1),"buyOpen")
		}
	}
}
//step 2：配置参数
config = {
	startDate: 2023.07.11 ,//回测开始日期
	endDate: 2023.07.11 , //回测结束日期
	strategyGroup: `stock,//股票策略
	cash: 1000000.,  //策略初始资金
	commission: 0.00015,//费用
	tax: 0.001,
	dataType: 3//回测行情，dataType = 3 表示分钟行情
}
callbacks = { onBar:onBar}
try{Backtest::dropBacktestEngine("test01")}catch(ex){print ex}//删除引擎
 //step 3:创建引擎，不开启JIT
 engine = Backtest::createBacktester("test01", config, callbacks, false)
 // step 4:执行回测，获取结果
colName=`symbol`tradeTime`open`low`high`close`volume`amount`upLimitPrice`downLimitPrice
colType=["SYMBOL","TIMESTAMP","DOUBLE","DOUBLE","DOUBLE","DOUBLE","LONG","DOUBLE","DOUBLE","DOUBLE"]
dayData = loadText(filename="./barData.csv",schema=table(colName as name ,colType as type ))
Backtest::appendQuotationMsg(engine, dayData) //执行策略回测
tradeDetails = Backtest::getTradeDetails(engine)
ret = Backtest::getReturnSummary(engine)
```

### 1.2 展示回测结果

在完成回测之后，用户可以通过相关接口获取回测结果。以下为通过 `getTradeDetails`
接口获得的部分交易明细表的内容。其中字段 “direction” 表示订单委托买卖方向，1 表示买开，2
表示卖开；“orderPrice”，“orderQty” 分别表示委托的价格以及数量；“label” 为标签，是方便标识的字符串，可在下单时自行设置。

![](../images/quick_start/1_1.png)

### 1.3 代码讲解

下面我们将详细讲解 1.1 中的策略代码，以便于读者理解以及学习回测插件的使用。

第 **1-12** 行定义的 `onBar` 为 K
线行情回调函数，用户可以在该函数中编写策略逻辑，如开仓、平仓等。该函数包含三个参数，分别为
*context*、*msg*、*indicator*。其中 context 为逻辑上下文，需要在引擎配置参数
*userConfig* 中定义；msg 为 K 线行情数据，在第 **31** 行回测引擎将插入的行情数据逐条传入
`onBar` 中进行策略实现；*indicator*
为指标，用户不仅可以将已有的指标传入，也可通过内置引擎计算自定义指标并订阅，下一章将详细介绍指标的定义。在 `onBar`
策略中，通过接口 `getPosition` 获取当前的持仓情况，作为后续策略判断；最后通过接口
`submitOrder` 进行委托下单。

第 **14-22** 行中配置了回测引擎的基本参数，如回测开始日期、结束日期、策略类型、初始资金、手续费用等等，用户必须正确配置才能保证回测的进行。而
*context* 则为策略所需的参数，可以根据实际需求设置。

第 **26** 行通过接口`createBacktester`创建回测引擎。需要注意的是，“test01”
为引擎的名称，若已有该名称的引擎则会创建失败，因此可以先删除同名的引擎，如第 **24** 行。在创建引擎前，需要确保所有的参数已经定义完成。其中
*config* 为引擎参数，*callbacks* 为事件回调函数（第 **23** 行），false 表示不开启 JIT
优化。

第 **28-30** 行获取行情数据，并插入引擎中执行策略回测。由于回测引擎对行情数据结构有明确的要求，因此可以通过 *schema*
确保结构一致再传入。

最后，通过不同的引擎接口，获取不同回测结果，如第 **32-33** 行。

## 2. 回测进阶：策略扩展与性能优化

本章将从上一章的简单策略出发，介绍如何利用回测引擎的事件驱动机制，灵活运用各类事件函数，逐步扩展和优化策略逻辑。

### 2.1 事件函数概览

回测引擎采用灵活高效的事件驱动机制，针对用户不同的策略需求提供了一系列丰富的事件函数，其中包括用于策略参数和环境初始化的初始化函数（`initialize`），用于实现每日盘前准备工作的盘前回调函数（`beforeTrading`）以及每日盘后策略总结分析的盘后回调函数（`afterTrading`）；在行情处理方面，引擎不仅提供了用于实时快照数据处理的回调函数（`onSnapshot`），还为不同时间粒度的数据提供了分钟和日频的行情回调函数（`onBar`），能够有效支持多种交易频率的策略；此外，引擎还为交易过程中的委托和成交事件分别提供了委托状态回调函数（`onOrder`）和成交回报回调函数（`onTrade`），方便用户实时监控和调整策略的执行过程。通过这些丰富的事件回调函数，用户可以轻松地实现精细化、自定义的策略逻辑。

接下来我们将通过具体的例子来讲解上述事件函数该如何使用。

### 2.2 在策略初始化函数中定义指标

策略初始化函数在策略回测过程中只触发一次。用户可在此函数中初始化全局变量
context，设定策略所需的全局参数或状态；同时，也可在此阶段订阅或配置策略运行期间需要使用的各类指标计算，以确保后续策略运行过程中能获取相关指标数据。

为展示策略初始化函数的作用，我们将实现一个简化的示例策略，完整代码将在下一节介绍 `onSnapshot`
函数时给出。该策略以股票的快照数据为行情源，当当日最新价格相较昨日收盘价上涨超过 1%，买入 100股，单日最多开仓一次，最大持仓不超过 500
股。在初始化函数中，我们定义了一个名为 `pctChg` 的指标，用于计算当前 tick
与昨日收盘价之间的收益率变化，用作交易信号的触发依据。

```
@state
def pctChg(lastPrice, prevClosePrice){
	return lastPrice\prevClosePrice - 1
}
def initialize(mutable context){
	//初始化回调函数
	print("initialize")
	//订阅快照行情的指标
	d = dict(STRING,ANY)
	d["pctChg"] = <pctChg(lastPrice, prevClosePrice)>
	Backtest::subscribeIndicator(context["engine"], "snapshot", d)
	context["maxPos"] = 500
}
```

在策略中，如果想要订阅最新价格与昨日收盘价的指标，可以使用引擎提供的 Backtest::subscribeIndicator
接口，指定相应的因子名称和因子表达式即可实现该的策略指标的订阅。该接口使用示例如下：

```
Backtest::subscribeIndicator(engine, quote, indicatorDict)
```

订阅指标之后，在 `onSnapshot`策略回调函数中可以通过 indicator.pctChg 获取相应的指标计算结果。

### 2.3 基于快照行情数据编写策略

基于上一节的策略思路，下面将展示基于股票快照行情调用 `onSnapshot`
实现策略的代码。`onSnapshot` 的 *msg*
参数，为回测引擎传来的最新快照行情；*indicator* 中包含 `initialize`
中策略订阅的指标值。回调函数的行情 *msg* 和 *indicator* 为字典，msg.bidPrice 返回的是该标的最新十档买价，而
indicator.pctChg 返回的就是最新价相比于前价的收益率。本示例的完整回测代码及数据模拟代码见附件。

```
def onSnapshot(mutable context, msg, indicator){
    //查询目前该的持仓
    &pos = Backtest::getPosition(context["engine"], msg.symbol)
    if (indicator.pctChg > 0.01 and pos.longPosition <= context.maxPos and
        context["open"][msg.symbol] != true){
		Backtest::submitOrder(context["engine"],
			(msg.symbol, context["tradeTime"], 5, msg.offerPrice[0], 100, 1), "buy")
		context["open"][msg.symbol] = true
    }
}
```

### 2.4 多种行情类型数据

DolphinDB 的回测引擎支持多种行情消息的策略回测，以满足不同用户的回测需求，除了上述示例展示的 `onBar` 和
`onSnapshot`
以外，用户同样可以基于不同的行情数据通过调用相对应的事件回调函数来实现策略，行情的类型通过配置参数的 `dataType`
配置项指定。

| config的配置项 | 行情类型 |
| --- | --- |
| "dataType" | 0：股票逐笔（逐笔委托+逐笔成交）或者股票逐笔+快照  1：快照  2：快照+成交明细  3：分钟频率  4：日频  5：股票逐笔（逐笔委托+逐笔成交合并的宽表）  6：股票逐笔+快照（逐笔委托+逐笔成交+快照合并的宽表） |

不同的品种同频率的行情数据也稍有差别，如银行间债券快照频率的数据包括到期收益率字段。具体可以参考 Backtest 插件该品种的指定频率的行情数据说明，不同类型的行情输入表均支持
DOUBLE、STRING、INT 类型的扩展字段。

### 2.5 多品种及多资产混合回测

除了不同频率的行情以外，DolphinDB 回测引擎不仅支持对各类资产品种（如 “stocks”、“futures”、“options”、 “bond”和
“universal”等）进行单一品种的策略回测，还支持在同一个回测引擎中对多个资产进行联合回测。同时，用户可以通过单一账户或多个账户对相应的多个资产进行现金和持仓管理。针对不同的品种，用户需要在创建引擎时通过配置参数的
`strategyGroup` 配置项指定策略类型。

| config的配置项 | 策略类型 |
| --- | --- |
| "strategyGroup" | * "stock"：股票 * "futures"：期货 * "option"：期权 * "cryptocurrency"：数字货币 * "securityCreditAccount"：融资融券 * "CFETSBond"：银行间债券 * "XSHGBond"：上交所债券 * "universal"：通用品种 * "multiAsset"：多资产 |

当指定配置项 *strategyGroup*为 “multiAsset” 时，初始资金 `cash`
配置项为字典，支持使用同一个账户或多个账户分别管理不同资产的资金。如 `cashDict["futures,
options"]=100000000.` 代表 futures 和 options 多资产类型使用同一个资金账户，如
`cashDict["futures"]=100000000.` 则代表 futures
独立使用一个资金账户。`cash` 配置项不仅决定了账户资金，还控制子回测引擎和模拟撮合引擎的创建。仅当资产类型在
`cash` 配置项中被指定时，才会创建对应的回测和模拟撮合引擎。

下面将通过一个股票与期货使用独立资金账户的案例，展示如何在 DolphinDB
中实现多资产混合回测。为简化策略逻辑，选取一只股票和一只期货作为回测标的，基于二者的分钟频 K
线行情，当账户无持仓时触发买入操作。案例所使用的数据及完整回测代码详见附件。

```
//step 1：选取回测标的
def beforeTrading(mutable context){
	context["futuresCode"] = "IC2401"
	context["stockCode"] = "600000"
}
//step 2：编写策略逻辑
def onBar( mutable context, msg, indicator){
	longPos = Backtest::getPosition(context.engine, context["stockCode"], "stock").longPosition
	if(longPos < 0  and context["stockCode"] in msg.keys() ){
		price = msg[context["stockCode"]].close
		symbolSource = msg[context["stockCode"]].symbolSource
		orderMsg=(context["stockCode"],msg[context["stockCode"]].symbolSource , context.tradeTime, 5, price, ,,100,1,,,)
		//print("委托订单")
		Backtest::submitOrder(context.engine, orderMsg,"买入股票",0)
	}
	longPos = Backtest::getPosition(context.engine, context["futuresCode"], "futures").longPosition
	if(longPos<1 and context["futuresCode"] in msg.keys()){
		futuresPrice = msg[context["futuresCode"]].close
		symbolSource = msg[context["futuresCode"]].symbolSource
		orderMsg=(context["futuresCode"],msg[context["futuresCode"]].symbolSource , context.tradeTime, 5, futuresPrice, ,,100,1,,,)
		//print("委托订单")
		Backtest::submitOrder(context.engine, orderMsg,"买入期货",0,"futures")
	}
}
//step 3：配置参数
config = {
    startDate:2000.01.01,
    endDate:2025.12.31,
    strategyGroup: "multiAsset",
    cash: {
        stocks:100000000.,
        futures:100000000.
    },
    dataType:3,
    matchingMode:3,
    frequency:0,
    outputOrderInfo:true,
    multiAssetQuoteUnifiedInput:false,
    depth:5,
    commission: 0.00,
    tax:0.00
}
callbacks = { onBar:onBar,beforeTrading:beforeTrading}
```

### 2.6 JIT优化

DolphinDB 回测引擎从 3.00.2.1 JIT 版本中支持 JIT 优化，只需在创建回测引擎时把
`Backtest::createBacktester` 函数的 *jit* 参数设置为 true 即可。JIT
相关内容可以参考 DolphinDB
回测平台使用和性能优化攻略文档。

## 3. 注意事项

本章将介绍在使用 DolphinDB 回测引擎过程中应关注的重要事项，涵盖事件回调函数参数的说明、行情数据细节、JIT 优化兼容性等内容。

### 3.1 事件回调函数参数说明

* *context* 参数（逻辑上下文）：所有回调函数中的 *context*
  参数是一个字典类型，用于存储策略全局变量及运行状态。引擎会自动维护以下内置变量：
  + context.tradeTime：当前行情的最新时间；
  + context.tradeDate：当前交易日；
  + context.BarTime：当前 Bar 的时间戳（在快照降频为低频行情时）；
  + context.engine：当前回测引擎实例。
* *msg* 参数（行情数据）
  + 在 高频回调函数（如 `onSnapshot`）中，*msg*
    是一个字典，行情字段如最新价可通过 msg.lastPrice 形式获取。
  + 在 低频回调函数（如 `onBar`）中，*msg* 是一个嵌套字典：第一层以标的代码为
    key，行情消息为 value 的字典，每一条行情消息又是一个字典。因此，可以通过 msg[stock].lastPrice
    来获取。
  + 策略订阅指标时，指标 *indicator* 的数据类型需同 *msg* 参数的数据类型保持一致。
  + 在进行多资产联合回测时，*msg* 为字典，key 为资产类型或者 'indicator'，value
    为对应品种的行情表。

### 3.2 行情数据

* 基于沪深交易所中高频逐笔行情进行策略回测时，支持同时回测沪深两个交易所的股票，引擎内部维护两个交易所的模拟撮合引擎，此时行情中的 symbol
  必须带有交易所标识（即以 ".XSHG",".XSHE" 结尾），例如 "600000.XSHG"，否则系统会报错。

### 3.3 基本功能

* 回测结束标志：当引擎接收到 symbol 为 `"END"`
  的消息时，表示策略回测结束，相关回调逻辑可在此时清理状态或输出结果。
* 支持多标的回测：一个回测引擎可以同时支持多只股票的回测，只需要同时回放多只股票的行情即可。
* 并行回测：如果策略想并行回测，可以创建多个回测引擎，在脚本中向多个引擎并发插入数据执行回测。

### 3.4 JIT优化相关说明（从3.00.2版本起支持）

* 推荐使用接口：`Backtest::createBacktester` 是 3.00.2 和 2.00.14
  版本新引入的创建回测引擎接口。我们强烈推荐使用新接口编写回测策略。使用该接口编写的策略代码，可以在 2.00.14 及以上版本，3.00.2
  及以上版本，JIT 版本， 非 JIT 版本跨平台使用。
* 老接口兼容性限制：回测引擎同时支持调用老版本的 `createBacktestEngine` 接口进行创建，但不支持
  JIT 优化技术，该接口支持通过 `msgAsTable=true` 配置，将事件函数中的 *msg*
  参数转换为表格结构完整的参数列表可以参阅回测插件的接口说明文档。
* 开启 JIT 优化时，策略回调函数的实现不能用默认参数和部分应用；策略中的全局变量的定义需要在 *config* 的 *context*配置项中声明；JIT 优化不支持直接对字典嵌套赋值，具体可以参考 DolphinDB 回测平台使用和性能优化攻略中的开启 JIT 优化注意事项。

## 4. 常见问题

### 4.1 执行策略回测时，出现“行情不匹配”报错

通过接口 `Backtest::appendQuotationMsg(engine, msg)` 执行策略回测时报错，通常是由于
msg
的数据结构与策略所配置的行情类型不一致。不同品种或相同品种在不同行情频率下，其行情字段略有差异。建议仔细检查当前行情数据表的字段及其类型是否与相应的行情类型严格匹配。

### 4.2 成交明细中大量拒单或者部分成交订单

* 在使用逐笔行情进行策略回测时，若合成的行情快照持续出现买卖价格倒挂，订单将无法撮合，可能由以下原因导致：
  + **行情数据顺序错误：**当行情数据时间戳相同时，深交所逐笔委托单应先于逐笔成交单，上交所逐笔委托单应在逐笔成交单之后。请根据错误提示检查行情数据的顺序，确保买单、卖单和成交单顺序正确。
  + **行情数据不完整：**如果只输入了当天某一时间段内的行情数据，例如筛选 10:00之后的行情数据，该时间段内的成交单依赖
    10:00 之前的委托单，导致撮合失败。请检查输入的行情数据，确保买单、卖单和成交单数据齐全。
  + **行情数据标的有误**：行情数据有误，".XSHE" 结尾的标的代表深交所股票，".XSHG"
    结尾的标的代表上交所股票。不同交易所的委托单和成交单顺序不同，因此逐笔策略回测时，不同交易所的股票代码必须以相应的交易所代码结尾。
* 在使用快照或中低频行情时，如遇大量未成交或部分成交订单，可考虑以下因素：
  + 与行情的成交量撮合时，默认成交比例为 20%。委托的订单量很大时，可以通过 *matchingRatio*进行调整。
  + 在股票回测中，默认的交易单位为“股”行情中的 volume 字段的单位如果是“万股”或者“手”，请提前处理行情数据。
* 订单的委托数量可能不满足要求，股票买入数量需为 100 的整数倍（68开头的股票，买入时数量需大于等于 200）。
* 可以配置参数 *outputOrderInfo* 为 true，可在订单明细表中增加拒单原因，便于调试。

## 5. 附录

1.1 示例使用的分钟频数据 [barData.csv](../data/quick_start/barData.csv)

2.2 股票快照行情示例代码 [股票快照.dos](../script/quick_start/%E8%82%A1%E7%A5%A8%E5%BF%AB%E7%85%A7.dos)

2.5 多资产回测示例数据及完整代码 [股票与期货策略.dos](../script/quick_start/%E8%82%A1%E7%A5%A8%E4%B8%8E%E6%9C%9F%E8%B4%A7%E7%AD%96%E7%95%A5.dos)
[futureData.csv](../data/quick_start/futureData.csv)
