<!-- Auto-mirrored from upstream `documentation-main/plugins/CSM.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# CSM

CSMAR 面向机构提供金融数据，覆盖股票、债券、基金、指数、期货期权、宏观经济、行业及市场资讯等多个类别，强调内容专业、数据准确、来源权威、更新及时和交付方式灵活。围绕机构研究、量化分析和实时应用等场景，CSMAR 提供了覆盖多层级、多品类的数据服务能力。

DolphinDB CSM 插件用于获取其中的 CSM Level2 实时行情，并将回调数据异步写入 DolphinDB 流数据表，便于后续的流式计算、订阅转发和实时落库。目前插件支持获取如下类别的数据：

* SSEL2\_Quotation：上交所 Level2 十档快照数据。
* SZSEL2\_Quotation：深交所 Level2 十档快照数据。
* SSEL2\_Tick：上交所 Level2 逐笔数据。
* SZSEL2\_Tick：深交所 Level2 逐笔数据。

## 安装插件

### 版本要求

* DolphinDB Server：3.00.4 及更高版本，且部署于 Linux x86-64 系统。
* CSM SDK：当前插件基于 CSM SDK 3.25 开发。

1. 在 DolphinDB 客户端中使用 listRemotePlugins
   函数查看可供安装的插件。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 installPlugin
   函数安装插件。

   ```
   installPlugin("CSM")
   ```
3. 使用 loadPlugin
   函数加载插件。

   ```
   loadPlugin("CSM")
   ```

## 接口说明

### connect

**语法**

```
CSM::connect(username, password, host, port, [option])
```

**详情**

建立与 CSM 服务器之间的连接，返回一个连接句柄。

注：

一个 DolphinDB 进程内只能维护一个 CSM 连接句柄。如果在同一个进程内重复调用
`CSM::connect` 且连接参数完全一致，则返回已有句柄；如果参数不一致，会报冲突错误。

**参数**

**username** STRING 类型标量，指定登录 CSM 服务器所需的用户名。

**password** STRING 类型标量，指定登录 CSM 服务器所需的密码。

**host** STRING 类型向量，指定 CSM 服务器的主机地址。

**port** 正整数向量，指定 CSM 服务器的端口，长度必须与 *host* 一致。

**option**（可选参数）字典，支持以下 key：

* ReceivedTime：key 为字符串，value 为 BOOL 类型标量，默认为 false，指定是否记录数据进入插件的时间。
* OutputElapsed：key 为字符串，value 为 BOOL 类型标量，默认为 false，指定是否记录从数据进入插件到写入流表前的时间间隔。

**返回值**

RESOURCE 类型的连接句柄。

**例子**

```
// 以下连接参数均为示例，请根据实际情况修改
USERNAME = "your_user"
PASSWORD = "your_password"
HOST = ["127.0.0.1"]
PORT = [9000]

