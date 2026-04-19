# updateOrderBookEngineParams

## 语法

`updateOrderBookEngineParams(engine, [prevClose], [maxPrice], [minPrice],
[outputCodeMap])`

## 详情

在线为 OrderBook 引擎设定参数值。该函数必须在创建 OrderBook 引擎后，向引擎注入数据前调用。

## 参数

**engine** OrderBook 引擎名或者或 `createOrderBookSnapshotEngine`
返回的句柄。

**prevClose** 字典，其 key 为字符串标量或向量，表示股票代码；其 value 为数值类型，表示对应于股票代码的上一个交易日的收盘价格。

**maxPrice** 可选参数，字典。其 key 为字符串类型，表示证券代码；其 value 为 DOUBLE 类型，表示涨停价格。

**minPrice** 可选参数，字典。其 key 为字符串类型，表示证券代码；其 value 为 DOUBLE 类型，表示跌停价格。

**outputCodeMap** 可选参数，字符串向量，表示股票代码，例如：“000803.SZ”。指定该参数后，将只输出指定股票对应的数据。

## 例子

运行代码前，先下载 [../data/orderbookDemoInput.zip](https://docs.dolphindb.cn/zh/funcs/data/orderbookDemoInput.zip) 文件。

```
// 通过参数 outputTable 指定输出表
suffix = string(1..10)
colNames = `SecurityID`timestamp`lastAppSeqNum`tradingPhaseCode`modified`turnover`volume`tradeNum`totalTurnover`totalVolume`totalTradeNum`lastPx`highPx`lowPx`ask`bid`askVol`bidVol`preClosePx`invalid  join ("bids" + suffix) join ("bidVolumes" + suffix) join ("bidOrderNums" + suffix) join ("asks" + suffix)  join ("askVolumes" + suffix) join ("askOrderNums" + suffix)
colTypes = [SYMBOL,TIMESTAMP,LONG,INT,BOOL,DOUBLE,LONG,INT,DOUBLE,LONG,INT,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG,LONG,DOUBLE,BOOL] join take(DOUBLE, 10) join take(LONG, 10) join take(INT, 10) join take(DOUBLE, 10) join take(LONG, 10) join take(INT, 10)
share table(10000000:0, colNames, colTypes) as outTable

// 通过参数 dummyTable 指定输入表的表结构
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
dummyOrderStream = table(1:0, colNames, colTypes)

// 通过参数 inputColMap 指定输入表各字段的含义
inputColMap = dict(`codeColumn`timeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn`seqColumn, `SecurityID`Time`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType`ApplSeqNum)
prevClose = dict(SYMBOL, DOUBLE)

// 定义引擎，每 1s 计算输出深交所股票 10 档买卖盘口
engine = createOrderBookSnapshotEngine(name="demo", exchange="XSHE", orderbookDepth=10, intervalInMilli = 1000, date=2022.01.10, startTime=09:15:00.000, prevClose=prevClose, dummyTable=dummyOrderStream, outputTable=outTable, inputColMap=inputColMap)

// 通过 updateOrderBookEngineParams 为引擎传入 prevClose 的具体取值
prevClose = dict(`000587.SZ`002694.SZ`002822.SZ`000683.SZ`301063.SZ`300459.SZ`300057.SZ`300593.SZ`301035.SZ`300765.SZ, [1.66, 6.56, 6.10, 8.47, 38.10, 5.34, 9.14, 48.81, 60.04, 16.52])
updateOrderBookEngineParams(engine, prevClose)

// 导入数据
filePath = "./orderbookDemoInput.csv"
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
orderTrade = table(1:0, colNames, colTypes)
orderTrade.append!(select * from loadText(filePath) order by Time)

// 10支股票的逐笔数据批量注入快照合成引擎
engine.append!(orderTrade)
select count(*) from outTable where SecurityID="300593.SZ", timestamp between 2022.01.10T13:15:01.000 and 2022.01.10T13:15:10.000
```
