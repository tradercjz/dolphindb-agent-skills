<!-- Auto-mirrored from upstream `documentation-main/plugins/ASTTrader.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# ASTTrader

ASTTrader 插件用于对接恒生极速交易系统，支持高速下单、快速撤单、持仓查询等功能。借助该插件，用户可在 DolphinDB 中基于实时行情灵活实现多种交易策略。

## 安装插件

### 版本要求

DolphinDB Server：2.00.16/3.00.3 及更高版本，支持 Linux x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins`
   命令查看插件仓库中的插件信息。

   ```
   listRemotePlugins()
   ```
2. 使用 `installPlugin`
   命令完成插件安装。

   ```
   installPlugin("ASTTrader")
   ```
3. 使用 `loadPlugin`
   命令加载插件。

   ```
   loadPlugin("ASTTrader")
   ```

注：

定时任务，`onSnapshot` 以及
`onOrder`/`onTrade`
在不同线程中触发，因此存在同时触发的可能。

## 接口说明

### createASTEngine

**语法**

```
createASTEngine(name, config, dummyQuotationTable, eventCallbacks)
```

**详情**

创建一个实时交易引擎，会连接、登录、并订阅交易主推消息。订阅时指定的参数为获取最新的消息，以及按交易员过滤。

注：

在调用该接口之前，要确保 dolphindb 同目录下存在文件
StepMonitorSDK\_tradeapi.json 和 UST\_API\_Config.ini， 否则无法创建成功。

**参数**

**name** STRING 类型标量，表示交易引擎名称。

**config** 一个字典，表示交易引擎的配置项。字典的 key 是 STRING 类型，代表配置项的名称，value 是该配置项的具体配置：

| key | value 类型 | 含义 |
| --- | --- | --- |
| frontAddress | STRING 类型标量 | 必填项。前置服务器地址或者 UST Core 服务器地址，地址格式规范为：`tcp://[server-address]:[server-port];[server-address]:[server-port]` 。例如：`tcp://10.20.39.103:25555;10.20.39.103:26666`。 |
| operatorID | STRING 类型标量 | 必填项。交易员账号。 |
| password | STRING 类型标量 | 必填项。密码。 |
| IPAddress | STRING 类型标量 | 必填项。交易员IP地址。 |
| strategyGroup | STRING 类型标量 | 必填项。表示策略类型。目前支持：  * “StockOpt” ：股票期权（即将支持） * “Stock”：股票ETF |
| symbolColumnIndex | 整型标量 | 可选项。指示行情表中 symbol 列的下标，从0开始。如不指定该参数，则要求表中存在列名为 symbol 的列。 |
| context | 字典 | 可选项。作为各回调函数的第一个参数传入。如果要开启定时任务，需要指定一个同步字典。 |
| outputRecordInfo | 布尔值 | 可选项。是否将插件日志、回调函数中的 print 打印信息输出到一个记录表里。默认为 false。该表可以通过 `getRecordInfo` 接口获取，`clearRecordInfo` 接口清空。 |

**dummyQuotationTable** 一个与插入的行情数据表结构相同的表。

**eventCallbacks** 一个字典，表示策略回调函数。

### appendQuotationMsg

**语法**

```
appendQuotationMsg(engine, msg)
```

**详情**

向交易引擎输入实时行情。

如果一次 `appendQuotationMsg` 的表中如果出现多个相同的 symbol，只保留最后一个进行 onSnapshot
调用。

**参数**

**engine** 交易引擎句柄。

**msg** 行情输入表。要求 schema 与调用 `createASTengine` 时传入的
*dummyQuotationTable* 相同。并已按时间递增排序。

### submitOrder

**语法**

```
submitOrder(engine, msg)
```

**详情**

提交订单。返回一个 INT 数字，表示订单编号。

该接口异步提交订单信息，会立刻返回，提交结果通过 `onOrder` 接口来通知。

**参数**

**engine** 交易引擎句柄。

**msg** 一个字典，表示订单信息：

