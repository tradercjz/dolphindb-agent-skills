<!-- Auto-mirrored from upstream `documentation-main/plugins/redis.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Redis

通过 DolphinDB 的 Redis 插件，用户可以建立连接到指定 IP 和端口的 Redis 服务器，并进行数据操作。Redis 插件使用了 Hiredis 库，这是一个轻量级的 Redis C 客户端库。

## 在插件市场安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x64、Windows x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("redis")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("redis")
   ```

## 接口说明

### connect

**语法**

```
redis::connect(host, port)
```

**详情**

与 Redis server 建立一个连接，返回一个 Redis 连接的句柄。

**参数**

**host** 要连接的 Redis server 的 IP 地址，类型为 STRING。

**port** 要连接的 Redis server 的端口号，类型为 INT。

**返回值**

返回创建的 Redis 连接的句柄。

**示例**

假设 redis server 监听在 127.0.0.1:6379 端口。

```
conn = redis::connect("127.0.0.1",6379)
```

### run

**语法**

```
redis::run(conn, arg1, arg2, arg3, ...)
```

**详情**

执行 Redis 命令，注意如果 Redis 设置有密码，需要首先 redis::run(conn, "AUTH", "password") 来获取权限。返回值可以是 Redis 可以返回的任何数据类型，如 string, list, 或 set。

注意如果运行时报错，那么该连接不能再被使用，应该 release 这个连接并重新 connect 建立一个新的连接。如果继续使用之前的连接，会一直报同样的报错。

**参数**

**conn** 通过 `redis::connect` 获得的 Redis 连接句柄。

**arg1** SET, GET 等 Redis 命令，类型为 STRING。

**arg2, arg3, ...** Redis 命令所需的额外参数。

**返回值**

返回命令运行结果。

**示例**

运行 SET, GET 等 Redis 命令，并自动在 DolphinDB 数据和 Redis 请求/响应值之间转换 DolphinDB 的类型；例如下面 `redis::run(conn, "SET", "abc","vabc")` 自动将 DolphinDB 的字符串 `"abc"` 转化为了 Redis 的字符串 `"abc"` 和 `"vabc"`。

```
conn = redis::connect("127.0.0.1",6379)
redis::run(conn, "SET", "abc", "vabc")
val = redis::run(conn, "GET", "abc")
val == "vabc"
```

### batchSet

**语法**

```
redis::batchSet(conn, key, value)
```

**详情**

批量执行 Redis 的 set 操作，可通过 `subscribeTable` 函数来订阅流数据表。

注意：如果运行时报错，那么该连接不能再被使用，应该 `release` 这个连接并重新 `connect` 建立一个新的连接。如果继续使用之前的连接，会一直报同样的报错。

**参数**

**conn** 通过 `connect` 获得的 Redis 连接句柄。

**key** 要设置的 key，为 String 标量或者向量。

**value** 要设置的 value，为 String 标量或者向量。

**示例**

```
conn = redis::connect("127.0.0.1",6379)

redis::batchSet(conn, "k1", "v1")

key = ["k2", "k3", "k4"]
value = ["v2", "v3", "v4"]
redis::batchSet(conn, key, value)
```

### batchHashSet

**语法**

```
redis::batchHashSet(conn, key, fieldData)
```

**详情**

批量执行 Redis 的 HSET 操作。

注意：如果运行时报错，那么该连接不能再被使用，应该 `release` 这个连接并重新 `connect` 建立一个新的连接。如果继续使用之前的连接，会一直报同样的报错。

**参数**

**conn** 通过 `connect` 获得的 Redis 连接句柄。

**key** 一个 String 类型数组，每一个元素作为 HSET 中的一个 key 对应 fieldData 表中的一行数据。

**fieldData** 一个每列都是 String 类型的表，每列列名作为 Redis HSET 中的 field，值作为 HSET 中的 value。

**示例**

