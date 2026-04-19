<!-- Auto-mirrored from upstream `documentation-main/stream/narrow_reactive_state_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 窄表响应式状态引擎

随着量化交易竞争的加剧，量化投资团队需要处理大量因子。在许多情况下，因子数据量甚至会远远超过高频的行情数据量。在海量因子数据存储场景下，相较于宽表，窄表存储支持更加高效地添加、更新、删除因子等操作，因此，更适合使用窄表存储因子数据。DolphinDB
提供的窄表响应式状态引擎在响应式状态引擎的基础上支持将结果输出到窄表，可以满足因子数据存储需求。此外，窄表响应式状态引擎还支持动态管理计算指标：使用 getReactiveMetrics
函数可实时获取指标详情，而 addReactiveMetrics 则能在不中断业务的情况下动态添加新指标，极大地增强了灵活性。

与响应式状态引擎的计算规则和计算方式一致，每输入一条数据，窄表响应式状态引擎都将触发一次结果输出。然而与响应式状态引擎的输出形式不同，窄表响应式状态引擎将以窄表形式输出指标（由
*metricNames* 指定）的计算结果，即计算结果输出到不同行的相同列。

* 窄表响应式状态引擎由 `createNarrowReactiveStateEngine` 函数创建。语法如下：

  `createNarrowReactiveStateEngine(name, metrics, metricNames, dummyTable,
  outputTable, keyColumn, [filter], [snapshotDir], [snapshotIntervalInMsgCount],
  [keepOrder], [keyPurgeFilter], [keyPurgeFreqInSecond=0], [raftGroup],
  [outputElapsedMicroseconds=false], [keyCapacity=1024],
  [parallelism=1])`

  其参数的详细含义可以参考：createNarrowReactiveStateEngine。

* 窄表响应式状态引擎的指标详情可以由 `getReactiveMetrics` 函数实时获取。语法如下：

  `getReactiveMetrics(name)`

  其参数的详细含义可以参考：getReactiveMetrics。

* 若需要动态增加窄表响应式状态引擎的计算指标，可由 `addReactiveMetrics` 函数实现。语法如下：

  `addReactiveMetrics(name, metricNames, metrics)`

  其参数的详细含义可以参考：addReactiveMetrics。

## 应用示例

### 示例1. 动态增加计算指标

业务场景常需动态扩展计算指标。响应式状态引擎通常要求计算逻辑在初始化时完全确定；相比之下，窄表响应式状态引擎提供了动态添加指标的能力。指标更新后，无需重启引擎即可对后续数据流生效。

首先，使用窄表响应式状态引擎计算累计均价、累计最高价和累计成交量这三个指标，其计算代码如下：

```
dummy =  streamTable(1:0, `sym`date`time`price`qty, [STRING,DATE,TIME,DOUBLE, INT])
outputTable = streamTable(10000:0, `sym`date`time`metricNames`factorValue, [STRING,DATE,TIME,STRING,DOUBLE])
//这里定义计算指标，本例中定义了累计均价、累计最高价和累计成交量三个指标。用户可根据实际需要修改指标。
factor = [<date>, <time>, <cumavg(price)>, <cummax(price)>, <cumsum(qty)>]
Narrowtest = createNarrowReactiveStateEngine(name="narrowtest", metrics=factor, metricNames=["cumAvgPx","cumMaxPx","cumTotalQty"],dummyTable=dummy,outputTable=outputTable,keyColumn="sym")

//模拟数据
num = 5
tmp = table(take("A" + lpad(string(1..4),4,"0"),num) as sym, take(2023.09.01,num) as date, 2023.09.01 00:00:00+take(1..num, num).sort() as time, take(rand(100.0,num) join take(int(),30),num) as price, rand(50,num) as qty)
Narrowtest.append!(tmp)
```

上例通过 `createNarrowReactiveStateEngine`
引擎计算累计均价、累计最高价和累计成交量这三个指标，并将计算结果输出到窄表中，即三个指标的结果依次输出到同一列。其结果示例如下：

| sym | date | time | metricNames | factorValue |
| --- | --- | --- | --- | --- |
| A0001 | 2023.09.01 | 09:30:01.000 | cumAvgPx | 90.83 |
| A0001 | 2023.09.01 | 09:30:01.000 | cumMaxPx | 90.83 |
| A0001 | 2023.09.01 | 09:30:01.000 | cumTotalQty | 802 |
| A0002 | 2023.09.01 | 09:30:02.000 | cumAvgPx | 7.88 |
| A0002 | 2023.09.01 | 09:30:02.000 | cumMaxPx | 7.88 |
| A0002 | 2023.09.01 | 09:30:02.000 | cumTotalQty | 448 |
| A0003 | 2023.09.01 | 09:30:03.000 | cumAvgPx | 67.40 |
| A0003 | 2023.09.01 | 09:30:03.000 | cumMaxPx | 67.40 |
| A0003 | 2023.09.01 | 09:30:03.000 | cumTotalQty | 80 |
| A0004 | 2023.09.01 | 09:30:04.000 | cumAvgPx | 32.14 |
| A0004 | 2023.09.01 | 09:30:04.000 | cumMaxPx | 32.14 |
| A0004 | 2023.09.01 | 09:30:04.000 | cumTotalQty | 11 |
| A0001 | 2023.09.01 | 09:30:05.000 | cumAvgPx | 86.33 |
| A0001 | 2023.09.01 | 09:30:05.000 | cumMaxPx | 90.83 |
| A0001 | 2023.09.01 | 09:30:05.000 | cumTotalQty | 1,351 |

以新增累计最大成交量指标为例，其具体代码如下：

```
//新增累计最大成交量指标
metrics = [<cummax(qty)>]
addReactiveMetrics("narrowtest", "cumMaxQty", metrics)

