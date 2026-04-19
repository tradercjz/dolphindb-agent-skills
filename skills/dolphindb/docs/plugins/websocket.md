<!-- Auto-mirrored from upstream `documentation-main/plugins/websocket.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# WebSocket

DolphinDB 的 WebSocket 插件提供了强大的 WebSocket 客户端功能。作为一个 WebSocket 客户端，该插件能够连接到 WebSocket 服务端，并实现双向通信。它支持从 WebSocket 服务端读取数据，例如实时的行情数据、交易数据等。同时，插件也支持向 WebSocket 服务端发送数据，比如下单指令、订阅请求等。除此之外，该插件还能够提取 WebSocket 通信过程中的响应头文件，帮助用户更好地了解通信状态和获取相关信息。该插件目前仅支持 wss 协议。

## 安装插件

### 版本要求

DolphinDB Server：2.00.12 及更高版本，支持 Linux x86-64。

### 安装步骤

1. 在DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("WebSocket")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("WebSocket")
   ```

## 接口说明

### createSubJob

**语法**

```
WebSocket::createSubJob(url, onOpen, onMessage, onError, onClose, tag, [config])
```

**详情**

创建一个 WebSocket 订阅，返回一个 WebSocket 对象。如果订阅 tag 已存在且正在运行，则抛出错误；否则覆盖之前的订阅信息。

**参数**

**url** STRING 类型标量，表示 WebSocket 的地址。

**onOpen** 一个函数，其第一个参数为 WebSocket 对象。通过该参数指定建立连接时将调用的 `onOpen` 函数。

函数签名如下:

```
def onOpen(ws){}
```

**onMessage** 一个函数，其第一个参数为 WebSocket 对象；第二个参数是一个表，表示订阅的数据，其仅包含一个列，类型为 BLOB，列名为 msg。通过该参数指定 WebSocket 数据接入时将调用 `onMessage` 函数。

函数签名如下:

```
def onMessage(ws, data){}
```

**onError** 一个函数，其第一个参数为 WebSocket 对象；第二个参数是错误信息，为 BLOB 类型标量。通过该参数指定发生错误时将调用的 `onError` 方法。

函数签名如下:

```
def onError(ws, error){}
```

**onClose** 一个函数，其第一个参数为 WebSocket 对象，第二个参数是错误码，为 INT 类型标量；第三个参数是关闭信息，为 BLOB 类型标量。通过该参数指定关闭订阅时将调用的 `onClose` 方法。

函数签名如下:

```
def onClose(ws, statusCode, msg){}
```

**tag** STRING 类型标量，表示 WebSocket 的订阅标识。

**config** 字典，用于指定一些额外的配置项。其键为 STRING 类型标量、值为 ANY。目前支持的键为：

* "proxy"：设置代理地址，键值为 STRING 类型标量，例如 “http://proxy.example.com:8080/"。
* "reconnectCount"：用于设置非用户主动取消订阅的情况下，连接断开后重新连接的尝试次数，键值为 INT 类型标量。默认是 -1，表示会一直尝试重连直到成功连接。

```
share table(1:0, ["data"], [BLOB]) as table1
def onOpen(ws){
    WebSocket::send(ws, blob('{"method": "SUBSCRIBE","params": ["btcusdt@aggTrade","btcusdt@depth"], "id": 1}'))
}
def onMessage(ws, data){
  	table1.append!(table(data.msg as col1))
}

def onError(ws, error){
  writeLog("failed to receive data: " + error)
}
def onClose(ws, statusCode, msg){
  writeLog("connection is close, statusCode: " + statusCode + ", " + string(msg))
}
url = "ws://localhost:8080"
config = dict(STRING, ANY)
config[`proxy] = "http://proxy.example.com:8080/"
ws = WebSocket::createSubJob(url, onOpen, onMessage, onError, onClose, "sub1", config)
```

### send(ws, data)

**语法**

```
WebSocket::send(ws, data)
```

**详情**

发送 WebSocket 消息，可以在 `WebSocket::createSubJob` 的参数 *onOpen*、*onMessage* 中调用，也可以使用`WebSocket::createSubJob` 返回的 WebSocket 对象发送消息。返回一个布尔值，表示是否发送成功。

**参数**

**ws** WebSocket 对象。

**data** BLOB 类型标量，表示需要发送的数据。

### getSubJobStat()

**语法**

```
WebSocket::getSubJobStat()
```

**详情**

获取所有的 WebSocket 后台任务信息，包含已经通过 `WebSocket::cancelSubJob` 取消的任务。注意，如果不同任务的 *tag* 值相同，前一个任务的信息将会被后一个任务的信息覆盖掉。返回一个表，包含如下列：

* tag：WebSocket 任务标识。
* startTime：任务创建时间。
* endTime：任务取消时间。任务可以通过 WebSocket::cancelSubJob 来取消，初始值是空值，表示任务未被取消，或者是重连成功。
* firstMsgTime：第一条数据的接收时间。
* lastMsgTime：上一条消息的接收时间。
* processedMsgCount：成功接收的消息行数。初始值是0。
* failedNetMsgCount：网络错误的消息行数。初始值是0。
* failedMsgCount：处理失败的消息行数。初始值是0。
* netErrCount：上一次处理失败的错误信息。
* lastOnFuncErrMsg：上一次回调函数出现的错误。
* lastFailedTimestamp：上一次处理失败的时间。

### cancelSubJob

**语法**

```
WebSocket::cancelSubJob(tag)
```

**详情**

取消一个 WebSocket 的后台任务，返回一个布尔值。

**参数**

**tag** STRING 类型标量，表示 WebSocket 的任务标识。可以通过 `WebSocket::getSubJobStat()` 获取 *tag*。

**使用示例**

```
tag = (exec tag from WebSocket::getSubJobStat())[0]
WebSocket::cancelSubJob(tag)
```

### getResponseHeader

**语法**

```
WebSocket::getResponseHeader(ws, key)
```

**详情**

获取 WebSocket 的消息头。返回一个字符串标量。该消息头可以在 `WebSocket::createSubJob` 的参数 *onOpen*、*onMessage* 中调用。

**参数**

**ws** WebSocket 对象。

**key** STRING 类型标量，表示需要获取的 Header 的对应的 key。

```
data = WebSocket::getResponseHeader(ws, "server")
```
