# updateDataViewItems

## 语法

`updateDataViewItems(engine, keys, valueNames, newValues)`

## 详情

更新 DataView 引擎中指定键值对应的指定字段的值。若 *keys* 指定的键值列（key）不存在，则更新时会报错 。

该函数可在 CEP 引擎内部或外部调用。如果在 CEP 引擎内部调用此函数，系统将优先在 CEP 引擎中查找句柄为 *engine* 的 DataView
引擎；若未找到，则会在 CEP 引擎外部进行查找。如果在 CEP 引擎外部调用此函数，系统只会在 CEP 引擎外部进行查找。

## 参数

**engine** DataView 引擎句柄或引擎名。

**keys** 标量、向量或 tuple，表示需要更新的键值， 如果是复合键值，则需要传入一个 tuple，其中每个元素表示组成键值的列，且顺序需与引擎中
*keyedColumns* 的指定顺序保持一致。

**valueNames** 字符串标量或向量，需要更新的字段的名称，需要与 DataView 引擎中 *outputTable*
指定的列名匹配。

**newValues** 标量、向量或 tuple，表示需要更新的字段对应的值。指定方式同 *keys*。

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

**相关函数**：createCEPEngine, createDataViewEngine,
deleteDataViewItems, getDataViewEngine
