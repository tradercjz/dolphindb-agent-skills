# createStreamDispatchEngine

## 语法

`createStreamDispatchEngine(name, dummyTable, keyColumn,
outputTable, [dispatchType='hash'], [hashByBatch=false], [outputLock=true],
[queueDepth=4096], [outputElapsedTime=false], [mode='buffer'])`

## 详情

创建流数据分发引擎，返回一个表对象。该引擎将输入的数据分发到不同的输出表，以实现负载均衡。其中输出表可以是内存表，分布式表或流数据引擎。

引擎特性：

* 支持多线程输入和多线程输出。
* 只提供数据分发功能，不提供指标计算功能。

场景应用：

将快照数据分发给一个或多个计算引擎进行因子计算，以提高计算性能。

## 参数

**name** 字符串，表示流数据分发引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**keyColumn** 字符串。若设置，则会以 *dispatchType* 指定的方式，基于该列分发数据。*keyColumn*
列中的每个唯一值被视为一个 key。

**outputTable** 表对象，若 *outputElapsedTime*= false，则 *outputTable* 的表结构和
*dummyTable* 相同；否则 *outputTable* 比 *dummyTable* 在最后多了一个 LONG
类型和一个 NANOTIMESTAMP 类型的列，分别表示每一个 batch 的输出耗时（单位是微秒）及其输出时的时间戳（精度为纳秒）。

可以指定1~100个输出表。引擎会为每个表创建一个线程来接收分发到该表的数据。以 tuple 或嵌套 tuple
的方式指定多张表，例如：outputTable=[table1, table2, table3,
table4]，表示将注入的数据平均分发到4张表中，每张表的数据不同；outputTable=[[table1\_1, table1\_2], [table2\_1,
table2\_2]]，则会将数据拆分并复制。两份副本分别分发到各个子元素中对应的表中。具体来说，副本1的数据分发到 table1\_1
table1\_2，副本2的数据分发到 table2\_1 和 table2\_2。此时 table1\_1 和 table2\_1
除耗时和时间列外，其它列的数据相同；table1\_2 和 table2\_2 除耗时和时间列外，其它列的数据相同。

**dispatchType** 可选参数，字符串，可选值为：

* "hash"（默认值）：对 *keyColumn*
  列进行哈希计算，并根据计算结果，将数据分发到各个输出表。由于哈希计算得到的分布不一定均匀，因此可能会出现数据分配不均的情况。
