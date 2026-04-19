<!-- Auto-mirrored from upstream `documentation-main/plugins/quick_fix.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# QuickFix

DolphinDB QuickFix 插件基于全球金融行业通用的 FIX
协议标准，为机构用户提供银行间市场现券买卖行情的实时接入能力。该插件具备协议标准化、数据直达、解析高效以及系统稳定等特点，能够满足实时定价、风险监控和交易决策等核心业务场景的需求，实现对现券市场报价与成交数据的无缝对接与流式处理。

该插件通过实时接收并解析 FIX 协议报文，获取银行间市场现券交易行情，并将数据异步写入 DolphinDB
流数据表，便于后续开展实时分析、策略计算以及历史数据存储。目前，该插件仅支持基于 FIX 协议扩展的特定数据源消息类型（如森浦的 5100、5102 消息类型）。

## 安装插件

### 版本要求

DolphinDB Server 2.00.14 及更高版本，支持 Linux x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.net/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("QuickFix")
   ```
3. 用 `loadPlugin`
   命令加载插件。

   ```
   loadPlugin("QuickFix")
   ```

## 函数接口

### connect

**语法**

```
QuickFix::connect(id, configFilePath, outputTable)
```

**详情**

用于连接 FIX 协议服务器，并接收实时消息数据。函数返回一个连接句柄，同时将接收到的消息写入指定的表中，便于后续处理与分析。

注意：

* 配置文件通常包含如下内容：

  ```
  TransportDataDictionary=./FIXT11.xml
  AppDataDictionary=./FIX50SP2.xml
  ```

  上述路径为相对路径，相对路径的起点为 DolphinDB 工作目录（可通过
  `getWorkDir()` 查看）。

* 当需要创建多个连接时，必须注意以下约束：

  + 不同连接不能使用完全相同的配置文件内容。
  + 每个连接必须对应唯一的 FIX Session（Session 唯一性由配置文件中的
    BeginString、SenderCompID 以及 TargetCompID 共同决定）。如果多个连接中包含相同
    Session，可能会导致未定义行为、 程序异常、甚至进程崩溃。
  + 在连接过程中，系统和服务端会持久化部分关键数据，请勿在连接过程中随意更换执行目录（例如升级 DolphinDB
    版本后切换目录），但仍使用相同配置重新连接，可能会出现登录失败。

**参数**

**id** STRING 类型标量，用于标识当前连接实例的唯一 ID。要求全局唯一，不能为空字符串。

**configFilePath** STRING 类型标量，指定 FIX 连接所需的配置文件路径（通常为 QuickFIX
配置文件），必须是绝对路径。

**outputTable** 字典 ， key 是字符串，表示消息类型（目前支持 5100 和 5102），value 是表。关于表的
schema，参考附录。建议使用 `getSchema` 获取目标数据的 schema，根据该 schema 创建输出表。

**返回值**

返回一个连接句柄。

### Close

**语法**

```
QuickFix::close(handle)
```

**详情**

关闭当前连接。

**参数**

**handle**
`connect` 接口返回的句柄。

**返回值**

无。

### getStatus

**语法**

```
QuickFix::getStatus(handle)
```

**详情**

获取已订阅数据的状态。

**参数**

**handle**
`connect` 接口返回的句柄。

**返回值**

返回一个表格，包含各种已订阅数据的状态。

| 列名 | 含义 | 类型 |
| --- | --- | --- |
| startTime | 订阅开始的时间 | TIMESTAMP |
| firstMsgTime | 第一条消息收到的时间 | TIMESTAMP |
| lastMsgTime | 最后一条消息收到的时间 | TIMESTAMP |
| processedMsgCount | 已经处理的消息数 | LONG |
| lastErrMsg | 最后一条错误信息 | STRING |
| failedMsgCount | 处理失败的消息数 | LONG |
| lastFailedTimestamp | 最后一条错误发生的时间 | TIMESTAMP |

### getSchema

**语法**

```
QuickFix::getSchema(dataType)
```

**详情**

获取行情数据的表结构。

**参数**

**dataType** STRING 类型标量，表示行情的类型。目前支持 "5100" 和 "5102"。

**返回值**

返回一个表，包含三列：name，type 和 typeInt，分别表示该行情表中字段的名字、字段数据类型的名称、字段数据类型对应 ID。数据类型和 ID
的对应关系可以参考数据类型表。

### getHandle

**语法**

```
QuickFix::getHandle([id])
```

**详情**

获取当前已有的连接句柄。

**参数**

**id** 字符串标量，可选参数，表示连接标识，对应于调用 `connect` 接口时指定的 *id*。

**返回值**

* 指定 *id* 时，返回该 *id* 标识的 handle。
* 不指定 *id* 时，返回一个字典，包含所有当前存在的 handle。

## 使用示例

