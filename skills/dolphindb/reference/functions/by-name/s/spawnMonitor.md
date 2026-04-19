# spawnMonitor

## 语法

```
spawnMonitor(name, handler, arguments...)
```

## 详情

在 Monitor 中，通过 `spawnMonitor` 接口深拷贝构造一个
subMonitor。`spawnMonitor` 的功能如下:

1. 构造一个深拷贝的 Monitor 新实例。
2. 深拷贝原 Monitor 中所有支持深拷贝的属性和方法。
3. 在生成的 Monitor 实例中可以通过参数，指定需要执行的操作。

## 参数

**name** 生成 monitor 实例的名称。不可与已存在的实例重名。

**handler** 生成的 Monitor 实例的方法。在生成新的实例后，将调用这个方法。

**arguments**
*handler* 的参数。

## 返回值

一个 Monitor 实例

## 例子

```
class NewStock {
    code :: STRING
    price :: DOUBLE
    def NewStock(c, p){
        code = c
        price = p
    }
}
class SimpleShareSearch : CEPMonitor {
    numberTicks :: INT
    price :: DOUBLE
    stockName :: STRING
    def SimpleShareSearch(){
        stockName = ""
		numberTicks = 0
		price = 0.0
	}
    def matchTicks(newStock)
    def spawnTicks(newStock){
        numberTicks = numberTicks+1
        spawnMonitor("MonitorOf"+newStock.code, matchTicks, newStock)
    }
    // 监听所有 NewStock 事件。当发现 NewStock 事件时,
    // 调用从当前监视器深拷贝构造一个监视器实例，并执行 matchTicks() 方法。
    // 这个操作深拷贝了当前监视器的状态。
    def onload() {
        addEventListener(handler=spawnTicks, eventType="NewStock", times="all")
    }
    def processTick(ticks)
    def matchTicks(newStock) {
        stockName=newStock.code
        price = newStock.price
        addEventListener(handler=processTick, eventType="StockTick", condition=<StockTick.code==stockName>,times="all")
    }
   def processTick(ticks) {
		str = "StockTick event received" +
			" name = " + ticks.code +
			" Price = " + ticks.price.string()
		writeLog(str)
   }
}
```
