<!-- Auto-mirrored from upstream `documentation-main/api/python/BasicOperations/Subscription/Subscription.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 2.00.9 及之后的版本，开启订阅，无需指定端口
s.enableStreaming()
```

**注意**：若同时升级 API 和 Server 至 2.00.9 及之后的版本，须在升级前先取消订阅，完成升级后再重新订阅。

## 订阅

使用 `subscribe` 方法订阅 DolphinDB 中的流数据表，接口示例如下：

```
subscribe(host, port, handler, tableName, actionName=None, offset=-1, resub=False,
          filter=None, msgAsTable=False, batchSize=0, throttle=1.0,
          userName=None, password=None, streamDeserializer=None, backupSites=None,
          resubTimeout=100, subOnce=False)
```

### 参数介绍

#### 连接参数： *host*, *port*, *userName*, *password*, *backupSites*

* **host** ：字符串，必填，表示发布端节点的 IP 地址。
* **port** ：字符串，必填，表示发布端节点的端口号。
* **userName** ：字符串，可选，表示所连接 DolphinDB 的登录用户名。
* **password** ：字符串，可选，表示所连接 DolphinDB 的登录用户名对应的密码。
* **backupSites** ：字符串，可选，字符串列表，表示备用的发布端节点列表，由节点 ip 和端口号组成，例如 ["192.168.0.1:8848", "192.168.0.2:8849"]。

  + 指定 *backupSites*，表示启动主备节点切换。如果发生节点切换（例如连接断开），会在可用节点列表中不断轮询订阅，直至订阅成功。
  + 若配置该参数，用户需保证主节点（由 *host* 和 *port* 参数指定）和备用节点上存在相同结构、相同数据的同名流数据表。否则，可能出现订阅的数据不符合预期。
  + 若订阅的是高可用流表，重连时将从 *backupSites* 指定的节点列表中选择节点。
  + 取消订阅需使用主节点 IP 和端口号进行取消。

#### 回调参数： *handler*

* **handler** ：用户自定义的回调函数，用于处理每次流入的数据。

下例定义了一个简单的回调函数：

```
def handler(msg):
    print(msg)
```

#### 订阅参数：*tableName*, *actionName*, *offset*, *resub*, *filter*, *resubTimeout*, *subOnce*

* **tableName** ：表示发布表的名称。
* **actionName** ：表示订阅任务的名称。

  + 订阅时，订阅主题由订阅表所在节点的别名、流数据表名称和订阅任务名称组合而成，使用“/”分隔。注意，如果订阅主题已经存在，将会订阅失败。
* **offset** ：整数，表示订阅任务开始后的第一条消息所在的位置。消息即为流数据表中的行。

  + 若该参数未指定，或设为 -1，订阅将会从流数据表的当前行开始。
  + 若该参数设为 -2，系统会获取持久化到磁盘上的 offset，并从该位置开始订阅。其中，offset 与流数据表创建时的第一行对应。如果某些行因为内存限制被删除，在决定订阅开始的位置时，这些行仍然考虑在内。
* **resub** ：布尔值，表示订阅中断后，API 是否进行自动重订阅。默认值为 False，表示不会自动重订阅。
* **filter** ：一个数组，表示过滤条件。在流数据表过滤列中，只有符合 *filter* 过滤条件的数据才会发布到订阅端。
* **resubTimeout** ：一个非负整数，表示在检测到连接断开后，经过多长时间开始尝试重新连接（单位毫秒），默认值为 100。
* **subOnce** ：布尔值，表示节点在切换重连时，同一个节点是否只能被订阅一次。

  + 默认为 False：节点被订阅后，再次进行重连时，该节点仍可参与后续的切换重连。
  + 若设置为 True：节点被订阅后，若发生了节点切换，该节点将不再参与后续的切换重连。

  当订阅单个节点，且 *resub*=true 时，该参数不生效。

#### 模式参数：*msgAsTable*, *batchSize*, *throttle*, *streamDeserializer*