handler = CSM::connect(USERNAME, PASSWORD, HOST, PORT)
```

### getSchema

**语法**

```
CSM::getSchema(dataType)
```

**详情**

获取要订阅的数据类别的 schema。使用 `subscribe` 接口订阅数据前需要创建与该 schema 相匹配的输出表。

注：

建议始终使用 `getSchema` 动态获取
schema，避免通过硬编码指定输出表的 schema。数据类别的 schema 依赖创建连接句柄时设置的 *option*，因此必须先调用
`connect`，再调用 `getSchema`。

**参数**

**dataType** STRING 类型标量，指定要订阅的数据类别。有效值如下：

* SSEL2\_Quotation：上交所 Level2 十档快照数据。
* SZSEL2\_Quotation：深交所 Level2 十档快照数据。
* SSEL2\_Tick：上交所 Level2 逐笔数据。
* SZSEL2\_Tick：深交所 Level2 逐笔数据。

**返回值**

一张表，包含以下三列：

* name：数据字段名称。
* type：数据类型，如 INT。
* typeInt：整数，表示数据类型的 ID，如数字 4 表示的数据类型为 INT。数据类型和 ID 的对应关系可以参考数据类型表。

注：

如果设置了 *option* 参数，schema 中会增加对应列：

* receivedTime：数据进入插件的时间，类型为 NANOTIMESTAMP。只有创建连接句柄时在 *option* 参数中设置
  `ReceivedTime=true`，返回结果中才会增加该列。
* perPenetrationTime：从插件接收到数据，到写入流表前的时间间隔。类型为 LONG，单位为微秒。只有创建连接句柄时在
  *option* 参数中设置
  `OutputElapsed=true`，返回结果中才会增加该列。

**例子**

```
sseQuotationSchema = CSM::getSchema("SSEL2_Quotation")
```

### subscribe

```
CSM::subscribe(handle, dataType, outputTable, [queueDepth=1000000])
```

**详情**

订阅指定类别的数据。

**参数**

**handle** RESOURCE 类型的连接句柄，由 `connect` 接口创建。

**dataType** STRING 类型标量，指定需要订阅的数据的类别。有效值如下：

* SSEL2\_Quotation：上交所 Level2 十档快照数据。
* SZSEL2\_Quotation：深交所 Level2 十档快照数据。
* SSEL2\_Tick：上交所 Level2 逐笔数据。
* SZSEL2\_Tick：深交所 Level2 逐笔数据。

**outputTable** 输出表，用于接收被订阅的数据，支持共享流数据表或流计算引擎。创建输出表前需要使用 `getSchema` 获取目标数据类别的 schema，并按照该 schema 创建表。

**queueDepth**（可选参数）正整数标量，表示订阅队列中最多可以容纳的数据条数，默认 1000000。

**返回值**

无

**例子**

```
sseQuotationSchema = CSM::getSchema("SSEL2_Quotation")
sseQuotation = streamTable(10000:0, sseQuotationSchema[`name], sseQuotationSchema[`type])
share sseQuotation as sseQuotation

CSM::subscribe(handler, "SSEL2_Quotation", sseQuotation)
```

### unsubscribe

**语法**

```
CSM::unsubscribe(handle, dataType)
```

**详情**

取消订阅指定的数据类别。

注：

* 如需退订多个数据类别，需要分别调用 `unsubscribe`。
* 退订后订阅队列的状态信息不会清空，调用 `getStatus` 仍可查看之前订阅产生的
  processedMsgCount、failedMsgCount、startTime、endTime 等信息。

**参数**

**handle** RESOURCE 类型的连接句柄，由 `connect` 接口创建。

**dataType** STRING 类型标量，指定需要取消订阅的数据的类别。有效值如下：

* SSEL2\_Quotation：上交所 Level2 十档快照数据。
* SZSEL2\_Quotation：深交所 Level2 十档快照数据。
* SSEL2\_Tick：上交所 Level2 逐笔数据。
* SZSEL2\_Tick：深交所 Level2 逐笔数据。

**返回值**

无

**例子**

```
CSM::unsubscribe(handle, "SSEL2_Quotation")
```

### getStatus

**语法**

```
CSM::getStatus(handle)
```

**详情**

查询订阅队列的状态信息。

**参数**

**handle** RESOURCE 类型的连接句柄，由 `connect` 接口创建。

**返回值**

一张表，包含以下列：

| 列名 | 类型 | 含义 |
| --- | --- | --- |
| topicType | STRING | 订阅队列的名称，有效值：  * SSEL2\_Quotation * SZSEL2\_Quotation * SSEL2\_Tick * SZSEL2\_Tick |
| dataType | STRING | 被订阅数据的类别，有效值：  * quotation：Level2 十档快照数据 * tick：Level2 逐笔数据 |
| market | STRING | 交易所代码，有效值：  * SSE：上交所 * SZSE：深交所 |
| isSubscribed | BOOL | 表示对应数据类别的队列是否仍处于订阅状态。 |
| startTime | NANOTIMESTAMP | 订阅队列的启动时间。 |
| endTime | NANOTIMESTAMP | 订阅队列的停止时间；未停止时为空。 |
| firstMsgTime | NANOTIMESTAMP | 首条成功进入处理流程的数据的时间。 |
| lastMsgTime | NANOTIMESTAMP | 最近一条成功进入处理流程的数据的时间。 |
| processedMsgCount | LONG | 已成功处理的数据条数。 |
| failedMsgCount | LONG | 处理失败的数据条数。 |
| lastErrMsg | STRING | 最近一次处理失败的错误信息。 |
| lastFailedTimestamp | NANOTIMESTAMP | 最近一次处理失败发生的时间。 |
| queueDepthLimit | LONG | 当前队列可容纳的数据条数上限，由 subscribe 接口的queueDepth 参数指定。 |
| queueDepth | LONG | 当前队列内待处理的数据条数。 |

### getHandle

**语法**

```
CSM::getHandle()
```

**详情**

返回当前进程里已存在的 CSM 连接句柄。

**参数**

无

**返回值**

RESOURCE 类型的连接句柄。

### close

**语法**

```
CSM::close(handle)
```

**详情**

关闭 CSM 连接句柄。

**参数**

**handle** RESOURCE 类型的连接句柄，由 `connect` 接口创建。

**返回值**

无

## 使用示例

订阅沪深 Tick 和 Quotation 数据。

```
loadPlugin("CSM")
 go
