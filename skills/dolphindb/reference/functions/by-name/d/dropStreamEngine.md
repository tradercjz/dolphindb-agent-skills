# dropStreamEngine

## 语法

`dropStreamEngine(name)`

别名： dropAggregator

## 详情

释放指定的流计算引擎的定义。

注：

该函数无法用于删除由 Orca 创建的流计算引擎。如需删除 Orca 流计算引擎，请使用 dropStreamGraph 删除其所属的流图。

## 参数

**name**：字符串，表示一个流计算引擎的名称。需指定为已创建的引擎名称，否则会抛出异常。通过 getStreamEngineStat 可查看已创建的引擎名称。

## 返回值

无。

## 例子

```
share streamTable(1000:0, `time`sym`qty, [TIMESTAMP, SYMBOL, INT]) as trades
outputTable = table(10000:0, `time`sym`sumQty, [TIMESTAMP, SYMBOL, INT])
tradesAggregator = createTimeSeriesAggregator(name="StreamAggregatorDemo", windowSize=3, step=3, metrics=<[sum(qty)]>, dummyTable=trades, outputTable=outputTable, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50)
subscribeTable(tableName="trades", actionName="tradesAggregator", offset=0, handler=append!{tradesAggregator}, msgAsTable=true)

def writeData(n){
    timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
    symv =take(`A`B, n)
    qtyv = take(1, n)
    insert into trades values(timev, symv, qtyv)
}

writeData(6);

select * from outputTable;
```

| time | sym | sumQty |
| --- | --- | --- |
| 2018.10.08T01:01:01.003 | A | 1 |
| 2018.10.08T01:01:01.006 | A | 1 |
| 2018.10.08T01:01:01.006 | B | 2 |

```
dropStreamEngine("StreamAggregatorDemo");
```