* **msgAsTable** ：布尔值。若该参数设置为 True，表示订阅的数据将会转换为 DataFrame 格式。须注意，只有设置了参数 *batchSize*，参数 *msgAsTable* 才会生效。**注意**：若设置了 *streamDeserializer*，则参数 *msgAsTable* 必须设置为 False。
* **batchSize** ：整数，表示批处理的消息的数量。
  + 如果该参数是正数：
    - 设置 `msgAsTable = False` 时，直到消息的数量达到 *batchSize* 时，*handler* 才会处理进来的 *batchSize* 条消息，并返回一个 list，其中每一项都是单条数据。
    - 设置 `msgAsTable = True` 时，回调参数 *handler* 将基于消息块（由 DolphinDB 中的参数 *maxMsgNumPerBlock* 进行配置）处理消息。当收到的记录总数大于等于 *batchSize* 时，*handler* 将处理所有达到条件的消息块。举例说明：若设置 `batchSize = 1500`，API 收到 DolphinDB 发送的第一个消息块（包含 1024 条记录），1024<1500，*handler* 将不处理消息；API 收到第 2 个消息块（包含 500 条记录），此时，1024+500>1500，即两个消息块中包含的记录数大于 *batchSize*，*handler* 将开始处理这两个消息块中的 1524 条记录。
  + 如果该参数是非正数或者未被指定，消息到达之后，*handler* 将立刻逐条处理消息，返回的数据将为单条数据组成的 list。
* **throttle** ：浮点数，表示 *handler* 处理到达的消息之前等待的时间。单位为秒，默认值为 1.0。如果未指定 *batchSize*，参数 *throttle* 将无法产生作用。
* **streamDeserializer** ：表示订阅的异构流表对应的反序列化器。

**注意：** 订阅流表时，参数 *batchsize*、*msgAsTable*、*streamDeserializer* 的值都将影响传入回调函数 *handler* 中变量的格式，各种参数的订阅示例请参考章节流订阅。

### 订阅示例

先在 DolphinDB 中创建共享的流数据表，指定进行过滤的列为 sym，并向 5 个 symbol 各插入 2 条记录，共 10 条记录：

```
share streamTable(10000:0,`time`sym`price`id, [TIMESTAMP,SYMBOL,DOUBLE,INT]) as trades
setStreamTableFilterColumn(trades, `sym)
insert into trades values(take(now(), 10), take(`000905`600001`300201`000908`600002, 10), rand(1000,10)/10.0, 1..10)
```

在 Python API 中，首先指定订阅端口号并启用流订阅（ 本例中使用 1.30.x 和 2.00.9 之前版本的 DolphinDB，故需要指定订阅端口号），然后定义回调函数 *handler* 。再调用 `subscribe` 方法开启流订阅，其中设置 `offset=-1`，`filter=np.array(["000905"])`。最后通过 `Event().wait()` 的方式阻塞主线程，保持进程不退出。

```
import dolphindb as ddb
import numpy as np
s = ddb.session()
s.enableStreaming(0) # DolphinDB 的版本为 1.30.x 或小于 2.00.9 时，需指定端口

def handler(lst):
    print(lst)

s.subscribe("192.168.1.113", 8848, handler, "trades", "action", offset=-1, filter=np.array(["000905"]))

from threading import Event
Event().wait()          # 阻塞主线程，保持进程不退出
```

执行脚本，发现此时没有流数据被打印出来。该情况是由于 offset 设置为 -1，表示订阅将会从流数据表的当前行开始，因此 DolphinDB `insert into` 命令中包含的数据将不会发送到流订阅客户端。

在 DolphinDB 中再次执行同一脚本：

```
insert into trades values(take(now(), 10), take(`000905`600001`300201`000908`600002, 10), rand(1000,10)/10.0, 1..10)
```

此时 Python 进程开始打印收到的流数据，输出内容如下：

```
[numpy.datetime64('2023-03-17T10:11:19.684'), '000905', 69.3, 1]
[numpy.datetime64('2023-03-17T10:11:19.684'), '000905', 96.5, 6]
```

在 API 收到的数据中，由于 *filter* 参数生效，故打印结果中仅保留了 `sym="000905"`的数据，其余数据都被过滤掉。

## 获取订阅主题

通过 `getSubscriptionTopics` 方法可以获取当前 session 中的所有订阅主题。主题的构成方式是：`host/port/tableName/actionName`，每个 session 的主题互不相同。

使用示例如下：

```
s.getSubscriptionTopics()
```

示例的输出结果如下所示：

```
['192.168.1.113/8848/trades/action']
```

## 取消订阅

使用 `unsubscribe` 方法可以取消订阅，接口如下：

```
unsubscribe(host, port, tableName, actionName=None)
```

取消示例中的订阅：

```
s.unsubscribe("192.168.1.113", 8848, "trades", "action")
```
