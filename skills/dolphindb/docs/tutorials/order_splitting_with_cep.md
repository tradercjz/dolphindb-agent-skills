<!-- Auto-mirrored from upstream `documentation-main/tutorials/order_splitting_with_cep.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# CEP 引擎应用：算法拆单调度系统实现-基础篇

教程难度

* 高级

面向读者

* 已经掌握 DolphinDB 基础操作，包括 server 部署、客户端部署、库表创建代码编写和调试：新用户入门指南（金融篇）
* 有代码开发和调试能力的 DolphinDB 用户
* 计划基于 DolphinDB 的 CEP 引擎搭建大额委托单自动拆单下单系统的 DolphinDB 用户
* 已经掌握 DolphinDB 数据回放，流数据表订阅和 CEP 引擎的 DolphinDB 用户

在金融市场中，大额订单的一次性交易可能会对市场价格产生较大冲击，导致交易成本增加。例如，大额买入订单可能会迅速推高股价，使后续买入成本上升；大额卖出订单则可能打压股价，造成资产贱卖。拆单算法通过将大额订单拆分成多个小额订单，在指定时间段的不同时间点进行小额订单交易，避免了一次性大额交易对市场价格的过度影响。

本教程使用了 DolphinDB 的 CEP（复杂事件处理引擎用）产品，系统的讲解了基于 CEP 引擎搭建拆单调度系统的全流程，包括 TWAP 和 VWAP
两种拆单算法。读者将学习以下内容：

* CEP 的基础介绍。
* 如何基于 CEP 引擎实现 TWAP 算法拆单。
* 如何基于 CEP 引擎实现 VWAP 算法拆单。

## 1. CEP 引擎介绍

复杂事件处理（Complex Event Processing，简称 CEP
）引擎是一款用于实时处理和分析事件流中复杂事件的引擎。其主要功能包括接收实时数据流，定义事件并从事件流中检测特定事件，进而对满足指定规则的事件执行预设的操作。详细功能介绍如下：

* 事件捕捉和过滤： 从大量实时数据流中找到特定事件。
* 事件模式：识别指定的事件模式，这些模式可以涉及多个事件的组合，形成具有特定含义的事件序列。
* 复杂事件处理：执行复杂的事件处理逻辑，包括筛选、聚合、转换等操作，以识别关键信息或发现特定的业务模式。

![](images/order_splitting_with_cep/1_1.png)

图 1. 图 1-1 CEP 引擎架构图

由图 1-1 可以看出，一个完整的 CEP 应用包括以下几个部分：事件流序列化器、事件流反序列化器、事件分发器、CEP
子引擎。事件是贯穿这些部分的基本元素，详细介绍请查阅官网。

## 2. TWAP 拆单算法

本章将介绍如何使用 CEP 引擎实现 TWAP 拆单算法。

### 2.1 算法思想

TWAP（Time Weighted Average
Price），时间加权平均价格算法，是一种最简单的拆单算法交易策略，主要适用于流动性较好的市场和订单规模较小的交易。该模型将交易时间进行均匀分割，并在每个分割节点上等量拆分订单进行提交。例如，可以将某个交易日的交易时间平均分为
n 段，TWAP 算法会将该交易日需要执行的订单均匀分配在这 n 个时间段上去执行，从而使得交易均价跟踪 TWAP 。TWAP
模型设计的目的是使交易对市场影响减小的同时提供一个较低的平均成交价格，从而达到减小交易成本的目的。TWAP 算法的公式如下：

![](images/order_splitting_with_cep/formula1.png)

其中，*n* 为时间段的个数，*pricei* 为分割节点上拆分订单的价格。但使用 TWAP
算法进行拆单存在一些问题：

* 在订单规模很大的情况下，均匀分配到每个节点上的下单量仍然较大，当市场流动性不足时仍可能对市场造成一定的冲击。
* 传统的 TWAP
  算法对交易时间和订单规模进行均匀拆分，这种有规律的交易模式容易被市场其他参与者察觉和预测。一旦其他交易者发现了这种模式，就可以根据其规律提前布局，增加交易成本。

本例基于上述问题，对传统 TWAP 算法做了如下改进：

* 子单规模、下单时间间隔在用户指定的范围内随机，使得交易模式更加隐蔽，避免被其他市场参与者察觉和针对。
* 对大额母单的拆单状态进行实时管理，包括暂停下单、恢复下单和终止下单。用户可以根据实时市场形势，对母单状态进行管理，增加风险容错。

### 2.2 功能模块

TWAP 算法逻辑实现主要依赖 DolphinDB 的如下功能模块：

* CEP 引擎：核心组件，把所有流式数据包括行情和订单都看作是事件流，自定义事件流的处理规则。
* 数据回放功能：模拟实时快照行情。
* 流表的发布订阅功能：解耦用户母单发布和拆单 CEP 引擎，促进系统内模块间的通信。

TWAP 的算法逻辑实现流程图如下所示：

![](images/order_splitting_with_cep/2_1.png)

图 2. 图 2-1 TWAP 算法流程图

本例中 CEP 引擎的策略启动事件是母单事件 `ParentOrder` ，母单事件进入引擎后，将启动对母单状态管理事件
`OrderAlterAction` 的监听。行情快照数据通过回放功能进入键值内存表后，供拆单核心函数
`PlaceOrder` 读取，以确定子单下单的价格。下面将分模块介绍它们的主要功能。

**1）数据回放**

数据回放 `Replay` 是 DolphinDB
中常用于高频策略回测场景的方法，它可以根据指定的回放模式，按时间顺序将一个或多个数据表的数据回放到某个数据表或引擎，模拟实时数据的写入。

由于行情快照由交易所按固定时间间隔推送， `Replay`
可以很好地将这种数据按时间戳排序后输出到流数据表。而行情快照数据中包含了交易所中多种基金的大量的历史行情，因此直接提供给 CEP
引擎会导致慢查询。在现实市场中，确定子单价格只需要该基金最新的快照盘口数据，因此一支基金只需要保留最新的行情快照记录，DolphinDB
提供的键值内存表可以实现上述思路。有关键值内存表的说明见官方文档 。

本例中键值内存表以基金 ID 为主键，快照行情数据（包含买卖盘口十档价格）为非主键列，就可以向 CEP
引擎提供多支基金的实时行情快照数据，以模拟实时行情快照写入。

**2）流表发布订阅**

DolphinDB
的流表订阅采用经典的发布-订阅（Pub-Sub）通信模型，通过消息队列实现流数据的发布与订阅，从而将流数据生产者（发布者）与消费者（订阅者）解耦。异构流数据表接收流数据的输入，当新的流数据注入到该流数据表时，发布者会将这些数据发送到所有订阅者的消费队列，并通知所有订阅方，从消费队列中获取数据进行增量处理。

内存表可以通过 `subscribeTable`
函数订阅流数据表，上文中的键值内存表订阅流数据表，需要自定义回调函数，并在回调函数中将接收到的增量数据插入到键值内存表中。最终键值内存表中记录了所有基金的最新行情快照数据。如下图所示。

![](images/order_splitting_with_cep/2_2.png)

图 3. 图2-2 键值对内存表功能示意图

CEP引擎可以通过 `subscribeTable` 函数订阅流数据表，需要指定 *handler* 为 CEP
引擎的句柄，通过 `getStreamEngine` 获得对应 CEP 引擎的句柄。CEP 引擎订阅异构流数据表，当流表中出现增量
`ParentOrder` 和 `OrderAlterAction` 事件时，将事件注入
CEP 引擎，CEP 引擎添加对应的监视器和回调函数进行事件处理，完成拆单下单和母单状态管理的过程。

**3）CEP 引擎**

CEP 引擎模块是拆单系统中最重要，也是最复杂的部分。在本案例中，采用了动态启动策略的方式：当引擎内的事件监听器（Event Listener）捕获策略启动事件
`ParentOrder` 时，才会设置对 `OrderAlterAction`
的监听。行情快照通过数据回放进入流数据表，流数据表将数据发布到键值内存表中，供 CEP 引擎查询基金最新的盘口价格。

* 拆单下单：`ParentOrder` 注入 CEP 引擎后，调用核心函数
  `PlaceOrder`
  进行拆单下单。`PlaceOrder`首先判断母单状态，若处于初始化/下单中，则进行拆单。`PlaceOrder`
  根据用户指定的子单股数范围，使用 DolphinDB 的 `rand`
  函数随机选取子单股数。从键值内存表中读取当前基金的最新盘口价格，确定子单价格。确定子单参数后，将子单输出到子单流表中即下单。下单后判断是否下单完毕，若下单完毕则注销监视器；否则使用
  `rand` 函数随机选取间隔时间后，定时启动下一次拆单下单。
* 母单状态修改：策略启动后，CEP 引擎设置对 `OrderAlterAction` 事件的监听，当
  `OrderAlterAction`注入 CEP
  引擎，监视器根据母单当前状态和目标状态对母单进行操作。例如将处于下单状态的母单设置为暂停下单，此时 CEP 引擎会暂停拆单下单的过程，监听下一个
  `OrderAlterAction`
  事件注入引擎，从而恢复下单。`OrderAlterAction` 事件输出到状态修改流表中。
* 可视化：Dashboard 是 DolphinDB
  提供的一个强大的数据可视化和分析工具，旨在帮助用户更好地理解和利用数据。将子单流表和状态修改流表中的数据输出到 Dashboard
  ，可以实时观察母单的拆单下单过程，以及母单的状态修改情况。

### 2.3 代码实现

在本节中我们将具体介绍 TWAP 拆单系统代码的实现，包括定义事件类、键值内存表订阅流表、回放行情数据、定义监视器、创建 CEP 引擎、CEP
引擎订阅流表、启动策略实例等功能模块，完整代码见文末附录。

**step1-定义事件类**

DolphinDB 将事件定义为类，首先使用 DolphinDB 脚本语言将母单信息、母单状态变更信息定义为类。完整的事件类代码见附件。

* 母单类 `ParentOrder` ：除了母单的基本信息，例如母单
  ID、批次、基金代码、证券代码、执行人、母单股数、买卖方向等，需要定义为母单类的成员变量外，还需要将拆单的核心参数定义为母单类的成员变量：

```
    fundCode :: STRING            //基金ID
    tradeQuantity :: LONG     //母单股数
    tradeDirection :: STRING  // 买卖方向，"B"对应买，"S"对应卖

    //拆单参数
    splitMethod :: STRING          // 拆单算法
    priceOption :: INT             // 买一还是卖一价格
    startTime :: TIMESTAMP         // 拆单开始时间
    endTime :: TIMESTAMP           // 拆单结束时间
	lowChildOrderQty :: INT           // 子单最小股数
    highChildOrderQty :: INT           // 子单最大股数
    lowSplitInterval :: INT           // 最小拆单间隔（秒）
    highSplitInterval :: INT           // 最大拆单间隔（秒）
    orderStatus :: STRING          // 拆单状态
