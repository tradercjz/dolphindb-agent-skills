<!-- Auto-mirrored from upstream `documentation-main/plugins/insight/insight.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# INSIGHT

INSIGHT 是华泰证券提供的极速金融数据服务，为方便与该金融数据服务对接，DolphinDB 开发了 insight 插件，获取由华泰提供的实时行情数据。插件基于华泰 INSIGHT SDK TCP 版本开发，通过实现行情的回调接口获取数据。目前支持接入多家证券市场与期货市场的实时行情，数据品类包括逐笔、股票、基金、期权、期货快照、融券通等。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本。支持 Linux x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("insight")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("insight")
   ```

## 接口说明

### connect

**语法**

```
insight::connect(outputDict, host, port, username, password, [workerNum=5], [option], [seqCheckMode=1], [certDirPath], [dataVersion="3.2.8"], backupList)
```

**详情**

注册消息接收接口并连接 Insight 服务器，返回 Insight tcpClient 连接的句柄。

**参数**

**outputDict** 类型为 Dictionary，Dictionary 的键为 StockTick, IndexTick, FuturesTick, OrderTransaction, Transaction, Order, FundTick, BondTick，OptionTick 或 SecurityLending，值为共享流表或者一个字典。

以上几种数据分别接入股票快照、指数快照、期货快照、逐笔合成类型、逐笔成交类型、逐笔委托类型、基金快照、债券快照、期权快照、融券通数据。

当值为字典时，key 为整型，代表 channel 号。value 为一个共享流表，即对应 channel 数据需要接入的数据表。

**host** STRING 类型标量，表示服务器地址。

**port** 整型标量，表示服务器端口。

**username** STRING 类型标量，表示用户名。

**password** STRING 类型标量，表示密码。

**workerNum** 可选，整型标量，表示处理线程池的线程数，默认为 5。大小需要在 1-32767 之间。

**option** 可选，是字典类型，表示扩展参数，key 为 STRING 类型，value 为 BOOL 类型。当前支持 ReceivedTime, OutputElapsed。
ReceivedTime 表示是否获取插件收到行情数据的时间戳，默认为 true。其指定为 dict(["ReceivedTime"], [true]) 时，插件处理输出的数据将包含行情数据的时间戳列。
OutputElapsed 表示是否获取 Insight 插件 接收数据处理的时延，默认为 false。其指定为 dict(["OutputElapsed"],[true]) 时，插件处理输出的数据将包含行情数据的时延列。

时延的定义：“insight 回调函数返回数据”到“准备开始 transform 处理”，或“准备 append 到共享流表”前这段时间。该列的单位为纳秒。

**seqCheckMode** 可选，整型或 STRING 类型标量，默认为 1。在 OrderTransaction 合并类型订阅中生效，用于控制在数据不连续时插件接收数据的行为。

* seqCheckMode 为 0 或者 'check'：代表在数据不连续时，停止接收数据。
* seqCheckMode 为 1 或者 'ignoreWithLog'：代表在数据不连续时，继续接收数据，同时输出对应具体序号跳变情况到 INFO 级别的 Log。
* seqCheckMode 为 2 或者 'ignore'：代表在数据不连续时，继续接收数据，不输出任何 Log。

判断数据是否连续的方式（随着交易所规则改变，该规则也可能发生改变）：

* 上交所：不同标的 Order 和 Transaction 数据的 applSeqNum 共同连续递增。
* 深交所：不同标的 Order 和 Transaction 数据的 applSeqNum 共同连续递增。

**certDirPath** 可选，STRING 类型标量。如果未指定，默认会在 DolphinDB 当前节点的 Home 目录（可以通过 `getHomeDir` 函数进行查看，单节点、集群的各个节点之间的 Home 目录都不相同），以及 pluginDir 中的 insight 文件夹中进行查找。

如果指定了错误的且存在的文件夹，在连接时会报错：failed to registHandleAndLogin: create client failed。但如果在进行错误连接前已经进行过正确的连接，那么由于已经验证过，则使用错误参数进行的连接可能可以连上。

**dataVersion** 可选，STRING 类型标量。可以指定华泰 INSIGHT 数据 schema 的版本。目前仅支持 "3.2.8" 版本支持 "3.2.8"，"3.2.11" 。"3.2.11" 版本 Order 数据较 "3.2.8" 版本多了字段 TradeQty。

**backupList** 可选，STRING 类型向量，表示 insight 服务器的 IP 地址。如果有多个服务器，可以通过此参数实现与 Insight 服务器之间的高可用。地址需要以 IP:PORT 形式填写，如：218.94.125.135:8162。

### subscribe

**语法**

```
insight::subscribe(handle, marketDataTypes, securityIDSource, securityType)
```

**详情**

订阅数据，并将所订阅的数据保存在由 connect 的 handles 参数指定的表中。

注意：插件所接收的数据不会对华泰 INSIGHT 本身的倍率进行处理，使用时倍率的转换请参考华泰 INSIGHT 数据字典的相关介绍，本文不做赘述。

**参数**

**handle** `connect` 的返回值。

