# DStream::cryptoOrderBookEngine

首发版本：3.00.3

## 语法

`DStream::cryptoOrderBookEngine(inputColMap, depth, [updateRule='direct'],
[errorHandler=NULL], [cachingInterval=5000], [timeout=-1],
[cachedDepth])`

## 详情

创建流计算数字货币实时订单簿引擎，支持根据数字货币全量深度快照和增量深度信息，实时更新订单簿。参考：createCryptoOrderBookEngine。

## 参数

**inputColMap** 字典，将 *dummyTable* 中列字段的名称映射为引擎计算所需要的列。

**depth** 正整数或字典，用于指定订单簿的深度。

* 正整数：所有数字货币的订单簿深度都为该设置值。
* 字典：键是字符串标量或向量，表示数字货币代码；值是整型，表示订单簿深度。对于指定的数字货币，将按照设定的深度输出订单簿。未被指定的数字货币将不输出订单簿结果。

**updateRule** 可选参数，字符串标量，用于指定订单簿更新规则。可选值为：

* "direct"：默认值，表示直接更新，系统将不进行数据丢失判断，仅根据 isIncremental
  字段判断是对订单簿执行增量更新（isIncremental=true）还是覆盖（isIncremental-false）。
* "general"：通用更新规则。要求按顺序插入增量数据，并确保数据中 updateId 单调递增。
* "Binance-spot"：基于 Binance 现货交易所订单簿更新机制定义的规则。
* "Binance-futures"：基于 Binance 期货交易所订单簿更新机制定义的规则。

**errorHandler** 可选参数，自定义错误处理函数。当增量数据出现缺失时，可通过该函数进行错误处理。包含 2
个参数：

* 第一个是字符串标量，表示数字货币代码。
* 第二个是整型标量，表示错误码，包括以下情况：
  + 1：接收到历史数据。
  + 2：接收到应在未来时间点到达的乱序数据。
  + 3：超时错误，指定时间间隔内没有新的订单簿合成。
  + 4：买卖价格交叉错误。判断交叉的条件为最高买价大于等于最低卖价。

**cachingInterval** 可选参数，整型标量，表示缓存增量深度数据的时间间隔。默认值为
5000，单位为毫秒。对于每个数字货币，当缓存中的数据时间与当前最新一条数据时间的差值小于等于 *cachingInterval*
时，该数据才会被保留在缓存中。

**timeout** 可选参数，整型标量，表示订单簿更新超时时间。单位为毫秒，默认值为 -1，表示不设置超时时间。在
*timeout* 指定的时间内未合成新的订单簿时，将触发超时错误，此时会通过 *errorHandler* 进行错误处理。

**cachedDepth** 可选参数，正整数或字典，用于指定缓存中价格和数量（包括 askQty, askPrice,
bidQty, bidPrice）的深度。

* 正整数：缓存中所有数字货币的价格和数量将按照该值的深度进行缓存。
* 字典：键是字符串标量或向量，表示数字货币代码；值是整型，表示对应的深度。对于指定的数字货币，将按照设定的深度缓存价格和数量。未被指定的数字货币将保留实际收到的所有价格和数量信息。

## 返回值

返回一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// Define input table schema
colNames = `isIncremental`exchange`eventTime`transactionTime`symbol`firstUpdateId`lastUpdateId`prevLastUpdateId`bidPrice`bidQty`askPrice`askQty
colTypes = [BOOL, SYMBOL, TIMESTAMP, TIMESTAMP, SYMBOL, LONG, LONG, LONG, DECIMAL128(18)[], DECIMAL128(8)[], DECIMAL128(18)[], DECIMAL128(8)[]]

inputTarget = ["symbol", "eventTime", "isIncremental", "bidPrice", "bidQty", "askPrice", "askQty", "lastUpdateId", "firstUpdateId", "prevLastUpdateId"]
inputSource = ["symbol", "eventTime", 'isIncremental', 'bidPrice', 'bidQty', 'askPrice', 'askQty', 'lastUpdateId', 'firstUpdateId', 'prevLastUpdateId']

// Map input columns
inputColMap = dict(inputTarget, inputSource)

// Set depth
depth = dict(["BTCUSDT"], [1000])

cptGraph = createStreamGraph("cptEngine")
cptGraph.source("cptInput", colNames,colTypes)
.cryptoOrderBookEngine(inputColMap, depth)
.sink("output")
cptGraph.submit()
```
