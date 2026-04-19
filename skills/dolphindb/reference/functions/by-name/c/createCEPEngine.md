# createCEPEngine

## 语法

`createCEPEngine(name, monitors, dummyTable, eventSchema,
[deserializeParallelism=1], [timeColumn], [eventQueueDepth=1024], [outputTable],
[dispatchKey], [dispatchBucket], [useSystemTime=true],
[eventTimeField="eventTime"])`

## 详情

创建一个复杂事件处理（CEP）引擎实例，用于处理实时事件流。

## 参数

**name** 字符串标量，表示 CEP 引擎的名称。可包含字母，数字和下划线，但必须以字母开头。

**monitors** 元代码或元代码元组，可包含一个或多个 Monitor 类的构造函数调用。如果指定了多个 Monitor 类的构造函数调用，在创建
subEngine 时，将按照指定的顺序构造这些对象。Monitor 的创建方法参见 简单的 Monitor
实例。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致。

**eventSchema** 事件类型类的声明，用于指定为外部输入的事件类型，可以是一个标量或向量。例如：

```
class event1 {
  var1:: STRING
  var2:: INT
  def event1(){
    var1 = ""
    var2 = 0
  }
}

class event2 {
  var1:: DOUBLE
  var2:: INT
  def event2(){
    var1 = 0.0
    var2 = 0
  }
}

//指定为标量
eventSchema = event1
//指定为向量
eventSchema = [event1, event2]
```

**deserializeParallelism** 整型标量，用于指定反序化的线程数，默认值为1。

**timeColumn** 可选参数，字符串标量或向量，用于指定 *dummyTable* 中的时间列。指定后，通过事件流序列化器（Stream
Event Serializer）向 CEP 引擎插入事件时，该列将作为事件时间。

**eventQueueDepth** 整型标量，用于指定子引擎接收事件队列和输出队列的最大深度，默认值是1024。

**outputTable** 可选参数，可以指定为一个或多个 `StreamEventSerializer`
返回的序列化器。用于配合 emitEvent 函数将事件输出到序列化器指定的输出表中。不同序列化器之间的序列化与输出过程相互独立，并发执行。

**dispatchKey** 字符串标量，用于指定事件中的属性，该属性中的每个唯一值被视为一个 key。若不指定
*dispatchKey*，则引擎将创建一个名为 *name* 的子引擎（与 CEP 引擎同名）。

**dispatchBucket** 整型标量，表示哈希分组的数量。如果指定该参数，引擎将对 *dispatchKey*指定的字段进行哈希分组*。*

注意：

* CEP 引擎根据 *dispatchKey* 和 *dispatchBucket*
  自动创建子引擎，并行处理数据。各个子引擎之间互相独立。若未指定 *dispatchKey*，则 CEP
  引擎只有一个处理线程，即只创建一个子引擎。
* 当监听多种事件类型时，事件分发遵循以下规则：

  + 包含 `dispatchKey` 指定字段的事件：根据字段值哈希分发到对应的特定子引擎
  + 不包含 `dispatchKey` 指定字段的事件：将被广播发送到所有子引擎

**useSystemTime** 布尔值，表示是否使用数据注入引擎时的系统时间进行计算。

* 当 *useSystemTime* = true 时（缺省值）时，CEP
  引擎中的计算都基于数据注入引擎的时刻（以毫秒精度表示的本地系统时间）进行，与数据中的时间列无关。
* 当 *useSystemTime* = false 时，CEP 引擎中的计算都基于数据中的 *timeColumn* 列进行。

**eventTimeField** 可选参数，字符串标量或向量，用于指定事件中的时间字段，仅在 *useSystemTime* = false
有效。如果所有事件的时间字段名都相同，则 *eventTimeField* 是一个标量；否则，*eventTimeField* 是一个向量，其长度和
*eventSchema* 的长度相同，每个元素分别代表每个事件的时间字段。通过 `appendEvent` 直接向
CEP 引擎插入事件时，必须通过该参数指定事件的时间。

## 返回值

一个表。

## 例子

例 1. 本例创建三种类型的事件（市场数据、订单、成交），且为每种事件类型创建了独立的序列化器。最后，通过 `appendEvent`
将事件注入引擎，由引擎根据事件类型选择对应的序列化器，并输出到不同的流表中。此外，例子中通过设置 *dispatchKey*='code' 和
*dispatchBucket*=4，实现按股票分组并行处理的功能。

```
class MarketData{
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def MarketData(m,c,p,q){
        market = m
        code = c
        price = p
        qty = q
    }
}

class Orders{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def Orders(t, m,c,p,q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
    }
}

class Trades{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def Trades(t, m,c,p,q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
    }
}

share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as MarketDataChannel
serializer1 = streamEventSerializer(name=`MarketDataChannel, eventSchema=[MarketData], outputTable=MarketDataChannel)

share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as OrdersChannel
serializer2 = streamEventSerializer(name=`OrdersChannel, eventSchema=[Orders], outputTable=OrdersChannel)

share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as TradesChannel
serializer3 = streamEventSerializer(name=`TradesChannel, eventSchema=[Trades], outputTable=TradesChannel)

class SimpleShareSearch:CEPMonitor {
	//构造函数
	def SimpleShareSearch(){
	}
	def processMarketData(event){
        emitEvent(event,,"MarketDataChannel")
    }
    def processOrders(event){
        emitEvent(event,,"OrdersChannel")
    }
    def processTrades(event){
        emitEvent(event,,"TradesChannel")
    }
	// 创建 CEP 子引擎之后，系统会自动构造 SimpleShareSearch 类对象为 Monitor 实例并调用 onload 函数
	def onload() {
		//监听StockTick事件
		addEventListener(handler=processMarketData, eventType="MarketData", times="all")
		addEventListener(handler=processOrders, eventType="Orders", times="all")
		addEventListener(handler=processTrades, eventType="Trades", times="all")
	}
}

