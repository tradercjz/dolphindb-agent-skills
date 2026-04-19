<!-- Auto-mirrored from upstream `documentation-main/tutorials/order_splitting_with_cep_advanced.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# CEP 引擎应用：算法拆单调度系统实现-进阶篇

教程难度

* 高级

面向读者

* 已经掌握 DolphinDB 基础操作，包括 server 部署、客户端部署、库表创建代码编写和调试：新用户入门指南（金融篇）
* 已经掌握 DolphinDB 数据回放，流数据表订阅和 CEP 引擎
* 已经掌握 CEP 引擎应用：算法拆单调度系统实现-基础篇
* 具备代码开发和调试能力
* 计划基于 DolphinDB 产品搭建拆单+模拟撮合的全流程仿真系统

在金融市场的实际交易策略中会有许多复杂的场景。例如大额拆单的冰山算法，为了隐藏交易意图，每次只维持一小部分订单在盘口，根据接收的成交回报做对应处理；如套利场景，需要接入至少 2
个实时数据流进行触发下单，并结合模拟撮合引擎进行买卖单的撮合。

本教程使用了 DolphinDB 的 CEP (复杂事件处理引擎用)产品和模拟撮合引擎插件产品，系统的讲解了使用 CEP
引擎+模拟撮合引擎来实现复杂的拆单、下单策略，包括冰山拆单算法和套利下单实现。本教程读者将学习以下内容：

* 模拟撮合引擎简介。
* 如何实现冰山拆单算法，并接入模拟撮合引擎插件，模拟成交回报。
* 如何实现自定义套利下单，并接入模拟撮合引擎，完成套利操作。

## 1. 模拟撮合引擎简介

本教程中的拆单策略均要根据市场反馈也就是成交回报来进行相应处理，所以本节将先简单介绍 DolphinDB 的模拟撮合引擎产品。

在中高频策略中，我们常常会遇到这样的情况：一些在回测中表现良好的策略，一旦应用于实际交易，效果就不如预期。其中一个非常重要的原因是低估了交易成本。为了更准确地模拟实际交易中的成本，DolphinDB
开发了模拟撮合引擎。使我们能够更合理地评估和预测策略在实际交易中的表现，并进行相应的优化。

模拟撮合引擎的主要功能是模拟用户在某个时间点发出订单或取消之前已发出订单的操作，并获取相应的交易结果。该引擎以行情数据（快照数据或逐笔数据）和用户委托订单（买方或卖方）作为输入，根据订单撮合规则实现模拟撮合后，将订单成交结果（含部分成交结果、拒绝订单和已撤订单）输出至订单明细输出表，未成交部分等待与后续行情撮合成交，或者等待用户撤单。逻辑架构如下图所示。

![](images/order_splitting_with_cep_advanced/1_1.png)

图 1. 图1-1 模拟撮合引擎逻辑架构图

关于模拟撮合引擎的更详细内容及使用教程，请登录官网查阅。

## 2. 冰山算法接入模拟撮合引擎

### 2.1 算法思想

#### 2.1.1 冰山算法

冰山算法（Iceberg）是一种大额订单拆分策略，主要用于隐藏真实交易规模，减少市场冲击。该策略将大订单拆分为多个小订单，每次仅显示一小部分（即“冰山一角”），其余部分隐藏。当已显示的部分成交后，再逐步释放新的订单，直至全部成交。

与TWAP按时间均匀分配不同，冰山订单的核心在于隐藏流动性，避免因大单暴露而引发市场过度反应。该策略适用于流动性较好但订单规模较大的交易场景，尤其适合机构投资者在不影响市场价格的情况下执行大额交易。

#### 2.1.2 模拟撮合引擎

在中高频策略中，常有一些在回测中表现良好的策略，一旦应用于实际交易，效果就不如预期。为了使拆单算法研究更贴近真实的交易情况，本例在拆单系统中引入
DolphinDB
提供的模拟撮合引擎插件。模拟撮合引擎可以模拟用户在某个时间点发出订单或取消之前已发出订单的操作，并获取相应的交易结果，其逻辑架构如下图所示。

![](images/order_splitting_with_cep_advanced/2_1.png)

图 2. 图2-1 模拟撮合引擎插件架构图

模拟撮合引擎以行情（快照数据或逐笔数据）和用户委托订单（买方或卖方）作为输入，根据订单撮合规则模拟撮合，将订单的成交结果（包含部分成交结果、拒绝订单和已撤订单）输出至交易明细输出表，未成交部分等待与后续行情撮合成交或者等待撤单。关于更多引擎运行机制的说明和撮合规则的解释见官方文档 。

### 2.2 功能模块

算法逻辑通过 CEP 引擎实现；通过数据回放功能模拟实时行情快照写入；使用流表订阅功能解耦用户母单发布和拆单 CEP
引擎；将快照行情、子单流表中的委托单、撤单注入模拟撮合引擎，模拟真实的市场交易；将撮合结果构造为部分成交事件和完全成交事件注入 CEP
引擎，作为冰山算法的成交回报。大致流程如下图所示。

![](images/order_splitting_with_cep_advanced/2_2.png)

图 3. 图2-2 算法流程图

冰山算法的算法流程与 TWAP 算法相似，区别有以下几点。

* 冰山算法接入模拟撮合引擎插件，将快照行情数据、子单流表中的委托订单和撤单，注入模拟撮合引擎，模拟现实市场的订单成交。并将撮合结果注入 CEP
  引擎，作为冰山算法的成交回报。
* CEP 引擎中新增事件类 `SubOrderTransaction` 和
  `SubOrderPartTransaction`
  ，即子单完全成交事件和子单部分成交事件，子单部分成交事件用于累计当前子单的总成交量，用于超时未完全成交时，撤销剩余股数的挂单。
* 监视器中的拆单核心函数 `placeOrder`
  中，下完一个子单后，设置子单部分成交事件监听、子单完全成交事件监听和子单成交超时监听。当上一个子单在规定时间内完全成交后，会继续拆单下单；若子单未在设定时间内完全成交，则下达撤单到子单流表，撤销当前子单剩余股数的挂单，并下新的子单。

### 2.3 代码实现

在本节中我们介绍代码实现。

#### 2.3.1 定义事件类

* 定义母单类中拆单参数如下：

```
	//拆单参数开始
    splitMethod :: STRING          // 拆单算法
    orderType :: STRING            // 订单类型（限价/市价）
    price :: DOUBLE                // 限定价格
    priceOption :: INT             // 买一还是卖一价格
    orderQty :: INT                // 子单股数
    timeoutNum :: INT              // 超时时间（秒）
    startTime :: TIMESTAMP         // 拆单开始时间
    endTime :: TIMESTAMP           // 拆单结束时间
    orderStatus :: STRING          // 拆单状态
```

其中 `orderQty` 表示子单的固定股数， `timeoutNum`
表示子单成交事件的超时时间。

* 子单完全成交事件类中成员变量如下：

```
    splitOrderId :: STRING         //操作的母单号
    eventType :: STRING          // 事件类型
    subOrderID :: STRING     // 子单唯一ID，对应子单流表中的tagBatchId
    eventTime :: TIMESTAMP   // 下达子单成交时间
```

其中，`splitOrderId` 表示操作的母单号；`eventType`
表示事件类型；`subOrderID` 表示子单唯一 ID ；`eventTime`
表示事件到达时间。

* 子单部分成交事件类与子单完全成交事件类相似，但需要一个成交量字段，子单部分成交事件类中成员变量如下：

```
    splitOrderId :: STRING         //操作的母单号
    eventType :: STRING          // 事件类型
    subOrderID :: STRING     // 子单唯一ID，对应子单流表中的tagBatchId
    tradeQty :: INT          // 成交量
    eventTime :: TIMESTAMP   // 下达子单成交时间
```

其中，`splitOrderId` 表示操作的母单号；`eventType`
表示事件类型；`subOrderID` 表示子单唯一 ID ；`tradeQty`
表示成交量；`eventTime` 表示事件到达时间。

#### 2.3.2 创建内存表

创建内存表代码与 TWAP 算法 step2-创建母单、子单记录内存表
相似，母单记录内存表略有不同；并增加子单内存表订阅子单流表，子单内存表新增 `transactionQty` 和
`subOrderStatus` ，实时展示委托单的成交量和子单状态。

* 母单记录内存表、修改母单内存表定义

```
//创建母单记录内存表
colNames=["splitOrderId","eventType","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","tradeDirection","market","handlerEmpid","handlerName","splitMethod","orderType","price","startTime","endTime","orderQty","orderStatus","timeoutNum","eventTime","lastUpdateTime"]
colTypes=[STRING,SYMBOL,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,SYMBOL,DOUBLE,TIMESTAMP,TIMESTAMP,INT,SYMBOL,INT,TIMESTAMP,TIMESTAMP]
share table(1:0,colNames,colTypes) as parentOrderManage

//创建修改订单记录内存表
colNames=`splitOrderId`eventType`operation`batchId`handlerEmpid`handlerName`eventTime
colTypes=[STRING,STRING,STRING,STRING,STRING,STRING,TIMESTAMP]
share table(1:0, colNames, colTypes) as alterOrderManage
```

`orderQty` 和 `timeoutNum`
分别表示子单的固定股数和子单成交事件的超时时间。

* 子单内存表订阅子单流表

```
// 创建子单接收流数据表
colNames=["splitOrderId","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","tradeDirection","market","handlerEmpid","handlerName","orderType","price","lastUpdateTime"]
colTypes=[STRING,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,DOUBLE,TIMESTAMP]
share streamTable(1:0, colNames, colTypes) as subOrderStream

// 创建子单接收内存表订阅子单接受流表，作为信息展示
colNames=["splitOrderId","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode",
"stockName","tradeDate","tradeQuantity","transactionQty","subOrderStatus","tradeDirection","market","handlerEmpid","handlerName","orderType","price","lastUpdateTime"]
colTypes=[STRING,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,LONG,STRING,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,DOUBLE,TIMESTAMP]
share table(1:0, colNames, colTypes) as subOrderTb

// 子单内存表订阅子单流表处理函数
def subscribeSubOrderStream(msg){
    // 拿到所有数据
    data = exec * from msg
    s = data.size()
    // 准备已成交量和子单状态初始值
    tQtyV = array(LONG,s,s,0)
    staV = array(STRING,s,s,"等待成交")
    // 向subOrderTb表写入
    insert into subOrderTb values(data[`splitOrderId],data[`batchId],data[`tagBatchId],data[`sortNum],
                                  data[`fundCode],data[`fundName],data[`assetId],data[`assetName],
                                  data[`combinationNo],data[`combinationName],
                                  data[`stockCode],data[`stockName],data[`tradeDate],data[`tradeQuantity],
                                  tQtyV,staV,
                                  data[`tradeDirection],data[`market],data[`handlerEmpid],data[`handlerName],
                                  data[`orderType],data[`price],data[`lastUpdateTime])
}

// 订阅流表
subscribeTable(tableName = `subOrderStream,actionName=`subscribeSubOrderStream,handler = subscribeSubOrderStream,msgAsTable=true,batchSize = 1)
```

`subOrderStream` 表用于接收子单和撤单；`subOrderTb` 用于在
Dashboard 中进行信息展示，新增两个字段 `transactionQty` 和
`subOrderStatus` ，实时展示委托单的成交量和子单状态。

#### 2.3.3 创建模拟撮合引擎

在本例中，模拟撮合引擎也需要订阅行情快照数据，因此模拟撮合引擎需要在订阅行情快照前创建。

* 加载模拟撮合引擎插件

```
login("admin", "123456")
//使用 installPlugin 命令完成插件安装
installPlugin("MatchingEngineSimulator")
//使用 loadPlugin 命令加载插件。
loadPlugin("MatchingEngineSimulator")
```

模拟撮合插件需要用户使用上述代码，自行从插件仓库下载并加载。

* 创建模拟撮合引擎

加载模拟撮合引擎插件后，创建模拟撮合引擎。

```
// 定义函数创建模拟撮合引擎
//撮合引擎cfg
config = dict(STRING, DOUBLE);
config["latency"] = 0;                  //用户订单时延为0
config["depth"] = 10;                   //十档买盘
config["outputOrderBook"] = 0            // 不输出订单簿
config["orderBookMatchingRatio"] = 0.2;    //与订单薄匹配时的成交百分比
config["dataType"] = 1;                  //行情类别：1表示股票快照
config["matchingMode"] = 1;              //撮合模式一：与最新成交价以及对手方盘口按配置的比例撮合
config["matchingRatio"] = 0.1;           //快照模式下，快照的区间成交百分比
config["userDefinedOrderId"] = true     // 新增用户指定的订单id列userOrderId

//行情表结构
// 创建行情内存表，作为模拟撮合引擎的输入参数
colNames=`SecurityID`Market`TradeTime`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty`BidPrice`BidOrderQty`OfferPrice`OfferOrderQty
colTypes=[STRING,STRING,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE[],INT[],DOUBLE[],INT[]]
dummyQuoteTable =  table(1:0, colNames, colTypes)
//行情数据表列名映射关系，即自己定义的和引擎内部的映射关系
quoteColMap = dict(  `symbol`symbolSource`timestamp`lastPrice`upLimitPrice`downLimitPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty,
                     `SecurityID`Market`TradeTime`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty`BidPrice`BidOrderQty`OfferPrice`OfferOrderQty,)

//用户委托单的结构
// 创建用户委托单内存表
colNames=`securityID`market`orderTime`orderType`price`orderQty`BSFlag`orderID
colTypes=[STRING, SYMBOL, TIMESTAMP, INT, DOUBLE, LONG, INT, LONG]
dummyUserOrderTable =  table(1:0, colNames, colTypes)
//映射关系
userOrderColMap = dict( `symbol`symbolSource`timestamp`orderType`price`orderQty`direction`orderId,
                        `securityID`market`orderTime`orderType`price`orderQty`BSFlag`orderID)

//订单详情结果输出表，包括订单委托回报、成交、拒单和撤单状态，此表输出的成交事件会变成成交事件输出到CEP引擎中
//4：已报，-2：表示撤单被拒绝，-1：表示订单被拒绝，0：表示订单部分成交，1：表示订单完全成交，2：表示订单被撤单
// 创建模拟撮合引擎的输出结果表，该表输出的成交记录会转为成交事件输出到CEP引擎
// 输出结果表添加userOrderId列，并且作为流表
colNames=`orderId`symbol`direction`sendTime`orderPrice`orderQty`tradeTime`tradePrice`tradeQty`orderStatus`sysReceiveTime`userOrderId
colTypes=[LONG, STRING, INT,TIMESTAMP,DOUBLE,LONG, TIMESTAMP,DOUBLE,LONG, INT,NANOTIMESTAMP, LONG]
orderDetailsOutput = streamTable(1:0, colNames, colTypes)
//共享
share orderDetailsOutput as outputTb

//撮合深交所股票
exchange = "XSHE"
//创建引擎
name = "MatchingEngine"
matchingEngine = MatchingEngineSimulator::createMatchEngine(name, exchange,
config, dummyQuoteTable, quoteColMap, dummyUserOrderTable, userOrderColMap, orderDetailsOutput,,)

