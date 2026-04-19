<!-- Auto-mirrored from upstream `documentation-main/plugins/signal/sipui2.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SipUI2

DolphinDB SipUI2 插件通过使用中畅原生 API（SipUI2）来订阅实时行情，包括沪深市场的股票、基金、债券的快照和沪深市场的逐笔行情，并将数据存入
DolphinDB 的数据表。

## 安装插件

### 版本要求

DolphinDB Server：2.00.14/2.00.15/3.00.2 及更高版本，支持 Linux x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("SipUI2")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("SipUI2")
   ```

## 接口说明

### connect

**语法**

```
SipUI2::connect(id, username, password, hosts, ports, [option])
```

**详情**

连接中畅行情服务器。如果连接成功则返回一个句柄。如果发生断线重连，则依次尝试由 hosts/ports 指定的各个服务器地址。

**参数**

**id** STRING 类型标量，表示连接的唯一标识。要求全局唯一，且不能为空字符串。

**username** STRING 类型标量，表示行情服务器的用户名。

**password** STRING 类型标量，表示行情服务器的密码。

**hosts** STRING 类型向量，表示服务器 IP 列表，需要和端口列表数量相同。

**ports** 整型向量，表示服务器端口列表。

**option** 可选参数，字典类型，表示扩展参数。其键支持 "receiveTime"，"OutputElapsed"。其中：

* “receiveTime” 布尔值，表示是否获取插件收到行情数据的时间戳。
* “OutputElapsed” 布尔值，表示是否获取插件从收到行情到准备插入流表的时延，单位是纳秒。

### subscribe

**语法**

```
SipUI2::subscribe(handle, codeList, outputTable)
```

**详情**

订阅实时行情，目前支持沪深市场的股票、基金、债券的快照和沪深市场的逐笔行情。

注意：`subscribe` 是异步接口，服务器端的错误（如非法订阅）不会直接体现在函数返回值中。如需获取相关错误信息，请调用
`getStatus` 查看服务器状态。

**参数**

**handle**
`connect` 接口返回的句柄。

**codeList** STRING 类型向量，表示合约数组。

**outputTable** 一个字典，用来指定输出表。其 key 类型是 STRING，value 必须是共享表。目前仅支持如下 key：

* "FundSnapshot"：表示基金快照（证券代码前缀为 5、15、16、18）
* "StockSnapshot"：表示股票快照（证券代码前缀为 6、00、30）
* "BondSnapshot"：表示债券快照（指除基金和股票快照以外的所有快照）
* "SHZS"：上海证券市场逐笔合并行情
* "SZZS"：深圳证券市场逐笔合并行情
* "SZXZC"：深圳债券逐笔行情
* "SHXZS”：上海债券逐笔行情

### unsubscribe

**语法**

```
SipUI2::unsubscribe(handle, [codeList])
```

**详情**

取消对行情数据的订阅。

**参数**

**handle**
`connect` 接口返回的句柄。

**codeList** 可选参数，STRING 类型向量，表示需要取消订阅的合约数组。不填该参数表示取消所有订阅。

### close

**语法**

```
SipUI2::close(handle)
```

**详情**

关闭当前连接。

**参数**

**handle**
`connect` 接口返回的句柄。

### getSchema

**语法**

```
SipUI2::getSchema(dataType, [option])
```

**详情**

获取行情数据的表结构。返回一个表，包含三列：name，type 和 typeInt，分别表示该行情表中字段的名字，字段类型的名称和类型的枚举值。

**参数**

**dataType** STRING 类型标量，表示行情数据的类型。可取值与 `subscribe` 接口中
*outputTable* 字典的 key 一致。

**option** 可选参数，字典类型，表示扩展参数。含义同 `connect` 接口中的
*option*。

### getStatus

**语法**

```
SipUI2::getStatus(handle)
```

**详情**

获取订阅数据的状态。返回一个表格：

| 列名 | 含义 |
| --- | --- |
| startTime | 订阅开始的时间 |
| endTime | 订阅结束的时间 |
| firstMsgTime | 第一条消息收到的时间 |
| lastMsgTime | 最后一条消息收到的时间 |
| processedMsgCount | 已经处理的消息数 |
| lastErrMsg | 最后一条错误信息 |
| failedMsgCount | 处理失败的消息数 |
| lastFailedTimestamp | 最后一条错误消息发生的时间 |

**参数**

**handle**
`connect` 接口返回的句柄。

### getHandle

**语法**

```
SipUI2::getHandle([id])
```

**详情**

获取当前已建立的连接句柄。若指定 *id*，则返回对应的句柄，否则返回一个包含所有当前句柄的字典。

**参数**

**id** 字符串标量，可选参数，表示连接的唯一标识。

## 使用示例

```
optionDic = dict(STRING, ANY);
optionDic["receiveTime"] = true
optionDic["OutputElapsed"] = true
handle = SipUI2::connect("con1", "user1", "password", ["192.168.57.103"], [10000], optionDic)
handle=SipUI2::getHandle(`con1)
SipUI2::getStatus(handle)
FundSchema = SipUI2::getSchema("FundSnapshot", optionDic)
StockSchema = SipUI2::getSchema("StockSnapshot", optionDic)
BondSchema = SipUI2::getSchema("BondSnapshot", optionDic)
SHZSSchema = SipUI2::getSchema("SHZS", optionDic)
SZZSSchema = SipUI2::getSchema("SZZS", optionDic)
share  streamTable(1:0, FundSchema.name, FundSchema.typeInt) as FundTable
share  streamTable(1:0, StockSchema.name, StockSchema.typeInt) as StockTable
share  streamTable(1:0, BondSchema.name, BondSchema.typeInt) as BondTable
share  streamTable(1:0, SHZSSchema.name, SHZSSchema.typeInt) as SHZSTable
share  streamTable(1:0, SZZSSchema.name, SZZSSchema.typeInt) as SZZSTable
tableDic = dict(STRING, ANY);
tableDic["FundSnapshot"] = FundTable
tableDic["StockSnapshot"] = StockTable
tableDic["BondSnapshot"] = BondTable
tableDic["SHZS"] = SHZSTable
tableDic["SZZS"] = SZZSTable
enableTablePersistence(table=FundTable, cacheSize=100000, retentionMinutes=30)
enableTablePersistence(table=StockTable, cacheSize=100000, retentionMinutes=30)
enableTablePersistence(table=BondTable, cacheSize=100000, retentionMinutes=30)
enableTablePersistence(table=SHZSTable, cacheSize=100000, retentionMinutes=30)
enableTablePersistence(table=SZZSTable, cacheSize=100000, retentionMinutes=30)
SipUI2::subscribe(handle, ["SH.*.L2", "SZ.*.L2", "SH.*.ZS", "SZ.*.ZS"], tableDic)
SipUI2::unsubscribe(handle)
SipUI2::close(handle)
```
