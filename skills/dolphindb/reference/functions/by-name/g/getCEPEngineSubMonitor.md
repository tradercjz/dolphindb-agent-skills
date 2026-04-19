# getCEPEngineSubMonitor

## 语法

```
getCEPEngineSubMonitor(engine, subEngineName, monitorName)
```

## 详情

返回指定 monitor 在指定 CEP 引擎中生成的 subMonitor。如果指定的是一级（非 spawn）monitor，则该函数返回它生成的所有
subMonitor，包括所有嵌套级别。如果指定的是一个 subMonitor，则该函数仅返回它直接生成的监视器（即下一层）。

## 参数

**engine** CEP 引擎句柄或名称。

**subEngineName** 字符串标量，表示 CEP 子引擎名称。

**monitorName** 字符串标量，表示 monitor 名称。

## 返回值

一个字典，键为 monitor 名称， 值为 monitor 实例。

## 例子

```
class mainMonitor:CEPMonitor{
    ordersTable :: ANY
    def mainMonitor(){
        ordersTable = array(ANY, 0)
    }

    def updateOrders(event) {
        ordersTable.append!([event.trader, event.market, event.code, event.price, event.qty])
    }

    def onload(){
        addEventListener(updateOrders, 'Orders',,'all')
    }
}

class Orders{
    eventTime :: TIMESTAMP
    sym :: STRING
    val0 :: INT
    val1 :: FLOAT
    val2 :: DOUBLE
    def Orders(s,v0,v1,v2){
        sym = s
        val0 = v0
        val1 = v1
        val2 = v2
        eventTime = now()
    }
}

dummy = table(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
try{dropStreamEngine("cep1")}catch(ex){}
engine=createCEPEngine("cep1",<mainMonitor()>,dummy,Orders,,'eventTime',,,"sym")

appendEvent(`cep1,Orders("a000", 3, 3.0, 30.0))

// 查看 subEngine 的名称
getCEPEngineStat('cep1').subEngineStat["subEngineName"]

monitors = getCEPEngineSubMonitor('cep1', 'a000', 'mainMonitor')
```
