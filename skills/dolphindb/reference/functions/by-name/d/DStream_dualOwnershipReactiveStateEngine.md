# DStream::dualOwnershipReactiveStateEngine

首发版本：3.00.3

## 语法

`DStream::dualOwnershipReactiveStateEngine(metrics1, metrics2, keyColumn1,
keyColumn2, [keyPurgeFilter1], [keyPurgeFilter2],
[keyPurgeFreqInSecond=0])`

## 详情

创建流计算 Dual Ownership 响应式状态引擎。参考：createDualOwnershipReactiveStateEngine。

## 参数

`dualOwnershipReactiveStateEngine` 与
`reactiveStateEngine` 参数基本一致，这里仅介绍有区别的参数：

对 *keyColumn1* 分组后的数据按照 *metrics1* 进行计算，分组数据的清条件则由参数 *keyPurgeFilter1*
设置。

对 *keyColumn2* 分组后的数据按照 *metrics2* 进行计算，分组数据的清条件则由参数 *keyPurgeFilter2*
设置。

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
// dropStreamGraph('dualOwnershipReactive')

g = createStreamGraph('dualOwnershipReactive')

g.source("trades", `date`time`sym`market`price`qty, [DATE, TIME, SYMBOL, CHAR, DOUBLE, INT])
.dualOwnershipReactiveStateEngine(metrics1=<mfirst(price, 3)>, metrics2=<mmax(price, 3)>, keyColumn1=`date`sym, keyColumn2=`date`market)
.sink("output")
g.submit()
go

dates=take(2012.01.01, 10) join take(2012.01.02, 4)
times=[09:00:00.030, 09:00:00.030, 09:00:00.031, 09:00:00.031, 09:00:00.031, 09:00:00.033, 09:00:00.033, 09:00:00.034, 09:00:00.034, 09:00:00.035, 09:00:00.031, 09:00:00.032, 09:00:00.032, 09:00:00.040]
syms=[`a, `a, `b, `a, `a, `b, `a, `b, `b, `a, `b, `a, `b, `c]
markets=['B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B']
prices=[10.65, 10.59, 10.59, 10.65, 10.59, 10.59, 10.59, 10.59, 10.22, 11.0, 10.22, 11.0, 15.6, 13.2]
qtys=[1500, 2500, 2500, 1500, 2500, 2500, 2500, 2500, 1200, 2500, 1200, 2500, 1300, 2000]
tmp=table(dates as date, times as time, syms as sym, markets as market, prices as price, qtys as qty)

appendOrcaStreamTable("trades", tmp)
select * from orca_table.output
```

| date | sym | market | mfirst\_price | mmax\_price |
| --- | --- | --- | --- | --- |
| 2012.01.01 | a | B |  |  |
| 2012.01.01 | a | B |  |  |
| 2012.01.01 | b | A |  |  |
| 2012.01.01 | a | B | 10.65 | 10.65 |
| 2012.01.01 | a | A | 10.59 |  |
| 2012.01.01 | b | B |  | 10.65 |
| 2012.01.01 | a | A | 10.65 | 10.59 |
| 2012.01.01 | b | A | 10.59 | 10.59 |
| 2012.01.01 | b | A | 10.59 | 10.59 |
| 2012.01.01 | a | A | 10.59 | 11 |