* "uniform"：按照 *keyColumn* 列，将数据均匀分发到各个输出表。
* "saltedHash"：对 *keyColumn* 列进行加盐处理，然后进行哈希计算。通过[加盐处理](https://en.wikipedia.org/wiki/Salt_%28cryptography%29)，可以确保即使输入相同，也能产生独特的哈希值，从而避免碰撞。该选项在需要进行多层哈希分发的场景（例如分发引擎嵌套分发引擎，且都采用哈希计算进行数据分发）中更为适用。

提示：

建议使用默认的分发方式，即 "hash"。如果因为哈希分配不均匀而影响性能，则可以尝试使用
"uniform" 方式。

**hashByBatch** 可选参数, 布尔类型。该参数决定了是否将一个 batch 中的所有数据输出到同一个表中。默认为 false，表示对一个 batch
中的所有 key 分组后，按照 *dispatchType* 指定的方式分发数据。 仅当 *dispatchType*='hash' 时，才可设置
*hashByBatch*=true，此时，引擎随机取 batch 中一个 key 进行哈希计算，根据计算结果，将该 batch
中的所有数据输出到某一个表。

注：

当 *hashByBatch*=false 时，可以保证相同
key 的数据被输出到同一张表，但是这种分组操作会增加一些开销。

**outputLock** 可选参数，布尔类型，默认值为
true，表示是否对输出表进行加锁以避免并发访问的冲突。若设置为
false，则不对输出表进行加锁，此时需要保证其他线程不会对输出表进行并发操作。一般情况下，建议使用默认值（true）。

当除了分发引擎以外，还有其他线程（比如其他引擎、流订阅等等）写入到输出表时，输出表需要加锁（因为内存表不允许并发写入），但加锁会增加开销。但在某些场景下，例如在输出线程数量大于等于输入线程数量，且能保证多个输入线程不会同时向一个输出线程写入数据的场景下，如果用户能保证只有一个线程写入输出表，则可以设置该参数为
false，即不对输出表加锁，以提高数据分发的性能。

**queueDepth** 可选参数，正整数，默认为4096（单位为行）。

* *mode* = “buffer” 时，表示每个输出线程的缓存表大小。
* *mode* = “queue” 时，表示每个输出线程的队列深度。

建议根据输入数据的记录数大小，适当调节该参数。如果输入数据量较小但该参数设置过大，则会导致内存空间的浪费；相反，如果输入数据量较大但该参数设置过小，可能会导致数据输出阻塞。

**outputElapsedTime** 可选参数，布尔类型，表示是否输出每个 batch 从注入引擎到分发输出的总耗时。默认为
false，不输出总耗时。若设置为 true，则会在输出表最后两列中输出耗时（单位为微秒）和数据输出的时间戳（单位为纳秒）。

**mode** 可选参数，字符串，可选值为：

* "buffer"（默认值）：引擎会为每个输出线程创建一个内存缓存表，并将待分发的数据复制到缓存表中。对于数据写入引擎过程中，可能会并发读写输入表，或频繁
  append 数据到引擎且每次 append 的数据量较小的场景，建议使用该配置。
* "queue"：引擎为每一个输出线程维护一个数据队列，只将输入表的引用加入到分发队列，不复制数据。此配置要求写入数据的过程中不能对输入表进行并发读写，适合不频繁
  append 数据到引擎且每次 append 的数据量较大的场景。

## 返回值

返回一个表对象。

## 例子

**例 1**
通过分发引擎，将流数据表中的数据分发到3个状态引擎，以进行因子计算，最终将结果输出到同一个输出表中。

```
//定义状态引擎的输入和输出表
share streamTable(1:0, `sym`price, [STRING,DOUBLE]) as tickStream
share streamTable(1000:0, `sym`factor1, [STRING,DOUBLE]) as resultStream
//定义将要使用的输出表。这里定义3个状态引擎。
for(i in 0..2){
rse = createReactiveStateEngine(name="reactiveDemo"+string(i), metrics =<cumavg(price)>, dummyTable=tickStream, outputTable=resultStream, keyColumn="sym")
}
//定义分发引擎
dispatchEngine=createStreamDispatchEngine(name="dispatchDemo", dummyTable=tickStream, keyColumn=`sym, outputTable=[getStreamEngine("reactiveDemo0"),getStreamEngine("reactiveDemo1"),getStreamEngine("reactiveDemo2")])