| key | value 类型 | 含义 |
| --- | --- | --- |
| account | STRING | 必填项。资金账号 |
| miniEntrustRatio | INT | 可选项。最小委托比例，取值区间为 [0, 100]，默认值为 100 |
| product | STRING | 必填项。产品。 |
| project | STRING | 必填项。项目。 |
| strategy | STRING | 可选项。策略。 |
| orders | Vector of Dict | 必填项。报单具体信息，是一个数组，其中每个元素都是一个字典，该字典要求如下表所示。 |
| exchange | STRING | 必填项。SSE 表示上交所，SZSE 代表深交所。 |
| symbol | STRING | 必填项。证券代码。 |
| direction | 数值类型 | 必填项。买卖方向，1代表买，2代表卖。 |
| price | 数值类型 | 必填项。报单价格 |
| volume | 数值类型 | 必填项。报单数量 |
| command | 数值类型 | 必填项。报单指令，支持的数值见文档[附录1](#topic_yrm_zkf_2gc)。 |
| remark | 数值类型 | 可选项。备注，可选值为[0,100]。 |

### cancelOrder

**语法**

```
cancelOrder(engine, msg)
```

**详情**

撤单。

**参数**

**engine** 交易引擎句柄。

**msg** 整型标量，表示订单编号。

### getPosition

**语法**

```
getPosition(engine, account, exchange, symbol)
```

**详情**

获取持仓信息。

不指定 *symbol* 时，返回表；指定 *symbol* 时返回字典。

**参数**

**engine** 交易引擎句柄。

**account** STRING 类型标量，表示资金账号。

**exchange** STRING 类型标量，可选参数，表示交易所代码：SSE 表示上交所，SZSE 代表深交所。

**symbol** 证券代码，可选参数。

**返回值**

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| account | STRING | 账号 |
| exchangeID | STRING | 交易所 |
| symbol | STRING | 证券代码 |
| positionVolume | DOUBLE | 持仓当前数量 |
| availablePositionVolume | DOUBLE | 可用持仓数量 |
| project | STRING | 项目 |
| positionCost | DOUBLE | 持仓成本 |
| positionCostPrice | DOUBLE | 持仓成本价 |
| accountID | STRING | 证券账号 |

### runInterval

**语法**

```
runInterval(engine, job, seconds, startTime, endTime)
```

**详情**

开启定时任务。该定时任务的最小间隔时间为 1 秒。

定时器每次会检查上次是否已经完成。如果在定时任务中做非常耗时的事情，下次定时任务会检查上次任务是否完成，如果已经完成，则触发定时任务，如果没有完成，则该次任务不执行，在日志中通知。

**参数**

**engine** 交易引擎句柄。

**job** 函数对象，只能有一个参数 *context*。

**seconds** 间隔，单位是秒。

**startTime**  SECOND 类型标量，表示开启时间。

**endTime** SECOND 类型标量，表示结束时间。

### stopTrade

**语法**

```
stopTrade(engine)
```

**详情**

主动停止交易，该接口会触发 finialize 回调。

**参数**

**engine** 交易引擎句柄。

### queryOrderInfo

**语法**

```
queryOrderInfo(engine, account, orderID)
```

**详情**

获取订单详细信息。

**参数**

**engine** 交易引擎句柄。

**account** 账户。

**orderID** `submitOrder` 接口返回的 orderID。

返回一个字典，信息如下

| key | value值类型 | 含义 |
| --- | --- | --- |
| account | STRING | 资产账户 |
| orderID | INT | 报单编码 |
| exchange | STRING | 交易所 |
| symbol | STRING | 证券代码 |
| direction | INT | 买卖方向 |
| price | DOUBLE | 报单价格 |
| volume | DOUBLE | 报单数量 |
| status | CHAR | 报单状态，可取值见文档[附录2](#topic_fxm_zkf_2gc) |
| tradeVolume | DOUBLE | 成交数量 |
| tradeBalance | DOUBLE | 成交金额 |
| cancelVolume | DOUBLE | 撤单数量 |
| insertDate | DATE | 报单日期 |
| insertTime | TIME | 报单时间 |
| confirmTime | TIME | 确认时间 |
| command | INT | 报单指令 |
| errorNo | INT | 错误号 |
| errorMsg | STRING | 错误信息 |

### getContext

**语法**

```
getContext(engine)
```

**详情**

获取 context。

**参数**

**engine**交易引擎句柄。

### getTradingAccount

**语法**

```
getTradingAccount(engine, account)
```

**详情**

获取账户资金信息。

**参数**

**engine** 交易引擎句柄。

**account** 账户。

### destroyASTEngine

**语法**

```
destroyASTEngine(engineName)
```

**详情**

阻塞直至 engine 被销毁。

注：

回调函数中只能使用 `stopTrade` 来中止交易，禁止使用
`destroyASTEngine`。

**参数**

**engineName** STRING 类型标量，表示引擎名称。

### getRecordInfo

**语法**

```
getRecordInfo(engine)
```

**详情**

获取该引擎中的信息记录表。

**参数**

**engine** 交易引擎句柄。

### clearRecordInfo

**语法**

```
clearRecordInfo(engine)
```

**详情**

清空该引擎中的信息记录表。

**参数**

**engine** 交易引擎句柄。

### getASTEngines

**语法**

```
getASTEngines()
```

**详情**

获取所有的交易引擎。返回一个字典，key 是引擎名字，value 是引擎句柄。

## 回调函数

### initialize

**语法**

```
def initialize(mutable context){}
```

**详情**

进行初始化，在创建引擎之后会调用一次。

**参数**

**context** 一个字典，表示全局上下文。

### onSnapshot

**语法**

```
def onSnapshot(mutable context, msg, indicator){}
```

**详情**

快照行情回调函数。

若同时收到某个标的的多条快照数据，将使用最新的数据触发回调，其他数据舍弃。

**参数**

**context** 一个字典，表示全局上下文。

**msg** 包含行情的字典。每次调用的 *msg* 对应一行行情。

**indicator** 订阅的指标，暂不生效。

### onOrder

**语法**

```
def onOrder(mutable context, orders){}
```

**详情**

委托回报回调函数，通过本引擎提交的每个订单状态发生变化时触发。

**参数**

**context** 一个字典，表示全局上下文。

**orders** 是一个字典，表示订单状态，包含以下键值：

| key | value 值类型 | 含义 |
| --- | --- | --- |
| account | STRING | 资产账户 |
| orderID | INT | 报单编码 |
| exchange | STRING | 交易所 |
| symbol | STRING | 证券代码 |
| direction | INT | 买卖方向 |
| price | DOUBLE | 报单价格 |
| volume | DOUBLE | 报单数量 |
| status | CHAR | 报单状态，可取值见[附录2](#topic_fxm_zkf_2gc) |
| tradeVolume | DOUBLE | 成交数量 |
| tradeBalance | DOUBLE | 成交金额 |
| cancelVolume | DOUBLE | 撤单数量 |
| insertTime | TIME | 报单时间 |
| confirmTime | TIME | 确认时间 |
| batchNo | INT | 委托批号 |
| command | INT | 报单指令 |
| errorNo | INT | 错误号 |
| errorMsg | STRING | 错误信息 |
| project | STRING | 项目 |
| strategy | STRING | 策略 |
| remark | INT | 备注 |

### onTrade

**语法**

```
def onTrade(mutable context, trade){}
```

**详情**

成交回报回调函数，有订单成交时触发。

**参数**

**context** 一个字典，表示全局上下文。

**trades** 一个字典，表示成交信息，包含以下键值：

| key | value值类型 | 含义 |
| --- | --- | --- |
| account | STRING | 资产账户 |
| tradeID | STRING | 成交编码 |
| orderID | INT | 报单编码 |
| exchange | STRING | 交易所 |
| symbol | STRING | 合约代码 |
| codeType | CHAR | 代码类型 |
| direction | INT | 买卖方向 |
| tradeVolume | DOUBLE | 成交数量 |
| tradePrice | DOUBLE | 成交价格 |
| tradeFee | DOUBLE | 成交费用 |
| tradeBalance | DOUBLE | 成交金额 |
| tradeTime | TIME | 成交时间 |
| tradingDay | DATE | 交易日 |
| project | STRING | 项目 |
| strategy | STRING | 策略 |

### finalize

**语法**

```
def finalize(mutable context){}
```

**详情**

结束时回调。

**参数**

**context** 一个字典，表示全局上下文。

## 使用示例

```
config = dict(STRING, ANY)
config["frontAddress"] = "tcp://127.0.0.1:23578"
config["operatorID"] = "1111"
config["password"] = "aaaa"
config["IPAddress"] = "127.0.0.1"
config["strategyGroup"] = "Stock"
config["context"] = syncDict(STRING, ANY, `context)
def job(mutable context) {
	writeLog("running job...")
	sleep(4000)
}
def initialize(mutable context) {
	writeLog("initialize")
	//nowTime = second(now())
	//ASTTrader::runInterval(context["engine"], job, 3,nowTime , nowTime+10)
}
def finalize(mutable context) {
	writeLog("finalize")
}
def onOrder( mutable contextDict,orders){
	writeLog("=== onOrder Start")
	writeLog(orders)
	writeLog("=== onOrder End")
}
def onOrderMonitor( mutable contextDict,orders){
	writeLog("=== onOrderMonitor Start")
	writeLog(orders)
	writeLog("=== onOrderMonitor End")
}
def onTrade(mutable contextDict,trades){
	writeLog("=== onTrade Start")
	writeLog(trades)
	writeLog("=== onTrade End")
}
def onSnapshot( mutable contextDict, msg, indicator = NULL){
	writeLog("onSnapshot start")
	print(msg)
	writeLog("onsnapshot end")
}
events = dict(STRING, ANY)
events["initialize"] = initialize
events["finalize"] = finalize
events["onOrder"] = onOrder
events["onOrderMonitor"] = onOrderMonitor
events["onTrade"] = onTrade
events["onSnapshot"] = onSnapshot
tb = table(`123445`223443`abcde as symbol,6 9 4 as v1, 1 4 3 as v2)
trader = ASTTrader::createASTEngine("12345", config, tb, events);
ASTTrader::appendQuotationMsg(trader, tb);
```

## 附录

### 1. 报单时支持的报单指令

| 报单指令 | 说明 |
| --- | --- |
| 1 | 限价 |
| 2 | 限价即时全部成交否则撤销 |
| 3 | 限价任意数量即时成交剩余撤销 |
| 4 | 限价止损 |
| 5 | 限价止盈 |
| 6 | 市价 |
| 7 | 市价即时全部成交否则撤销 |
| 8 | 市价任意数量即时成交剩余撤销 |
| 9 | 市价指定成交数量即时成交剩余撤销 |
| 10 | 市价止损 |
| 11 | 市价止盈 |
| 12 | 市价即时成交剩余转限价 |
| 13 | 五档市价即时成交剩余撤销 |
| 14 | 五档市价即时成交剩余转限价 |
| 15 | 最优价即时成交剩余转限价 |
| 16 | 最优价即时成交剩余撤销 |
| 17 | 最优价即时全部成交否则撤销 |
| 18 | 本方最优价转限价 |
| 19 | 对手方最优价申报 |

### 2. 报单状态

| 状态码 | 说明 |
| --- | --- |
| `'0'` | 未报 |
| `'1'` | 待报 |
| `'2'` | 已报 |
| `'3'` | 已报待撤 |
| `'4'` | 部成待撤 |
| `'5'` | 部撤 |
| `'6'` | 已撤 |
| `'7'` | 部成 |
| `'8'` | 已成 |
| `'9'` | 废单 |
| `'A'` | 待报待撤 |
