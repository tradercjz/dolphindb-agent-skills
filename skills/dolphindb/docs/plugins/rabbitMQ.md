<!-- Auto-mirrored from upstream `documentation-main/plugins/rabbitMQ.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# RabbitMQ

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本。支持 Linux x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 listRemotePlugins 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 installPlugin 命令完成插件安装。

   ```
   installPlugin("rabbitmq")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("rabbitmq")
   ```

## 接口说明

* connection, connectionAMQP 在连接建立失败时会抛出异常
* 如果某个传入channel的函数调用失败，channel就会失效。所以推荐在调用不同函数时创建新的channel。但是不推荐每次publish时创建新的channel。
* channel的成员函数除publish以及consume外，其他函数都是同步函数，如果执行失败，会抛出异常，这可能是因为参数不正确(IllegalArgumentException)，可能是因为函数本身运行失败(RuntimeException)，也可能是因为connection或channel失效(RuntimeException)。如果是因为后两个原因，此时需要重新创建channel。

  + 在close(channel)之后调用channel的成员函数会抛出异常，提示“Please create channel first”
  + 在close(connection)之后调用channel的成员函数会抛出异常，提示“failed to ..., refer to log for more information”，并且日志提示“Frame could not be sent”
  + 在connection断开导致channel失效或channel的成员函数运行失败使channel失效之后再调用channel的成员函数会抛出异常，提示“failed to ..., refer to log for more information”，并且日志提示“Frame could not be sent”
  + 创建channel的过程中如果因为connection已经被关闭或者连接数达到上限，会抛出异常
  + 综上：channel失效之后需要创建新的channel，如果创建channel的过程中如果抛出异常，此时需要重新创建connection。
* channel的成员函数publish如果失败会抛出异常。可以通过捕获异常来重新建立connection和channel并重新发送。
* channel的成员函数consume本身是同步的，可以知道订阅是否成功。但是consume在后续调用处理消息的回调函数中可能会因为connection或channel失效而失败，此时没办法通知用户发生了错误。
* 一个channel上不能进行并发操作（也有可能是一个connection上）。如果需要多线程调用，应该创建每个线程的channel（也有可能是connection）。

### connection

**语法**

```
rabbitmq::connection(host, [port=5672], [username='guest'], [password='guest'], [vhost="/"], [isTls=false])
```

**详情**

使用给定信息连接 RabbitMQ，返回连接对象。

**参数**

**host** 主机，STRING 类型标量。

**port**（可选）端口号，INT 类型标量，默认为 5672。

**username** （可选）用户名，STRING 类型标量，默认为 'guest'。

**password**（可选）密码，STRING 类型标量，默认为 'guest'。

**vhost**（可选）虚拟主机，STRING 类型标量，默认为"/"。

**isTls**（可选）是否开启 TLS 加密，布尔类型标量，默认为 false。

**例子**

```
conn = rabbitmq::connection('localhost', 5672, 'guest', 'guest', "/")
```

### connectionAMQP

**语法**

```
rabbitmq::connectionAMQP(amqpUri)
```

**详情**

使用 AMQP 地址连接 RabbitMQ，返回连接对象。

**参数**

**amqpUri** AMQP 协议地址，STRING 类型向量。

**例子**

```
conn = rabbitmq::connectionAMQP(['amqp://guest:guest@192.168.0.1:5672', 'amqp://guest:guest@192.168.0.2:5672', 'amqp://guest:guest@192.168.0.3:5672'])
```

### channel

**语法**

```
rabbitmq::channel(conn)
```

**详情**

使用指定连接创建 Channel，返回 Channel 对象

**参数**

**conn** RabbitMQ 连接。

**例子**

```
ch = rabbitmq::channel(conn)
```

### declareExchange

**语法**

```
rabbitmq::declareExchange(channel, name, [type='fanout'], [flags])
```

**详情**

声明 Exchange。

**参数**

**channel** Channel 对象。

**name** 交换器名称，STRING 类型标量。

**type**（可选）STRING 类型标量，支持的取值：'fanout'，'direct'，'topic'，'headers'，'consistent\_hash'，默认为 'fanout'。

**flags**（可选）STRING 类型向量，支持的取值：'durable'，'autodelete'，'passive'，'internal'。

**例子**

```
rabbitmq::declareExchange(ch, 'test-exchange', 'fanout', ['autodelete'])
```

### bindExchange

**语法**

```
rabbitmq::bindExchange(channel, source, target, routingKey)
```

**详情**

绑定 Exchange。

**参数**

**channel** Channel 对象。

**source** source Exchange 名称

**target** target Exchange 名称

**routingKey** 路由规则名称

**例子**

```
rabbitmq::bindExchange(ch, 'test-exchange1', 'test-exchange2', 'rule1')
```

### unbindExchange

**语法**

```
rabbitmq::bindExchange(channel, source, target, routingKey)
```

**详情**

解绑 Exchange。

**参数**

同 `bindExchange`。

**例子**

```
rabbitmq::unbindExchange(ch, 'test-exchange1', 'test-exchange2', 'rule1')
```

### removeExchange

**语法**

```
rabbitmq::removeExchange(channel, name, [flags])
```

**详情**

移除 Exchange。

**参数**

**channel** Channel 对象。

**name** Exchange 名称。

**flags**（可选）STRING 类型向量。支持的取值：'ifunused'。

**例子**

```
rabbitmq::removeExchange(ch, 'test-exchange')
```

### declareQueue

**语法**

```
rabbitmq::declareQueue(channel, name, [flags], [options])
```

**详情**

声明 Queue。

**参数**

**channel** Channel 对象。

**name** 声明的队列名，STRING 类型标量。

**flags**（可选）队列标志，STRING 类型向量。支持的取值：'durable'，'autodelete'，'passive'，'exclusive'。

**options**（可选）队列参数，字典。键为字符串，值支持的类型：STRING，CHAR，LONG，INT，BOOL。

**例子**

```
options = dict(STRING, ANY)
options['x-max-length'] = 10000
options['x-overflow'] = 'drop-head'
options['x-queue-type'] = 'quorum'
rabbitmq::declareQueue(ch, 'test', ['exclusive'], options)
```

### bindQueue

**语法**

```
rabbitmq::bindQueue(channel, exchange, queue, routingKey)
```

**详情**

绑定 Queue。

**参数**

**channel** Channel 对象。

**exchange** source Exchange 名称。

**queue** target Queue 名称。

**routingKey** 路由规则名称。

**例子**

```
rabbitmq::bindQueue(ch, 'test-exchange1', 'test-queue1', 'rule1')
```

### unbindQueue

**语法**

```
rabbitmq::unbindQueue(channel, exchange, queue, routingKey)
```

**详情**

解绑 Queue。

**参数**

同 bindQueue。

**例子**

```
rabbitmq::unbindQueue(ch, 'test-exchange1', 'test-queue', 'rule1')
```

### removeQueue

**语法**

```
rabbitmq::removeQueue(channel, name, [flags])
```

**详情**

移除 Queue。

**参数**

**channel** Channel 对象。

**name** Queue 名称，字符串标量。

**flags**（可选）用于控制队列的删除行为，字符串向量。支持如下值："ifunused" 和 "ifempty"。

**例子**

```
rabbitmq::removeQueue(ch, 'test-queue1')
```

### publish

**语法**

```
rabbitmq::publish(channel, exchange, routingKey, message, format＝'default', [flags])
```

**详情**

以指定方式发布 DolphinDB 对象。

**参数**

**channel** Channel 对象。

**exchange** STRING 类型标量

**routingKey** STRING 类型标量。

**message** 要发送的信息。

**format** 指定信息格式，STRING 类型标量或函数（由 `createJSONFormatter`或 `createCSVFormatter` 创建）。

| format | 取值 |
| --- | --- |
| default | DolphinDB 默认格式 |
| bytestream | 字节流 |
| protobuf | protocol buffer |

**flags**（可选）STRING 类型向量。支持的取值：'mandatory'，'immediate'。

**例子**

```
rabbitmq::publish(ch, 'test-exchange1', 'rule1', 'Hello World1', 'bytestream')
```

### consume

**语法**

```
rabbitmq::consume(channel, queue, handler, parser, tag, [flags], [onCancel])
```

**详情**

订阅队列。

**参数**

**channel** Channel 对象。

**queue** 订阅的队列名称，STRING 类型标量。

**handler** 一元函数，用于处理订阅的数据。请注意，传入的一元函数中不能存在对 DFS 表的操作，例如：读取或写入 DFS 表，获取 DFS 表的 schema 等。

**parser** 订阅数据的格式，STRING 类型标量，取值范围同`publish`，或者是解析函数（由 `createJSONParser` 或`createCSVParser` 创建）。

**tag** 消费者标识，STRING 类型标量。

**flags**（可选）STRING 类型向量。支持的取值：'nolocal'，'noack'，'exclusive'。

**onCancel** （可选）一元函数。其输入参数的类型为字符串标量，表示订阅时传入的 tag。在订阅因 RabbitMQ 服务器端问题（例如队列被删除或存储队列的节点被终止）而被取消时，会调用该函数。

**例子**

```
def handle(msg){
}
rabbitmq::consume(ch, 'test-queue1', handler, 'bytestream', 'consumer1')
```

### cancelConsume

**语法**

```
rabbitmq::cancelConsume(channel, tag)
```

**详情**

取消 consume。

**参数**

**channel** Channel 对象。

**tag** 消费者标识，STRING 类型标量。

**例子**

```
rabbitmq::cancelConsume(ch, 'consumer1')
```

### 后台订阅相关接口

### createSubJob

**语法**

```
rabbitmq::createSubJob(queue, handler, parser, tag, hosts, ports, [username='guest'], [password='guest'], [vhost="/"], [flags], [onCancel], [isTls=false])
```

**详情**

后台订阅。

**参数**

**queue** 订阅的队列名称，STRING 类型标量。

**handler** 处理订阅数据的 handle，能接受一个参数的函数。

**parser** 解析数据的字符串或函数（同 `consume`）。

**tag** 消费者标识，STRING 类型标量。

**hosts** 主机，STRING 类型向量，为集群中每一台主机的 IP 地址。

**ports** 端口号，INT 类型向量，为集群中每一台主机的端口号，注意，端口号的顺序要与 *hosts* 中的 IP 地址匹配。

**username**（可选）用户名，STRING 类型标量，默认为 'guest'。

**password**（可选）密码，STRING 类型标量，默认为 'guest'。

**vhost**（可选）虚拟主机，STRING 类型标量，默认为"/"。

**flags**（可选）STRING 类型向量。支持的取值：'nolocal'，'noack'，'exclusive'。

**onCancel** （可选）一元函数。其输入参数的类型为字符串标量，表示订阅时传入的 tag。在订阅因 RabbitMQ 服务器端问题（例如队列被删除或存储队列的节点被终止）而被取消时，会调用该函数。

**isTls**（可选）是否开启 TLS 加密，布尔类型标量，默认为 false。

**例子**

```
def handle(msg){
}
rabbitmq::createSubJob('test-queue2', handler, 'bytestream', 'consumer1',['localhost'], [5672], 'guest', 'guest')
```

### getSubJobStat

**语法**

```
rabbitmq::getSubJobStat()
```

**详情**

获取所有后台订阅信息（订阅 id，queue，tag，订阅时间戳）

**参数**

无

**例子**

```
tb = rabbitmq::getSubJobStat()
print(tb)
```

### cancelSubJob

**语法**

```
rabbitmq::cancelSubJob(id)
```

**详情**

取消某一个后台订阅。

### 打/解包功能

### createCSVFormatter

**语法**

```
rabbitmq::createCSVFormatter([format], [delimiter], [rowDelimiter])
```

**详情**

创建一个 CSV 格式的 Formatter 函数。

**参数**

**format** STRING类型向量。

**delimiter** 列之间的分隔符，默认是','。

**rowDelimiter** 是行之间的分隔符，默认是';'。

**例子**

```
MyFormat = take("", 3)
MyFormat[1] = "0.000"
formatter = rabbitmq::createCSVFormatter(MyFormat,',',';')
```

### createCSVParser

**语法**

```
rabbitmq::createCSVParser(schema, [delimiter], [rowDelimiter])
```

**详情**

创建一个 CSV 格式的 Parser 函数。

**参数**

**schema** 包含各列数据类型的向量。

**delimiter** 列之间的分隔符，默认是','。

**rowDelimiter** 行之间的分隔符，默认是';'。

**例子**

```
parser = rabbitmq::createCSVParser([INT,STRING,INT], ',',';')
```

### createProtoBuformatter

**语法**

```
rabbitmq::createProtoBuformatter()
```

**详情**

创建一个 protobuf 格式的 Formatter 函数。

**参数**

无

**例子**

```
formatter = rabbitmq::createProtoBuformatter()
```

### createProtoBufParser

```
rabbitmq::createProtoBufParser()
```

**详情**

创建一个 protobuf 格式的 Parser 函数。

**参数**

无

**例子**

```
parser = rabbitmq::createProtoBufParser()
```

### createJSONFormatter

```
rabbitmq::createJSONFormatter()
```

**详情**

创建一个 JSON 格式的 Formatter 函数。

**参数**

无

**例子**

```
formatter = rabbitmq::createJSONFormatter()
```

### createJSONParser

```
rabbitmq::createJSONParser(schema, colNames)
```

**详情**

创建一个 JSON 格式的 Parser 函数。

**参数**

**schema** 向量，表示各列的数据类型。

**colNames** 向量，表示列名。

**例子**

```
parser = rabbitmq::createJSONParser([INT,TIMESTAMP,INT], ["id","ts","volume"])
```

### close

```
rabbitmq::close(handle)
```

**详情**

关闭一个 connection 或者一个 Channel，注意，如果关闭 connection，其上的 Channel 也会自动关闭。

**参数**

**handle** 一个handle, 由 `connection` 接口或者 `channel` 接口返回。

**例子**

```
conn = rabbitmq::connection('localhost', 5672, 'guest', 'guest', "/")
rabbitmq::close(conn)
```

### closeAll

```
rabbitmq::closeAll()
```

关闭所有已经建立的 connection 和 Channel。

**例子**

```
rabbitmq::closeAll()
```

### getConnections

**语法**

```
rabbitmq::getConnections()
```

**详情**

获取所有已创建的 RabbitMQ 连接信息。

返回一个元组，每个元素都是一个字典，其键值如下：

* connection：连接句柄。
* createTime：创建连接的时间，类型为 TIMESTAMP。

### getChannels

**语法**

```
rabbitmq::getChannels([conn])
```

**详情**

如果填写了 conn 参数，则查询通过该 connection 所创建的通道信息；否则则查询所有已创建的通道信息。

返回一个元组，每个元素都是一个字典，其键值如下：

* connection：通道句柄所对应的连接句柄。
* channel：通道句柄。
* createTime：表示创建通道的时间，类型为 TIMESTAMP。

**参数**

**conn** 连接句柄。

## 完整例子

### GUI1

```
// 加载插件
loadPlugin("/home/yxu/Desktop/DolphinDBPlugin/rabbitmq/build/PluginRabbitMQ.txt")
// 建立连接
conn = rabbitmq::connection('localhost', 5672, 'guest', 'guest', '');
// 创建通道
ch = rabbitmq::channel(conn)
// 声明 Exchange
rabbitmq::declareExchange(ch, 'test-exchange', 'fanout', ['durable'])
rabbitmq::declareExchange(ch, 'test-exchange1', 'fanout', ['durable'])
rabbitmq::declareExchange(ch, 'test-exchange2', 'fanout', ['durable'])
rabbitmq::declareExchange(ch, 'test-exchange3', 'fanout', ['durable'])
rabbitmq::declareExchange(ch, 'test-exchange4', 'fanout', ['durable'])
// 绑定 Exchange
rabbitmq::bindExchange(ch, 'test-exchange1', 'test-exchange2', 'rule1')
// 解绑 Exchange
rabbitmq::unbindExchange(ch, 'test-exchange1', 'test-exchange2', 'rule1')
// 移除 Exchange
rabbitmq::removeExchange(ch, 'test-exchange')
rabbitmq::removeExchange(ch, 'test-exchange1')
rabbitmq::removeExchange(ch, 'test-exchange2')
rabbitmq::removeExchange(ch, 'test-exchange3')
rabbitmq::removeExchange(ch, 'test-exchange4')
// 声明 Queue
rabbitmq::declareQueue(ch, 'test-queue1', ['durable'])
rabbitmq::declareQueue(ch, 'test-queue2', ['durable'])
rabbitmq::declareQueue(ch, 'test-queue3', ['durable'])
rabbitmq::declareQueue(ch, 'test-queue4', ['durable'])
// 绑定 Queue
rabbitmq::bindQueue(ch, 'test-exchange1', 'test-queue1', 'rule1')
rabbitmq::bindQueue(ch, 'test-exchange2', 'test-queue2', 'rule1')
rabbitmq::bindQueue(ch, 'test-exchange3', 'test-queue3', 'rule1')
rabbitmq::bindQueue(ch, 'test-exchange4', 'test-queue4', 'rule1')
// 解绑 Queue
rabbitmq::unbindQueue(ch, 'test-exchange1', 'test-queue', 'rule1')
// 移除 Queue
rabbitmq::removeQueue(ch, 'test-queue1')
rabbitmq::removeQueue(ch, 'test-queue2')
rabbitmq::removeQueue(ch, 'test-queue3')
rabbitmq::removeQueue(ch, 'test-queue4')
// 发数据
rabbitmq::publish(ch, 'test-exchange1', 'rule1', 'Hello World1', 'bytestream')
rabbitmq::publish(ch, 'test-exchange2', 'rule1', 'Hello World1', 'bytestream')
// 取数据
def handle(msg){
}
rabbitmq::consume(ch, 'test-queue1', handle, 'bytestream', 'consumer1')

