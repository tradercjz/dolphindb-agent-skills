<!-- Auto-mirrored from upstream `documentation-main/plugins/zmq/zmq.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# zmq

ZeroMQ (zmq) 是一个高性能异步消息库，能够支持可伸缩的分布式或并发应用程序设计。与面向消息的中间件不同，zmq 可以在无需专门消息代理的情况下运行。其名称中的 "Zero" 代表零代理。更多详细信息可参考 [ZeroMQ](https://zeromq.org/) 官方文档。

通过 DolphinDB 的 zmq 插件，用户可以创建 zmq socket，实现 zmq 消息通信的常见操作，包含：

* 通过请求应答机制的会话建立。
* 实现发布/订阅功能。
* 完成消息的管道传输。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本。

支持 Linux-x86、Linux ARM。

### 安装步骤

1. 在 DolphinDB 客户端中通过 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("zmq")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("zmq")
   ```

## 消息发送相关接口说明

### socket

**语法**

```
zmq::socket(type, formatter, [batchSize], [prefix])
```

**详情**

创建一个 zmq socket。

**注意**：

对 `connect`, `bind`, `send`, `close` 接口进行并发操作时，需要为各线程创建不同的 zmq socket 连接句柄。

**参数**

**type** STRING 类型标量，表示要创建的 socket 类型，取值为 "ZMQ\_PUB" 或 "ZMQ\_PUSH"。

**formatter** 一个函数，用于指定发布的数据的打包格式，目前 zmq 插件自带 CSV 或 JSON 两种格式，分别由 `createJSONFormatter` 或 `createCSVFormatter` 创建。也可以自行创建自定义的格式函数，输入参数是 `zmq::send` 的参数 *data*。

**batchSize** INT 类型标量，表示每次发送的记录行数。当待发布内容是一个表时，可以进行分批发送。

**prefix** STRING 类型标量，表示发送前缀。

**例子**

```
formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
```

### connect

**语法**

```
zmq::connect(socket, address, [prefix])
```

**详情**

进行 zmq 的 socket 连接，将 socket 连接到远端节点上，然后开始接收该端点上的传入连接。tcp 建立连接后会保活，使得网络断开又恢复后可以自动重连。

**参数**

**socket** zmq 连接句柄。

**address** STRING 类型标量，表示 socket 连接到的远端地址，格式为 "transport://address:port"。其中，transport 表示要使用的底层协议，取值为 tcp, ipc, inproc, pgm 或 epgm；address:port 表示远端的 IP 地址和端口号。

**prefix** STRING 类型标量，表示发送前缀。

**例子**

```
formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
zmq::connect(socket, "tcp://localhost:55632", "prefix1")
```

### bind

**语法**

```
zmq::bind(socket, address, [prefix])
```

**详情**

绑定 socket，接收发来的链接请求。

**参数**

**socket** zmq 连接句柄。

**address** STRING 类型标量，表示 socket 绑定的地址，格式为 "transport://address:port"。其中，transport 表示要使用的底层协议，取值为 tcp, ipc, inproc, pgm 或 epgm；address:port 表示进行绑定的地址和端口号，若指定为 \*:port，则表示同一个服务器的所有 IP。

**prefix** STRING 类型，表示发送前缀。

**例子**

```
formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
zmq::bind(socket, "tcp://*:55631", "prefix1")
```

### send

**语法**

```
zmq::send(socket, data, [prefix])
```

**详情**

发送一条 zmq 消息。如果发送成功，则返回 true。

**参数**

**socket** zmq 连接句柄。

**data** 发送的数据，类型应与创建 `zmq::socket` 时传入的 *formatter* 参数类型保持一致。否则在调用 *formatter* 进行数据格式化时,可能会抛出异常。

**prefix** STRING 类型标量，表示消息前缀。

**例子**

```
formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
zmq::connect(socket, "tcp://localhost:55632", "prefix1")
zmq::send(socket, table(1..10 as id))
```

### close

**语法**

```
zmq::close(socket)
```

**详情**

关闭一个 zmq 连接句柄。

**参数**

**socket** zmq 连接句柄。

**例子**

```
formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
zmq::connect(socket, "tcp://localhost:55632", "prefix1")
zmq::close(socket)
```

## 订阅相关接口说明

### createSubJob

**语法**

```
zmq::createSubJob(address, type, isClientMode, handler, parser, [prefix])
```

**详情**

创建一个 zmq 订阅，且满足网络断线重连后，订阅也自动重连。

**参数**