```
loadPlugin("path/PluginRedis.txt");
go

// 生成数据
n=43200
instrument_id = take("HO2305-D-",n)+string(1..n)
time_stamp = timestamp(2024.02.02T09:30:01..2024.02.02T21:30:00)
jiaoyisuo = take("CFFEX",n)
last_price = rand(10.0,n)
volume = rand(100000,n)
bid_price1 = rand(10.0,n)
bid_volume1 = rand(1000,n)
bid_price2 = rand(10.0,n)
bid_volume2 = rand(1000,n)
bid_price3 = rand(10.0,n)
bid_volume3 = rand(1000,n)
bid_price4 = rand(10.0,n)
bid_volume4 = rand(1000,n)
bid_price5 = rand(10.0,n)
bid_volume5 = rand(1000,n)
t = table(instrument_id, time_stamp,jiaoyisuo, last_price,volume, bid_price1,bid_volume1, bid_price2,bid_volume2,bid_price3,bid_volume3,bid_price4,bid_volume4,bid_price5,bid_volume5)
conn=redis::connect("127.0.0.1",6379)

// 批量设置
ids = exec instrument_id from t
fieldData =  select string(time_stamp) as time_stamp,string(jiaoyisuo) as jiaoyisuo,string(last_price) as last_price,string(volume) as volume,string(bid_price1) as bid_price1,string(bid_volume1) as bid_volume1,string(bid_price2) as bid_price2,string(bid_volume2) as bid_volume2,string(bid_price3) as bid_price3,string(bid_volume3) as bid_volume3,string(bid_price4) as bid_price4,string(bid_volume4) as bid_volume4,string(bid_price5) as bid_price5,string(bid_volume5) as bid_volume5 from t

redis::batchHashSet(conn, ids, fieldData)
```

### batchPush

**语法**

```
redis::batchPush(conn, key, value, [rightPush=true])
```

**详情**

批量执行 Redis 的 RPUSH 或 LPUSH 操作。

注意：该函数不能保证对所有 key 的操作都成功，但可以保证对单个 key 操作的原子性，即对一个 key 的操作要么全部成功，要么全部失败。

**参数**

**conn** 通过 `connect` 获得的 Redis 连接句柄。

**key** 要设置的 key，为 STRING 类型向量。

**value** 要设置的 value，为一个元组，其元素必须是 STRING 类型向量。

**rightPush** 可选参数，为 BOOL 标量。默认为 true，表示 RPUSH；若设置为 false，则为 LPUSH。

**示例**

```
conn = redis::connect("127.0.0.1",6379)
key = ["k1", "k2", "k3"]
value = [["v1, v2"], ["v3", "v4", "v5"], ["v6"]]
redis::batchPush(conn, key, value)
```

### batchGet

**语法**

```
redis::batchGet(conn, key)
```

**详情**

批量查询指定的键，返回一个 STRING 类型向量。

**参数**

**conn** 通过 `redis::connect` 获得的 Redis 连接句柄。

**key** STRING 类型向量，表示要查询的键。

**示例**

```
conn = redis::connect("127.0.0.1",6379)
key = ["k2", "k3", "k4"]
redis::batchGet(conn, key)
```

### release

**语法**

```
redis::release(conn)
```

**详情**

关闭与 Redis server 的连接 conn。

**参数**

**conn** 通过 `connect` 获得的 Redis 连接句柄。

**示例**

```
conn = redis::connect("127.0.0.1",6379)
redis::release(conn)
```

### releaseAll

**语法**

```
redis::releaseAll()
```

**详情**

关闭所有与 Redis server 的连接。

**示例**

```
conn = redis::releaseAll()
```

### getHandle

**语法**

```
redis::getHandle(token)
```

**详情**

获取 token 对应的 Redis 句柄。

**参数**

**token** 通过 `redis::getHandleStatus` 返回表中的第一列得知，用于唯一标识一个 Redis 连接。

**返回值**

返回对应 token 的句柄。

**示例**

```
handle = redis::getHandle(token)
```

### getHandleStatus

**语法**

```
redis::getHandleStatus()
```

**详情**

返回一张表描述当前所有已建立的连接：

* token 列是该连接的唯一标识，可通过 `redis::getHandle(token)` 来获取句柄。
* address 是连接的 Redis server 的 "ip:port" 网络地址。
* createdTime 是该连接创建的时间。
* channel 表示通过 subscribe 订阅的频道或模式。若包含多个频道或模式，需以空格分隔。

**示例**

```
status = redis::getHandleStatus()
```

### subscribe

**语法**

```
redis::subscribe(conn, channel, handler, [isPattern=false], [password=""])
```

**详情**

该函数用于开启订阅，每当收到消息时会触发 handler 回调。

* 订阅模式下，该连接仅支持 subscribe、unsubscribe 和 release 接口。
* 订阅一旦开启，该接口只能调用一次；调用 release 将释放 Redis 连接并终止订阅。