// 共享模拟撮合引擎
share matchingEngine as mEngine
```

使用 `createMatchEngine` 创建模拟撮合引擎。步骤如下：

1. 定义 *config* 参数。`latency`
   指定撮合时延，当最新行情时间>=订单时间时，开始撮合用户订单；`depth`
   表示盘口深度为10；`orderBookMatchingRatio` 和
   `matchingRatio` 指定成交比例；`matchingMode`
   指定第一种撮合模式，即与最新成交价以及对手方盘口按配置的比例撮合（快照行情无区间成交明细信息时）；`userDefinedOrderId`
   设置为 `true` 表示在撮合结果表中新增用户指定订单 ID 列。
2. 定义行情表 `dummyQuoteTable` 、用户委托表结构
   `dummyUserOrderTable` ，以及和引擎内部对应表的字段映射关系；定义撮合结果输出表
   `orderDetailsOutput` 并共享为 `outputTb`
   ，后续 CEP 引擎会订阅 `outputTb` 中的成交事件，并将撮合结果在 Dashboard
   中展示。
3. *exchange* 定义交易所为深交所，指定引擎名称，使用 `createMatchEngine`
   函数创建模拟撮合引擎。

#### 2.3.4 订阅行情快照

* 定义行情快照流表和键值对表

```
// 定义行情快照流表，这个流表用于接收回放的行情快照数据
colNames = `Market`TradeDate`TradeTime`SecurityID`OfferPrice`BidPrice`OfferOrderQty`BidOrderQty`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty
coltypes = [SYMBOL,DATE,TIME,SYMBOL,DOUBLE[],DOUBLE[],INT[],INT[],DOUBLE,DOUBLE,DOUBLE,INT,INT]
share streamTable(1:0,colNames,coltypes) as snapshotStream

// 创建键值对表，该表订阅snapshotStream，存储每个股票的买盘和卖盘,每个股票的买盘和卖盘只有一条记录
colNames = `Market`TradeDate`TradeTime`SecurityID`OfferPrice`BidPrice`OfferOrderQty`BidOrderQty
coltypes = [SYMBOL,DATE,TIME,SYMBOL,DOUBLE[],DOUBLE[],INT[],INT[]]
snapshotOutputKeyedTbTmp = keyedTable(`SecurityID,1:0,colNames,coltypes)
share snapshotOutputKeyedTbTmp as snapshotOutputKeyedTb
```

`snapshotStream`
用于接收回放的行情快照数据，`snapshotOutputKeyedTb`
用于存储每个股票的最新快照数据，为拆单系统提供子单委托价格参考。

* 模拟撮合引擎订阅行情快照

```
// 处理表格，使其返回一个年月日，时分秒的向量
def handleCompleteTime(tb){
    s = tb.size()
    // 初始化结果向量
    res = array(TIMESTAMP,s,s,now())
    for(i in 0:s){
        dictTime = tb[i]
        // 拼接
        tempTimeStr = dictTime[`TradeDate]+" "+dictTime[`TradeTime]+"000"
        // 转换
        tempTime = temporalParse(tempTimeStr,"yyyy.MM.dd HH:mm:ss.nnnnnn")
        // 赋值
        res[i] = tempTime
    }
    return res
}

// 处理交易时间，使其从2023年变为2026年的快照数据
def handleTradeTime(x){
    return temporalAdd(x,3,"y")
}

// 订阅snapshotStream
def handleSnapshot(msg) {
    // 拿到所有数据
    data = exec * from msg
    // 向snapshotOutputKeyedTb表写入
    // 对TradeDate做处理，使其晚于委托单的时间
    TimeV = exec TradeDate from msg
    tV = each(handleTradeTime, TimeV)
    insert into snapshotOutputKeyedTb values(data[`Market],tV,data[`TradeTime],data[`SecurityID],
                                             data[`OfferPrice],data[`BidPrice],data[`OfferOrderQty],data[`BidOrderQty])

    // 向模拟撮合引擎中写入快照数据
    colNames=`SecurityID`Market`TradeTime`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty`BidPrice`BidOrderQty`OfferPrice`OfferOrderQty
    colTypes=[STRING,STRING,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE[],INT[],DOUBLE[],INT[]]
    snapshotTempTb = table(100:0,colNames,colTypes)
    // 需要对快照时间做处理，使其晚于委托单的时间
    TimeV = exec TradeDate,TradeTime from msg
    TimeV1 = handleCompleteTime(TimeV)
    tV = each(handleTradeTime, TimeV1)
    snapshotTempTb.tableInsert(data[`SecurityID],data[`Market],tV,
                               data[`LastPrice],data[`UpLimitPx],data[`DownLimitPx],data[`TotalBidQty],data[`TotalOfferQty],
                               data[`BidPrice],data[`BidOrderQty],data[`OfferPrice],data[`OfferOrderQty])
    MatchingEngineSimulator::insertMsg(getStreamEngine("MatchingEngine"), snapshotTempTb, 1)
}

// 订阅流表
subscribeTable(tableName = `snapshotStream,actionName=`handleSnapshot,handler = handleSnapshot,msgAsTable=true,batchSize = 1)
```

订阅 `snapshotStream` ，当 `snapshotStream`
有增量行情快照，将快照分别写入 `snapshotOutputKeyedTb`
和模拟撮合引擎。`snapshotOutputKeyedTb`
用于存储每个股票的最新快照数据，为拆单系统提供子单委托价格参考；使用 `insertMsg`
向模拟撮合引擎写入快照数据，在撮合引擎中，行情快照时间须晚于委托单下单时间，引擎才会进行撮合，因此这里对历史快照的时间做处理，将 2023
年的快照数据改为 2026 年的快照数据。

本例中，`snapshotOutputKeyedTb` 中的快照数据和模拟撮合引擎中的快照数据被同步写入，而
`snapshotOutputKeyedTb`
为子单提供委托价格，保证子单委托价格符合模拟撮合引擎中的实时行情，避免了长期挂单无法成交的情况。

#### 2.3.5 订阅子单流表

模拟撮合引擎需要输入行情数据和用户委托单，前面已经通过回放和订阅将行情数据注入模拟撮合引擎，本节通过订阅，将子单流表中的用户委托单和撤单注入模拟撮合引擎，代码如下：

```
// 在这里通过订阅，将用户订单注入模拟撮合引擎

// orderType需要转换，引擎内部需要INT类型，限价单转为5，撤单转为6
def handleOrderType(x){
    if(x=="Limit"){
        return 5
    }else{
        return 6
    }
}

// 买卖方向需要转换，引擎内部需要INT类型，买转为1，卖转为2
def handleDirection(x){
    if(x=="B"){
        return 1
    }else{
        return 2
    }
}

// 子单id，引擎内部需要long类型，用字符切割，拼成子单id
def handleOrderId(x){
    oV = split(x,"_")
    res = ""
    for(str in oV){
        res = res+str
    }
    return long(res)
}

