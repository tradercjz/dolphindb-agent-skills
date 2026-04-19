# DStream::getOutputSchema

首发版本：3.00.3

## 语法

`DStream::getOutputSchema()`

## 详情

返回当前 DStream 对象的表结构。

## 参数

无

## 例子

```
aggGraph = createStreamGraph("aggregation")
engine = aggGraph.source("trade", `time`sym`price, [TIMESTAMP, SYMBOL, FLOAT])
	.timeSeriesEngine(windowSize=60, step=60, metrics=[<sum(price)>],
timeColumn="time", keyColumn="sym")
engine.getOutputSchema()

/* output:
time sym sum_price
---- --- ---------
*/
```