// 1. 创建 CSM 连接句柄
// 以下连接参数均为示例，请根据实际情况修改
USERNAME = "your_user"
PASSWORD = "your_password"
HOST = ["127.0.0.1"]
PORT = [9000]

opt = dict(`ReceivedTime`OutputElapsed, [true, true])
handler = CSM::connect(USERNAME, PASSWORD, HOST, PORT, opt)

// 2. 获取各个数据类别对应的 schema，创建并共享输出表
sseQuotationSchema = CSM::getSchema("SSEL2_Quotation")
sseQuotation = streamTable(10000:0, sseQuotationSchema[`name], sseQuotationSchema[`type])
share sseQuotation as sseQuotation

szseQuotationSchema = CSM::getSchema("SZSEL2_Quotation")
szseQuotation = streamTable(10000:0, szseQuotationSchema[`name], szseQuotationSchema[`type])
share szseQuotation as szseQuotation

sseTickSchema = CSM::getSchema("SSEL2_Tick")
sseTick = streamTable(10000:0, sseTickSchema[`name], sseTickSchema[`type])
share sseTick as sseTick

szseTickSchema = CSM::getSchema("SZSEL2_Tick")
szseTick = streamTable(10000:0, szseTickSchema[`name], szseTickSchema[`type])
share szseTick as szseTick

// 3. 订阅数据
go
CSM::subscribe(handler, "SSEL2_Quotation", sseQuotation)
CSM::subscribe(handler, "SZSEL2_Quotation", szseQuotation)
CSM::subscribe(handler, "SSEL2_Tick", sseTick)
CSM::subscribe(handler, "SZSEL2_Tick", szseTick)

// 4. 查询订阅队列的状态
CSM::getStatus(handler)

// 5. 关闭 CSM 连接句柄
CSM::close(handle)
```

## 常见问题

### 1. 为什么 getSchema 需要在 connect 之后调用？

因为 schema 不是静态固定的，调用 `connect` 时传入的 *option* 会决定是否为 schema 附加 receivedTime 和 perPenetrationTime 列。

### 2. 为什么创建输出表后调用 subscribe 报 schema mismatch？

常见原因有：

* 数据类别的 schema 和输出表的 schema 不匹配。
* 创建连接句柄时设置了 `ReceivedTime=true` 或 `OutputElapsed=true`，但创建输出表时没有调用 `getSchema` 获取最新的 schema。

### 3. 为什么退订后调用 getStatus 还能查看订阅队列的状态？

退订时会停止队列，但不会清空状态，因此仍可查看之前订阅产生的状态数据：

* processedMsgCount
* failedMsgCount
* startTime
* endTime

保留订阅队列的历史状态有利于排查订阅期间出现的问题。
