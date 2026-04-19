<!-- Auto-mirrored from upstream `documentation-main/stream/cep_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# CEP 引擎

## 创建 CEP 引擎

**语法**

`createCEPEngine(name, monitors, dummyTable, eventSchema,
[deserializeParallelism=1], [timeColumn], [eventQueueDepth=1024], [outputTable],
[dispatchKey], [dispatchBucket], [useSystemTime=true],
[eventTimeField="eventTime"])`

**参数**

**name** 字符串标量，表示 CEP 引擎的名称。可包含字母，数字和下划线，但必须以字母开头。

**monitors** 元代码或元代码元组，可包含一个或多个 Monitor 类的构造函数调用。如果指定了多个 Monitor 类的构造函数调用，在创建
subEngine 时，将按照指定的顺序构造这些对象。Monitor 的创建方法参见 简单的 Monitor 实例。

**dummyTable** 一个异构流表（未分区的内存表/流数据表），至少包含三列：

* 如果指定 *eventTimeField*，第一列为时间戳；
* 第二列为 STRING 类型，表示事件类型；
* 第三列为 BLOB 类型，用于存储事件序列化后的结果。

**eventSchema**
事件类型类的声明，用于指定为外部输入的事件类型，可以是一个标量或向量。例如：

```
class event1 {
  var1:: STRING
  var2:: INT
  def event1(){
    var1 = ""
    var2 = 0
  }
}

class event2 {
  var1:: DOUBLE
  var2:: INT
  def event2(){
    var1 = 0.0
    var2 = 0
  }
}

//指定为标量
eventSchema = event1
//指定为向量
eventSchema = [event1, event2]
```

**deserializeParallelism** 整型标量，用于指定反序化的线程数，默认值为1。

**timeColumn** 可选参数，字符串标量或向量，用于指定 *dummyTable* 中的时间列。指定后，通过事件流序列化器（Stream
Event Serializer）向 CEP 引擎插入事件时，该列将作为事件时间。

**eventQueueDepth** 整型标量，用于指定子引擎接收事件队列和输出队列的最大深度，默认值是1024。

**outputTable** 一个表对象，用于输出事件以供后续操作使用。如果调用了 `emitEvent` 接口，则需要指定该参数为
`StreamEventSerializer` 返回的表对象。

**dispatchKey** 字符串标量，用于指定事件中的属性，该属性中的每个唯一值被视为一个 key。若不指定
*dispatchKey*，则引擎将创建一个名为 *name* 的子引擎（与 CEP 引擎同名）。

**dispatchBucket** 整型标量，表示哈希分组的数量。如果指定该参数，引擎将对 *dispatchKey*指定的字段进行哈希分组*。*

CEP 引擎根据 *dispatchKey* 和 *dispatchBucket* 自动创建子引擎，并行处理数据。各个子引擎之间互相独立。若未指定
*dispatchKey*，则 CEP 引擎只有一个处理线程，即只创建一个子引擎。

**useSystemTime** 布尔值，表示是否使用数据注入引擎时的系统时间进行计算。

* 当 *useSystemTime* = true 时（缺省值）时，CEP
  引擎中的计算都基于数据注入引擎的时刻（以毫秒精度表示的本地系统时间）进行，与数据中的时间列无关。
* 当 *useSystemTime* = false 时，CEP 引擎中的计算都基于数据中的 *timeColumn* 列进行。

**eventTimeField** 可选参数，字符串标量或向量，用于指定事件中的时间字段，仅在 *useSystemTime* = false
有效。如果所有事件的时间字段名都相同，则 *eventTimeField* 是一个标量；否则，*eventTimeField* 是一个向量，其长度和
*eventSchema* 的长度相同，每个元素分别代表每个事件的时间字段。通过 `appendEvent` 直接向
CEP 引擎插入事件时，必须通过该参数指定事件的时间。

## 追加事件

向 CEP 引擎注入事件有两种方法：

* 通过 `appendEvent` 接口，直接将事件实例写入 CEP 引擎的事件输入队列。
* 将异构流表中的数据写入 CEP 引擎：在实时场景中，通过 `subscribeTable`
  函数订阅异构流表，可以将不同类型的数据输入引擎。异构流表数据来自 `replay` 事件回放或者通过 API
  写入。

这两种方式的主要区别在于，`appendEvent`
写入事件不需要序列化和反序列化；而通过异构流表写入事件则需要进行序列化和反序列化操作，优点是可以将多个不同的事件类型写入到一个异构流数据表。

### appendEvent

**语法**

```
appendEvent(engine, events)
```

**参数**

**engine** 引擎句柄。目前支持序列化引擎和 CEP 引擎。

**events** 事件类型，可以是事件类型实例或者字典。如果指定为字典，系统会根据键值对构造出事件实例，因此字典的键必须包含 *eventType*和 *eventSchema* 中指定的 eventField。

**示例**1

假如已定义的事件类型 Orders，其包含字段 sym，val0，val1，val2：

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

创建CEP 引擎如下：

```
engine=createCEPEngine(name="test_CEP",monitors=<Monitor1()>,dummyTable=dummy,eventSchema=Orders,timeColumn='eventTime')
```

下面说明如何通过事件实例或字典向 CEP 引擎中追加事件。

* *events* 指定为一个事件类型实例：

  ```
  appendEvent(`test_CEP,Orders("b"+lpad(string(i),3,"0"),i,i*1,i*10))
  ```
* *events* 指定为一个字典：

  ```
  d=dict(['eventType',"sym", "val0","val1", "val2"],["Orders",'a000',5,float(3.6),double(5.3)])
  appendEvent(`test_CEP,d)
  ```

**示例2**

使用 `appendEvent` 直接向 CEP 引擎插入事件时，通过 *eventTimeField*
指定事件的时间。

```
class Test{
    key :: string
    et :: TIMESTAMP
    def Test(c){
        key = c
        et = now()
    }
}

