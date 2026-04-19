<!-- Auto-mirrored from upstream `documentation-main/plugins/windtdf.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# WindTDF

为接收万得实时行情数据，DolphinDB 开发了 WindTDF 插件。通过该插件可以获取实时的股票、债券、期货等行情。

注意，DolphinDB 仅提供对接万得 TDF C++ Remote API 的 WindTDF 插件。数据源和接入服务可咨询数据服务商或证券公司。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本。支持 Linux x86-64。

### 安装步骤

1. 在DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("WindTDF")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("WindTDF")
   ```

## 用户接口

### createHandle

**语法**

```
WindTDF::createHandle(host, port, username, password, [option])
```

**详情**

返回一个 WindTDF 句柄，用于订阅、取消订阅、连接、关闭。在同一个 dolphindb 进程中，只能创建一个 WindTDF 连接句柄。

如果前4个参数指定了长度大于 1 的向量，则插件会采用双活模式进行连接（目前最多支持两路连接 ）。否则，插件采用单个服务器连接的方式。

**参数**

**host** 字符串向量或标量，表示服务器的 IP 或者域名。向量的长度不能大于 2。

**port** 整型向量或标量，表示端口号。向量的长度不能大于 2。

**username** 字符串向量或标量，表示用户 ID。向量的长度不能大于 2。

**password** 字符串向量或标量，表示，用户密码。向量的长度不能大于 2。

**option** 可选参数。是字典类型，用于指定扩展参数。当前键只支持 outputRecvTime，outputElapsed。

其中：

* outputRecvTime 表示是否获取插件收到行情数据的时间戳，对应值为布尔值。指定为 dict(["outputRecvTime"], [true]) 时，`getSchema` 获取的表结构中将包含插件收到行情数据的时间戳列。
* outputElapsed 表示是否获取 WindTDF 插件接收行情数据并转换为 DolphinDB 格式数据的时延，对应值为布尔值。指定为 dict(["outputElapsed"], [true]) 时，`getSchema` 获取的表结构中将包含插件收到行情数据的时延列。

  时延的定义：‘WindTDF 回调函数返回数据’ 到 ‘准备 append 到共享流表前’ 的时间。

**注意**

前4个参数指定的参数形式需要保持一致。当全部指定为向量时，需要保持向量的长度一致，即如果 *host* 是长度为 2 的向量，其余3个参数也必须是长度为 2 的向量。

### getSchema

**语法**

```
WindTDF::getSchema(dataType)
```

**详情**

该函数应该在 `WindTDF::createHandle` 函数之后，`WindTDF::connect` 函数之前调用，用于获取行情数据的表结构。

返回一个表，包含三列：name，typeString 和 typeInt，分别表示该行情表各个字段的名称、类型名和类型枚举值。可通过该表来创建具有相同结构的共享流表。

如果在 `createHandle` 中指定了*options*，则在返回的 schema 中会增加对应的列。如果指定了 outputRecvTime 为 true，则会增加一个 NANOTIMESTAMP 类型的列（receivedTime，表示数据进入插件的时间）；如果指定了 outputElapsed 为 true，则会增加一个 LONG 类型列（perPenetrationTime，表示从插件接收到数据，到写入流表前的时间间隔，单位为微秒）。

**参数**

**dataType** STRING 类型标量，表示行情数据类型或者投资品类型，可取以下值：'snapshot', 'trade', 'order', 'index', 'futures', 'options', 'orderTrade'。

### subscribe

**语法**

```
WindTDF::subscribe(handle, outputTable, market, dataType, [codeList], [seqCheckMode=1])
```

**详情**

订阅指定市场，指定类型的行情数据。

注意： 该插件必须在连接建立前进行订阅，连接建立后将无法进行订阅。

**参数**

**handle** `WindTDF::createHandle` 返回的连接句柄。

**outputTable** 行情数据输出的目标表，需要是一个共享流表，且结构与 `WindTDF::getSchema` 返回的结构相同。

**market** STRING 类型标量，表示需要订阅的的市场名称。支持的订阅市场和类型的映射关系见下文的映射表。

**dataType** STRING 类型标量，表示需要订阅的行情数据类型。可以为 “snapshot”（快照），”order”（逐笔委托），”trade”（逐笔成交），”orderTrade”（逐笔成交与逐笔委托合并），”index”（指数），”futures”（期货），”options”（期权）。

注意，期货、期权依赖于当天的市场元数据信息，如需订阅，每次清盘需要重连。

**codeList** 可选，字符串向量，表示订阅的股票代码，默认为空。 注意，如果有一种类型在 `WindTDF::subscribe` 订阅了全部的股票代码，则其他种类都会订阅全部的代码。

**seqCheckMode** 可选，可以为整型标量，也可以为 STRING 类型标量，默认为 1。在 orderTrade 合并类型订阅中生效，控制在数据不连续时插件接收数据的行为。

