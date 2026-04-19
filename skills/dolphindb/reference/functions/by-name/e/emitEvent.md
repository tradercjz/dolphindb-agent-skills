# emitEvent

## 语法

`emitEvent(event, [eventTimeField], [outputName])`

## 详情

`emitEvent` 是 CEP monitor 内部的事件控制接口，用于将事件插入到 CEP 引擎的事件输出队列的队尾。当 CEP
引擎指定了多个事件流序列化器时，`emitEvent` 必须通过参数 *outputName*
指定目标序列化器（`StreamEventSerializer`）的名称，CEP
引擎据此进行匹配，并将事件输出到对应的一个或多个流表中。

## 参数

**event** 事件实例。

**eventTimeField** 字符串标量，表示事件中的时间字段名。若要指定此参数，*event* 必须包含时间字段。当
*useSystemTime*=true 时，输出事件中的时间为系统时间；否则，输出最新事件时间。

**outputName** 可选，字符串标量，指定事件流序列化器的名称。

* 若 CEP 引擎中仅指定了一个输出表，则无需指定该参数。
* 若 CEP 引擎指定了多个输出表，必须指定 *outputName*，引擎将根据名称将事件输出至对应的序列化器。

## 返回值

无。

## 例子

下例展示如何通过 *outputName* 参数，指定不同事件流序列化器，由 CEP 引擎进行匹配，并将事件输出到对应的流数据表中。

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
    // 通过 emitEvent 指定事件流需要发送的序列化器的名称
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

// 创建 CEP 引擎，指定3个事件流序列化器
engine = createCEPEngine(name='cep1', monitors=<SimpleShareSearch()>, dummyTable=dummy, eventSchema=[MarketData,Orders,Trades], outputTable=[serializer1,serializer2,serializer3])

m= MarketData("m", "c", 10.0, 100)

appendEvent(engine, m)

o = Orders("a","m", "c", 10.0, 100)
t = Trades("a","m", "c", 10.0, 100)

appendEvent(engine, o)
appendEvent(engine, t)
```

**相关函数**：addEventListener, createCEPEngine, appendEvent, routeEvent, sendEvent
