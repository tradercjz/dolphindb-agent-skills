# dropDataViewEngine

首发版本：3.00.4

## 语法

`dropDataViewEngine(name)`

## 详情

删除当前 CEP 引擎中指定的 DataView 引擎。

## 参数

**name** 字符串，表示 DataView 引擎的名称。

## 返回值

无。

## 例子

```
class MainMonitor:CEPMonitor {
    def MainMonitor(){
    }
    // 删除引擎时自动调用，删除共享流表
    def onunload(){
      undef('orderDV', SHARED)
      dropDataViewEngine('orderDV')
    }
	def checkOrders(newOrder)
    // 创建 DataViewEngine, 指定主键为 code 列，统计每个股票的最新的委托信息
    def onload(){
        addEventListener(checkOrders,'Orders',,'all')
        orderDV = streamTable(array(STRING, 0) as market, array(STRING, 0) as code, array(DOUBLE, 0) as price, array(INT, 0) as qty, array(TIMESTAMP, 0) as updateTime)
        share(orderDV,'orderDV')
        createDataViewEngine('orderDV', objByName('orderDV'), `code, `updateTime)
    }
    // 更新每个股票的最新的委托信息
    def checkOrders(newOrder){
		getDataViewEngine('orderDV').append!(table(newOrder.market as market, newOrder.code as code, newOrder.price as price, newOrder.qty as qty))
    }
}
```

**相关函数**：createCEPEngine, createDataViewEngine, getDataViewEngine