//订阅流数据表tickStream
subscribeTable(tableName=`tickStream, actionName="sub", handler=tableInsert{dispatchEngine}, msgAsTable = true)

//订阅的数据注入引擎
n=100000
symbols=take(("A" + string(1..10)),n)
prices=100+rand(1.0,n)
t=table(symbols as sym, prices as price)
tickStream.append!(t)

select count(*) from resultStream
100,000

//查看状态引擎状态
getStreamEngineStat().ReactiveStreamEngine
```

| name | user | status | lastErrMsg | numGroups | numRows | numMetrics | metrics | snapshotDir | snapshotInterval | snapshotMsgId | snapshotTimestamp | garbageSize | memoryUsed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dispatchDemo | admin | OK | 0 | 100,000 | 0 | 0 | -1 | 0 | 0 |  |  |  |  |

**例 2** 30 只股票的数据持续流入。为了提高因子计算的吞吐量，使用分发引擎将数据按股票代码 sym 分发到 3 个响应式状态引擎，每个引擎独立计算
`cumavg` 因子。

* 采用哈希分发（`dispatchType='hash'`）

  ```
  dummy = table(1:0, `sym`price, [STRING, DOUBLE])
  // 定义输出表
  share streamTable(1000:0, `sym`factor1, [STRING, DOUBLE]) as result_hash0
  share streamTable(1000:0, `sym`factor1, [STRING, DOUBLE]) as result_hash1
  share streamTable(1000:0, `sym`factor1, [STRING, DOUBLE]) as result_hash2
  // 定义响应式状态引擎
  for(i in 0..2) {
      createReactiveStateEngine(name="rse_hash" + string(i), metrics=<cumavg(price)>,
          dummyTable=dummy, outputTable=objByName("result_hash" + string(i)), keyColumn="sym")
  }
  // 定义分发引擎
  dispatchHash = createStreamDispatchEngine(name="dispatch_hash", dummyTable=dummy, keyColumn=`sym,
      outputTable=[getStreamEngine("rse_hash0"), getStreamEngine("rse_hash1"), getStreamEngine("rse_hash2")],
      dispatchType='hash')

  // 模拟 30 只股票、共 9 万条数据
  n = 90000
  t = table(take("A" + string(1..30), n) as sym, (100 + rand(1.0, n)) as price)
  dispatchHash.append!(t)
  sleep(1000)

  result_hash0.size() //27,000
  result_hash1.size() //36,000
  result_hash2.size() //27,000
  ```
* 采用均匀分发（`dispatchType='uniform'`）

  ```
  dummy = table(1:0, `sym`price, [STRING, DOUBLE])
  // 定义输出表
  share streamTable(1000:0, `sym`factor1, [STRING, DOUBLE]) as result_uniform0
  share streamTable(1000:0, `sym`factor1, [STRING, DOUBLE]) as result_uniform1
  share streamTable(1000:0, `sym`factor1, [STRING, DOUBLE]) as result_uniform2
  // 定义响应式状态引擎
  for(i in 0..2) {
      createReactiveStateEngine(name="rse_uniform" + string(i), metrics=<cumavg(price)>,
          dummyTable=dummy, outputTable=objByName("result_uniform" + string(i)), keyColumn="sym")
  }
  // 定义分发引擎
  dispatchUniform = createStreamDispatchEngine(name="dispatch_uniform", dummyTable=dummy, keyColumn=`sym,
      outputTable=[getStreamEngine("rse_uniform0"), getStreamEngine("rse_uniform1"), getStreamEngine("rse_uniform2")],
      dispatchType='uniform')

  // 模拟 30 只股票、共 9 万条数据
  n = 90000
  t = table(take("A" + string(1..30), n) as sym, (100 + rand(1.0, n)) as price)
  dispatchUniform.append!(t)
  sleep(1000)

  result_uniform0.size() //30,000
  result_uniform1.size() //30,000
  result_uniform2.size() //30,000
  ```

可以看出，uniform 分发的各表行数会更均匀。

**例 3** 对于多层分发的场景：engineA 分发至 engine1和 engine2，engine1 分发至 table1\_1 和
table1\_2，engine2 分发至 table2\_1 和 table2\_2，使用
`dispatchType='saltedHash'` 可有效就避免 hash
分发不均。

```
dummy = table(1:0, `sym`price, [STRING, DOUBLE])
// 定义输出表
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as s_t1_1
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as s_t1_2
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as s_t2_1
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as s_t2_2
// 定义两层分发引擎
salt1 = createStreamDispatchEngine(name="salt1", dummyTable=dummy, keyColumn=`sym,
    outputTable=[s_t1_1, s_t1_2], dispatchType='saltedHash')
salt2 = createStreamDispatchEngine(name="salt2", dummyTable=dummy, keyColumn=`sym,
    outputTable=[s_t2_1, s_t2_2], dispatchType='saltedHash')

saltA = createStreamDispatchEngine(name="saltA", dummyTable=dummy, keyColumn=`sym,
    outputTable=[getStreamEngine("salt1"), getStreamEngine("salt2")], dispatchType='saltedHash')
// 写入数据
n = 100000
t = table(take("S" + string(1..100), n) as sym, rand(100.0, n) as price)
hashA.append!(t)
saltA.append!(t)
sleep(1000)

s_t1_1.size()//27,000
s_t1_2.size()//20,000
s_t2_1.size()//29,000
s_t2_2.size()//24,000
```

若使用哈希分发，则多层分发的场景下会出现明显的分发不均。

```
dummy = table(1:0, `sym`price, [STRING, DOUBLE])
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as h_t1_1
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as h_t1_2
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as h_t2_1
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as h_t2_2

