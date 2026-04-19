<!-- Auto-mirrored from upstream `documentation-main/plugins/MDL.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# MDL

通联数据依托于金融大数据，结合人工智能技术为投资者提供个性化、智能化、专业化投资服务。而 MDL 是通联数据提供的高频行情数据服务，DolphinDB 提供了能够从 MDL 服务器获取高频行情数据的 DolphinDB MDL 插件，帮助用户方便地通过 DolphinDB 脚本语言将实时行情数据接入 DolphinDB 中，以便进行后续的计算或存储。

MDL 目前支持接收上交所、深交所等数据。请联系 DolphinDB 技术支持获取数据服务支持列表。

## 在插件市场安装插件

### 版本要求

支持 DolphinDB Server 2.00.10 及更高版本；支持 Shark；支持 Linux x86-64, Linux ABI。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456");
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("mdl");
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("mdl");
   ```

## 用户接口

### createHandle

**语法**

```
createHandle(name, host, port, username, [workerNum=1], [option])
```

**参数**

**name** STRING 类型标量，作为句柄的唯一标识，不可重复。

**host** STRING 类型向量，服务器的 IP 或者域名。

**port** INT 类型向量，端口号，个数需要与 *host* 参数的数量一致。

**username** STRING 类型标量，用户 ID。

**workerNum** INT 类型标量，MDL 工作线程的数量，可选参数。

**option** 一个字典，类型为 (STRING, BOOL)，可选参数。支持如下键值：

* "outputMetaData" 表示是否获取 MDL 接收数据的元数据信息，如接收时间、接收序列号等。将其指定为 dict (["outputMetaData"], [true]) 时，订阅的数据将包含元相关数据列。
* "outputRecvTime" 表示是否获取插件收到行情数据的时间戳。其指定为 dict (["outputRecvTime"], [true]) 时，订阅的数据中将包含插件收到行情数据的时间戳列。
* "outputElapsed" 表示是否获取 MDL 插件接收数据处理的时延。其指定为 dict (["outputElapsed"], [true]) 时，订阅的数据将包含插件收到行情数据的时延列。时延的定义同上。

**详情**

返回一个 MDL 句柄，用于之后的操作。

### getSchema

**语法**

```
getSchema(svrID, msgID, [extraOrderLevel=0], [option])
```

**参数**

**svrID** STRING 类型标量，数据服务 ID。支持的数据服务 ID 列表参见附录。

**msgID** INT 类型标量，消息 ID。消息 ID 与通联的数据 MessageID 相同，请联系通联查阅具体订阅种类信息。

**extraOrderLevel** INT 类型标量，值为 0-10，默认为 0。在指定 svrID、msgID 为 "MDLSID\_MDL\_SZL2", 28 或者 "MDLSID\_MDL\_SHL2", 4 即订阅 snapshot 时有效，会决定是否在表末尾增加 order queue 相关信息的字段。有 10 档可选，所以可以指定为 0-10。

**option** 一个字典，类型为 (STRING, BOOL)，可选参数。支持如下键值：

* "outputMetaData" 表示是否获取 MDL 接收数据的元数据信息，如接收时间、接收序列号等。将其指定为 dict (["outputMetaData"], [true]) 时，订阅的数据将包含元相关数据列。
* "outputRecvTime" 表示是否获取插件收到行情数据的时间戳。其指定为 dict (["outputRecvTime"], [true]) 时，订阅的数据中将包含插件收到行情数据的时间戳列。
* "outputElapsed" 表示是否获取 MDL 插件接收数据处理的时延。其指定为 dict (["outputElapsed"], [true]) 时，订阅的数据将包含插件收到行情数据的时延列。时延的定义同上。

**详情**

获取对应消息的表结构。
另外，可以通过 `schema = getSchema("SHL2_SZL2_ORDER_AND_TRANSACTION", 0)` 获取用于 order transaction 合并类型表的结构。

### subscribe

**语法**

```
subscribe(handle, outputTable, svrID, [svrVersion], [msgID], [fieldName], [fieldValues], [extraOrderLevel=0])
```

**参数**

**handle** MDL 句柄。

