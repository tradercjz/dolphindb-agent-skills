<!-- Auto-mirrored from upstream `documentation-main/api/cpp/threadedclient.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# ThreadedClient

ThreadedClient 针对每个订阅新建一个数据处理线程。每当发布端的流数据表产生新数据，其对应的订阅线程即会获取数据并调用回调函数。本小节将从构造函数、订阅和取消订阅对
ThreadedClient 进行介绍，并展示一个使用示例。

## 构造函数

```
ThreadedClient(int listeningPort = 0)
```

其中：`listeningPort` 表示单线程客户端的订阅端口号。

注：

2.00.9 及之后版本的 server 发布端通过订阅端的请求连接推送数据，不再需要接收端指定端口，参数
*listeningPort* 填 0 或者不填即可。若进行指定，则该输入值无效，会被 API 忽略。

## 订阅

```
//订阅接口1：
using MessageHandler = std::function<void(Message)>;
ThreadSP subscribe(
    string host, int port,
    const MessageHandler &handler,
    string tableName,
    string actionName = DEFAULT_ACTION_NAME,
    int64_t offset = -1,
    bool resub = true,
    const VectorSP &filter = nullptr,
    bool msgAsTable = false,
    bool allowExists = false,
    string userName = "",
    string password = "",
    const StreamDeserializerSP &blobDeserializer = nullptr,
    const std::vector<std::string>& backupSites = std::vector<std::string>(),
    int resubTimeout = 100,
    bool subOnce = false
)
//订阅接口2：
using MessageBatchHandler = std::function<void(vector<Message>)>;
ThreadSP subscribe(
    string host, int port,
    const MessageBatchHandler &handler,
    string tableName,
    string actionName = DEFAULT_ACTION_NAME,
    int64_t offset = -1,
    bool resub = true,
    const VectorSP &filter = nullptr,
    bool allowExists = false,
    int batchSize = 1,
    double throttle = 1,
    bool msgAsTable = false,
    string userName = "",
    string password = "",
    const StreamDeserializerSP &blobDeserializer = nullptr,
    const std::vector<std::string>& backupSites = std::vector<std::string>(),
    int resubTimeout = 100,
    bool subOnce = false
)
```

## 参数

* `host`：表示发布端节点的主机名。
* `port`：表示发布端节点的端口号。
* `handler`：表示用户自定义的回调函数，用于处理每次流入的消息。
* `tableName`：表示发布端上共享流数据表的名称。
* `actionName`：表示订阅任务的名称。传入值可以包含字母、数字和下划线。
* `offset`：表示订阅任务开始后的第一条消息所在的位置。消息是流数据表中的行。如果没有指定
  *offset*、或其为负数、或超过了流数据表的记录行数，则订阅将会从流数据表的当前行开始。*offset*
  与流数据表创建时的第一行对应。如果某些行因为内存限制被删除，在决定订阅开始的位置时，这些行仍然考虑在内。
* `resub`：表示订阅中断后，API 是否会自动重订阅。
* `filter`：一个向量，表示过滤条件。流数据表过滤列在 *filter* 中的数据才会发布到订阅端，不在
  *filter* 中的数据不会发布。
* `msgAsTable`：只有设置了 *batchSize* 参数，该参数才会生效。若其设置为
  true，则订阅的数据会转换为 Table；若其设置为 false，则订阅的数据会转换成 AnyVector。
* `allowExists`：若该参数设置为 true，则支持对同一个订阅流表使用多个 *handler*
  处理数据；若其设置为 False，则不支持同一个订阅流表使用多个 *handler* 处理数据。
* `batchSize`：表示批处理的消息的数量。如果该参数是正数，则直到消息的数量达到 *batchSize*
  时，*handler* 才会处理进来的消息；如果其未指定或者是非正数，则消息到达后，handler 会立刻处理消息。
* `throttle`：表示 *handler* 处理到达的消息之前等待的时间，以秒为单位。默认值为
  1。如果没有指定 *batchSize*，则 *throttle* 将不会起作用。
* `userName`：表示 API 所连接服务器的登录用户名。
* `password`：表示 API 所连接服务器的登录密码。
* `blobDeserializer`：表示订阅的异构流表对应的反序列化器。
* `backupSites`: 字符串列表，可选，表示备用的发布端节点列表，由节点 ip 和端口号组成，例如
  [“192.168.0.1:8848“, “192.168.0.2:8849“]。
  + 指定*backupSites*，表示启动主备节点切换。如果发生节点切换（例如连接断开），会在可用节点列表中不断轮询订阅，直至订阅成功。
  + 若配置该参数，用户需保证主节点（由 host 和 port
    参数指定）和备用节点上存在相同结构、相同数据的同名流数据表。否则，可能出现订阅的数据不符合预期。
  + 若订阅的是高可用流表，重连时将从 *backupSites* 指定的节点列表中选择节点。
  + 取消订阅需使用主节点 ip 和端口号进行取消。
* `resubTimeout`：一个整数，表示重订阅距离断线最小时间间隔，默认值为 100 毫秒。
* `subOnce`：布尔值，False表示在节点切换时，不去尝试之前成功连接过的节点。默认值为 False。

接口区别说明

订阅接口1每收到一条消息就回调一次，而订阅接口2则存在一个缓存机制，由batchSize和throttle来约束，满足条件时才会进行回调，每次回调可能包含多条消息。

返回类型

ThreadSP 指向循环调用 *handler* 的线程的指针。该线程在此 topic
被取消订阅后会自动退出。

## 取消订阅

`void unsubscribe( string host, int
port, string tableName, string actionName
)`

参数值需要与订阅时的填入参数值相同。

## 使用示例

本例使用2.00.10版本的DolphinDB server

**DolphinDB 脚本**：新建一个 Stream 表，然后共享该表，名为`shared_stream_table`。

```
rt = streamTable(`XOM`GS`AAPL as id, 102.1 33.4 73.6 as x)
share rt as shared_stream_table
```

**C++代码**：从头订阅`shared_stream_table`，等待10秒后取消订阅。若在这10秒中发布端向`shared_stream_table`内追加数据，则订阅端可以实时得到数据。

```
#include <iostream>
#include "Streaming.h"
using namespace dolphindb;

int main(int argc, const char **argv)
{
    auto batchHandler = [](std::vector<Message> msgs){
        std::cout << "receive " << msgs.size() << " msgs\n";
        for(auto& msg : msgs){
            std::cout << msg->getString() << std::endl;
        }
    };
    ThreadedClient client(0);
    ThreadSP t = client.subscribe("127.0.0.1", 8848, batchHandler, "shared_stream_table", "action1", 0, true, nullptr, false, 3, 1.0);
    sleep(10);
    client.unsubscribe("127.0.0.1", 8848, "shared_stream_table", "action1");
    return 0;
}
```