// 订阅subOrderStream，作为模拟撮合引擎的输入参数
def handleUserOrders(msg) {
    // 拿到所有订单（非撤单）
    data = exec * from msg

    // 向dummyUserOrderTable表写入，这里orderType和direction需要转换，内部需要INT类型
    // orderId转为long
    orderTypeV = exec orderType from msg
    otV = each(handleOrderType, orderTypeV)

    directionV = exec tradeDirection from msg
    dV = each(handleDirection, directionV)

    orderIdV = exec tagBatchId from msg
    oV = each(handleOrderId, orderIdV)

    // 暂存表
    colNames=`securityID`market`orderTime`orderType`price`orderQty`BSFlag`orderID
    colTypes=[STRING, SYMBOL, TIMESTAMP, INT, DOUBLE, LONG, INT, LONG]
    subOrderTempTb = table(1:0, colNames, colTypes)
    subOrderTempTb.tableInsert(data[`fundCode],data[`market],data[`lastUpdateTime],
                                       otV,data[`price],data[`tradeQuantity],dV,oV)
    MatchingEngineSimulator::insertMsg(getStreamEngine("MatchingEngine"), subOrderTempTb, 2)
}

// 订阅流表
subscribeTable(tableName = `subOrderStream,actionName=`handleUserOrders,handler = handleUserOrders,msgAsTable=true,batchSize = 1)
```

`handleOrderType` 、`handleDirection`
、`handleOrderId`
分别用于处理子单流表和模拟撮合引擎中委托表，`orderType`
、`tradeDirection` 、`tagBatchId`
三个字段类型不符的情况；使用 `insertMsg` 将委托单或者撤单注入模拟撮合引擎。

#### 2.3.6 定义监视器

CEP 引擎内部监视器的配置是拆单系统实现中最关键的步骤。监视器内封装了整个拆单策略，其结构大致如下。

```
class SplitMonitor:CEPMonitor{

	def SplitMonitor() {
		//本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
	}

    //更新母单记录信息
    def updatePOrderManageInfo(pOrder,opTime){...}

    def placeOrder(){}

}

//Iceberg 算法下单监听 monitor，继承关系
class IceBergSplitMonitor:SplitMonitor {

    // 记录子单总下股数的变量
    subOrderQtys :: INT
    // 母单
	parentOrder :: ParentOrder
    // 记录母单当前子单已经成交的股数，初始为0，用于撤单管理，撤单或者全部成交后要将该变量归0，用于下个子单的撤单管理复用
    transactionQty :: INT

	def IceBergSplitMonitor() {
		//本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
	}
    // 更新子单当前状态和已成交量
    def updateSubOrder(Qty,status){...}

    // 返回最新的快照时间
    def getLastTime(){...}

    // 接收到对应的成交单，进行下一次拆单
    def ifPlaceOrder(subOrderTran){...}

    // 最后一次完全成交的逻辑
    def ifPlaceOrderLast(subOrderTran){...}

    // 子单id，引擎内部需要long类型，用字符切割，拼成子单id
    def handleOrderId(x){...}

    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){...}

    // 下达撤单事件,将上一次的子单进行撤单，恢复子单已下总股数
    def cancelOrder(){...}

    //Iceberg 下单方法
    def placeOrder(){...}

    //初始化sub monitor
    def startPlaceOrder(pOrder){...}

    //复制母单下单sub_monitor实例
	def forkParentOrderMonitor(pOrder){...}

	//初始任务
	def onload(){
		addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
	}
}
```

成员变量 `subOrderQtys` ：记录当前已下子单的股数和，避免超出母单股数。

成员变量 `parentOrder` ：记录当前母单的参数，包括基本信息，拆单参数，和拆单状态。

成员变量 `transactionQty`
：记录当前子单的成交股数，用于在规定时间未能完全成交时，对剩余股数进行撤单。

下面将按照 CEP 引擎运作的逻辑顺序，依次介绍监视器中各个成员方法的具体内容。

* **onload 初始任务**

创建引擎并实例化监视器后，将首先调用其内部的 `onload` 函数。在 `onload`
函数中，使用 `addEventListener` 函数监听 `ParentOrder`
事件注入，指定回调函数为 `forkParentOrderMonitor` ，事件类型是
`ParentOrder` ，设置监听次数为持续监听。

```
    //初始任务
	def onload(){
		addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
	}
```

`onload` 方法设置了一个事件监听器，监听所有的母单事件 `ParentOrder`
。当监听到该类型事件时，下一步将启动整个拆单下单过程。从 `onload`
方法开始，函数调用的流程与实现的功能可以分为三个模块，如下图所示。

![](images/order_splitting_with_cep_advanced/2_3.png)

图 4. 图2-3 模块调用流程图

其中， `startPlaceOrder` 函数是后三个模块的启动函数，启动顺序如上图所示。模块 3
中，函数调用的流程与实现的功能如下图所示。

![](images/order_splitting_with_cep_advanced/2_4.png)

图 5. 图2-4 模块3流程图

接下来从策略启动事件对应的回调函数 `forkParentOrderMonitor` 开始来介绍具体的代码实现。

* **forkParentOrderMonitor 生成监视器实例**

CEP 引擎内的初始 Monitor 只负责监控策略启动事件注入，参考上文的 `onload` 函数。每当
`onload` 函数监测到新的 `ParentOrder` 事件注入，调用
`forkParentOrderMonitor` 生成一个新的 sub-Monitor
实例，进行当前委托单的拆单下单操作。

```
    //生成一个母单下单monitor实例
	def forkParentOrderMonitor(pOrder){
        name = "母单下单["+pOrder.splitOrderId +"]"
        spawnMonitor(name,startPlaceOrder, pOrder)
	}
```

`forkParentOrderMonitor` 中，使用 DolphinDB 的
`spawnMonitor` 函数，生成一个 sub-Monitor 实例，并调用
`startPlaceOrder` 方法，并将注入的 `ParentOrder`
事件 `pOrder` 传入。启动后续核心模块。

* **startPlaceOrder 启动核心模块**

`startPlaceOrder` 函数中，包含模块 2 、模块 3 和模块 4 的启动步骤，函数定义如下。

```
    //初始化sub monitor
    def startPlaceOrder(pOrder){
        // 设置当前子任务 monitor 对象的内部母单变量
        parentOrder = pOrder
        // 对子单量总股数初始化为0
        subOrderQtys = 0
        //TWAP 拆单初始化
        parentOrder.setAttr(`orderStatus,'初始化')
        parentOrder.setAttr(`sortNum,0)  //拆单顺序号
        // 初始化子单成交股数
        transactionQty = 0
        //记录母单状态到内存表
        initPOrderManageInfo(parentOrder)

        //计算母单开始拆单下单时间
        if(parentOrder.startTime == null|| now()>=parentOrder.startTime){//初始下单时间为空，或者初始下单时间早于现在,则立即开始下单
            placeOrder()
        }else {//下单等待时间，按指定startTime 时间开始下单
            //当前时间到开始下单时间间隔,计算出来的是毫秒数,转成秒
            period_wait = round((parentOrder.startTime - now())\1000 ,0)
            //指定在 period_wait 秒后开始启动一次下单
            addEventListener(placeOrder,,,1,,duration(period_wait+"s"))
        }
	}
```

函数逻辑如下：

1. 先进行当前 Monitor 母单成员变量 `parentOrder` 、子单总股数成员变量
   `subOrderQtys` 和子单成交股数
   `transactionQty` 的初始化。然后调用
   `initPOrderManageInfo` 函数，将当前母单事件记录到内存表
   `parentOrderManage` 中，对应模块 2 。
2. 初始化完成，检查当前时间是否到达开始拆单时间。若已经超过开始下单时间，则调用 `placeOrder`
   函数对当前委托单进行拆单下单；否则等待到达开始时间后，调用 `placeOrder` 函数。对应模块 3
   中的拆单开始时间判断。

* **getLastTime 查询最新快照时间**

`getLastTime` 函数代码如下：

```
    // 返回最新的快照时间
    def getLastTime(){
        tb = exec top 1 TradeDate,TradeTime from snapshotOutputKeyedTb
        s = tb.size()
        // 初始化结果向量
        res = array(TIMESTAMP,s,s,now())
        for(i in 0:s){
            dictTime = tb[i]
            // 拼接
            tempTimeStr = dictTime[`TradeDate]+" "+dictTime[`TradeTime]+"000"
            // 转换
            tempTime = temporalParse(tempTimeStr,"yyyy.MM.dd HH:mm:ss.nnnnnn")
            // 赋值
            res[i] = tempTime
        }
        return res[0]
    }
```

模拟撮合引擎中，当前的行情快照时间需要晚于委托单时间，引擎才会撮合委托单成交。因此本例使用
`snapshotOutputKeyedTb`
表中的最新快照时间作为全局时间，将子单的委托下单时间、母单的更新时间都设置为快照时间，保证行情快照时间需要晚于委托单时间。定义
`getLastTime` 函数查询最新快照时间。

* **initPOrderManageInfo 记录母单信息**

`initPOrderManageInfo` 函数的定义十分简单，将监听到的母单事件记录到对应内存表
`parentOrderManage` 中。

```
    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){
        parentOrderManage=objByName('parentOrderManage')
        tempTime = getLastTime()
        insert into parentOrderManage values(
            pOrder.splitOrderId,pOrder.eventType,pOrder.batchId,pOrder.tagBatchId,pOrder.sortNum,
            pOrder.fundCode,pOrder.fundName,pOrder.assetId,pOrder.assetName,pOrder.combinationNo,
            pOrder.combinationName,pOrder.stockCode,pOrder.stockName,pOrder.tradeDate,pOrder.tradeQuantity,
            pOrder.tradeDirection,pOrder.market,pOrder.handlerEmpid,pOrder.handlerName,
            pOrder.splitMethod,pOrder.orderType,pOrder.price,pOrder.startTime,pOrder.endTime,
            pOrder.orderQty,pOrder.orderStatus,pOrder.timeoutNum,tempTime,tempTime)
    }
```

其中，母单的下单时间和最后更新时间字段，都赋值为使用 `getLastTime` 函数查询得到的最新快照时间。

* **updatePOrderManageInfo 更新母单最后修改时间**

`updatePOrderManageInfo` 函数用于修改母单的最后修改时间。

```
    //更新母单记录信息
    def updatePOrderManageInfo(pOrder,opTime){
        parentOrderManage=objByName('parentOrderManage')
        update parentOrderManage set sortNum = pOrder.sortNum,orderStatus=pOrder.orderStatus, lastUpdateTime = opTime where splitOrderId = pOrder.splitOrderId
    }
```

* **updateSubOrder 更新子单已成交量**

`updateSubOrder` 更新子单当前状态和已成交量，代码如下：

```
    // 更新子单当前状态和已成交量
    def updateSubOrder(Qty,status){
        // 如果传-1，则根据累计量更新，否则为全部成交，根据子单委托量更新
        tQty=0
        if(Qty==-1){
            tQty = transactionQty
        }else{
            tQty = Qty
        }
        subOrderTB = objByName('subOrderTb')
        // 查出应该修改的子单id，是最新的Limit单
        ids = exec top 1 tagBatchId from subOrderTB where orderType="Limit" order by lastUpdateTime desc
        id = ids[0]
        update subOrderTB set transactionQty = tQty,subOrderStatus = status where tagBatchId = id
    }
```

*Qty* 参数指定成交量，*status* 指定子单成交状态，`updateSubOrder`
将更新最新的 Limit 委托单的成交量和订单成交状态。每次调用该函数，Dashboard 中的子单成交量和订单成交状态会实时变化。

* **QtyAdd 累计子单部分成交量**

`QtyAdd` 作为子单部分成交事件监听器的回调函数，代码如下：

```
    // 累计部分成交
    def QtyAdd(subOrderPartTran){
        qty = subOrderPartTran.tradeQty
        transactionQty = transactionQty+qty
        // 更新子单状态和已成交量
        updateSubOrder(-1,"部分成交")
    }
```

`QtyAdd` 先根据部分成交事件的成交量，更新累计量 `transactionQty`
；然后调用`updateSubOrder` ，指定根据累计量
`transactionQty` 更新子单已成交量，更新子单状态为 `"部分成交"`
。

* **ifPlaceOrder 进行下一次拆单**

`ifPlaceOrder` 作为子单完全成交事件监听器的回调函数，为了避免函数调用本身，使用
`ifPlaceOrder` 函数调用 `placeOrder` 下单函数。

```
    // 接收到对应的成交单，进行下一次拆单
    def ifPlaceOrder(subOrderTran){
        // 注销部分成交监听
        QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)
        QtyAddListener = getEventListener(QtyAddListenerName)
        QtyAddListener.terminate()
        // 更新子单状态和已成交量
        subOrderTB = objByName('subOrderTb')
        // 查出委托量
        qtys = exec top 1 tradeQuantity from subOrderTB where orderType="Limit" order by lastUpdateTime desc
        qty = qtys[0]
        updateSubOrder(qty,"完全成交")
        writeLog("========接收到成交单======")
        // 归零已成交股数
        transactionQty = 0
        //最新的子单收到成交事件，启动下一次拆单
        placeOrder()
    }
```

`ifPlaceOrder` 函数逻辑如下：

1. 当子单完全成交事件注入 CEP ，代表子单已经完全成交。此时已不需要累计子单成交量，因此注销部分成交监听；
2. 子单完全成交事件注入 CEP ，代表成交量为子单委托量，因此查出对应委托量，并调用`updateSubOrder`
   ，指定根据委托量更新子单已成交量，更新子单状态为 `"完全成交"` ；
3. 归零 `transactionQty` 进行复用，用于下个子单的部分成交量累计；
4. 调用 `placeOrder` ，启动下一次拆单。

* **ifPlaceOrderLast 定义最后一次完全成交的逻辑**

`ifPlaceOrderLast` 作为最后一单中，子单完全成交事件监听器的回调函数，为了避免函数调用本身，使用
`ifPlaceOrder` 函数调用 `placeOrder` 下单函数。

```
    // 最后一次完全成交的逻辑
    def ifPlaceOrderLast(subOrderTran){
        // 注销部分成交监听
        QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)
        QtyAddListener = getEventListener(QtyAddListenerName)
        QtyAddListener.terminate()
        parentOrder.setAttr(`orderStatus,'下单完毕')
        tempTime = getLastTime()
        //保存母单信息
        updatePOrderManageInfo(parentOrder,tempTime)
        // 更新子单状态和已成交量
        subOrderTB = objByName('subOrderTb')
        // 查出委托量
        qtys = exec top 1 tradeQuantity from subOrderTB where orderType="Limit" order by lastUpdateTime desc
        qty = qtys[0]
        updateSubOrder(qty,"完全成交")
        //下单完结,销毁监视器
        destroyMonitor()
    }
```

`ifPlaceOrderLast` 函数逻辑如下：

1. 当子单完全成交事件注入 CEP ，代表子单已经完全成交。此时已不需要累计子单成交量，因此注销部分成交监听；
2. 子单完全成交事件注入 CEP ，代表成交量为子单委托量，因此查出对应委托量，并调用`updateSubOrder`
   ，指定根据委托量更新子单已成交量，更新子单状态为 `"完全成交"` ；
3. 最后一单完全成交，下单完毕，摧毁拆单监视器，停止下单。

* **cancelOrder 撤单**

若在规定时间内，没有接收到对应的子单完全成交事件，则将上一次下达的子单进行撤单，并下新的子单。

```
    // 下达撤单事件,将上一次的子单进行撤单，恢复子单已下总股数
    def cancelOrder(){
        // 注销部分成交监听
        QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)
        QtyAddListener = getEventListener(QtyAddListenerName)
        QtyAddListener.terminate()
        writeLog("========超时单======")
        oType = parentOrder.orderType
        subOrderTB = objByName('subOrderTb')
        subOrderFromStreams = exec top 1 * from subOrderTB where orderType = oType order by lastUpdateTime desc
        s = subOrderFromStreams.size()
        if(s==0){//还没有下子单
            return
        }
        // 拿到上一次下的子单
        subOrder = subOrderFromStreams[0]

        cancelOrderType = "cancel"
        // 查询现在的快照最新时间，作为撤单的下单时间
        cancelOrderPlaceTime = getLastTime()
        // 下达撤单到子单流表，这里撤单的id需要转换
        // 拿到当前需要撤单的子单的id
        tagBatchId = subOrder[`tagBatchId]
        tagBatchId = handleOrderId(tagBatchId)
        // 查出对应的系统id
        orderIds = exec top 1 orderId from outputTb where userOrderId = tagBatchId and orderStatus = 4
        if(orderIds == 0){
            writeLog("========不存在对应的未成交子单========")
            return
        }
        orderId = orderIds[0]

        // 使用累计成交量，计算应该撤单的量
        // 总量
        tQty = subOrder[`tradeQuantity]
        cQty = tQty - transactionQty
        insert into subOrderStream values(subOrder[`splitOrderId],subOrder[`batchId],orderId,subOrder[`sortNum],
        subOrder[`fundCode],subOrder[`fundName],subOrder[`assetId],subOrder[`assetName],
        subOrder[`combinationNo],subOrder[`combinationName],subOrder[`stockCode],subOrder[`stockName],
        subOrder[`tradeDate],cQty,subOrder[`tradeDirection],subOrder[`market],
        subOrder[`handlerEmpid],subOrder[`handlerName],cancelOrderType,subOrder[`price],
        cancelOrderPlaceTime);

        // 恢复子单总股数
        subOrderQtys = subOrderQtys-cQty
        // 更新子单状态和已成交量
        updateSubOrder(-1,"已撤单")
        // 归零已成交股数
        transactionQty = 0
        // 继续进行拆单下单
        placeOrder()
    }
```

`cancelOrder` 函数的逻辑如下：

1. 规定时间内，没有子单完全成交事件注入 CEP ，代表子单成交已经超时。此时已不需要累计子单成交量，因此注销部分成交监听；
2. 子单成交超时，下达撤单到子单流表 `subOrderStream` ，撤单量根据委托量和成交量计算得到；
3. 恢复子单总股数 `subOrderQtys` ，保证母单的已下单股数正确；
4. 调用 `updateSubOrder` ，更新子单成交状态为已撤单；
5. 归零 `transactionQty` 进行复用，用于下个子单的部分成交量累计；
6. 调用 `placeOrder` ，启动下一次拆单。

* **placeOrder 拆单核心函数**

`placeOrder` 函数用于拆单下单，函数代码如下：

```
    //Iceberg 下单方法
    def placeOrder(){
        writeLog("==========开始下单===========")
        //判断是否超过下单时限
        if(now()>= parentOrder.endTime){ //当前时间大于下单结束时间,则不再下单
            parentOrder.setAttr(`orderStatus,'时限中止')
            tempTime = getLastTime()
            updatePOrderManageInfo(parentOrder,tempTime)
            return
        }
        //判断当前母单状态是否是可以下单状态,不是则退出
        if(!(parentOrder.orderStatus in ['初始化','下单中'])){
            return
        }

        // 计算已经下过的单数
        totalQty = subOrderQtys
        //计算剩余待下单股数 = 母单股数 - 所有子单数，这里的子单数要保存到向量里
        remainQty = parentOrder.tradeQuantity - totalQty
        // 当前应该下的子单数
        subOrderQty = parentOrder.orderQty
        //子单数可能超过剩余单数
        subOrderQty = min(subOrderQty,remainQty)
        // 更新子单股数
        subOrderQtys = subOrderQtys+subOrderQty
        // 更新剩余单数
        remainQty = remainQty-subOrderQty

        // 拿到母单的基金代码
        v_securityId = parentOrder.fundCode
        // 直接从分布式表中进行查询，定义一个函数
        // 如果是买单，则使用买一价格挂单，如果是卖单，则使用卖一价格挂单
        if(parentOrder.tradeDirection == "S"){//从卖一价格获取
            // 从键值对表中获取
            OfferPrice = exec OfferPrice from snapshotOutputKeyedTb where SecurityID = v_securityId
            // 卖一价格
            subOrderPrice = OfferPrice[0]
        }else{//从买一价格获取
            // 从键值对表中获取
            BidPrice = exec BidPrice from snapshotOutputKeyedTb where SecurityID = v_securityId
            // 买一价格
            subOrderPrice = BidPrice[0]
        }

        //构建子单
        //创建子单时间
        // 查询现在的快照最新时间，作为撤单的下单时间
        subOrderPutTime = getLastTime()
        //构建下达子单到流表

        subOrderStream = objByName('subOrderStream')
        // 插入子单流数据表，初始已成交量为0，初始状态为等待成交
        insert into subOrderStream values(parentOrder.splitOrderId,parentOrder.batchId,
            parentOrder.splitOrderId+'_'+(parentOrder.sortNum+1),parentOrder.sortNum+1,
            parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
            parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
            parentOrder.tradeDate,subOrderQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
            parentOrder.handlerName,parentOrder.orderType,subOrderPrice,subOrderPutTime);
        //设置下单次数
        parentOrder.setAttr(`sortNum,parentOrder.sortNum+1)

        //判断是否还需继续下单
        if(remainQty>0){
            parentOrder.setAttr(`orderStatus,'下单中')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,subOrderPutTime)
            // 函数条件中不能使用类成员变量判断
            pOrder = parentOrder
            //超时时间
            timeoutN = parentOrder.timeoutNum
            timeoutTime = duration(timeoutN+"s")

            QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)

            // 监听部分成交事件，用于撤单量管理，这里不能指定匹配次数，需要一直监听，在完全成交或者撤单函数进行注销
            addEventListener(QtyAdd, "SubOrderPartTransaction", <SubOrderPartTransaction.splitOrderId = pOrder.splitOrderId>,"all",,,,,QtyAddListenerName)
            // 两个监听只会触发一个，相当于互相注销
            // 30s内有成交事件注入监听子单成交事件，触发一次后删除
            addEventListener(ifPlaceOrder, "SubOrderTransaction", <SubOrderTransaction.splitOrderId = pOrder.splitOrderId>,1,,,timeoutTime,,)
            // 监听超时，超过30s没有成交事件注入，则进行撤单，即将撤单放入子单流表
            addEventListener(cancelOrder, "SubOrderTransaction", <SubOrderTransaction.splitOrderId = pOrder.splitOrderId>,1,,,,timeoutTime,)
        }else{//最后一次下单，等待最后一单成交完毕，再设置下单完毕的状态
            parentOrder.setAttr(`orderStatus,'下单中')
            tempTime = getLastTime()
            //保存母单信息
            updatePOrderManageInfo(parentOrder,tempTime)
            // 函数条件中不能使用类成员变量判断
            pOrder = parentOrder
            //超时时间
            timeoutN = parentOrder.timeoutNum
            timeoutTime = duration(timeoutN+"s")

            QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)

            // 监听部分成交事件，用于撤单量管理，这里不能指定匹配次数，需要一直监听，在完全成交或者撤单函数进行注销
            addEventListener(QtyAdd, "SubOrderPartTransaction", <SubOrderPartTransaction.splitOrderId = pOrder.splitOrderId>,"all",,,,,QtyAddListenerName)
            // 两个监听只会触发一个，相当于互相注销
            // 30s内有成交事件注入监听子单成交事件，触发一次后删除，这里需要调用不同的回调，处理完全成交逻辑
            addEventListener(ifPlaceOrderLast, "SubOrderTransaction", <SubOrderTransaction.splitOrderId = pOrder.splitOrderId>,1,,,timeoutTime,,)
            // 监听超时，超过30s没有成交事件注入，则进行撤单，即将撤单放入子单流表
            addEventListener(cancelOrder, "SubOrderTransaction", <SubOrderTransaction.splitOrderId = pOrder.splitOrderId>,1,,,,timeoutTime,)
        }
    }
```

`placeOrder` 函数逻辑如下：

1. 判断当前时间是否超过拆单结束时间，若超过结束时间，则设置母单状态为 `'时限中止'`
   ，并调用`updatePOrderManageInfo` 函数更新母单最后修改时间。
2. 判断当前母单状态是否处于 `'初始化'` 或 `'下单中'`
   ，如果不满足，则停止拆单。
3. 根据成员变量 `subOrderQtys` 和母单属性
   `tradeQuantity` 计算剩余待下单股数 `remainQty`
   ，根据母单确定固定子单股数 `subOrderQty` ，并对
   `subOrderQtys` 和 `remainQty`
   进行更新。
4. 根据母单属性 `tradeDirection` 确定子单价格为买一还是卖一价格，并从键值内存表
   `snapshotOutputKeyedTb` 中查询。
5. 构建子单，并插入子单流表 `subOrderStream` 。
6. 根据剩余股数 `remainQty`
   判断是否是最后一单。若不是最后一单，则保存母单状态和修改时间，设置子单部分成交事件监听，回调函数为
   `QtyAdd` ，设置子单完全成交事件监听，回调函数为
   `ifPlaceOrder` ，设置子单成交超时监听，回调函数为
   `cancelOrder` ；若是最后一单，则保存母单状态和修改时间，设置子单部分成交事件监听，回调函数为
   `QtyAdd` ，设置子单完全成交事件监听，回调函数为
   `ifPlaceOrderLast` ，设置子单成交超时监听，回调函数为
   `cancelOrder` 。`ifPlaceOrderLast`
   中，定义最后一次完全成交的逻辑，然后摧毁监视器。

`placeOrder` 函数需要注意的点： `ifPlaceOrder`
、`cancelOrder` 和 `placeOrder` 会相互调用，而
`ifPlaceOrder` 、`cancelOrder` 函数定义在
`placeOrder` 前面。由于 DolphinDB 中函数调用前必须先定义，因此这里在监视器父类
`SplitMonitor` 中先将 `placeOrder`
函数进行声明。

#### 2.3.7 创建 CEP 引擎订阅流表

使用 `createCEPEngine` 函数创建 CEP 引擎，并使用
`subscribeTable` 函数使 CEP 引擎订阅异构流表
`orderBlobStream` ，`orderBlobStream` 中接收
`ParentOrder` 、 `OrderAlterAction` 、
`SubOrderTransaction` 和
`SubOrderPartTransaction` 事件流。

```
//创建下单任务引擎
dummy = table(1:0, `timestamp`eventType`blobs`splitOrderId, `TIMESTAMP`STRING`BLOB`STRING)
//创建cep 监听引擎
engine = createCEPEngine(name='IceBergSplitMonitor', monitors=<IceBergSplitMonitor()>, dummyTable=dummy, eventSchema=[ParentOrder,OrderAlterAction,SubOrderTransaction,SubOrderPartTransaction],timeColumn=`timestamp)

// 订阅异构流表
subscribeTable(tableName="orderBlobStream", actionName="orderBlobStream",handler=getStreamEngine("IceBergSplitMonitor"),msgAsTable=true)
```

#### 2.3.8 订阅成交回报

模拟撮合引擎中，撮合结果表 `outputTb` 定义为一个流数据表。本节订阅
`outputTb` ，当结果表中有新增部分成交或完全成交记录，构造对应的部分成交事件或完全成交事件注入 CEP
引擎，作为冰山算法的成交回报。代码如下：

```
//处理成交单id，返回一个向量，第一个元素是splitOrderId，第二个元素是subOrderID
def handleTransactionId(tIdNum){
    tId = string(tIdNum)
    s = tId.size()
    splitOrderId = substr(tId,0,13)
    s1 = s-13
    sortNum = substr(tId,13,s1)
    subOrderID = splitOrderId+"_"+sortNum
    return [splitOrderId,subOrderID]
}

// 定义事件流序列化器
streamEventSerializer("blobStreamEventSerializer",[ParentOrder,OrderAlterAction,SubOrderTransaction,SubOrderPartTransaction],objByName("orderBlobStream"),"eventTime","splitOrderId")

// 订阅撮合引擎的输出流表，当订单完全成交或者部分成交，将成交事件注入CEP引擎
// 订阅outputTb
def handleOutputTb(msg) {
    // 拿到最新的完全成交的订单ID
    data = exec top 1 userOrderId from msg where orderStatus = 1 order by tradeTime desc
    s = data.size()
    // 当size>0，构建成交单，注入CEP
    if(s>0){
        // 根据long类型的成交单id，构建出splitOrderId_，subOrderID_
        tId = data[0]
        IdVector = handleTransactionId(tId)
        // 构建成交单
        soTransaction = SubOrderTransaction(IdVector[0],"SubOrderTransaction",IdVector[1],now())
        // 注入CEP引擎（流表）
        appendEvent(`blobStreamEventSerializer,soTransaction)
        // 一次只注入完全成交单或者部分成交单
        return
    }

    // 拿到最新的部分成交的订单ID
    data = exec top 1 userOrderId,tradeQty from msg where orderStatus = 0 order by tradeTime desc
    s = data.size()
    // 当size>0，构建部分成交单，注入CEP
    if(s>0){
        // 根据long类型的成交单id，构建出splitOrderId_，subOrderID_
        tId = data[0][`userOrderId]
        IdVector = handleTransactionId(tId)
        tradeQty = data[0][`tradeQty]
        // 构建部分成交单
        sopTransaction = SubOrderPartTransaction(IdVector[0],"SubOrderTransaction",IdVector[1],tradeQty,now())
        // 注入CEP引擎（流表）
        appendEvent(`blobStreamEventSerializer,sopTransaction)
    }
}

// 订阅流表
subscribeTable(tableName = `outputTb,actionName=`handleOutputTb,handler = handleOutputTb,msgAsTable=true,batchSize = 1)
```

逻辑如下：

1. 定义事件流序列化器 `blobStreamEventSerializer`
   ，用于将部分成交事件和完全成交事件序列化，然后放入 CEP 引擎订阅的流表 `blobStream` 。
2. 订阅 `outputTb` ，查询新增的部分成交和完全成交记录，构造对应的成交事件，使用
   `blobStreamEventSerializer` 将成交事件放入
   `blobStream` ，从而注入 CEP 引擎。

#### 2.3.9 回放行情快照

使用 `replay` 回放历史行情数据，代码如下：

```
// 往行情流表里回放行情数据
snapshotTb = loadTable("dfs://l2TLDB_IceBerg","snapshot")
// 回放，选择需要的列
replayData = select Market,TradeDate,TradeTime,SecurityID,OfferPrice,BidPrice,OfferOrderQty,BidOrderQty,
                    LastPrice,UpLimitPx,DownLimitPx,TotalBidQty,TotalOfferQty
                    from snapshotTb where TradeTime>=09:30m
// 精确回放条回放
submitJob("replay_snapshot", "snapshot",  replay{replayData, snapshotStream, `TradeDate, `TradeTime, 1, false,,,true})
```

`replay` 函数中，通过指定 `preciseRate=true`
，`replayRate=1` 设置根据相邻两条快照记录时间戳的 1 倍速度精确回放，使得回放速度与历史快照表
`snapshot` 中快照记录的间隔时间相对应，更贴近市场的实际情况。

#### 2.3.10 策略启动

使用 DolphinDB 提供的 JAVA API ，将 `ParentOrder` 事件放入
`orderBlobStream` ，启动拆单策略。核心函数 `putOrder`
如下。完整的启动策略项目文件见附录。

```
    public static void putOrder() throws IOException, InterruptedException {

        //        连接dolphindb数据库
        DBConnection conn = DBUtil.getConnection();
        //        封装母单订阅流表
        EventSender sender1 = EventSenderHelperIceBerg.createEventSender(conn);
        //      拿到拆单参数map
        HashMap<String, Object> map = getMap();

        //        定义母单
        DolphinDbParentSplitParamsIceBergVo dolphinDbParentVo1 = new DolphinDbParentSplitParamsIceBergVo(
                "2025030500001",                    // splitOrderId: 母单拆单操作单元唯一ID
                "ParentOrder",                  // eventType: 事件类型
                "2025030500001",           // batchId: 母单唯一ID
                "",    // tagBatchId: 子单唯一ID
                0,                              // sortNum: 拆单顺序号（从1开始）
                "300041",                       // fundCode: 基金代码
                "蓝筹精选混合",                  // fundName: 基金名称
                "A123456789",                   // assetId: 资产单元ID
                "量化投资组合",                  // assetName: 资产单元名称
                "C789",                         // combinationNo: 组合编号
                "全天候策略",                    // combinationName: 组合名称
                "600000",                       // stockCode: 证券代码
                "浦发银行",                      // stockName: 证券名称
                "20231010",                     // tradeDate: 交易日期（yyyyMMdd）
                400000L,                         // tradeQuantity: 交易量（注意L后缀）
                "B",                            // tradeDirection: 交易方向（1-买入）
                "XSHE",                          // market: 交易市场
                "E1001",                        // handlerEmpid: 执行人工号
                "王强",                          // handlerName: 执行人姓名
                (String) map.get("splitMethod"),     // splitMethod: 拆单算法
                (String) map.get("orderType"),      // orderType: 订单类型
                (Double) map.get("price"),           // 子单下单价格
                (Integer) map.get("priceOption"),    //选择卖一价格下子单
                (Integer) map.get("orderQty"),    //子单股数
                (Integer) map.get("timeoutNum"),    //超时时间
                (LocalDateTime) map.get("startTime"),   // startTime: 拆单开始时间
                (LocalDateTime) map.get("endTime"),     // endTime: 拆单结束时
                "",                        // orderStatus: 拆单状态
                LocalDateTime.now()             // eventTime: 事件下达时间
        );

        //发送母单，将母单放入订阅流表，供CEP引擎消费
        sender1.sendEvent(dolphinDbParentVo1.getEventType(), dolphinDbParentVo1.toEntities());
        System.out.println("母单放入母单订阅流表");
    }
```

母单中的拆单参数，通过 `HashMap` 传入，模拟现实系统中的用户自定义拆单参数传递。

### 2.4 结果检视

本小节通过查看 Dashboard 中的输出事件展示拆单系统运行的结果。在本例中，母单事件、母单状态修改事件注入 CEP
引擎后，都分别记录到对应的内存表；子单下单到子单接收流表后，发布到子单内存表；模拟撮合引擎撮合委托单产生成交单、超时产生撤单，记录到撮合结果流表中。如此在
Dashboard 中便可以选取需要的数据进行可视化。

**step1-JAVA环境准备**

配置系统的 maven 、jdk 环境，本例中的 jdk 和 maven 版本如下：

```
jdk - java version "1.8.0_441"
maven - Apache Maven 3.8.6
```

**step2-数据准备**

下载附录中的冰山算法代码并解压。将 `data/snapshot_IceBerg.csv` 放到
`dolphindb/server` 目录下。运行导入脚本
`data/data_input_snapshot.dos` 进行建库建表，并将测试数据导入建好的分布式表中。运行
`data/loadMatchEngine.dos` ，加载模拟撮合引擎插件。将附录中的
`data/dashboard.IceBerg成交回报 拆单监控.json` 导入到 Dashboard 。

**step3-系统环境准备**

运行脚本 `01 clearEnv.dos` 、 `02 Event.dos` 、
`03 createTable.dos` 、`04
createMatchEngine.dos` 、`05 subscribeSnapshot.dos`
。`01 clearEnv.dos` 脚本将系统中已存在的内存共享表、订阅信息、流式引擎等进行清除，确保不会重复定义；
`02 Event.dos` 、 `03 createTable.dos` 、
`04 createMatchEngine.dos` 、`05
subscribeSnapshot.dos`
脚本分别对应上文介绍的定义事件类、创建内存表、创建模拟撮合引擎、订阅行情快照的功能。

**step4-订阅子单流表**

运行脚本 `06 subscribeSubOrder.dos` ，使得模拟撮合引擎订阅子单流表。

**step5-CEP引擎创建**

运行脚本 `07 Monitor.dos` 、`08 createCEPEngine.dos`
，分别对应上文中定义监视器、创建CEP引擎的功能。

**step6-订阅成交回报**

运行脚本 `09 subscribeTransactionOrder.dos` ，使得 CEP
引擎订阅模拟撮合引擎的撮合结果表，作为冰山算法的成交回报事件输入。

**step7-回放行情快照数据**

运行脚本 `10 replaySnapshot.dos` ，将快照数据回放到快照流表
`snapshotStream` 中。由于键值内存表
`snapshotOutputKeyedTb` 和模拟撮合引擎订阅了
`snapshotStream` ，数据会被自动同步发布到
`snapshotOutputKeyedTb` 和模拟撮合引擎中。

**step8-启动策略**

下载附录中的 JAVA API 策略启动代码并解压。修改 `common/DBUtil.java`
中的数据库配置为用户自己的环境。运行 `startIceBerg.java` ，将母单事件放入异构流表中，观察 Dashboard
中的对应输出。

![](images/order_splitting_with_cep_advanced/2_5.gif)

图 6. 图2-5 母单、子单、撮合结果动态图

* 将母单放入流表 `orderBlobStream` ，如图2-5 中的母单监控。母单买卖方向为
  `"B"` 即买单，委托总股数为 `400000` ，单个子单股数为
  `100000` ，成交超时限制为 `30s` ，即委托单超过 30s
  未完全成交，则撤单剩余股数。
* 系统开始拆单下单，母单拆单状态从 `“初始化”` 变为 `“下单中”` ，并将一个股数为
  `100000` 的限价单放入子单流表。子单委托价格指定为实时行情快照的买一价格。如图2-5
  中的子单监控。
* 模拟撮合引擎开始根据实时行情撮合委托单成交，撮合结果显示到撮合结果表，如图2-5
  中的撮合成交监控。撮合记录根据成交或者撤单时间倒序显示，便于观测最新的撮合情况。
* 图2-5
  中的子单监控能根据成交量和子单状态实时观测子单成交情况，子单记录根据下单时间倒序显示，便于观测最新子单的成交情况。若超时未完全成交，则撤销剩余股数的委托单，并下新的委托子单；当子单（委托单）在规定时间内完全成交，则直接下新的委托子单。
* 当子单成交量达到母单总股数 400000 ，停止拆单下单，母单状态从 `“下单中”` 变为
  `“下单完毕”` 。

### 2.5 总结

本章通过循序渐进的方式，介绍了如何使用 DolphinDB 的
CEP引擎和模拟撮合引擎，实现冰山算法接入模拟撮合引擎。首先说明了算法思想；然后模块化介绍了系统的功能；其次详细介绍了系统的实现流程和代码，其中最复杂的是监视器定义的部分，详细阐述了各个函数之间的调用关系；最后将系统的拆单、撮合成交过程，在结果检视部分使用
Dashboard 进行展示。

## 3. 自定义套利下单

### 3.1 算法思想

#### 3.1.1 股指期货套利

无风险套利是指通过实时捕捉期货与现货指数之间的定价偏差，同步建立方向相反的对冲头寸（如升水时卖出期货/买入现货指数，贴水时买入期货/卖空现货指数），利用市场力量驱动价格回归的特性，在价差收敛时平仓锁定无风险利润。

![](images/order_splitting_with_cep_advanced/3_1.png)

图 7. 图3-1 股指、期货行情示意图

图3-1是回放的沪深300股指期货在某段时间内的 `LastPrice` 走势图，红色折线表示指数
`LastPrice` ，绿色折线表示期货 `LastPrice` ，市场会驱使
`LastPrice_hs300Index` 和
`LastPrice_hs300Futures`
回归。因此当价差比例大于一定值（图中黄色矩形框），判定存在套利空间，此时购入现货指数；当价差比例小于一定值（图中蓝色矩形框），判定两者价格回归完成，指数价格达到高点，此时卖空本轮买入的现货指数，即可实现无风险套利。图中沪深
300 股指和沪深 300 期货，每次价格偏离（图中黄色矩形框）再回归（图中蓝色矩形框）都可能存在套利空间，可以进行一轮套利。

与单向投机依赖价格涨跌不同，套利的核心在于消除市场方向性风险，纯粹依赖价差修复获利；其有效性高度依赖高速算法实时监控基差、精确计算交易成本（手续费、融券利息）及快速执行能力，适用于分红季贴水扩大、跨期合约价差异常等短期定价失效场景。本例展示的是在不考虑手续费等额外费用的情况下，单纯根据价差进行套利，用户可以参考本例根据自己的应用场景进行完善。

#### 3.1.2 模拟撮合引擎

与冰山算法 [模拟撮合引擎](#topic_w5w_qjv_fgc)
相似，本例中也接入模拟撮合引擎。将指数委托买单、指数委托卖单和指数实时行情信息注入模拟撮合引擎，并接收成交回报事件，最终计算每个订单的套利所得利润。

### 3.2 功能模块

套利下单算法逻辑通过 CEP 引擎实现；通过数据回放功能，模拟股指、期货实时行情数据写入；使用流表订阅功能解耦用户母单发布和套利下单 CEP
引擎；将快照行情、子单流表中的委托单、撤单注入模拟撮合引擎，模拟真实的市场交易；将撮合结果构造为成交事件注入 CEP
引擎，作为算法的成交回报；接收到成交回报后，计算每个订单各自所得利润。大致流程如下图所示。

![](images/order_splitting_with_cep_advanced/3_2.png)

图 8. 图3-2 算法流程图

套利下单算法的算法流程与冰山算法相似，区别有以下几点。

* 套利下单同样接入模拟撮合引擎插件，将指数快照行情数据、子单流表中的指数委托订单和撤单，注入模拟撮合引擎，模拟现实市场的订单成交。但委托订单既有买单也有卖单，低买高卖获取无风险套利利润。
* CEP 引擎中新增事件类 `HS300Index` 、`HS300Futures`
  ，并定义为成员变量，分别存储实时的股指、期货行情数据；本例中价差使用 `lastPrice`
  字段计算，当价差大于指定值时，根据股指实时的 `lastPrice` 下委托买单，并监听成交、超时事件；新增事件类
  `ratioLow` ，当价差小于指定值时，将`ratioLow` 事件注入 CEP
  引擎，将本轮的成交的买单，根据股指实时的 `lastPrice` 挂单卖出，并监听成交事件计算套利利润。
* 下单指数买单后，会监听成交、超时事件，当本轮指数价格达到高点（股指期货价差小于指定值），会撤单本轮未成交的买单剩余股数；而下单卖单后，只监听成交事件，以期获得更多套利利润。

### 3.3 代码实现

在本节我们介绍套利下单的代码实现。

#### 3.3.1 定义事件类

* 定义沪深300指数行情类和沪深300期货行情类，这两个类有相同的字段：

```
splitOrderId :: STRING         // 母单拆单操作单元唯一ID
eventType :: STRING            // 事件类型
TradeDate :: DATE              // 交易日期
TradeTime :: TIME              // 交易时间
SecurityID :: STRING           // 股票代码
OpenPrice :: DOUBLE            // 开盘价格
LastPrice :: DOUBLE            // 最新价格
PreClosePrice :: DOUBLE         // 昨日收盘价
eventTime :: TIMESTAMP         // 事件下达时间
```

其中各个字段的含义见每行注释。股指和期货的价差使用 `LastPrice` 字段来计算，同时子单的价格也限价为指数的实时
`LastPrice` 。

* 定义母单类，拆单参数如下：

```
//拆单参数开始
splitMethod :: STRING          // 拆单算法
orderType :: STRING            // 订单类型（限价/市价）
orderQty :: INT                // 子单股数
timeoutNum :: INT              // 超时时间（秒）
startTime :: TIMESTAMP         // 拆单开始时间
endTime :: TIMESTAMP           // 拆单结束时间
orderStatus :: STRING          // 拆单状态
```

其中，`orderQty`
代表子单的固定股数，每次价差大于指定值，下指定股数的子单；`timeoutNum`
表示每个买单的超时时间，如果超时还未完全成交，则会撤单未成交股数。

* 定义子单成交类，与冰山算法不同，子单成交类使用字段 `transactionType`
  来区分部分成交和完全成交：

```
splitOrderId :: STRING         //操作的母单号
eventType :: STRING          // 事件类型
transactionType :: STRING   // 成交类型（all: 完全成交；part :部分成交）
subOrderID :: STRING     // 子单唯一ID，对应子单流表中的tagBatchId
tradeQty :: INT          // 成交量
tradePrice :: DOUBLE    // 成交价格
eventTime :: TIMESTAMP   // 下达子单成交时间
```

其余字段含义见注释。

* 定义价差回归类，表示价差小于指定值：

```
splitOrderId :: STRING         //操作的母单号
eventType :: STRING          // 事件类型
price :: DOUBLE            // 卖单价格
eventTime :: TIMESTAMP   // 下达子单成交时间
```

`price` 字段表示价差小于指定值时，指数的 `LastPrice`
值，用于确定卖单价格。

* 定义存储一轮套利的买单 id 的自定义 `mySet` 类：

```
// 存储子单id的set，使用自定义类
class mySet{
    ids :: STRING VECTOR
    def mySet(ids_){
        ids = ids_
    }
    def clear(){
        ids = array(STRING,0)
    }
    def appendId(newId){//不能添加重复元素
        // 先检查数组中有无id
        for(id in ids){
            if(id==newId){
                return
            }
        }
        ids.append!(newId)
    }
}
```

向 `mySet` 类的数组中添加买单 id 时，会先检查数组中有无对应值，没有对应值才会添加，起到 id
排重的作用。

#### 3.3.2 创建表

* 定义母单记录内存表、子单接收流表：

```
//创建母单记录内存表
colNames=["splitOrderId","eventType","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","tradeDirection","market","handlerEmpid","handlerName","splitMethod","orderType","startTime","endTime","orderQty","orderStatus","timeoutNum","eventTime","lastUpdateTime"]
colTypes=[STRING,SYMBOL,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,SYMBOL,TIMESTAMP,TIMESTAMP,INT,SYMBOL,INT,TIMESTAMP,TIMESTAMP]
share table(1:0,colNames,colTypes) as parentOrderManage

// 创建子单接收流数据表
colNames=["splitOrderId","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","tradeDirection","market","handlerEmpid","handlerName","orderType","price","lastUpdateTime"]
colTypes=[STRING,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,DOUBLE,TIMESTAMP]
share streamTable(1:0, colNames, colTypes) as subOrderStream
```

字段含义同冰山算法。

* 创建指数持有表，存储成功买入的指数现货，并记录买入卖出记录，还会实时更新卖出后得到的利润：

```
colNames=["splitOrderId","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","saleQty","tradeDirection","market","handlerEmpid","handlerName","orderType","price","salePrice","profit","lastUpdateTime"]
colTypes=[STRING,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,INT[],INT[],SYMBOL,SYMBOL,STRING,STRING,SYMBOL,DOUBLE[],DOUBLE[],DOUBLE,TIMESTAMP]
colTypes.size()
share table(1:0, colNames, colTypes) as purchasedIndexTb
```

`tradeQuantity` 、`saleQty`
用两个数组记录买入和卖出的股数情况；`price` 、`salePrice`
用两个数组记录买入和卖出的成交价格；`profit`
实时更新该订单获得的利润；`orderType` 实时更新订单的套利情况。

#### 3.3.3 定义监视器

CEP 引擎内部监视器的配置，是套利下单系统实现中最关键的步骤。监视器内封装了整个套利下单策略，其结构大致如下。

```
//套利拆单算法下单监听 monitor
class arbiSplitMonitor:CEPMonitor{
    // 母单属性
    parentOrder :: ParentOrder
    // 沪深300指数行情
    hs300Index :: HS300Index
    // 沪深300期货行情
    hs300Futures :: HS300Futures
    // 是否能下单的标志位
    canOrder :: BOOL
    // 卖单顺序号，和母单的拼接应该先拼上0，再拼上顺序号，和买单id区分
    sNum :: INT
    // ratioLow事件监听器顺序号，用于监听器命名
    ratioLowNum :: INT
    // 子单id数组，存储每个套利轮，买到的子单id，每次挂单卖出时清空
    subOrderIds :: mySet

    def arbiSplitMonitor() {
        //本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
    }

    // 处理日期和时间，使其返回一个年月日，时分秒的向量
    def handleCompleteTime(dt,ti){...}

    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){...}

    //更新母单记录信息
    def updatePOrderManageInfo(pOrder){...}

    // 累计部分成交接收到部分成交后，先检查持有表中是否有对应子单，如果有，则对持有量进行变更，否则新增记录
    def QtyAdd(subOrderPartTran){...}

    // 卖单和买单id转换
    def saleID2buyID(saleID){...}

    // 买单和卖单id转换
    def buyID2saleID(buyID){...}

    def saleQtyAdd(subOrderPartTran){...}

    // 当有完全成交事件注入，更新持有表，更新买单id数组
    def ifPlaceOrder(subOrderPartTran){...}

    // 卖单完全成交事件
    def saleIfPlaceOrder(subOrderPartTran){...}

    // 子单id，引擎内部需要long类型，用字符切割，拼成子单id
    def handleOrderId(x){...}

    // 当超时后，先注销部分成交监听，然后将撤单放入子单流表
    def cancelOrder(){...}

    // 根据id撤单，由于这里还在等待该子单成交或超时，所以这里应该注销对应的三个买单监听
    def cancelOrderById(id,qty){...}

    // 套利下单卖单函数，卖单Id与买单id只差一个0
    // 对数组内每个id，如果无成交和部分成交，需要撤单，并销毁对应的所有监听器
    // 监听器名称：根据子单id得到对应的sortNum，然后拼接对应的监听器名称
    def saleIndex(price){...}

    def ratioLowHandler(lowRatio){...}

    //套利下单买单函数
    def placeOrder_hs300_arbitrage(){...}

    // 沪深30指数
    def HS300IndexHandler(hs300IndexEvent){...}

    // 沪深300期货
    def HS300FuturesHandler(hs300FuturesEvent){...}

    //初始化sub monitor
    def startPlaceOrder(pOrder){...}

    //创建母单下单sub-monitor实例
    def forkParentOrderMonitor(pOrder){...}

    //初始任务
    def onload(){
        addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
    }
}
```

成员变量 `parentOrder` ：记录当前母单的属性值。

成员变量 `hs300Index` ：实时记录当前指数的行情信息。

成员变量 `hs300Futures` ：实时记录当前期货的行情信息。

成员变量 `canOrder`
：能否下买单的标志位。在一轮套利中，上一个买单成交后，才能继续下买单；当卖空指数平仓获利时，不能继续下买单。

成员变量 `sNum` ：卖单顺序号，和母单中的 `sortNum`
字段作用类似。且买单和卖单 id 存在对应关系，可以互相转换。

成员变量 `ratioLowNum` ：顺序号，用于监听价格回归事件的监听器命名。

成员变量 `subOrderIds` ：记录每一轮套利的所有买单 id ，当平仓获利时，用于下达对应的卖单。

* **onload 初始任务**

创建引擎并实例化监视器后，将首先调用其内部的 `onload` 函数。在 `onload`
函数中，使用 `addEventListener` 函数监听 `ParentOrder`
事件注入，指定回调函数为 `forkParentOrderMonitor` ，事件类型是
`ParentOrder` ，设置监听次数为持续监听。

```
    //初始任务
	def onload(){
		addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
	}
