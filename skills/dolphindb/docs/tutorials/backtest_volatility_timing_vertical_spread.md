<!-- Auto-mirrored from upstream `documentation-main/tutorials/backtest_volatility_timing_vertical_spread.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 回测应用：期权中高频波动率择时价差策略回测

**教程难度**

* 中级

**面向读者**

* 本教程面向已有一定基础的 DophinDB Backtest 回测插件使用者，意在帮助读者进一步学习 DolphinDB Backtest
  回测插件在高频期权回测场景下的灵活用法
* 建议读者首先阅读和掌握以下教程，再阅读本文的内容

  + 多资产回测使用说明及示例

**扩展材料**

* 除了基础 DolphinDB 概念外，本教程还推荐以下扩展阅读以更好理解本案例的代码：

  + DolphinDB
    回测插件使用和性能优化攻略
  + DolphinDB
    回测插件接口说明

在当今高度复杂的金融衍生品市场中，期权及其衍生品策略已成为机构投资者进行精细化风险管理与 alpha 收益创造的重要工具。隐含波动率（Implied Volatility，简称
IV）作为期权定价的核心参数，其短期波动为波动率套利提供了丰富的交易机会。实际场景中可以通过构建期权组合，限制方向性风险，并获得波动率变化带来的稳健收益。

在将此类涉及多腿组合、高频信号计算与动态风控的复杂策略投入实盘之前，利用丰富的历史高频数据对其进行严谨、高效的回测验证，是评估策略有效性与可行性的关键环节。DolphinDB
依托其高性能计算引擎与强大的数据处理能力，成为了中高频策略回测的理想选择。本文将以一个融合波动率择时的期权快照频垂直价差策略为例，详细展示如何利用 DolphinDB
回测插件完成全流程回测。

期权合约本质是一种选择权，使其买方在某个日期或之前以某一价格买入或卖出相对应的资产。期权价格的影响因素包括当前标的价格（S0）、执行价格（K）、期限（T）、标的未来波动率（σ）以及无风险利率（r）。其中，标的的未来波动率（σ）是唯一不可直接观测的变量，这使其成为了期权定价与交易的核心因素。在交易实践中，通常使用Black-Scholes-Merton（BSM
）等定价模型，用市场上的期权报价反推计算隐含波动率，以衡量市场对未来波动率的共识预期。

在实践中，波动率交易者可以通过构建 Delta
中性组合，从波动率的绝对定价错误或相对变化中获利。一个典型的例子是，当交易者认为当前隐含波动率低于预期时，会通过买入跨式价差等方式，构建一个正 Vega
的组合；反之，则会构建一个负 Vega 的组合。

同时，波动率交易者也可以**将波动率状态作为一个关键性的择时因子，融入期权方向性策略的构建之中**。例如，在持有温和看涨观点且隐含波动率偏低时，选择牛市看涨价差策略可以在较低成本下建立方向性头寸，同时限制标的价格下跌带来的损失；反之，在持有温和看跌观点且隐含波动率偏高时，可以通过熊市看跌价差建立方向性头寸，同时限制标的价格上涨带来的损失。

基于上述思路，本文实现了一种**融合波动率择时的垂直价差策略**。**该策略基于对标的资产价格的方向性判断，同时结合当前隐含波动率的状态，构建牛市看涨价差或熊市看跌价差的期权组合。**

中高频量化交易策略回测平台的实现主要包括三个重要环节：行情数据按顺序回放，委托订单撮合，以及策略开发与策略回测绩效评估。而在实现中高频策略回测时往往面临以下几个挑战：

* 海量中高频交易数据对回测引擎的查询与计算性能提出了极高的要求。
* 为确保策略评估和优化的有效性，回测过程中应尽可能模拟实际的交易过程，例如考虑订单能否成交、成交价格、成交量以及市场冲击等因素。
* 回测引擎还应具有灵活的架构，能够支持多种交易策略和技术指标的实现，并且易于扩展，以适应不同的市场和交易需求。

针对上述挑战，DolphinDB
基于其高性能的分布式存储和计算架构，为用户提供了一个易扩展、性能优的中高频量化交易策略回测解决方案。该方案实现了库内行情回放、模拟撮合引擎和事件型中高频回测引擎三大核心组件，支持通过
DLang、Python 或 C++ 语言完成中高频策略的研发和测试。具体来说，该方案涵盖以下三个模块：

* 回放功能：支持将一个或多个不同结构的分布式表中的数据严格按照时间或者按指定多列排序顺序**回放**到流表中，因此可以方便地解决因子计算和量化策略研发中研发和生产一体化的问题。
* 模拟撮合引擎插件：支持沪深交易所 Level-2
  逐笔行情和快照行情，遵循“价格优先、时间优先”的撮合规则，提供高精度撮合能力，并支持多种基于不同行情数据的撮合模式以及丰富的参数配置，用于更真实地模拟实盘交易环境。
* 回测插件：用户可以在其中自定义指标，支持基于逐笔、快照、分钟和日频行情进行策略回测，获取回测的收益、持仓、交易明细等信息。其中基于逐笔和快照行情进行高精度策略回测，可以实现仿真和回测一体化的策略验证。

值得一提的是，这三个模块化解决方案与外部解决方案兼容性良好。即使用户已经实现了某个环节的解决方案，DolphinDB 提供的解决方案也可以与其融合成一个完整的回测方案。

## 1. 基于 DolphinDB 的期权波动率择时价差策略

### 1.1 策略逻辑

本文利用上期所黄金期权一个交易日中日盘的全部数据，基于 DolphinDB Backtest 回测插件实现了期权波动率套利策略，策略的逻辑如下所示：

| 策略参数 | 参数值 |
| --- | --- |
| 开始日期 | 2025.02.17（日盘开始） |
| 结束日期 | 2025.02.17（日盘结束） |
| 回测频率 | 快照频 |
| 初始资金 | 1000000 |
| 回测标的 | 黄金期货主力合约对应的看涨期权 & 看跌期权 |
| 开仓信号 | * **牛市看涨开仓信号（IV 偏低 & 标的价格上升趋势）：**   + 期权 IV < 过去 30 个快照的 IV 均值 - 1.0 \* 标准差   + 期货最新价 MACD > 0，上一个快照的 MACD < 0 * **熊市看跌开仓信号（IV 偏高 & 标的价格下降趋势）：**   + 期权 IV > 过去 30个快照的 IV 均值 + 1.0 \* 标准差   + 期货最新价 MACD < 0，上一个快照的 MACD > 0 |
| 开仓规则 | 实时根据 IV 信号进行期权对市价单双开：   * **牛市看涨价差：做多平值+ 做空虚值二档看涨期权** * **熊市看跌价差：做多平值 + 做空虚值二档看跌期权** |
| 平仓信号 | 实时监控（平值 – 虚值）期权对的价差情况，对该期权对进行市价单双平：  **牛市看涨价差 & 熊市看跌价差：平值 - 虚值价差越大越好**  价差相对初始值变动比例上下界：[-0.03, 0.05] |

### 1.2 盈亏情景

对于当前策略的期权组合盈亏进行情景分析，假设当前的黄金期货价格为 **675 元/g**，此时对应的看涨 / 看跌方向的平值 &
虚值二档期权及其开仓权利金如下所示：

【注：由于平值期权权利金 > 虚值期权权利金，故 C1>C2，C3>C4】

| 情景假设对象 | 名称 | 开仓权利金 |
| --- | --- | --- |
| 平值看涨期权 | AU2503-C-672 | C1 |
| 虚值二档看涨期权 | AU2503-C-688 | C2 |
| 平值看跌期权 | AU2503-P-672 | C3 |
| 虚值二档看跌期权 | AU2503-P-656 | C4 |

#### 1.2.1 牛市看涨价差期权组合

假设当前隐含波动率偏低并且标的当前价格呈现上升态势，触发了牛市看涨价差信号，即做多平值看涨期权 + 做空虚值二档看涨期权。

未来黄金期货价格（St）可能会出现以下三种情况：

1. 大幅下跌（St << 672）
2. 小幅上涨或震荡（672 ≤ St ≤ 688）
3. 大幅上涨（St >> 688）

对于这三种情况，平值看涨期权 & 虚值二档看涨期权以及期权组合的盈亏方向与大小如下表所示：

| 黄金期货 | 平值看涨期权（多单） | 虚值二档看涨期权（空单） | 1 : 1 期权组合 |
| --- | --- | --- | --- |
| 1. 大幅下跌 | 大幅浮亏，期权价值快速衰减  损益：-C1 | 大幅浮盈，期权价值快速衰减  损益：+C2 | 组合浮亏，达到最大亏损，平值-虚值二档期权价差急剧收窄  损益：-（C1 - C2） |
| 2. 小幅上涨 | 浮动盈利：此时 Delta 通常为正（期权价格随标的价格的上升而上升），多头盈利上升  损益：> -C1 | 浮动亏损：此时 Delta 通常为正（期权价格随标的价格的上升而上升），空头盈利下降  损益：< +C2 | **看涨期权：|平值Delta| > |虚值 Delta|，盈亏取决于多单-空单的价差变动：**   * 标的价格上涨时，价差通常扩大，组合浮动盈利 * 标的价格下跌时，价差通常缩小，组合浮动亏损 |
| 3. 大幅上涨 | 深度实值，多头浮盈加速  损益：(St - 672) - C1 | 深度实值，空头浮亏加速  损益：（St - 688）+ C2 | 组合浮盈，达到最大盈利，平值-虚值二档期权价差急剧扩大  损益：（688 - 672）-（C1 - C2） |

#### 1.2.2 熊市看跌价差期权组合

假设当前隐含波动率偏高并且标的当前价格呈现下降态势，触发了熊市看跌价差信号，即做多平值看跌期权 + 做空虚值二档看跌期权。

未来黄金期货价格（St）可能会出现以下三种情况：

1. 大幅下跌（St << 656）
2. 小幅下跌或震荡（656≤ St ≤ 672）
3. 大幅上涨（St >> 672）

对于这三种情况，平值看跌期权 & 虚值二档看跌期权以及期权组合的盈亏方向与大小如下表所示：

| 黄金期货 | 平值看跌期权（多单） | 虚值二档看跌期权（空单） | 1 : 1 期权组合 |
| --- | --- | --- | --- |
| 1. 大幅下跌 | 深度实值，多头浮盈加速  损益：（672 - St）- C3 | 深度实值，空头浮亏加速  损益：（St - 656）+ C4 | 组合浮盈，达到最大盈利，平值-虚值二档期权价差急剧扩大  损益：（672 - 656）-（C3 - C4） |
| 2. 小幅上涨 | 浮动盈利：此时 Delta 通常为负（期权价格随标的价格的上升而下降），多头盈利下跌  损益：> -C3 | 浮动亏损：此时 Delta 通常为负（期权价格随标的价格的上涨而下跌），空头盈利上升  损益：< +C4 | **看跌期权：|平值Delta| > |虚值Delta|，盈亏取决于多单-空单的价差变动：**   * 标的价格下跌时，价差通常扩大，组合浮动盈利 * 标的价格上涨时，价差通常缩小，组合浮动亏损 |
| 3. 大幅上涨 | 大幅浮亏，期权价值快速衰减  损益：-C3 | 大幅浮盈，期权价值快速衰减  损益：+C4 | 组合浮亏，达到最大亏损，平值-虚值二档期权价差急剧缩小  损益：-（C3 - C4） |

#### 1.2.3 盈亏总结

牛市看涨价差与熊市看跌价差两者均通过卖出期权获得权利金收入，以对冲买入期权的开仓成本。这一设计具有两个关键特征：（1）其最大亏损被锁定为期初净支出，当标的价格向不利方向移动时，期权组合的整体损失有限。（2）其最大盈利上限为行权价之差减去净权利金支出。牺牲了盈利方向的无限潜在收益为代价，显著降低了整体策略的盈亏平衡点与减仓成本。

### 1.3 策略结构

DolphinDB Backtest 回测插件中提供了多样的事件化回调函数，包括 onSnapshot（快照回调函数）、onBar（Bar
回调函数）、onTrade（成交回报函数）等，本文主要利用 onSnapshot 快照回调函数，结合 DolphinDB Backtest 回测插件中的
context 状态字典完成快照频期权波动率择时价差策略的开发。

本文在 context 上下文状态变量中一共设计了三个变量：lastTimeDict（每个期货合约的上个时间戳）、longPair &
shortPair（各期货合约对应的牛市 & 熊市价差期权对）以及 longState & shortState（牛市 &
熊市价差期权对及设定的价差上下限），整体策略的实现逻辑如下所示：

![](images/backtest_volatility_timing_vertical_spread/1_1.png)

图 1. 图 1-1：快照频期权波动率择时价差策略结构

#### 1.3.1 获取基本信息

在 DolphinDB Backtest 回测插件的 `onSnapshot`
快照回调函数中，依次有三个入参：上下文状态字典 *context*、快照行情字典 *msg* 与自定义指标
*indicator*。这里首先获取了期权标的维度层面的信息（期权代码、期货合约代码、期权方向、期权档位等），之后取出当天的主力合约列表，过滤非主力合约的相关行情。

```
def onSnapshot(mutable contextInfo, msg, indicator){
    /*快照行情回调函数
    msg数据结构:(一个标的在这个快照上的数据字典)
    symbol->
    symbolSource->
    ...
    indicator数据结构:(一个标的在这个快照上的指标字典)
    ...
    */
    // 获取期权标的维度信息
    ioption = msg.symbol                                // 标的代码
    direction = contextInfo["directionDict"][ioption]   // 期权看涨(1)还是看跌(2)
    contract = contextInfo["contractDict"][ioption]    // 合约代码
    strike = contextInfo["strikePriceDict"][ioption]    // 期权行权价
    // 获取信号信息
    level = msg["signal"][0]                            // 期权挡位
    ivSignal = msg["signal"][1]                         // 期权 IV 信号
    trendSignal = msg["signal"][2]                      // 期货价格 MACD 趋势信号
    // 获取当前时间维度信息
    tradeTime = contextInfo["tradeTime"]
    tradeDate = contextInfo["tradeDate"]
    // 过滤非主力合约
    contractList = contextInfo["mainContractDict"][tradeDate] // 当日主力合约列表
    if (!(contract in contractList)){ // 非主力合约
        return
    }
    ...
}
```

#### 1.3.2 选择期权组合

由于标的期货的最新价格会实时变动，所以需要实时对目标期权的档位进行追踪。为了策略中多品种多合约的可拓展性，这里设计了数据结构为 <String,
Dict<String, List>> 的嵌套字典作为状态变量，外层的 String 为期货合约名称，内层的 String 为期权对名称，List
为一个长度为 2 的字符串列表，其值对应着**[平值期权名称，虚值二档期权名称]**，同一列表中的期权组成一个期权对，在后续的开仓逻辑中，每次会对该期权对执行对应的下单逻辑。

在 `onSnapshot`
回调函数中实时选择目标组合期权对的代码如下：对所有期权都进行判断，若为牛市看涨方向的期权（这里即为平值看涨、虚值二档看涨），则放入 longPair
这一状态变量；反之，若为熊市看跌方向的期权（这里即为平值看跌、虚值二档看跌），则放入 shortPair 这一状态变量。在后续开仓逻辑中，会依据
longPair 与 shortPair 中的期权对进行开仓。

```
ivSignal = msg["signal"][1]  // ivFactor
trendSignal = msg["signal"][2] // trendFactor
// 牛市看涨/熊市看跌信号是否触发 -> 添加至longPair & shortPair
if (ivSignal == 1 and trendSignal == 1){
    // 牛市看涨信号触发 -> 做多平值看涨期权 + 做空虚值二档看涨期权
    if (!(contract in keys(contextInfo["longPair"]))){
        contextInfo["longPair"][contract] = array(STRING, 2)
    }
    if (level == 0 and direction == 1){ // 平值看涨期权
        contextInfo["longPair"][contract][0] = ioption
    }else if (level == -2 and direction == 1){ // 虚值二档看涨期权
        contextInfo["longPair"][contract][1] = ioption
    }
}else if (ivSignal == -1 and trendSignal == -1){
    // 熊市看跌信号触发 -> 做多平值看跌期权 + 做空虚值二档看跌期权
    if (!(contract in keys(contextInfo["shortPair"]))){
        contextInfo["shortPair"][contract] = array(STRING, 2)
    }
    if (level == 0 and direction == 2){ // 平值看跌期权
        contextInfo["shortPair"][contract][0] = ioption
    }else if (level == -2 and direction == 2){ // 虚值二档看跌期权
        contextInfo["shortPair"][contract][1] = ioption
    }
}
```

#### 1.3.3 划分快照截面

由于 DolphinDB Backtest 回测插件中，`onSnapshot`
回调函数是每个标的的每个快照到来时触发一次，这里可以**根据每类标的时间戳的变动时刻，去划分不同的截面，从而实现截面下单的逻辑**。因为注入引擎的数据是已经根据时间戳排序的，故这里每个合约回调的
tradeTime 一定是单调递增的，所以这个逻辑成立。

在 `onSnapshot`
回调函数中划分快照截面的代码如下：同一期货合约截面快照中不同期权此时可以直接结束本次回调；只有当前时间戳不等于上一个时间戳，即进入下一个快照截面的期货合约，此时需要从
context 上下文状态变量拿出对应的状态变量进行平仓 & 开仓操作，继续执行后面的代码逻辑。

```
// 获取当前时间维度信息
... // 所有标的都需要执行的逻辑代码块
tradeTime = contextInfo["tradeTime"]
if (contextInfo["lastTimeDict"][contract]==tradeTime){
    return
}else{ // 下一个截面到来
    contextInfo["lastTimeDict"][contract]=tradeTime.copy()
}
... // 只有触发快照变动时需要执行的逻辑代码块
```

#### 1.3.4 组合平仓下单

基于 2.1
部分的分析，平值-虚值期权的价差在本文构造的期权组合中，对最终的损益起到了至关重要的作用。因而需要实时追踪价差的变化，并在合适时机对期权对进行平仓。

平仓部分的代码段如下（以牛市看涨价差期权对平仓为例）：

```
 if (contract in keys(contextInfo["longState"])){
   // longState 中是做多平值看涨期权 + 做空虚值二档看涨期权 -> 平仓时应为 [平多, 平空]
    for (optPair in keys(contextInfo["longState"][contract])){
        opt1 = optPair.split("$")[0]    // 取出平值看涨期权
        opt2 = optPair.split("$")[1]    // 取出虚值二档看涨期权
        price1 = contextInfo["lastPriceDict"][opt1]
        price2 = contextInfo["lastPriceDict"][opt2]
        state = price1 - price2 // 计算组合最新价差
        stateList = contextInfo["longState"][contract][optPair] // 组合最低价差 & 组合最高价差
        // 判断最新价差是否突破阈值
        if (state<stateList[0] or state>stateList[1]){
            vol1 = Backtest::getPosition(contextInfo["engine"], symbol=opt1)["longPosition"][0]
            // 平值看涨期权多仓
            vol2 = Backtest::getPosition(contextInfo["engine"], symbol=opt2)["shortPosition"][0]
            // 虚值二档看涨期权空仓
            if (isNull(vol1) or isNull(vol2)){
                continue
            }
            if (vol1>0 and vol2>0){
                orderDirection = 3 // 平多
                Backtest::submitOrder(contextInfo["engine"],
                    (opt1, "SHFE", tradeTime, 0, price1, price1, vol1, orderDirection, 0),
                    label="closeLong",orderType=0)
                orderDirection = 4 // 平空
                Backtest::submitOrder(contextInfo["engine"],
                    (opt2, "SHFE", tradeTime, 0, price2, price2, vol2, orderDirection, 0),
                    label="closeShort",orderType=0)
                // 删除价差记录
                contextInfo["longState"][contract].erase!(opt1+"$"+opt2)
                contextInfo["longPair"] = array(STRING, 2)
            }
        }
    }
}
```

#### 1.3.5 组合开仓下单

开仓部分首先利用 `Backtest::getAvailableCash`
函数查看实时可用资金，防止可用资金不足无法下单的情况。之后，根据 longPair 与 shortPair 中的实时牛市价差 &
熊市价差期权对进行下单。需要注意的是，为了防止重复下单，这里需要先利用 `Backtest::getPosition`
函数取出该标的持仓，检查是否有对应方向的持仓。

开仓部分的代码段如下所示（以牛市看涨价差期权对开仓为例）：

```
if (Backtest::getAvailableCash(contextInfo["engine"]) <= 100000){
    return
}
// 牛市看涨价差 -> 做多平值看涨期权 + 做空虚值二档看涨期权
if (contract in keys(contextInfo["longPair"])){
    opt1 = contextInfo["longPair"][contract][0]
    opt2 = contextInfo["longPair"][contract][1]
    vol1 = Backtest::getPosition(contextInfo["engine"], symbol=opt1)["longPosition"][0]
    vol2 = Backtest::getPosition(contextInfo["engine"], symbol=opt2)["shortPosition"][0]
    price1 = contextInfo["lastPriceDict"][opt1]
    price2 = contextInfo["lastPriceDict"][opt2]
    optPair = opt1+"$"+opt2
    if (!isNull(opt1) and !isNull(opt2) and price1!=price2){  // 初始价差不为0
        // 判断当前期权是否持仓
        state = false
        if (!(isNull(vol1))){
            if (vol1 >0){
                state = true
            }
        }
        if (!(isNull(vol2))){
            if (vol2 >0){
                state = true
            }
        }
        if (!state){
            // 开仓1手
            orderDirection = 1 // 平值看涨期权开多
            Backtest::submitOrder(contextInfo["engine"],
                (opt1, "SHFE", tradeTime, 0, price1, price1, 1, orderDirection, 0),
                label="openLong",orderType=0) // 下单(0：市价单)
            orderDirection = 2 // 虚值二档看涨期权开空
            Backtest::submitOrder(contextInfo["engine"],
                (opt2, "SHFE", tradeTime, 0, price2, price2, 1, orderDirection, 0),
                label="openShort",orderType=0) // 下单(0：市价单)
            // 添加价差记录
            if (!(contract in keys(contextInfo["longState"]))){
                contextInfo["longState"][contract] = dict(SYMBOL, ANY)
                // 期权对代码: [最低价差限制, 最高价差限制]
            }
          contextInfo["longState"][contract][optPair] = [
            (price1-price2) * (1-contextInfo["lowLimit"]),
            (price1-price2) * (1+contextInfo["upLimit"])
          ]
        }
    }
}
```

## 2. 回测流程

这里展示了使用 Backtest 插件进行期权中高频回测数据处理的全流程，相关数据结构可参考 DolphinDB Backtest 回测插件官方文档：期权回测所需数据结构。

![](images/backtest_volatility_timing_vertical_spread/2_1.png)

图 2. 图 2-1：利用 Backtest 回测插件进行中高频期权回测的流程

在回测过程中，若合约的交易乘数、费率、保证金 等基本参数发生变更，可以在 `beforeTrading` 盘前回调函数中编写相关逻辑，通过
`Backtest::setSecurityReference`
函数将更新后的基本信息表传入回测引擎，从而使得回测更贴合真实交易场景。

### 2.1 创建回测引擎

回测引擎通过接口 `Backtest::createBacktester` 进行创建，该函数包含以下核心参数：

1. *eventCallbacks*：回调函数字典，用于定义策略在不同事件触发点（如行情更新、撮合结果返回等）下的处理逻辑（详见本教程第2章）；
2. *config*：引擎配置字典，包含策略运行所需的各类参数以及用于维护策略状态的上下文字典 context；
3. *securityReference*：标的基本信息表。

本教程已将清洗完成的期权行情数据 optData 与标的基础信息表 securityReference 分别保存为 CSV
格式文件，并在附件中提供下载。用户可使用 `loadText` 函数加载使用。

创建回测引擎的完整代码如下所示：

```
/* 1. 创建回测引擎 */
// 标的基本信息表
filePath = "/ssd/ssd0/single16coreJIT/server/optionData/" // 需要自行换成DolphinDB所在服务器的csv路径
schemaTb = table(["symbol","underlyingAssetType","multiplier","type","strikePrice","marginRatio","tradeUnit",
                  "priceUnit","priceTick","commission","deliveryCommissionMode","lastTradingDay","exerciseDate",
                  "exerciseSettlementDate","exDate","adjStrikePrice","adjMultiplier"] as `name,
                 ["SYMBOL","INT","DOUBLE","INT","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","INT",
                 "DATE","DATE","DATE","DATE","DOUBLE","DOUBLE"] as `types)
