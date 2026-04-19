# routeEvent

## 语法

`routeEvent(event)`

## 详情

routeEvent 是 CEP monitor 内部的事件控制接口，用于将一个事件插入到当前子引擎的事件输入队列的队首。

## 参数

**event** 事件实例。

## 例子

定义事件：

```
class UpdateFactor{
    sym :: STRING
    factor :: DOUBLE
    def UpdateFactor(code, val){
        sym = code
        factor = val
    }
}

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
```

定义 monitor：

```
class MainMonitor : CEPMonitor{
    maxPrice :: DOUBLE

    def MainMonitor(){ maxPrice = 0.0 }

    def updateMarketData(event)

    // Monitor 启动时注册事件监听器
    def onload(){
        addEventListener(handler=updateMarketData, eventType='MarketData', times='all')
    }

    // 核心事件处理函数
    def updateMarketData(event){
        print("处理 MarketData: "+event.code+" 价格="+string(event.price))

        if(event.price > maxPrice){
            maxPrice = event.price

            // emitEvent：输出到流表
            emitEvent(UpdateFactor("maxPrice", maxPrice))

            // routeEvent：队首插入一个警告事件，优先处理
            routeEvent(UpdateFactor("alert", maxPrice))

            // sendEvent：队尾插入一个信息事件，顺序处理
            sendEvent(UpdateFactor("info", maxPrice))
        }
    }
}
```

创建流表接收输出事件：

```
share streamTable(array(STRING,0) as eventType, array(BLOB,0) as blobs) as simulateResult

serializer = streamEventSerializer(
    name=`simulate,
    eventSchema=[UpdateFactor],
    outputTable=simulateResult
)

dummy = table(array(STRING,0) as eventType, array(BLOB,0) as blobs)
```

创建 CEP 引擎：

```
engine = createCEPEngine(
    name='cep1',
    monitors=<MainMonitor()>,
    dummyTable=dummy,
    eventSchema=[MarketData],
    outputTable=serializer
)
```

**相关函数**：addEventListener, createCEPEngine, appendEvent,
emitEvent, sendEvent