**outputTable** 可以为一个共享流表，需要在订阅前创建，该表的 schema 可以通过插件提供的 `getSchema` 函数来获取。连接服务器后会将订阅的数据实时刷新到这个流表中。也可以为字典类型，key 是 Int 类型的 channelNo，value 是对应 channelNo 行情要写入的共享流表，该表的结构通过 `getSchema` 函数来获取`（getSchema("SHL2_SZL2_ORDER_AND_TRANSACTION", 0)）`，目前支持 "SHL2\_SZL2\_ORDER\_AND\_TRANSACTION" 一种，对应上交所 L2 和深交所 L2 的 order 和 transaction 合并类型行情。这种情况下，不支持填写 svrVersion、msgID、fieldName、fieldValues、extraOrderLevel 字段。

**svrID** STRING 类型标量，要订阅的数据服务 ID（联系 DolphinDB 技术支持获取数据服务列表）。如果 outputTable 为字典类型，还支持 "SHL2\_ORDER\_AND\_TRANSACTION" 和 "SZL2\_ORDER\_AND\_TRANSACTION" 两种，每一种分别订阅对应交易所的 order 和 transaction 行情。支持的 svrID 列表参见附录。

**svrVersion** STRING 类型标量，要订阅的数据服务版本号。支持的 svrVersion 列表参见附录。

**msgID** INT 类型标量，要订阅的消息 ID。消息 ID 与通联的数据 MessageID 相同，请联系通联查阅具体订阅种类信息。

**fieldName** STRING 类型标量，要过滤的字段名，可选参数。

**fieldValues** STRING 类型向量，要过滤的字段对应的值，可选参数，对于日期类型，"0" 用于订阅日期为空的情况，"20230808" 这种形式用于订阅指定的日期。

**extraOrderLevel** INT 类型标量，值为 0-10，默认为 0。在指定 svrID、msgID 为 "MDLSID\_MDL\_SZL2", 28 或者 "MDLSID\_MDL\_SHL2", 4 即订阅 snapshot 时有效，会决定是否在表末尾增加 order queue 相关信息的字段。有 10 档可选，所以可以指定为 0-10。

**详情**

记录要订阅的消息，然后在连接到服务器时提交订阅请求，必须在调用 connect 之前调用。可以使用字段名与字段值对要订阅的服务进行过滤，如可以通过 *fieldName* 指定股票编码字段，通过 *fieldValues* 指定要订阅的股票编码。
一个 MDL 句柄订阅的一种消息只能指定一个流表，如果需要对一个消息订阅多次并分别写入到多个流表，可以通过 `createHandle` 创建多个句柄，分别进行订阅并指定要写入到的流表。

注意：

1. 因为通联 MDL 不支持同时订阅在不同服务器的数据源，也就是当同时订阅上交所 L2 和深交所 L2 时，只能收到其中一个数据源的行情。为了解决这个问题，需要创建两个句柄，分别订阅上交所 L2 和深交所 L2 的数据，一个句柄只订阅一个数据源的行情。
2. 如果订阅了 order transaction 合并类型，MDDate 字段为 handle 创建日期，如果需要跨天订阅，该字段无效。
3. 如果订阅了 order transaction 合并类型，上交所 SecurityType 字段为 marketInfo 回调所得，因此如果在盘中订阅，最开始记录的 SecurityType 字段可能为空。

### unsubscribe

**语法**

```
unsubscribe(handle, svrID, [svrVersion], [msgID], [fieldName], [fieldValues])
```

**参数**

**handle** MDL 句柄。

**svrID** STRING 类型标量，要取消订阅的数据服务 ID（联系 DolphinDB 技术支持获取数据服务列表）。另外支持指定 "SHL2\_ORDER\_AND\_TRANSACTION" 和 "SZL2\_ORDER\_AND\_TRANSACTION" 两种用于取消 order transaction 合并类型的订阅。这种情况下不支持后续参数的指定。支持的 svrID 列表参见附录。

**svrVersion** STRING 类型标量，要取消订阅的数据服务版本号。支持的 svrVersion 列表参见附录。

**msgID** INT 类型标量，要取消订阅的消息 ID。消息 ID 与通联的数据 MessageID 相同，请联系通联查阅具体订阅种类信息。

**fieldName** STRING 类型标量，要过滤的字段名，可选参数。

**fieldValues** STRING 类型向量，要过滤的字段对应的值，可选参数。

**详情**

取消订阅，必须在调用 `connect` 之前调用。

### connectMDL

**语法**

```
connectMDL(handle)
```

**参数**

**handle** MDL 句柄。

**详情**

连接服务器并提交用户的订阅请求。

### deleteHandle

**语法**

```
deleteHandle(handle)
```

**参数**

**handle** MDL 句柄。

**详情**