securityReference = loadText(filePath+"optSecurityReference.csv",schema=schemaTb)

// 准备回测配置参数
config = dict(STRING, ANY)
config["startDate"] = startDate // 回测开始日期
config["endDate"] = endDate // 回测结束日期
config["strategyGroup"] = "option" ///策略类型
config["dataType"] = 1 // 行情选择快照行情
config["callbackForSnapshot"] = 0 // 当dataType==1 时生效, 0: 只触发onSnapshot, 1: 触发onSnapshot和onBar, 2: 只触发onBar
config["maintenanceMargin"] = 1.0 // 维持保证金比率
config["cash"] = 1000000
config["enableAlgoOrder"] = true // 开启算法订单
config["outputOrderInfo"] = true // 是否输出拒单原因
config["matchingMode"] = 3
config["latency"] = 50 // 模拟订单延时(ms)
contractDict = dict(securityReference[`symbol], split(securityReference[`symbol],"-")[0])
directionDict = dict(securityReference[`symbol], securityReference[`type])
strikePriceDict = dict(securityReference[`symbol],securityReference[`strikePrice])

// 配置主力合约信息
mainContractDict = dict(DATE,ANY)
mainContractDict[2025.02.17] = ["AU2504"] // 存放每日主力合约列表

// 配置回测参数
config["context"] = {
    // 基本信息部分
    "lastTimeDict": dict(SYMBOL, TIMESTAMP), // {期货名称: 上一个时间戳}
    "contractDict": contractDict,  // {期权名称: 期货合约名称}
    "directionDict": directionDict, // 1为看涨期权, 2为看跌期权
    "strikePriceDict": strikePriceDict, // {期权标的名称: 行权价}
    "mainContractDict": mainContractDict, // {日期: 主力合约列表}

    // 信号部分
    "upLimit": 0.05,  // 当期权价差向盈利方向突破该比例时, 期权对进行双平
    "lowLimit": 0.03,  // 当期权价差向亏损方向突破该比例时, 期权对进行双平
    "longState": dict(SYMBOL, ANY), // {期货:{牛市看涨期权对: [价差下限, 价差上限]}}
    "shortState": dict(SYMBOL, ANY), // {期货:{熊市看跌期权对: [价差下限, 价差上限]}}

    // 下单部分
    "lastPriceDict": dict(SYMBOL, DOUBLE), // 期权最新价格
    "longPair": dict(SYMBOL, ANY), // 多头期权对
    "shortPair": dict(SYMBOL, ANY) // 看跌期权对
}

