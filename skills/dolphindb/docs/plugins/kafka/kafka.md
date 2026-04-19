<!-- Auto-mirrored from upstream `documentation-main/plugins/kafka/kafka.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Kafka

Kafka 是一种高吞吐量的分布式消息队列，DolphinDB 提供了 Kafka 插件用于发布或订阅 Kafka 流服务。Kafka 插件支持以 Json 格式、DolphinDB 序列化格式以及纯字符串格式发送、接收数据，也可以通过自定义回调函数的方式，订阅数据流写入 DolphinDB 中。Kafka 插件基于开源库 [librdkafka](https://github.com/confluentinc/librdkafka), [cppkafka](https://github.com/mfontanini/cppkafka) 进行开发。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本，支持 x86-64 Linux，ARM Linux。

其中 ARM Linux 版本的 Kafka 插件不支持 SASL 验证，且在生产和消费时不支持 zstd 压缩格式。

### 安装步骤

1. 在 DolphinDB 客户端中使用 listRemotePlugins 命令查看插件仓库中的插件信息。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 installPlugin 命令完成插件安装。

   ```
   installPlugin("kafka")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("kafka")
   ```

## 基础知识

在使用 Kafka 插件之前，需要对 Kafka 这一消息队列系统有一定的了解。以下是一些基础知识，在进一步阅读接口文档前您需要了解：

* **Kafka 集群（Cluster）**
  + 一个 Kafka 集群 （cluster）由多个 Kafka 实例 （broker）组成，每个实例在集群内都有唯一的编号。
* **数据生产与消费**
  + 生产者（Producer）将数据以主题（topic）为分类发送到 Kafka cluster 中。
  + 消费者（Consumer）从 Kafka cluster 中消费数据。
* **主题与分区（Topic & Partition）**
  + 每个 Kafka topic 可以有多个分区（partition），同一主题不同分区中的数据是不重复的。
  + 分区用于提高 Kafka 系统的吞吐量。
* **消费者组（Consumer Group）**
  + 可以将多个消费者组成一个消费者组（consumer group）。
  + 同一个分区的数据只能被消费者组中的某一个消费者所消费。
  + 建议同时订阅同一个主题的消费者数量小于分区数量，以避免消费者空转以及带来的重平衡（rebalance）问题。
* **重平衡机制（Rebalance）**
  + 当消费者组内的消费者数量或订阅的 topic 的分区数量发生变化时，Kafka 会重新分配 consumer 和 partition 之间的映射关系，以确保每个分区都会被消费。
* **副本与容错**
  + Kafka 主题的每个分区都可以有多个副本（replication）。
  + 如果主分区（Leader）出现故障，则会使用从分区（Follower）处理数据。
  + 副本的数量不能大于 broker 的数量。
* **偏移量与消费记录（Offset & Consumer Offset Committing）**：
  + Kafka 通过 commit 操作来记录某一个分区中消费者已经消费的 message 的偏移量（offset）。
  + 当消费者 crash 或发生重平衡时，Kafka 集群会基于 offset 继续发送数据。

更多参考资料请见：[Apache Kafka](https://kafka.apache.org/documentation/#gettingStarted)。

## 接口

### producer

**语法**

`kafka::producer(config, [errCallback])`

**详情**

根据指定配置创建一个 Kafka 生产者并返回。注意，目前没有显式的函数用于关闭 producer，如要删除可以将其置空触发析构。Server 的 `close` 函数无法关闭 producer。

**参数**

**config** 字典，表示 Kafka 生产者的配置。字典的 key 为字符串，value 为字符串或布尔值。

producer 的配置一般只需要填写地址就可以进行连接，如果 Kafka 集群启用了安全校验则需要有更多的配置选项。有关 Kafka 配置的详细信息，请参阅 [librdkafka/CONFIGURATION.md at master · confluentinc/librdkafka](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md) 。

**errCallback** 可选参数，函数类型，用于在后台发生错误（ERROR）或者警告（WARNING）情况下进行回调。该函数必须有三个入参，都是字符串类型，分别表示 level 错误等级，errorName 错误名称，message 具体错误信息。level 的值只可能为 “ERROR” 或者 “WARNING”。

**Kafka** **通用配置参数**

以下通用参数也可以在 consumer 中使用。

| 参数名 | 参数含义 | 示例 |
| --- | --- | --- |
| metadata.broker.list | 需要连接的 Kafka broker 地址，格式 host:port | 单地址："localhost:9092" 多地址："192.168.100.11:9092,192.168.100.11:9092,192.168.100.11:9092" |
| debug | 要开启的 debug 内容Producer 选项： broker, topic, msgConsumer 选项：consumer, cgrp, topic, fetch, all | 消费者取得 broker 和 topic 的 debug 信息： "broker,topic" 获取所有 debug 信息："all" 注意，Kafka 的 debug info 也会以 DolphinDB 的 DEBUG level 在日志中进行输出。 |
| session.timeout.ms | 客户端 session 和故障检测超时时间配置。客户端会定期发送心跳到 Kafka broker。如果 broker 在会话超时时间内没有收到心跳，则 broker 将从组中删除该 Consumer 并触发重新平衡，单位 ms。 | 45秒超时："45000" |
| max.poll.interval.ms | consumer 的 poll 操作调用间最大间隔时长，如果超过此间隔，则认为该 consumer 已经失效，将发起重新平衡，单位 ms。 | 5 分钟超时："3000000" |
| sasl.mechanisms | 用于验证的 SASL 机制，可以为 GSSAPI, PLAIN, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER。 注意只能填写一种机制。 | 无验证方式："PLAIN" GSSAPI 验证方式："GSSAPI" |
| security.protocol | 与 Kafka broker 连接时的验证机制，可以为 plaintext, ssl, sasl\_plaintext, sasl\_ssl | 明文连接："plaintext"ssl 连接："ssl" |
| sasl.username | 用于 PLAIN 和 SASL-SCRAM 机制的 SASL 用户名 | "username" |
| sasl.password | 用于 PLAIN 和 SASL-SCRAM 机制的 SASL 密码 | "password" |
| sasl.kerberos.service.name | Kafka 运行时使用的 Kerberos 服务名 | "kafkaAdmin" |
| sasl.kerberos.principal | Kafka broker 客户端的 kerberos principal | "kafkaClient@EXAMPLE.COM" |
| sasl.kerberos.keytab | kerberos 密钥表文件的路径 | "/path\_to\_keytab/client.keytab" |

**Kafka producer 专属配置参数**

| **参数名** | **参数含义** | **示例** |
| --- | --- | --- |
| compression.type | 消息压缩所要使用的方法，可以为 none, gzip, snappy, lz4, zstd。 | 如果要使用 gzip 压缩："gzip" |
| queue.buffering.max.messages | 生产者队列中最多能够存有的数据数量，注意不同的 topic 和 partition 会共用同一个队列。 | "10000000" |
| queue.buffering.max.kbytes | 生产者队列中所有消息大小的总和，该配置项生效的优先级高于 queue.buffering.max.messages。 | "2147483647" |

**示例**

创建一个普通连接本地 Kafka 的 producer。

```
producerCfg = dict(STRING, ANY)
producerCfg["metadata.broker.list"] = "localhost:9092"
handle = kafka::producer(producerCfg)
```

创建一个带有回调的 producer。

```
producerCfg = dict(string, any)
producerCfg["bootstrap.servers"] = "192.168.100.3"
share table(1:0, `level`err`reason, [STRING,STRING,STRING]) as produceDest
def producerCallback(mutable dest, level, err, reason) {
    tb = table([level] as level, [err] as err, [reason] as reason)
    dest.append!(tb)
}
producer = kafka::producer(producerCfg, producerCallback{produceDest})
```

### produce

**语法**

```
kafka::produce(producer, topic, key, value, marshalType, [partition])
```

**参数**

**producer** Kafka 生产者的句柄。

**topic** STRING 类型标量，要将数据发送到的 Kafka 的 topic。

**key** STRING 类型标量，需要发送的 Kafka 消息的 key。Kafka 的分区函数将会根据 key 的值进行分区，填写了相同 key 的消息会被分配到同一个分区中。

**value** STRING 类型标量，需要发送的 Kafka 消息体对应的数据。

**marshalType** 可选参数，STRING 类型标量，表示以何种格式序列化数据。具体取值可以为 "JSON", "DOLPHINDB", "PLAIN"，分别表示使用 JSON 格式序列化、DolphinDB 内部格式序列化，以及不进行序列化直接发送。最后一种方式只能发送字符串。

**partition** 可选参数，整型标量，表示要发送到的 Kafka topic 分区号。如果未填写则 Kafka 集群会将消息均匀地按 key 进行分区分配到 topic 的各个分区下。

**详情**

以选定的序列化格式，将数据发送到 Kafka 集群对应的 topic 中。具体的使用方式以及与 consumer 的配合见 [使用示例](#%E4%BD%BF%E7%94%A8%E7%A4%BA%E4%BE%8B)。

**注意**

* JSON 格式如果发送的是表格类型数据，会将一列的数据都写入一个数组中。
* 使用 DolphinDB 序列化格式发送的数据只能使用 Kafka 插件并指定对应的 DOLPHINDB marshalType 进行接收，否则二进制序列化数据将无法被处理。极有可能导致乱码的问题。

### producerFlush

**语法**

```
kafka::producerFlush(producer);
```

**参数**

**producer** Kafka 生产者的句柄。

**详情**

将生产者的所有缓存记录发送到 Kafka。通常在发送可能产生堆积时，调用该函数。

### consumer

**语法**

```
kafka::consumer(config, [errCallback])
```

**详情**

根据指定配置创建一个 Kafka 消费者，并返回。

注意，目前没有显式的函数用于关闭 consumer，如要删除可以将其置空触发析构。如果该 consumer 被用于 `kafka::createSubJob` 的话，如果想要关闭该 consumer，还需取消对应的后台任务。server 的 close 函数无法关闭 consumer。

**参数**

**config** 字典，表示 Kafka 消费者的配置。字典的 key 是一个字符串，value 是字符串或布尔值。

consumer 的配置中 metadata.broker.list 与 group.id 为必填项，通用配置参数的含义参考 [kafka::producer](#producer) 一节，有关 Kafka 配置的更多信息，请参阅 <https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md> 。

**errCallback** 可选参数，函数类型，用于在后台发生错误（ERROR）或者警告（WARNING）情况下进行回调。该函数必须有三个入参，都是字符串类型，分别表示 level 错误等级，errorName 错误名称，message 具体错误信息。level 的值只可能为 “ERROR” 或者 “WARNING”。

**kafka consumer 专属配置参数**

| 参数名 | 参数含义 | 示例 |
| --- | --- | --- |
| group.id | 必填项，该 consumer 对应的消费者组的名称 | “group1" |
| auto.offset.reset | 订阅开始的消息偏移，可以为 smallest, earliest, beginning, largest, latest, end, error。 | 从第一条开始订阅 "beginning"，"smallest" 或 "earliest" 订阅最新的消息 "latest" 或 "largest" |
| enable.auto.commit | 布尔值，是否启用自动 commit，默认为 true | 不开启自动 commit：false |
| auto.commit.interval.ms | 自动 commit 的时间间隔，默认 60000 ms | 修改为 100 ms 就自动自动 commit："100" |

**示例**

创建一个普通连接本地 Kafka 的 consumer，指定 group.id 为 group1。

```
consumerCfg = dict(STRING, ANY)
consumerCfg["group.id"] = "group1"
consumerCfg["metadata.broker.list"] = "localhost:9092";
consumer = kafka::consumer(consumerCfg)
```

### subscribe

**语法**

```
kafka::subscribe(consumer, topic)
```

**参数**

**consumer** Kafka 消费者的句柄。

**topic** STRING 类型标量或者向量，表示订阅的主题。

**详情**

订阅一个 Kafka 主题，无返回值。

注意：

1. 在使用插件时，同一消费者组中消费者的数量不要超过 topic 分区数，否则即使有分配了分区的消费者退出，先前没分配到分区的消费者也无法参与到 rebalance 中。
2. 如果订阅了不存在的 topic 或者订阅失败，并不会有返回信息与 log，但可以通过 `kafka::getAssignment` 函数查看订阅情况。

### unsubscribe

**语法**

```
kafka::unsubscribe(consumer)
```

**参数**

**consumer** 要取消 topic 订阅的 Kafka 消费者句柄。

**详情**

取消该消费者的所有订阅。

注意，即使是使用 `kafka::assign` 方式指定的以偏移量订阅，也能被 `kafka::unsubscribe` 所取消，需要谨慎使用。

### consumerPoll

**语法**

```
kafka::consumerPoll(consumer, [timeout=1000], [marshalType])
```

**参数**

**consumer** Kafka 消费者的句柄。

**timeout** INT 类型标量，可选。表示请求获取消息的最大等待时间，单位为毫秒。

**marshalType** STRING 类型标量，可选。表示以何种格式解析数据。具体取值可以为 “JSON”, ”DOLPHINDB”, ”PLAIN”，分别表示使用 JSON 格式解析、DolphinDB 内部格式解析，以及直接返回原始字符串。如果不指定，则会进行检测，选择 JSON 或者 DOLPHINDB 格式进行解析。

**详情**

从 Kafka 集群中获取订阅的消息，返回一个元组。第一个元素表示出错信息的字符串，若成功获取则为空。 第二个元素是一个元组，其元素包括：主题、分区、键、值和消费者收到数据的时间戳。具体的使用方式以及与 consumer 的配合见 [使用示例](#%E4%BD%BF%E7%94%A8%E7%A4%BA%E4%BE%8B)。

### consumerPollBatch

**语法**

```
kafka::consumerPollBatch(consumer, batchSize, [timeout=1000], [marshalType])
```

**参数**

**consumer** Kafka 消费者的句柄。

**batchSize** INT 类型标量，表示要批量消费的条数。

**timeout** INT 类型标量，可选。表示请求获取消息的最大等待时间，单位为毫秒。

**marshalType** STRING 类型标量，可选。表示以何种格式解析数据。具体取值可以为 “JSON”, ”DOLPHINDB”, ”PLAIN”，分别表示使用 json 格式解析、DolphinDB 内部格式解析，以及直接返回原始字符串。如果不指定，则会进行检测，基于检测结果，选择 JSON 或者 DOLPHINDB 格式进行解析。

**详情**

从 Kafka 集群中批量获取订阅的消息，返回一个元组。其中每个元素都是一个元组，其元素包括：主题、分区、键、值和消费者收到数据的时间戳。具体的使用方式以及与 consumer 的配合见 [使用示例](#%E4%BD%BF%E7%94%A8%E7%A4%BA%E4%BE%8B)。

### createSubJob

**语法**

```
kafka::createSubJob(consumer, table, parser, actionName, [throttle=1.0], [autoCommit], [msgAsTable=false], [batchSize=1], [queueDepth=1000000])
```

**consumer** 消费者的句柄。

**table** 表类型，可以是共享流表、共享内存表、共享键值表、共享索引表或 DFS 表。订阅数据会直接插入到该表中。

**parser** 可以为一元函数、二元函数、三元函数或者四元函数，用于处理 Kafka 的订阅数据。返回类型为表，返回结果将输出到 *table* 参数中：

* 如果指定 *msgAsTable* 为 false，*parser* 的参数数目可以为 1-4 个，依次为 Kafka 消息的 value、key、 topic、timestamp（类型为 TIMESTAMP）。若 Kafka 消息没有可用 timestamp，则第四个参数为 null。
* 如果指定 *msgAsTable* 为 true，*parser* 的输入参数需要为一个表。

注意：请勿在 *parser* 指定的回调函数中使用 `print` 函数。若需要输出打印信息，请使用 `writeLog` 函数将信息输出到 log 中。

**actionName** 是一个字符串，表示订阅任务的名称，与已经创建的订阅名称不可重复。

**throttle** 是一个浮点数，单位为秒，默认值为 1.0。表示继上次 *parser* 处理消息之后，若未达到 *batchSize* 条件，多久后再次处理消息。仅当 *msgAsTable* 为 *true* 时有效。

**autoCommit** 是一个布尔值，无默认值。表示是否在 *parser* 处理消息完成、插入到 *table* 数据表之后进行一次 Kafka 的 commit。

* 如果 *consumer* 对应的 comsumer 不会自动 commit，开启 *autoCommit* 可以防止因为系统崩溃而在插件端丢失 Kafka 订阅数据。因为没有进入 table 的数据没有被 commit，会随着系统恢复而被插件重新接收。
* 如果传入的 Kafka 的 config 中指定了 enable.auto.commit 为 false，且 *autoCommit* 没有指定为 *false*，则也会在消息处理后进行 commit 操作。

**msgAsTable** 是一个布尔值，默认值是 false。表示订阅的数据是否为表。

* 如果为 false，输入到 *parser* 的数据视 *parser* 参数个数而定，参数数目可以为 1-4 个，依次为 Kafka 消息的 value、key、 topic、timestamp（类型为 TIMESTAMP）。若 Kafka 消息没有可用 timestamp，则第四个参数为 null。
* 如果为 true，输入到 *parser* 的数据将为一个四列表，列名分别为 payload、key、topic、timestamp，列类型分别为 STRING、STRING、STRING、TIMESTAMP。

**batchSize** 是一个整数，默认值为 0。若为正数，表示未处理消息的数量达到 *batchSize* 时，*parser* 才会处理消息。若未指定或为非正数，每一批次的消息到达之后，*handler* 会立即处理。仅当 *msgAsTable* 为 *true* 时有效。

**queueDepth** 是一个整数，大于 0，默认值为 1000000。表示 Kafka 后台接收数据队列的深度。

**详情**

返回一个 subJob connection handle。具体的使用方式见 [使用示例](#%E4%BD%BF%E7%94%A8%E7%A4%BA%E4%BE%8B)。

### getJobStat

**语法**

```
kafka::getJobStat()
```

**详情**

返回一个表，包含通过 `kafka::createSubJob` 所创建的后台订阅任务的信息。

| **字段名称** | **类型** | **描述** |
| --- | --- | --- |
| subscriptionId | STRING | 订阅的字符串 ID |
| user | STRING | 使用者 |
| actionName | STRING | 描述，创建后台任务时指定的唯一名称 |
| createTimestamp | TIMESTAMP | 任务的创建时间 |
| processedMsgCount | LONG | 已经处理的消息数 |
| failedMsgCount | LONG | 处理失败的消息数 |
| lastErrMsg | STRING | 最后一条错误消息的信息 |
| lastFailedTimestamp | TIMESTAMP | 最后一条错误消息发生的时间 |
| msgAsTable | BOOL | 表示订阅的数据是否为表 |
| batchSize | LONG | parser 批量处理的消息数 |
| throttle | FLOAT | 表示继上次 parser 处理消息之后，若 batchSize 条件一直未达到，多久后再次处理消息 |
| autoCommit | BOOL | 是否在 parser 处理消息完成、插入到 table 数据表之后进行一次 Kafka 的 commit |

### cancelSubJob

**语法**

```
kafka::cancelSubJob(handle|actionName)
```

**参数**

**handle|actionName** 可以为函数 `kafka::createSubJob` 的返回值，也可以为创建任务时所指定的 *actionName*。

**详情**

取消对应的 Kafka subJob 后台任务。在取消后 `kafka::getJobStat` 也将无法查询到对应的记录。

注意，为保持兼容性，函数也可以传入 `kafka::getJobStat` 中对应记录的 *subscriptionId*，如果 *actionName* 与 *subscriptionId* 同名，则优先取消 *actionName* 对应的后台任务。

### getSubJobConsumer

**语法**

```
kafka::getSubJobConsumer(handle|actionName)
```

**参数**

**handle|actionName** 可以为函数 `kafka::createSubJob` 的返回值，也可以为创建任务时所指定的 *actionName*。

**详情**

每个 `kafka::createSubJob` 创建的后台任务都会有一个对应的 consumer handle，如果需要获取特定后台订阅中的 consumer 进行特殊处理，可以使用此接口。

### commit

**语法**

```
kafka::commit(consumer, [topic], [partition], [offset])
```

**参数**

**consumer** Kafka 消费者的句柄。

**topic** 可选，字符串标量或向量，表示订阅的主题。

**partition** 可选，整型标量或向量，表示对应主题的分区。

**offset** 可选，整型标量或向量，表示每个主题的偏移量。

*topic*, *partition*, *offset* 须保证形式相同，长度相同，其中的元素一一对应。

**详情**

将 consumer 最新消费数据的偏移量同步给 Kafka 集群。

如果指定了 topic、partition、offset，会以指定的信息进行 commit。

如果没有指定，则会 commit 传入的 consumer 所订阅的所有分区的最新消费 offset。

### assign

**语法**

```
kafka::assign(consumer, topic, partition, offset)
```

**参数**

**consumer** Kafka 消费者的句柄。

**topic** 字符串标量或向量，表示订阅的主题。

**partition** 整型标量或向量，表示每个主题的分区。

**offset** 整型标量或向量，表示每个主题的偏移量。

*topic*, *partition*, *offset* 须保证形式相同，长度相同，其中的元素一一对应。

**详情**

与 `kafka::subscribe` 不同，该函数为消费者手动指定特定的主题、分区和偏移量。

**注意**

* 当执行该函数后，消费者组将不会对这个 consumer 产生约束，即可以有多个 consumer 通过 assign 的方式消费同一个主题的同一个分区的数据。
* 在使用时，尽量避免对同一个消费者同时操作 `kafka::subscribe` 与 `kafka::assign` 操作，也尽量避免操作将以上函数执行多次，可能会出现一些未定义行为。

**示例**

指定 consumer 消费 test 主题，分区 1，偏移量为 3000 的消息。

```
kafka::assign(consumer, "test", 1, 3000)
```

### unassign

**语法**

```
kafka::unassign(consumer)
```

**参数**

**consumer** Kafka 消费者的句柄。

**详情**

取消 consumer 订阅的主题，对通过 `kafka::subscribe` 与 `kafka::assign` 执行的订阅都可以生效。

### getAssignment

**语法**

```
kafka::getAssignment(consumer)
```

**参数**

**consumer** Kafka 消费者的句柄。

**详情**

获取 consumer 对应的 offset assign 情况。返回一个 table，包含 3 列，topic 代表主题，partition 代表分区号，offset 代表偏移量。

注意，即便对应的 consumer 没有调用 assign 函数，只调用了 subscribe 函数，也能够得到具体的返回。

### getOffsetInfo

**语法**

```
kafka::getOffsetInfo(consumer, topic, partition)
```

**参数**

**consumer** Kafka 消费者的句柄。

**topic** 字符串标量或向量，表示订阅的主题。

**partition** 整型标量或向量，表示每个主题的分区。

*topic*, *partition* 须保证形式相同，长度相同，其中的元素一一对应。

**详情**

获取 consumer 对应的 topic 和 partition 的偏移量信息。注意，consumer 需要已经 subscribe 或者 assign 该 topic、partition，否则无法查出有效的信息。

返回一个 table，字段内容如下：

| **字段名称** | **类型** | **描述** |
| --- | --- | --- |
| topic | STRING | Kafka 主题名称 |
| partition | INT | 分区号 |
| minOffset | LONG | 该分区最小偏移量 |
| maxOffset | LONG | 该分区最大偏移量 |
| offsetPosition | LONG | 当前消费到的最新偏移量（该偏移量可能尚未被 commit） |
| offsetCommitted | LONG | 当前已经 commit 的偏移量 |

**示例**

`kafka::getAssignment` 与 `kafka::getOffsetInfo` 的使用常常引起疑问，这里举一个例子说明用法和各个字段的含义。

首先发送 10 条消息到 offsetTopic 这个新的 topic 中。

```
producerCfg = dict(string, any);
producerCfg["bootstrap.servers"] = "localhost"
producer = kafka::producer(producerCfg)
for (i in 0..9) {
    kafka::produce(producer, "offsetTopic", "0", "message", "PLAIN")
}
```

然后创建 consumer，消费两次。

```
consumerCfg = dict(string, any);
consumerCfg["metadata.broker.list"] = "localhost"
consumerCfg["enable.auto.commit"] = "false"
consumerCfg["group.id"] = "test"
consumer = kafka::consumer(consumerCfg)
kafka::assign(consumer, "offsetTopic", 0, 3)
kafka::consumerPoll(consumer,,"PLAIN")
kafka::consumerPoll(consumer,,"PLAIN")
```

此时执行 `kafka::getAssignment` 能看到订阅了 partition 0，offset 为 -1000 说明未指定具体的订阅 offset。

```
kafka::getAssignment(consumer)
```

| **topic** | **partition** | **offset** |
| --- | --- | --- |
| offsetTopic | 0 | -1,000 |

而执行 `kafka::getOffsetInfo` 会看到 offsetTopic 这个主题的 partition 0 的各类 offset 数据。其中 *minOffset* 为 0，因为发送了 10 条消息所以 *maxOffset* 为 10，当前 consumer 消费了 2 条数据，所以 *offsetPosition* 为 2。由于建立 consumer 时指定了不自动 commit，所以 *offsetCommitted* 为无意义值即尚未 commit 过。

```
kafka::getOffsetInfo(consumer, "offsetTopic", 0)
```

| **topic** | **partition** | **minOffset** | **maxOffset** | **offsetPosition** | **offsetCommitted** |
| --- | --- | --- | --- | --- | --- |
| offsetTopic | 0 | 0 | 10 | 2 | -1,001 |

如果执行一遍 `kafka::commit`，再查询偏移量相关信息，则会发现 *offsetCommitted* 字段变成了 2，即当前消费并 commit 的 offset。

```
kafka::commit(consumer)
kafka::getOffsetInfo(consumer, "offsetTopic", 0)
```

| **topic** | **partition** | **minOffset** | **maxOffset** | **offsetPosition** | **offsetCommitted** |
| --- | --- | --- | --- | --- | --- |
| offsetTopic | 0 | 0 | 10 | 2 | 2 |

### getMemId

**语法**

```
kafka::getMemId(consumer)
```

**参数**

**consumer** Kafka 消费者的句柄。

**详情**

返回一个字符串。每个 consumer 成员会有一个对应的 ID，可以通过该函数获取传入 consumer 的 ID。

**示例**

```
consumerCfg = dict(STRING, ANY)
consumerCfg["group.id"] = string(now())
consumerCfg["metadata.broker.list"] = "localhost:9092";
consumer = kafka::consumer(consumerCfg)
kafka::subscribe(consumer, "test");
kafka::consumerPoll(consumer); // 因为如果不进行数据的拉取，可能在 Kafka 集群端不会被分配对应 ID
kafka::getMemId(consumer)
// output: 'rdkafka-d9eded44-358f-49fc-be01-cc099b121d59'
```

### getMetadata

**语法**

```
kafka::getMetadata(handle|config)
```

**参数**

**handle|config** 可以为已经建立的 producer、consumer，或者用于建立连接的 dict，或者 Kafka cluster 的 IP PORT。

**详情**

用于获取对应 Kafka 集群的元数据信息。返回一个字典，包括以下键值对：

| **key** | **value 含义** | **value 形式** |
| --- | --- | --- |
| brokers | Kafka 集群各个节点的信息 | 一个 TABLE，包含 3 列 id、host、port，代表节点的 id、域名和对应端口。 |
| consumerGroups | 消费者组相关信息 | 一个 DICT，其中每个键值对对应一个消费者组，value 也是一个 DICT，包含 rebalance protocol 等元数据信息与消费者组中的成员列表信息。 |
| topics | 集群中已有的主题相关信息 | 一个 DICT，其中每个键值对对应一个 topic，value 为包含了 topic 下各个分区信息的表。 |

**示例**

直接查询 localhost Kafka 的元数据。

```
kafka::getMetadata("localhost:9092")
```

查询 consumer handle 对应 Kafka 集群的元数据。

```
kafka::getMetadata(consumer)
```

输出示例：

```
brokers->
  id host           port
  -- -------------- ----
  2  192.168.100.45 9092
  1  192.168.100.44 9092
  0  192.168.100.43 9092

consumerGroup->
  test->
    state->Stable
    protocolType->consumer
    protocol->range
    error->Success
    members->
      rdkafka-0b501728-5344-4f2f-a450-bc056f6e3400->
        clientID->rdkafka
        clientHost->/192.168.0.38
        memberAssignmentVersion->0
        partitions->
          topic partition offset
          ----- --------- ------
          test  0         -1001
          test  1         -1001
          test  2         -1001

topics->
  test->
    id error   leader replicas
    -- ------- ------ --------
    0  Success 0      [0]
    1  Success 1      [1]
    2  Success 2      [2]
```

## 使用示例

1. producer 以不同的格式生产数据，consumer 进行消费。注意，下面示例中，Kafka server 必须已存在名为 "msgTopic" 的 topic。

   ```
   // 建立生产者
   producerCfg = dict(string, any);
   producerCfg["bootstrap.servers"] = "localhost"
   producer = kafka::producer(producerCfg)

   // 建立消费者
   consumerCfg = dict(STRING, ANY)
   consumerCfg["group.id"] = string(now())
   consumerCfg["metadata.broker.list"] = "localhost:9092";
   consumer = kafka::consumer(consumerCfg)
   kafka::subscribe(consumer, "msgTopic");
   ```

   * PLAIN 格式发送

   ```
   // PLAIN 格式发送 table 通过 toStdJson 生成的字符串
   str = toStdJson(table([1,2,3] as c1, `a`b`c as c2))
   kafka::produce(producer, "msgTopic", "key", str, "PLAIN", 0)
   // Kafka 终端输出：[{"c1": 1,"c2": "a"},{"c1": 2,"c2": "b"},{"c1": 3,"c2": "c"}]

   // consumer 指定 PLAIN 格式进行消费
   kafka::consumerPoll(consumer,,"PLAIN")
   // output: (,("msgTopic","key","[{\"c1\": 1,\"c2\": \"a\"},{\"c1\": 2,\"c2\": \"b\"},{\"c1\": 3,\"c2\": \"c\"}]",0,2024.09.02T03:18:02.446))
   ```

   * JSON 格式发送

   ```
   // 发送 scalar
   kafka::produce(producer, "msgTopic", "key", 1, "JSON", 0)
   // Kafka 终端 ouput：[1]。注意，即便是一个 scalar，也会将其放入一个列表中

   // 发送 vector
   kafka::produce(producer, "msgTopic", "key", [1,2,3], "JSON", 0)
   // Kafka 终端 ouput：[1,2,3]

   // 发送 table
   kafka::produce(producer, "msgTopic", "key", table([1,2,3] as c1, `a`b`c as c2), "JSON", 0)
   // kafka 终端 ouput：{"c1":[1,2,3],"c2":["a","b","c"]}。注意，插件是以列的形式发送数据的

   // consumer 指定 JSON 格式进行批量消费
   kafka::consumerPollBatch(consumer, 3,100,"JSON")
   ```

   ```
   /*
   output，输出 ANY vector，其中每一个元素也是一个 ANY vector
   ((,("msgTopic","key",(1),0,2024.09.02T03:21:41.925)),
    (,("msgTopic","key",(1,2,3),0,2024.09.02T03:21:42.376)),
    (,("msgTopic","key",c1->(1,2,3) c2->("a","b","c"),0,2024.09.02T03:21:42.836)))
   */
   ```

   * DOLPHINDB 格式发送

   ```
   // 发送 table
   kafka::produce(producer, "msgTopic", "key", table([1,2,3] as c1, `a`b`c as c2), "DOLPHINDB", 0)
   // Kafka 终端 ouput:c1c2abc。注意，由于是以 DolphinDB 序列化格式进行发送，所以数据的格式会比较奇怪，也会有一些二进制字符

   // consumer 指定 DOLPHINDB 格式进行批量消费
   kafka::consumerPoll(consumer,100,"DOLPHINDB")
   /*
   output:
   (,("msgTopic","key",
     c1 c2
     -- --
     1  a
     2  b
     3  c
   ,0,2024.09.02T03:31:09.886))
   */
   ```
2. 以 Kafka 接收 JSON 数据写入后台流表的例子说明 createSubJob、cancelSubJob、getJobStat 等函数的使用方法。

   * 使用 `parseJsonTable` 解析非递归 JSON 对象。注意，下面示例中，Kafka server 必须已存在名为 "msgTopic1" 的 topic。

   ```
   consumerCfg = dict(STRING, ANY)
   consumerCfg["group.id"] = "subjob1"
   consumerCfg["metadata.broker.list"] = "localhost";
   consumer1 = kafka::consumer(consumerCfg)
   kafka::subscribe(consumer1, "msgTopic1");
   // 建立要输出的共享流表
   share streamTable(1:0, `date`id`msg, [DATE,INT,STRING]) as st1
   def parser1(msg) {
       // 指定 msgAsTable 为 true 后，回调时会返回 table
       // 将其中的 payload 列传入指定 schema 的 parseJsonTable，获取解析后的 JSON 数据
       return parseJsonTable(msg.payload, table(`date`id`msg as name, `DATE`INT`STRING as type))
   }
   // 指定 msgAsTable 为 true，throttle 0.1， batchSize 1000 建立后台任务 subjob1
   kafka::createSubJob(consumer1, st1, parser1, "subJob1", 0.1, false, true, 1000)

   // 发送 JSON 数据
   producerCfg = dict(string, any);
   producerCfg["bootstrap.servers"] = "localhost"
   producer = kafka::producer(producerCfg)
   /* 预期发送的 JSON 格式消息内容：
      {"msg":"kafka",
       "id":1,
       "date":"2024.08.30"}
   */
   kafka::produce(producer, "msgTopic1", "key", {date:2024.08.30, id:1, msg:"kafka"}, "JSON")
   kafka::produce(producer, "msgTopic1", "key", {date:2024.08.30, id:2, msg:"zookeeper"}, "JSON")
   kafka::produce(producer, "msgTopic1", "key", {date:2024.08.30, id:3, msg:"raft"}, "JSON")

   // 查看流表内容
   select * from st1
   ```

   | **date** | **id** | **msg** |
   | --- | --- | --- |
   | 2024.08.30 | 1 | kafka |
   | 2024.08.30 | 2 | zookeeper |
   | 2024.08.30 | 3 | raft |

   * 使用 `eval`、`parseExpr` 解析递归 JSON 数据。注意，下面示例中，Kafka server 必须已存在名为 "msgTopic2" 的 topic。

   ```
   consumerCfg["group.id"] = "subjob2"
   consumer2 = kafka::consumer(consumerCfg)
   kafka::subscribe(consumer2, "msgTopic2");
   share streamTable(1:0, `topic`date`id`msg, [STRING,DATE,INT,STRING]) as st2
   def parser2(payload, key, topic) {
       // 指定 msgAsTable 为 false，则每个消息都会出一遍回调
       ret = payload.parseExpr().eval()
       idVec = []$INT
       msgVec = []$STRING
       for (record in ret.record) {
           idVec.append!(record.id)
           msgVec.append!(record.msg)
       }
       count = ret.record.size()
       return table(take(topic, count) as topic, take(date(ret.date), count) as date, idVec as id, msgVec as msg)
   }
   kafka::createSubJob(consumer2, st2, parser2, "subjob2")

   /*
   发送嵌套 JSON 数据，预期发送的数据:
    {"record":[{"msg":"buy","id":1},
               {"msg":"sell","id":2},
               {"msg":"sell","id":3},
               {"msg":"withdraw","id":4}],
     "date":"2024.09.01"}
   */
   kafka::produce(producer, "msgTopic2", "key", {date:2024.08.30, record:[{id:1, msg:"buy"}, {id:2, msg:"withdraw"}]}, "JSON")
   kafka::produce(producer, "msgTopic2", "key", {date:2024.08.31, record:[{id:1, msg:"sell"}]}, "JSON")
   kafka::produce(producer, "msgTopic2", "key", {date:2024.09.01,  record:[{id:1, msg:"buy"}, {id:2, msg:"sell"}, {id:3, msg:"sell"}, {id:4, msg:"withdraw"}]}, "JSON")

   // 查看流表内容
   select * from st2
   ```

   | **topic** | **date** | **id** | **msg** |
   | --- | --- | --- | --- |
   | msgTopic2 | 2024.08.30 | 1 | buy |
   | msgTopic2 | 2024.08.30 | 2 | withdraw |
   | msgTopic2 | 2024.08.31 | 1 | sell |
   | msgTopic2 | 2024.09.01 | 1 | buy |
   | msgTopic2 | 2024.09.01 | 2 | sell |
   | msgTopic2 | 2024.09.01 | 3 | sell |
   | msgTopic2 | 2024.09.01 | 4 | withdraw |

   * 查看后台任务接收状态

   ```
   kafka::getJobStat()
   ```

   | **subscriptionId** | **user** | **actionName** | **createTimestamp** | **processedMsgCount** | **failedMsgCount** | **lastErrMsg** | **lastFailedTimestamp** | **msgAsTable** | **batchSize** | **throttle** | **autoCommit** |
   | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
   | 83095808 | admin | subJob1 | 2024.09.02 14:52:01.028 | 3 | 0 |  |  | true | 1,000 | 0.10000000149011612 | false |
   | 86054464 | admin | subjob2 | 2024.09.02 14:52:13.382 | 3 | 0 |  |  | false | 0 | 1 | false |

   * 通过订阅名取消所有后台订阅任务

   ```
   stat = kafka::getJobStat()
   for (action in stat.actionName) {
       kafka::cancelSubJob(action)
   }
   ```
3. 连接配置 SASL认证的 Kafka

   consumer 与 producer 连接时需要增加的配置相同，具体配置项的含义参考 [kafka::producer](#produce) 一节。

   * 基于密码进行认证

   ```
   consumerCfg = dict(string, any);
   consumerCfg["metadata.broker.list"] = "localhost";
   consumerCfg["group.id"] = "test";
   consumerCfg["sasl.mechanisms"] = "PLAIN";
   consumerCfg["security.protocol"] = "sasl_plaintext";
   consumerCfg["sasl.username"] = "username";
   consumerCfg["sasl.password"] = "password";
   consumer = kafka::consumer(consumerCfg);
   topics=["test"];
   kafka::subscribe(consumer, topics);
   kafka::consumerPoll(consumer);
   ```

   * 基于 kerberos 认证。需要运行 DolphinDB 的机器上安装了 kerberos 客户端，并有验证过的密钥文件才能连接。

   ```
   producerCfg=dict(STRING, ANY)
   producerCfg["metadata.broker.list"] = "aftersale2:9094"
   producerCfg["sasl.mechanisms"] = "GSSAPI"
   producerCfg["security.protocol"] = "sasl_plaintext";
   producerCfg["sasl.kerberos.service.name"] = "kafkaAdmin";
   producerCfg["sasl.kerberos.principal"] = "kafkaclient@EXAMPLE.COM";
   producerCfg["sasl.kerberos.keytab"] = "/path_to_kerberos/kerberos/kafkaclient.keytab";
   producer = kafka::producer(producerCfg)
   ```
4. 连接配置 SSL 认证的 Kafka

通过插件连接启用 SSL 认证的 kafka broker。有关生成 SSL 认证文件的具体方法，请参考：[Using SSL with librdkafka](https://github.com/confluentinc/librdkafka/wiki/Using-SSL-with-librdkafka) 。

```
ca_path = "/home/slshen/opt/kafka_ssl_rdkafka/ca"
producerCfg = dict(string, any);
producerCfg["bootstrap.servers"] = "host:port"
producerCfg["security.protocol"] = "ssl";
producerCfg["ssl.ca.location"] = ca_path + "/rdkafka/ca-cert"
producerCfg["ssl.certificate.location"] = ca_path + "/rdkafka/client_c1_client.pem"
producerCfg["ssl.key.location"] = ca_path + "/rdkafka/client_c1_client.key"
producerCfg["ssl.key.password"] = "key.password"
producer = kafka::producer(producerCfg)
```

## 常见问题

1. 后台线程解析出现问题，如何排查？

   通过 `kafka::getJobStat` 函数查看是否有解析失败的情况出现，也可以监控消费数据的条数。
2. 为什么插件发送的数据有非法字符出现在开头？

   使用 DOLPHINDB 序列化类型发送的消息会以 DolphinDB 二进制的协议进行发送，此时如果直接接收字符串查看则看起来会是乱码。
3. Kafka 报错在哪里看，有时候 poll 不出数据了怎么排查？

   通过查看 DolphinDB server log 中 `[PLUGIN::KAFKA]` 开头的日志，从中可能找到后台记录的报错信息。
4. assign 和 subscribe 的区别是什么？

   assign 将会消费指定 topic、partition 从 offset 开始的消息，此时消费者组将会失效。

   subscribe 时，每个 consumer 将会属于一个消费者组，同一个消费者组中，对同一 topic、partition 消息的消费不会重复。
5. 想手动控制 commit 信息怎么操作？

   首先需要在 consumer 的配置中设置 enable.auto.commit 选项为 false ，避免自动进行消息的 commit。

   然后在需要 commit 时调用 `kafka::commit` 函数，commit 消息。
6. produce 时出现 Local: Queue full 的原因？

   发送速度过快，需要修改参数配置 queue.buffering.max.messages、queue.buffering.max.kbytes。详细用法可以参考 [kafka::producer](#producer) 一节。
7. 后台订阅时，第一条消息会收到 Application maximum poll interval (3000000 ms) exceeded by ... ，而不是具体的信息。

   两次 poll 的间隔时间太长，可能是建立 consumer 后太久没有进行 poll 操作导致。
8. 经过 Kerberos 认证的 Kafka 连接失败，如何排查？

在配置了 Kerberos 认证的 Kafka 环境中，连接失败的排查主要依赖日志信息，因为 Kafka 的认证过程通常在后台完成，前台仅会显示通用错误，例如 `broker transport failure`。由于 Kerberos 配置较为复杂，建议具有一定运维经验的用户启用。

以下为几种常见的 Kerberos 认证失败原因及其对应的日志示例：

* 如果 Kafka 插件加载所在机器没有配置好 /etc/hosts，找不到 Kafka server 的域名会无法连接成功，日志报错例子：
  `2024-12-09 06:54:02.445669000,2fea <ERROR> :[PLUGIN::KAFKA] facility: FAIL, message: [thrd:sasl_plaintext://aftersale2:9094/bootstrap]: sasl_plaintext://aftersale2:9094/bootstrap: Failed to resolve 'aftersale2:9094': Name or service not known (after 12ms in state CONNECT)`
* 环境中缺少 Kerberos 库，则连接会失败。前台报错 `sh: kinit: command not found`，日志报错例子：

  ```
  :[PLUGIN::KAFKA] facility: SASLREFRESH, message: [thrd:main]: Kerberos ticket refresh failed: kinit -R -t "/path_to_kerberos/kerberos/kafkaclient.keytab" -k    kafkaclient@EXAMPLE.COM || kinit -t "/path_to_kerberos/kerberos/kafkaclient.keytab" -k kafkaclient@EXAMPLE.COM: exited with code 127
  2024-12-09 07:02:08.319563000,cea <ERROR> :[PLUGIN::KAFKA] facility: LIBSASL, message: [thrd:sasl_plaintext://aftersale2:9094/bootstrap]: sasl_plaintext://aftersale2:9094/bootstrap: Cyrus/libsasl2 is missing a GSSAPI module: make sure the libsasl2-modules-gssapi-mit or cyrus-sasl-gssapi packages are installed
  2024-12-09 07:02:08.319742000,cea <ERROR> :[PLUGIN::KAFKA] facility: FAIL, message: [thrd:sasl_plaintext://aftersale2:9094/bootstrap]: sasl_plaintext://aftersale2:9094/bootstrap: Failed to initialize SASL authentication: SASL handshake failed (start (-4)): SASL(-4): no mechanism available: No worthy mechs found (after 0ms in state AUTH_REQ)
  ```
* Kerberos 客户端未正确配置 krb5.conf文件会导致连接失败。前台报错 kinit: Invalid UID in persistent keyring name while getting default ccache，日志报错例子：

  ```
  2024-12-09 07:24:26.230664000,79b6 <ERROR> :[PLUGIN::KAFKA] facility: LIBSASL, message: [thrd:sasl_plaintext://aftersale2:9094/bootstrap]: sasl_plaintext://aftersale2:9094/bootstrap: GSSAPI Error: Unspecified GSS failure.  Minor code may provide more information (No Kerberos credentials available: Invalid UID in persistent keyring name)
  2024-12-09 07:24:26.230852000,79b6 <ERROR> :[PLUGIN::KAFKA] facility: FAIL, message: [thrd:sasl_plaintext://aftersale2:9094/bootstrap]: sasl_plaintext://aftersale2:9094/bootstrap: Failed to initialize SASL authentication: SASL handshake failed (start (-1)): SASL(-1): generic failure: GSSAPI Error: Unspecified GSS failure.  Minor code may provide more information (No Kerberos credentials available: Invalid UID in persistent keyring name) (after 1ms in state AUTH_REQ)
  ```
* 如果 Kafka 服务端的 Kerberos 主体不存在会导致连接失败。可以在 Kerberos server 机器上通过 kadmin.local 的 listprincs 命令查询是否数据库中存在对应的凭据。日志报错例子：

  ```
  2024-12-09 08:07:05.294237000,24e8 <ERROR> :[PLUGIN::KAFKA] facility: LIBSASL, message: [thrd:sasl_plaintext://aftersale2:9094/bootstrap]: sasl_plaintext://aftersale2:9094/bootstrap: GSSAPI Error: Unspecified GSS failure.  Minor code may provide more information (Server kafkaClient/aftersale2@EXAMPLE.COM not found in Kerberos database)
  ```

  如果本身不存在 `kafkaClient/aftersale2@EXAMPLE.COM` 凭据，则无法连接成功。
