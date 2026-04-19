# genOutputColumnsForOBSnapshotEngine

## 语法

`genOutputColumnsForOBSnapshotEngine([basic=true], [time=true], [depth],
[tradeDetail=true], [orderDetail=true], [withdrawDetail=true],
[orderBookDetailDepth=0], [prevDetail=true], [seqDetail=false],
[residualDetail=false])`

## 详情

该函数用于配合订单簿引擎，简化订单簿引擎的创建过程。

## 参数

以下参数都用于指定订单簿需要包含的字段，每个参数名都表示一个字段类别，每个类别中包含多个字段。通过
`createOrderBookSnapshotEngine` 函数页的附录，查看字段类别及其包含的字段。

**basic** 布尔值。表示是否输出类别 basic 中的字段。默认为 true。

**time** 布尔值。表示是否输出类别 time 中的字段。默认为 true。

**depth** 元组。长度为 2，默认为 (10, true)。

* 第一个元素为整型标量，范围是[0, 100]，表示报价/询价的价格和数量的档位。若为 0 则不输出 depth 中的字段；
* 第二个元素为布尔值，决定多档报价/询价的价格和数量的输出形式。若为 false，表示以多列的形式输出；若为 true，以数组向量的形式输出。

**tradeDetail** 布尔值，表示是否输出 tradeDetail 中的字段（不包含tradeBuyOrderTypeList 和
tradeSellOrderTypeList）。默认为 true。

**orderDetail** 布尔值，表示是否输出 orderDetail 中的字段。默认为 true。

**withdrawDetail** 布尔值，表示是否输出 withdrawDetail 中的字段（不包含 withdrawBuyOrderNoList
和withdrawSellOrderNoList）。默认为 true。

**orderbookDetailDepth** 整型标量，用于指定输出订单簿明细的档位（orderbookDetail 类别）
*。*默认值为0，表示不输出。该参数的值必须和 `createOrderBookSnapshotEngine` 的
*orderbookDetailDepth* 参数的值保持一致。

**prevDetail** 布尔值，表示是否输出 prevDetail 中的字段。默认为 true。

**seqDetail** 布尔值，表示是否输出 seqDetail 中的字段。默认为 false。

**residualDetail** 布尔值，表示是否输出剩余委托明细（residualDetail）中的字段（不包含 ResidualBidOrderNoList
和 ResidualAskOrderNoList）。默认为 false。

## 返回值

返回一个元组，包含2个元素。

* 第一个元素是字符串向量，表示订单簿需要包含的字段，可用于`createOrderBookSnapshotEngine` 的
  *outputColMap* 参数。
* 第二个元素是空的内存表，表示订单簿需要具备的表结构，可用于`createOrderBookSnapshotEngine` 的
  *outputTable* 参数。

## 例子

创建订单簿引擎时，需要通过 *outputColMap* 参数指定需要输出的字段；通过 *outputTable*
参数指定输出表。`genOutputColumnsForOBSnapshotEngine`可以简化这两个参数的定义流程。在创建订单簿引擎前，先进行如下操作：

首先，通过 `genOutputColumnsForOBSnapshotEngine` 函数设置需要输出的字段；

然后，指定 *outputColMap* 为 `genOutputColumnsForOBSnapshotEngine`
函数返回值的第一个元素；指定 *outputTable* 为返回值的第二个元素。

运行代码前，先下载 <../data/orderbookDemoInput.zip> 文件。

```
try { dropStreamEngine("demo") } catch(ex) { print(ex) }

filePath = "./orderbookDemoInput.csv"

// 创建引擎参数 dummyTable，即指定输入表的表结构
colNames = `SecurityID`Date`Time`SecurityIDSource`SecurityType`Index`SourceType`Type`Price`Qty`BSFlag`BuyNo`SellNo`ApplSeqNum`ChannelNo
colTypes = [SYMBOL, DATE, TIME, SYMBOL, SYMBOL, LONG, INT, INT, LONG, LONG, INT, LONG, LONG, LONG, INT]
dummyOrderStream = table(1:0, colNames, colTypes)

// 创建引擎参数 inputColMap，即指定输入表各字段的含义
inputColMap = dict(`codeColumn`timeColumn`typeColumn`priceColumn`qtyColumn`buyOrderColumn`sellOrderColumn`sideColumn`msgTypeColumn`seqColumn, `SecurityID`Time`Type`Price`Qty`BuyNo`SellNo`BSFlag`SourceType`ApplSeqNum)

// 创建引擎参数 prevClose，即昨日收盘价，prevClose 不影响最终的输出结果中除昨日收盘价以外的其他字段
prevClose = dict(`000587.SZ`002694.SZ`002822.SZ`000683.SZ`301063.SZ`300459.SZ`300057.SZ`300593.SZ`301035.SZ`300765.SZ, [1.66, 6.56, 6.10, 8.47, 38.10, 5.34, 9.14, 48.81, 60.04, 16.52])

//创建使用 outputColMap 和 outputTableSch 接收 genOutputColumnsForOBSnapshotEngine 的返回值。它们分别用于确定 outputColMap 和 outputTable
outputColMap, outputTableSch = genOutputColumnsForOBSnapshotEngine(basic=true, time=false, depth=(10, true), tradeDetail=true, orderDetail=false, withdrawDetail=false, orderBookDetailDepth=0, prevDetail=false)

engine = createOrderBookSnapshotEngine(name="demo", exchange="XSHE", orderbookDepth=10, intervalInMilli = 1000, date=2022.01.10, startTime=09:15:00.000, prevClose=prevClose, dummyTable=dummyOrderStream, outputTable=outputTableSch, inputColMap=inputColMap, outputColMap=outputColMap, orderBookAsArray=true)

// 10支股票的逐笔数据批量注入快照合成引擎
engine.append!(select * from loadText(filePath) order by Time)
select top 10 * from outputTableSch where code="300593.SZ", timestamp between 2022.01.10T13:15:01.000 and 2022.01.10T13:15:10.000
```

部分结果展示如下：

![](../../images/orderBook1.png)