// 回调函数字典
eventCallBacks = dict(STRING, ANY) // 回调函数字典
eventCallBacks["initialize"] = initialize  // 初始化函数
eventCallBacks["beforeTrading"] = beforeTrading // 每日盘前回调函数
eventCallBacks["onSnapshot"] = onSnapshot // 快照回调函数
eventCallBacks["afterTrading"] = afterTrading // 每日盘后回调函数
eventCallBacks["finalize"] = finalized // 回测结束函数
try{Backtest::dropBacktestEngine(strategyName)}catch(ex){print(ex)}  // 删除已经存在的回测引擎

// 创建回测引擎
engine = Backtest::createBacktester(strategyName, config, eventCallBacks, jit, securityReference)
```

![](images/backtest_volatility_timing_vertical_spread/2_2.png)

图 3. 图 2-2：期权合约基本信息表

### 2.2 执行回测

本节重点介绍策略实现过程中所需的三个核心指标的计算方法，即期权档位、MACD 趋势信号以及 IV 信号，对应于自定义指标列 signal
的构建逻辑。同时，说明如何将包含上述自定义指标的行情数据传入回测引擎，进而执行回测。

**Step1. 读取行情数据**

由于本文策略只涉及主力合约，这里只将主力合约的数据取出：

```
// 获取数据并执行策略回测
schemaTb = table(["symbol","symbolSource","timestamp","tradingDay","lastPrice",
                  "upLimitPrice","downLimitPrice","totalBidQty","totalOfferQty",
                  "bidPrice","bidQty","offerPrice","offerQty","highPrice","lowPrice",
                  "prevClosePrice","prevSettlementPrice","underlyingPrice",
                  "Theta","Vega","Gamma","Delta","IV",
                  "contract","strike","direction"] as `name,
                  ["SYMBOL","SYMBOL","TIMESTAMP","DATE","DOUBLE","DOUBLE","DOUBLE",
                  "LONG","LONG","DOUBLE[]","LONG[]","DOUBLE[]","LONG[]","DOUBLE",
                  "DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE","DOUBLE",
                  "DOUBLE","DOUBLE","SYMBOL","DOUBLE","INT"] as `types)
