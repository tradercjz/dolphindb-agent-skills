# createStreamBroadcastEngine

## 语法

`createStreamBroadcastEngine(name, dummyTable, outputTables)`

## 详情

创建流数据广播引擎，将同一份流数据复制后分发至不同的目标表对象。该函数返回一个表对象，通过向该表对象注入数据，实现流数据的多路广播。

该引擎的应用场景是对同一份流数据同时进行不同的处理，例如将拷贝后的一份数据存入磁盘，另一份数据则输入引擎进行后续计算等。

## 参数

**name** 字符串标量，表示流数据广播引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTables** 由2个及以上表对象组成的元组，每个表对象的结构和 dummyTable 相同。表对象可以是内存表、分布式表或流计算引擎。

## 返回值

返回一个表对象。

## 例子

```
share streamTable(1:0, `sym`price, [STRING,DOUBLE]) as tickStream
share streamTable(1000:0, `sym`factor1, [STRING,DOUBLE]) as resultStream

t=table(100:0, `sym`price, [STRING, DOUBLE])

//定义将要使用的输出表。这里定义1个状态引擎，1个分布式表用于存储数据
rse = createReactiveStateEngine(name="reactiveDemo", metrics =<cumavg(price)>, dummyTable=tickStream, outputTable=resultStream, keyColumn="sym")
if(existsDatabase("dfs://database1")){
	dropDatabase("dfs://database1")
}
db=database("dfs://database1", VALUE, "A"+string(1..10))
pt=db.createPartitionedTable(t,`pt,`sym)

//定义广播引擎
broadcastEngine=createStreamBroadcastEngine(name="broadcastEngine", dummyTable=tickStream, outputTables=[loadTable("dfs://database1", `pt),getStreamEngine("reactiveDemo")])

//订阅流数据表tickStream
subscribeTable(tableName=`tickStream, actionName="sub", handler=tableInsert{broadcastEngine}, msgAsTable = true)

//订阅的数据注入引擎
n=100000
symbols=take(("A" + string(1..10)),n)
prices=100+rand(1.0,n)
t1=table(symbols as sym, prices as price)
tickStream.append!(t1)

// 查看分布式表中数据有100,000 条
select count(*) from loadTable("dfs://database1", `pt)
// output: 100,000

//查看状态引擎状态
getStreamEngineStat().ReactiveStreamEngine
```

| name | user | status | lastErrMsg | numGroups | numRows | numMetrics | memoryInUsed | snapshotDir | snapshotInterval | snapshotMsgId | snapshotTimestamp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reactiveDemo | admin | OK | 10 | 100,000 | 1 | 2,600 | -1 |  |  |  |  |
