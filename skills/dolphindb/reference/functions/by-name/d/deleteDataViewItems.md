# deleteDataViewItems

## 语法

`deleteDataViewItems(engine, keys)`

## 详情

删除 DataView 引擎中指定键值的数据。若 *keys* 指定的键值列（key）不存在，则删除时会报错 。

该函数可在 CEP 引擎内部或外部调用。如果在 CEP 引擎内部调用此函数，系统将优先在 CEP 引擎中查找句柄为 *engine* 的 DataView
引擎；若未找到，则会在 CEP 引擎外部进行查找。如果在 CEP 引擎外部调用此函数，系统只会在 CEP 引擎外部进行查找。

## 参数

**engine** DataView 引擎句柄或引擎名。

**keys** 需要更新的键值， 如果是复合键值，则需要传入一个 tuple，其中每个元素表示组成键值的列，且顺序需与引擎中
*keyedColumns* 的指定顺序保持一致。

## 返回值

无。

## 例子

```
class Monitor1:CEPMonitor{
    def addNewData(order)
    def deleteData(s)
    def Monitor1(){
    }
    def onload(){
        addEventListener(addNewData,"Orders",,"all")
        addEventListener(deleteData,"Drop",,"all")
        try{
            share(streamTable(1:0,`eventTime`sym`val0`val1`val2,[TIMESTAMP,SYMBOL,INT,FLOAT,DOUBLE]),'test_DV')
            createDataViewEngine("test_DV",objByName('test_DV'),`sym,`eventTime,false)
        }catch(ex){}
    }
    def unload(){
        undef(`test_DV,SHARED)
    }
    def addNewData(order){
        getDataViewEngine('test_DV').append!(table([order.eventTime] as eventTime,[order.sym] as sym,[order.val1] as v1,[order.val2] as v2,[00i] as v3,[00i] as v4,[00i] as v5))
    }
    def deleteData(s){
        deleteDataViewItems('test_DV',s.sym)
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
class Drop{
    sym :: STRING
    eventTime :: TIMESTAMP
    def Drop(s){
        sym = s
        eventTime = now()
    }
}
dummy = table(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
try{dropStreamEngine("test_CEP")}catch(ex){}
engine=createCEPEngine("test_CEP",<Monitor1()>,dummy,[Orders,Drop],,'eventTime',,,"sym")
share streamTable(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as input
try{dropStreamEngine(`serInput)}catch(ex){}
serializer = streamEventSerializer(name=`serInput, eventSchema=Orders, outputTable=input, eventTimeField = "eventTime")
subscribeTable(,`input, `subopt1, 0,getStreamEngine('test_CEP'),true)
appendEvent(`serInput,Orders(`a1,1,1.0,2.0))
```

**相关函数**：createCEPEngine, createDataViewEngine, getDataViewEngine