data = select * from loadText(filePath+"optData.csv",schema=schemaTb)
        where symbol.startsWith("AU2504") // 只取主力合约进行交易
```

![](images/backtest_volatility_timing_vertical_spread/2_3.png)

图 4. 图 2-3：快照频期权行情结构

**Step2. 计算期权档位**

为便于后续策略逻辑的统一调用，在获取期权行情数据后，采用 SQL 向量化计算的方式对期权档位进行预处理。无论是看涨期权还是看跌期权，最终均输出一列 INT
类型的期权档位标识，其中 0 表示平值期权、-k 表示虚值 k 档、k 表示实值 k 档。SQL 期权档位计算代码如下所示：

```
// 获取每小时价差
hourRank = select firstNot(strike)-firstNot(underlyingPrice) as priceDiff from data
           group by contract, tradingDay, direction, symbol, hour(timestamp) as tradeHour
// 一小时截面获取挡位等级
update hourRank set levelRank = iif(direction == 1,
            rank(priceDiff,true), rank(priceDiff,false))
            context by direction, contract, tradingDay, tradeHour
// 一小时截面找到平值期权(价差最接近0的期权)对应的挡位
eqData = select sum(eqRank) as eqRank from (
    select tradingDay, tradeHour, direction, contract,
    iif(abs(priceDiff) == min(abs(priceDiff)), levelRank, 0) as eqRank from hourRank
    context by tradingDay, tradeHour, direction, contract)
    group by tradingDay, tradeHour, direction, contract