**参数**

**conn** 通过 connect 获得的 Redis 连接句柄。

**channel** STRING 类型标量或向量，表示要订阅的一个或多个频道或模式。

**handler** 一个二元函数，订阅消息到达时回调执行。参数为 (channel， message)，channel 表示频道或模式，message 表示接收到的消息。

**isPattern** 可选参数，BOOL 类型标量，默认为 false。

* false：订阅使用 SUBSCRIBE 命令，channel 为频道名；
* true：订阅使用 PSUBSCRIBE 命令，channel 为模式。

**password** 可选参数，STRING 类型标量，表示认证信息，默认为空。如果未设置此参数，插件重连时会因缺少认证信息而订阅失败，建议设置此参数避免该问题。

### unsubscribe

**语法**

```
redis::unsubscribe(conn, channel)
```

**详情**

取消指定频道或模式的订阅。

**参数**

**conn** 通过 connect 获得的 Redis 连接句柄。

**channel** STRING 类型标量或向量，表示要取消订阅的一个或多个频道或模式，必须是先前通过 subscribe 指定的频道或模式（可通过 getHandleStatus 查询已订阅的频道或模式）。

### 流数据接口

#### createStreamGroup

**语法**

```
redis::createStreamGroup(conn, key, group, [msgId="$"], [mkStream=false])
```

**详情**

根据指定配置创建一个 Redis 消费者组，用于消费流数据。

**参数**

**conn** 通过 `redis::connect` 获得的 Redis 连接句柄。

**key** STRING 类型标量，指定要消费的 stream 的名称。

**group** STRING 类型标量，指定消费者组的名称。

**msgId** 可选参数，STRING 类型标量，指定消费组从哪个 ID 开始消费。默认为 "$"，表示从最新消息开始消费；"0" 表示从头开始消费。

**mkStream** 可选参数，布尔值，指定是否创建 stream。为 true 且指定的 stream 不存在时，根据 *key* 值自动创建新的 stream。默认为 false。

**返回值**

无。

#### readStreamGroup

**语法**

```
redis::readStreamGroup(conn, key, group, consumer, [count=1], [readPending=">"], [maxWaitTime=0], [writeToPending=false])
```

**详情**

以同步的方式通过消费者组消费流数据。

**参数**

**conn** 通过 `redis::connect` 获得的 Redis 连接句柄。

**key** STRING 类型标量，指定要消费的 stream 的名称。

**group** STRING 类型标量，指定消费者组的名称。

**consumer** STRING 类型标量，指定消费者的名称（如不存在会自动创建）。

**count** 可选参数，INT 类型标量，指定消息的最大读取条数，默认为 1。

**readPending** 可选参数，STRING 类型标量，指定是否读取待处理消息，目前只支持 ">" 和 "0"，默认为 ">"。

* ">"：只读取新消息，即从未传递给任何消费者的消息。
* "0"：只读取当前 consumer 已读取但未 ACK 确认的待处理消息。在这种模式下，*maxWaitTime* 和 *writeToPending* 参数不可设置，因为该模式只用于重新获取当前 consumer 尚未处理完成的消息。

**maxWaitTime** 可选参数，INT 类型标量，指定等待新消息的最大时间（单位：毫秒）。默认为 0，表示如果没有新消息，系统立即返回空结果；如果大于 0，系统会在指定时间内等待新消息，只要有新消息就立即返回，或超时返回空结果。

**writeToPending** 可选参数，布尔值，指定是否将消息放入待处理队列中，默认为 false，表示不放入待处理队列，相当于读取时自动确认，为 true 时则需要手动确认。

**返回值**

一个字典，其中 key 是 STRING 类型，表示消息 ID；value 是字典类型，包含消息的键值数据，其中键值均为 STRING 类型。如果没有消息，返回空字典。示例如下：

```
{
  "1702200000000-0": {"field1": "value1", "field2": "value2"},
  "1702200000001-0": {"field1": "value3", "field2": "value4"}
}
```

#### subscribeStream

**语法**

```
redis::subscribeStream(host, port, key, group, consumer, outputTable, parser, actionName, [readPending=">"], [batchSize=100], [autoAck=true], [password=""])
```

**详情**

创建一个后台订阅任务，持续从指定的 Redis stream 消费消息，并调用 `parser` 回调函数处理。

**参数**