```

`splitMethod` 指定算法类型，这里为 TWAP；`priceOption`
指定子单价格使用行情快照中的买一价格还是卖一价格；`startTime`
、`endTime` 指定拆单时间范围；`lowChildOrderQty`
、`highChildOrderQty`
指定子单下单股数范围；`lowSplitInterval`
、`highSplitInterval` 指定子单拆单时间间隔范围；
`orderStatus` 记录母单状态，例如初始化、下单中、暂停等。

* 母单状态变更类 `OrderAlterAction`
  ：将对母单状态变更操作的信息定义为母单状态变更类，包含以下成员变量。

```
    splitOrderId :: STRING         //操作的母单号
	eventType :: STRING    		//事件类型
    operation :: STRING         //操作类型
	batchId :: STRING        //批次ID（母单的唯一ID）
	handlerEmpid :: STRING         //执行人
    handlerName :: STRING        // 执行人
    eventTime :: TIMESTAMP // 下达变更单时间
```

核心成员变量是 `operation` 指定此次状态变更的操作类型，例如暂停、恢复、终止下单等。CEP
引擎的监视器根据操作类型对母单的 `orderStatus` 进行变更。

**step2-创建母单、子单记录内存表**

创建母单记录内存表 `parentOrderManage` ，修改订单记录内存表
`alterOrderManage` ，子单接收流表 `subOrderStream` 以及
CEP 引擎订阅的异构流数据表 `orderBlobStream` 。

```
//创建母单记录内存表
colNames=["splitOrderId","eventType","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","tradeDirection","market","handlerEmpid","handlerName","splitMethod","orderType","price","startTime","endTime","splitInterval","orderStatus","splitOrderAmount","eventTime","lastUpdateTime"]
colTypes=[STRING,SYMBOL,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,SYMBOL,DOUBLE,TIMESTAMP,TIMESTAMP,INT,SYMBOL,INT,TIMESTAMP,TIMESTAMP]
share table(1:0,colNames,colTypes) as parentOrderManage

//创建修改订单记录内存表
colNames=`splitOrderId`eventType`operation`batchId`handlerEmpid`handlerName`eventTime
colTypes=[STRING,STRING,STRING,STRING,STRING,STRING,TIMESTAMP]
share table(1:0, colNames, colTypes) as alterOrderManage

// 创建子单接收流数据表
colNames=["splitOrderId","batchId","tagBatchId","sortNum","fundCode","fundName","assetId","assetName","combinationNo","combinationName","stockCode","stockName","tradeDate","tradeQuantity","tradeDirection","market","handlerEmpid","handlerName","orderType","price","lastUpdateTime"]
colTypes=[STRING,STRING,STRING,INT,SYMBOL,SYMBOL,STRING,STRING,STRING,STRING,SYMBOL,SYMBOL,STRING,LONG,SYMBOL,SYMBOL,STRING,STRING,SYMBOL,DOUBLE,TIMESTAMP]
share streamTable(1:0, colNames, colTypes) as subOrderStream

// 创建异构流数据表，被CEP引擎订阅
share(streamTable(100:0,`timestamp`eventType`blob`splitOrderId, [TIMESTAMP, STRING,BLOB,STRING]),"orderBlobStream")
```

**step3-键值内存表订阅流表**

使用键值内存表 `snapshotOutputKeyedTb` 订阅行情快照流表
`snapshotStream` ，首先定义两张表。

* **表结构定义：**定义行情快照流表 `snapshotStream`
  ，用于接收回放的行情快照数据；定义键值内存表`snapshotOutputKeyedTb`
  ，用于存储每支基金的最新行情快照。