hourData = lj(hourRank, eqData, `tradingDay`tradeHour`direction`contract)
update hourData set levelRank = eqRank-levelRank
// 截面排序得到挡位, 预期输出(0:平值期权, -k:虚值期权, +k:实值期权, k表示挡位)

// 拼接回原始行情数据
data = select * from data a left join (
  select contract, tradingDay, direction, symbol, tradeHour, levelRank from hourData) b
        on a.timestamp.hour() == b.tradeHour
        and a.contract == b.contract
        and a.tradingDay == b.tradingDay
        and a.direction == b.direction
        and a.symbol == b.symbol
        order by timestamp asc
```

**Step3. 开仓信号计算**

根据策略设计，当 MACD 由负转正，且 IV 突破 30 根快照均值 + 标准差时，判定为牛市看涨价差开仓信号；当 MACD 由正转负，且 IV 突破 30
根快照均值 - 标准差时，判定为熊市看跌价差开仓信号。以下为 MACD 与 IV 信号的计算代码：

```
/* 计算MACD趋势信号 */
macdFunc = def (lastPrice, short_=24, long_=52, m=18) {
    dif = ewmMean(lastPrice, span=short_, adjust=false) -
    ewmMean(lastPrice, span=long_, adjust=false)
    dea = ewmMean(dif, span=m, adjust=false)
    macd = (dif - dea) * 2
    return round(macd, 4)
}
update data set macd = macdFunc(underlyingPrice).nullFill(0) context by symbol
update data set trendFactor = iif(macd>0 and prev(macd)<0, 1,
                        iif(macd<0 and prev(macd)>0, -1, 0)) context by symbol
