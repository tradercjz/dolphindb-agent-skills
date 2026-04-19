<!-- Auto-mirrored from upstream `documentation-main/plugins/SSEQuotationFile.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SSEQuotationFile

上交所提供多种行情文件的转发服务，例如港股通行情、指数通行情等。通过 DolphinDB 的 SSEQuotationFile 插件，用户可以解析上交所提供的这些行情文件，将信息存储到 DolphinDB 的表中。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("SSEQuotationFile")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("SSEQuotationFile")
   ```

## 接口说明

### subscribe

**语法**

```
SSEQuotationFile::subscribe(fileType, path, table, [option])
```

**详情**

开始解析行情文件，同一个类型的文件不能重复订阅。每当文件被修改时解析一次。

3.00.1.4/2.00.13.4 版本新增：

* MktStatus 列，表示 mktdt04 行情文件头中的交易状态信息。详细说明如下：

  + 0：全日收市
  + 1：输入买卖盘（开盘集合竞价时段）
  + 2：对盘（开盘集合竞价时段）
  + 3：持续交易
* MDTime 列，表示 mktdt04 行情文件头中的文件生成时间。

**参数**

**fileType** STRING 类型标量，表示行情文件类型。当前支持两种，分别是港股通文件”mktdt04.txt”以及中证指数”csiYYYYMMDD.txt”。

**path** STRING 类型标量，表示文件路径的绝对地址。

**table** 一个表，完成解析的数据会追加到该表中。

**option** 可选参数，一个 key 类型为 STRING 的字典，包含如下配置项：

| 配置项 | 值类型 | 说明 |
| --- | --- | --- |
| receiveTime | BOOL | 可选参数，用于设定是否将接收到数据的时间并为表的最后一列。类型为 NANOTIMESTAMP。true 表示增加该列；默认为 false，表示不增加。 |
| OutputElapsed | BOOL | 可选参数，用于设定是否为行情表增加最后一列。该列数据类型为 LONG，表示插件从收到行情开始到准备插入流表为止的延时，单位为纳秒。true 表示增加该列；默认为 false，表示不增加。 |

### unsubscribe

**语法**

```
SSEQuotationFile::unsubscribe(fileType)
```

**详情**

停止解析行情文件。

**参数**

**fileType** STRING 类型标量，表示行情文件类型。当前支持两种，分别是港股通文件”mktdt04.txt”以及中证指数”csiYYYYMMDD.txt”。

### getStatus

**语法**

```
SSEQuotationFile::getStatus()
```

**详情**

获取解析状态。返回一个表，包含如下列：类型（SYMBOL）, 开始时间（NANOTIMESTAMP）, 结束时间（NANOTIMESTAMP）, 成功解析条数（LONG），失败解析条数（LONG）， 最后一条消息时间（NANOTIMESTAMP），最后一条错误时间（NANOTIMESTAMP）, 最后一条错误消息时间（STRING）。

### getSchema

**语法**

```
SSEQuotationFile::getSchema(fileType, [outputRecvTime], [outputElapsed])
```

**详情**

获取存储对应类型行情文件的表的 shema。返回一个表，包含三列，分别是 name, typeString, typeInt，分别表示该行情表中字段的名字、字段类型的名称和类型的枚举值。

**参数**

**fileType** STRING 类型标量，表示行情文件类型。当前支持两种，分别是港股通文件”mktdt04.txt”以及中证指数”csiYYYYMMDD.txt”。

**outputRecvTime** BOOL 类型标量，可选参数，表示是否需要包含 receiveTime 列，默认为 false，表示不需要。如果在 `subscribe` 时，指定了 receiveTime 配置，那么该参数须设置为 true。

**outputElapsed** BOOL 类型标量，可选参数，表示返回的 shcmea 是否包含 elapsedTime 列。默认为 false，表示不包含。

## 使用示例

```
t = table(1:0, `SecurityID`Symbol`SymbolEn`TradeVolume`TotalValueTraded`PreClosePx`NominalPrice`HighPrice`LowPrice`TradePrice`BuyPrice1`BuyVolume1`SellPrice1`SellVolume1`SecTradingStatus`Timestamp, [SYMBOL, SYMBOL, SYMBOL,LONG, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, DOUBLE, LONG, DOUBLE, LONG, SYMBOL, TIME])
SSEQuotationFile::subscribe("mktdt04.txt", "/home/luzhouzheng/code/lzz/bin/mktdt04.txt", t)

SSEQuotationFile::unsubscribe("mktdt04.txt")

SSEQuotationFile::getStatus()

SSEQuotationFile::getSchema("mktdt04.txt", true)
SSEQuotationFile::getSchema("csiYYYYMMDD.txt", true)
```