```
// 定义行情快照流表，这个流表用于接收回放的行情快照数据
colNames = `Market`TradeDate`TradeTime`SecurityID`OfferPrice`BidPrice`OfferOrderQty`BidOrderQty
coltypes = [SYMBOL,DATE,TIME,SYMBOL,DOUBLE[],DOUBLE[],INT[],INT[]]
share streamTable(1:0,colNames,coltypes) as snapshotStream

// 创建键值对表，该表订阅snapshotStream，存储每个基金的买盘和卖盘,每个基金的买盘和卖盘只有一条记录
snapshotOutputKeyedTbTmp = keyedTable(`SecurityID,1:0,colNames,coltypes)
share snapshotOutputKeyedTbTmp as snapshotOutputKeyedTb
```

`snapshotStream` 中，`SecurityID` 为基金唯一 ID
，`OfferPrice` 为卖盘十档价格，`OfferOrderQty`
为卖盘对应的十档委托量；`BidPrice` 为买盘十档价格，`BidOrderQty`
为买盘对应的十档委托量。

`snapshotOutputKeyedTb` 中，主键为 `SecurityID` ，字段和
`snapshotStream` 一致。最终每支基金只会保存一条最新的行情快照记录。

* **订阅：**`snapshotOutputKeyedTb` 订阅
  `snapshotStream` 中的增量行情快照数据。

```
// 订阅snapshotStream回调函数
def handleSnapshot(msg) {
    // 拿到所有数据
    data = exec * from msg
    // 向snapshotOutputKeyedTb表写入
    insert into snapshotOutputKeyedTb values(data[`Market],data[`TradeDate],data[`TradeTime],data[`SecurityID],
                                             data[`OfferPrice],data[`BidPrice],data[`OfferOrderQty],data[`BidOrderQty])
}
// 订阅
subscribeTable(tableName = `snapshotStream,actionName=`handleSnapshot,handler = handleSnapshot,msgAsTable=true,batchSize = 1)
```

使用 `subscribeTable` 函数订阅 `snapshotStream`
，回调函数 `handleSnapshot` 接收到的增量行情快照数据插入到
`snapshotOutputKeyedTb` 。

**step4-定义监视器**

CEP 引擎内部监视器的配置是拆单系统实现中最关键的步骤。监视器内封装了整个拆单策略，其结构大致如下。

```
class SplitMonitor:CEPMonitor{
	def SplitMonitor() {
		//本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
	}
    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){...}

    //更新母单记录信息
    def updatePOrderManageInfo(pOrder,opTime){...}
}

//TWAP 算法下单监听 monitor，继承关系
class TWAPSplitMonitor:SplitMonitor {

    // 记录子单总下股数的变量
    subOrderQtys :: INT
    // 当前母单
	parentOrder :: ParentOrder

	def TWAPSplitMonitor() {
		//本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
	}

    // 在范围内选取随机数，被时间浮动和单量浮动调用
    def randNum(lowNum, highNum){...}

    //TWAP 下单方法
    def placeOrder(){...}

    //母单拆单状态变更操作
    def orderAlter(oaAction){...}

    //初始化parentOrder，进行拆单下单，设置OrderAlterAction事件监听
    def startPlaceOrder(pOrder){...}

    //创建母单下单monitor实例
	def forkParentOrderMonitor(pOrder){...}

	//初始任务
	def onload(){
		addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
	}
}
```

成员变量 `subOrderQtys` ：由于子单是给定股数范围内随机股数下单，使用
`subOrderQtys` 记录当前已下子单的股数和，避免超出母单股数。

成员变量 `parentOrder` ：记录当前母单的参数，包括基本信息，拆单参数，和拆单状态。

下面将按照 CEP 引擎运作的逻辑顺序，依次介绍监视器中各个成员方法的具体内容。

* **onload 初始任务**

创建引擎并实例化监视器后，将首先调用其内部的 `onload` 函数。回顾上文， CEP 引擎工作流的源头是监听策略启动事件
`ParentOrder` ，一旦监听到 `ParentOrder`
注入才进行下一步的操作。因此，在 `onload` 函数中，只需考虑设置相关的事件监听器以便启动策略即可。使用
`addEventListener` 函数监听 `ParentOrder`
事件注入，指定回调函数为 `forkParentOrderMonitor` ，事件类型是
`ParentOrder` ，设置监听次数为持续监听。

```
    //初始任务
	def onload(){
		addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
	}
```

`onload` 方法设置了一个事件监听器，监听所有的母单事件 `ParentOrder`
。当监听到该类型事件时，下一步将启动整个拆单下单过程。为了控制母单拆单下单的线程安全，为每个母单创建不同的 Monitor 实例，因此在对应的回调函数
`forkParentOrderMonitor` 中需要包含对 Monitor 实例的创建和母单参数传递等步骤。从
`onload` 方法开始，函数调用的流程与实现的功能可以分为四个模块，如下图所示。

![](images/order_splitting_with_cep/2_3.png)

图 4. 图2-3 函数调用模块图

其中， `startPlaceOrder` 函数是后三个模块的启动函数，启动顺序如上图所示。模块 3 、模块 4
中，函数调用的流程与实现的功能如下图所示。

![](images/order_splitting_with_cep/2_4.png)

图 5. 图 2-4 模块 3 、模块 4 流程图

接下来从策略启动事件对应的回调函数 `forkParentOrderMonitor` 开始来介绍具体的代码实现。

* **forkParentOrderMonitor 生成监视器实例**

在现实的交易市场中，系统会同时接到多个需要拆分的大额委托单。若 CEP 引擎内只使用一个 Monitor 实例来操作当前委托单的拆单下单，由于一个 Monitor
实例只有一个 `parentOrder` 成员变量，则会使得成员变量 `parentOrder`
的属性值一直被新注入的母单事件修改，引起线程安全问题。

为了解决上面的问题，CEP 引擎内的初始 Monitor 只负责监控策略启动事件注入，参考上文的 `onload` 函数。每当
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
`startPlaceOrder` 方法，并将注入的 `ParentOrder` 事件
`pOrder` 传入。启动后续核心模块。

* **startPlaceOrder 启动核心模块**

`startPlaceOrder` 函数中，包含模块 2 、模块 3 和模块 4 的启动步骤，函数定义如下。

```
    //模块启动函数
    def startPlaceOrder(pOrder){
        // 设置当前子任务 monitor 对象的内部母单变量
        parentOrder = pOrder
        // 对子单量总股数初始化为0
        subOrderQtys = 0

        //TWAP 拆单初始化
        parentOrder.setAttr(`orderStatus,'初始化')
        parentOrder.setAttr(`sortNum,0)  //拆单顺序号

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

        //创建母单变更操作监听器，持续监听
        addEventListener(orderAlter, "OrderAlterAction", <OrderAlterAction.splitOrderId = pOrder.splitOrderId>,"all")
	}
```

函数逻辑如下：

1. 先进行当前 Monitor 母单成员变量 `parentOrder` 、子单总股数成员变量
   `subOrderQtys` 的初始化。然后调用
   `initPOrderManageInfo` 函数，将当前母单事件记录到内存表
   `parentOrderManage` 中，对应模块 2 。
2. 初始化完成，检查当前时间是否到达开始拆单时间。若已经超过开始下单时间，则调用 `placeOrder`
   函数对当前委托单进行拆单下单；否则等待到达开始时间后，调用 `placeOrder` 函数。对应模块 3
   中的拆单开始时间判断。
3. 拆单启动完成，使用 `addEventListener` 函数启动对
   `OrderAlterAction` 事件的监听。对应模块 4 中的初始监听。

* **initPOrderManageInfo 记录母单信息**

`initPOrderManageInfo` 函数的定义十分简单，将监听到的母单事件记录到对应内存表
`parentOrderManage` 中。

```
    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){
        parentOrderManage=objByName('parentOrderManage')
        insert into parentOrderManage values(
            pOrder.splitOrderId,pOrder.eventType,pOrder.batchId,pOrder.tagBatchId,pOrder.sortNum,
            pOrder.fundCode,pOrder.fundName,pOrder.assetId,pOrder.assetName,pOrder.combinationNo,
            pOrder.combinationName,pOrder.stockCode,pOrder.stockName,pOrder.tradeDate,pOrder.tradeQuantity,
            pOrder.tradeDirection,pOrder.market,pOrder.handlerEmpid,pOrder.handlerName,
            pOrder.splitMethod,pOrder.orderType,pOrder.price,pOrder.startTime,pOrder.endTime,
            0,pOrder.orderStatus,0,pOrder.eventTime,now())
    }