/* 计算IV信号 */
update data set ivLongLevel = mavg(IV.ffill(), 30) - mstd(IV.ffill(), 30) context by symbol
update data set ivShortLevel = mavg(IV.ffill(), 30) + mstd(IV.ffill(), 30) context by symbol
update data set ivFactor = iif(IV<ivLongLevel, 1.0, iif(IV>ivShortLevel, -1.0, 0.0)) // IV信号
```

**Step4. 合并注入引擎**

将回测过程中使用到的全部自定义指标，通过 `fixedLengthArrayVector`
函数合并为数组向量格式，作为行情数据的一部分传入回测引擎。

最终，向引擎中注入一条标的为 `"END"` 的数据，结束回测。

```
// 最终注入引擎的数据 = 行情列 + IV & Greeks列 + 信号列
data = select symbol, symbolSource, timestamp, tradingDay, lastPrice, upLimitPrice, downLimitPrice,
          totalBidQty, totalOfferQty, bidPrice, bidQty, offerPrice, offerQty, highPrice, lowPrice,
          prevClosePrice, prevSettlementPrice,
          prevSettlementPrice as settlementPrice,
          underlyingPrice, Theta, Vega, Gamma, Delta, IV,
          fixedLengthArrayVector(double(levelRank),double(ivFactor),double(trendFactor)) as signal
          from data
          order by timestamp asc

timer Backtest::appendQuotationMsg(engine, data) // 注入回测引擎, 执行回测

