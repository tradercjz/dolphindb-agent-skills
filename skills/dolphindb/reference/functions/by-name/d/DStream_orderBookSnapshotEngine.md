# DStream::orderBookSnapshotEngine

首发版本：3.00.3

## 语法

`DStream::orderBookSnapshotEngine(exchange, orderbookDepth, intervalInMilli,
date, startTime, prevClose, inputColMap, [outputColMap], [outputCodeMap],
[outputIntervalOffsetMap], [checkRestrict], [maxPrice], [minPrice],
[userDefinedMetrics], [priceNullFill], [triggerType], [forceTriggerTime],
[precision], [orderBySeq], [skipCrossedMarket=true], [orderBookDetailDepth=0],
[orderBookAsArray=false],
[useSystemTime=false],[independentForceTriggerTime])`

## 详情

创建一个订单簿引擎。参考：createOrderBookSnapshotEngine。

## 参数

**exchange** 字符串标量，用于指定交易所及标的类别。可选参数：

* "XSHE" 或 "XSHESTOCK"：深交所股票
* "XSHEBOND"：深交所债券
* "XSHEFUND"：深交所基金
* "XSHG" 或 "XSHGSTOCK"：上交所股票
* "XSHGBOND"：上交所债券
* "XSHGFUND"：上交所基金

**orderbookDepth** 正整数，表示 orderbook 中最多能够显示的买卖报价的档位。

**intervalInMilli** 正整数，表示触发输出数据的时间间隔，即合成快照的时间频率，单位为毫秒。

**date** DATE 类型标量，表示交易日期。该参数和窗口右边界组合成输出表的 TIMESTAMP 列。

**startTime** TIME
类型标量，表示触发输出数据的起始时刻。引擎只会输出该参数指定时刻（规整后）之后的数据。

**prevClose** 字典，其 key 为字符串标量或向量，表示股票代码；其 value
为数值类型，表示对应于股票代码的上一个交易日的收盘价格。注意：若 value 为浮点型，则认为是真实价格，引擎处理过程中会乘以
*priceScale*，以匹配输入表中 priceColumn 字段的精度。若为整型，则视为已和 priceColumn
具备相同精度，不再进行缩放。

**inputColMap** 字典，将输入表中列字段的名称映射为引擎计算所需要的列。其中：

* key 为字符串类型，表示引擎所需要的固定的输入字段。具体字段名和含义见下表。注意，这些 key 区分大小写，必须全部指定，但顺序可以不固定。
* value 为字符串类型，表示输入表中对应的列名称。

| key | value 对应的字段类型 | 含义 |
| --- | --- | --- |
| "codeColumn" | SYMBOL | 标的代码（如300010.SZ） |
| "timeColumn" | TIME | 交易时间 |
| "typeColumn" | INT | 交易类型：  * 如果是逐笔委托单，则：1 表示市价；2 表示限价；3 表示本方最优；10 表示撤单（仅上交所）；11   市场状态（仅上交所） * 如果是逐笔成交单，则：0 表示成交；1 表示撤单（仅深交所） |
| "priceColumn" | LONG | 价格，由 *priceScale* 决定，默认是真实价格\*10000 |
| "qtyColumn" | LONG | 数量（股数） |
| "buyOrderColumn" | LONG | * 逐笔成交：对应其原始成交中的买方委托序号。 * 逐笔委托：   + 上交所：填充原始委托中的原始订单号，即上交所在新增、删除订单时用以标识订单的唯一编号（OrderNo     字段）   + 深交所：填充 0。此字段为深交所为了补全上交所数据格式而增加的冗余列 |
| "sellOrderColumn" | LONG | * 逐笔成交：对应其原始成交中的卖方委托序号。 * 逐笔委托：   + 上交所：填充原始委托中的原始订单号，即上交所在新增、删除订单时用以标识订单的唯一编号（OrderNo     字段）   + 深交所：填充 0。此字段深交所为了补全上交所数据格式而增加的冗余列 |
| "sideColumn" | INT | 买卖方向：1 表示买单；2 表示卖单 说明：   * 委托单的 BSFlag，必填 * 撤单的 BSFlag 由原始委托单决定买卖方向，必填 * 成交单的 BSFlag，不影响结果，非必填 |
| "msgTypeColumn" | INT | 数据类型：  * 0 表示逐笔委托； * 1 表示逐笔成交； * -1 表示产品状态。 |
| "seqColumn" | LONG | 一个通道内从 1 开始递增的逐笔数据序号。深交所为 appseqlnum 字段，若深交所数据中包含 index 字段，也可以使用 index；上交所为 bizIndex 字段。 |
| "receiveTime" | NANOTIMESTAMP | 逐笔数据的接收时间 |

注：

引擎规范了枚举类型中各枚举值的具体含义。输入表对应的枚举值必须遵守这个规范。比如枚举类型字段
sideColumn 所对应的输入表中的字段必须使用 1 代表买方向，2 代表卖方向。