**address** STRING 类型标量，格式为 "transport://address:port"。其中，transport 表示要使用的底层协议，取值为 tcp, ipc, inproc, pgm 或 epgm；address:port 表示 zmq 绑定的地址和端口。

**type** STRING 类型标量，表示 zmq 的 socket 类型，取值为 "ZMQ\_SUB" 或 "ZMQ\_PULL"。

**isClientMode** BOOL 类型标量，表示是否是对 *address* 进行连接，如果为否，则对 *address* 进行绑定。

**handler** 一个函数或表，用于处理从 zmq 接收的消息。

**parser** 一个函数，用于对发布的数据进行解包。目前 zmq 插件提供2种解包方式：`createJSONParser` 或 `createCSVParser`。输入参数是一个 STRING 类型的标量，输出结果是一个表。

**prefix** STRING 类型标量，表示消息前缀。

**例子**

```
handler = streamTable(10:0, [`int], [INT])
enableTableShareAndPersistence(table=handler, tableName=`test1, asynWrite=true, compress=true, cacheSize=10000000, retentionMinutes=120)
parser = zmq::createJSONParser([INT], [`bool])
zmq::createSubJob("tcp://localhost:55633", "ZMQ_SUB", true, handler, parser, "prefix1")
```

**与之搭配的 python 脚本**

```
import zmq
import time
import sys

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:55633")
msg = '[{"bool":234}]'

while True:
	socket.send(msg.encode('utf-8'))
	time.sleep(2)