// 回测结束标志
endSignal = select * from data where timestamp = max(timestamp) limit 1
update endSignal set symbol = "END"
Backtest::appendQuotationMsg(engine, endSignal)
go
```

## 3. 策略评价

### 3.1 策略结果

在整体策略运行完毕之后，可以运行以下函数查看回测整体结果，完整的策略评价函数详见：DolphinDB
回测插件接口说明。

```
// 查看回测结果
contextInfo = Backtest::getContextDict(engine) // 期末context上下文字典
tradeDetails = Backtest::getTradeDetails(engine) // 订单明细表
openOrders = Backtest::getOpenOrders(engine) // 期末未成交订单
totalPosition = Backtest::getPosition(engine)  // 当前持仓
dailyPosition = Backtest::getDailyPosition(engine) // 每日持仓表
enableCash = Backtest::getAvailableCash(engine) // 期末可用资金
dailyPortfolios = Backtest::getDailyTotalPortfolios(engine) // 每天的损益指标
returnSummary = Backtest::getReturnSummary(engine) // 返回一个综合分析结果表
```

这里展示了 tradeDetails（成交订单）的相关结果。从下图中可以看出，该策略的结果符合其策略逻辑：

* 在触发了牛市看涨价差信号后，9 点 30 分 25 秒，AU2504-P-672 & AU2504-P-656 这一期权对成交，此时价差为
  11.58 - 5.68 = 5.9；
* 9 点 51 分 06 秒，AU2504-P-672 & AU2504-P-656 这一期权对价差下跌至 11.1 - 5.4 =
  5.7，触发了价差变动幅度下限，因而此时期权对双平。

![](images/backtest_volatility_timing_vertical_spread/3_1.png)

图 5. 图 3-1：策略成交订单信息

### 3.2 策略性能

DolphinDB Backtest 回测插件支持开启 JIT 优化，以提升回测性能。通过
`Backtest::createBacktester` 创建回测引擎时，将 *jit* 参数设置为
true，即可开启 JIT 优化。本文分别对比了开启/不开启 JIT 优化后，使用相同参数和相同数据回测的性能，测试结果如下所示：

|  | 注入引擎数据条数 | 成交订单数 | 回测耗时 | 处理速率（条/s） |
| --- | --- | --- | --- | --- |
| 不开启 JIT 优化 | 283177 | 38 | 2.39 s | 118484 |
| 开启 JIT | 283177 | 38 | 1.51 s | 187534 |

从上表结果中可以看出，无论是否开启 JIT 优化，Backtest 回测插件的行情处理速率均 **> 10w条/s**，开启 JIT 相比不开启 JIT
的**性能提升了 50% 以上**。

* **JIT 功能注意事项：**

1. DolphinDB Backtest 回测插件只在 3.00.2 以上版本的 DolphinDB Server 下支持开启 JIT 优化。
2. 若在回测插件中开启 JIT 优化功能，则在部分情况下需要调整输入引擎的数据结构，详见官网相关数据结构说明部分 Backtest。
3. 在开启 JIT 优化之后，在回调函数中不能够使用表这一数据结构，需要转换为字典进行处理。

### 3.3 测试环境配置

安装 DolphinDB server，配置为集群模式。本次测试所涉及到的硬件环境和软件环境如下：

* **硬件环境**

  | 硬件名称 | 配置信息 |
  | --- | --- |
  | 内核 | 3.10.0-1160.88.1.el7.x86\_64 |
  | CPU | Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz |
  | 内存 | 512 GB |

* **软件环境**

  | 软件名称 | 版本及配置信息 |
  | --- | --- |
  | 操作系统 | CentOS Linux 7 (Core) |
  | DolphinDB | server 版本：3.00.4 2025.09.09 LINUX\_JIT x86\_64 |
  | license 限制：16 核 128 GB |

## 4. 总结

本文利用 DolphinDB Backtest
回测插件实现了一种融合了波动率择时的期权价差快照频策略，并对中高频期权策略的回测全流程进行了梳理，给出了计算期权档位、交易信号的相关 SQL
脚本。该策略的核心逻辑为根据当前期货标的价格走势与期权隐含波动率水平，通过牛市看涨价差与熊市看跌价差期权组合，以较低成本建立方向性头寸，并实时监控期权对价差变动状况以实现止盈止损平仓。

该场景体现了 Backtest 回测插件优异的性能、丰富的策略触发机制以及全面的回测评价结果，能够为 FICC 领域的中高频交易策略回测提供一定借鉴。

## 5. 常见问题（FAQ）

### 5.1 Csmar 数据源如何匹配 DolphinDB Backtest 回测插件所需数据格式？

为了方便回测数据的获取，这里给出了 Csmar 数据源进行数据格式转换为 DolphinDB Backtest 所需数据源的转换代码并封装为函数便于调用：

```
/* 1. 配置信息 */
dbName = "dfs://OptBackTest"
tbName = "csmar"
csmTAQDB = "dfs://Csmar_Futures_TAQ"
csmTAQTB = "TAQ"
csmMetricDB = "dfs://Csmar_Futures_TAQ"
csmMetricTB = "TAQ_Metrics"
startDate = 2025.02.17 // 开始日期
endDate = 2025.02.17 // 结束日期
targetProduct = "AU"
dateList = getMarketCalendar("CFFEX", startDate, endDate) // DolphinDB 交易日历获取区间所有交易日

