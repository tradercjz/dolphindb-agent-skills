# getCEPEngineStat

## 语法

`getCEPEngineStat(engine)`

## 详情

查看指定 CEP 引擎当前的运行状态，包括 CEP 引擎及其子引擎的状态。

## 参数

**engine** CEP 引擎的句柄。

## 返回值

一个字典，包含以下字段：

* EngineStat：一个字典，记录 CEP 引擎的状态，和
  `getStreamEngineStat().CEPEngine`
  返回的信息一致。

  ```
  eventsOnOutputQueue->0
  lastErrorTimestamp->
  numOfSubEngine->15
  lastErrorMessage->
  eventsEmitted->0
  eventsReceived->15
  name->test_CEP
  queueDepth->1024
  user->admin
  useSystemTime->true
  status->OK
  ```
* eventSchema：记录所有 CEP 引擎中进行反序列化的事件及其结构。

  | 列名 | 含义 |
  | --- | --- |
  | eventType | 事件类型 |
  | eventField | 事件类型中所声明的字段名。多个字段名之间以逗号（,）分隔 |
  | fieldType | eventField 中各字段对应的数据类型的名称，多个名称之间以逗号（,）分隔 |
  | fieldTypeId | eventField 中各字段对应的数据类型的 ID。为整型数组向量 |
  | fieldFormId | eventField 中各字段对应的数据形式的 ID。整型数组向量，0：标量; 1：向量; 2：数据对; 3：矩阵; 4：集合; 5：字典; 6：表  注意：目前只能指定标量和向量，其他形式需要以 ANY 类型指定，因此这里的返回值只有0和1两种 |
* subEngineStat：一个表，记录每个子引擎的详细状态。

  | 列名 | 含义 |
  | --- | --- |
  | subEngineName | 子引擎的名称 |
  | eventsOnInputQueue | 当前子引擎的事件队列中待处理的事件数量 |
  | monitorNumber | 当前 Monitor 数量 |
  | listeners | 事件监听器的数量 |
  | timers | 计时器数量，当 `addEventListener` 中指定了以下参数的任意一个都会创建1个计时器：*at*，*wait*，*within*，*exceedTime* |
  | eventsRouted | 插入到子引擎事件队列队首的事件数量 |
  | eventsSent | 插入到子引擎事件队列尾部的事件数量 |
  | eventsReceived | 从外部收到的事件数量 |
  | eventsConsumed | 匹配成功的事件数量 |
  | lastEventTime | 最近收到的事件时间 |
  | lastErrorMessage | 最近一条错误信息 |
  | lastErrorTimestamp | 最近一次错误信息的时间戳 |
* dataViewEngines：一个表，记录所有 dataView 引擎的状态。

  | 列名 | 含义 |
  | --- | --- |
  | name | dataView 引擎的名称 |
  | user | 创建 dataView 引擎的用户名 |
  | status | dataView 引擎状态 |
  | lastErrorMessage | 最后一条错误信息 |
  | lastErrorTimestamp | 最后一次错误信息的时间戳 |
  | keyColumns | 参数 keyColumns 指定的字段。多个字段之间以空格分隔 |
  | outputTableName | 输出表的名称 |
  | useSystemTime | 是否使用系统时间 |
  | throttle | 数据输出到 outputTable 的时间间隔。如果未指定 *throttle* 参数，则输出为空 |
  | numItems | dataView 引擎中的数据行数 |
  | memoryUsed | dataView 引擎所占用的内存量，单位为字节 |

## 例子

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
dummy = table(array(TIMESTAMP, 0) as eventTime,array(STRING, 0) as eventType,  array(BLOB, 0) as blobs)
engine=createCEPEngine(name="cep_engine",monitors=<mainMonitor()>,dummyTable=dummy,eventSchema=Orders,timeColumn='eventTime')

appendEvent(`cep_engine,Orders("a000", 3, 3.0, 30.0))

getCEPEngineStat(`cep_engine)
```

**相关函数**：createCEPEngine, dropStreamEngine
