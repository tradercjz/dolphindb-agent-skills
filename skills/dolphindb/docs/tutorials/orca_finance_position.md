<!-- Auto-mirrored from upstream `documentation-main/tutorials/orca_finance_position.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Orca 声明式 DStream API 应用：账户持仓损益实时监控

在日益复杂的金融市场中，投资者需要及时了解所持投资组合的盈亏变化情况，以调整投资策略，规避风险。本文主要介绍如何利用 DolphinDB 的 Orca 声明式 Dstream
API 来实现逐笔交易流数据表和快照流数据表的双流关联，以实时监控资产持仓损益情况。

本教程在附录中提供了完整代码和样例数据，以便用户能够跟随本文实操练习。代码已在 DolphinDB 3.00.4 上验证通过。此外，若初次使用 Dstream API
，也欢迎阅读教程 Orca 声明式 DStream API
应用：实时计算日累计逐单资金流 中的前两章，这里通过一个简单的入门案例，介绍了 Orca 流计算作业的关键组成部分与编写流程。

## 1. 应用场景描述

在当今高速运转、高度互联的全球金融市场中，市场波动频繁且剧烈，价格信息以毫秒级速度刷新。投资者管理着日益复杂的投资组合，涵盖股票、期货、期权、外汇乃至加密货币等多种资产类别。在这种环境下，实时、准确地掌握投资组合的盈亏状况，不再是一种“锦上添花”的能力，而是进行有效风险管理、及时调整策略、把握交易机会和满足合规要求的刚性需求。分钟级甚至小时级的损益延迟，可能导致重大的机会成本或未察觉的风险暴露。

然而，实现高效的多资产实时损益监控面临着诸多挑战：

* 海量行情数据流：需要每秒处理数十万乃至数百万条行情更新。
* 计算复杂度高：损益计算涉及当前持仓、实时最新价、成本基准、潜在的外汇换算以及衍生品的复杂定价模型。
* 极致的低延迟要求：业务决策依赖秒级甚至亚秒级的损益更新。
* 系统扩展与维护困难：传统基于关系型数据库的批处理方案或拼接多个组件的架构，往往在性能、延迟和扩展性上力不从心，且开发和维护成本高昂。

DolphinDB 推出的 企业级实时计算平台 Orca
特别适合于这种吞吐量大、时延要求高、复杂实时分析的业务场景。一方面，Orca 声明式 Dstream API
为用户提供了更加简洁的接口设计。它以声明式编程范式为核心，允许用户通过描述“做什么”而非“如何做”的方式，来定义流数据的处理逻辑，从而降低流处理应用的开发门槛。另一方面，Orca
提供的任务自动调度、计算高可用等能力，保证了计算任务不遗漏任何数据，在提升系统稳定性的同时，大大降低了开发和运维成本。

## 2. 实现方案

本文主要实现账户层级下各标的持仓损益的实时监控。数据处理方案大致可以分为两个阶段：

* 第一阶段是数据预处理，用流数据关联引擎将委托成交数据表与持仓信息表、行情快照数据表进行关联，生成一张信息丰富的宽表，用于后续业务指标计算。
* 第二阶段是持仓监控指标的计算，利用响应式状态引擎计算自定义的十余个持仓监控指标。用户也可以在在此框架上添加个性化的指标。

本文将使用从 DolphinDB 分布式数据库表中回放历史数据的方式，模拟实时数据写入。在实际应用中，实时数据流可以由消息中间件插件（如 Pulsar、Kafka
插件等）、行情插件（如 AMD、Insight 插件等）或者 API （如 C++ 、 Java API 等）写入 DolphinDB 流数据表中。

计算结果可以由外部 API 订阅或者查询，也可以由消息中间件插件等工具发送到外部。本文将使用 DolphinDB
自带的数据面板（Dashboard）完成数据可视化，实时展示监控结果。 具体效果见本文 5.3 小节。

具体的流程框架如下图所示：

![](images/orca_finance_position/2_1.png)

图 1. 图2-1 数据处理流程图

## 3. 数据与指标说明

本文使用的委托成交数据表、静态持仓信息表和行情快照数据均存储在 DolphinDB
分布式数据库中。我们将通过回放功能，模拟实际业务场景中委托成交数据流和行情快照数据流源源不断写入 DolphinDB 流数据表的过程。

样例数据及其导入代码均可以在附录中下载。样例数据为半个交易日的模拟数据，委托成交数据表模拟了 5 个账户所持有的 20 支标的委托成交流水记录；持仓信息表模拟了当日开盘时
5 个账户所持的每支标的的持仓信息；行情快照数据包括 20 支标的的 L2 快照数据。

### 3.1 数据结构

具体数据结构如下所示：

* 持仓信息表：

  | 列名 | 类型 | 备注 |
  | --- | --- | --- |
  | AccountID | SYMBOL | 账户代码 |
  | SecurityID | SYMBOL | 证券代码 |
  | Date | DATE | 日期 |
  | SecurityName | STRING | 证券名称 |
  | Threshold | INT | 阈值数量 |
  | OpenVolume | INT | 期初数量 |
  | PreVolume | INT | 盘前持仓 |
  | PreClose | DOUBLE | 昨收价 |

* 委托和成交数据表：

| 列名 | 类型 | 备注 |
| --- | --- | --- |
| AccountID | SYMBOL | 账户代码 |
| Type | INT | 委托为1，成交为2 |
| OrderNo | INT | 委托编号 |
| SecurityID | SYMBOL | 证券代码 |
| Date | DATE | 日期 |
| Time | TIME | 时间 |
| BSFlag | SYMBOL | 方向 |
| Price | DOUBLE | 价格 |
| Volume | INT | 数量 |
| TradeNo | INT | 成交编号 |
| State | SYMBOL | 状态：全部成交、部分成交、撤单成交 |
| Mark | INT | 方向标记   * 全部成交：-1 * 部分成交：1 * 撤单成交：0 |
| NetVolume | INT | 净买入 |
| CumSellVol | INT | 累计卖出股数 |
| CumBuyVol | INT | 累计买入股数 |
| SellPrice | DOUBLE | 卖出均价 |
| BuyPrice | DOUBLE | 买入均价 |
| ReceivedTime | NANOTIMESTAMP | 数据接收时刻 |

* 行情快照数据表：

| 列名 | 类型 | 备注 |
| --- | --- | --- |
| SecurityID | SYMBOL | 证券代码 |
| Date | DATE | 日期 |
| Time | TIME | 时间 |
| LastPx | DOUBLE | 最新价 |

### 3.2 监控指标计算规则

本文在持仓监控指标的计算中自定义了一系列指标，其具体含义和代码实现如下所示。需要注意的是，在流计算引擎中使用自定义函数计算指标时，需在定义前添加声明
`@state`。

**CanceledVolume**：撤单的委托数量

* 公式：

![](images/orca_finance_position/formula1.png)

其中 TolVolumei 表示委托 i 的初始委托股数，CumVolumei 表示委托 i 的成交数量。

* 代码实现：

```
@state
def calCanceledVolume(Mark, Type, Volume){
    return iif(Mark != 0, NULL, cumfirstNot(iif(Type==1, Volume, NULL)).nullFill!(0)-cumsum(iif(Mark in [-1, 1], Volume, 0)))
}
```

**PositionVolume**：实时持仓数量

* 公式：

![](images/orca_finance_position/formula2.png)

* 代码实现：

```
@state
def calPositionVolume(Type, PreVolume, CumBuyVol, CumSellVol){
    positionVolume = iif(Type==2, PreVolume+CumBuyVol-CumSellVol, ffill(PreVolume+CumBuyVol-CumSellVol))
    return iif(isNull(positionVolume), PreVolume, positionVolume)
}
```

**ThresholdDeviation**：阈值偏离度

* 公式：

![](images/orca_finance_position/formula3.png)

* 代码实现：

```
@state
def calThresholdDeviation(Type, PreVolume, CumBuyVol, CumSellVol, Threshold){
    thresholdDeviation = iif(Threshold>0 and calPositionVolume(Type, PreVolume, CumBuyVol, CumSellVol)>0, (calPositionVolume(Type, PreVolume, CumBuyVol, CumSellVol)-Threshold)\Threshold, 0)
    return round(thresholdDeviation, 6)
}
```

**PositionDeviation**：持仓偏离度

* 公式：

![](images/orca_finance_position/formula4.png)

* 代码实现：

```
@state
def calPositionDeviation(Type, OpenVolume, PreVolume, CumBuyVol, CumSellVol){
	positionDeviation = iif(OpenVolume>0 and calPositionVolume(Type, PreVolume, CumBuyVol, CumSellVol)>0, calPositionVolume(Type, PreVolume, CumBuyVol, CumSellVol)\OpenVolume-1, 1)
	return round(positionDeviation, 6)
}
```

**BuyVolume**：当日买入数量

* 公式：

![](images/orca_finance_position/formula5.png)

* 代码实现：

```
@state
def calBuyVolume(Type, CumBuyVol){
    buyVolume = iif(Type==2, CumBuyVol, ffill(CumBuyVol))
    return iif(isNull(buyVolume), 0, buyVolume)
}
```

**BuyPrice**：当日买入均价

* 公式：

![](images/orca_finance_position/formula6.png)

其中，n 表示当天到当前时刻为止的成交买单数量，Pricei 和 Volumei 分别表示买单 i
的成交价格和成交数量。

* 代码实现：

```
@state
def calBuyPrice(Type, BSFlag, CumBuyVol, BuyPrice){
    buyPrice = cumsum(iif(isNull(prev(deltas(ffill(CumBuyVol)))) and CumBuyVol!=NULL, BuyPrice*CumBuyVol, ffill(BuyPrice)*deltas(ffill(CumBuyVol))))\ffill(CumBuyVol)
    return round(iif(isNull(buyPrice), 0, buyPrice), 6)
}
```

**SellVolume**：当日卖出数量

* 公式：

![](images/orca_finance_position/formula7.png)

* 代码实现：

```
@state
def calSellVolume(Type, CumSellVol){
    sellVolume = iif(Type==2, CumSellVol, ffill(CumSellVol))
    return iif(isNull(sellVolume), 0, sellVolume)
}
```

**SellPrice**：当日卖出均价

* 公式：

![](images/orca_finance_position/formula8.png)

其中，m 表示当天到当前时刻为止的成交卖单数量，Pricej 和 Volumej 分别表示卖单 j
的成交价格和成交数量。

* 代码实现：

```
@state
def calSellPrice(Type, BSFlag, CumSellVol, SellPrice){
    sellPrice = cumsum(iif(isNull(prev(deltas(ffill(CumSellVol)))) and CumSellVol!=NULL, SellPrice*CumSellVol, ffill(SellPrice)*deltas(ffill(CumSellVol))))\ffill(CumSellVol)
    return round(iif(isNull(sellPrice), 0, sellPrice), 6)
}
```

**NetBuyVolume**：当日净买入数量

* 公式：

![](images/orca_finance_position/formula9.png)

* 代码实现：

```
@state
def calNetBuyVolume(NetVolume){
    netBuyVolum = ffill(NetVolume)
    return iif(isNull(netBuyVolum), 0, netBuyVolum)
}
```

**FreezeVolume**：冻结持仓

* 公式：

![](images/orca_finance_position/formula11.png)

其中 CanceledVolumesi 表示卖单 i 中撤单的委托数量。

* 代码实现：

```
@state
def calFreezeVolume(VOLUME, BSFlag, Mark, Type){
	return cumsum(iif(BSFlag=="B", 0, iif(Mark==0, -calCanceledVolume(Mark, Type, VOLUME), iif(Mark in [1, -1], -VOLUME, VOLUME))))
}
```

**AvailableVolume**：可用持仓

* 公式：

![](images/orca_finance_position/formula12.png)

* 代码实现：

```
@state
def calAvailableVolume(Type, PreVolume, CumBuyVol, CumSellVol, VOLUME, BSFlag, Mark){
	availableVolume = PreVolume-calSellVolume(Type, CumSellVol)-calFreezeVolume(VOLUME, BSFlag, Mark, Type)
	return  availableVolume
}
```

**AvailableVolumeRatio**：可用持仓比例

* 公式：

![](images/orca_finance_position/formula13.png)

* 代码实现：

```
@state
def calAvailableVolumeRatio(Type, PreVolume, CumBuyVol, CumSellVol, VOLUME, BSFlag, Mark){
	availableVolumeRatio = calAvailableVolume(Type, PreVolume, CumBuyVol, CumSellVol, VOLUME, BSFlag, Mark)\PreVolume
	return round(iif(isNull(availableVolumeRatio), 0, availableVolumeRatio), 6)
}
```

**Profit**：当日盈亏

* 公式：

![](images/orca_finance_position/formula14.png)

* 代码实现：

```
@state
def calProfit(Type, PreVolume, BSFlag, SellPrice, BuyPrice, CumSellVol, CumBuyVol, LastPx, PreClose){
    profit = (PreVolume-calSellVolume(Type, CumSellVol))*(LastPx-PreClose)+calSellVolume(Type, CumSellVol)*(calSellPrice(Type, BSFlag, CumSellVol, SellPrice)-PreClose)+calBuyVolume(Type, CumBuyVol)*(LastPx-calBuyPrice(Type, BSFlag, CumBuyVol, BuyPrice))
    return round(profit, 6)
}
```

## 4. 持仓监控代码实现

本章首先介绍使用 DStream API 构建持仓监控指标实时计算任务的具体代码，随后提供数据回放代码，以模拟实时计算任务的数据输入。完整代码见附录。

### 4.1 构建流图

本小节将分步构建流图实现持仓监控指标的实时计算。

#### (1) 创建数据目录和流图

首先，创建名为 positionMonitorDemo 的数据目录，然后在 positionMonitorDemo 下创建流图
positionMonitor。代码如下：

```
// 创建数据目录
if (!existsCatalog("positionMonitorDemo")) {
	createCatalog("positionMonitorDemo")
}
go

