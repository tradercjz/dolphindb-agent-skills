# destroyMonitor

## 语法

`destroyMonitor()`

## 详情

终止 monitor 实例。若该实例声明了 `onDestroy` 方法，则会在终止前自动执行该方法。终止后，monitor
内部的事件监听器将不再生效。

## 参数

无

## 返回值

无。

## 例子

```
class Monitor1:CEPMonitor{
    def addNewData(order)
    //def updateData(change)
    def Monitor1(){
    }
    def myDestroyMonitor(Orders){
        destroyMonitor()
    }
    def onload(){
        addEventListener(addNewData,"Orders",,"all")
        // 当收到事件 Orders 的 v1 值为5.0时，单次触发该 listenser，调用 myDestroyMonitor 方法销毁当前的监控器实例
        addEventListener(handler=myDestroyMonitor, eventType="Orders", condition=<Orders.v1=5.0>, times=1)
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
try{dropStreamEngine("test_CEP")}catch(ex){}
engine=createCEPEngine("test_CEP",<Monitor1()>,dummy,Orders,,'eventTime',,,"sym")
share streamTable(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as input
try{dropStreamEngine(`serInput)}catch(ex){}
serializer = streamEventSerializer(name=`serInput, eventSchema=Orders, outputTable=input, eventTimeField = "eventTime")
subscribeTable(,`input, `subopt1, 0,getStreamEngine('test_CEP'),true)
```