* seqCheckMode 为 0 或者 'check'：代表在数据不连续时，停止接收数据。
* seqCheckMode 为 1 或者 'ignoreWithLog'：代表在数据不连续时，继续接受数据，但是会输出对应具体序号跳变情况到 info 级别的 log。该选项为默认选项。
* seqCheckMode 为 2 或者 'ignore'：代表在数据不连续时，继续接受数据，且不输出任何 log。

判断是否连续的方式：

* 上交所：不同标的 order 和 trade 数据的 nBizIndex 共同连续递增。
* 深交所：不同标的 order 和 trade 数据的 nBizIndex 共同连续递增。
  注意，随着交易所规则改变，该规则也可能发生改变。

订阅市场与类型映射表

| market | dataType |
| --- | --- |
| SH-2-0 | snapshot, trade, order, orderTrade |
| SZ-2-0 | snapshot, trade, order, orderTrade |
| SI-1-0 | index |
| SH-1-1 | futures, options |
| SZ-1-1 | futures, options |
| CF-2-0 | futures, options |

### unsubscribe

**语法**

```
WindTDF::unsubscribe(handle, market, dataType)
```

**详情**

取消订阅指定市场与类型的行情数据。

注意： 该插件必须在连接建立前取消订阅，连接建立后将无法取消订阅。

**参数**

**handle** `WindTDF::createHandle` 返回的连接句柄。

**market** STRING 类型标量，表示需要订阅的的市场名称。支持的订阅市场和类型的映射关系见 `WindTDF::subscribe` 里的映射表。

**dataType** STRING 类型标量，表示需要订阅的行情数据类型。可以为 “snapshot”（快照），”order”（逐笔委托），”trade”（逐笔成交），”orderTrade”（逐笔成交与逐笔委托合并），”index”（指数），”futures”（期货），”options”（期权）。

### connect

**语法**

```
WindTDF::connect(handle, [replay])
```

**详情**

建立与 WindTDF 行情服务器之间的连接，开始接收行情数据。如果指定了 `replay` 则会回放当前的所有数据。

**参数**

**handle** `WindTDF::createHandle` 返回的连接句柄。

**replay** BOOL 类型标量，默认为 false，表示订阅实时数据。若设置为 true，则在交易结束后回放当天的所有数据。该参数对应于万得 TDF 的 time 参数。

注意，以下2种情况不允许设置 replay = true：

* createHandle 传入了多对 IP:PORT。
* 交易时间，即 8 点至 15 点之间。

### close

**语法**

```
WindTDF::close(handle)
```

**详情**

关闭 WindTDF 连接句柄。在关闭后可以再次连接。

**参数**

**handle** `WindTDF::createHandle` 返回的连接句柄。

### delete

**语法**

```
WindTDF::delete(handle)
```

**详情**

删除一个 WindTDF 连接句柄。删除之后将无法再次连接。

**参数**

**handle** `WindTDF::createHandle` 返回的连接句柄。

### getHandle

**语法**

```
WindTDF::getHandle()
```

**详情**

返回已连接的 WindTDF 连接句柄。

### getStatus

**语法**

```
WindTDF::getStatus()
```

**详情**

返回一个表格，包含各种已订阅数据的状态信息，不包含未订阅过的数据类型。

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| **topicName** | 订阅的名称 | STRING |
| **startTime** | 订阅开始的时间 | NANOTIMESTAMP |
| **endTime** | 订阅结束的时间 | NANOTIMESTAMP |
| **firstMsgTime** | 第一条消息收到的时间 | NANOTIMESTAMP |
| **lastMsgTime** | 最后一条消息收到的时间 | NANOTIMESTAMP |
| **processedMsgCount** | 已经处理的消息数 | LONG |
| **lastErrMsg** | 最后一条错误信息 | STRING |
| **failedMsgCount** | 处理失败的消息数 | LONG |
| **lastFailedTimestamp** | 最后一条错误消息发生的时间 | NANOTIMESTAMP |

## 完整示例

```
// 建立 handle

handle = WindTDF::createHandle(HOST, PORT, USERNAME, PASSWORD, dict(["outputRecvTime", "outputElapsed"], [true, true]));
// 订阅上交所的股票快照
schema = WindTDF::getSchema(`snapshot);
snapshot_sh_s = streamTable(10000:0, schema[`name], schema[`typeString]);
share snapshot_sh_s as snapshot_sh_s1;
WindTDF::subscribe(handle, snapshot_sh_s1, "SH-2-0", "snapshot");

// 订阅上交所的期权快照
schema = WindTDF::getSchema(`futures);
futures_sh_s = streamTable(10000:0, schema[`name], schema[`typeString]);
share futures_sh_s as futures_sh_s1;
WindTDF::subscribe(handle, futures_sh_s1, "SH-1-1", "futures");

// 获取已有的 handle
handle = WindTDF::getHandle();

// 建立连接
WindTDF::connect(handle)

// 查看订阅状态
WindTDF::getStatus()

// 关闭连接
WindTDF::close(handle)

// 取消已有的订阅（非必要）
WindTDF::unsubscribe(handle, "SH-2-0", "snapshot");
WindTDF::unsubscribe(handle, "SH-1-1", "futures");

// 移除handle
WindTDF::delete(handle)
```
