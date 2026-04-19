# peekAppend

首发版本：3.00.5

## 语法

`peekAppend(engine, data)`

## 详情

在不更新流引擎状态且不向输出表写入结果的情况下，返回在引擎当前状态基础上加上指定数据后的即时计算结果。目前仅支持 TimeSeriesEngine
和ReactiveStateEngine 的部分算子，具体如下：

**TimeSeriesEngine**：设置 *keyColumn* 且未设置
*useSystemTime*、*acceptedDelay*、*forceTriggerTime*。

**ReactiveStateEngine**：`cumavg`、`cumsum`、`cumstd`、`cumstdp`、`cumvar`、`cumvarp`、`cumprod`、`cumcount`、`mcount`、`msum`、`mavg`、`mstd`、`mstdp`、`mvar`、`mvarp`
以及无状态算子（表达式，无状态函数等）。

## 参数

**engine** 流引擎。

**data** 一个表或元组，表示要写入流数据引擎的消息。

## 返回值

返回一个表对象，即在引擎当前状态上加上 *data* 的即时计算结果。引擎状态不会更新，也不会有输出结果到 outputTable。

## 例子

**ReactiveStateEngine 示例**

```
share streamTable(100:0, `sym`time`price, [STRING,DATETIME,DOUBLE]) as tickStream
share streamTable(1000:0, `sym`time`factor1, [STRING,DATETIME,DOUBLE]) as result
rse = createReactiveStateEngine(name="reactiveDemo", metrics =[<time>, <cumsum(price)>], dummyTable=tickStream, outputTable=result, keyColumn="sym")
data = table(take(["000001.SH","000002.SH","000003.SH"], 3) as sym, take(2021.02.08T09:31:00 + 1..3, 3) as time, take(100.0, 3) as price)
res = rse.peekAppend(data)
rse.append!(data)
//res和result一致
```

![](../images/peekAppend/1.png)

```
share streamTable(100:0, `sym`time`price, [STRING,DATETIME,DOUBLE]) as tickStream
share streamTable(1000:0, `sym`time`factor1, [STRING,DATETIME,DOUBLE]) as result
rse = createReactiveStateEngine(name="reactiveDemo", metrics =[<time>, <cumsum(price)>], dummyTable=tickStream, outputTable=result, keyColumn="sym")

data = table(take(["000001.SH"], 3) as sym, take(2021.02.08T09:31:00 + 1..3, 3) as time, 100 200 300 as price)
res2 = rse.peekAppend(data)
```

![](../images/peekAppend/2.png)

**TimeSeriesEngine 示例**

```
share streamTable(1000:0, `sym`time`volume, [STRING,DATETIME,INT]) as tickStream
share streamTable(1000:0, `time`sym`sumVolume, [DATETIME,STRING,INT]) as result
tse = createTimeSeriesEngine(name="tse", windowSize=60, step=60, metrics=<[sum(volume)]>, dummyTable=tickStream, outputTable=result, timeColumn="time", useSystemTime=false, keyColumn="sym")

insert into tse values([`"000001.SH", 2021.02.08T09:30:00, 100])
data = table(take(["000001.SH"], 3) as sym, take(2021.02.08T09:30:00 + 1..3, 3) as time, 100 200 300 as price)
res = tse.peekAppend(data)
```

![](../images/peekAppend/3.png)