```

### getSubJobStat

**语法**

```
zmq::getSubJobStat()
```

**详情**

查询所有 zmq 订阅信息。返回一个表，包含如下字段：

* subscriptionId：表示订阅标识符。
* addr：zmq 订阅地址。
* prefix：zmq 订阅前缀。
* recvPackets：zmq 订阅收到的消息报文数。
* createTimestamp：表示订阅建立时间。

**例子**

```
handler = streamTable(10:0, [`int], [INT])
enableTableShareAndPersistence(table=handler, tableName=`test1, asynWrite=true, compress=true, cacheSize=10000000, retentionMinutes=120)
parser = zmq::createJSONParser([INT], [`bool])
zmq::createSubJob("tcp://localhost:55633", "ZMQ_SUB", handler, parser, "prefix1")
zmq::getSubJobStat()
```

### cancelSubJob

**语法**

```
zmq::cancelSubJob(subscription)
```

**详情**

关闭一个 zmq 订阅。

**参数**

**subscription** 是 `createSubJob` 函数返回的值或 `getJobStat` 返回的订阅标识符。

**例子**

```
zmq::cancelSubJob(sub1)
zmq::cancelSubJob(42070480)
```

### createPusher

**语法**

```
zmq::createPusher(socket, dummyTable)
```

**详情**

创建一个 zmq 的 pusher，注入该 pusher 的数据将被推送出去。支持两种用法：

* 通过 `append!` 方法追加数据至 pusher。
* 流数据引擎输出表（outputTable）数据注入 pusher。

**参数**

**socket** zmq 连接句柄。

**dummyTable** 一个表对象，用于接收注入的数据。

**例子**

```
share streamTable(1000:0, `time`sym`volume, [TIMESTAMP, SYMBOL, INT]) as trades
output1 = table(10000:0, `time`sym`sumVolume, [TIMESTAMP, SYMBOL, INT])

formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
zmq::connect(socket, "tcp://localhost:55632")
pusher = zmq::createPusher(socket, output1)

engine1 = createTimeSeriesEngine(name="engine1", windowSize=60000, step=60000, metrics=<[sum(volume)]>, dummyTable=trades, outputTable=pusher, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50, useWindowStartTime=false)
subscribeTable(tableName="trades", actionName="engine1", offset=0, handler=append!{engine1}, msgAsTable=true);

insert into trades values(2018.10.08T01:01:01.785,`A,10)
insert into trades values(2018.10.08T01:01:02.125,`B,26)
insert into trades values(2018.10.08T01:01:10.263,`B,14)
insert into trades values(2018.10.08T01:01:12.457,`A,28)
insert into trades values(2018.10.08T01:02:10.789,`A,15)
insert into trades values(2018.10.08T01:02:12.005,`B,9)
insert into trades values(2018.10.08T01:02:30.021,`A,10)
insert into trades values(2018.10.08T01:04:02.236,`A,29)
insert into trades values(2018.10.08T01:04:04.412,`B,32)
insert into trades values(2018.10.08T01:04:05.152,`B,23)
```

### setMonitor

**语法**

```
zmq::setMonitor(enabled)
```

**详情**

是否启用监视日志。启用后，ZMQ 的以下事件将写入 INFO 级别的 log：新建连接、连接重连、端口绑定、连接断开。

**参数**

**enabled** 布尔值，表示是否开启 ZeroMQ 监视日志。若设置为 true，则会启用监视日志。

## 打/解包功能相关接口

### createCSVFormatter

**语法**

```
zmq::createCSVFormatter([format], [delimiter], [rowDelimiter])
```

**详情**

创建一个 CSV 格式的 Formatter 函数。

**参数**

**format** STRING 类型向量。

**delimiter** 列之间的分隔符，默认是','。

**rowDelimiter** 行之间的分隔符，默认是';'。

**例子**

```
MyFormat = take("", 5)
MyFormat[2] = "0.000"
f = createCSVFormatter(MyFormat, ',', ';')
```

### createCSVParser

**语法**

```
zmq::createCSVParser(colTypes, [delimiter], [rowDelimiter])
```

**详情**

创建一个 CSV 格式的 Parser 函数。

**参数**

**colTypes** 一个包含各列数据类型的向量。

**delimiter** 列之间的分隔符，默认是','。

**rowDelimiter** 行之间的分隔符，默认是';'。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
f = zmq::createCSVFormatter([BOOL,CHAR,SHORT,INT,LONG,DATE,MONTH,TIME,MINUTE,SECOND,DATETIME,TIMESTAMP,NANOTIME,NANOTIMESTAMP,FLOAT,DOUBLE,STRING,SYMBOL])
s=f(t)
p = zmq::createCSVParser([BOOL,CHAR,SHORT,INT,LONG,DATE,MONTH,TIME,MINUTE,SECOND,DATETIME,TIMESTAMP,NANOTIME,NANOTIMESTAMP,FLOAT,DOUBLE,STRING,SYMBOL])
p(s)
```

### createJSONFormatter

**语法**

```
zmq::createJSONFormatter()
```

**详情**

创建一个 JSON 格式的 Formatter 函数。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
f = zmq::createJSONFormatter()
f(t)
```

### createJSONParser

**语法**

```
zmq::createJSONParser(colTypes, colNames)
```

**详情**

创建一个 JSON 格式的 Parser 函数。

**参数**

**colTypes** 一个向量，表示各列的数据类型。

**colNames** 一个向量，表示列名。

**例子**

```
def createT(n) {
    return table(take([false, true], n) as bool, take('a'..'z', n) as char, take(short(-5..5), n) as short, take(-5..5, n) as int, take(-5..5, n) as long, take(2001.01.01..2010.01.01, n) as date, take(2001.01M..2010.01M, n) as month, take(time(now()), n) as time, take(minute(now()), n) as minute, take(second(now()), n) as second, take(datetime(now()), n) as datetime, take(now(), n) as timestamp, take(nanotime(now()), n) as nanotime, take(nanotimestamp(now()), n) as nanotimestamp, take(3.1415, n) as float, take(3.1415, n) as double, take(`AAPL`IBM, n) as string, take(`AAPL`IBM, n) as symbol)
}
t = createT(100)
f = zmq::createJSONFormatter()
p = createJSONParser([BOOL,CHAR,SHORT,INT,LONG,DATE,MONTH,TIME,MINUTE,SECOND,DATETIME,TIMESTAMP,NANOTIME,NANOTIMESTAMP,FLOAT,DOUBLE,STRING,SYMBOL],
`bool`char`short`int`long`date`month`time`minute`second`datetime`timestamp`nanotime`nanotimestamp`float`double`string`symbol)
s=f(t)
x=p(s)
```

## 完整例子

```
loadPlugin("zmq")
go
formatter = zmq::createJSONFormatter()
socket = zmq::socket("ZMQ_PUB", formatter)
zmq::bind(socket, "tcp://localhost:55632")
data = table(1..10 as id, take(now(), 10) as ts, rand(10, 10) as volume)
zmq::send(socket, data)
```

**与之搭配的 python 脚本**

```
import zmq
from zmq.sugar import socket
import json
if __name__=='__main__':
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    socket.setsockopt(zmq.TCP_KEEPALIVE, 1);
    socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 30);
    socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 1);
    socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 5);

    socket.connect("tcp://192.168.0.48:55632")
    zip_filter = ""
    socket.setsockopt(zmq.SUBSCRIBE, zip_filter.encode('ascii'))

    while True:
        recvStr = socket.recv()
        print (recvStr)
```