**host** STRING 类型标量，指定主机地址。

**port** INT 类型标量，指定主机端口号。

**key** STRING 类型标量，指定要消费的 stream 的名称。

**group** STRING 类型标量，指定消费者组的名称。需提前通过 `createStreamGroup` 创建。

**consumer** STRING 类型标量，指定消费者的名称。

**outputTable** 一个表，用于存放 `parser` 函数的返回结果。

**parser** 回调函数，拥有一个参数，为订阅收到的消息字典。此函数用来解析订阅的消息，结果需要返回一张表，用于写入到 *outputTable* 中。

**actionName** STRING 类型标量，指定订阅任务的名称，用于标识和管理订阅。

**readPending** 可选参数，STRING 类型标量，指定订阅开始后是否优先读取待处理消息，目前支持 ">" 和 "0"，默认为 ">"。

* ">"：表示只读取新消息，即从未传递给任何消费者的消息。
* "0"：读取当前 consumer 已读取但未 ACK 确认的待处理消息，注意会直接读取全部 待处理消息，不受 *batchSize* 影响。

**batchSize** 可选参数，INT 类型标量，指定每次从 Redis 批量读取的消息条数，默认为 100。

**autoAck** 可选参数，布尔值，指定是否在 `parser` 处理完成后自动确认消息，默认为 true。

**password** 可选参数，STRING 类型标量，表示认证信息，默认为空。如果未设置此参数，插件重连时会因缺少认证信息而订阅失败，建议设置此参数避免该问题。

**返回值**

无。

#### getSubscriptionStats

**语法**

```
redis::getSubscriptionStats()
```

**详情**

获取后台订阅任务的信息。

**参数**

无。

**返回值**

返回一个表，包含以下列：

| **列名** | **类型** | **描述** |
| --- | --- | --- |
| actionName | STRING | 订阅任务的名称。 |
| conn | STRING | Redis 连接地址。 |
| stream | STRING | stream 的名称。 |
| group | STRING | 消费者组的名称。 |
| consumer | STRING | 消费者的名称。 |
| createTime | TIMESTAMP | 任务的创建时间。 |
| processedMsgCount | LONG | 已成功处理的消息数。 |
| status | STRING | 任务的状态。OK 代表正常，FATAL 代表出错停止。 |
| lastErrMsg | STRING | 最后一条错误信息。 |
| lastFailedTime | TIMESTAMP | 最后一次错误发生的时间。 |
| autoAck | BOOL | 是否自动确认消息。 |

#### unsubscribeStream

**语法**

```
redis::unsubscribeStream(actionName)
```

**详情**

取消指定的订阅任务。取消后，后台线程停止消费。

**参数**

**actionName** STRING 类型标量，指定订阅任务的名称。

**返回值**

无。

#### ackMessages

**语法**

```
redis::ackMessages(conn, key, group, msgIds)
```

**详情**

确认消息已被处理，将消息从消费者组的待处理列表中移除。

**参数**

**conn** 通过 `redis::connect` 获得的 Redis 连接句柄。

**key** STRING 类型标量，指定 stream 的名称。

**group** STRING 类型标量，指定消费者组的名称。

**msgIds** STRING 类型向量，指定要确认的消息 ID 列表。

**返回值**

INT 类型标量，为成功确认的消息数量。

## 使用示例

### 示例 1：将流数据表中的数据写入 Redis

```
loadPlugin("redis");
go

dropStreamTable(`table1)