手动关闭 MDL 句柄并释放掉资源。注意会话结束时 MDL 句柄不会断开连接和释放资源，之后可以通过 `getHandle` 来重新获取句柄来释放。

### getHandle

**语法**

```
getHandle(name)
```

**参数**

**name** STRING 类型标量，是 createHandle 创建时给该 MDL 句柄赋予的标识名。

**详情**

获取对应 *name* 的 MDL 句柄。

### getHandleStatus

**语法**

```
getHandleStatus()
```

**详情**

返回一张表，表中保存着 MDL 实例的各种信息。

* HandleName 记录着句柄名。
* Address 记录着连接服务器的地址，格式是 “host1:port1; host2:port2;…”。
* UserName 记录着用户名；CreateTime 记录着 MDL 实例创建的时间。
* IsConnect 记录着是否已建立连接。

### getStatus

```
MDL::getStatus(handle)
```

**参数**

**handle** MDL 句柄。

**详情**

返回一个表格，包含各种已订阅数据的状态信息，包含数据类型 StockTick, IndexTick, FuturesTick, OrderTransaction, Transaction, Order, FundTick, BondTick，OptionTick 或 SecurityLending。

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| **market** | 订阅的市场 | STRING |
| **dataType** | 数据品类 | STRING |
| **channelNo** | OrderTransaction 分 channel 订阅时的 channel 号 | INT |
| **startTime** | 订阅开始的时间 | NANOTIMESTAMP |
| **endTime** | 订阅结束的时间 | NANOTIMESTAMP |
| **firstMsgTime** | 第一条消息收到的时间 | NANOTIMESTAMP |
| **lastMsgTime** | 最后一条消息收到的时间 | NANOTIMESTAMP |
| **processedMsgCount** | 已经处理的消息数 | LONG |
| **lastErrMsg** | 最后一条错误信息 | STRING |
| **failedMsgCount** | 处理失败的消息数 | LONG |
| **lastFailedTimestamp** | 最后一条错误消息发生的时间 | NANOTIMESTAMP |

有关 MDL 插件对数据品类的支持情况，请联系 DolphinDB 技术支持。

## 使用示例

**示例1**

```
loadPlugin("mdl") // 加载插件

schema = MDL::getSchema(`MDLSID_MDL_SHL2, 4) // 获取 MDLSID_MDL_SHL2 即上交所 L2 的 4 号行情的表结构
tb1 = streamTable(10000:0, schema[`name], schema[`type])
enableTableShareAndPersistence(table=tb1, tableName=`Tb1, cacheSize=10000)

schema = MDL::getSchema(`MDLSID_MDL_SHL2, 6)
tb2 = streamTable(10000:0, schema[`name], schema[`type])
enableTableShareAndPersistence(table=tb2, tableName=`Tb2, cacheSize=10000)

host = ["mdl-XXX.datayes.com"]
port = [端口号]
handle = MDL::createHandle(`handle1, host, port, 用户token) // 创建 MDL 句柄

MDL::subscribe(handle, tb1, `MDLSID_MDL_SHL2, `MDLVID_MDL_SHL2, 4, "SecurityID", [`603238, `510650])
MDL::subscribe(handle, tb2, `MDLSID_MDL_SHL2, `MDLVID_MDL_SHL2, 6)

MDL::connectMDL(handle) // 连接服务器，host 和 port 在 createHandle 创建句柄时指定

handle2 = MDL::getHandle(`handle1) // 获取名为 "handle1" 的 MDL 句柄

status = MDL::getHandleStatus() // 获取当前所有句柄的消息，并以表形式返回

MDL::deleteHandle(handle) // 删除句柄
```

**示例2**

```
loadPlugin("mdl");

dropStreamTable(`Tb1)
dropStreamTable(`Tb2)
dropStreamTable(`Tb3)

// 创建 4 个相同的目标表
schema = MDL::getSchema("SHL2_SZL2_ORDER_AND_TRANSACTION", 0)
tb1 = streamTable(10000:0, schema[`name], schema[`type])
enableTableShareAndPersistence(table=tb1, tableName=`Tb1, cacheSize=10000)
tb2 = streamTable(10000:0, schema[`name], schema[`type])
enableTableShareAndPersistence(table=tb2, tableName=`Tb2, cacheSize=10000)
tb3 = streamTable(10000:0, schema[`name], schema[`type])
enableTableShareAndPersistence(table=tb3, tableName=`Tb3, cacheSize=10000)

// 创建两个句柄，分别对应上交所 L2 和 深交所 L2
handle1 = MDL::createHandle(`handle1, ["mdlXXX.datayes.com"], [端口号], 用户token) // 上交 L2
handle2 = MDL::createHandle(`handle2, ["mdlXXX.datayes.com"], [端口号], 用户token) // 深交 L2

// 订阅
dict1 = dict([1, 2],[tb1, tb2]) // channelNo -> streamTable
MDL::subscribe(handle1, dict1, `SHL2_ORDER_AND_TRANSACTION) // 按 channelNo 订阅上交 L2 的 order 和 transaction

