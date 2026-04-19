<!-- Auto-mirrored from upstream `documentation-main/tutorials/redis_plugin_tutorial.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Redis 插件使用教程

DolphinDB 是一个高性能的分布式数据库。通过 Redis 插件，DolphinDB 用户可以轻松地与 Redis 数据库进行交互。用户不仅可以从 DolphinDB 向 Redis 发送数据，实现高速的数据写入操作；还可以从 Redis 读取数据，将实时数据流集成到 DolphinDB 中进行分析和处理。这种集成提供了一种强大的工具，用于构建高效且可扩展的实时数据处理和分析应用程序，以满足当今数据驱动决策环境中对速度和灵活性的严格要求。

本文主要介绍如何使用 DolphinDB 的 Redis 插件进行 Redis 数据库的数据写入和读取，并提供实际使用案例。本文中的代码需要运行在 DolphinDB Server 2.00.10 或更高版本以及对应插件上，且支持 Linux 和 Windows 系统。

## 1. Redis 数据库介绍

Redis 是一个开源的高性能键值数据库，以其快速的数据操作和丰富的数据结构支持而广受欢迎。基于内存运行的 Redis 具有极高的读写速度。Redis 通过持久化存储功能确保数据的安全性和可靠性。其灵活的数据结构支持包括字符串（String）、列表（List）、集合（Set）、有序集合（Sorted Set）、哈希表（Hash）等，使其能够应用于从简单的缓存系统到复杂的实时数据处理系统的各种应用场景。

Redis 中的字符串可以被视为最简单的数据类型，是其他所有类型的基础。String 类型是二进制安全的，即 Redis 的字符串可以包含任何数据，比如图像或序列化对象的二进制数据。例如整数和浮点数在 Redis 内部以字符串形式存储，当使用命令如 `SET key 100` 时，虽然存储的是一个数值，实际上是将数值`100`转换成等效的字符串 "100" 并存储它。

## 2. 基本使用说明

### 2.1 安装与加载

Redis 插件目前可以在 2.00.10 版本及以后的 DolphinDB Server 通过插件市场进行安装。节点启动后，连接节点并在 GUI（或 VS Code、Web UI）等 DolphinDB 客户端中执行 `installPlugin` 函数，则可以下载与当前 server 版本适配的 Redis 插件文件，插件文件包括插件描述文件及插件的二进制文件。

```
installPlugin("redis")
```

在脚本中调用插件相关的接口前，需要先加载插件，在 GUI（或 VS Code、Web UI）等客户端中执行 `loadPlugin("Redis")` 即可完成加载。

### 2.2 基础接口使用说明

Redis 插件提供的主要功能包括：建立与 Redis 服务器的连接、对 Redis 数据库进行读取和写入操作、连接状态监控、操作结束后关闭连接，具体示例如下：

通过 `connect` 接口建立连接，得到连接句柄。

```
conn = redis::connect("<IPAddr>", 6379)
```

通过 `run` 接口执行 Redis 命令，如 "AUTH", "GET", "SET" 等。

```
// 使用 "GET" 命令读取键 "key" 的值
val = redis::run(conn, "GET", "key")

