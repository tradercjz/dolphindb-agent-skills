# appendEvent

## 语法

`appendEvent(engine, events)`

## 详情

将事件实例写入 CEP 引擎的事件输入队列，无需序列化与反序列化。

## 参数

**engine** 引擎句柄。目前支持序列化引擎和 CEP 引擎。

**events** 可以是事件类型实例或者字典。如果指定为字典，系统会根据键值对构造出事件实例，因此字典的键必须包含事件类型（eventType ）
字段和事件定义中指定的事件字段（eventField）。

## 例子

定义事件 Orders，其包含字段 sym，val0，val1，val2：

```
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
```

定义一个简单的 monitor：

```
class mainMonitor:CEPMonitor {
    ordersTable :: ANY  // 定义成员变量 ordersTable，不限制数据类型和形式
    def mainMonitor(){
        ordersTable = array(ANY, 0)  // 这里确定 ordersTable 为一个元组
    }

    def updateOrders(event) {
        ordersTable.append!([event.sym, event.val0, event.val1, event.val2])
    }
    def onload(){
        addEventListener(updateOrders, 'Orders',,'all')
    }
}
```

创建 CEP 引擎如下：

```
dummy = table(array(TIMESTAMP, 0) as eventTime,array(STRING, 0) as eventType,  array(BLOB, 0) as blobs)
engine=createCEPEngine(name="test_CEP",monitors=<mainMonitor()>,dummyTable=dummy,eventSchema=Orders,timeColumn='eventTime')
```

向引擎中追加事件：

* *events*
  指定为一个事件类型实例：

  ```
  appendEvent(`test_CEP,Orders("a000", 3, 3.0, 30.0))
  ```
* *events*
  指定为一个字典：

  ```
  d=dict(['eventType',"sym", "val0","val1", "val2", "eventTime"],["Orders",'a000',5,float(3.6),double(29.3),2025.09.24T11:35:22.789])
  appendEvent(`test_CEP,d)
  ```

**相关函数**：addEventListener, createCEPEngine, emitEvent, routeEvent, sendEvent