//新增计算指标后，再次向引擎注入数据，则会输出更新后的指标计算结果
tmpNew = table("A0001" as sym, 2023.09.01 as date, 2023.09.01 00:00:06 as time, 88 as price, 666 as qty)
Narrowtest.append!(tmpNew)
```

新增计算指标后，引擎会对后续接收的新数据立即生效，其输出结果为：

| sym | date | time | metricNames | factorValue |
| --- | --- | --- | --- | --- |
| A0001 | 2023.09.01 | 09:30:06.000 | cumAvgPx | 86.88 |
| A0001 | 2023.09.01 | 09:30:06.000 | cumMaxPx | 90.83 |
| A0001 | 2023.09.01 | 09:30:06.000 | cumTotalQty | 2,017 |
| A0001 | 2023.09.01 | 09:30:06.000 | cumMaxQty | 666 |

### 示例2. 基于引擎级联的多因子窄表计算示例

DolphinDB
内置的流计算引擎包括响应式状态引擎，时间序列聚合引擎，横截面引擎和异常检测引擎等。这些引擎都以数据表作为输入和输出，因此解决复杂的因子计算问题时，可以将多个流计算引擎通过级联的方式合并成一个复杂的数据流拓扑。窄表响应式状态引擎适用于下游基于多因子窄表处理的场景，如下游因子计算依赖于不同因子的最新值。

本例首先通过窄表响应式状态引擎计算每只产品的累计均价和累计成交量，进一步使用响应式无状态引擎对其中一只产品的累计均价进行调整。

```
/**
    @ 若执行过示例 1，可使用以下语句清理计算环境
    dropStreamEngine("narrowtest")
 */
share streamTable(1:0, `sym`date`time`price`qty, [STRING,DATE,TIME,DOUBLE, INT]) as tickStream
share streamTable(1:0, `sym`metricNames`factorValue, [STRING,STRING,DOUBLE]) as tempResultStream
result = table(100:0, `sym`metricNames`factorValue, [STRING,STRING,DOUBLE])

// 创建 metrics 描述数据间的依赖关系
metrics = array(ANY, 0, 0)
metric = dict(STRING,ANY)
// 依赖关系 product_A:factorNew=product_A:factor1*product_A:factor2/(product_A:factor2+product_B:factor2)
metric["outputName"] = `product_A:`factorNew
metric["formula"] = <A*B\(B+C)>
metric["A"] = `product_A:`factor1
metric["B"] = `product_A:`factor2
metric["C"] = `product_B:`factor2
metrics.append!(metric)

rsle = createReactiveStatelessEngine("reactiveStateless", metrics, result)

//这里定义计算指标，本例中定义了累计均价和累计成交量两个指标。用户可根据实际需要修改指标。
factor = [<cumavg(price)>, <cumsum(qty)>]
Narrowtest = createNarrowReactiveStateEngine(name="narrowtest", metrics=factor, metricNames=["factor1","factor2"],dummyTable=tickStream,outputTable=tempResultStream,keyColumn="sym")
subscribeTable(tableName=`tickStream, actionName="factors", handler=tableInsert{Narrowtest})
subscribeTable(tableName=`tempResultStream, actionName="factorsNew", handler=tableInsert{rsle})

//模拟数据
num = 10
tmp = table(take(`product_A`product_B, num) as sym, take(2023.09.01, num) as date, 09:30:00+(1..num) as time, rand(10.0, num) as price, rand(1000, num) as qty)
tickStream.append!(tmp)
```

结果示例如下：

| sym | metricNames | factorValue |
| --- | --- | --- |
| product\_A | factorNew | 7.938898 |
| product\_A | factorNew | 2.399637 |
| product\_A | factorNew | 2.710666 |
| product\_A | factorNew | 2.440562 |
