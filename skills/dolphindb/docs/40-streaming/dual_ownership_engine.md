<!-- Auto-mirrored from upstream `documentation-main/stream/dual_ownership_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 双分组响应式状态引擎

双分组响应式状态引擎是对响应式状态引擎的拓展，其计算规则和触发计算的方式与响应式状态引擎相同。不同之处在于，双分组响应式状态引擎在响应式状态引擎的基础上，增加支持对同一输入流数据同时定义两种分组规则（即两个分组键）。引擎会据此创建两个独立的计算实例，对同一份数据并行处理各自对应的指标集。每条输入数据仍对应输出一条结果，不同分组的各个指标保存在不同的字段中。

实际的金融场景常常会有按照不同的分组方式应用不同的指标进行计算的需求，与响应式状态引擎级联实现的解决方案相比，双分组响应式状态引擎计算方式更加简洁高效。

双分组响应式状态引擎由 `createDualOwnershipReactiveStateEngine` 函数创建。其语法如下：

`createDualOwnershipReactiveStateEngine(name, metrics1, metrics2, dummyTable,
outputTable, keyColumn1, keyColumn2, [snapshotDir], [snapshotIntervalInMsgCount],
[keyPurgeFilter1], [keyPurgeFilter2], [keyPurgeFreqInSecond=0], [raftGroup],
[outputHandler], [msgAsTable=false])`

双分组响应式状态引擎的参数与 `createReactiveStateEngine` 的基本相同，其详细含义可以参考：createDualOwnershipReactiveStateEngine。

## 计算规则

每注入一条数据都会计算并产生一条结果，计算将分别基于 *keyColumn1、keyColumn2* 以及对应的
*metrics1、metrics2* 执行，不同分组的各个指标保存在不同的字段中。

## 应用示例

### 基于逐笔成交数据实时计算买卖单累计成交额

在金融实际场景中，常常需要基于逐笔成交数据分别按照买卖订单号聚合进行相应的计算。本例对逐笔成交数据中的成交金额分别按照买单号和卖单号进行聚合，计算相应的累计成交金额。

```
// 定义表结构
colName = `SecurityID`TradeTime`TradePrice`TradeQty`TradeAmount`BuyNum`SellNum`TradeBSFlag
colType = [SYMBOL, TIMESTAMP, DOUBLE, LONG, DOUBLE, LONG, LONG, SYMBOL]
share(streamTable(1000:0, colName, colType), `tickStream)
go

colName = `SecurityID`BuyNum`SellNum`TradeTime`BuyTotalAmount`SellTotalAmount
colType = [SYMBOL, LONG, LONG, TIMESTAMP, DOUBLE, DOUBLE]
share(streamTable(1000:0, colName, colType), `processOrder)
go

// 定义双分组响应式状态引擎
dors = createDualOwnershipReactiveStateEngine(
    name="test",
    metrics1=[<TradeTime>, <cumsum(TradeAmount)>],
    metrics2=<cumsum(TradeAmount)>,
    dummyTable=tickStream,
    outputTable=processOrder,
    keyColumn1=`SecurityID`BuyNum,
    keyColumn2=`SecurityID`SellNum
)

// 订阅流数据表
subscribeTable(tableName=`tickStream, actionName="test", msgAsTable=true, handler=tableInsert{dors})

// 创建模拟数据生成函数
def generateMockTradeData(n, startTime) {
    // 生成基础数据
    securities = `000001.SZ`000002.SZ`600000.SH`600036.SH
    sides = `B`S

    // 生成随机交易数据
    securityList = take(securities, n)
    timeList = startTime + 1..n * 1000  // 每秒一条数据
    priceList = 10.0 + rand(100.0, n)  // 价格在10-110之间
    qtyList = rand(1000, n) + 100  // 成交量100-1100股
    amountList = priceList * qtyList  // 计算成交金额
    buyNumList = rand(1000..10000, n)  // 买方订单号
    sellNumList = rand(1000..10000, n)  // 卖方订单号
    bsFlagList = take(sides, n)  // 买卖方向

    return table(
        securityList as SecurityID,
        timeList as TradeTime,
        priceList as TradePrice,
        qtyList as TradeQty,
        amountList as TradeAmount,
        buyNumList as BuyNum,
        sellNumList as SellNum,
        bsFlagList as TradeBSFlag
    )
}

// 生成并注入模拟数据
mockData = generateMockTradeData(10, 2023.02.01T09:30:00.000)
tickStream.append!(mockData)

// 查询结果
select * from processOrder
```

其结果示例如下：

| SecurityID | BuyNum | SellNum | TradeTime | BuyTotalAmount | SellTotalAmount |
| --- | --- | --- | --- | --- | --- |
| 000001.SZ | 9,183 | 7,233 | 2023.02.01 09:30:01.000 | 24,564.96 | 24,564.96 |
| 000002.SZ | 4,536 | 7,949 | 2023.02.01 09:30:02.000 | 6,315.87 | 6,315.87 |
| 600000.SH | 4,132 | 8,528 | 2023.02.01 09:30:03.000 | 7,361.26 | 7,361.26 |
| 600036.SH | 4,890 | 6,103 | 2023.02.01 09:30:04.000 | 60,081.05 | 60,081.05 |
| 000001.SZ | 4,109 | 9,144 | 2023.02.01 09:30:05.000 | 6,610.39 | 6,610.39 |
| 000002.SZ | 9,145 | 5,634 | 2023.02.01 09:30:06.000 | 48,972.04 | 48,972.04 |
| 600000.SH | 8,980 | 5,341 | 2023.02.01 09:30:07.000 | 35,359.49 | 35,359.49 |
| 600036.SH | 7,919 | 6,908 | 2023.02.01 09:30:08.000 | 15,604.20 | 15,604.20 |
| 000001.SZ | 6,827 | 3,572 | 2023.02.01 09:30:09.000 | 13,989.02 | 13,989.02 |
| 000002.SZ | 1,416 | 5,907 | 2023.02.01 09:30:10.000 | 80,293.77 | 80,293.77 |