```

* **randNum 生成范围内随机数**

`randNum` 函数用于在给定范围内生成随机整数并返回。上文提到，用户可以在母单事件中指定子单股数范围为
`lowChildOrderQty` ~ `highChildOrderQty`
，拆单时间间隔范围为 `lowSplitInterval` ~
`highSplitInterval` 。`randNum`
函数用于在给定范围内随机生成子单股数和时间间隔。

```
    // 在范围内选取随机数，被时间浮动和单量浮动调用
    def randNum(lowNum, highNum){
        if(lowNum == highNum){
            return lowNum
        }
        // 向量保存可以选择的浮动值
        nums = array(INT, 0).append!(lowNum..highNum)
        // 随机下标，范围是0~highnum-lownum，这里返回的是数组，因此要带上索引
        indexNum = highNum-lowNum
        index = rand(indexNum, 1)[0];
        // 取出浮动值
        return nums[index];
    }
```

`randNum` 函数先生成一个数组保存给定范围内的所有整数，然后生成随机下标，根据随机下标访问并返回。

* **updatePOrderManageInfo 更新母单最后修改时间**

`updatePOrderManageInfo` 函数用于修改母单的最后修改时间。

```
    //更新母单记录信息
    def updatePOrderManageInfo(pOrder,opTime){
        parentOrderManage=objByName('parentOrderManage')
        update parentOrderManage set sortNum = pOrder.sortNum,orderStatus=pOrder.orderStatus, lastUpdateTime = opTime where splitOrderId = pOrder.splitOrderId
    }
```

* **placeOrder 拆单核心函数**

`placeOrder` 函数是拆单下单的核心函数，对应模块 3 中的后半部分。

```
    //TWAP 下单方法
    def placeOrder(){

        //判断是否超过下单时限
        if(now()>= parentOrder.endTime){ //当前时间大于下单结束时间,则不再下单
            parentOrder.setAttr(`orderStatus,'时限中止')
            updatePOrderManageInfo(parentOrder,now())
            return
        }

        //判断当前母单状态是否是可以下单状态,不是则退出
        if(!(parentOrder.orderStatus in ['初始化','下单中'])){
            return
        }

        // 计算子单已经下过的单数
        totalQty = subOrderQtys

        //计算剩余待下单股数 = 母单股数 - 所有子单数
        remainQty = parentOrder.tradeQuantity - totalQty

        // 计算当前应该下的子单数
        //若剩余股数大于等于最小子单股数, 下随机子单股数
        if(remainQty >= parentOrder.lowChildOrderQty){
            //下单股数，分两个区间，如果剩余股数在low-high之间，则下的股数在low-remain之间随机，否则在low-high之间随机
            if(remainQty < parentOrder.highChildOrderQty){
                subOrderQty = randNum(parentOrder.lowChildOrderQty, remainQty)
            }else{
                subOrderQty = randNum(parentOrder.lowChildOrderQty, parentOrder.highChildOrderQty)
            }
        }else{//否则下单剩余股数
            subOrderQty = remainQty
        }

        // 更新子单股数
        subOrderQtys = subOrderQtys+subOrderQty

        // 更新剩余单数
        remainQty = remainQty-subOrderQty

        // 拿到母单的基金代码
        v_securityId = parentOrder.fundCode
        // 直接从分布式表中进行查询，定义一个函数
        if(parentOrder.priceOption == 0){//从买一价格获取，从BidPrice[0]获取价格
            // 从键值对表中获取
            BidPrice = exec BidPrice from snapshotOutputKeyedTb where SecurityID = v_securityId
            // 买一价格
            subOrderPrice = BidPrice[0]
        }else{//从卖一价格获取，从OfferPrice[0]获取价格
            // 从键值对表中获取
            OfferPrice = exec OfferPrice from snapshotOutputKeyedTb where SecurityID = v_securityId
            // 卖一价格
            subOrderPrice = OfferPrice[0]
        }

        //构建子单
        //创建子单时间
        subOrderPlaceTime = now()
        //构建下达子单到流表
        subOrderStream = objByName('subOrderStream')
        // 插入子单流数据表
        insert into subOrderStream values(parentOrder.splitOrderId,parentOrder.batchId,
            parentOrder.splitOrderId+'_'+(parentOrder.sortNum+1),parentOrder.sortNum+1,
            parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
            parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
            parentOrder.tradeDate,subOrderQty,parentOrder.tradeDirection,parentOrder.market,parentOrder.handlerEmpid,
            parentOrder.handlerName,parentOrder.orderType,subOrderPrice,subOrderPlaceTime);

        //设置下单次数
        parentOrder.setAttr(`sortNum,parentOrder.sortNum+1)

        //判断是否还需继续下单
        if(remainQty>0){
            parentOrder.setAttr(`orderStatus,'下单中')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,subOrderPlaceTime)
            //设置下次下单的监听,等待时间为拆单策略参数中设定
            // addEventListener(handler=placeOrder, wait=duration(parentOrder.splitInterval+"s"), times=1)
            // 等待时间进行浮动
            realTime = randNum(parentOrder.lowSplitInterval, parentOrder.highSplitInterval)
            addEventListener(placeOrder,,,1,,duration(realTime+"s"))
        }else{//最后一次下单，销毁下单监听
            parentOrder.setAttr(`orderStatus,'下单完毕')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,now())
            //下单完结,销毁监视器
            destroyMonitor()
        }
    }
