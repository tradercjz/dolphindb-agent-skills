<!-- Auto-mirrored from upstream `documentation-main/plugins/amdquote/amdhistory.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# amdHistory

为了方便在 DolphinDB 中对 AMD 历史行情数据进行分析与建模，DolphinDB 提供了 amdHistory 插件。该插件基于华锐 AMD
历史行情服务接口开发，可以将 AMD 历史数据导入到 DolphinDB 的库表中。amdHistory
插件目前支持股票、期货、期权等全品类历史行情，包括逐笔成交、逐笔委托、快照等数据类型。

## 安装插件

### 版本要求

DolphinDB Server：2.00.10 及更高版本，支持 Linux x86-64。

AMD SDK 版本：V4.5.3.240202-rc3.4。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("amdHistory")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("amdHistory")
   ```

注：

不能同时创建 amdQuote 和 amdHistory 两个连接。

## 接口说明

### connect

**语法**

```
amdHistory::connect(username, password, host, port, [option])
```

**详情**

连接 AMD 历史行情服务器。如果连接成功则返回一个句柄。目前只能创建一个句柄。

**参数**

**username** STRING 类型标量，AMD 行情服务器的用户名。

**password** STRING 类型标量，AMD 行情服务器的密码。

**host** STRING 类型标量，AMD 行情服务器 IP 列表，需要和端口列表数量相同。

**port** 为整型标量，AMD 行情服务器端口列表，需要和 IP 列表数量相同。

**option** 可选参数，一个字典，表示扩展参数，类型为<STRING, ANY>。其中：

* Timeout 表示超时时间，单位为分钟。其值为整型，取值范围为1- 60，默认值为1。

### query

**语法**

```
amdHistory::query(handle, marketType, dataType, security, date, beginTime, endTime, table, [ignoredColumnNum = 0])
```

**详情**

通过指定市场类型、证券代码等参数来查询历史数据，并将结果记录到表中。

**参数**

**handle**
`connect` 接口返回的句柄。

**marketType**整型标量，表示市场类型。2：北交所，3：上期所，4：中金所，5：大商所，6：郑商所，7：上海国际能源交易中心，101：上交所，102：深交所

**dataType** STRING 类型标量，表示行情的类型。

| 行情类型 | 含义 | 说明 |
| --- | --- | --- |
| order | 逐笔委托 | 对应 AMD 插件中的 order、fundOrder、bondOrder 三种行情类型，有效数据只包含前12列，其余列填充为空值。 |
| execution | 逐笔成交 | 对应 AMD 插件中的 execution、fundExecution、bondExecution 三种行情类型。 |
| snapshot | 现货（股债基）快照 | 对应 AMD 插件中的 snapshot、fundSnapshot、bondSnapshot 三种行情类型，有效数据只包含前65列，其余列填充为空值。 |
| indexSnapshot | 指数快照 | 对应 AMD 插件中的 index 行情类型，有效数据包含前12列，其余列填充为空值。 |
| optionSnapshot | 期权快照 | 对应 AMD 插件中的 option 行情类型，有效数据包含前39列，其余列填充为空值。 |
| futureSnapshot | 期货快照 | 对应 AMD 插件中的 future 行情类型，有效数据包含50列。如下列被填充空值：exchangeInstId、exchangeInstGroupid、hisHighPrice、hisLowPrice、arbiType、instrumentId1、instrumentId2、instrumentName。 |
| HKTSnapshot | 港股快照 | AMD 插件中无对应行情 |

**security** STRING 类型标量，表示证券代码。

**date** DATE 类型标量，表示查询日期。

**beginTime** TIME 类型标量，表示查询开始时间。

**endTime** TIME 类型标量，表示查询结束时间。

**table** 表示要追加历史数据的表。

**ignoredColumnNum** 整型标量，表示需要忽略的列的数量，默认为0。为了与 AMD 行情插件的表结构一致，需要忽略可能存在的
'ReceivedTime'、'DailyIndex'、'OutputElapsed' 三列，并为这些列插入空值。

### getSchema

**语法**

```
amdHistory::getSchema(dataType)
```

**详情**

获取行情数据的表结构。返回一个表，包含三列：name，typeString 和 typeInt，分别表示该行情表中字段的名字，字段类型的名称和类型的枚举值。与
AMD 插件对应的行情表相同。

**参数**

**dataType** STRING 类型标量，表示行情的类型。可选值与 query 接口中 dataType 参数相同。

### getHandle

**语法**

```
amdHistory::getHandle()
```

**详情**

获取当前已有的连接句柄。如果不存在连接句柄，则抛出异常。

### close

**语法**

```
amdHistory::close(handle)
```

**详情**

断开连接，销毁句柄。

**参数**

**handle**
`connect` 接口返回的句柄。

### queryCodeTable

**语法**

```
amdHistory::queryCodeTable(handle)
```

**详情**

返回服务端存储的代码表，包含如下几列：

* securityCode： 交易所证券代码
* symbol：证券简称
* englishName： 英文简称
* marketType： 市场类型
* securityType： 证券类别
* currency：币种

**参数**

**handle**
`connect` 接口返回的句柄。

## 示例

```
loadPlugin("amdHistory")
handle = amdHistory::connect("SJLH001", "SJLH001", "192.168.179.49", 9200)
indexTableSchema = amdHistory::getSchema("indexSnapshot")
share  table(1:0, indexTableSchema.name, indexTableSchema.typeInt) as indexTable
exeSchema = amdHistory::getSchema("execution")
share  table(1:0, exeSchema.name, exeSchema.typeInt) as exeTable
snapshotSchema = amdHistory::getSchema("snapshot")
share  table(1:0, snapshotSchema.name, snapshotSchema.typeInt) as snapshotTable
//marketType   101: Shanghai  102: Shenzhen
//dataType       "order" : 逐笔委托;    "execution": 逐笔成交;     "snapshot": 现货（股债基）快照;
// 	            "indexSnapshot" : 指数快照;   "optionSnapshot": 期权快照;    "futureSnapshot" : 期货快照
def queryHistory(handle, marketType, dataType, security, startDate, endDate, startTime, endTime, table) {
	for(d in startDate .. endDate){
		result = amdHistory::query(handle, 101, dataType, security ,d, startTime, endTime, table)
		print(d + "  " + result)
	}
}
queryHistory(handle, 101, "snapshot", "110096", 2025.02.17, 2025.03.12, 09:00:00.000, 16:00:00.000, snapshotTable)
amdHistory::close(handle)
```