**outputColMap** 可选参数，字符串向量，用于指定需要输出的字段名称，不区分大小写。为方便指定
*outputColMap*，用户可通过 `genOutputColumnsForOBSnapshotEngine`
函数生成需要输出的字段名称，将返回值的第一个元素赋值给 *outputColMap* 即可。

注：

`genOutputColumnsForOBSnapshotEngine`函数生成的字段列表中不包含以下字段：

* tradeDetail（成交明细）中的 tradeBuyOrderTypeList 和
  tradeSellOrderTypeList。

* withdrawDetail（撤单明细）中的
  withdrawBuyOrderNoList和withdrawSellOrderNoList。
* residualDetail（剩余委托明细）中的 ResidualBidOrderNoList 和
  ResidualAskOrderNoList。

如需要输出上述字段，请在 *outputColMap* 中手动添加。

**outputCodeMap**
可选参数，字符串向量，表示股票代码，例如："000803.SZ"。指定该参数后，将只输出指定股票对应的数据。

**outputIntervalOffsetMap**
可选参数，向量或字典，用于指定输出表中股票被触发计算的时间偏移量（单位：毫秒）。

* **计算逻辑**：引擎会根据偏移量重新定义各股票的快照边界。第一个窗口会自动包含从 *startTime* 到 *startTime
  + intervalInMilli + offset* 之间的所有逐笔数据，从而确保偏移期间产生的数据被纳入当条快照计算。
* **向量形式**：引擎将根据输入的股票数量自动将这些股票均匀分配到这些偏移量上。例如，`outputIntervalOffsetMap
  = [400, 500]`，表示引擎将自动将输入的股票均匀分成两部分，经过 intervalInMilli + 400(ms)
  后触发其中一部分股票的数据输出；经过 intervalInMilli + 500(ms) 后触发另一部分股票的数据输出。
* **字典形式**： key 为字符串类型，表示股票代码；其 value
  为整型，表示时间偏移量。例如：`outputIntervalOffsetMap
  =dict(["127053.sz","123082.SZ"],[400, 500])`，表示经过
  intervalInMilli + 400(ms) 后触发 127053.sz 股票的数据输出；经过 intervalInMilli + 500(ms)
  后触发 123082.SZ 股票的数据输出。

**checkRestrict** 可选参数，布尔值，默认值为 true，表示开启价格笼子机制；若设置为
false，则关闭笼子机制，此时会取消对股票交易的限制，创业板合成出的快照可能不正确。

注：

深交所对创业板标的（标的代码以 3 开头）设定了价格笼子。在 *checkRestrict*=true
时，引擎只会将标的代码的首字符是否为 3 作为是否执行价格笼子的判断标准。因此，在向引擎输入创业板数据时，标的代码必须以 3 开头。

**maxPrice** 可选参数，字典。其 key 为字符串类型，表示标的代码；其 value 为 DOUBLE 或 INT
类型，表示涨停价格。注意：若 *maxPrice* 为浮点型，则认为是真实价格，引擎处理过程中会乘以 *priceScale*，以匹配输入表中
priceColumn 字段的精度。若为整型，则视为已和 priceColumn 具备相同精度，不再进行缩放。

**minPrice** 可选参数，字典。其 key 为字符串类型，表示标的代码；其 value 为 DOUBLE 或 INT
类型，表示跌停价格。注意：若 *minPrice* 为浮点型，则认为是真实价格，引擎处理过程中会乘以 *priceScale*，以匹配输入表中
priceColumn 字段的精度。若为整型，则视为已和 priceColumn 具备相同精度，不再进行缩放。

**userDefinedMetrics** 可选参数，一元函数。

* 函数的入参是一个表，表的每一行是一个标的，每一列是标的对应的快照。若指定 *outputColMap*，则表中数据为
  *outputColMap*设置的字段；否则表中数据为基础字段和报价/询价的价格和数量。
* 函数的返回值是一个元组，元组的每一个元素是一个常规向量，代表每个标的经对应指标计算后的结果。

**priceNullFill** 一个数字。该参数值用于填充输出表中多档买/卖价格中缺失档位的价格。例如涨停后卖单的价格都为
NULL，此时如有指定卖单价格为 0 的需求，可以设置 priceNullFill=0。

**triggerType** 可选参数，字符串标量，表示触发方式。可选值为：

* "mutual"（默认值）：新收到任意一条逐笔数据，当其时间戳大于窗口右边界时，就会触发所有股票未计算的快照合成输出。触发计算的数据并不会参与该次计算。
* "independent"：新收到任意一条逐笔数据，当其时间戳大于窗口右边界时，只触发该条数据对应股票未计算的快照合成输出。触发计算的数据并不会参与该次计算。
* "perRow"：每收到一行逐笔数据都会触发该条数据对应股票计算并输出，触发计算的数据并参与该次计算。

