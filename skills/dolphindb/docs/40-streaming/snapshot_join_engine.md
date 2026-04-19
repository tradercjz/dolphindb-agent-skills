<!-- Auto-mirrored from upstream `documentation-main/stream/snapshot_join_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# snapshot join 引擎

snapshot join 引擎的连接机制可以看作一个双向的 lookup join
引擎，当左右两表的数据注入引擎时都能触发关联。在默认情况下，引擎采用内连接方式，当左表（右表）中的每一条记录，成功匹配上右表（左表）中的记录时，引擎将输出最新一条结果。用户可以通过设置参数，决定引擎采用内连接还是外连接方式、关联全部记录或仅关联最新一条记录。

与 lookup join 引擎不同的是，snapshot join 引擎的左右表只能是数据流而不能是数据集。与 equi join 引擎相比，snapshot join
引擎可以一直保留引擎中缓存的记录，不会进行过期清理。

下图展示默认设置下，字段结构为（连接列，时间列，指标）的输入数据注入 snapshot join 引擎的效果。

![](images/snapshot_join_engine_1.png)

snapshot join 引擎由 `createSnapshotJoinEngine` 函数创建，其语法如下：

`createSnapshotJoinEngine(name, leftTable, rightTable, outputTable, metrics,
matchingColumn, [timeColumn], [outputElapsedMicroseconds=false],
[keepLeftDuplicates=false], [keepRightDuplicates=false], [isInnerJoin=true],
[snapshotDir], [snapshotIntervalInMsgCount])`

其参数的详细含义可以参考：createSnapshotJoinEngine。

## 应用例子 1- 账户交易数据与行情快照数据关联计算账户持仓盈亏

在计算账户持仓盈亏的场景中，账户交易数据和行情快照数据往往都是从实时更新的数据源获取，通过关联两个表格获取资产的最新市场价格与账户持仓信息，计算持仓盈亏的监控指标。

这个场景的特征是，当账户交易数据更新一条资产的交易数据时，需要立即从行情快照数据中关联相应资产市场价格的最新数据；而行情快照数据更新一条资产的快照数据时，需要立即从账户交易数据中关联账户中对相应资产的最新交易数据。以下脚本用
snapshot join 引擎来实现此场景。

```
// 创建流表
colNames = `SecurityID`Time`LastPrice
colTypes = [SYMBOL, TIMESTAMP, DOUBLE]
share streamTable(1:0, colNames, colTypes) as snapshot

colNames = `ACCT_ID`ORDER_NO`TRADE_TIME`SecurityID`Net`LONG_AVG_PRICE`SHORT_AVG_PRICE
colTypes = `SYMBOL`STRING`TIMESTAMP`SYMBOL`INT`DOUBLE`DOUBLE
share streamTable(1:0, colNames, colTypes) as trades

output=table(100:0, ["SecurityID", "TRADE_TIME", "Time", "ACCT_ID", "ORDER_NO", "PNL"],
[SYMBOL, TIMESTAMP, TIMESTAMP, SYMBOL, STRING, DOUBLE])

// 创建引擎
metrics = [<ACCT_ID>, <ORDER_NO>, <round(Net*(LastPrice-iif((Net>0), LONG_AVG_PRICE, SHORT_AVG_PRICE))) as PNL>]
snapshot_engine = createSnapshotJoinEngine(name = "SJE", leftTable=trades, rightTable=snapshot, outputTable=output, metrics=metrics,
                    matchingColumn = `SecurityID, timeColumn = `TRADE_TIME`Time, isInnerJoin=true, keepLeftDuplicates=false,
                    keepRightDuplicates=false)

