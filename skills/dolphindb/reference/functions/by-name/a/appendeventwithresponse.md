# appendEventWithResponse

首发版本：3.00.5

## 语法

`appendEventWithResponse(engine, event, responseType, [timeout=5000],
[condition], [returnType="instance"])`

## 详情

CEP 引擎的同步事件处理函数，用于发送事件并阻塞等待特定响应事件返回。

与 appendEvent 的异步模式不同，该函数采用同步等待响应模式：向 CEP 引擎发送事件后，当前线程会阻塞等待，直到收到匹配的响应事件或超时。

## 参数

**engine** CEP 引擎句柄或引擎名。

**event** 事件类型实例或者字典，指定要发送的事件。如果指定为字典，系统会根据键值对构造出事件实例，因此字典的键必须包含
"eventType"（事件类型）和事件类型中声明的字段名（eventField）。

**responseType** 字符串标量，指定期望接收的响应事件类型。

**timeout** 可选，整型标量，单位为毫秒，默认为 5000 毫秒。等待响应的超时时间。

**condition** 可选，元代码类型。指定过滤表达式响应事件进行筛选，如 `<event.id=1>`。若指定了
*condition* 参数，系统将在类型匹配的基础上增加条件筛选，只有同时满足类型要求和条件表达式的响应事件才会被接受。

**returnType** 可选，字符串标量，指定返回的响应事件类型的数据形式。可选值为：

* "dict"：以字典形式返回响应事件。
* "instance"：默认值，返回响应事件实例。

## 返回值

返回值形式由 *returnType* 参数控制：

* *returnType*="dict" 时，返回一个字典。
* *returnType*="instance" 时，返回一个事件实例。

## 例子

该示例展示了如何实现策略启动请求的处理与同步响应机制。

外部调用方发送 startRequest 事件向 CEP 引擎发起策略启动请求，CEP Monitor 接收并处理该事件，在完成相应的启动逻辑后，通过
StartResponse 事件返回启动结果。

调用方通过 `appendEventWithResponse` 函数同步等待指定策略实例（以 instanceId
匹配）的启动响应，从而实现基于事件的请求-响应交互模式。

```
try {
    dropStreamEngine(`cep)
} catch(ex) { print(ex) }

try {
    dropStreamEngine(`streamEventSerializer)
} catch(ex) { print(ex) }

class StartRequest{
    instanceId :: STRING
    strategyParams :: INT
    def StartRequest(instanceId_, strategyParams_){
        instanceId = instanceId_
        strategyParams = strategyParams_
    }
}

class StartResponse{
    instanceId :: STRING
    status :: STRING
    def StartResponse(instanceId_, status_){
        instanceId = instanceId_
        status = status_
    }
}

class Stratege:CEPMonitor {
	//构造函数
	def Stratege(){
	}
    def startStratege(StartRequestEvent){
        // 启动策略实例
    }
	def processStartRequest(StartRequestEvent){
        startStratege(StartRequestEvent)
        // 发送策略启动成功响应
        emitEvent(StartResponse(StartRequestEvent.instanceId, "success"))
    }
	def onload() {
        // 注册事件监听，监听策略启动请求
		addEventListener(handler=processStartRequest, eventType="StartRequest", times="all")
	}
}

dummy = table(array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
share streamTable(array(STRING, 0) as eventType, array(BLOB, 0) as blobs) as outputTable
serializer = streamEventSerializer(name=`streamEventSerializer, eventSchema=[StartResponse], outputTable=outputTable)
// 创建 CEP 引擎
engine = createCEPEngine(name='cep1', monitors=<Stratege()>, dummyTable=dummy, eventSchema=[StartRequest], outputTable=serializer)

// 发送策略启动请求，同步等待策略实例 instance_001 启动成功的响应
request = StartRequest(`instance_001, 100)
response = appendEventWithResponse(engine=getStreamEngine(`cep1), event=request, responseType="StartResponse", timeout=3000, condition=<StartResponse.instanceId==request.instanceId>)
```

**相关函数**：appendEvent