class MarketData{
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    et :: TIMESTAMP
    def MarketData(m,c,p,q){
        market = m
        code = c
        price = p
        qty = q
        et = now()
  }
}

class MainMonitor:CEPMonitor{
    streamMinuteBar_1min :: ANY //行情 K 线计算结果
    tsAggrOHLC :: ANY //时间序列聚合引擎
    def MainMonitor(){
        colNames = ["time","symbol","open","max","min","close","volume","amount","ret","vwap"]
        colTypes = [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT, DOUBLE, DOUBLE, DOUBLE]
        streamMinuteBar_1min = table(10000:0,colNames, colTypes)
    }

    def updateMarketData(event)
    // 监听行情数据并创建时间序列聚合引擎，计算一分钟行情 K 线。
    def onload(){
        addEventListener(updateMarketData,'MarketData',,'all')
        colNames=["symbol","time","price","type","volume"]
        colTypes=[SYMBOL, TIMESTAMP, DOUBLE, STRING, INT]
        dummy = table(10000:0,colNames,colTypes)
        colNames = ["time","symbol","open","max","min","close","volume","amount","ret","vwap"]
        colTypes = [TIMESTAMP, SYMBOL, DOUBLE, DOUBLE, DOUBLE, DOUBLE, INT, DOUBLE, DOUBLE, DOUBLE]
        output = table(10000:0,colNames, colTypes)
        tsAggrOHLC = createTimeSeriesEngine(name="tsAggrOHLC", windowSize=60000, step=60000, metrics=<[first(price) as open ,max(price) as max,min(price) as min ,last(price) as close ,sum(volume) as volume ,wsum(volume, price) as amount ,(last(price)-first(price)/first(price)) as ret, (wsum(volume, price)/sum(volume)) as vwap]>, dummyTable=dummy, outputTable=streamMinuteBar_1min, timeColumn='time', useSystemTime=false, keyColumn="symbol", fill=`none)
    }

    def updateMarketData(event){
        tsAggrOHLC.append!(table(event.code as symbol, event.et as time, event.price as price, event.market as type, event.qty as volume))
    }
}
dummy = table(array(TIMESTAMP, 0) as eventTime,array(STRING, 0) as eventType,  array(BLOB, 0) as blobs)
engine = createCEPEngine(name='cep1', monitors=<MainMonitor()>, dummyTable=dummy, eventSchema=[MarketData,Test],dispatchKey='key',eventTimeField='et',useSystemTime=false,timeColumn="eventTime")

data = Test("hk")
// 直接向 engine 追加事件
appendEvent(engine, data)

data = MarketData("hk","e", 1.0, 1)

// 直接向 engine 追加事件
appendEvent(engine, data)
```

## 路由事件

在 Monitor
中，事件通常有四种流向：插入事件输入队列的队尾、插入输入处理队列的队首、继续进行模式匹配、以及插入事件输出队列等待输出。其中，继续进行模式匹配是在监听器的
*handler*
中定义的另一个监听器。若要添加监听器，请参考上一节内容。本节将主要介绍将事件插入事件输入队列队尾、插入事件输入队列的队首以及插入输出队列的方法。

### 插入事件输入队列队尾

将事件插入到当前子引擎的事件处理队列的尾部。

**语法**

`sendEvent(event)`

**参数**

**event** 事件类型实例。

### 插入事件输入队列队首

将事件插入到当前子引擎的事件处理队列的队首。

**语法**

`routeEvent(event)`

**参数**

**event** 事件类型实例。

### 插入输出队列队尾

将事件插入到 CEP 引擎的事件输出队列的队尾。引擎会异步地将事件发送到输出队列。

**语法**

`emitEvent(event, [eventTimeField])`

**参数**

**event** 事件类型实例。

**eventTimeField** 字符串标量，表示事件中的时间字段名。若要指定此参数，*event* 必须包含时间字段。当
*useSystemTime*=true 时，输出事件中的时间为系统时间；否则，输出最新事件时间。

## 停止子引擎

**语法**

`stopSubEngine()`

**详情**

关闭执行此函数的 Monitor 实例所在的子引擎。在关闭子引擎前，将调用其内部所有 Monitor 实例中已声明的 `onunload`
方法。如果存在通过 spawn 产生的 Monitor 实例，将首先调用这些由 spawn 产生的 Monitor 实例中已声明的
`onDestroy` 方法。