dict2 = dict([2011, 2012],[tb2, tb3])
MDL::subscribe(handle2, dict2, `SZL2_ORDER_AND_TRANSACTION) // 按 channelNo 订阅深交 L2 的 order 和 transaction

// 连接并开始接受数据
MDL::connectMDL(handle1)
MDL::connectMDL(handle2)

MDL::deleteHandle(handle1)
MDL::deleteHandle(handle2)
```

**示例3** 订阅港交所市场行情数据

```
schema = MDL::getSchema(`MDLSID_MDL_HKEX, 2)
tb1 = streamTable(10000:0, schema[`name], schema[`type])
share tb1 as Tb1

//创建句柄
host = ["ABC.com"]
port = [123]
handle = MDL::createHandle(`handle1, host, port, "token")

MDL::subscribe(handle, Tb1, `MDLSID_MDL_HKEX, `MDLVID_MDL_HKEX, 2) //准备订阅港交所市场行情
MDL::connectMDL(handle)  //连接，发起订阅

re_stat = MDL::getStatus(handle)
MDL::deleteHandle(handle)
```

* 如需订阅港交所指数行情，在调用 `subscribe` 时将 msgID 设置为 7，例如：`` MDL::subscribe(handle, Tb1, `MDLSID_MDL_HKEX, `MDLVID_MDL_HKEX, 7) ``。
* 如需订阅港交所证券信息表，在调用 `subscribe` 时将 msgID 设置为 8，例如：`` MDL::subscribe(handle, Tb1, `MDLSID_MDL_HKEX, `MDLVID_MDL_HKEX, 8) ``。
* 如需订阅港交所逐笔行情，在调用 `subscribe` 时将 msgID 设置为 9，例如：`` MDL::subscribe(handle, Tb1, `MDLSID_MDL_HKEX, `MDLVID_MDL_HKEX, 9) ``。

## MDL 与 DolphinDB 类型对照

| 描述 | MDL 类型 | DolphinDB 类型 |
| --- | --- | --- |
| 32 位整数 | int32\_t | INT |
| 64 位整数 | int64\_t | LONG |
| 32 位无符号整数 | uint32\_t | LONG |
| 64 位无符号整数 | uint64\_t | LONG |
| 单精度浮点 | MDLFloatT<x> | FLOAT |
| 双精度浮点 | MDLDouble<x> | DOUBLE |
| Ascii 字符串 | MDLAnsiString | STRING |
| UTF8 字符串 | MDLUTF8String | STRING |
| 时间 | MDLTime | TIME |
| 日期 | MDLDate | DATE |

## 行情源品种与 svrID 和 svrVersion 对照表

| **行情源品种** | **svrID** | **svrVersion** |
| --- | --- | --- |
| 上交所L2 | MDLSID\_MDL\_SHL2 | MDLVID\_MDL\_SHL2 |
| 上交所L2股票行情快照实时合成，对接rderbookSnapshotEngine | "SHL2\_ORDER\_AND\_TRANSACTION" |  |
| 上交所 L1 | MDLSID\_MDL\_SHL1 | MDLSID\_MDL\_SHL1 |
| 深交所L2 | MDLSID\_MDL\_SZL2 | MDLVID\_MDL\_SZL2 |
| 深交所 L2 股票行情快照实时合成，对接rderbookSnapshotEngine | "SZL2\_ORDER\_AND\_TRANSACTION" |  |
| 深交所 L1 | MDLSID\_MDL\_SZL1 | MDLSID\_MDL\_SZL1 |
| 中金所 L2 | MDLSID\_MDL\_CFFEXL2 | MDLVID\_MDL\_CFFEXL2 |
| 中金所 L1 | MDLSID\_MDL\_CFFEX | MDLVID\_MDL\_CFFEX |
| 郑商所 L2 | MDLSID\_MDL\_CZCEL2 | MDLVID\_MDL\_CZCEL2 |
| 郑商所 L1 | MDLSID\_MDL\_CZCE | MDLVID\_MDL\_CZCE |
| 上期能源 L2 | MDLSID\_MDL\_SHFEL2 | MDLVID\_MDL\_SHFEL2 |
| 上期所 L1 | MDLSID\_MDL\_SHFE | MDLVID\_MDL\_SHFE |
| 能源所 L1 | MDLSID\_MDL\_SHNY | MDLVID\_MDL\_SHNY |
| 大商所 L2 | MDLSID\_MDL\_DCEL2 | MDLVID\_MDL\_DCEL2 |
| 大商所 L1 | MDLSID\_MDL\_DCE | MDLVID\_MDL\_DCE |
| 广期所 L2 | MDLSID\_MDL\_GFEXL2 | MDLVID\_MDL\_GFEXL2 |
| 广期所 L1 | MDLSID\_MDL\_GFEX | MDLVID\_MDL\_GFEX |
| 港交所 | MDLSID\_MDL\_HKEX | MDLVID\_MDL\_HKEX |
| 北交所 | MDLSID\_MDL\_NEEQ | MDLVID\_MDL\_NEEQ |
| 中证指数 | MDLSID\_MDL\_CSI | MDLVID\_MDL\_CSI |

## FAQ

### 1. 无法连接某一个市场

检查填写的地址和端口是否正确。例如，上海和深圳市场的地址和端口可能不同，连接时需确保配置正确。若配置正确的情况下仍无法连接，请联系通联技术支持解决问题。

### 2. 是否支持丢失重传功能？

该插件基于 MDL SDK 实现，不支持丢失重传功能。在网络环境不稳定的情况下，建议通过 MDL 客户端进行连接。插件可通过接收客户端转发的行情数据来提升稳定性。如需了解 MDL 客户端的具体使用方法，请联系通联技术支持。

### 3. 如何处理内存耗尽（OOM）问题？

若流表长时间没有收到数据，且日志中出现以 [PLUGIN::MDL] 开头的 out of memory 或 bad alloc 信息，则可能发生了 OOM。OOM 会导致数据写入失败，进而影响后续计算。为避免 OOM，建议采取以下措施：

合理分配流数据的容量（capacity），并降低接收行情数据的流表的 cacheSize，减少数据长时间驻留内存的可能性。

在接收行情数据的节点上，若需要同时处理大规模数据或执行复杂查询，需特别关注内存使用情况。

及时释放不再需要的临时变量，可通过 undef 函数管理 session 变量。

### 4. 是否支持跨天连接？

MDL 支持跨天连接功能。若在前一日收盘前建立连接，次日开盘后连接仍会保持，并继续接收数据。注意：在收盘后尝试建立连接将无法成功。

### 5. 插件是否支持断线重连？

插件内置了由 MDL SDK 提供支持的断线重连机制，对插件本身完全透明。可通过日志筛选以 [PLUGIN::MDL] 开头的记录，关注包含 connect 和 disconnect 的条目，了解断线重连的具体情况。注意：插件在成功重连后，SDK 不会补传断连期间的数据，因此这些数据将不可恢复。

### 6. 如何避免因阻塞导致的数据丢失？

在插件接收数据时，建议使用异步持久化的流表，并预设初始容量（如 100 万条）。这样可以避免因流表扩容影响写入性能，从而避免 SDK 端行情缓存因满载导致数据丢失。

### 7. 连接出现报错，如何排查原因？

根据报错内容判断错误原因，或联系通联技术支持获取帮助。常见连接错误代码及含义如下：

| 错误代码 | 含义 |
| --- | --- |
| 0 | 成功 |
| 1 | 服务编号错误 |
| 2 | 消息编号错误 |
| 3 | 服务版本错误 |
| 4 | 密码错误 |
| 5 | 用户未授权 |
| 6 | 达到最大用户数 |
| 7 | 没有资源 |
| 8 | 字段名错误 |
| 9 | 参数错误 |
| 10 | 未定义 |
| 11 | 超时 |
| 12 | 正在执行中 |
| 13 | 达到最大请求数 |
| 14 | 服务忙 |

### 8. 为何数据中 receiveTime 早于 TickTime

这可能是由于插件所在服务器的系统时间未校准，导致快于交易所时间。建议对系统时间进行校准，否则使用 receiveTime 和 TickTime 计算数据传输时延可能会产生不准确的结果。