// 使用 "HGET" 命令从名称为 "id" 的哈希表中读取键 "key" 的值
val = redis::run(conn, "HGET", "id", "key")
```

此外，对于批量写入操作，Redis 插件还提供了 `batchSet、batchHashSet` 等高性能的批量写入接口进行优化。

通过 `getHandleStatus` 接口可以获得连接状态表。

```
status = redis::getHandleStatus()
```

返回结果如下，可以看到表中有 token、address、createdTime 三列。其中 token 是连接的标识，`getHandle` 接口可以通过该 token 获取连接句柄；address 连接的 Redis server 的 "ip:port" 网络地址；createdTime 是该连接创建的时间，如下图：

![](images/redis_plugin_tutorial/%E5%9B%BE2_1.png)

操作结束后通过 `release` 接口关闭特定的连接。

```
redis::release(conn)
```

或者通过 `releaseAll` 接口关闭全部已建立的连接。

```
redis::releaseAll()
```

此外 Redis 插件还提供了 `getHandle` 接口用于获取特定连接句柄，因为通过 `redis::connect` 接口建立的连接并不会随着 DolphinDB 的会话结束而自动释放。

```
redis::getHandle(token)
```

其中参数 token 是通过 `getHandleStatus` 接口获取的连接的 id。

插件使用的详细内容请参考 Redis 插件文档

### 2.3 数据类型转换

因为在 Redis 中存储的键和值实际上都是以字符串的形式保存的，所以 Redis 插件提供的 `run`、`batchSet`、`batchHashSet` 接口传入的键和值都是 DolphinDB 的 STRING 类型。如果使用其他类型的数据，需要调用 DolphinDB 的 `string` 函数先将其转为字符串类型再使用。

## 3. 案例演示

### 3.1 案例1

本小节以将行情插件实时订阅的行情数据实时写入 Redis 数据库为例，对 Redis 插件的使用进行说明，整体流程如下图：

![](images/redis_plugin_tutorial/%E5%9B%BE3_1.png)

通过 DolphinDB 的众多行情插件，您可以非常方便高效地将实时行情数据写入 DolphinDB 分布式数据库。本文不关注如何订阅实时行情到 DolphinDB 数据库，该部分可参考 MDL 行情插件 和 amdQuote 行情插件 等行情类插件教程。

通过 `submitJob` 提交一个 Redis 写入作业，每 500ms 执行一次 `redisjob` 自定义函数，将订阅的最新行情数据更新到 Redis 数据库。

```
def submitByHalfSecond(){
    do {
        redisjob()
        sleep(500)
    } while(true)
}
submitJob("submitByHalfSecond", "submitByHalfSecond", submitByHalfSecond)
```

函数 `redisjob` 中首先通过 `connect` 接口建立起到 Redis 数据库的连接，然后通过 `run` 接口执行 Redis AUTH 命令来登录。数据表 CFFEX\_PRICE 和 CZCE\_PRICE 由行情插件实时订阅写入，数据内容类似下图：

![](images/redis_plugin_tutorial/%E5%9B%BE3_2.png)

然后通过 SQL 语句 `context by id order by time_stamp limit -1` 过滤，获取行情数据表中每个 id 的最新一条行情数据，如下图：

![](images/redis_plugin_tutorial/%E5%9B%BE3_3.png)

获取到要更新的数据后，用 `saveHashDataToRedis` 自定义函数将最新数据写入 Redis 数据库，完成后调用 `release` 释放连接。

```
def redisjob(){
    conn=redis::connect(host, port)
    redis::run(conn, "AUTH", "password")
    go

    // 获取每个 id 对应的最新时间的行情数据
    cffex_data = select * from loadTable("dfs://CFFEX", "CFFEX_PRICE") context by id order by time_stamp limit -1
    czce_data = select * from loadTable("dfs://CZCE", "CZCE_PRICE") context by id order by time_stamp limit -1

    saveHashDataToRedis(conn, cffex_data)
    saveHashDataToRedis(conn, czce_data)

    redis::release(conn)
}
```

函数 `saveHashDataToRedis` 中使用了 `batchHashSet` 接口，批量高效地执行 Redis 的 HSET 操作。

接口 `batchHashSet` 的第二个参数是一个 String 类型数组，每一个元素作为 HSET 中的一个 key 对应 fieldData 表中的一行数据；第三个参数是一个每列都是 String 类型的表，每列列名作为 Redis HSET 中的 field，值作为 HSET 中的 value。

```
def saveHashDataToRedis(conn, tb){
    id = exec id from tb
    // 通过 string 函数将数据转为 string 类型
    data = select string(time_stamp) as time_stamp, exchange, string(last_price) as last_price,
        string(volume) as volume, string(bid_price1) as bid_price1, string(bid_volume1) as bid_volume1,
        string(bid_price2) as bid_price2, string(bid_volume2) as bid_volume2, string(bid_price3) as bid_price3,
        string(bid_volume3) as bid_volume3, string(bid_price4) as bid_price4, string(bid_volume4) as bid_volume4,
        string(bid_price5) as bid_price5, string(bid_volume5) as bid_volume5, string(ask_price1) as ask_price1,
        string(ask_volume1) as ask_volume1, string(ask_price2) as ask_price2, string(ask_volume2) as ask_volume2,
        string(ask_price3) as ask_price3, string(ask_volume3) as ask_volume3, string(ask_price4) as ask_price4,
        string(ask_volume4) as ask_volume4, string(ask_price5) as ask_price5, string(ask_volume5) as ask_volume5
        from tb

    redis::batchHashSet(conn, id, data)
}
```

之后可以通过 HGET 查看已写入的数据，例如查看 id 为 “id01” 哈希表的 ”time\_stamp“ 字段的值：

```
redis::run(conn, "HGET", "id01", "time_stamp")
```

![](images/redis_plugin_tutorial/%E5%9B%BE3_4.png)

至此，已经成功将实时订阅的行情数据写入到 Redis 数据库中。

### 3.2 案例2

该案例展示了如何结合 DolphinDB 的流订阅功能，将流数据表订阅的数据实时写入 Redis 服务器中。

1. 通过 DolphinDB 的 `streamTable` 函数创建流数据表，然后使用 `enableTableShareAndPersistence` 函数将该流数据表共享并持久化到磁盘上。

   ```
   colName=["key", "value"]
   colType=["string", "string"]
   enableTableShareAndPersistence(table=streamTable(100:0, colName, colType),
     tableName=`table1, cacheSize=10000, asynWrite=false)
   ```
2. 调用 `subscribeTable` 函数订阅流数据表，并通过自定义的 `myHandle` 函数来处理订阅数据，该函数调用 `batchSet` 接口将订阅的数据实时写入 Redis 数据库中。

   ```
   def myHandle(conn, msg) {
   	redis::batchSet(conn, msg[0], msg[1])
   }
   conn = redis::connect(host, port)
   subscribeTable(tableName="table1", handler=myHandle{conn})
   ```
3. 插入数据到流数据表中，流数据表订阅到数据后会调用 `myHandle` 自定义函数。

   ```
   n = 1000000
   for(x in 0:n){
   	insert into table1 values("key" + x, "value" + x)
   }
   ```
4. 通过 `run` 接口执行 GET 命令将刚才写入 Redis 数据库的数据插入到内存表中，查看表中数据说明之前已经成功写入数据到 Redis 数据库中。

   ```
   t = table(n:0, [`id, `val], [`string, `string])
   for(x in 0:n){
   	insert into t values("key" + x, redis::run(conn, "GET", "key" + x))
   }
   ```

## 4. 总结

本文介绍了 DolphinDB Redis 插件，并通过具体的将订阅的实时行情数据写入 Redis 数据库的例子说明了插件的使用方法，为 DolphinDB 与 Redis 数据库数据交互提供了演示案例。

## 附录

### 1. 脚本文件

[案例1](script/redis_plugin_tutorial/example1.txt)

[案例2](script/redis_plugin_tutorial/example2.txt)

### 2. 常见问题

* 如果重复执行 `loadPlugin` 加载插件，会抛出模块已经被使用的错误提示 `"The module [Redis] is already in use."`，因为节点启动后，只允许加载一次 Redis 插件，即可在任意会话中调用该插件提供的函数。
  可以通过 `try-catch` 语句捕获这个错误，避免因为插件已加载而中断后续脚本代码的执行。

  ```
  try{
      loadPlugin("./plugins/Redis/PluginRedis.txt")
  } catch(ex) {
      print ex
  }
  ```
* 如果一个连接句柄在使用中报错，那么该连接不能再被使用，应该使用 `redis::release` 接口释放掉该出错的句柄，并使用 `redis::connect` 接口建立一个新的连接。如果继续使用之前的连接，会一直报同样的报错，这是使用的 [hiredis](https://github.com/redis/hiredis) 第三方库的限制：`"Once an error is returned the context cannot be reused and you should set up a new connection."`
* 如果遇到 `"[Plugin::Redis] Redis reply error: NOAUTH Authentication required."` 报错，说明 Redis 服务器设置了密码，需要通过 AUTH 命令认证，脚本如下：

  ```
  conn = redis::connect(host, port)
  redis::run(conn, "AUTH", "password")
  ```

  ​
