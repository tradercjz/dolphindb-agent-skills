# DStream::narrowReactiveStateEngine

首发版本：3.00.3

## 语法

`DStream::narrowReactiveStateEngine(metrics, metricNames, keyColumn, [filter],
[keepOrder], [keyPurgeFilter], [keyPurgeFreqInSecond=0], [keyCapacity=1024],
[parallelism=1])`

## 详情

创建流计算生成窄表的响应式状态引擎。参考：createNarrowReactiveStateEngine。

## 参数

**metrics** 以元代码的格式表示计算指标，支持输入元组，表示需要输出到 outputTable 中的除 keyColumn
外的输入表中的列或计算指标。注意：这里不要求必须指定除 keyColumn 外的列，但必须指定计算指标，且计算指标必须与 *metricNames*
指定的名称一一对应。

**metricNames** 字符串标量或向量，表示输出到 *outputTable* 中的指标的名称。

**keyColumn** 可选参数，字符串标量或向量表示分组列名。若指定该参数，计算将在各分组进行。

**filter** 可选参数，以元代码的形式表示过滤条件。过滤条件只能是一个表达式，并且只能包含 *dummyTable*中的列。设置多个条件时，用逻辑运算符（and, or）连接。引擎会先计算指标，然后根据 *filter*指定的过滤条件，输出满足条件的输入数据对应的计算结果。

**keepOrder** 可选参数，表示输出表数据是否按照输入时的顺序排序。设置 *keepOrder* =
true，表示输出表按照输入时的顺序排序。当 *keyColumn* 包含有时间列时，*keepOrder* 默认值为 true，否则默认值为
false。

**keyPurgeFilter** 可选参数，是一个由布尔表达式组成的元代码，表示清理条件。各表达式只能引用
*outputTable* 中的字段。必须指定 *keyColumn* 才能使用该参数。

**keyPurgeFreqInSecond** 正整数，表示触发数据清理需要满足的时间间隔（以秒为单位）。必须指定
*keyColumn* 才能使用该参数。

响应式状态引擎提供了 *keyPurgeFilter*, *keyPurgeFreqInSecond*
两个参数，用来清理不再需要的分组数据。每次数据注入时，系统会依次根据以下条件决定是否触发数据清理：

1. 检测本次数据注入与上一次数据注入的时间间隔是否大于等于 *keyPurgeFreqInSecond*
   （第一次数据注入时，检测注入时间和引擎创建时间的间隔）；
2. 若满足上述条件，系统将根据 *keyPurgeFilter* 指定的条件，过滤出待清理的数据；
3. 若待清理的数据所属的分组数大于等于所有分组数的 10%，则触发清理。

若需要查看清理前后的状态，可以通过调用 getStreamEngineStat 函数查看 ReactiveStreamEngine 引擎状态的 numGroups
列，来对比响应式状态引擎清理前后分组数的变化。

**keyCapacity** 正整数，可选参数，表示建表时系统为该表预分配的 key 分组数量，用于调整状态表中 key
的函数。通过该参数的合理设置，能够降低在 key 分组较多时可能出现的延迟。

**parallelism** 不超过63的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。

注：

*parallelism* 不能超过 min(许可核数, 逻辑核数)-1。

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

factor = [<createTime>, <updateTime>,<cumsum(qty)>,<cumavg(upToDatePrice)>]

g.source("trades", ["securityID1","securityID2","securityID3","createTime","updateTime","upToDatePrice","qty","value"], [STRING,STRING,STRING,TIMESTAMP,TIMESTAMP,DOUBLE,DOUBLE,INT])
.narrowReactiveStateEngine(metrics=factor,metricNames=["factor1","factor2"], keyColumn=["securityID1","securityID2","securityID3"])
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

num = 5
tmp = table(take("A" + lpad(string(1..4),4,"0"),num) as securityID1,take("CC.HH" + lpad(string(21..34),4,"0"),num) as securityID2,take("FFICE" + lpad(string(13..34),4,"0"),num) as securityID3, 2023.09.01 00:00:00+(1..num) as createTime, 2023.09.01 00:00:00+take(1..num, num).sort() as updateTime,take(rand(100.0,num) join take(int(),30),num) as upToDatePrice,take(take(100.0,num) join take(int(),30),num)+30 as qty,take(1..20 join take(int(),5),num) as value)

appendOrcaStreamTable("trades", tmp)

select * from orca_table.output
```

| securityID1 | securityID2 | securityID3 | createTime | updateTime | metricName | metricValue |
| --- | --- | --- | --- | --- | --- | --- |
| A0001 | CC.HH0021 | FFICE0013 | 2023.09.01 00:00:01.000 | 2023.09.01 00:00:01.000 | factor1 | 130 |
| A0001 | CC.HH0021 | FFICE0013 | 2023.09.01 00:00:01.000 | 2023.09.01 00:00:01.000 | factor2 | 5.729826227745667 |
| A0002 | CC.HH0022 | FFICE0014 | 2023.09.01 00:00:02.000 | 2023.09.01 00:00:02.000 | factor1 | 130 |
| A0002 | CC.HH0022 | FFICE0014 | 2023.09.01 00:00:02.000 | 2023.09.01 00:00:02.000 | factor2 | 40.09022097935429 |
| A0003 | CC.HH0023 | FFICE0015 | 2023.09.01 00:00:03.000 | 2023.09.01 00:00:03.000 | factor1 | 130 |
| A0003 | CC.HH0023 | FFICE0015 | 2023.09.01 00:00:03.000 | 2023.09.01 00:00:03.000 | factor2 | 40.181519178922024 |
| A0004 | CC.HH0024 | FFICE0016 | 2023.09.01 00:00:04.000 | 2023.09.01 00:00:04.000 | factor1 | 130 |
| A0004 | CC.HH0024 | FFICE0016 | 2023.09.01 00:00:04.000 | 2023.09.01 00:00:04.000 | factor2 | 21.328769097950172 |
| A0001 | CC.HH0025 | FFICE0017 | 2023.09.01 00:00:05.000 | 2023.09.01 00:00:05.000 | factor1 | 130 |
| A0001 | CC.HH0025 | FFICE0017 | 2023.09.01 00:00:05.000 | 2023.09.01 00:00:05.000 | factor2 | 50.23656470375805 |