```

`onload` 方法设置了一个事件监听器，监听所有的母单事件 `ParentOrder`
。当监听到该类型事件时，下一步将启动整个套利下单过程。从 `onload`
方法开始，函数调用的流程与实现的功能可以分为三个模块，如下图所示。

![](images/order_splitting_with_cep_advanced/3_3.png)

图 9. 图3-3 函数调用模块图

接下来从策略启动事件对应的回调函数 `forkParentOrderMonitor` 开始来介绍具体的代码实现。

* **forkParentOrderMonitor 生成监视器实例**

CEP 引擎内的初始 Monitor 只负责监控策略启动事件注入，参考上文的 `onload` 函数。每当
`onload` 函数监测到新的 `ParentOrder` 事件注入，调用
`forkParentOrderMonitor` 生成一个新的 sub-Monitor
实例，进行当前委托单的套利下单操作。

```
    //创建母单下单sub-monitor实例
	def forkParentOrderMonitor(pOrder){
        writeLog("@@@@@@@@@@@@@@@@@@@arbiTradeSplitMonitor-forkParentOrderMonitor+ in")
        spawnMonitor(pOrder.splitOrderId + "_forksubMonitor",startPlaceOrder, pOrder)
	}
```

`forkParentOrderMonitor` 中，使用 DolphinDB 的
`spawnMonitor` 函数，生成一个 sub-Monitor 实例，并调用
`startPlaceOrder` 方法，并将注入的 `ParentOrder`
事件 `pOrder` 传入。启动后续核心模块。

* **startPlaceOrder****启动核心模块**

`startPlaceOrder` 函数中，包含了模块2、模块3的启动步骤，实现代码如下：

```
    //初始化sub monitor
    def startPlaceOrder(pOrder){
        // 标志位初始化
        canOrder = true
        sNum = 0
        ratioLowNum = 1
        // 排重向量
        subOrderIds = mySet(array(STRING,0))
        // demo 构造一个初始化对象，生产场景可以加载前一天最后数据
        indexEvent = HS300Index(
            `2025030500001,
            `HS300Index,
            2026.02.01,
            09:30:00.000,
            "510300",
            4.1640,
            4.1640,
            4.1590,
            now()
        )
        // 初始化类成员变量
        hs300Index = indexEvent

        futuresEvent = HS300Futures(
            `2025030500001,
            `HS300Futures,
            2026.02.01,
            09:30:00.000,
            "IF2406",
            89.00,
            69.98,
            92.09,
            now()
        )
        // 初始化类成员变量
        hs300Futures = futuresEvent

        //设置当前子任务 monitor 对象的内部母单变量
        parentOrder = pOrder
        //拆单初始化
        parentOrder.setAttr(`orderStatus,'初始化')
        parentOrder.setAttr(`sortNum,0)  //拆单顺序号
        //保存母单状态
        initPOrderManageInfo(parentOrder)

        //创建沪深300指数数据监听
        addEventListener(HS300IndexHandler, "HS300Index", ,"all")
        //创建沪深300期货数据监听
        addEventListener(HS300FuturesHandler, "HS300Futures", ,"all")
    }
