# getDataViewEngine

## 语法

`getDataViewEngine([CEPEngine], dataViewEngineName)`

## 详情

获取 DataView 引擎中的数据。

## 参数

**CEPEngine** CEP 引擎的句柄。

**dataViewEngineName** DataView 引擎的名称。

## 返回值

一个表。该表记录了每个键值对应的最新记录。

## 例子

```
class trades{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def trades(t, m, c, p, q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
        eventTime = now()
    }
}

class mainMonitor:CEPMonitor{
    tradesTable :: ANY
    isBusy :: BOOL
    def mainMonitor(){
        tradesTable = array(ANY, 0)
        isBusy = false
    }

    def updateTrades(event)

    def updateTrades2(event)

    def unOnload(){
        undef('traderDV', SHARED)
    }

    def onload(){
        addEventListener(updateTrades, `trades, , "all",,,,,"trades1")
        addEventListener(updateTrades2, `trades, , "all",,,,,"trades2")
        traderDV = streamTable(array(STRING, 0) as trader, array(STRING, 0) as market, array(SYMBOL, 0) as code, array(DOUBLE, 0) as price, array(INT, 0) as qty, array(INT, 0) as tradeCount, array(BOOL, 0) as busy, array(DATE, 0) as orderDate, array(TIMESTAMP, 0) as updateTime)
        share(traderDV, 'traderDV')
        createDataViewEngine('traderDV', objByName('traderDV'), `trader, `updateTime, true)
    }

    def updateTrades(event) {
        tradesTable.append!([event.trader, event.market, event.code, event.price, event.qty])
        getDataViewEngine('traderDV').append!(table(event.trader as trader, string() as market, string() as code, 0.0 as price, 0 as qty, 0 as tradeCount, false as busy, date(event.eventTime) as orderDate))
        updateDataViewItems('traderDV', event.trader, ['market', 'code', 'price', 'qty', 'tradeCount'], [event.market, event.code, event.price, event.qty, tradesTable.size()])
    }

    def updateTrades2(event) {
        tradesTable.append!([event.trader, event.market, event.code, event.price, event.qty])
        getDataViewEngine('traderDV').append!(table(event.trader as trader, string() as market, string() as code, 0.0 as price, 0 as qty, 0 as tradeCount, false as busy, date(event.eventTime) as orderDate))
        updateDataViewItems('traderDV', event.trader, ['market', 'code', 'price', 'qty', 'tradeCount'], [event.market, event.code, event.price, event.qty, tradesTable.size()])
    }
}

dummy = table(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
engineCep = createCEPEngine('cep1', <mainMonitor()>, dummy, [trades], 1, 'eventTime', 10000)
trade1 = trades('t1', 'sz', 's001', 11.0, 10)
go
appendEvent(engineCep, trade1)
// 查看 monitor
monitors = getCEPEngineMonitor('cep1',"cep1","mainMonitor")
// 查看 listener
listeners = monitors.getEventListener()
print(listeners)
// 终止 listener
listeners['trades1'].terminate()
print(listeners)
```

**相关函数**：createCEPEngine, createDataViewEngine, deleteDataViewItems
