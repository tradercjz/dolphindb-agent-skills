# StreamGraph::sourceByName

首发版本：3.00.3

## 语法

`StreamGraph::sourceByName(name)`

## 详情

按表名引用流图中已提交（即已经通过 submit 注册）的共享流表对象。

## 参数

**name** 表示流表的名称。字符串标量，可以传入完整的流表全限定名（如
"trading.orca\_table.trades"）；也可以仅提供流表名（如 "trades"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

一个 DStream 对象。

## 例子

首先创建并提交流图 “aggregation”。

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

aggGraph = createStreamGraph("aggregation")
aggGraph.source("trade", `time`sym`price, [TIMESTAMP, SYMBOL, FLOAT])
  .timeSeriesEngine(windowSize=60, step=60, metrics=[<sum(price) as price>], timeColumn="time", keyColumn="sym")
  .sink("aggregated")
aggGraph.submit()
```

在另一个流图中，通过 `sourceByName` 引用已提交流图 “aggregation” 中的输出流表
"aggregated"。

```
def EMA(S, N) {
	return ::ewmMean(S, span = N, adjust = false)
}
indicatorGraph = createStreamGraph("indicators")
indicatorGraph.sourceByName("aggregated")
  .reactiveStateEngine(metrics=[<EMA(price, 20)>], keyColumn=`sym)
  .sink("indicators")
indicatorGraph.submit()
```