/* 2. 转换函数 */
def initOptDB(dbName, tbName, dropDB, dropTB){
    /* 初始化Csmar数据库
    dbName: 希望创建的数据库名称
    tbName: 希望创建的表名称
    dropDB: 是否删除已存在的数据库
    dropTB: 是否删除已存在的表
    */
    if (dropDB){
        try {dropDatabase(dbName)}
        catch(ex){print ex}
    };
    if (dropTB){
        try {dropTable(database(dbName), tbName)}
        catch(ex){print ex}
    }
    // 建库语句
    if (!existsDatabase(dbName)){
        db1 = database(, VALUE, 2021.01.01..2030.12.31, engine="OLAP")
        db2 = database(,HASH,[SYMBOL,30], engine="OLAP")
        db = database(dbName, COMPO, [db1, db2], engine="TSDB")
    }
    // 建表语句
    if (!existsTable(dbName, tbName)){
        colNames = ["symbol","symbolSource","timestamp","tradingDay","lastPrice","upLimitPrice","downLimitPrice","totalBidQty","totalOfferQty",
               "bidPrice","bidQty","offerPrice","offerQty","highPrice","lowPrice","prevClosePrice","prevSettlementPrice","underlyingPrice",
                "Theta","Vega","Gamma","Delta","IV",
                "contract","strike","direction"]
        colTypes = [SYMBOL,SYMBOL,TIMESTAMP,DATE,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,
                    DOUBLE[],LONG[],DOUBLE[],LONG[],DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,
                    DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,
                    SYMBOL,DOUBLE,INT]
        schemaTb = table(1:0, colNames, colTypes)
        tb = database(dbName).createPartitionedTable(schemaTb, tbName, partitionColumns=`tradingDay`contract, sortColumns=`symbol, keepDuplicates=ALL)
    }
}
def addOptData(csmTAQDB, csmTAQTB, csmMetricDB, csmMetricTB, dbName, tbName, ts, targetProduct){
    /*
    每日快照Csmar期权数据处理
    csmTAQDB: csmar TAQ数据库
    csmTAQTB: csmar TAQ表
    csmMetricDB: csmar Metric数据库
    csmMetricTB: csmar Metric表
    dbName: 目标数据库名称(由initOptDB函数创建)
    tbName: 目标表名称
    targetProduct: 目标品种
    ts: 日期
    */

    //上传数据的函数
    InsertData = def (DBName, TBName, data, batchsize){
        // 预防Out of Memory，分批插入数据，batchsize为每次数据的记录数
        start_idx = 0
        end_idx = batchsize
        krow = rows(data)
        do{
            slice_data = data[start_idx:min(end_idx,krow),]
            if (rows(slice_data)>0){
                loadTable(DBName, TBName).append!(slice_data)
            }
            start_idx = start_idx + batchsize
            end_idx = end_idx + batchsize
        }while(start_idx < krow)
    }

    // 从Csmars TAQ表中取出期权行情
    optData = select Symbol as symbol, Market as symbolSource, TradingTime as timestamp, TradingDate as tradingDay,
                LastPrice as lastPrice, // 最新价
                PriceUpLimit as upLimitPrice, // 涨停价
                PriceDownLimit as downLimitPrice, // 跌停价
                long(100) as totalBidQty, // 区间成交买数量
                long(100) as totalOfferQty, // 区间成交卖数量
                BuyPrice as bidPrice, // 委托买价
                long(BuyVolume) as bidQty,  // 委托买量
                SellPrice as offerPrice, // 委托卖价
                long(SellVolume) as offerQty, // 委托卖量
                Highprice as highPrice, // 最高价
                Lowprice as lowPrice, // 最低价
                PreClosePrice as prevClosePrice, // 前收盘价
                PreSettlePrice as prevSettlementPrice,
                Delta,Gamma,Theta,Vega // Greeks
             from loadTable(csmTAQDB, csmTAQTB)
             where TradingDate == ts and strlen(Symbol)>=7 and Symbol.startsWith(targetProduct) // 筛选出当天期权数据
             order by TradingTime

    // IV数据 + 期货行情数据
    futData =  select Symbol as symbol, TradingTime as timestamp, TradingDate as tradingDay,
                    futu_LastPrice as underlyingPrice, // 期货最新价格
                    ImpliedVolatility as IV // IV
                from loadTable(csmMetricDB, csmMetricTB)
                where TradingDate == ts and strlen(Symbol)>=7 and Symbol.startsWith(targetProduct)
                order by TradingTime

    // as of Join 后得到完整行情数据
    data =  select symbol, symbolSource, timestamp, tradingDay, lastPrice, upLimitPrice, downLimitPrice,
                       totalBidQty, totalOfferQty, bidPrice, bidQty, offerPrice, offerQty, highPrice, lowPrice,
                       prevClosePrice, prevSettlementPrice,
                       underlyingPrice, Theta, Vega, Gamma, Delta, IV,
                       split(symbol, "-")[0] as contract,
                       double(split(symbol,"-")[2]) as strike, // 行权价提取
                       iif(split(symbol,"-")[1] =="C", 1, 2) as direction  // 1为看涨, 2为看跌
                from aj(optData, futData, `symbol`tradingDay`timestamp)
                order by tradingDay,timestamp
    InsertData(dbName, tbName, data, 1000000)
}

/* 3. 调用函数完成数据库初始化 + Csmar 期权数据->转换为DolphinDB回测插件所需格式 -> 入库 */
initOptDB(dbName, tbName, dropDB=false, dropTB=true)
for (date in dateList){
    addOptData(csmTAQDB, csmTAQTB, csmMetricDB, csmMetricTB, dbName, tbName, date, targetProduct)
}
```

运行上述代码后，可以看到系统已成功创建名为 `dfs://OptBackTest` 的分布式数据库，并在该数据库下生成了一张名为
`csmar` 的数据表。后续可直接取出表中数据用于 DolphinDB Backtest 回测引擎的注入：

![](images/backtest_volatility_timing_vertical_spread/5_1.png)

图 6. 图 5-1：可直接用于注入 DolphinDB Backtest 回测引擎的数据

### 5.2 长时间段回测如何处理换月逻辑？

由于本文所选取的时间较短，在长时间的策略回测中会涉及换月逻辑，用户可以按照以下方式进行处理：

* 若回测的标的为金融期权，此时近月合约就是主力合约。则可以在 context
  上下文字典中添加一个内存表，包含每个品种-每个合约-剩余到期日，在策略中根据剩余到期日（如 Csmar 数据源中的 tenor
  字段）确定当前主力合约。同时在取数时，为了兼顾策略整体性能与准确性，**在换月的交易日当天需要将被换月的合约行情一同取出注入引擎，以便执行换月平仓的相关逻辑，剩余时间只取主力合约行情注入引擎注入引擎回测即可**。
* 若回测标的为商品期权，则可以根据教程基于期货快照行情数据计算合约 K
  线以及主连行情，确定每日的主力合约，或根据已有的主力合约表进行取数。取数逻辑同金融期权。

## 附录

* 回测脚本：[回测脚本.dos](https://cdn.dolphindb.cn/zh/tutorials/script/backtest_volatility_timing_vertical_spread/%E5%9B%9E%E6%B5%8B%E8%84%9A%E6%9C%AC.dos)
* 所有数据：[data.zip](https://cdn.dolphindb.cn/zh/tutorials/data/backtest_volatility_timing_vertical_spread/data.zip)