// 订阅流表
subscribeTable(tableName="trades", actionName="joinLeft", offset=0, handler=appendForJoin{snapshot_engine, true}, msgAsTable=true)
subscribeTable(tableName="snapshot", actionName="joinRight", offset=0, handler=appendForJoin{snapshot_engine, false}, msgAsTable=true)
```

流表 snapshot 用于存放行情快照数据。流表 trades 用于存放账户交易数据，其中
Net表示账户对资产的持仓净数量，LONG\_AVG\_PRICE表示资产的多头成交均价，SHORT\_AVG\_PRICE 表示资产的空头成交均价。

账户交易数据 trades 注入引擎的左表，行情快照数据 snapshot 注入引擎的右表。snapshot join 引擎中 *isInnerJoin*
设置为 true，则两表进行内连接。参数 *keepLeftDuplicates* 和 *keepRightDuplicates* 设置为
false，能保证 trades（snapshot）数据注入引擎时只关联 snapshot（trades）中的最新数据。

在本例中，资产持仓盈亏指标的计算规则为：资产持仓净数量为正时，用资产持仓净数量乘以资产最新价与资产多头成交均价的差值；资产持仓净数量为负时，用资产持仓净数量乘以资产最新价与资产空头成交均价的差值。

通过以下代码往 trades 和 snapshot 中插入数据样例，模拟账户交易数据和行情快照数据实时更新。

```
insert into trades values(`a, `1, 2024.10.10T10:00:02.784,`111111, 100, 19.03, 17.71)
sleep(10)
insert into snapshot values(`111111, 2024.10.10T10:00:03.000, 18.79)
insert into snapshot values(`222222, 2024.10.10T10:00:03.000, 5.54)
sleep(10)
insert into trades values(`a, `2, 2024.10.10T10:00:04.447,`222222, 300, 5.43, 11.63)
sleep(10)
insert into snapshot values(`111111, 2024.10.10T10:00:06.000, 17.71)
insert into snapshot values(`222222, 2024.10.10T10:00:06.000, 14.99)
sleep(10)
insert into trades values(`a, `3, 2024.10.10T10:00:06.637,`111111, -200, 13.2, 7.47)
sleep(10)
insert into trades values(`a, `4, 2024.10.10T10:00:08.380,`222222, 200, 15.62, 13.19)
sleep(10)
insert into snapshot values(`111111, 2024.10.10T10:00:09.000, 19.81)
insert into snapshot values(`222222, 2024.10.10T10:00:09.000, 13.49)
sleep(10)
insert into trades values(`a, `5, 2024.10.10T10:00:10.680,`111111, -100, 11.09, 3.69)
```

关联结果 output 如下：

![](images/snapshot_join_engine_2.png)

## 应用例子 2

将参数 *isInnerJoin* 设置为 false，引擎将以外连接的方式关联左右表。

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, INT]) as rightTable
output=table(100:0, `sym`time1`time2`price`val`total, [SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, INT, DOUBLE])

engine=createSnapshotJoinEngine(name = "engine1", leftTable=leftTable,
                        rightTable=rightTable, outputTable=output,
                        metrics=[<price>, <val>, <price*val>], matchingColumn=`sym,
                        timeColumn=`time, isInnerJoin=false)
subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{engine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{engine, false}, msgAsTable=true)

n = 6
tem1 = table( (2018.10.08T01:01:01.001 + 1..n) as time,take(`A`B`C, n) as sym,take(1..4,n) as val)
rightTable.append!(tem1)

n = 5
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as time,take(`A`B`C, n) as sym,take(0.1+10..13,n) as price)
leftTable.append!(tem2)
```

| sym | time1 | time2 | price | val | total |
| --- | --- | --- | --- | --- | --- |
| A |  | 2018.10.08 01:01:01.002 |  | 1 |  |
| B |  | 2018.10.08 01:01:01.003 |  | 2 |  |
| C |  | 2018.10.08 01:01:01.004 |  | 3 |  |
| A |  | 2018.10.08 01:01:01.005 |  | 4 |  |
| B |  | 2018.10.08 01:01:01.006 |  | 1 |  |
| C |  | 2018.10.08 01:01:01.007 |  | 2 |  |
| A | 2019.10.08 01:01:01.002 | 2018.10.08 01:01:01.005 | 10.1 | 4 | 40.4 |
| B | 2019.10.08 01:01:01.003 | 2018.10.08 01:01:01.006 | 11.1 | 1 | 11.1 |
| C | 2019.10.08 01:01:01.004 | 2018.10.08 01:01:01.007 | 12.1 | 2 | 24.2 |
| A | 2019.10.08 01:01:01.005 | 2018.10.08 01:01:01.005 | 13.1 | 4 | 52.4 |
| B | 2019.10.08 01:01:01.006 | 2018.10.08 01:01:01.006 | 10.1 | 1 | 10.1 |

使用以下代码清理环境：

```
dropStreamEngine("engine1")
unsubscribeTable(tableName="leftTable", actionName="joinLeft")
unsubscribeTable(tableName="rightTable", actionName="joinRight")
undef(`leftTable, SHARED)
undef(`rightTable, SHARED)
```

参数*keepLeftDuplicates* 和 *keepRightDuplicates* 设置为
true，左表（右表）更新数据时将关联右表（左表）全部匹配的记录。

```
share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, INT]) as rightTable
output=table(100:0, `sym`time1`time2`price`val`total, [SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, INT, DOUBLE])

engine=createSnapshotJoinEngine(name = "engine1", leftTable=leftTable,
                    rightTable=rightTable, outputTable=output,
                    metrics=[<price>, <val>, <price*val>], matchingColumn=`sym,
                    timeColumn=`time, keepLeftDuplicates=true,
                    keepRightDuplicates=true)
subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{engine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{engine, false}, msgAsTable=true)

n = 6
tem1 = table( (2018.10.08T01:01:01.001 + 1..n) as time,take(`A`B`C, n) as sym,take(1..4,n) as val)
rightTable.append!(tem1)

n = 5
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as time,take(`A`B`C, n) as sym,take(0.1+10..13,n) as price)
leftTable.append!(tem2)
```

| sym | time1 | time2 | price | val | total |
| --- | --- | --- | --- | --- | --- |
| A | 2019.10.08 01:01:01.002 | 2018.10.08 01:01:01.002 | 10.1 | 1 | 10.1 |
| A | 2019.10.08 01:01:01.002 | 2018.10.08 01:01:01.005 | 10.1 | 4 | 40.4 |
| B | 2019.10.08 01:01:01.003 | 2018.10.08 01:01:01.003 | 11.1 | 2 | 22.2 |
| B | 2019.10.08 01:01:01.003 | 2018.10.08 01:01:01.006 | 11.1 | 1 | 11.1 |
| C | 2019.10.08 01:01:01.004 | 2018.10.08 01:01:01.004 | 12.1 | 3 | 36.3 |
| C | 2019.10.08 01:01:01.004 | 2018.10.08 01:01:01.007 | 12.1 | 2 | 24.2 |
| A | 2019.10.08 01:01:01.005 | 2018.10.08 01:01:01.002 | 13.1 | 1 | 13.1 |
| A | 2019.10.08 01:01:01.005 | 2018.10.08 01:01:01.005 | 13.1 | 4 | 52.4 |
| B | 2019.10.08 01:01:01.006 | 2018.10.08 01:01:01.003 | 10.1 | 2 | 20.2 |
| B | 2019.10.08 01:01:01.006 | 2018.10.08 01:01:01.006 | 10.1 | 1 | 10.1 |

指定 outputElapsedMicroseconds 为 true，在结果表 output 记录单次响应计算耗时和单次响应的数据条数，此时 output
需要在最后指定耗时列和 batchSize 列。

```
dropStreamEngine("engine1")
unsubscribeTable(tableName="leftTable", actionName="joinLeft")
unsubscribeTable(tableName="rightTable", actionName="joinRight")
undef(`leftTable, SHARED)
undef(`rightTable, SHARED)

share streamTable(1:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as leftTable
share streamTable(1:0, `time`sym`val, [TIMESTAMP, SYMBOL, INT]) as rightTable
output=table(100:0, `sym`time1`time2`price`val`total`execTime`batchSize, [SYMBOL, TIMESTAMP, TIMESTAMP, DOUBLE, INT, DOUBLE, LONG, INT])

engine=createSnapshotJoinEngine(name = "engine1", leftTable=leftTable,
                      rightTable=rightTable, outputTable=output,
                      metrics=[<price>, <val>, <price*val>], matchingColumn=`sym,
                      timeColumn=`time, outputElapsedMicroseconds=true)
subscribeTable(tableName="leftTable", actionName="joinLeft", offset=0, handler=appendForJoin{engine, true}, msgAsTable=true)
subscribeTable(tableName="rightTable", actionName="joinRight", offset=0, handler=appendForJoin{engine, false}, msgAsTable=true)

n = 6
tem1 = table( (2018.10.08T01:01:01.001 + 1..n) as time,take(`A`B`C, n) as sym,take(1..4,n) as val)
rightTable.append!(tem1)

n  = 5
tem2 = table( 2019.10.08T01:01:01.001 + 1..n as time,take(`A`B`C, n) as sym,take(0.1+10..13,n) as price)
leftTable.append!(tem2)
```

| sym | time1 | time2 | price | val | total | execTime | batchSize |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 2019.10.08 01:01:01.002 | 2018.10.08 01:01:01.005 | 10.1 | 4 | 40.4 | 112 | 5 |
| B | 2019.10.08 01:01:01.003 | 2018.10.08 01:01:01.006 | 11.1 | 1 | 11.1 | 112 | 5 |
| C | 2019.10.08 01:01:01.004 | 2018.10.08 01:01:01.007 | 12.1 | 2 | 24.2 | 112 | 5 |
| A | 2019.10.08 01:01:01.005 | 2018.10.08 01:01:01.005 | 13.1 | 4 | 52.4 | 112 | 5 |
| B | 2019.10.08 01:01:01.006 | 2018.10.08 01:01:01.006 | 10.1 | 1 | 10.1 | 112 | 5 |

相关信息

streamTable

createSnapshotJoinEngine

subscribeTable

appendForJoin