def handle(msg){
}
rabbitmq::consume(ch, 'test-queue2', handle, 'bytestream', 'consumer2')

// 取消取数据
rabbitmq::cancelConsume(ch, 'consumer1')
rabbitmq::cancelConsume(ch, 'consumer2')

// 发送 json 格式数据
formatter = rabbitmq::createJSONFormatter()
data = table(1..10 as id, take(now(), 10) as ts, rand(10, 10) as volume)
rabbitmq::publish(ch, 'test-exchange3', 'rule1', data, formatter)

// 发送 csv 格式数据
MyFormat = take("", 3)
MyFormat[1] = "0.000"
print(MyFormat)
data = table(1..10 as id, take(now(), 10) as ts, rand(10, 10) as volume)
formatter = rabbitmq::createCSVFormatter(MyFormat,',',';')
rabbitmq::publish(ch, 'test-exchange4', 'rule1', data, formatter)

// 接收 json 格式数据
parser = rabbitmq::createJSONParser([INT,TIMESTAMP,INT], ["id","ts","volume"])
def handle(msg){
}
rabbitmq::consume(ch, 'test-queue3', handle, parser, 'consumer3')

// 接收 csv 格式数据
parser1 = rabbitmq::createCSVParser([INT,STRING,INT], ',',';')
def handle(msg){
}
rabbitmq::consume(ch, 'test-queue4', handle, parser1, 'consumer4')

rabbitmq::cancelConsume(ch, 'consumer3')
rabbitmq::cancelConsume(ch, 'consumer4')

// 获取后台订阅信息
tb = rabbitmq::getSubJobStat()
print(tb)
// 取消某个后台订阅
rabbitmq::cancelSubJob(订阅id)
```

### GUI2

```
// 订阅完成 GUI2 可关闭
def handle(msg){
}
rabbitmq::createSubJob('test-queue2', handle, 'bytestream', 'consumer1',['localhost'], [5672], 'guest', 'guest')

// 后台订阅 json 格式数据
parser = rabbitmq::createJSONParser([INT,TIMESTAMP,INT], ["id","ts","volume"])
def handle(msg){
}
rabbitmq::createSubJob('test-queue3', handle, parser, 'consumer1',['localhost'], [5672], 'guest', 'guest')

// 后台订阅 csv 格式数据
parser1 = rabbitmq::createCSVParser([INT,STRING,INT], ',',';')
def handle(msg){
}
rabbitmq::createSubJob('test-queue4', handle, parser1, 'consumer1',['localhost'], [5672], 'guest', 'guest')
```