```

包含的步骤如下：

1. 对 CEP 类成员变量 `canOrder` 、`sNum`
   、`ratioLowNum` 、`subOrderIds`
   、`hs300Index` 、`hs300Futures`
   、`parentOrder` 进行初始化。
2. 对拆单状态和顺序号进行初始化。
3. 保存母单信息到母单内存表。
4. 建立沪深300指数行情事件、沪深300期货行情事件监听，回调函数分别为 `HS300IndexHandler`
   、`HS300FuturesHandler` 。

* **initPOrderManageInfo 初始记录母单信息**

`initPOrderManageInfo` 函数被 `startPlaceOrder`
函数调用，实现代码如下：

```
    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){
        parentOrderManage=objByName('parentOrderManage')
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        insert into parentOrderManage values(
            pOrder.splitOrderId,pOrder.eventType,pOrder.batchId,pOrder.tagBatchId,pOrder.sortNum,
            pOrder.fundCode,pOrder.fundName,pOrder.assetId,pOrder.assetName,pOrder.combinationNo,
            pOrder.combinationName,pOrder.stockCode,pOrder.stockName,pOrder.tradeDate,pOrder.tradeQuantity,
            pOrder.tradeDirection,pOrder.market,pOrder.handlerEmpid,pOrder.handlerName,
            pOrder.splitMethod,pOrder.orderType,pOrder.startTime,pOrder.endTime,
            pOrder.orderQty,pOrder.orderStatus,pOrder.timeoutNum,lastTime,lastTime)
    }
```

该函数用于将母单记录插入母单内存表，但下单时间设置为当前的快照时间。

* **updatePOrderManageInfo 更新母单信息**

`updatePOrderManageInfo` 函数用于更新母单的基本信息，实现步骤如下：

```
    //更新母单记录信息
    def updatePOrderManageInfo(pOrder){
        parentOrderManage=objByName('parentOrderManage')
        opTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        update parentOrderManage set sortNum = pOrder.sortNum,orderStatus=pOrder.orderStatus, lastUpdateTime = opTime where splitOrderId = pOrder.splitOrderId
    }
```

该函数是对母单内存表的记录进行更新，更新时间也设置为当前的快照时间。

* **handleCompleteTime 得到完整时间**

`handleCompleteTime` 函数处理一个日期参数和一个时间参数，返回一个完整的时间，实现代码如下：

```
    // 处理日期和时间，使其返回一个年月日，时分秒的向量
    def handleCompleteTime(dt,ti){
        // 拼接
        tempTimeStr = dt+" "+ti+"000"
        // 转换
        tempTime = temporalParse(tempTimeStr,"yyyy.MM.dd HH:mm:ss.nnnnnn")
        // 赋值
        return tempTime
    }
```

步骤如下：

1. 使用字符串拼接，拼接出完整的时间字符串。
2. 使用 `temporalParse` 系统函数，转换为特定格式并返回。

* **HS300IndexHandler 处理沪深300指数行情事件**

当沪深300指数事件注入 CEP 引擎，调用 `HS300IndexHandler` 函数进行处理。实现代码如下：

```
    // 沪深30指数
    def HS300IndexHandler(hs300IndexEvent){
        // 更新沪深300指数信息
        hs300Index = hs300IndexEvent
        // 检查时间
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        // 检查是否回放完毕，如果回放完毕，摧毁监视器，将母单状态设置为套利完成
        if(lastTime==2026.02.01 09:39:58){
            parentOrder.setAttr(`orderStatus,'套利完成')
            //保存母单信息
            updatePOrderManageInfo(parentOrder)
            //下单完结,销毁监视器
            destroyMonitor()
            return
        }
        // 检查ratio
        ratio = (hs300Futures.LastPrice - hs300Index.LastPrice)/hs300Index.LastPrice
        if(ratio<=0.0005){
            price = hs300Index.LastPrice
            lowRatioEvent = ratioLow("2025030500001","ratioLow",price,now())
            appendEvent(`blobStreamEventSerializer,lowRatioEvent)
        }
        // 判断是否触发下单
        placeOrder_hs300_arbitrage()
    }
```

步骤如下：

1. 将注入的指数行情事件赋值给类成员变量 `hs300Index` 。
2. 检查时间是否结束。由于本例回放十分钟的股指期货行情，因此当到达特点时间回放完成，套利运行结束，此时需要将母单状态设置为
   `'套利完成'` ，并摧毁监视器。
3. 检查利差是回归，如果利差小于 0.0005 ，则将回归事件注入 CEP 引擎。
4. 判断是否触发下单。

* **HS300FuturesHandler 处理沪深300期货行情事件**

`HS300FuturesHandler` 处理期货行情事件，实现代码如下：

```
    // 沪深300期货
    def HS300FuturesHandler(hs300FuturesEvent){
        // 更新沪深300期货信息
        hs300Futures = hs300FuturesEvent
    }
```

即将注入的期货行情事件，赋值给成员变量 `hs300Futures` 。

* **placeOrder\_hs300\_arbitrage 下委托买单**

`placeOrder_hs300_arbitrage` 函数被
`HS300IndexHandler` 调用，实现代码如下：

```
    //套利下单买单函数
    def placeOrder_hs300_arbitrage(){
        ratio = (hs300Futures.LastPrice - hs300Index.LastPrice)/hs300Index.LastPrice

        // 下单条件，加上标志位的限制
        if (ratio >= 0.0014 && canOrder == true) {
            // 下一个子单
            // 获取指数的最新时间，调用handleCompleteTime
            lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
            subOrderStream = objByName('subOrderStream')
            // 买单Id
            tbId = parentOrder.splitOrderId+'_'+(parentOrder.sortNum+1)
            // 插入子单流表
            insert into subOrderStream values(parentOrder.splitOrderId,parentOrder.batchId,
            tbId,parentOrder.sortNum+1,
            parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
            parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
            parentOrder.tradeDate,parentOrder.orderQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
            parentOrder.handlerName,parentOrder.orderType,hs300Index.LastPrice,lastTime);
            // 标志位变更，等待买单成交
            canOrder = false
            // 更新数组
            subOrderIds.appendId(tbId)
            //设置下单次数
            parentOrder.setAttr(`sortNum,parentOrder.sortNum+1)
            parentOrder.setAttr(`orderStatus,'下单中')
            //保存母单信息
            updatePOrderManageInfo(parentOrder)
            //超时时间
            timeoutN = parentOrder.timeoutNum
            timeoutTime = duration(timeoutN+"s")

            QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)
            // 监听成交，将成功买入的股票放入持有的股票内存表中
            // 监听部分成交事件，用于撤单量管理。当利差缩小到指定范围时，需要撤单未成交的股数
            partstr = "part"
            allstr = "all"
            writeLog("=========定义买单监听器=========")
            addEventListener(QtyAdd, "SubOrderTransaction", <SubOrderTransaction.transactionType = partstr && SubOrderTransaction.subOrderID = tbId>,"all",,,,,QtyAddListenerName)
            // 两个监听只会触发一个，相当于互相注销
            // 30s内有完全成交事件注入监听子单成交事件，触发一次后删除
            ifPlaceOrderListenerName = "ifPlaceOrderListener"+"_"+string(parentOrder.sortNum)
            addEventListener(ifPlaceOrder, "SubOrderTransaction", <SubOrderTransaction.transactionType = allstr && SubOrderTransaction.subOrderID = tbId>,1,,,timeoutTime,,ifPlaceOrderListenerName)
            // 监听超时，超过30s没有完全成交，则进行撤单，即将撤单放入子单流表
            cancelOrderListenerName = "cancelOrderListener"+"_"+string(parentOrder.sortNum)
            addEventListener(cancelOrder, "SubOrderTransaction", <SubOrderTransaction.transactionType = allstr && SubOrderTransaction.subOrderID = tbId>,1,,,,timeoutTime,cancelOrderListenerName)

            // 每一轮开始，才需要创建一个lowRatio监听，当利差满足条件，调用处理函数
            // 这时子单id列表只有一个元素
            s = subOrderIds.ids.size()
            if(s==1){
                lName = "ratioLowListener_"+string(ratioLowNum)
                addEventListener(ratioLowHandler, "ratioLow",,"all",,,,,lName)
            }
        }
    }