dummy = table(array(STRING, 0) as eventType, array(BLOB, 0) as blobs)

engine = createCEPEngine(name='cep1', monitors=<SimpleShareSearch()>, dummyTable=dummy,
                        eventSchema=[MarketData,Orders,Trades],
                        outputTable=[serializer1,serializer2,serializer3],
                        dispatchKey=`code, dispatchBucket=4)  // 按股票代码分组，创建4个并行处理组

m= MarketData("m", "c", 10.0, 100)
appendEvent(engine, m)

o = Orders("a","m", "c", 10.0, 100)
t = Trades("a","m", "c", 10.0, 100)

appendEvent(engine, o)
appendEvent(engine, t)
```

例 1 中未指定
*useSystemTime*，因此引擎默认使用系统时间作为计算基准。在引擎内部的事件监听器（`addEventListener`）中，时间相关参数（例如
*within*、*exceedTime* 等）均使用时间注入引擎时的系统时间进行计算。

若希望使用事件自身的时间作为计算基准，则可以通过参数进行配置，示例如下。

例 2. 本例介绍如何使用数据中的时间列（事件时间）作为计算基准。CEP 引擎中的关键参数设置如下：

* *useSystemTime*=false：引擎使用事件时间而非系统时间进行计算
* *timeColumn*：指定 dummy 表中的时间列
* *eventTimeField*：指定事件中的时间字段名

```
// 首先清理环境
def cleanupCEPEngine(){
    try { dropStreamEngine("cep1") } catch(ex) {}
    try { dropStreamEngine("MarketDataChannel") } catch(ex) {}
    try { dropStreamEngine("OrdersChannel") } catch(ex) {}
    try { dropStreamEngine("TradesChannel") } catch(ex) {}

    try { dropStreamTable("MarketDataChannel") } catch(ex) {}
    try { dropStreamTable("OrdersChannel") } catch(ex) {}
    try { dropStreamTable("TradesChannel") } catch(ex) {}

    try { undef("MarketDataChannel", SHARED) } catch(ex) {}
    try { undef("OrdersChannel", SHARED) } catch(ex) {}
    try { undef("TradesChannel", SHARED) } catch(ex) {}

    print("CEP 引擎环境清理完成")
}
cleanupCEPEngine()

class MarketData{
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def MarketData(m,c,p,q,et){
        market = m
        code = c
        price = p
        qty = q
        eventTime = et
    }
}

class Orders{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def Orders(t, m,c,p,q,et){
        trader = t
        market = m
        code = c
        price = p
        qty = q
        eventTime = et
    }
}

class Trades{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def Trades(t, m,c,p,q,et){
        trader = t
        market = m
        code = c
        price = p
        qty = q
        eventTime = et
    }
}

share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as MarketDataChannel
serializer1 = streamEventSerializer(name=`MarketDataChannel, eventSchema=[MarketData], outputTable=MarketDataChannel)

share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as OrdersChannel
serializer2 = streamEventSerializer(name=`OrdersChannel, eventSchema=[Orders], outputTable=OrdersChannel)

share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as TradesChannel
serializer3 = streamEventSerializer(name=`TradesChannel, eventSchema=[Trades], outputTable=TradesChannel)

class SimpleShareSearch:CEPMonitor {
    def SimpleShareSearch(){
    }
    def processMarketData(event){
        emitEvent(event,,"MarketDataChannel")
    }
    def processOrders(event){
        emitEvent(event,,"OrdersChannel")
    }
    def processTrades(event){
        emitEvent(event,,"TradesChannel")
    }
    def onload() {
        addEventListener(handler=processMarketData, eventType="MarketData", times="all")
        addEventListener(handler=processOrders, eventType="Orders", times="all")
        addEventListener(handler=processTrades, eventType="Trades", times="all")
    }
}

// 创建 CEP 引擎，修改 dummy 表结构，添加 eventTime 列
dummy = table(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs)

// 创建 CEP 引擎，同时指定 timeColumn 和 eventTimeField
engine = createCEPEngine(name='cep1', monitors=<SimpleShareSearch()>, dummyTable=dummy,
                        eventSchema=[MarketData,Orders,Trades],
                        outputTable=[serializer1,serializer2,serializer3],
                        dispatchKey=`market, dispatchBucket=4,
                        useSystemTime=false, timeColumn=`eventTime,
                        eventTimeField=`eventTime)

// 创建和注入事件
// 创建事件时指定 eventTime
currentTime = 2026.03.01T09:30:00.000
m1 = MarketData("NASDAQ", "AAPL", 10.0, 100, currentTime)
m2 = MarketData("NYSE", "IBM", 150.0, 200, currentTime)

currentTime = 2026.03.01T09:30:01.000
o1 = Orders("trader1","NASDAQ", "AAPL", 10.0, 100, currentTime)
o2 = Orders("trader2","NYSE", "IBM", 150.0, 200, currentTime)

currentTime = 2026.03.01T09:30:02.000
t1 = Trades("trader1","NASDAQ", "AAPL", 10.0, 100, currentTime)
t2 = Trades("trader2","NYSE", "IBM", 150.0, 200, currentTime)

// 注入事件
appendEvent(engine, m1)
appendEvent(engine, m2)
appendEvent(engine, o1)
appendEvent(engine, o2)
appendEvent(engine, t1)
appendEvent(engine, t2)
```

**相关函数**：addEventListener, dropStreamEngine, getCEPEngineStat, stopSubEngine
