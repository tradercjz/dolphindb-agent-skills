<!-- Auto-mirrored from upstream `documentation-main/plugins/rocketMQ.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# RocketMQ

DolphinDB 的 RocketMQ 插件，支持发送数据消息到 RocketMQ 集群、从 RocketMQ 集群中的 Topic 中接收数据。

## 安装插件

### 版本要求

DolphinDB Server：2.00.10 及更高版本。支持 x64 的 Linux 版本。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("RocketMQ")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("RocketMQ")
   ```

## 接口说明

### createProducer

**语法**

```
createProducer(namesrvAddr, groupName, [producerConfig])
```

**详情**

创建一个 RocketMQ 的 producer，可用于通过接口 send 发送数据到 RocketMQ。

一个 RocketMQ 的 producer 对象。

**参数**

**namesrvAddr** STRING 类型标量，表示 RocketMQ 集群的 NameServer 的地址，形式为 "ip:port" 。

**groupName** STRING 类型标量，表示生产者组。

**producerConfig** 一个字典，类型为 (STRING, ANY)，表示 producer 配置项，支持的配置项包括：

* sessionCredentials：STRING 类型的数组，代表用户凭证，元素分别为 accessKey，secretKey，accessChannel 。
* namesrvDomain：STRING 类型标量。当 RocketMQ 的客户端启动时，客户端会向指定的 NamesrvDomain 发送请求，以获取 Name Server 的地址列表。
* nameSpace：STRING 类型标量。通过使用 NameSpace，用户可以在一个 RocketMQ 集群中创建多个独立的逻辑分区，每个分区拥有独立的 Topic、Producer 和 Consumer。
* instanceName：STRING 类型标量，用于标识 RocketMQ 客户端实例的唯一名称。
* unitName：STRING 类型标量。用于标识 RocketMQ 的一个具体的业务单元的名称。
* sendMsgTimeout：INT 类型标量，表示单次发送的超时时间，单位是毫秒。必须大于 0，默认值为 3000。如果超过 \*sendMsgTimeout \*毫秒后仍失败，则再次发送，直到发送次数超过 *retryTimes*。
* retryTimes：INT 类型标量，表示发送重试次数。必须大于 0，默认值为 5 。
* compressMsgBodyOverHowmuch：INT 类型标量，用于指定消息体超过多大时启用压缩，单位是字节。必须大于 0，默认值为 4096。
* compressLevel：INT 类型标量，表示压缩等级。取值范围为 1-9，默认值为 4 。
* maxMessageSize：INT 类型标量，表示单条消息的最大长度，单位是字节。必须大于 0，默认值为 133632。
* tcpTransportConnectTimeout：INT 类型标量，表示连接超时时间，单位是毫秒。必须大于 0，默认值为 3000。

### send

**语法**

```
send(producer, data, topic, [tag = ""])
```

**详情**

发送数据到 RocketMQ。

返回一个布尔值，true 表示发送成功。

**参数**

**producer** 通过 `createProducer` 创建的 producer 对象。

**data** STRING、BLOB 类型的标量或向量，表示待发送的数据。

**topic** STRING 类型标量，表示待发送数据的主题。

**tag** STRING 类型标量，表示消息的 tag 标签。默认值为空字符串。

**示例**

```
producer = createProducer("192.168.1.38:9876", "group1");
msg = "msg1"
send(msg)
msg2 = ["msg1", "msg2"]
send(msg2)
```

### createSubJob

**语法**

```
createSubJob(namesrvAddr, groupName, topic, handler, [subExpression = "*"], [consumerConfig])
```

**详情**

创建一个 RocketMQ 的订阅任务，用于后台接收 RocketMQ 的数据。

返回任务 ID，类型为 STRING。

**参数**

**namesrvAddr** STRING 类型标量，表示 RocketMQ 集群的 NameServer 的地址，形式为 "ip:port" 。

**groupName** STRING 类型标量，表示消费者组。

**topic** STRING 类型标量，表示主题。

**handler** 一个一元函数对象，用于处理消息的函数句柄。接收的参数的数据结构是表。表中包含 BLOB 类型的 msg 列。

**subExpression** STRING 类型的标量，用于消息过滤，默认值为”\*”。

