<!-- Auto-mirrored from upstream `documentation-main/plugins/opc/opc.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# OPC

OPC 是一项应用于自动化行业及其他行业的数据安全交换可互操作性标准。DolphinDB 的 OPC 插件可用于访问并采集自动化行业 OPC 服务器的数据。OPC DA 插件实现了 OPC DA 2.05A 版本规范。

## 安装插件

### 版本要求

DolphinDB Server：Window、2.00.10 及更高版本。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   **注意**：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("opc")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("opc")
   ```

## 接口说明

目前只支持 OPC 2.0 协议，且不支持异步读写。

### getOpcServerList

**语法**

```
getOpcServerList(host)
```

**详情**

获取 OPC server。

返回的结果是一个包含两列的表，一列是 progID，表示 server 的标志符；另一列是该 server 对应的 CLSID。

**注意**：获取远程 OPC 服务器前，需要对 OPC Server 和 OPC Client 两侧都进行 DCOM 配置。详细配置可参考[远程连接 opc 服务器设置](https://blog.csdn.net/steventian72/article/details/104039459)。

**参数**

**host** STRING 类型标量，表示 IP 地址，如 "127.0.0.1"。

**例子**

```
getOpcServerList("desk9")
```

### connect

**语法**

```
connect(host, serverName，[reqUpdateRateMs=100])
```

**详情**

连接 OPC server。

返回的结果是一个 connection，可以显式的调用 close 函数去关闭，也可以在 reference count 为 0 的时候自动释放。

**注意**：获取远程 OPC 服务器前，需要对 OPC Server 和 OPC Client 两侧都进行 DCOM 配置。详细配置可参考[远程连接 opc 服务器设置](https://blog.csdn.net/steventian72/article/details/104039459)。

**参数**

**host** STRING 类型标量，表示 IP 地址。

**serverName** STRING 类型标量，表示 OPC Server 的名称。

**reqUpdateRateMs** INT 类型标量，表示请求更新频率，单位为毫秒，默认为 100。可选参数。

**例子**

```
connection=connect(`127.0.0.1,`Matrikon.OPC.Simulation.1,100)
```

### readTag

**语法**

```
readTag(conn, tagNames, [outputTables])
```

**详情**

读取一个 tag 的值，使用前需要先建立一个 OPC 连接。

**参数**

**conn** 接口`connect`的返回。

**tagNames** STRING 类型标量或向量，表示 tag 的名称。

**outputTables** 是表或表的数组（为数组时，表的个数须与 tag 个数相同），用于存放读取的结果。

* 若是一个表，将所有 tag 的值都插入这张表中。
* 若是多个表，将每个 tag 读取的值分别插入这些表中。
* 若不指定，则返回一张表，表的记录是读取的 tag 值。

**例子**

```
t = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, DOUBLE, INT])
readTag(conn, "testwrite.test9",t)
readTag(conn, ["testwrite.test5","testwrite.test8", "testwrite.test9"],t)
tm = table(200:0,`time`tag1`quality1`tag2`quality2, [TIMESTAMP,STRING, INT,INT,INT])
readTag(conn, ["testwrite.test1","testwrite.test4"],tm)
t1 = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, STRING, INT])
t2 = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, INT, INT])
t3 = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, DOUBLE, INT])
readTag(conn, ["testwrite.test1","testwrite.test4", "testwrite.test9"],[t1,t2,t3])
```

### writeTag

**语法**

```
writeTag(conn, tagNames, values)
```

**参数**

**conn** 接口`connect`的返回。

**tagNames** STRING 类型标量或向量，表示 tag 的名称。

**values** 表示 tag 的值或数组。

**详情**

写入一个或一组 tag 的值。

**例子**

```
writeTag(conn,"testwrite.test1",[1.112,0.123,0.1234])
writeTag(conn,["testwrite.test5","testwrite.test6"],[33,11])
```

### subscribe

**语法**

```
subscribe(conn, tagNames, handler)
```

**详情**

订阅 tag 的值。

**参数**

**conn** 接口`connect`的返回。

**tagNames** STRING 类型标量或向量，表示 tag 的名称。

**handler** 一个函数或表。当数据变化时，会调用 handler 函数或直接将数据写入 handler 指定的表。

**例子**

```
t1 = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, STRING, INT])
conn1=connect(`127.0.0.1,`Matrikon.OPC.Simulation.1,100)
subscribe(conn1,".testString",  t1)

t2 = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, DOUBLE, INT])
conn2=connect(`127.0.0.1,`Matrikon.OPC.Simulation.1,100)
subscribe(conn2,[".testReal8",".testReal4"],  t2)

def callback1(mutable t, d) {
	t.append!(d)
}
t3 = table(200:0,`tag`time`value`quality, [SYMBOL,TIMESTAMP, BOOL, INT])
conn10 = connect(`127.0.0.1,`Matrikon.OPC.Simulation.1,10)
subscribe(conn10,".testBool",   callback1{t3})
```

### getSubscriberStat

**语法**

```
getSubscriberStat()
```

**详情**

查询所有订阅信息。

返回的结果是一个包含 8 列的表，其结构为：

* subscriptionId, 表示订阅标识符
* user, 表示建立订阅的会话用户
* host, 表示 OPC server 的地址
* serverName, 表示 OPC server 的名称
* tag, 表示订阅标签
* createTimestamp, 表示可以订阅建立时间
* receivedPackets, 表示订阅收到的消息报文数
* errorMsg, 表示订阅的最新错误信息

**参数**

无

**例子**

```
t=getSubscriberStat()for(sub in t[`subscriptionId]){	unsubscribe(sub)}
```

### unsubscribe

**语法**

```
unsubscribe(subscription)
```

**详情**

取消 client 的订阅。

**参数**

**subscription** 接口`connect` 的返回或 `getSubscriberStat` 返回的订阅标识符。

**例子**

```
unsubscribe(connection)
```

### close

**语法**

```
close(connection)
```

**详情**

断开与 OPC server 的连接。

**参数**

**connection** 接口`connect` 的返回。

**例子**

```
close(connection)
```
