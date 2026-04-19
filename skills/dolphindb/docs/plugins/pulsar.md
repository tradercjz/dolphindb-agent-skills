<!-- Auto-mirrored from upstream `documentation-main/plugins/pulsar.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# pulsar

[Apache
Pulsar](https://pulsar.apache.org/) 是用于处理服务器间消息传递的多租户高性能解决方案。为便于在 DolphinDB 中使用 Apache Pulsar，现提供 Pulsar
客户端插件。通过 DolphinDB Pulsar 客户端插件，用户可以创建与 Pulsar Broker 的连接，创建 Producer 对象向主题发布消息，以及创建
Consumer 对象订阅并接收主题的消息。

插件目前仅支持发布和订阅 string 类型的消息。其中 `createSubJob` 接口在创建订阅任务时，支持传入自定义的 parser
对接收的消息进行解析。

## 安装插件

### 版本要求

DolphinDB Server 2.00.14 及更高版本，支持 Linux x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins`
   命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB
   用户社区](https://ask.dolphindb.net/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin`
   命令完成插件安装。

   ```
   installPlugin("pulsar")
   ```
3. 用 `loadPlugin`
   命令加载插件。

   ```
   loadPlugin("pulsar")
   ```

## 接口说明

### client

**语法**

`client(serviceUrl, [clientConfig])`

**参数**

**serviceUrl** 字符串标量，表示要使用的 Pulsar 终端（例如：pulsar://localhost:6650）。

**clientConfig** 可选参数，用于配置客户端行为的字典。字典的 key 为字符串，value 为元组。支持以下键值对：

* “operationTimeoutSeconds”：整型，客户端操作（如订阅，创建
  producer，关闭，取消订阅）的超时时间（单位：秒）。
* “connectionTimeoutMs”： 整型，连接 Pulsar broker 的超时时间（单位：毫秒）。
* “token”：字符串，鉴权所使用的令牌（token）。
* “memoryLimit”：整型，限制客户端可使用的内存上限（单位：MB）。

**详情**

获取连接到指定集群地址的 Pulsar client 对象。

**返回值**

Pulsar client 对象。

### producer

**语法**

`producer(client, topic, [producerConfig])`

**参数**

**client** 一个 Pulsar client 对象。

**topic** 字符串标量，表示 topic 名称。

**producerConfig** 可选参数，用于配置 producer 行为的字典。字典的 key 为字符串，value 为元组。支持以下键值对：

* “sendTimeoutMs”：整数，表示发送数据超时时间（单位：毫秒）。
* “maxPendingMessages”：整数，设置等待 broker 确认的消息队列的最大长度。
* “maxPendingMessagesAcrossPartitions”：整数，设置所有分区上待确认消息的最大数量。
* “blockIfQueueFull”：布尔值，表示当发送队列已满时，`send` 操作是否阻塞。默认值为
  false。
* “batchingEnabled”：布尔值，控制是否启用 producer 的消息自动批处理功能。
* “batchingMaxMessages”：整数，设置单个批次允许的最大消息数量。
* “batchingMaxPublishDelayMs”：整数，设置批量发送时允许的最大延迟时间（单位：毫秒）。

**详情**

根据 *topic* 创建一个 Pulsar producer 对象。

**返回值**

Pulsar producer 对象。

### send

**语法**

`send(producer, message, [partitionKey])`

**参数**

**producer** 一个 Pulsar producer 对象。

**message** 字符串标量，表示要发送的消息内容。

**partitionKey** 可选参数，字符串标量，表示该消息的分区键（ partition key）。分区键用于决定消息发送到哪个分区。

**详情**

将一条消息发送到指定的 Pulsar producer（生产者。支持可选的分区键（partition key）以实现精确控制消息路由。

**返回值**

无

### consumer

**语法**

`consumer(client, topic, subscriptionName, [consumerConfig])`

**参数**

**client** 一个 Pulsar client 对象。

**topic** 字符串标量，表示要订阅的 topic 名称。

**subscriptionName** 字符串标量，表示订阅名称。

**consumerConfig** 可选参数，用于配置消费者行为的字典。字典的 key 为字符串，value 为元组。支持以下键值对：

* “consumerType”：整数，表示消费者类型，取值如下：
  + 0：独占
  + 1：共享
  + 2：故障转移
  + 3：基于键的共享
* “receiverQueueSize”：整数，表示消费者接收队列的大小。设置较大的队列大小可以提高消费者的吞吐量，但会占用更多内存。
* “maxTotalReceiverQueueSizeAcrossPartitions”：设置所有分区上接收队列的最大总大小。
* “unAckedMessagesTimeoutMs”：设置未确认消息的超时时间（单位：毫秒），该值必须大于 10 秒。
* “subscriptionInitialPosition”：整数，表示消费者在首次订阅 topic 时从何处开始消费消息。取值如下：
  + 0：从最新位置开始
  + 1：从最早位置开始

**详情**

创建一个 Pulsar consumer 对象，用于订阅指定的 topic 并接收消息。

**返回值**

Pulsar consumer 对象。

### receive

**语法**

`receive(consumer, [timeoutMs=1000])`

**参数**

**consumer** 一个 Pulsar consumer 对象。

**timeoutMs** 可选参数，整数，表示接收消息的超时时间（单位：毫秒），默认值为 1000。

**详情**

从指定的 consumer 中接收一条已订阅的消息。

**返回值**

字符串，表示接收到的消息。

### createSubJob

**语法**

```
createSubJob(jobName, client, topic, subscriptionName, table, parser, [consumerConfig])
```

**参数**

**jobName** 字符串，表示任务名称。

**client** 一个 Pulsar client 对象。

**topic** 字符串，表示要订阅的 topic 名称。

**subscriptionName** 字符串，表示订阅的名称。

**table** 表对象或字符串标量，用于存储接收数据。若为字符串，仅支持 ORCA
的全限定表名，格式为"<catalog>.orca\_table.<name>"。

**parser** 一个函数，用于解析接收到的消息。该函数可接收 1 至 3 个字符串参数，依次对应消息的 data、partitionKey 和
topic。返回一个表对象作为处理结果。

**consumerConfig** 可选参数，用于配置 consumer 的字典。配置项详见 consumer 配置说明。

**详情**

创建一个订阅任务，持续订阅指定 topic。接收到的消息将由 `parser` 函数处理，并写入指定的 table 中。

**返回值**

订阅任务对象的 handle。

### cancelSubJob

**语法**

`cancelSubJob(subJob)`

**参数**

**subJob** 订阅任务对象的 handle，或者订阅任务名称（字符串）。

**详情**

取消指定的订阅任务。

**返回值**

无

### getJobStat

**语法**

`getJobStat()`

**详情**

获取当前所有订阅任务的状态信息。

**返回值**

返回包含当前所有订阅任务信息的表。

### getConfig

**语法**

`getConfig(handle, configName)`

**参数**

**handle** Pulsar 客户端（client）、生产者（producer）、消费者（consumer）或订阅任务对象。

**configName** 字符串，指定要查询的配置名称。支持的配置项详见 client，producer，和 consumer 接口。

**详情**

查询指定对象的某个配置项的当前生效值。

**返回值**

返回对应配置项的值。

## 例子

```
installPlugin("pulsar")
loadPlugin("pulsar")

// CLIENT

// define config dictionary
clientConfig = dict(["connectionTimeoutMs"], [2000])

client = pulsar::client("pulsar://localhost:6650", clientConfig)

// PRODUCER

producer = pulsar::producer(client, "persistent://public/default/my-topic")

pulsar::send(producer, "my message")

// CONSUMER

consumer = pulsar::consumer(client, "persistent://public/default/my-topic", "consumer-1")

pulsar::receive(consumer)

// SUBSCRIPTION JOB

// define parser
def parser(x) {
     return table([x] as msg)
}

demoTable = table(`a as msg)
share streamTable(1:0, demoTable.schema().colDefs.name, demoTable.schema().colDefs.typeString) as tb

subJob = pulsar::createSubJob("job-1", client, "persistent://public/default/my-topic", "subJob-1", tb, parser)
```

## FAQ

Q1：本地运行插件示例正常，为什么在生产环境中报错 "AuthorizationError"？

A1：生产环境通常禁用了默认命名空间 `public/default` 或未授予写权限。即使 token
正确，若无命名空间权限也会导致连接失败。请使用实际业务中已授权的命名空间进行连接。此外，Pulsar 的日志文件 pulsar-cpp-client.log 位于
server 目录中，可查看日志以进一步定位问题。