```

实现步骤如下：

1. 计算此时的沪深300指数和期货价差比例 `ratio` 。
2. 若此时价差不够高或 `canOrder` 为 `false` ，则不进行下单。
   `canOrder` 为 `false`
   代表上一个买单还未成交，或者此时正在卖出指数现货进行平仓获利。
3. 如果此时价差和 `canOrder` 都满足条件，则进行下单。将买单插入子单流表，并将
   `canOrder` 设置为 `false` 等待该买单成立。将买单 id
   加入 id 数组 `subOrderIds` 。
4. 更新母单信息，即下单次数 `sortNum` ，下单状态，最后更新时间。
5. 根据超时时间 `timeoutNum` 、下单次数 `sortNum`
   设置当前买单的三个监听器。即部分成交监听、完全成交监听和超时监听。
6. 如果这是当前套利轮第一次下买单，则设置价差回归事件监听。

* **QtyAdd 累计买单部分成交量**

`QtyAdd` 函数用于处理买单的部分成交事件，实现代码如下：

```
    // 累计部分成交接收到部分成交后，先检查持有表中是否有对应子单，如果有，则对持有量进行变更，否则新增记录
    def QtyAdd(subOrderPartTran){
        qty = subOrderPartTran.tradeQty
        id = subOrderPartTran.subOrderID
        writeLog("========部分成交事件============"+id)
        tPrice = subOrderPartTran.tradePrice
        subOrders = select * from purchasedIndexTb where tagBatchId=id
        s = subOrders.size()
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        if(s==0){//新增持有表记录
            bQty = array(INT[],0)
            bQty.append!(qty)
            sQty = array(INT[],0)
            sQty.append!(0)
            bPrice = array(DOUBLE[],0)
            bPrice.append!(tPrice)
            sPrice = array(DOUBLE[],0)
            sPrice.append!(0)
            insert into purchasedIndexTb values(
                parentOrder.splitOrderId,parentOrder.batchId,
                id,parentOrder.sortNum,
                parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
                parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
                parentOrder.tradeDate,bQty,sQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
                parentOrder.handlerName,"买部分成交",bPrice,sPrice,0,lastTime)
        }else{//更新持有量，更新买入股数的数组和价格数组
            // 先查出买入股数的数组和价格数组
            indexs = select tradeQuantity,price from purchasedIndexTb where tagBatchId=id
            bQty = indexs[0][`tradeQuantity]
            bPrice = indexs[0][`price]
            bQtyu = append!(bQty,qty)
            bPriceu = append!(bPrice,tPrice)
            update purchasedIndexTb set tradeQuantity = bQtyu,price = bPriceu,orderType = "买部分成交",lastUpdateTime = lastTime where tagBatchId=id
        }
    }
```

该函数根据买单 id ，检查持有表中是否有对应的订单。如果不存在，则新增记录，并将部分成交的股数、价格写入数组；如果存在，则进行更新。

* **ifPlaceOrder 处理买单完全成交事件**

`ifPlaceOrder` 函数用于处理买单完全成交事件。实现代码如下：

```
    // 当有完全成交事件注入，更新持有表
    def ifPlaceOrder(subOrderPartTran){

        id = subOrderPartTran.subOrderID
        writeLog("========完全成交事件============"+id)
        // 更新表记录
        tPrice = subOrderPartTran.tradePrice
        // 拿到下单量
        qty = subOrderPartTran.tradeQty
        subOrders = select * from purchasedIndexTb where tagBatchId=id
        s = subOrders.size()
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        if(s==0){//新增持有表记录
            bQty = array(INT[],0)
            bQty.append!(qty)
            sQty = array(INT[],0)
            sQty.append!(0)
            bPrice = array(DOUBLE[],0)
            bPrice.append!(tPrice)
            sPrice = array(DOUBLE[],0)
            sPrice.append!(0)
            writeLog("==========开始插入持有表")
            insert into purchasedIndexTb values(
                parentOrder.splitOrderId,parentOrder.batchId,
                id,parentOrder.sortNum,
                parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
                parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
                parentOrder.tradeDate,bQty,sQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
                parentOrder.handlerName,"买完全成交",bPrice,sPrice,0,lastTime)
            writeLog("==========插入持有表完成")
        }else{//更新持有量，更新买入股数的数组和价格数组
            // 先查出买入股数的数组和价格数组
            indexs = select tradeQuantity,price from purchasedIndexTb where tagBatchId=id
            bQty = indexs[0][`tradeQuantity]
            bPrice = indexs[0][`price]
            bQtyu = append!(bQty,qty)
            bPriceu = append!(bPrice,tPrice)
            update purchasedIndexTb set tradeQuantity = bQtyu,price = bPriceu,orderType = "买完全成交",lastUpdateTime = lastTime where tagBatchId=id
        }
        // 标志位变更
        canOrder = true
    }