// 创建流图
use catalog positionMonitorDemo
try { dropStreamGraph("positionMonitor") } catch (ex) {}
positionMonitorGraph = createStreamGraph("positionMonitor")
```

#### (2) 创建流数据表

创建流图后，在流图中定义数据源。代码如下：

```
// 委托和成交原始数据表
colNameMarketData = `AccountID`Type`OrderNo`SecurityID`Date`Time`BSFlag`Price`Volume`TradeNo`State`Mark`NetVolume`CumSellVol`CumBuyVol`SellPrice`BuyPrice`ReceivedTime
colTypeMarketData = `SYMBOL`INT`INT`SYMBOL`DATE`TIME`SYMBOL`DOUBLE`INT`INT`SYMBOL`INT`INT`INT`INT`DOUBLE`DOUBLE`NANOTIMESTAMP
MarketDataStream = positionMonitorGraph.source("MarketDataStream", colNameMarketData, colTypeMarketData).parallelize("AccountID", 2)
// 持仓监控基础信息表
colNamePositionInfo = `AccountID`SecurityID`Date`SecurityName`Threshold`OpenVolume`PreVolume`PreClose
colTypePositionInfo = `SYMBOL`STRING`DATE`STRING`INT`INT`INT`DOUBLE
PositionInfo = positionMonitorGraph.source("PositionInfo", colNamePositionInfo, colTypePositionInfo)
// 行情快照数据表
colNameSnapshot = `SecurityID`Date`Time`LastPx
colTypeSnapshot = `SYMBOL`DATE`TIME`DOUBLE
SnapshotStream = positionMonitorGraph.source("SnapshotStream", colNameSnapshot, colTypeSnapshot)
```

使用 `StreamGraph::source` 方法定义持久化共享流数据表作为数据源。由于委托成交数据量庞大，可以使用
`DStream::parallelize` 方法，根据 AccountID
对委托成交数据进行哈希分区，生成多个并行的分支，提高数据处理的效率。

#### (3) 关联委托成交数据与基础信息表

为了计算持仓监控指标，需要将委托成交数据与持仓基础信息表进行连接，以获取必要的持仓历史信息。具体代码如下：

```
// 关联持仓监控基础信息表
marketJoinPositionInfo = MarketDataStream.lookupJoinEngine(
    rightStream = PositionInfo,
    metrics = [
        <Type>, <OrderNo>, <Date>, <Time>, <BSFlag>, <Price>,
        <Volume>, <TradeNo>, <State>, <Mark>, <NetVolume>, <CumSellVol>,
        <CumBuyVol>, <SellPrice>, <BuyPrice>, <ReceivedTime>, <SecurityName>,
        <Threshold>, <OpenVolume>, <PreVolume>, <PreClose>
    	],
    matchingColumn = `AccountID`SecurityID,
    rightTimeColumn = `Date
    )
```

运用 `DStream::lookupJoinEngine`
方法可以在流图中创建关联引擎。其中，*matchingColumn* 指定了左表和右表的连接列，*rightTimeColumn*指定了右表的时间列。

#### (4) 关联行情快照数据

为了计算实时持仓损益情况，需要实时获取价格行情信息。通过以下代码可以将委托成交数据与行情快照数据进行连接：

```
// 每一笔成交相应关联 snapshot 获取市场最新的价格
marketJoinSnapshot = marketJoinPositionInfo.lookupJoinEngine(
	rightStream = SnapshotStream,
	metrics = [
		<AccountID>, <Type>, <OrderNo>, <Date>, <Time>, <BSFlag>, <Price>,
        <Volume>, <TradeNo>, <State>, <Mark>, <NetVolume>, <CumSellVol>,
        <CumBuyVol>, <SellPrice>, <BuyPrice>, <ReceivedTime>, <SecurityName>,
        <Threshold>, <OpenVolume>, <PreVolume>, <PreClose>, <LastPx>
		],
	matchingColumn = `SecurityID,
	rightTimeColumn = `Date
	)
```

通过再次使用 `DStream::lookupJoinEngine`
创建关联引擎，将响应式状态引擎输出的数据与行情快照数据进行关联。当委托成交数据更新时，新的记录将通过关联引擎来获取行情快照数据中相应的最新价格。

#### (5) 计算监控指标

完成流数据的关联后，使用以下代码来计算持仓监控指标：

```
// 实时计算监控指标
metrics = [<ReceivedTime>, <Date>, <Time>, <SecurityName>
	, <calPositionVolume(Type, PreVolume, CumBuyVol, CumSellVol) as `PositionVolume>
	, <Threshold>
	, <calThresholdDeviation(Type, PreVolume, CumBuyVol, CumSellVol, Threshold) as `ThresholdDeviation>
	, <OpenVolume>
	, <calPositionDeviation(Type, OpenVolume, PreVolume, CumBuyVol, CumSellVol) as `PositionDeviation>
	, <PreClose>, < PreVolume>
	, <calBuyVolume(Type, CumBuyVol) as `BuyVolume>
	, <calBuyPrice(Type, BSFlag, CumBuyVol, BuyPrice) as `BuyPrice>
	, <calSellVolume(Type, CumSellVol) as `SellVolume>
	, <calSellPrice(Type, BSFlag, CumSellVol, SellPrice) as `SellPrice>
	, <calNetBuyVolume(NetVolume) as `NetBuyVolume>
	, <calAvailableVolume(Type, PreVolume, CumBuyVol, CumSellVol, Volume, BSFlag, Mark) as `AvailableVolume>
	, <calAvailableVolumeRatio(Type, PreVolume, CumBuyVol, CumSellVol, Volume, BSFlag, Mark) as `AvailableVolumeRatio>
	, <calFreezeVolume(Volume, BSFlag, Mark, Type) as `FreezeVolume>
	, <LastPx>
	, <calProfit(Type, PreVolume, BSFlag, SellPrice, BuyPrice, CumSellVol, CumBuyVol, LastPx, PreClose) as `Profit>
	, <now(true) as UpdateTime>
    ]
positionMonitor = marketJoinSnapshot.reactiveStateEngine(
	metrics=metrics,
	keyColumn=`AccountID`SecurityID,
	keepOrder=true)
	.sync()
	.sink("PositionMonitorStream")
```

在响应式状态引擎中调用之前定义的监控指标计算函数，按账户号和标的分组来计算监控指标。响应式状态引擎在每接收一条输入数据时都会触发一条结果输出，且针对生产业务中的常见状态函数（滑动窗口函数、累积函数、序列相关函数和
topN 相关函数等）进行增量计算优化，大幅提升了这些函数在响应式状态引擎中的计算效率。`DStream::sync`
用于汇合并行计算路径，必须与 `DStream::parallelize` 方法一起调用。完成所有计算，使用
`DStream::sink` 方法将流数据输出至持久化共享流数据表。

#### (6) 提交流图

最后，使用 `StreamGraph::submit` 方法来提交流图。注意，直到流图调用
`submit` 方法，才真正地提交了这个流计算作业，如果没有调用 `submit`
方法，流图将无法启动。代码如下所示：

```
// 提交流图
positionMonitorGraph.submit()
```

### 4.2 数据回放

由于持仓基础信息表是静态数据，因此可以在每日开盘前调用 `appendOrcaStreamTable` 方法来批量插入数据。

为模拟委托成交数据和行情快照数据的实时传入，本教程使用 `useOrcaStreamTable` 函数将模拟数据传入 Orca
流表。`useOrcaStreamTable` 函数通过 Orca
流表名称定位其所在节点，并在该节点获取流表对象。随后将该流表作为首个参数传递给用户指定的函数并执行。具体代码如下：

```
// 开盘前写入静态持仓基础信息
positionInfo = select * from loadTable("dfs://positionMonitorData", "positionInfo")
appendOrcaStreamTable("PositionInfo", positionInfo)
// 数据回放模拟实时数据写入
// 回放委托成交数据
useOrcaStreamTable("MarketDataStream", def (table) {
    submitJob("replayOrderTrade", "replayOrderTrade", def (table) {
        ds1 = replayDS(sqlObj=<select * from loadTable("dfs://positionMonitorData", "marketData") where Date=2023.02.01>, dateColumn=`Date, timeColumn=`Time, timeRepartitionSchema=cutPoints(09:30:00.000..15:00:00.000, 50))
        replay(inputTables=ds1, outputTables=table, dateColumn=`Date, timeColumn=`Time, replayRate=1, absoluteRate=false, preciseRate=true)
    }, table)
})
// 回放行情快照数据
useOrcaStreamTable("SnapshotStream", def (table) {
    submitJob("replaySnapshot", "replaySnapshot", def (table) {
        ds2 = replayDS(sqlObj=<select * from loadTable("dfs://positionMonitorData", "snapshot") where Date=2023.02.01>, dateColumn=`Date, timeColumn=`Time, timeRepartitionSchema=cutPoints(09:30:00.000..15:00:00.000, 50))
        replay(inputTables=ds2, outputTables=table, dateColumn=`Date, timeColumn=`Time, replayRate=1, absoluteRate=false, preciseRate=true)
    }, table)
})
```

在本文中，我们通过自定义的数据回放函数来模拟行情快照的实时传入。在自定义的函数中，`replayDS` 函数可以将输入的 SQL
表达式，根据时间维度划分为多个数据源，作为 `replay`
函数的输入，逐一进行回放。其中，*timeRepartitionSchema* 参数用于划分数据源，通过
`cutPoints` 函数可以将一个交易日均匀划分为50个桶。*replayRate*参数决定了数据回放的速率，在 *replayRate*=1、*absoluteRate*=false
的情况下，数据将根据时间列的时间跨度原速完成回放。最后，通过 `submitJob` 函数将数据回放任务提交到 Orca
流表所在的数据节点。

## 5. 结果展示

本章展示在完成流图的构建和数据回放后，如何查看流图的运行状态和计算结果。

### 5.1 查看流图状态

创建流图后，我们可以通过 Web 以及 Orca 提供的 API 接口来查看流图的运行状态。

#### (1) 通过 web 查看流图状态

流图提交后，可以在 Web 流图监控界面里查看已经定义好的流图结构。本例中通过 `DStream::parallelize`
方法将计算并行度设置为 2 时，流图如下图所示：

![](images/orca_finance_position/5_1.png)

图 2. 图5-1 流图结构

通过下方的流任务订阅、流任务发布和流引擎等表格，我们可以实时查看流图中订阅节点的工作线程状态、订阅表对应的发布端连接状态、以及引擎和流表的状态，如下图所示：

![](images/orca_finance_position/5_2.png)

图 3. 图5-2 流任务状态

#### (2) 通过运维函数查看流图状态

Orca 提供了丰富的运维函数来支持流图的监控和维护。Web 页面显示的内容实际上是调用这些运维函数返回的结果的可视化。

通过 `getStreamGraphInfo` 方法可以查看流图的结构、调度等元信息。

```
getStreamGraphInfo("positionMonitorDemo.orca_graph.positionMonitor")
```

使用 `getOrcaStreamTableMeta` 方法可以查看流图中指定流表的元信息。

```
getOrcaStreamTableMeta('positionMonitorDemo.orca_table.MarketDataStream')
```

使用 `getOrcaStreamEngineMeta` 方法获取流图中所有流引擎的元信息。

```
getOrcaStreamEngineMeta("positionMonitorDemo.orca_graph.positionMonitor")
```

关于 Orca 运维函数的更多介绍可以参考 Orca 系列。

### 5.2 查看计算结果

通过以下 SQL 语句，可以查询持仓监控指标的计算结果：

```
result = select * from positionMonitorDemo.orca_table.PositionMonitorStream
```

其中，PositionMonitorStream
是之前定义的用于存放计算结果的流数据表。在查询流图中的对象时，需要输入查询对象完整的全限定名。查询结果如下所示：

![](images/orca_finance_position/5_3.png)

图 4. 图5-3 监控指标实时计算结果

### 5.3 结果可视化

通过编辑 Web 中的数据面板，可以对计算结果进行可视化展示，如下图所示。该面板的 json 配置文件可以在附录中获取。

![](images/orca_finance_position/5_4.png)

图 5. 图5-4 数据面板

## 6. 性能测试

本文通过回放大批量历史数据，测试了响应每条成交委托记录完成 12 个指标计算所花费的计算时延。计算时延指每条记录完成响应计算的时刻（ UpdateTime
），与该条成交委托记录到达系统的时刻（ReceiveTime）的差值。我们对全部记录的计算时延分别取了平均值和99分位数，其中99分位数指超过 99%
的记录的计算时延均小于该数值。

此外，我们还测试了不同并发数、不同回放速度下的计算性能。不同的回放速度对应了不同的数据流量，其中五倍速回放模拟了高负载场景，委托成交流水的处理速率（TPS）高达 5
万笔每秒。

### 6.1 测试数据量

* 模拟委托成交流水

  + 每秒 1 万条
  + 3,000 支标的
  + 800个账户（每个账户均有2,300+标的）
  + 总共 72,026,955 条记录（09:30-11:30 半个交易日）
* 模拟静态持仓信息

  + 模拟数据
  + 当日800个账户所持的每支标的为一条记录
* 真实行情快照

  + 3 秒频 Level 2 股票行情快照

### 6.2 测试结果

**时延单位：微秒**

| 并发数 | 回放速度 | 委托成交流水TPS | 全链路总时延（平均/99分位） |
| --- | --- | --- | --- |
| 8 | 1X | 1w | 743 / 1622 |
| 16 | 1X | 1w | 697 / 1391 |
| 8 | 5X | 5w | 1045 / 8928 |
| 16 | 5X | 5w | 877 / 4155 |

图 6. 表6-1 性能测试结果

* 并发度为 8 时，面对 1 万 TPS 的流量，全链路平均时延为 743 微秒。
* 同样，并发度为 8 时，即使系统的流量增加至 5 万 TPS，全链路平均时延依然保持在约 1 毫秒。
* 通过提升并发数，可以进一步降低计算时延。尤其在大压力下，并发度由 8 并发增加至 16，99
  分位时延能够降低一倍多，这得益于更多的算力保证了系统在流量峰值时刻的表现。

### 6.3 测试环境

本测试使用了 DolphinDB server 的单节点模式，具体的软硬件环境配置如下表所示：

| 环境 | 型号/配置/软件名称/软件版本号 |
| --- | --- |
| DolphinDB | 3.00.4 2025.09.09 LINUX\_JIT x86\_64 |
| 物理服务器1台 | 系统：CentOS Linux 7 (Core) |
| 内核：3.10.0-1160.el7.x86\_64 |
| CPU：Intel(R) Xeon(R) Gold 5220R CPU @ 2.20GHz |
| license 限制：   * 8 核 256 GB |
| 配置文件配置测试节点最大可用内存：256 GB |

图 7. 表6-2 环境配置详情

## 7. 总结与展望

Orca 声明式 DStream API 通过简洁的编程风格实现了传统的流计算功能，降低了使用 DolphinDB 执行复杂流计算任务的开发难度。本文基于
Orca，提供了一种持仓监控指标实时计算的低延时解决方案，旨在为开发人员使用 DolphinDB 开发高性能流计算业务场景提供参考，从而提高开发效率。

后续，企业级实时平台 Orca 还将推出以下核心功能与优化。依托下述低延时引擎技术，本文中的持仓监控程序的反应速度，还会进一步大幅提升。

* 低延时引擎：支持十微秒级别极低计算延时
* 流式 SQL 引擎：集成低延时流式 SQL 计算
* 流高可用：支持全内存、极低延时高可用
* 即时编译：支持流引擎算子融合与即时编译
* 开发与调试：支持更易用的流计算任务开发与调试

Orca 旨在为金融机构构建新一代内部统一平台提供完整的技术基座，将机构的反应速度从 T+1 提升至 T+0 ，甚至是微秒级。

## 附录

* 示例代码-持仓监控流计算：[PositionMonitor.dos](https://cdn.dolphindb.cn/zh/tutorials/script/orca_finance_position/PositionMonitor.dos)
* 示例代码-库表创建与样例数据导入：[importData.dos](https://cdn.dolphindb.cn/zh/tutorials/script/orca_finance_position/importData.dos)

* 示例数据：[SampleData.zip](https://cdn.dolphindb.cn/zh/tutorials/script/orca_finance_position/SampleData.zip)

* 数据面板配置文件：[dashboard.positionMonitor.json](https://cdn.dolphindb.cn/zh/tutorials/script/orca_finance_position/dashboard.positionMonitor.json)