colName=["key", "value"]
colType=["string", "string"]
enableTableShareAndPersistence(table=streamTable(100:0, colName, colType), tableName=`table1, cacheSize=10000, asynWrite=false)

def myHandle(conn, msg) {
	redis::batchSet(conn, msg[0], msg[1])
}

conn = redis::connect("replace_with_redis_server_ip",6379)
subscribeTable(tableName="table1", handler=myHandle{conn})

n = 1000000
for(x in 0:n){
	insert into table1 values("key" + x, "value" + x)
}

t = table(n:0, [`id, `val], [`string, `string])
for(x in 0:n){
	insert into t values("key" + x, redis::run(conn, "GET", "key" + x))
}

ret = exec count(*) from t

assert "test", n==ret
```

### 示例 2：同步消费流数据

加载 redis 插件并配置消费所需的基本信息。

```
loadPlugin("redis")

host = "127.0.0.1"
port = 6379
streamKey = "test_stream"
groupName = "test_group"
consumerName = "consumer1"
```

创建 Redis 连接和消费者组。

```
conn = redis::connect(host, port)

// 删除 stream (如果存在)
redis::run(conn, "DEL", streamKey)

// msgId="0" 从头开始消费，mkStream=true 自动创建不存在的 stream
redis::createStreamGroup(conn, streamKey, groupName, "0", true)
```

往 Redis stream 中插入 3 条消息。

```
msgId1 = redis::run(conn, "XADD", streamKey, "*", "time", string(now()), "msg", string("XADD_MSG" + rand(10000000000)[0]))
msgId2 = redis::run(conn, "XADD", streamKey, "*", "time", string(now()), "msg", string("XADD_MSG" + rand(10000000000)[0]))
msgId3 = redis::run(conn, "XADD", streamKey, "*", "time", string(now()), "msg", string("XADD_MSG" + rand(10000000000)[0]))
// 查看 stream 内的消息条数
redis::run(conn, "XLEN", streamKey)
```

读取和确认消息。

```
// 读取新消息（readPending=false）
/*
count = 10 最多读取 10 条新消息
readPending = false 不读取待处理消息
maxWaitTime = 0 不等待新消息
writeToPending = true 不自动确认
*/
redis::readStreamGroup(conn, streamKey, groupName, consumerName, 10, ">", 0, true)

// 读取待处理消息（readPending=true）
msgs = redis::readStreamGroup(conn, streamKey, groupName, consumerName, 10, "0")
// 确认消息
redis::ackMessages(conn, streamKey, groupName, keys(msgs))
// 再次读取待处理消息（结果应该为空）
redis::readStreamGroup(conn, streamKey, groupName, consumerName, 10, "0")
```

### 示例 3：异步消费流数据

加载 redis 插件，往 Redis stream 中写入数据。

```
loadPlugin("redis")
// 在一个单独会话中往 stream 中写入数据
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
STREAM_KEY = "test_stream_sub"
GROUP_NAME = "test_group"
CONSUMER_NAME = "consumer1"
ACTION_NAME = "test_action"
conn = redis::connect(REDIS_HOST, REDIS_PORT)
for (i in 1..100000) {
    redis::run(conn, "XADD", STREAM_KEY, "*", "field1", "value_" + string(i), "field2", string(i * 100))
    sleep(10)
}
```

配置订阅信息。

```
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
STREAM_KEY = "test_stream_sub"
GROUP_NAME = "test_group"
CONSUMER_NAME = "consumer1"
ACTION_NAME = "test_action"
conn = redis::connect(REDIS_HOST, REDIS_PORT)
// 清理之前的测试数据（可选）
// redis::run(conn, "DEL", STREAM_KEY)
// redis::run(conn, "XGROUP", "DESTROY", STREAM_KEY, GROUP_NAME)
```

创建消费者组，定义输出表和 `parser` 函数。

```
// 创建消费者组
redis::createStreamGroup(conn, STREAM_KEY, GROUP_NAME, "0", true)

// 定义 输出表
share table(100:0, `msgId`field1`field2`timestamp, [STRING, STRING, STRING, TIMESTAMP]) as outputTable

// 定义 parser 函数，将消息字典转换为表
def msgParser(msgs) {
    msgIds = msgs.keys()
    n = msgIds.size()
    if (n == 0) {
        return table(0:0, `msgId`field1`field2`timestamp, [STRING, STRING, STRING, TIMESTAMP])
    }
    result = table(n:0, `msgId`field1`field2`timestamp, [STRING, STRING, STRING, TIMESTAMP])
    for (msgId in msgIds) {
        fields = msgs[msgId]
        field1 = fields["field1"]
        field2 = fields["field2"]
        insert into result values(msgId, field1, field2, now())
    }
    return result
}
```

启动订阅、查看订阅结果、取消订阅和清理环境。

```
// 启动订阅
redis::subscribeStream(REDIS_HOST, REDIS_PORT, STREAM_KEY, GROUP_NAME, CONSUMER_NAME,
                       outputTable, msgParser, ACTION_NAME, ">", 100, true)
// 查看订阅结果
redis::getSubscriptionStats()
select * from outputTable

// 取消订阅
redis::unsubscribeStream(ACTION_NAME)
redis::getSubscriptionStats()

// 清理环境
redis::release(conn)
undef(`outputTable, SHARED);
```