```

`placeOrder` 函数逻辑如下：

1. 判断当前时间是否超过拆单结束时间，若超过结束时间，则设置母单状态为 `'时限中止'`
   ，并调用`updatePOrderManageInfo` 函数更新母单最后修改时间。
2. 判断当前母单状态是否处于 `'初始化'` 或 `'下单中'`
   ，如果不满足，则停止拆单。
3. 根据成员变量 `subOrderQtys` 和母单属性 `tradeQuantity`
   计算剩余待下单股数 `remainQty` ，调用 `randNum` 函数确定子单的股数
   `subOrderQty` ，并对 `subOrderQtys` 和
   `remainQty` 进行更新。
4. 根据母单属性 `priceOption` 确定子单价格为买一还是卖一价格，并从键值内存表
   `snapshotOutputKeyedTb` 中查询。
5. 构建子单，并插入子单流表 `subOrderStream` 。
6. 根据剩余股数 `remainQty` 判断是否还需要下单。若还需要下单，则保存母单状态和修改时间，调用
   `randNum` 函数确定下单间隔，并定时再次调用 `placeOrder`
   函数重复上述步；若已经没有剩余股数，则保存母单状态和修改时间，最后摧毁监视器。

* **orderAlter 母单状态管理**

`startPlaceOrder` 函数中设置了对 `OrderAlterAction`
事件的监听。当 `OrderAlterAction` 事件注入，调用 `orderAlter`
函数对母单状态进行修改。

```
    //母单拆单变更操作
    def orderAlter(oaAction){

        alterOrderManage=objByName('alterOrderManage')
        insert into alterOrderManage values (oaAction.splitOrderId,oaAction.eventType,oaAction.operation,oaAction.batchId,oaAction.handlerEmpid,oaAction.handlerName,now())

        if(oaAction.operation=='暂停'){
            parentOrder.setAttr(`orderStatus,'暂停')
            updatePOrderManageInfo(parentOrder,now())
        }else if(oaAction.operation=='恢复'&& parentOrder.orderStatus=='暂停'){
            parentOrder.setAttr(`orderStatus,'下单中')
            updatePOrderManageInfo(parentOrder,now())
            //重新开始下单
            placeOrder()
        }else if(oaAction.operation=='终止母单'){
            parentOrder.setAttr(`orderStatus,'终止母单')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,now())
            //下单完结,销毁监视器
            destroyMonitor()
        }
    }
```

函数逻辑如下：

1. 将状态修改记录保存到状态修改流表 `alterOrderManage` 中。
2. 根据 `OrderAlterAction` 事件的 `operation`
   属性对母单做对应的操作。若 `operation` 为 `'暂停'`
   ，则将母单状态设置为暂停，并更新最后修改时间，此时 `placeOrder` 中的状态校验不通过，不会进行拆单操作；若
   `operation` 为 `'恢复'` 并且母单状态为
   `'暂停'` ，则将母单状态重置为下单中，并更新最后修改时间，此时
   `placeOrder` 中的状态校验通过，将继续拆单下单过程；若
   `operation` 为 `'终止母单'`
   ，则将母单状态设置为终止母单，更新最后修改时间，并摧毁监视器，结束拆单下单过程。

**step5-创建 CEP 引擎并订阅异构流表**

使用 `createCEPEngine` 函数创建 CEP 引擎，并使用
`subscribeTable` 函数使 CEP 引擎订阅异构流表
`orderBlobStream` ，`orderBlobStream` 中接收
`ParentOrder` 和 `OrderAlterAction` 事件流。

```
//创建下单任务引擎，表示TwapSplitMonitor引擎订阅的流数据表类型（母单类型和变更操作类型，多余的字段压缩到BLOB中）
dummy = table(1:0, `timestamp`eventType`blobs`splitOrderId, `TIMESTAMP`STRING`BLOB`STRING)
//创建cep 监听引擎
engine = createCEPEngine(name='TwapSplitMonitor', monitors=<TWAPSplitMonitor()>, dummyTable=dummy, eventSchema=[ParentOrder,OrderAlterAction],timeColumn=`timestamp)

// 订阅异构流表
subscribeTable(tableName="orderBlobStream", actionName="orderBlobStream",handler=getStreamEngine("TwapSplitMonitor"),msgAsTable=true)
```

**step6-回放行情数据**

使用 `replay` 函数，向行情快照流表 `snapshotStream`
中回放分布式表中的历史行情快照数据，模拟实时行情写入。

```
// 往行情流表里回放行情数据
snapshotTb = loadTable("dfs://l2TLDB_TWAP","snapshot")
// 回放前十支股票就行，选择需要的列
replayData = select Market,TradeDate,TradeTime,SecurityID,OfferPrice,BidPrice,OfferOrderQty,BidOrderQty
            from snapshotTb where SecurityID in (select distinct SecurityID from snapshotTb limit 10) and TradeTime>=09:30m
// 每秒20条回放
submitJob("replay_snapshot", "snapshot",  replay{replayData, snapshotStream, `TradeDate, `TradeTime, 20, true})
```

本例中历史行情快照数据保存在分布式表 `snapshot` 中，由于基金行情快照数据太多，这里仅回放 10
条基金的行情数据。`snapshotStream` 接收到回放数据后，自动将增量数据发布到
`snapshotOutputKeyedTb` 。最终
`snapshotOutputKeyedTb` 中，保存 10 支基金的最新行情快照数据。

**step7-启动策略实例**

使用 DolphinDB 提供的 JAVA API ，将 `ParentOrder` 事件放入
`orderBlobStream` ，启动拆单策略；随后将
`OrderAlterAction` 事件放入 `orderBlobStream` ，观察
CEP 引擎对母单状态的管理。核心函数 `putOrder` 如下。完整的启动策略项目文件见附录。

```
      public static void putOrder() throws IOException, InterruptedException {

        //        连接dolphindb数据库
        DBConnection conn = DBUtil.getConnection();
        //        封装母单订阅流表
        EventSender sender1 = EventSenderHelperTWAP.createEventSender(conn);
        //      拿到拆单参数map
        HashMap<String, Object> map = getMap();

        //        定义母单
        DolphinDbParentSplitParamsVo dolphinDbParentVo1 = new DolphinDbParentSplitParamsVo(
                "SP_001_2025030500001",                    // splitOrderId: 母单拆单操作单元唯一ID
                "ParentOrder",                  // eventType: 事件类型
                "2025030500001",           // batchId: 母单唯一ID
                "",    // tagBatchId: 子单唯一ID
                0,                              // sortNum: 拆单顺序号（从1开始）
                "501019",                       // fundCode: 基金代码
                "蓝筹精选混合",                  // fundName: 基金名称
                "A123456789",                   // assetId: 资产单元ID
                "量化投资组合",                  // assetName: 资产单元名称
                "C789",                         // combinationNo: 组合编号
                "全天候策略",                    // combinationName: 组合名称
                "600000",                       // stockCode: 证券代码
                "浦发银行",                      // stockName: 证券名称
                "20231010",                     // tradeDate: 交易日期（yyyyMMdd）
                48000L,                         // tradeQuantity: 交易量（注意L后缀）
                "B",                            // tradeDirection: 交易方向（1-买入）
                "SSE",                          // market: 交易市场
                "E1001",                        // handlerEmpid: 执行人工号
                "王强",                          // handlerName: 执行人姓名
                (String) map.get("splitMethod"),     // splitMethod: 拆单算法
                (String) map.get("orderType"),      // orderType: 订单类型
                (Double) map.get("price"),           // 子单下单价格
                (Integer) map.get("priceOption"),    //选择卖一价格下子单
                (LocalDateTime) map.get("startTime"),   // startTime: 拆单开始时间
                (LocalDateTime) map.get("endTime"),     // endTime: 拆单结束时间
                (Integer) map.get("lowChildOrderQty"),  //子单数量范围
                (Integer) map.get("highChildOrderQty"),
                (Integer) map.get("lowSplitInterval"),   // splitInterval: 拆单间隔范围（秒）
                (Integer) map.get("highSplitInterval"),
                "",                        // orderStatus: 拆单状态
                LocalDateTime.now()             // eventTime: 事件下达时间
        );
        //        定义暂停操作
        DolphinDbOrderActionVo orderAlterAction = new DolphinDbOrderActionVo(
                "SP_001_2025030500001",                    // splitOrderId: 母单拆单操作单元唯一ID
                "subOrder",                      // eventType
                "暂停",                        // operation
                "2025030500001",              // batchId
                "OOOO1",                      // handlerEmpid
                "王强",                        // handlerName
                LocalDateTime.now()           // eventTime
        );
        //        定义恢复操作
        DolphinDbOrderActionVo orderAlterAction1 = new DolphinDbOrderActionVo(
                "SP_001_2025030500001",                    // splitOrderId: 母单拆单操作单元唯一ID
                "subOrder",                      // eventType
                "恢复",                        // operation
                "2025030500001",              // batchId
                "OOOO1",                      // handlerEmpid
                "王强",                        // handlerName
                LocalDateTime.now()           // eventTime
        );

        //发送母单，将母单放入订阅流表，供CEP引擎消费
        sender1.sendEvent(dolphinDbParentVo1.getEventType(), dolphinDbParentVo1.toEntities());
        System.out.println("母单放入母单订阅流表");
        Thread.sleep(5000);

        //下达暂停，将母单状态暂停单放入订阅流表，供CEP引擎消费
        sender1.sendEvent(orderAlterAction.getEventType(), orderAlterAction.toEntities());
        System.out.println("暂停单放入订阅流表");
        Thread.sleep(5000);

        //下达恢复，将母单状态恢复单放入订阅流表，供CEP引擎消费
        sender1.sendEvent(orderAlterAction1.getEventType(), orderAlterAction1.toEntities());
        System.out.println("恢复单放入订阅流表");
    }
```

母单中的拆单参数，通过 `HashMap` 传入，模拟现实系统中的用户自定义拆单参数传递。

### 2.4 结果检视

本小节通过查看输出事件展示拆单系统运行的结果。DolphinDB Web
端提供了强大的数据可视化和分析工具——数据面板（Dashboard），旨在帮助用户更好地理解和利用数据。在本例中，母单事件、母单状态修改事件注入 CEP
引擎都分别记录到对应的内存表，拆分子单进行下单记录到子单接收流表，如此在 Dashboard 中便可以选取需要的数据进行可视化。

**step1-JAVA 环境准备**

配置系统的 maven 、jdk 环境，本例中的 jdk 和 maven 版本如下：

```
jdk - java version "1.8.0_441"
maven - Apache Maven 3.8.6
```

**step2-数据准备**

下载附录中的 TWAP 算法代码并解压。将 `data/snapshot_twap.csv` 放到
`dolphindb/server` 目录下。运行导入脚本
`data/data_input.dos` 进行建库建表，并将测试数据导入建好的分布式表中。将
`data/dashboard.TWAP 拆单监控.json` 导入到 Dashboard。

**step3-系统环境准备**

运行脚本 `01 clearEnv.dos` 、 `02 Event.dos` 、
`03 createTable.dos` 、 `04
subscribeSnapshot.dos` 。`01 clearEnv.dos`
脚本将系统中已存在的内存共享表、订阅信息、流式引擎等进行清除，确保不会重复定义； `02 Event.dos` 、
`03 createTable.dos` 、 `04
subscribeSnapshot.dos`
脚本分别对应上文介绍的定义事件类、创建母单子单记录内存表、键值内存表订阅流表的功能。

**step4-CEP引擎创建**

运行脚本 `05 Monitor.dos` 、`06 createCEPEngine.dos`
，分别对应上文中定义监视器、创建CEP引擎订阅异构流表的功能。

**step5-回放行情快照数据**

运行脚本 `07 replaySnapshot.dos` ，将快照数据回放到快照流表
`snapshotStream` 中。由于键值内存表
`snapshotOutputKeyedTb` 订阅了 `snapshotStream`
，数据会被自动发布到 `snapshotOutputKeyedTb` 中。回放后使用如下语句查询
`snapshotOutputKeyedTb` 中的数据：

```
select * from snapshotOutputKeyedTb
```

查询到十支基金的最新的行情数据如下：

![](images/order_splitting_with_cep/2_5.png)

图 6. 图2-5 键值内存表数据示意图

其中前四列分别表示基金所属市场、交易日期、交易时间和基金唯一代码； `OfferPrice` 和
`BidPrice` 表示市场中卖盘和买盘十档价格；`OfferOrderQty` 和
`BidOrderQty` 表示市场中对应的卖盘和买盘十档委托量。

**step6-启动策略**

下载附录中的 JAVA API 策略启动代码并解压。修改 `common/DBUtil.java`
中的数据库配置为用户自己的环境。运行 `startTWAP.java` ，将母单事件、母单状态修改事件放入异构流表中，观察
Dashboard 中，母单监控、子单监控、变更单监控中的对应输出如下：

![](images/order_splitting_with_cep/2_6.png)

图 7. 图2-6 Dashboard输出结果图

本例中，`startTWAP.java` 中指定：母单总股数为 48000 ，子单的下单数量在 10000 ~ 12000
间浮动，下单间隔在 7s ~ 9s 间浮动，母单的基金代码是 `501019` ，
`priceOption` 指定为 0 即选择子单价格为买一价格。

可以观察到，子单的下单数量在给定范围内随机；从子单的下单时间也能推理出，下单间隔也在给定范围内随机；子单的下单价格为
`snapshotOutputKeyedTb` 中基金代码为 `501019`
的买一价格。

### 2.5 总结

本章通过循序渐进的方式，介绍了如何使用 DolphinDB 的 CEP引擎实现 TWAP
拆单算法。首先说明了算法思想；然后模块化介绍了系统的功能；其次详细介绍了系统的实现流程和代码，其中最复杂的是监视器定义的部分，详细阐述了各个函数之间的调用关系；最后将系统的拆单过程，在结果检视部分使用
Dashboard 进行展示。

## 3. VWAP 拆单算法

本章将介绍如何使用 CEP 引擎实现 VWAP 拆单算法。

### 3.1 算法思想

VWAP（Volume Weighted Average
Price，成交量加权平均价格）算法是一种广泛使用的拆单交易策略，主要适用于大额订单执行。该模型通过分析历史成交量分布模式，将大订单按成交量比例拆分到各个时间段执行，使成交均价尽可能接近市场
VWAP 基准。VWAP 的计算公式如下：

![](images/order_splitting_with_cep/formula2.png)

其中，*pricei* 为分割节点上拆分订单的价格，*volumei*为分割节点上拆分订单的股数。

与 TWAP 均匀分配不同，VWAP
会根据市场典型的成交量分布特征动态调整下单量，在成交量大的时段分配更多订单，在成交量小的时段分配较少订单。这种设计既考虑了时间因素，又充分尊重市场的流动性分布规律。

### 3.2 功能模块

VWAP 算法的功能模块与上文中的 TWAP 相似。算法逻辑通过 CEP 引擎实现；通过数据回放功能模拟实时行情快照写入；使用流表订阅功能解耦用户母单发布和拆单
CEP 引擎。大致流程如下图所示。

![](images/order_splitting_with_cep/3_1.png)

图 8. 图3-1 VWAP算法流程图

与 TWAP 算法不同的是：

* VWAP
  拆单的子单股数不再是给定范围内随机，而是根据前一天的逐笔交易数据，先计算出每个时段的交易量占全天总交易量的比例，子单股数为前一天当前时段的交易量比例与母单股数的乘积。本例中时段长度为一分钟。
* VWAP 拆单的时间间隔不再是给定范围内随机，而是固定的时段间隔，即一分钟。

### 3.3 代码实现

在本节中我们介绍 VWAP 算法的代码实现，也主要围绕与上文 TWAP 算法的区别来阐述。

**step1-定义事件类**

定义事件类代码与 TWAP 算法 [step1-定义事件类](#topic_o4y_qj3_fgc__step1)
类似，不同的是，母单类中不再有子单股数范围上下限、拆单间隔范围上下限四个参数：

```
	//拆单参数开始
    splitMethod :: STRING          // 拆单算法
    orderType :: STRING            // 订单类型（限价/市价）
    price :: DOUBLE                // 限定价格
    priceOption :: INT             // 买一还是卖一价格
    startTime :: TIMESTAMP         // 拆单开始时间
    endTime :: TIMESTAMP           // 拆单结束时间
    orderStatus :: STRING          // 拆单状态
	//拆单参数结束
    eventTime :: TIMESTAMP         // 事件下达时间
```

**step2-创建**

* 创建母单记录内存表 `parentOrderManage` ，修改订单记录内存表
  `alterOrderManage` ，子单接收流表
  `subOrderStream` 以及 CEP 引擎订阅的异构流数据表
  `orderBlobStream` 。代码同 TWAP 算法。
* 创建一个内存表，用于存储基金一天每分钟的交易量。代码如下：

  ```
  // 创建内存表，用于存储每分钟的交易量
  trade = loadTable("dfs://l2TLDB","trade")
  tradeData = select * from trade where SecurityID  = "300041" and  TradeDate = 2023.02.01
  QtyTB =select * from (select sum(TradeQty) as TradeQty from tradeData group by minute(TradeTime) as TradeTimeInterval order by TradeTimeInterval) where  TradeTimeInterval > 09:29m
  share QtyTB as QtyTb
  ```

最终 `QtyTb` 表中记录了基金一天每分钟的交易量，如图所示。

![](images/order_splitting_with_cep/3_2.png)

图 9. 图3-2 历史交易量表

**step3-键值内存表订阅流表**

键内存表订阅流表代码同 TWAP 算法 [step3-键值内存表订阅流表](#topic_o4y_qj3_fgc__p_iqd_s53_fgc) 。

**step4-定义监视器**

VWAP 拆单算法中，子单股数和拆单时间间隔不需要在给定范围内随机，因此监视器类中不需要 `rand`
函数。监视器类的结构如下：

```
class SplitMonitor:CEPMonitor{
	def SplitMonitor() {
		//本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
	}
    //初始记录母单记录信息
    def initPOrderManageInfo(pOrder){...}
    //更新母单记录信息
    def updatePOrderManageInfo(pOrder,opTime){...}
}

//vwap 算法下单监听 monitor，继承关系
class VWAPSplitMonitor:SplitMonitor {
    // 记录子单总下股数的变量
    subOrderQtys :: INT
    // 母单
	parentOrder :: ParentOrder
    // 开始拆单与历史交易表对应的时间(分钟)
    splitStartTime :: MINUTE

	def VWAPSplitMonitor() {
		//本例中，初始monitor 不需要传值, 在克隆复制任务monitor 时进行设置。
	}

    //VWAP 下单方法
    def placeOrder(){...}

    //初始化parentOrder，进行拆单下单，设置OrderAlterAction事件监听
    def startPlaceOrder(pOrder){...}

    //创建母单下单monitor实例
	def forkParentOrderMonitor(pOrder){}

	//初始任务
	def onload(){
		addEventListener(forkParentOrderMonitor, "ParentOrder", ,"all")
	}
}
```

成员变量 `subOrderQtys` ：使用 `subOrderQtys`
记录当前已下子单的股数和，避免超出母单股数。

成员变量 `parentOrder` ：记录当前母单的参数，包括基本信息，拆单参数，和拆单状态。

成员变量 `splitStartTime` ：记录当前子单的时间，与历史交易表时段对应。

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
。当监听到该类型事件时，下一步将启动整个拆单下单过程。为了控制母单拆单下单的线程安全，为每个母单创建不同的 Monitor 实例，因此在对应的回调函数
`forkParentOrderMonitor` 中需要包含对 Monitor 实例的创建和母单参数传递等步骤。从
`onload` 方法开始，函数调用的流程与实现的功能可以分为三个模块，如下图所示。

![](images/order_splitting_with_cep/3_3.png)

图 10. 图3-3 函数调用模块图

其中， `startPlaceOrder` 函数是两个模块的启动函数，启动顺序如上图所示。模块 3
中，函数调用的流程与实现的功能如下图所示。

![](images/order_splitting_with_cep/3_4.png)

图 11. 图3-4 模块三函数调用流程图

接下来从策略启动事件对应的回调函数 `forkParentOrderMonitor` 开始来介绍具体的代码实现。

* **forkParentOrderMonitor 生成监视器实例**

`forkParentOrderMonitor` 函数代码实现同 TWAP 算法 [step4-定义监视器](#topic_o4y_qj3_fgc__p_m2q_s53_fgc) 。

* **startPlaceOrder 启动核心模块**

`startPlaceOrder` 函数代码实现大致同 TWAP 算法 [step4-定义监视器](#topic_o4y_qj3_fgc__p_m2q_s53_fgc)
。但需要对拆单时间进行初始化。

```
        // 交易开始时间初始化
        splitStartTime = minute(09:30m)
```

即从上午 9:30 开始拆单。

* **initPOrderManageInfo 记录母单信息**

`initPOrderManageInfo` 函数代码实现同 TWAP 算法 [step4-定义监视器](#topic_o4y_qj3_fgc__p_m2q_s53_fgc) 。

* **updatePOrderManageInfo 更新母单最后修改时间**

`updatePOrderManageInfo` 函数代码实现同 TWAP 算法 [step4-定义监视器](#topic_o4y_qj3_fgc__p_m2q_s53_fgc) 。

* **placeOrder 拆单核心函数**

`placeOrder` 函数是拆单下单的核心函数，对应模块 3 中的后半部分。

```
    //VWAP 下单方法
    def placeOrder(){
        writeLog("============开始下单==========")
        //判断是否超过下单时限
        if(now()>= parentOrder.endTime){ //当前时间大于下单结束时间,则不再下单
            parentOrder.setAttr(`orderStatus,'时限中止')
            updatePOrderManageInfo(parentOrder,now())
            // 摧毁监视器
            destroyMonitor()
            return
        }
        //判断当前母单状态是否是可以下单状态,不是则退出
        if(!(parentOrder.orderStatus in ['初始化','下单中'])){
            return
        }

        //计算剩余待下单股数 = 母单股数 - 所有子单数
        remainQty = parentOrder.tradeQuantity - subOrderQtys
        // 计算当前应该下的子单数
        // 查找历史交易表，计算总交易量
        totalQty = exec sum(TradeQty) from QtyTb
        // 跳过中间的空白区域
        if(splitStartTime==11:31m){
            splitStartTime = 13:00m
        }
        // 将当前拆单时间转为分钟
        nowTime = minute(splitStartTime)
        // 查找历史交易表，当前时段（一分钟），是否有交易量
        nowQtyVector = exec TradeQty from QtyTb where TradeTimeInterval=nowTime

        // 确定子单股数
        if(nowQtyVector.size()==0){//当前时段没有交易记录，不下单，直接设置下一次下单的监听
            parentOrder.setAttr(`orderStatus,'下单中')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,now())
            // 将拆单时间更新
            splitStartTime = temporalAdd(splitStartTime,1,"m")
            //设置下次下单的监听,等待时间为10s
            addEventListener(placeOrder,,,1,,duration(10+"s"))
            return
        }else{
            // 拿到当前时段总交易量
            nowQty = nowQtyVector[0]
            totalNum = parentOrder.tradeQuantity
            // 根据比例计算，这里类型转换是为了计算小数比例，否则为0，最后向上取整
            subOrderQty = ceil((double(nowQty)/totalQty)*totalNum)
            // subOrderQty可能会超过剩余单数
            subOrderQty = (subOrderQty>remainQty) ? remainQty : subOrderQty
        }

        // 将拆单时间更新
        splitStartTime = temporalAdd(splitStartTime,1,"m")

        // 更新子单股数
        subOrderQtys = subOrderQtys+subOrderQty
        // 更新剩余单数
        remainQty = remainQty-subOrderQty

        // 拿到母单的基金代码
        v_securityId = parentOrder.fundCode
        // 直接从分布式表中进行查询，定义一个函数
        if(parentOrder.priceOption == 0){//从买一价格获取，从BidPrice[0]获取价格
            // 从键值对表中获取
            BidPrice = exec BidPrice from snapshotOutputKeyedTb where SecurityID = v_securityId
            // 买一价格
            subOrderPrice = BidPrice[0]
        }else{//从卖一价格获取，从OfferPrice[0]获取价格
            // 从键值对表中获取
            OfferPrice = exec OfferPrice from snapshotOutputKeyedTb where SecurityID = v_securityId
            // 卖一价格
            subOrderPrice = OfferPrice[0]
        }

        //构建子单
        //创建子单时间
        subOrderPlaceTime = now()
        //构建下达子单到流表

        subOrderStream = objByName('subOrderStream')
        // 插入子单流数据表
        insert into subOrderStream values(parentOrder.splitOrderId,parentOrder.batchId,
            parentOrder.splitOrderId+'_'+(parentOrder.sortNum+1),parentOrder.sortNum+1,
            parentOrder.fundCode,parentOrder.fundName,parentOrder.assetId,parentOrder.assetName,
            parentOrder.combinationNo,parentOrder.combinationName,parentOrder.stockCode,parentOrder.stockName,
            parentOrder.tradeDate,subOrderQty,parentOrder.tradeDirection,parentOrder.market,
            parentOrder.handlerEmpid,parentOrder.handlerName,parentOrder.orderType,subOrderPrice,subOrderPlaceTime);
        //设置下单次数
        parentOrder.setAttr(`sortNum,parentOrder.sortNum+1)
        //更新剩余股数
        updateRemainQty()
        //判断是否还需继续下单
        if(remainQty>0){
            parentOrder.setAttr(`orderStatus,'下单中')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,subOrderPlaceTime)
            //设置下次下单的监听,等待时间为10s
            addEventListener(placeOrder,,,1,,duration(10+"s"))
        }else{//最后一次下单，销毁下单监听
            parentOrder.setAttr(`orderStatus,'下单完毕')
            //保存母单信息
            updatePOrderManageInfo(parentOrder,now())
            //下单完结,销毁监视器
            destroyMonitor()
        }
    }
```

`placeOrder` 函数逻辑如下：

1. 判断当前时间是否超过拆单结束时间，若超过结束时间，则设置母单状态为 `'时限中止'`
   ，并调用`updatePOrderManageInfo` 函数更新母单最后修改时间。
2. 判断当前母单状态是否处于 `'初始化'` 或 `'下单中'`
   ，如果不满足，则停止拆单。
3. 根据成员变量 `subOrderQtys` 和母单属性 `tradeQuantity`
   计算剩余待下单股数 `remainQty` ，查询历史交易表 `QtyTb`
   ，根据当前时段的历史交易比例和母单股数，计算确定子单的股数 `subOrderQty` ，并对
   `subOrderQtys` 和 `remainQty` 进行更新。
4. 根据母单属性 `priceOption` 确定子单价格为买一还是卖一价格，并从键值内存表
   `snapshotOutputKeyedTb` 中查询。
5. 构建子单，并插入子单流表 `subOrderStream` 。
6. 根据剩余股数 `remainQty` 判断是否还需要下单。若还需要下单，则保存母单状态和修改时间，并定时再次调用
   `placeOrder` 函数重复上述步；若已经没有剩余股数，则保存母单状态和修改时间，最后摧毁监视器。

**step5-创建 CEP 引擎订阅异构流表**

创建 CEP 引擎订阅异构流表代码同 TWAP 算法 [step5-创建
CEP 引擎并订阅异构流表](#topic_o4y_qj3_fgc__p_lfg_553_fgc) 。

**step6-回放行情数据**

回放行情数据代码同 TWAP 算法 [step6-回放行情数据](#topic_o4y_qj3_fgc__p_a5r_553_fgc) 。

**step7-启动策略实例**

启动策略实例代码同 TWAP 算法 [step7-启动策略实例](#topic_o4y_qj3_fgc__p_fyc_v53_fgc) 。

### 3.4 结果检视

本小节通过查看 Dashboard 中输出事件展示拆单系统运行的结果。在本例中，母单事件、母单状态修改事件注入 CEP
引擎都分别记录到对应的内存表，拆分子单进行下单记录到子单接收流表，如此在 Dashboard 中便可以选取需要的数据进行可视化。

**step1-JAVA环境准备**

配置系统的 maven 、jdk 环境，本例中的 jdk 和 maven 版本如下：

```
jdk - java version "1.8.0_441"
maven - Apache Maven 3.8.6
```

**step2-数据准备**

下载附录中的 VWAP 算法代码并解压。将 `data/snapshot_vwap.csv`
、`data/trade.csv`放到 `dolphindb/server`
目录下。运行导入脚本 `data/data_input_snapshot.dos`
进行建库建表，并将测试数据导入建好的分布式表中。运行导入脚本 `data/data_input_trade.dos`
进行建库建表，并将测试数据导入建好的分布式表中。将 `data/dashboard.VWAP 拆单监控.json` 导入到
Dashboard 。

**step3-系统环境准备**

运行脚本 `01 clearEnv.dos` 、 `02 Event.dos` 、
`03 createTable.dos` 、 `04
subscribeSnapshot.dos` 。`01 clearEnv.dos`
脚本将系统中已存在的内存共享表、订阅信息、流式引擎等进行清除，确保不会重复定义； `02 Event.dos` 、
`03 createTable.dos` 、 `04
subscribeSnapshot.dos` 脚本分别对应上文介绍的定义事件类、创建内存表、键值内存表订阅流表的功能。

**step4-CEP 引擎创建**

运行脚本 `05 Monitor.dos` 、`06 createCEPEngine.dos`
，分别对应上文中定义监视器、创建CEP引擎订阅异构流表的功能。

**step5-回放行情快照数据**

运行脚本 `07 replaySnapshot.dos` ，将快照数据回放到快照流表
`snapshotStream` 中。由于键值内存表
`snapshotOutputKeyedTb` 订阅了 `snapshotStream`
，数据会被自动发布到 `snapshotOutputKeyedTb` 中。

**step6-启动策略**

下载附录中的 JAVA API 策略启动代码并解压。修改 `common/DBUtil.java`
中的数据库配置为用户自己的环境。运行 `startVWAP.java` ，将母单事件放入异构流表中，观察 Dashboard
中的输出。

* 子单监控中的对应输出如下:

![](images/order_splitting_with_cep/3_5.png)

图 12. 图3-5 子单监控输出

本例中，`startVWAP.java` 中指定：母单的基金代码是 `300041`
，总股数为48000， `priceOption` 指定为 0 即选择子单价格为买一价格。

可以观察到，子单的下单数量根据当前时段的历史交易比例计算得到，下单时间间隔为 10s；子单的下单价格为
`snapshotOutputKeyedTb` 中基金代码为 `300041`
的买一价格。

### 3.5 总结

本章通过循序渐进的方式，介绍了如何使用 DolphinDB 的 CEP引擎实现 VWAP
拆单算法。首先说明了算法思想；然后模块化介绍了系统的功能；其次详细介绍了系统的实现流程和代码，其中最复杂的是监视器定义的部分，详细阐述了各个函数之间的调用关系；最后将系统的拆单过程，在结果检视部分使用
Dashboard 进行展示。

## 4. 总结

本文基于 CEP
引擎构建了一套完整的算法拆单调度框架。通过​​事件驱动架构​​和​​动态事件监听器​​来实现订单下达、拆单的监听与处理。同时利用​​键值内存表缓存实时行情快照，为子单价格计算提供毫秒级响应支持。在功能实现上，文中提供了了
TWAP 和 VWAP 拆单算法实现 Demo (随机浮动参数避免市场预测) ，并通过​​​​可视化监控面板​​进行了实时展示订单状态等信息。

## 5. 附录

### 5.1 TWAP 算法

[demo1\_TWAP](script/order_splitting_with_cep/demo1_TWAP.zip)

### 5.2 VWAP 算法

[demo2\_VWAP.zip](script/order_splitting_with_cep/demo2_VWAP.zip)

### 5.3 JAVA API 下达母单启动代码

[cepSplitDemo（基础）](script/order_splitting_with_cep/cepSplitDemo%EF%BC%88%E5%9F%BA%E7%A1%80%EF%BC%89.zip)