**forceTriggerTime**
可选参数，是非负整数，单位为毫秒。除了正常触发合成快照外，有时会出现一些数据因乱序不能触发合成快照，而是被缓存在引擎中。在这种情况下，可通过该参数设置强制触发引擎中长时间未处理的逐笔数据合成快照。触发规则为：

1. 最新收到的逐笔数据的时间戳（t ）减去最后一条已经处理的交易数据的时间戳（t0 ）大于或等于
   *forceTriggerTime*，则触发未处理的数据中序号最小的那条数据合成快照，并更新已经处理的交易数据的时间戳（t1）。
2. 重复上述操作，若判断 t-t1 >=
   *forceTriggerTime*，则触发未处理的数据中序号最小的那条数据合成快照，并更新已经处理的交易数据的时间戳（t2）；直到两个时间戳的差值小于
   *forceTriggerTime* 时，停止触发快照合成。

**precision** 可选参数，整数，表示小数位数，取值范围为[-1,4]。

* 当 *precision*=-1 时，引擎输出的价格相关字段为整型。注意：输出表中相应的字段可以是整型或非整型。
* 当 *precision* 取 [0, 4]
  中的值时，表示小数位数。输出表中所有的价格将按照指定的位数进行四舍五入。否则，按照原始结果输出。

**orderBySeq** 可选参数，布尔值或元组。

* 指定该参数值为布尔值时，表示是否按照逐笔数据中的 seqColumn 列中值的大小顺序处理数据。当 *exchange*="XSHG" 或
  "XSHGFUND" 时，默认值为 true；在其他情况下，默认值为 false。
  + 当 *orderBySeq*=true
    时，会根据逐笔数据的序号有序处理数据，并计算输出。例如引擎先后收到序号为1，3的数据，因为缺少序号为2的数据，引擎先将1和3的数据缓存，待收到序号2的数据时，再进行计算输出。此时也可以指定
    *forceTriggerTime* 强制触发计算输出。
  + 当 *orderBySeq*=false 时，每接收到一条数据都会立即进行计算并输出，此时不可设置
    *forceTriggerTime*。
* 指定该参数值为元组时，以（BOOL, INTEGER, [STRING]）的形式表示，其中：
  + 第一个元素为布尔值，表示是否按照逐笔数据的序号有序输出结果的布尔值，作用同上。
  + 第二个元素为正整数，表示记录缓存输入数据量的时间间隔，单位为毫秒（ms）。
  + 第三个元素为指定输出日志级别的字符串标量，可选参数，其可用值为 DEBUG （默认值）和 INFO，分别对应 Debug 和 Info
    级别的日志输出。

**orderBookDetailDepth** 可选参数，整型标量，表示 orderbook
明细的深度。默认值为0，表示不输出。该参数必须和 *outputColMap* 中 orderBookDetailDepth 字段的值保持一致。

**orderBookAsArray** 可选参数，布尔值，表示是否以数组向量形式输出报价/询价的价格和数量。默认值为
false，价格和数量将以多列形式输出。

**useSystemTime** 可选参数，布尔值，表示是否使用系统时间来触发快照输出。

* 当 *useSystemTime* = true 时，交易时段内，引擎将基于当前的系统时间，按照
  *intervalInMilli*
  设置的时间间隔触发快照输出。此时，休盘时段（(11:30:00.000，13:00:00.000]）不输出数据，下午盘第一个输出窗口时间戳为
  13:00:00.000+*intervalInMilli*。注意，若设置 *useSystemTime* =
  true，则不能指定 *forceTriggerTime*；可以不指定 *triggerType*，或者指定为
  *triggerType*="mutual"
* 当 *useSystemTime* = false（缺省值）时，引擎根据事件时间来触发快照输出。

**independentForceTriggerTime**
可选参数，非负整数，单位为毫秒。该参数用于设置在长时间未触发快照输出的分组中，强制输出快照的时间间隔。仅当设置
*triggerType*="independent" 时，该参数才会生效。

## 返回值

返回一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')
g = createStreamGraph('engine')

colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]

inputColMap = dict(`codeColumn`timeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn`seqColumn, `SecurityID`Time`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType`ApplSeqNum)

prevClose = dict(`000587.SZ`002694.SZ`002822.SZ`000683.SZ`301063.SZ`300459.SZ`300057.SZ`300593.SZ`301035.SZ`300765.SZ, [1.66, 6.56, 6.10, 8.47, 38.10, 5.34, 9.14, 48.81, 60.04, 16.52])

g.source("trades", colNames, colTypes)
.orderBookSnapshotEngine(exchange="XSHE", orderbookDepth=10, intervalInMilli = 1000, date=2024.01.10, startTime=09:15:00.000, prevClose=prevClose, inputColMap=inputColMap)
.sink("output")
g.submit()
```