hash1 = createStreamDispatchEngine(name="hash1", dummyTable=dummy, keyColumn=`sym,
    outputTable=[h_t1_1, h_t1_2], dispatchType='hash')
hash2 = createStreamDispatchEngine(name="hash2", dummyTable=dummy, keyColumn=`sym,
    outputTable=[h_t2_1, h_t2_2], dispatchType='hash')

hashA = createStreamDispatchEngine(name="hashA", dummyTable=dummy, keyColumn=`sym,
    outputTable=[getStreamEngine("hash1"), getStreamEngine("hash2")], dispatchType='hash')

n = 100000
t = table(take("S" + string(1..100), n) as sym, rand(100.0, n) as price)
hashA.append!(t)
sleep(1000)

h_t1_1.size()//56,000
h_t1_2.size()//0
h_t2_1.size()//44,000
h_t2_2.size()//0
```

**例 4** hashByBatch
可以设置是否将整批数据发往同一张表。

```
dummy = table(1:0, `sym`price, [STRING, DOUBLE])

share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as out_batchOn_0
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as out_batchOn_1

share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as out_batchOff_0
share streamTable(1000:0, `sym`price, [STRING, DOUBLE]) as out_batchOff_1

// hashByBatch=true: 一个 batch 的所有数据输出到同一张表
dispatchBatchOn = createStreamDispatchEngine(name="dispatch_batchOn", dummyTable=dummy, keyColumn=`sym,
    outputTable=[out_batchOn_0, out_batchOn_1],
    dispatchType='hash', hashByBatch=true)

// hashByBatch=false: 同一 batch 内按 key 分组后分发到不同表
dispatchBatchOff = createStreamDispatchEngine(name="dispatch_batchOff", dummyTable=dummy, keyColumn=`sym,
    outputTable=[out_batchOff_0, out_batchOff_1],
    dispatchType='hash', hashByBatch=false)

// 写入数据
t = table(take(`A`B`C`D`E, 1000) as sym, rand(100.0, 1000) as price)
dispatchBatchOn.append!(t)
dispatchBatchOff.append!(t)
sleep(500)

out_batchOn_0.size()//0
out_batchOn_1.size()//1,000

out_batchOff_0.size()//600
out_batchOff_1.size()//400
```

可以看到，*hashByBatch*
开启后，整批数据发往同一张表；关闭后，两表都有数据。

**例 5** 开启 *outputElapsedTime*
后，输出表中将记录分发耗时和输出时间戳。

```
dummy = table(1:0, `sym`price, [STRING, DOUBLE])

// outputElapsedTime=true 时，输出表需要比 dummyTable 多两列：LONG (耗时微秒) + NANOTIMESTAMP (输出时间戳)
share streamTable(1000:0, `sym`price`elapsed`ts, [STRING, DOUBLE, LONG, NANOTIMESTAMP]) as out_elapsed_0
share streamTable(1000:0, `sym`price`elapsed`ts, [STRING, DOUBLE, LONG, NANOTIMESTAMP]) as out_elapsed_1

dispatchElapsed = createStreamDispatchEngine(name="dispatch_elapsed", dummyTable=dummy, keyColumn=`sym,
    outputTable=[out_elapsed_0, out_elapsed_1],
    outputElapsedTime=true)

t = table(take(`A`B`C, 3000) as sym, rand(100.0, 3000) as price)
dispatchElapsed.append!(t)
sleep(500)

select top 5 * from out_elapsed_0
```

| sym | price | elapsed | ts |
| --- | --- | --- | --- |
| B | 5.156729068876414 | 81 | 2026.03.21 19:39:01.860162086 |
| C | 14.33727939481318 | 81 | 2026.03.21 19:39:01.860162086 |
| B | 56.25857125414968 | 81 | 2026.03.21 19:39:01.860162086 |
| C | 65.14644184269626 | 81 | 2026.03.21 19:39:01.860162086 |
| B | 48.80402196403686 | 81 | 2026.03.21 19:39:01.860162086 |