**marketDataTypes** STRING 类型向量，表示行情数据类型，支持以下值：MD\_TICK, MD\_ORDER, MD\_TRANSACTION, MD\_ORDER\_TRANSACTION 和 MD\_SECURITY\_LENDING。MD\_ORDER\_TRANSACTION 为特殊的订阅类型，指的是逐笔合成类型，其他类型均与 insight 规定的 EMarketDataType 枚举类型含义相同。

**securityIDSource** STRING 类型标量，表示交易所类型，支持以下值：XSHE, XSHG, CCFX, CSI, XBSE, XDCE, XSGE, NEEQ, XZCE, HKSC, HGHQ, CNI。类型含义与 Insight 规定的 ESecurityIDSource 枚举类型含义相同，具体含义详见华泰 Insight 官方数据字典。

**securityType** STRING 类型标量，表示产品类型，支持以下值：StockType, FundType, BondType, IndexType, FuturesType, OptionType。类型含义与 insight 规定的 ESecurityType 枚举类型含义相同，具体含义详见华泰 INSIGHT 官方数据字典。

### unsubscribe

**语法**

```
insight::unsubscribe(handle)
```

**详情**

取消当前所有订阅。

**参数**

**handle** insight 连接句柄，即 `connect` 函数的返回值。

### close

**语法**

`insight::close(handle)`

**详情**

关闭连接。

**参数**

**handle** `connect` 的返回值。

**示例**

```
insight::close(handle)
```

### getSchema

**语法**

```
insight::getSchema(dataType, [option], [dataVersion="3.2.8"])
```

**详情**

获取对应表结构。返回一个表，包含 name 和 type 两列。

**参数**

**dataType** STRING 类型标量，指需要获取 schema 的类型 OrderTransaction, StockTick, IndexTick, FuturesTick, Transaction, Order, FundTick, BondTick, OptionTick 或 OrderTransaction。

**option** 可选，是字典类型，表示扩展参数，key 为 STRING 类型，value 为 BOOL 类型。当前支持 ReceivedTime, OutputElapsed。
ReceivedTime 表示是否获取插件收到行情数据的时间戳，默认为 true。其指定为 dict(["ReceivedTime"],[true]) 时，getSchema 获取的表结构中将包含插件收到行情数据的时间戳列。
OutputElapsed 表示是否获取 Insight 插件 接收数据处理的时延，默认为 false。其指定为 dict(["OutputElapsed"], [true]) 时，getSchema 获取的表结构中将包含插件收到行情数据的时延列。时延的定义：'insight 回调函数返回数据' 到 '准备开始 transform' 处理，或准备 append 到共享流表前’ 这段时间。该列的单位为纳秒。

**dataVersion** 可选，STRING 类型标量，用于指定华泰 INSIGHT 数据 schema 的版本。目前支持 "3.2.8"，"3.2.11" 。"3.2.11" 版本 Order 数据较 "3.2.8" 版本多了字段 TradeQty。

### getStatus

**语法**

```
insight::getStatus(handle)
```

**详情**

返回一个表格，包含各种已订阅数据的状态信息，包含数据类型 StockTick, IndexTick, FuturesTick, OrderTransaction, Transaction, Order, FundTick, BondTick，OptionTick 或 SecurityLending。

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| **topicType** | 订阅的名称 | STRING |
| **channelNo** | OrderTransaction 分 channel 订阅时的 channel号 | INT |
| **startTime** | 订阅开始的时间 | NANOTIMESTAMP |
| **endTime** | 订阅结束的时间 | NANOTIMESTAMP |
| **firstMsgTime** | 第一条消息收到的时间 | NANOTIMESTAMP |
| **lastMsgTime** | 最后一条消息收到的时间 | NANOTIMESTAMP |
| **processedMsgCount** | 已经处理的消息数 | LONG |
| **lastErrMsg** | 最后一条错误信息 | STRING |
| **failedMsgCount** | 处理失败的消息数 | LONG |
| **lastFailedTimestamp** | 最后一条错误消息发生的时间 | NANOTIMESTAMP |
| **subscribeInfo** | 该订阅涉及的市场和投资品类型 | STRING |

**参数**

**handle** insight 连接句柄，即 `connect` 函数的返回值。

### getHandle

**语法**

```
handle = insight::getHandle()
```

**详情**

返回已有的 insight 连接句柄，如果插件没有被连接过，会抛出异常。

## 示例

1. 加载插件

   ```
   loadPlugin('insight');
   ```
2. 创建用于保存订阅数据的表

   ```
   stockTickSchema = insight::getSchema(`StockTick);
   share streamTable(10000:0, stockTickSchema[`name], stockTickSchema[`type]) as stockTickTable;
   ```
3. 连接服务器

   ```
   ip = "168.61.69.192";
   port = 10317;
   user = "mdc-flow-client-25-36";
   password = "mdc-vss-shlv1";

   handles = dict([`StockTick], [stockTickTable]);
   tcpClient = insight::connect(handles, ip, port, user, password);
   ```
4. 订阅

   ```
   insight::subscribe(tcpClient, `MD_TICK`MD_ORDER`MD_TRANSACTION, `XSHG, `StockType);
   ```
5. 取消订阅

   ```
   insight::unsubscribe(tcpClient);
   ```
6. 关闭连接

   ```
   insight::close(tcpClient);
   ```
