<!-- Auto-mirrored from upstream `documentation-main/plugins/opcua/opcua.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# OPCUA

OPC 是自动化行业与其他行业用于数据安全交换的互操作性标准。OPC DA 只可用于 Windows 操作系统，OPC UA 则可以独立于平台。本插件实现了 DolphinDB 与 OPC UA 服务器之间的数据传输，可以连接、查看以及读取写入信息。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x86-64, Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456");
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("opcua");
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("opcua");
   ```

## 测试用例

*opc.tcp://118.24.36.220:62547/DataAccessServer* 为一个在线服务端的 serverUrl，可用来测试插件的连接、读写 node、订阅等功能。

[prosys opc-ua-simulation-server](https://downloads.prosysopc.com/opc-ua-simulation-server-downloads.php) 提供了一个本地服务器，按照[使用手册](https://downloads.prosysopc.com/opcua/apps/JavaServer/dist/4.0.2-108/Prosys_OPC_UA_Simulation_Server_UserManual.pdf)可指定端点、加密策略、用户令牌、管理证书等，可用来测试插件的加密通信等功能。

## 接口说明

### getOpcServerList

**语法**

```
opcua::getOpcServerList(serverUrl)
```

**参数**

**serverUrl** 是字符串，表示 server 地址。例如：*opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer/*。

**详情**

获取 OPC server。

**返回值**

返回一个包含 5 列的表，分别是：

* "ServerUri" 表示 server 的标识符。
* "ServerName" 表示 server 的名字。
* "ProductUri" 表示 server 的 product 标识符。
* "Type" 表示 server 的类型。
* "DiscoveryUrl" 表示可以用来连接 server 的 url（若有多个，用 ';' 分割）。

**例子**

```
opcua::getOpcServerList(serverUrl);
```

### getOpcEndPointList

**语法**

```
opcua::getOpcEndPointList(serverUrl)
```

**参数**

**serverUrl** 是字符串，表示 server 地址，例如：*opc.tcp://127.0.0.1:53530/OPCUA/SimulationServer/*。

**详情**

获取 OPC server。

**返回值**

返回一个包含 5 列的表，分别是：

* "endpointUrl" 表示 server 可以用来连接的端点的 url。
* "transportProfileUri" 表示该端点传输配置文件的标识符。
* "securityMode" 表示该端点的安全模式。
* "securityPolicyUri" 表示该端点安全策略的标识符。
* "securityLevel" 表示该端点安全等级。

**例子**

```
opcua::getOpcEndPointList(serverUrl);
```

### connect

**语法**

```
opcua::connect(endPointUrl,clientUri,[userName],[password],[securityMode],[securityPolicy],[certificatePath],[privateKeyPath])
```

**参数**

**endPointUrl** 是字符串，表示要连接的 endpoint 的 url。

**clientUri** 是字符串，表示 client 的标识符，若指定 certificate，则需要与 certificate 里的 URI 保持一致。

**userName** 是字符串，表示用户名。若 server 未设置，可省略。

**password** 是字符串，表示用户密码，与 userName 一起使用。

**securityMode** 是字符串，表示连接的安全模式，必须是 "None", "Sign", "SignAndEncrypt" 中的一个，默认为 "None"。

**securityPolicy** 是字符串，连接的安全策略，必须是 "None", "Basic256", "Basic128Rsa15", "Basic256Sha256" 中的一个，默认为 "None"。若采用 "Basic256", "Basic128Rsa15", "Basic256Sha256" 加密，则需要指定 certificate 和 privateKey。可以使用./open62541/cert/ 目录下的 certificate 和 privateKey，也可以使用自己生成的证书（open62541 项目 tool 目录下的工具可用于[生成证书](https://github.com/open62541/open62541/tree/master/tools/certs)）。

**certificatePath** 是字符串，指定证书路径，若不采用加密通讯可不指定。

**privateKeyPath** 是字符串，指定私钥路径，若不采用加密通讯可不指定。

**详情**

连接 OPC server。

若采用加密通讯，服务端需要信任指定的证书。如果加密通信，使用 Prosys 作为本地模拟服务器。
需要在 Users 界面下添加用户名和密码。例如：用户名: "user1" 和 密码: "123456"。然后在 Certificates 界面下，信任 `open62541server@localhost`。

**返回值**

返回一个 conn，可以显式调用 close 函数进行关闭。

**例子**

```
conn=opcua::connect(serverUrl,"myClient");
conn=opcua::connect(serverUrl,"myClient","user1","123456");
conn=opcua::connect(serverUrl,"urn:opcua.client.application","user1","123456","SignAndEncrypt","Basic128Rsa15","./open62541/cert/client_cert.der","./open62541/cert/client_key.der");
```

### browseNode

**语法**

```
opcua::browseNode(conn)
```

**参数**

**conn** 是 `connect` 函数返回的值。

**详情**

查看所有 Node。

**返回值**

返回的结果是一个 table，包含两列，一列是 nodeNamespace，一列是 nodeIdString。

**例子**

```
conn=opcua::connect(serverUrl,"myClient");
opcua::browseNode(conn);
```

### readNode

**语法**

```
opcua::readNode(conn, nodeNamespace, nodeIdString, [table])
```

**参数**

**conn** 是 connect 函数返回的值。

**nodeNamespace** 是 int 的标量或数组，表示 node 的 Namespace。

**nodeIdString** 是字符串的标量或数组，表示 node 的字符串形式的 ID。

**table** 是表或表的数组（为数组时，表的个数须与 node 个数相同），用于存放读取的结果。

* 若是一个表，将所有 node 的值都插入这张表中。
* 若多个表，每个 node 读取的值分别插入这些表中。
* 若不输入表，则返回值是一张表，表的记录是读取的 node 值。

**详情**

读取一个 node 值，使用前需要先建立一个 OPC 连接。

**返回值**

每个 node 返回的结果包含四个值，分别是：

* "node id" 表示 Node 的 ID， 用 ":" 连接 nodeNamespace 和 nodeIdString。
* "value" 表示 node 的值。
* "timestamp" 表示 source timestamp（本地时间）。
* "status" 表示 node 的 value 状态。

**例子**

```
t1 = table(200:0,`nodeID`value`timestamp`status, [SYMBOL, INT, TIMESTAMP, SYMBOL])
opcua::readNode(conn, 3, "Counter",t1)
opcua::readNode(conn, 3, ["Counter","Expression","Random","Sawtooth"],t1)
t2 = table(200:0,`nodeID`value`timestamp`status`nodeID`value`sourceTimestamp`status,[SYMBOL, INT, TIMESTAMP, SYMBOL，SYMBOL, INT, TIMESTAMP, SYMBOL])
opcua::readNode(conn, 1, ["test1","test4"],t2)
t3 = table(200:0,`nodeID`value`timestamp`status, [SYMBOL, INT, TIMESTAMP, SYMBOL])
t4 = table(200:0,`nodeID`value`timestamp`status, [SYMBOL, INT, TIMESTAMP, SYMBOL])
t5 = table(200:0,`nodeID`value`timestamp`status, [SYMBOL, INT, TIMESTAMP, SYMBOL])
opc::readNode(conn, 1, ["test1","test4", "test9"],[t3,t4,t5])
```

### writeNode

**语法**

```
opc::writeNode(conn, nodeNamespace, nodeIdString, value)
```

**参数**

**conn** 是 `connect` 函数返回的值。

**nodeNamespace** 是 int 的标量或数组，表示 node 的 Namespace。

**nodeIdString** 是字符串的标量或数组，表示 node 的字符串形式的 ID。

**value** 是 Node 的值或数组。

**详情**

写入一个或一组 Node 的值。如果写入类型错误，会抛出异常。

**例子**

```
opcua::writeNode(conn,1,"testwrite.test1",1)
opcua::writeNode(conn,1,["testwrite.test5","testwrite.test6"],[33,11])
opcua::writwriteNodeeNode(conn,1,"testwrite.test2",[1,2,3,4])//one-dimensional array
m = matrix([[1,2,3],[1,2,3]])
opcua::writeNode(conn,1,"testwrite.test3",m)//two-dimensional array
```

### subscribe

**语法**

```
opcua::subscribe(conn, nodeNamespace, nodeIdString, handler, [actionName], [reconnect=false], [resubscribeInterval=0])
```

**参数**

**conn** 是 `connect` 函数返回的值。

**nodeNamespace** 是 int 的标量或数组，表示 node 的 Namespace。

**nodeIdString** 是字符串或字符串的数组，表示 node 的字符串形式的 ID。

**handler** 是数据发生变化时调用的回调函数或表。

**actionName** 可选，STRING 类型标量，表示订阅任务的名称。每个订阅必须指定唯一的 *actionName*。如不指定，将自动生成一个名称。

**reconnect** 可选，BOOL 类型标量，表示在订阅断开时是否自动重连。默认为 false；若设置为 true ，则会在订阅断开时自动尝试重连。

**resubscribeInterval** 可选，非负整数，表示重新订阅的最小时间间隔，单位毫秒，默认值为 0。

**详情**

使用 *handler* 处理订阅的 OPCUA 节点变化的值。

如果启用 *reconnect*，在订阅断开时，将每隔 *resubscribeInterval* 时间尝试重连。在重连过程中，已有的订阅信息不会被清除；如果重连成功，相关的订阅信息将基于重连前的状态继续更新。在重连过程中，用户可以取消该订阅，取消后将不再尝试重连。

注意：目前一个订阅需要独占一个 conn 连接，即若一个连接调用 `subscribe`，不能再用这个连接去进行 `readNode` 或 `writeNode` 等操作。

**例子**

```
t1 = table(200:0,`nodeID`value`timestamp`status, [SYMBOL, INT, TIMESTAMP, SYMBOL])
conn1=opcua::connect(serverUrl，"myClient")
opcua::subscribe(conn1,1,"test.subscribe",t1)
t2 = table(200:0,`nodeID`value`timestamp`status, [STRING, INT, TIMESTAMP, STRING])
conn2=opcua::connect(serverUrl，"myClient")
opcua::subscribe(conn2, 3, ["Counter","Expression","Random","Sawtooth"],t2)
t3 = table(200:0,`nodeID`value`timestamp`status, [SYMBOL, BOOL, TIMESTAMP, SYMBOL])
def callback1(mutable t, d) {
	t.append!(d)
}
conn3=opcua::connect(serverUrl，"myClient")
opcua::subscribe(conn3,2, "testsubscribe",callback1{t3})
```

### unsubscribe

**语法**

```
opcua::unsubscribe(conn|actionName)
```

**参数**

**conn|actionName** 是 `connect` 函数返回的值或订阅时指定的任务名称（actionName）。

**详情**

根据任务名称或连接取消对应的订阅。

**例子**

```
opcua::unsubscribe("action1")
```

### getSubscriberStat

**语法**

```
opcua::getSubscriberStat()
```

**详情**

查看当前所有的订阅状态，包括以下信息：

* actionName，表示订阅任务。
* subscriptionId，表示订阅标识符。
* user，表示建立订阅的会话用户。
* endPointUrl，表示连接的 endPointUrl。
* clientUri，表示连接的 client 标识符。
* nodeID，表示订阅的所有 Node，用 "NodenodeNamespace:nodeIdString" 表示每一个 Node，不同的 Node 用 ';' 分割。
* createTimestamp，表示订阅建立的时间。
* isConnected，是否已连接。
* firstMsgTime，收到第一条消息的时间。
* lastMsgTime，收到最后一条消息的时间。
* processedMsgCount，已经处理的消息数。
* failedMsgCount，处理失败的消息数。
* lastErrMsg，最后一条错误消息的信息。
* lastFailedTimestamp，最后一条错误消息发生的时间。
* lastReconnectTime，最后一次发生重连的时间。

**例子**

```
opcua::getSubscriberStat()
```

### close

**语法**

```
opcua::close(conn)
```

**参数**

**conn** 是 `connect` 函数返回的值。

**详情**

断开与 OPC server 的连接。如果该 conn 订阅了 Node，则在断开 OPC server 的同时也会取消对应的订阅。

**例子**

```
opcua::close(conn)
```