**consumerConfig** 一个字典，类型为 (STRING, ANY)，代表 consumer 配置项，支持的配置项包括：

* sessionCredentials：STRING 类型的数组，代表用户凭证，元素分别为 accessKey，secretKey，accessChannel 。
* messageModel：STRING 类型标量，表示消费模型：
  + "CLUSTERING" ：默认值，表示集群消费。
  + "BROADCASTING" ：表示广播消费。
* consumeFromWhere：STRING 类型标量，表示消费者从哪个位置开始消费数据：
  + "CONSUME\_FROM\_LAST\_OFFSET"：默认值，表示第一次启动从队列最后位置消费，后续再启动接着上次消费的进度开始消费。
  + "CONSUME\_FROM\_FIRST\_OFFSET"：第一次启动从队列初始位置消费，后续再启动接着上次消费的进度开始消费。
* namesrvDomain：STRING 类型标量。当 RocketMQ 的客户端启动时，客户端会向指定的 NamesrvDomain 发送请求，以获取 Name Server 的地址列表。
* instanceName：STRING 类型标量，用于标识 RocketMQ 客户端实例的唯一名称。
* unitName： STRING 类型标量。用于标识一个具体的业务单元的名称。
* nameSpace：STRING 类型标量，通过使用 *nameSpace*，用户可以在一个 RocketMQ 集群中创建多个独立的逻辑分区，每个分区拥有独立的 Topic、Producer 和 Consumer。
* consumeThreadCount：INT 类型标量，表示消费线程数。默认值为 1。
* pullMsgThreadPoolCount：INT 类型标量，表示拉取 RocketMQ 数据的线程数。必须大于 0，默认值为 1。
* maxReconsumeTimes：INT 类型标量，表示当消费消息失败时，RocketMQ 会尝试重新发送该消息最多次数。每次重试都会将消息放到队列的末尾，并等待其他消费者来消费。设置的值必须大于 0，不设置此参数时默认不会重试。
* tcpTransportConnectTimeout：INT 类型标量，表示连接超时时间，单位是毫秒。必须大于 0，默认值为 3000。
* asyncPull：BOOL 类型标量，表示在接收到数据后，是否异步执行 *handler*。默认值为 false，此时可以保证数据不丢失。
* batchSize：INT 类型标量，表示未处理消息的数量达到多少时，*handler* 才会处理消息。必须大于 0，默认值为 10000。仅在 \*asyncPull \*设置为 true 时生效。
* throttle：FLOAT 类型标量，表示继上次 *handler* 处理消息之后，若 *batchSize* 条件一直未达到，多久后再次处理消息，单位为毫秒。必须大于 0，默认值为 1。仅在 \*asyncPull \*设置为 true 时生效。

**例子**

```
def appendData(table1, data){
  table1.append!(data)
}
table1 = table(1:0, ["msg"], [BLOB])
RocketMQ::createSubJob("192.168.1.38:9876", "group1", ”topic1", appendData{table1})
```

### cancelSubJob

**语法**

```
cancelSubJob(jobId)
```

**详情**

取消后台订阅 RocketMQ 的任务。

返回一个布尔值，如果取消成功会返回 true。

**参数**

**jobId** STRING 类型标量，通过 `createSubJob` 或者是 `getSubJobStat` 返回的订阅任务 ID。

### getSubJobStat

**语法**

```
getSubJobStat()
```

**详情**

查询当前 RocketMQ 后台订阅任务的信息。

返回一个表，包含如下列：

* jobId：列类型为 STRING ，表示订阅 ID。
* startTime：列类型为 NANOTIMESTAMP，表示任务创建时间。
* endTime：列类型为 NANOTIMESTAMP，表示任务结束时间。任务可以通过 `cancelSubJob` 来取消。
* firstMsgTime：列类型为 NANOTIMESTAMP，表示第一条数据的接收时间。
* lastMsgTime：列类型为 NANOTIMESTAMP，表示上一条消息的接收时间。
* processedMsgCount：列类型为 LONG，表示成功处理的消息行数。
* failedMsgCount：列类型为 LONG，表示处理失败的消息行数。
* lastErrMsg：列类型为 STRING，表示上一次处理失败的错误信息。
* lastFailedTimestamp：列类型为 NANOTIMESTAMP，表示上一次处理失败的时间。

**参数**

无
