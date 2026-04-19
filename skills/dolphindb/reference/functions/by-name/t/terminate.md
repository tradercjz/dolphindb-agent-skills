# terminate

## 语法

`terminate()`

## 详情

`terminate` 是 EventListener
类的方法，用于停止当前事件监听器的运行。调用后，该监听器将不再继续接收或处理新的事件，即便其匹配条件仍满足也不会再触发回调函数。通常用于在运行过程中根据业务逻辑动态取消某些不再需要的事件监听，以避免资源占用或重复处理。

## 参数

无。

## 返回值

无。

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

**相关函数**：addEventListener