```

实现步骤如下：

1. 根据买单 id ，检查持有表中是否有对应的订单。如果不存在，则新增记录，并将完全成交的股数、价格写入数组；如果存在，则进行更新。
2. 将标志位 `canOrder` 设置为 `false`
   ，即当前买单完全成交后，如果利差大于指定值，可以继续委托买单。

* **cancelOrder 处理买单成交超时事件**

当买单超过规定时间还没完全成交，需要撤销剩余股数。实现代码如下：

```
    // 处理买单成交超时
    def cancelOrder(){

        // 将撤单放入子单流表，撤单id，从子单流表中获取，撤单最新的买单
        ids = exec top 1 tagBatchId,tradeQuantity from subOrderStream where tradeDirection = "B" order by lastUpdateTime desc
        id = ids[0][`tagBatchId]
        writeLog("========超时事件============"+id)

        // 注销部分成交监听
        // 这里listenerName需要根据子单id得到，因为sortNum变化了（下了其他子单，和冰山不同）
        QtyAddListenerName = "QtyAddListener"+"_"+string(parentOrder.sortNum)
        QtyAddListener = getEventListener(QtyAddListenerName)
        QtyAddListener.terminate()

        qty = ids[0][`tradeQuantity]
        // 查出对应的撤单id
        id2long = handleOrderId(id)
        orderIds = exec top 1 orderId from outputTb where userOrderId = id2long and orderStatus = 4
        orderId = orderIds[0]
        cancelOrderPlaceTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)

        // 撤单这里还是需要填写
        // 撤单的股数计算，这里qty是总下单股数，成交股数从持有表中查询
        qtys = select tradeQuantity from purchasedIndexTb where tagBatchId=id
        if(qtys.size()==0){
            qty1=0
        }else{
            qtyV = qtys[0][`purchasedIndexTb]
            qty1 = sum(qtyV)
        }
        cancelQty = qty-qty1
        // 将撤单加入子单流表
        insert into subOrderStream values(parentOrder.splitOrderId,parentOrder.batchId,orderId,parentOrder.sortNum,
        parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
        parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
        hs300Index.TradeDate,cancelQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
        parentOrder.handlerName,"cancel",0,cancelOrderPlaceTime);
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        // 更新持有表的状态，这里持有表可能没有，也需要检查
        subOrders = select * from purchasedIndexTb where tagBatchId=id
        s = subOrders.size()
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        if(s==0){//新增持有表记录
            bQty = array(INT[],0)
            bQty.append!(0)
            sQty = array(INT[],0)
            sQty.append!(0)
            bPrice = array(DOUBLE[],0)
            bPrice.append!(0)
            sPrice = array(DOUBLE[],0)
            sPrice.append!(0)
            writeLog("==========开始插入持有表")
            insert into purchasedIndexTb values(
                parentOrder.splitOrderId,parentOrder.batchId,
                id,parentOrder.sortNum,
                parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
                parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
                parentOrder.tradeDate,bQty,sQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
                parentOrder.handlerName,"买已撤单",bPrice,sPrice,0,lastTime)
            writeLog("==========插入持有表完成")
        }else{
            update purchasedIndexTb set orderType = "买已撤单",lastUpdateTime = lastTime where tagBatchId=id
        }
    }
```

实现步骤如下：

1. 从子单流表中查询应该撤单的买单 id 。由于当前买单完全成交，或者超时撤单后，才会委托下一个买单，因此需要撤单的买单 id
   是子单流表中，最新的买单的 id 。
2. 注销当前买单的部分成交监听。
3. 根据查询的买单 id ，从模拟撮合引擎输出表中查询撤单 id。
4. 计算需要撤单的股数。撤单股数等于委托股数减去成交股数，成交股数是持有表中 `tradeQuantity`
   字段中向量的成交股数和。
5. 将撤单记录插入子单流表。
6. 根据买单 id ，检查持有表中是否有对应的订单。如果不存在，则新增记录，并将套利状态设置为 `"买已撤单"`
   ；如果存在，则进行更新。

* **ratioLowHandler 处理价差回归事件**

`ratioLowHandler` 处理价差回归事件，实现代码如下：

```
    // 价差回归事件处理
    def ratioLowHandler(lowRatio){
        writeLog("=========ratio满足套利条件=将数组内的子单全部卖出=========")
        // 停止买单
        canOrder = false
        // 销毁监听器
        lName = "ratioLowListener_"+string(ratioLowNum)
        lowRatioListener = getEventListener(lName)
        lowRatioListener.terminate()
        // 新一轮套利，将计数器+1
        ratioLowNum = ratioLowNum+1

        price = lowRatio.price
        // 将数组内的对应的子单都挂单售卖。
        // 如果上一买单未完全成交，则先撤单剩余部分，并进行卖单；如果完全成交，则直接卖单
        saleIndex(price)
        // 开始新一轮买单
        canOrder = true
        // 更新买单数组
        subOrderIds = mySet(array(STRING,0))
    }
```

实现步骤如下：

1. 将标志位 `canOrder` 设置为 `false`
   ，即价差回归时，需要平仓获利，此时暂停买单下单。
2. 摧毁当前价差回归监听器，不再监听价差回归事件。将价差回归事件计数器加一。
3. 将 `subOrderIds` 内的买单 id 对应的买单，全部挂单售卖，平仓获利。
4. 将标志位 `canOrder` 设置为 `true` ，开启新一轮套利买单下单。清空
   `subOrderIds` 。

* **买单 id 和卖单 id 互相转换**

定义两个函数，实现持有表中，买单 id 和卖单 id 互相转换，实现代码如下：

```
    // 卖单和买单id转换
    def saleID2buyID(saleID){
        s = strlen(saleID)
        s1 = s-15
        buyID = substr(saleID,0,14)+substr(saleID,15,s1)
        return buyID
    }

    // 买单和卖单id转换
    def buyID2saleID(buyID){
        s = strlen(buyID)
        s1 = s-14
        saleID = substr(buyID,0,14)+"0"+substr(buyID,14,s1)
        return saleID
    }
```

同一批指数现货的买单和卖单 id ，只相差字符 `'0'` 。如买单 id 为
`"2025030500001_1"` ，则对应的卖单 id 为
`"2025030500001_01"` 。

* **saleIndex 卖单下单函数**

`saleIndex` 函数被 `ratioLowHandler`
调用，实现代码如下：

```
    def saleIndex(price){
        // 将数组内对应的子单id都挂单卖出
        ks =  subOrderIds.ids
        for(bId in ks){
            // 先检查是否完全成交，否则需要撤单，并销毁监听器
            // 买成交量
            bQtys = select tradeQuantity,orderType from purchasedIndexTb where tagBatchId=bId
            // 委托量
            wQtys = select tradeQuantity from subOrderStream where tagBatchId=bId
            wQty = wQtys[0][`tradeQuantity]
            s1 = bQtys.size()
            if(s1==0){//无成交
                // 计算应该撤销的股数
                writeLog("=========完全撤单")
                cQty = wQty
                cancelOrderById(bId,cQty)
            }else{
                bQty = sum(bQtys[0][`tradeQuantity])
                status = bQtys[0][`orderType]
                if(bQty<wQty && status!=`买已撤单){//需要撤单但是没有撤单，代表还在等待该子单成交
                    writeLog("=========部分撤单")
                    cQty = wQty-bQty
                    cancelOrderById(bId,cQty)
                }
            }

            // 买单Id转为卖单id
            sId = buyID2saleID(bId)
            writeLog("===========开始卖单=========="+bId+"===="+sId)

            // 从持有表中取出对应买单的成交量
            indexs = select * from purchasedIndexTb where tagBatchId=bId

            // 取出
            index = indexs[0]
            // 如果没有买入量，则直接检查下一个
            buyQty = sum(index[`tradeQuantity])
            if(buyQty==0){
                writeLog("=========无持有量,跳过===="+bId)
                continue
            }
            // 卖出买入的全部
            buyQtyV = index[`tradeQuantity]
            saleQty = sum(buyQtyV)
            // 卖单id
            tbId = sId
            lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
            // 放入子单流表
            insert into subOrderStream values(index.splitOrderId,index.batchId,
            tbId,sNum+1,
            index.fundCode,index.fundName,index.assetId,index.assetName,
            index.combinationNo,index.combinationName,index.stockCode,index.stockName,
            index.tradeDate,saleQty,"S",index.market,index.handlerEmpid,
            index.handlerName,parentOrder.orderType,price,lastTime);
            //设置下单次数
            sNum = sNum+1
            // 设置卖单对应的监听
            saleQtyAddListenerName = "saleQtyAddListener"+"_"+string(sNum)

            // 监听成交，将成功买入的股票放入持有的股票内存表中
            partstr = "part"
            allstr = "all"
            addEventListener(saleQtyAdd, "SubOrderTransaction", <SubOrderTransaction.transactionType = partstr && SubOrderTransaction.subOrderID = tbId>,"all",,,,,saleQtyAddListenerName)
            // 这里卖单的完全成交监听，也一直监听
            addEventListener(saleIfPlaceOrder, "SubOrderTransaction", <SubOrderTransaction.transactionType = allstr && SubOrderTransaction.subOrderID = tbId>,"all",,,,,)
        }
    }
```

实现步骤如下：

1. 检查 `subOrderIds` 对应的买单，是否完全成交。若没有完全成交，则需要将剩余股数撤单。这里撤单调用
   `cancelOrderById` 函数，与 `cancelOrder`
   函数实现有一些区别。
2. 将 `subOrderIds` 对应的买单的买入股数，全部挂单售卖，变更卖单序号
   `sNum` 。
3. 设置卖单的成交监听。包括部分成交监听、完全成交监听，并且没有超时时间。

* **cancelOrderById 根据 id 撤销买单**

`cancelOrderById` 被 `saleIndex` 调用，根据 id
、撤单量撤单对应买单，实现代码如下：

```
    // 根据id撤单，由于这里还在等待该子单成交或超时，所以这里应该注销对应的三个买单监听
    def cancelOrderById(id,qty){
        // 得到sortNumOrigin
        s = strlen(id)-14
        sortNumOrigin = substr(id,14,s)
        // 根据子单id，得到listenername
        // 部分监听名称
        pListenerName = "QtyAddListener_"+sortNumOrigin
        // 完全监听名称
        aListenerName = "ifPlaceOrderListener_"+sortNumOrigin
        // 超时监听名称
        tListenerName = "cancelOrderListener_"+sortNumOrigin
        // 销毁监听
        pListener = getEventListener(pListenerName)
        pListener.terminate()
        aListener = getEventListener(aListenerName)
        aListener.terminate()
        tListener = getEventListener(tListenerName)
        tListener.terminate()
        // 撤单
        // 查出对应的撤单id
        id2long = handleOrderId(id)
        orderIds = exec top 1 orderId from outputTb where userOrderId = id2long and orderStatus = 4
        orderId = orderIds[0]
        cancelOrderPlaceTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        // 将撤单加入子单流表
        insert into subOrderStream values(parentOrder.splitOrderId,parentOrder.batchId,orderId,parentOrder.sortNum,
        parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
        parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
        hs300Index.TradeDate,qty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
        parentOrder.handlerName,"cancel",0,cancelOrderPlaceTime);
        // 更新持有表的状态，这里持有表可能没有，也需要检查
        subOrders = select * from purchasedIndexTb where tagBatchId=id
        s = subOrders.size()
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        if(s==0){//新增持有表记录
            bQty = array(INT[],0)
            bQty.append!(0)
            sQty = array(INT[],0)
            sQty.append!(0)
            bPrice = array(DOUBLE[],0)
            bPrice.append!(0)
            sPrice = array(DOUBLE[],0)
            sPrice.append!(0)
            writeLog("==========开始插入持有表")
            insert into purchasedIndexTb values(
                parentOrder.splitOrderId,parentOrder.batchId,
                id,parentOrder.sortNum,
                parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
                parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
                parentOrder.tradeDate,bQty,sQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
                parentOrder.handlerName,"买已撤单",bPrice,sPrice,0,lastTime)
            writeLog("==========插入持有表完成")
        }else{
            update purchasedIndexTb set orderType = "买已撤单",lastUpdateTime = lastTime where tagBatchId=id
        }
    }
```

实现步骤如下：

1. 根据传入的买单 id ，拼接字符串得到下该买单时母单的买单顺序号 `sortNum` ，根据
   `sortNum` 拼接处成交监听、超时监听的监听器名称，并销毁对应的监听。
2. 根据买单 id ，从模拟撮合引擎输出表中查询撤单 id，将撤单放入子单流表。
3. 根据买单 id ，检查持有表中是否有对应的订单。如果不存在，则新增记录，并将套利状态设置为 `"买已撤单"`
   ；如果存在，则进行更新。

* **saleQtyAdd 累计卖单部分成交**

`saleQtyAdd` 处理卖单部分成交事件，实现代码如下：

```
    // 累计卖单部分成交
    def saleQtyAdd(subOrderPartTran){
        qty = subOrderPartTran.tradeQty
        id = saleID2buyID(subOrderPartTran.subOrderID)
        writeLog("========卖单部分成交事件============"+id)
        tPrice = subOrderPartTran.tradePrice
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        //更新持有量表中的卖出股数向量、卖出价格向量
        // 先查出买入股数的数组和价格数组
        indexs = select saleQty,salePrice from purchasedIndexTb where tagBatchId=id
        sQty = indexs[0][`saleQty]
        sPrice = indexs[0][`salePrice]
        if(sQty.size()==1 && sQty[0]==0){//第一次插入
            sQty[0]=qty
            sQtyu = sQty
            sPrice[0]=tPrice
            sPriceu = sPrice
        }else{//不是第一次
            sQtyu = append!(sQty,qty)
            sPriceu = append!(sPrice,tPrice)
        }
        // 更新
        update purchasedIndexTb set saleQty = sQtyu,salePrice = sPriceu,lastUpdateTime = lastTime where tagBatchId=id
        // 计算利润，即向量逐元素相乘相减
        indexs = select tradeQuantity,saleQty,price,salePrice from purchasedIndexTb where tagBatchId=id
        writeLog("=========开始计算利润========")
        bQty = indexs[0][`tradeQuantity]
        sQty = indexs[0][`saleQty]
        bPrice = indexs[0][`price]
        sPrice = indexs[0][`salePrice]
        pf = sum(sQty*sPrice) - sum(bQty*bPrice)
        //更新持有量表利润，状态
        update purchasedIndexTb set profit=pf,orderType = "卖部分成交",lastUpdateTime = lastTime where tagBatchId=id
    }
```

实现步骤如下：

1. 该函数根据卖单 id 转换为买单 id
   ，检查持有表中是否有对应的订单。如果不存在，则新增记录，并将卖出股数、价格进行记录；如果存在，则进行更新。
2. 计算当前得到的利润并对持有表进行更新。利润根据持有表中 `tradeQuantity`
   、`saleQty` 、`price`
   、`salePrice` 进行计算，将持有表对应订单的套利状态设置为
   `"卖部分成交"` 。

* **saleIfPlaceOrder 处理卖单完全成交事件**

`saleIfPlaceOrder` 处理卖单完全成交事件，实现代码如下：

```
    // 卖单完全成交事件
    def saleIfPlaceOrder(subOrderPartTran){

        id = saleID2buyID(subOrderPartTran.subOrderID)
        writeLog("========卖单完全成交事件============"+id)
        // 更新表记录
        tPrice = subOrderPartTran.tradePrice
        // 拿到成交量
        qty = subOrderPartTran.tradeQty
        // 获取指数的最新时间，调用handleCompleteTime
        lastTime = handleCompleteTime(hs300Index.TradeDate,hs300Index.TradeTime)
        //更新持有量表中的卖出股数向量、卖出价格向量
        // 先查出买入股数的数组和价格数组
        indexs = select saleQty,salePrice from purchasedIndexTb where tagBatchId=id
        sQty = indexs[0][`saleQty]
        sPrice = indexs[0][`salePrice]
        if(sQty.size()==1 && sQty[0]==0){//第一次插入
            sQty[0]=qty
            sQtyu = sQty
            sPrice[0]=tPrice
            sPriceu = sPrice
        }else{//不是第一次
            sQtyu = append!(sQty,qty)
            sPriceu = append!(sPrice,tPrice)
        }
        // 更新
        update purchasedIndexTb set saleQty = sQtyu,salePrice = sPriceu,lastUpdateTime = lastTime where tagBatchId=id
        // 计算利润，即向量逐元素相乘相减
        indexs = select tradeQuantity,saleQty,price,salePrice from purchasedIndexTb where tagBatchId=id
        bQty = indexs[0][`tradeQuantity]
        sQty = indexs[0][`saleQty]
        bPrice = indexs[0][`price]
        sPrice = indexs[0][`salePrice]
        pf = sum(sQty*sPrice) - sum(bQty*bPrice)
        //更新持有量表利润
        update purchasedIndexTb set profit=pf,orderType = "卖完全成交",lastUpdateTime = lastTime where tagBatchId=id
    }
```

实现步骤如下：

1. 该函数根据卖单 id 转换为买单 id
   ，检查持有表中是否有对应的订单。如果不存在，则新增记录，并将卖出股数、价格进行记录；如果存在，则进行更新。
2. 计算当前得到的利润并对持有表进行更新。利润根据持有表中 `tradeQuantity`
   、`saleQty` 、`price`
   、`salePrice` 进行计算，将持有表对应订单的套利状态设置为
   `"卖完全成交"` 。

#### 3.3.4 创建CEP引擎

使用 `createCEPEngine` 函数创建 CEP 引擎，并使用
`subscribeTable` 函数使 CEP 引擎订阅异构流表
`orderBlobStream` ，`orderBlobStream` 中接收
`ParentOrder` 、 `HS300Index` 、
`HS300Futures` 、 `SubOrderTransaction` 和
`ratioLow` 事件流。

```
//创建下单任务引擎
dummy = table(1:0, `timestamp`eventType`blobs`splitOrderId, `TIMESTAMP`STRING`BLOB`STRING)
//创建 cep 监听引擎
engine = createCEPEngine(name='arbitrageSplitMonitor', monitors=<arbiSplitMonitor()>, dummyTable=dummy, eventSchema=[ParentOrder,HS300Index,HS300Futures,SubOrderTransaction,ratioLow],timeColumn=`timestamp)

// 订阅异构流表
subscribeTable(tableName="orderBlobStream", actionName="orderBlobStream",handler=getStreamEngine("arbitrageSplitMonitor"),msgAsTable=true)
```

#### 3.3.5 创建模拟撮合引擎

在本例中，模拟撮合引擎也需要订阅行情快照数据，因此模拟撮合引擎需要在订阅行情快照前创建。

* 加载模拟撮合引擎插件

```
login("admin", "123456")
//使用 installPlugin 命令完成插件安装
installPlugin("MatchingEngineSimulator")
//使用 loadPlugin 命令加载插件。
loadPlugin("MatchingEngineSimulator")
```

模拟撮合插件需要用户使用上述代码，自行从插件仓库下载并加载。

* 创建模拟撮合引擎

加载模拟撮合引擎插件后，创建模拟撮合引擎。

```
// 定义函数创建模拟撮合引擎
//撮合引擎cfg
config = dict(STRING, DOUBLE);
config["latency"] = 0;                  //用户订单时延为0
config["depth"] = 10;                   //十档买盘
config["outputOrderBook"] = 0            // 不输出订单簿
config["orderBookMatchingRatio"] = 1;    //与订单薄匹配时的成交百分比
config["dataType"] = 1;                  //行情类别：1表示股票快照
config["matchingMode"] = 1;              //撮合模式一：与最新成交价以及对手方盘口按配置的比例撮合
config["matchingRatio"] = 1;           //快照模式下，快照的区间成交百分比
config["userDefinedOrderId"] = true     // 新增用户指定的订单id列userOrderId

//行情表结构
// 创建行情内存表，作为模拟撮合引擎的输入参数
colNames=`SecurityID`Market`TradeTime`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty`BidPrice`BidOrderQty`OfferPrice`OfferOrderQty
colTypes=[STRING,STRING,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE[],INT[],DOUBLE[],INT[]]
dummyQuoteTable =  table(1:0, colNames, colTypes)
//行情数据表列名映射关系，即自己定义的和引擎内部的映射关系
quoteColMap = dict(  `symbol`symbolSource`timestamp`lastPrice`upLimitPrice`downLimitPrice`totalBidQty`totalOfferQty`bidPrice`bidQty`offerPrice`offerQty,
                     `SecurityID`Market`TradeTime`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty`BidPrice`BidOrderQty`OfferPrice`OfferOrderQty,)

//用户委托单的结构
// 创建用户委托单内存表
colNames=`securityID`market`orderTime`orderType`price`orderQty`BSFlag`orderID
colTypes=[STRING, SYMBOL, TIMESTAMP, INT, DOUBLE, LONG, INT, LONG]
dummyUserOrderTable =  table(1:0, colNames, colTypes)
//映射关系
userOrderColMap = dict( `symbol`symbolSource`timestamp`orderType`price`orderQty`direction`orderId,
                        `securityID`market`orderTime`orderType`price`orderQty`BSFlag`orderID)

//订单详情结果输出表，包括订单委托回报、成交、拒单和撤单状态，此表输出的成交事件会变成成交事件输出到CEP引擎中
//4：已报，-2：表示撤单被拒绝，-1：表示订单被拒绝，0：表示订单部分成交，1：表示订单完全成交，2：表示订单被撤单
// 创建模拟撮合引擎的输出结果表，该表输出的成交记录会转为成交事件输出到CEP引擎
// 输出结果表添加userOrderId列，并且作为流表
colNames=`orderId`symbol`direction`sendTime`orderPrice`orderQty`tradeTime`tradePrice`tradeQty`orderStatus`sysReceiveTime`userOrderId
colTypes=[LONG, STRING, INT,TIMESTAMP,DOUBLE,LONG, TIMESTAMP,DOUBLE,LONG, INT,NANOTIMESTAMP, LONG]
orderDetailsOutput = streamTable(1:0, colNames, colTypes)
//共享
share orderDetailsOutput as outputTb

//撮合上交所股票
exchange = "XSHG"
//创建引擎
name = "MatchingEngine"
matchingEngine = MatchingEngineSimulator::createMatchEngine(name, exchange,
config, dummyQuoteTable, quoteColMap, dummyUserOrderTable, userOrderColMap, orderDetailsOutput,,)

// 共享模拟撮合引擎
share matchingEngine as mEngine
```

使用 `createMatchEngine` 创建模拟撮合引擎。步骤如下：

1. 定义 *config* 参数。`latency`
   指定撮合时延，当最新行情时间>=订单时间时，开始撮合用户订单；`depth`
   表示盘口深度为10；`orderBookMatchingRatio` 和
   `matchingRatio` 指定成交比例；`matchingMode`
   指定第一种撮合模式，即与最新成交价以及对手方盘口按配置的比例撮合（快照行情无区间成交明细信息时）；`userDefinedOrderId`
   设置为 `true` 表示在撮合结果表中新增用户指定订单 ID 列。
2. 定义行情表 `dummyQuoteTable` 、用户委托表结构
   `dummyUserOrderTable` ，以及和引擎内部对应表的字段映射关系；定义撮合结果输出表
   `orderDetailsOutput` 并共享为 `outputTb`
   ，后续 CEP 引擎会订阅 `outputTb` 中的成交事件，并将撮合结果在 Dashboard
   中展示。
3. *exchange* 定义交易所为深交所，指定引擎名称，使用 `createMatchEngine`
   函数创建模拟撮合引擎。

#### 3.3.6 订阅子单流表

模拟撮合引擎需要输入行情数据和用户委托单，本节通过订阅，将子单流表中的用户委托单（买单、卖单）和撤单注入模拟撮合引擎，代码如下：

```
// 在这里通过订阅，将用户订单注入模拟撮合引擎

// orderType需要转换，引擎内部需要INT类型，限价单转为5，撤单转为6
def handleOrderType(x){
    if(x=="Limit"){
        return 5
    }else{
        return 6
    }
}

// 买卖方向需要转换，引擎内部需要INT类型，买转为1，卖转为2
def handleDirection(x){
    if(x=="B"){
        return 1
    }else{
        return 2
    }
}

// 子单id，引擎内部需要long类型，用字符切割，拼成子单id
def handleOrderId(x){
    oV = split(x,"_")
    res = ""
    for(str in oV){
        res = res+str
    }
    return long(res)
}

// 订阅subOrderStream，作为模拟撮合引擎的输入参数
def handleUserOrders(msg) {
    // 拿到所有订单（非撤单）
    data = exec * from msg

    // 向dummyUserOrderTable表写入，这里orderType和direction需要转换，内部需要INT类型
    // orderId转为long
    orderTypeV = exec orderType from msg
    otV = each(handleOrderType, orderTypeV)

    directionV = exec tradeDirection from msg
    dV = each(handleDirection, directionV)

    orderIdV = exec tagBatchId from msg
    oV = each(handleOrderId, orderIdV)

    // 暂存表
    colNames=`securityID`market`orderTime`orderType`price`orderQty`BSFlag`orderID
    colTypes=[STRING, SYMBOL, TIMESTAMP, INT, DOUBLE, LONG, INT, LONG]
    subOrderTempTb = table(1:0, colNames, colTypes)
    subOrderTempTb.tableInsert(data[`fundCode],data[`market],data[`lastUpdateTime],
                                       otV,data[`price],data[`tradeQuantity],dV,oV)
    MatchingEngineSimulator::insertMsg(getStreamEngine("MatchingEngine"), subOrderTempTb, 2)
}

// 订阅流表
subscribeTable(tableName = `subOrderStream,actionName=`handleUserOrders,handler = handleUserOrders,msgAsTable=true,batchSize = 1)
```

`handleOrderType` 、`handleDirection`
、`handleOrderId`
分别用于处理子单流表和模拟撮合引擎中委托表，`orderType`
、`tradeDirection` 、`tagBatchId`
三个字段类型不符的情况；使用 `insertMsg` 将委托单或者撤单注入模拟撮合引擎。

#### 3.3.7 订阅成交回报

订阅成交回报，代码如下：

```
//处理成交单id，返回一个向量，第一个元素是splitOrderId，第二个元素是subOrderID
def handleTransactionId(tIdNum){
    tId = string(tIdNum)
    s = strlen(tId)
    splitOrderId = substr(tId,0,13)
    s1 = s-13
    sortNum = substr(tId,13,s1)
    subOrderID = splitOrderId+"_"+sortNum
    writeLog("=========subOrderID========= "+string(subOrderID))
    return [splitOrderId,subOrderID]
}

// 订阅撮合引擎的输出流表，当订单完全成交或者部分成交，将成交事件注入CEP引擎
// 订阅outputTb
// 这里只取最新存在问题，也是由于一次会下多个子单，因此同一时间会有不同成交单出现
def handleOutputTb(msg) {
    // 拿到最新的完全成交的订单ID和成交价格
    data = exec userOrderId,tradeQty,tradePrice from msg where orderStatus = 1 order by tradeTime desc
    s = data.size()
    // 当size>0，构建成交单，注入CEP
    if(s>0){
        for(i in 0:s){
            // 根据long类型的成交单id，构建出splitOrderId_，subOrderID_
            tId = data[i][`userOrderId]
            IdVector = handleTransactionId(tId)
            // 拿到成交量
            qty = data[i][`tradeQty]
            // 拿到成交价格
            tPrice = data[i][`tradePrice]
            // 构建成交单
            soTransaction = SubOrderTransaction(IdVector[0],"SubOrderTransaction","all",IdVector[1],qty,tPrice,now())
            // 注入CEP引擎（流表）
            appendEvent(`blobStreamEventSerializer,soTransaction)
            writeLog("========完全成交单注入CEP引擎========== "+IdVector[1])
            writeLog(soTransaction)
        }
    }

    // 拿到最新的部分成交的订单ID
    data = exec userOrderId,tradeQty,tradePrice from msg where orderStatus = 0 order by tradeTime desc
    s = data.size()
    // 当size>0，构建部分成交单，注入CEP
    if(s>0){
        for(i in 0:s){
            // 根据long类型的成交单id，构建出splitOrderId_，subOrderID_
            tId = data[i][`userOrderId]
            IdVector = handleTransactionId(tId)
            // 拿到成交量
            qty = data[i][`tradeQty]
            // 拿到成交价格
            tPrice = data[i][`tradePrice]
            // 构建成交单
            soTransaction = SubOrderTransaction(IdVector[0],"SubOrderTransaction","part",IdVector[1],qty,tPrice,now())
            // 注入CEP引擎（流表）
            appendEvent(`blobStreamEventSerializer,soTransaction)
            writeLog("========部分成交单注入CEP引擎========== "+IdVector[1])
        }
    }
}

// 订阅流表
subscribeTable(tableName = `outputTb,actionName=`handleOutputTb,handler = handleOutputTb,msgAsTable=true,batchSize = 1)
```

模拟撮合引擎中，撮合结果表 `outputTb` 定义为一个流数据表。本节订阅
`outputTb` ，当结果表中有新增部分成交或完全成交记录，构造对应的部分成交事件或完全成交事件注入 CEP
引擎，作为冰山算法的成交回报。

#### 3.3.8 订阅行情快照

* 定义指数、期货行情流表

首先定义两个流表，分别用于接收回放的指数、期货行情数据，代码如下：

```
// 定义股票行情快照流表，这个流表用于接收回放的行情快照数据
colNames = `Market`TradeDate`TradeTime`MDStreamID`SecurityID`SecurityIDSource`TradingPhaseCode`ImageStatus`PreCloPrice`NumTrades`TotalVolumeTrade`TotalValueTrade`LastPrice`OpenPrice`HighPrice`LowPrice`ClosePrice`DifPrice1`DifPrice2`PE1`PE2`PreCloseIOPV`IOPV`TotalBidQty`WeightedAvgBidPx`AltWAvgBidPri`TotalOfferQty`WeightedAvgOfferPx`AltWAvgAskPri`UpLimitPx`DownLimitPx`OpenInt`OptPremiumRatio`OfferPrice`BidPrice`OfferOrderQty`BidOrderQty`BidNumOrders`OfferNumOrders`ETFBuyNumber`ETFBuyAmount`ETFBuyMoney`ETFSellNumber`ETFSellAmount`ETFSellMoney`YieldToMatu`TotWarExNum`WithdrawBuyNumber`WithdrawBuyAmount`WithdrawBuyMoney`WithdrawSellNumber`WithdrawSellAmount`WithdrawSellMoney`TotalBidNumber`TotalOfferNumber`MaxBidDur`MaxSellDur`BidNum`SellNum`LocalTime`SeqNo`OfferOrders`BidOrders
colTypes = [SYMBOL,DATE,TIME,SYMBOL,SYMBOL,SYMBOL,SYMBOL,INT,DOUBLE,INT,INT,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,INT,DOUBLE,DOUBLE,INT,DOUBLE,DOUBLE,DOUBLE,DOUBLE,INT,DOUBLE,DOUBLE[],DOUBLE[],INT[],INT[],INT[],INT[],INT,INT,DOUBLE,INT,INT,DOUBLE,DOUBLE,DOUBLE,INT,INT,DOUBLE,INT,INT,DOUBLE,INT,INT,INT,INT,INT,INT,TIME,INT,INT[],INT[]]
share streamTable(1:0,colNames,colTypes) as hs300SnapshotStream

// 定义期货行情快照流表，这个流表用于接收回放的期货快照数据
colNames = `SecurityID`TradeDate`TradeTime`LastPrice
coltypes = [SYMBOL,DATE,TIME,DOUBLE]
share streamTable(1:0,colNames,coltypes) as ctpSnapshotStream
```

* 订阅指数、期货行情流表

订阅 `hs300SnapshotStream` 、`ctpSnapshotStream`
，当流表中有增量行情数据，封装为事件注入 CEP 引擎。代码如下：

```
// 处理交易时间，使其从2023年变为2026年的快照数据
def handleTradeTime(x){
    return temporalAdd(x,3,"y")
}

//=================订阅沪深300股票，当流表里有增量股票快照数据，将其注入CEP；注入模拟撮合引擎，作为指数的交易行情
def subscribeHs300(msg){
    // 向CEP注入Index事件
    datas = select top 1 * from msg order by TradeTime desc
    data = datas[0]
    splitOrderId = `2025030500001
    // 对TradeDate做处理，使其晚于委托单的时间
    td = handleTradeTime(data[`TradeDate])
    hs300Event = HS300Index(splitOrderId,`HS300Index,td,data[`TradeTime],data[`SecurityID],
                            data[`OpenPrice],data[`LastPrice],data[`PreClosePrice],now())
    appendEvent(`blobStreamEventSerializer,hs300Event)

    // 向模拟撮合引擎中写入快照数据
    data = exec * from msg
    colNames=`SecurityID`Market`TradeTime`LastPrice`UpLimitPx`DownLimitPx`TotalBidQty`TotalOfferQty`BidPrice`BidOrderQty`OfferPrice`OfferOrderQty
    colTypes=[STRING,STRING,TIMESTAMP,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE[],INT[],DOUBLE[],INT[]]
    snapshotTempTb = table(100:0,colNames,colTypes)
    // 需要对快照时间做处理，使其晚于委托单的时间
    TimeV = exec TradeDate,TradeTime from msg
    TimeV1 = handleCompleteTime(TimeV)
    tV = each(handleTradeTime, TimeV1)
    snapshotTempTb.tableInsert(data[`SecurityID],data[`Market],tV,
                               data[`LastPrice],data[`UpLimitPx],data[`DownLimitPx],data[`TotalBidQty],data[`TotalOfferQty],
                               data[`BidPrice],data[`BidOrderQty],data[`OfferPrice],data[`OfferOrderQty])
    MatchingEngineSimulator::insertMsg(getStreamEngine("MatchingEngine"), snapshotTempTb, 1)
}
subscribeTable(tableName = `hs300SnapshotStream,actionName=`subscribeHs300,handler = subscribeHs300,msgAsTable=true,batchSize = 1)

//================订阅期货，当流表里有增量期货快照数据，将其注入CEP
def subscribeCtp(msg){
    datas = select top 1 * from msg order by tradeTime desc
    data = datas[0]
    splitOrderId = `2025030500001
    InstrumentID = `IF2406
    ctpEvent = HS300Futures(splitOrderId,`HS300Futures,data[`TradeDate],data[`TradeTime],InstrumentID,
                            0,data[`LastPrice],0,now())
    appendEvent(`blobStreamEventSerializer,ctpEvent)
}
subscribeTable(tableName = `ctpSnapshotStream,actionName=`subscribeCtp,handler = subscribeCtp,msgAsTable=true,batchSize = 1)
```

分别订阅 `hs300SnapshotStream` 、`ctpSnapshotStream`
，当流表中有增量行情数据，分别封装为 `HS300Index`
、`HS300Futures` 事件注入 CEP 引擎。其中指数的行情数据还需要同步注入模拟撮合引擎。

#### 3.3.9 回放行情快照

回放指数、期货行情数据，代码如下：

```
// 往股票行情流表里回放行情数据
// ============回放开始
replayData = select * from loadTable("dfs://arbitrageSnapshot","snapshot_index")
// 精确回放条回放
submitJob("replay_hs300Snapshot", "hs300Snapshot",  replay{replayData, hs300SnapshotStream, `TradeDate, `TradeTime, 1, false,,,true})

// 往期货行情流表里回放构建的期货行情
replayData = select * from loadTable("dfs://arbitrageSnapshot","snapshot_future")
// 精确回放条回放
submitJob("replay_ctpSnapshot", "ctpSnapshot",  replay{replayData, ctpSnapshotStream, `TradeDate, `tradeTime, 1, false,,,true})
```

将分布式表中存储的指数、期货行情数据分别回放到 `hs300SnapshotStream`
、`ctpSnapshotStream` ，回放速度选择精确速度回放。

#### 3.3.10 启动策略

使用 DolphinDB 提供的 JAVA API ，将 `ParentOrder` 事件放入
`orderBlobStream` ，启动拆单策略。核心函数 `putOrder`
如下。完整的启动策略项目文件见附录。

```
public static void putOrder() throws IOException, InterruptedException {

    //        连接dolphindb数据库
    DBConnection conn = DBUtil.getConnection();
    //        封装母单订阅流表
    EventSender sender1 = EventSenderHelperArbitrage.createEventSender(conn);
    //      拿到拆单参数map
    HashMap<String, Object> map = getMap();

    //        定义母单
    DolphinDbParentSplitParamsArbitrageVo dolphinDbParentVo1 = new DolphinDbParentSplitParamsArbitrageVo(
            "2025030500001",                    // splitOrderId: 母单拆单操作单元唯一ID
            "ParentOrder",                  // eventType: 事件类型
            "2025030500001",           // batchId: 母单唯一ID
            "",    // tagBatchId: 子单唯一ID
            0,                              // sortNum: 拆单顺序号（从1开始）
            "510300",                       // fundCode: 基金代码
            "蓝筹精选混合",                  // fundName: 基金名称
            "A123456789",                   // assetId: 资产单元ID
            "量化投资组合",                  // assetName: 资产单元名称
            "C789",                         // combinationNo: 组合编号
            "全天候策略",                    // combinationName: 组合名称
            "600000",                       // stockCode: 证券代码
            "浦发银行",                      // stockName: 证券名称
            "20231010",                     // tradeDate: 交易日期（yyyyMMdd）
            400000L,                         // tradeQuantity: 交易量（注意L后缀）
            "B",                            // tradeDirection: 交易方向（1-买入）
            "XSHG",                          // market: 交易市场
            "E1001",                        // handlerEmpid: 执行人工号
            "王强",                          // handlerName: 执行人姓名
            (String) map.get("splitMethod"),     // splitMethod: 拆单算法
            (String) map.get("orderType"),      // orderType: 订单类型
            (Integer) map.get("orderQty"),    //子单股数
            (Integer) map.get("timeoutNum"),    //超时时间
            (LocalDateTime) map.get("startTime"),   // startTime: 拆单开始时间
            (LocalDateTime) map.get("endTime"),     // endTime: 拆单结束时
            "",                        // orderStatus: 拆单状态
            LocalDateTime.now()             // eventTime: 事件下达时间
    );

    //发送母单，将母单放入订阅流表，供CEP引擎消费
    sender1.sendEvent(dolphinDbParentVo1.getEventType(), dolphinDbParentVo1.toEntities());
    System.out.println("母单放入母单订阅流表");
}
```

### 3.4 结果检视

本小节通过查看 Dashboard 中的输出事件展示拆单系统运行的结果。在本例中，母单事件注入 CEP
引擎后，记录到对应的内存表；子单下单到子单接收流表；模拟撮合引擎撮合委托单产生成交单，将买入、卖出股数、价格及实时获利情况记录到套利结果内存表中。如此在
Dashboard 中便可以选取需要的数据进行可视化。

**step1-JAVA环境准备**

配置系统的 maven 、jdk 环境，本例中的 jdk 和 maven 版本如下：

```
jdk - java version "1.8.0_441"
maven - Apache Maven 3.8.6
```

**step2-数据准备**

下载附录中的套利下单算法并解压。将 `data/snapshot_index.csv` 、
`data/snapshot_future.csv` 导入到
`dolphindb/server` 目录下，运行导入脚本
`data/data_input_snapshot.dos` 进行建库建表，并将测试数据导入建好的分布式表中。运行脚本
`data/loadMatchEngine.dos` ，加载模拟撮合引擎插件。将
`data/dashboard.Arbitrage 拆单监控.json` 导入到 Dashboard 。

**step3-下单系统构建**

运行脚本 `01 clearEnv.dos` 、 `02 Event.dos` 、
`03 createTable.dos` 、`04
arbiTradeSplitMonitor.dos` 、`05 createCEPEngine.dos`
。`01 clearEnv.dos` 脚本将系统中已存在的内存共享表、订阅信息、流式引擎等进行清除，确保不会重复定义；
`02 Event.dos 、 03 createTable.dos 、04 arbiTradeSplitMonitor.dos 、05
createCEPEngine.dos` 脚本分别对应上文介绍的定义事件类、创建内存表、定义监视器、创建 CEP 引擎的功能。

**step4-模拟撮合引擎创建**

运行 `06 createMatchEngine.dos` ，创建模拟撮合引擎。

**step5-子单、成交回报、行情订阅**

运行 `07 subscribeSubOrder.dos` 、`08
subscribeTransacionOrder.dos` 、`09
subscribeSnapshot.dos` ，分别订阅子单、成交单及指数期货行情数据。

**step6-回放行情数据**

运行 `10 replaySnapshot.dos` ，回放指数期货行情数据。

**step7-策略启动**

下载附录中的 JAVA API 策略启动代码并解压。修改 `data/DBUtil.java` 中的数据库配置为用户自己的环境。运行
`startArbitrage.java` ，将母单事件放入异构流表中，观察 Dashboard 中的对应输出。

![](images/order_splitting_with_cep_advanced/3_4.png)

图 10. 图3-4 子单结果图

如图3-4所示，子单流表中记录了委托的买单和卖单、下单价格以及下单时间。

![](images/order_splitting_with_cep_advanced/3_5.png)

图 11. 图3-5 套利结果图

如图3-5所示，套利结果表中，存储了每个订单的买入卖出股数、买入卖出价格，并计算出所获利润。如图中红色矩形框和蓝色矩形框所示，低买高卖获取无风险利润。

### 3.5 总结

本章通过循序渐进的方式，介绍了如何使用 DolphinDB 的
CEP引擎和模拟撮合引擎，实现套利下单算法。首先说明了算法思想；然后模块化介绍了系统的功能；其次详细介绍了系统的实现流程和代码，其中最复杂的是监视器定义的部分，详细阐述了各个函数之间的调用关系；最后将系统的下单、成交过程和利润计算，在结果检视部分使用
Dashboard 进行展示。

## 4. 总结

本文基于 CEP
引擎构建了一套完整的算法拆单调度框架。通过​​事件驱动架构​​和​​动态事件监听器​​来实现订单下达、拆单、成交回报及订单超时的监听与处理。同时利用​​键值内存表缓存实时行情快照，为子单价格计算提供毫秒级响应支持。在功能实现上，文中​​隐蔽交易逻辑算法​​（冰山算法结合模拟撮合引擎实现闭环风控）以及及​​策略扩展层​​（跨品种套利）等
Demo，并通过​​​​可视化监控面板​​进行了实时展示订单状态以及套利利润等信息。

## 5. 附录

### 5.1 冰山拆单算法

[demo3\_IceBerg\_MatchEngine](script/order_splitting_with_cep_advanced/demo3_IceBerg_MatchEngine.zip)

### 5.2 套利下单算法

[demo4\_Arbitrage](script/order_splitting_with_cep_advanced/demo4_Arbitrage.zip)

### 5.3 JAVA API 策略启动代码

[cepSplitDemo（进阶）](script/order_splitting_with_cep_advanced/cepSplitDemo%EF%BC%88%E8%BF%9B%E9%98%B6%EF%BC%89.zip)

### 5.4 Python API 策略启动代码（仅套利策略）

[py\_split\_code](script/order_splitting_with_cep_advanced/py_split_code.zip)