```
// 加载插件
loadPlugin("QuickFix")
go
version()
getWorkDir()
outputTable = dict(STRING, ANY)
// 创建共享流表，用于接收行情数据
schema5100 = QuickFix::getSchema("5100")
share streamTable(10000:0, schema5100 [`name], schema5100 [`typeString]) as sum5100Table
schema5102 = QuickFix::getSchema("5102")
share streamTable(10000:0, schema5102 [`name], schema5102 [`typeString]) as sum5102Table
outputTable["5100"] = sum5100Table
outputTable["5102"] = sum5102Table
// 连接 FIX 协议服务器，将森浦 5100 和 5102 行情数据写入 outputTable
handle = QuickFix::connect("id", "/yourConfigPath/client_5.0sp2.cfg", outputTable)

QuickFix::getStatus(handle)
QuickFix::close(QuickFix::getHandle("id"))
```

## 附录

**森浦 5100 行情表的 schema**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| DataModel | STRING | 数据模型 |
| IC | STRING | 森浦代码 |
| ContributorID | STRING | 报价商 |
| MarketDataTime | TIMESTAMP | 市场数据时间 |
| MessageSeq | STRING | 消息序号 |
| SecurityID | STRING | 债券代码 |
| BondName | STRING | 债券简称 |
| DisplayListedMarket | STRING | 发行市场 |
| BidQuoteId | STRING | 买入编号 |
| AskQuoteId | STRING | 卖出编号 |
| BidQuoteStatus | INT | 买入报价状态：  * 0：正常 * 2：失效 |
| AskQuoteStatus | INT | 卖出报价状态：  * 0：正常 * 2：失效 |
| BidYield | DOUBLE | 买收益率 |
| AskYield | DOUBLE | 卖收益率 |
| BidPx | DOUBLE | 买价 |
| OfferPx | DOUBLE | 卖价 |
| BidPriceType | INT | 买入价格类型：  * 0：意向报价 * 1：净价 * 2：全价 * 3：收益率 * 4：利差 * 8：经纪商未指定 |
| AskPriceType | INT | 卖出价格类型：  * 0：意向报价 * 1：净价 * 2：全价 * 3：收益率 * 4：利差 * 8：经纪商未指定 |
| BidPrice | DOUBLE | 买入净价 |
| AskPrice | DOUBLE | 卖出净价 |
| BidDirtyPrice | DOUBLE | 买入全价 |
| AskDirtyPrice | DOUBLE | 卖出全价 |
| BidVolume | DOUBLE | 买量 |
| AskVolume | DOUBLE | 卖量 |
| MultiBidVolume | STRING | 多笔买量 |
| MultiAskVolume | STRING | 多笔卖量 |
| BidBargainFlag | INT | 买方可议价标志：  * 0 或者空：不可议价 * 1：可议价 * 2：可自由议价/允许更大幅度议价 |
| AskBargainFlag | INT | 卖方可议价标志：  * 0 或者空：不可议价 * 1：可议价 * 2：可自由议价/允许更大幅度议价 |
| BidPriceDesc | STRING | 买入价格描述 |
| AskPriceDesc | STRING | 卖出价格描述 |
| BidRelationFlag | INT | 买方报价的打包和 OCO 标志：  * 0 或空：无 OCO 无打包 * 1：OCO * 2：打包 |
| AskRelationFlag | INT | 卖方报价的打包和 OCO 标志：  * 0 或空：无 OCO 无打包 * 1：OCO * 2：打包 |
| BidExerciseFlag | INT | 买方行权标志：  * 0：行权收益率 * 1：到期收益率 * 空：经纪未提供信息 |
| AskExerciseFlag | INT | 卖方行权标志：  * 0：行权收益率 * 1：到期收益率 * 空：经纪未提供信息 |
| BidYldCalculatedExerciseFlag | STRING | 买方计算收益类型标识 ：  * 0：行权收益率 * 1：到期收益率 |
| AskYldCalculatedExerciseFlag | STRING | 卖方计算收益类型标识 ：  * 0：行权收益率 * 1：到期收益率 |
| BidSsDetect | INT | 买价异常是否标识  * 1：正常 * 2：异常 |
| OfrSsDetect | INT | 卖价异常是否标识  * 1：正常 * 2：异常 |
| Bidinterpret | STRING | 买方拆解后的报价 |
| Ofrinterpret | STRING | 卖方拆解后的报价 |

**森浦 5102 行情表的 schema**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| DataModel | STRING | 数据模型 |
| IC | STRING | 森浦代码 |
| ContributorID | STRING | 报价商 |
| MarketDataTime | TIMESTAMP | 市场数据时间 |
| ModifyTime | TIME | 数据更改时间 |
| MessageSeq | STRING | 消息序号 |
| SecurityID | STRING | 债券代码 |
| BondName | STRING | 债券简称 |
| DisplayListedMarket | STRING | 发行市场 |
| ExecID | STRING | 成交编号 |
| DealStatus | INT | 成交状态：  * 0：正常 * 2：作废 |
| TradeMethod | INT | 成交方式 |
| Yield | DOUBLE | 收益率 |
| TradePx | DOUBLE | 成交价 |
| PriceType | INT | 价格类型 |
| TradePrice | DOUBLE | 成交净价 |
| DirtyPrice | DOUBLE | 成交全价 |
| SettlSpeed | STRING | 清算速度 |
| SettlementSpeed2 | STRING | 清算速度分类 |
| ExerciseFlag | INT | 行权标志 |
| YldCalculatedExerciseFlag | STRING | 计算行权标识 |
| SettlDate | DATE | 结算日期 |
| TradePxSsDetect | INT | 成交异常标识 |
| Ofr0 | DOUBLE | 经纪商报卖 T+0 收益率 |
| Bid0 | DOUBLE | 经纪商报买 T+0 收益率 |
| Ofr1 | DOUBLE | 经纪商报卖 T+1 收益率 |
| Bid1 | DOUBLE | 经纪商报买 T+1 收益率 |
| Ofr2 | DOUBLE | 经纪商报卖远期收益率 |
| Bid2 | DOUBLE | 经纪商报买远期收益率 |
| AllBid1 | DOUBLE | 所有经纪商报买 T+1 收益率 |
| AllOfr1 | DOUBLE | 所有经纪商报卖 T+1 收益率 |
| Normal | STRING | 经纪商成交报价比较异常标签 |
