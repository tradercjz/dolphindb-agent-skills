# addEventListener

## 语法

`addEventListener(handler, [eventType], [condition], [times="all"], [at],
[wait], [within], [exceedTime], [name])`

## 详情

该函数用于为 CEP 引擎指定事件匹配规则和回调函数。事件监听器必须在 monitor
内调用，用于监测注入引擎的每个事件。当事件或事件模式与匹配规则相匹配时，会触发执行回调函数。

## 参数

**handler** 回调函数，如果指定了 *eventType*
则为一元函数，参数为匹配的事件。如果指定为按时间触发，则没有参数。

```
def actions1(stockVal){
    //将事件类型 stockVal 的属性写入一个共享表
    insert into objByName("sharedUSPrices") values([stockVal.price, stockVal.qty])
}
```

*handler*
中可以动态添加新的监听器：

```
def actions1(stockVal){
    //将事件类型 stockVal 的属性写入一个共享表
    insert into objByName("sharedUSPrices") values([stockVal.price, stockVal.qty])
    //新增加一个事件侦听器
    addEventListener(handler=action2, eventType="Stock", condition=<self.prices > stockVal.price>)
}
```

自 3.00.4 版本起，*handler* 支持调用 monitor
类之外的函数。调用外部类的方法时，应使用
self（当前实例的引用）进行访问，例如：

```
class Logic{
    monitor::ANY
    def Logic(monitor_){
        monitor = monitor_
    }
    def processTick(stockTickEvent) {
        str = "StockTick event received" +
                " name = " + stockTickEvent.name +
                " Price = " + stockTickEvent.price.string()
        writeLog(str)
    }
    def testAddListener(){
        monitor.addEventListener(self.processTick, "StockTick", ,"all")
    }
}
```

**eventType**字符串标量，表示事件类型。若指定为
"any"，则表示任意事件。

**condition**
元代码类型，指定匹配的事件条件，即事件匹配规则。元代码的返回结果必须是布尔值。例如 *eventType* 为 Stock 时，指定
<Stock.price > 10 and Stock.qty < 10> 。

**times**
可以是正整数或者 "all"，表示在 *handler* 被触发指定次数后自动删除监听，默认为 "all"。例如，若设置为 5，表示
*handler* 被触发 5 次后，将删除该监听器；若设置为 "all"，则会持续监听事件，对每个匹配的事件都触发
*handler*，直至引擎被删除。

**at** 一个长度为 6 的元组，用于指定触发 *handler* 的时间频率。其形式为 (seconds，minutes, hours,
days\_of\_the\_week，days\_of\_the\_month, month )
，其中各元素依次表示秒（必须指定）、分钟、小时、一周中的第几天、当月的第几天、月份。如果*times*="all"，则表示每月/日/周几/小时/分钟的第
seconds 秒触发 *handler*。例如：(0, 5, , , )，表示在每小时的 05 分触发 *handler*。如果
*times* 指定为具体数字，则 *handler* 只会被触发指定次数。

**wait** DURATION 类型，表示等待多长时间后触发 *handler*。如果 *times*="all"，则表示每隔多久触发
*handler*。例如：*wait* = 60s, *times* ="all"，每隔 60秒触发一次
*handler*。如果 *times* 指定为具体数字，则 *handler* 只会被触发指定次数。

**within** 仅在限定的时间内收到匹配的事件时才触发 *handler*。例如：*eventType*="tickets",
*within*=60s ，表示60秒内匹配到事件 tickets，则触发 *handler*，否则删除这个监听器。

**exceedTime** 仅在限定的时间内没有匹配的事件时才触发 *handler*。例如：*eventType*="tickets",
*exceedTime*=60s，表示若60秒内未匹配到事件 tickets，则触发 *handler*，否则删除这个监听器。

**name** 字符串标量，可选参数，表示监听器的名称，用于唯一标识该监听器。默认值根据 *condition* 得出：

* 若指定 *condition*，则名称为其表达式的字符串形式；
* 若 *condition* 为空且指定了 *eventType*，则名称为 *eventType*；
* 若 *condition* 和 *eventType* 均未指定，则默认名称为 "timer"；
* 若生成的名称与现有监听器重名，将自动在名称后追加编号以确保唯一性。

## 事件监听器触发方式

事件监听器可通过不同参数配置实现多种触发方式，包括：基于事件匹配触发、基于时间的定时触发，以及时间与事件条件的组合触发。

* **事件匹配**：监听单一事件或者所有事件，并且限定事件条件。相关参数：*handler*, *eventType*,
  *condition*。举例：
  + 监听价格大于10.0 的股票。下例中 *eventType* 为事件，*condition*
    为事件匹配条件，*handler*
    为监听到符合条件的事件之后的回调函数：

    ```
    addEventListener(handler=action, eventType=`Stock,
                                    condition=<Stock.price > 10.0>)
    ```
  + 监听所有的股票：

    ```
    addEventListener(handler=action, eventType=`Stock)
    ```
  + 监听任意事件

    ```
    addEventListener(handler=action, eventType="any")
    ```
* **基于事件时间触发**：此时不会进行事件匹配，因此不可指定 *eventType*。
  + 在固定时间触发，比如：在每天的 8:30
    触发（参数*at*）：

    ```
    addEventListener(handler=action, at=(0,30,8,,,))
    ```
  + 等待固定时间之后触发，比如从监听器被添加开始，每隔60秒触发一次（参数
    *wait*）：

    ```
    addEventListener(handler=action, wait=60s)
    ```
  + 等待固定时间之后触发，从监听器被添加开始，等待60秒触发一次（参数 *wait*,
    *times*）：

    ```
    addEventListener(handler=action, wait=60s,times=1)
    ```
* 同时限定时间和事件：*within*, *times*, *exceedTime*。
  + 在限定时间内匹配事件，比如在60秒内匹配到价格大于10.0的 Stock
    事件，则执行回调函数：

    ```
    addEventListener(handler=action, eventType=`Stock, condition=<Stock.price > 10.0>，within = 60s,times=1)
    ```
  + 在限定时间内未匹配事件，如在60秒内没有匹配到价格大于10.0的 Stock
    事件，则执行回调函数：

    ```
    addEventListener(handler=action, eventType=`Stock, condition=<Stock.price > 10.0>，exceedTime= 60s,times=1)
    ```

## 返回值

返回一个 EventListener 实例。

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

**相关函数**：getEventListener, terminate
