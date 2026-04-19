# streamFilter

## 语法

`streamFilter(name, dummyTable, filter, [msgSchema],
[timeColumn], [conditionColumn])`

## 详情

创建流数据过滤引擎，对输入引擎的数据进行过滤和分发处理，返回一个表对象。

该引擎的处理流程包含以下步骤：

1. 输入数据为异构流数据表（由 replay
   函数回放得到）时，解析（反序列化）数据。输入数据为普通流数据表时无此步骤。注意：1.30.18 版本开始，streamFilter
   函数支持过滤普通流数据表数据，并进行分发处理。
2. 根据 *filter* 指定的规则对流数据表进行过滤。
3. 过滤后的数据按照时间顺序分发到不同的 *handler* 处理。

注：

2.00.5 版本开始，DolphinDB 支持通过 replay
函数将多个结构不同的流数据表，回放（序列化）到一个流数据表里，这个流数据表被称为异构流数据表。`streamFilter`
函数用于解析（反序列化）和过滤异构流数据表的数据并进行分发处理。

## 参数

**name** 字符串标量，表示流数据过滤引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**dummyTable** 表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**filter** 单个字典或包含多个字典的 tuple。对注入引擎的数据进行过滤和处理。

字典可选的 key-value 说明如下：

* 'timeRange'：可选字段，一个数据对或包含多个数据对的 tuple。以指定的 *timeRange* 对
  *timeColumn* 进行过滤。注意：若分发普通流数据表，则 *timeRange* 必须和
  *timeColumn* 的数据类型一致；异构流数据表无该限制。
* 'condition'：表示过滤条件。

  + 若分发异构流数据表，则 'condition' 是一个字符串，且必须是 replay 参数 *inputTables*
    的键值（表的标识）。用于过滤出异构表中具有 *condition* 标识的数据。
  + 若分发普通流数据表，则 'condition'
    可以是一个字符串标量/向量，或者是包含一个或多个布尔表达式的元代码。其中表达式中可以使用内置函数，但不支持部分应用。请注意，若
    'condition' 指定为字符串标量/向量，必须为 *conditionColumn* 指定列的元素。
* 'handler'：一元函数或表对象（包括流数据引擎返回的表对象）。

  + 如果它是一元函数，它唯一的参数是经过解析和过滤后的数据表。
  + 如果它是表对象，经过解析和过滤后的数据会直接插入到该表中。

**msgSchema** 可选字段，字典。

* 若分发异构流数据表，其结构与 replay 回放到异构流数据表的数据表结构保持一致。引擎将根据
  *msgSchema* 指定的结构对注入的数据解析;
* 若分发普通流数据表，该参数必须设置为空。

以下参数仅在分发普通流数据表时指定：

**timeColumn** 字符串，指定为 *dummyTable* 中时间列的名称。若不指定，则取 *dummyTable*
第一列的列名。

**conditionColumn** 字符串，指定为 *dummyTable* 中的列名。注意 *conditionColumn* 只能指定
STRING 或 SYMBOL 类型的列。若不指定该参数，则 *filter* 的 *condition* 字段将失效。

## 返回值

返回一个表对象。

## 例子

(1) 异构流数据表分发：

一个典型场景：对分布式数据库中的订单表和交易表进行回放，模拟两者实时 asof join 的场景。如使用 replay 进行 N 对
N 回放，则无法保证数据严格按照时间戳 顺序注入 asof join 引擎的左表和右表（原因详见 `replay` 说明）。但通过
`replay` 将两表回放到一个异构流数据表则可以保证表内所有数据按照时间戳顺序排序， 之后通过
`streamFilter` 将表中数据分发至 asof join
引擎的左、右表时，可保证数据按时间戳顺序注入引擎左、右两表。

```
// 创建 order 表
n=1000
sym = take(take("IBM",n).join(take("GS",n)), n*2*3)
date=take(2022.01.04..2022.01.06, n*2*3).sort!()
timestamp1=take(2022.01.04 09:30:00.000+rand(1000,n),n) join take(2022.01.04 09:31:00.000+rand(1000,n),n)
timestamp2=take(2022.01.05 09:30:00.000+rand(1000,n),n) join take(2022.01.05 09:31:00.000+rand(1000,n),n)
timestamp3=take(2022.01.06 09:30:00.000+rand(1000,n),n) join take(2022.01.06 09:31:00.000+rand(1000,n),n)
timestamp=timestamp1 join timestamp2 join timestamp3
volume = rand(100, n*2*3)
t=table(sym,date,timestamp,volume)

if(existsDatabase("dfs://test_order")){
dropDatabase("dfs://test_order")
}
db1_or=database("",RANGE, 2022.01.04..2022.01.07)
db2_or=database("",VALUE,`IBM`GS)
db_or=database("dfs://test_order",COMPO,[db1_or, db2_or])
orders=db_or.createPartitionedTable(t,`orders,`date`sym)
orders.append!(t);
select count(*) from orders
// output
6000

// 创建trades表
n=2000
sym = take(take("IBM",n).join(take("GS",n)), n*2*3)
date=take(2022.01.04..2022.01.06, n*2*3).sort!()
timestamp1=take(2022.01.04 09:30:00.000+rand(1000,n),n) join take(2022.01.04 09:31:00.000+rand(1000,n),n)
timestamp2=take(2022.01.05 09:30:00.000+rand(1000,n),n) join take(2022.01.05 09:31:00.000+rand(1000,n),n)
timestamp3=take(2022.01.06 09:30:00.000+rand(1000,n),n) join take(2022.01.06 09:31:00.000+rand(1000,n),n)
timestamp=timestamp1 join timestamp2 join timestamp3
volume = rand(100, n*2*3)
price = rand(50.0, n*3) join  rand(20.0, n*3)

t=table(sym,date,timestamp,volume,price)

if(existsDatabase("dfs://test_trades")){
dropDatabase("dfs://test_trades")
}
db1=database("",RANGE, 2022.01.04..2022.01.07)
db2=database("",VALUE,`IBM`GS)
db=database("dfs://test_trades",COMPO,[db1, db2])
trades=db.createPartitionedTable(t,`trades,`date`sym)
trades.append!(t);
select count(*) from trades
// output
12000

// 准备回放的数据源和输出表
ds_or = replayDS(sqlObj=<select * from loadTable(db_or, `orders)>, dateColumn=`date, timeColumn=`timestamp)
ds = replayDS(sqlObj=<select * from loadTable(db, `trades)>, dateColumn=`date, timeColumn=`timestamp)
input_dict=dict(["orders","trades"], [ds_or, ds])
share streamTable(100:0,`timestamp`sym`blob`volume, [TIMESTAMP,SYMBOL, BLOB, INT]) as opt

// 订阅异构流数据表回放数据到分配引擎
share streamTable(100:0,`timestamp`sym`blob`volume, [TIMESTAMP,SYMBOL, BLOB, INT]) as streamFilterOpt
share streamTable(100:0, `sym`date`timestamp`volume, [SYMBOL, DATE, TIMESTAMP, INT] ) as streamOrders
share streamTable(100:0, `sym`date`timestamp`volume`price, [SYMBOL, DATE, TIMESTAMP, INT, DOUBLE] ) as streamTrades
streamOpt=table(100:0, `timestamp`sym`volume`price`result, [TIMESTAMP, SYMBOL, INT, DOUBLE, DOUBLE])

filter1=dict(STRING,ANY)
filter1['condition']=`orders
filter1['timeRange']=09:30:00.000:09:30:00.005

filter2=dict(STRING,ANY)
filter2['condition']=`trades
filter2['timeRange']=09:30:00.000:09:30:00.005

ajEngine=createAsofJoinEngine(name="ajEngine", leftTable=streamOrders, rightTable=streamTrades, outputTable=streamOpt, metrics=<[volume,price,price*volume]>, matchingColumn=`sym, useSystemTime=true)
filter1['handler']=getLeftStream(ajEngine)
filter2['handler']=getRightStream(ajEngine)
schema=dict(["orders","trades"], [streamOrders, streamTrades])

engine=streamFilter(name=`streamFilter,dummyTable=streamFilterOpt, filter=[filter1,filter2],msgSchema=schema)
subscribeTable(tableName="opt", actionName="sub1", offset=0, handler=engine, msgAsTable=true)

// 结构不同的两个表数据回放到opt
replay(inputTables=input_dict,outputTables=opt, timeColumn=`timestamp)

select count(*) from streamOpt
// output
20

// 取消订阅
unsubscribeTable(tableName="opt", actionName="sub1")
dropStreamEngine(`streamFilter)
dropStreamEngine(`ajEngine)
```

(2) 普通流数据表分发：

下例，将普通流数据表（trades）数据注入分发引擎中，根据过滤条件进行分发处理。

```
n=20
sym = symbol(take(`A`B`C,n))
name = string(rand(1..10,n))
date = temporalAdd(2012.12.06,0..(n-1),'d')
time = temporalAdd(09:30:00.000,0..(n-1),'ms')
vol = 100+take(1..8,20)
t = table(date,time,sym,name,vol)

// 定义两个流数据引擎，作为分发引擎 handler
share streamTable(100:0,`date`time`sym`name`vol,[DATE,TIME,SYMBOL,STRING,INT]) as st1
share streamTable(100:0,`date`time`sym`name`vol,[DATE,TIME,SYMBOL,STRING,INT]) as st2
share streamTable(100:0,`date`time`sym`name`vol,[DATE,TIME,SYMBOL,STRING,INT]) as st3

// handler为引擎时的输入流数据表
share streamTable(100:0,`time`sym`sum_vol,[TIME,SYMBOL,INT]) as output1
share streamTable(100:0,`time`avg_vol,[TIME,INT]) as output2
engine1=createTimeSeriesEngine(name="timeEngine", windowSize=3, step=3, metrics=<[sum(vol)]>, dummyTable=st3, outputTable=output1, timeColumn=`time, useSystemTime=false, keyColumn=`sym, garbageSize=50)
engine2=createReactiveStateEngine(name="reactiveEngine", metrics=<[mavg(vol, 3)]>, dummyTable=st1, outputTable=output2, keyColumn=`sym)

// 需要注入分发引擎的流数据表
share streamTable(100:0,`date`time`sym`name`vol,[DATE,TIME,SYMBOL,STRING,INT]) as trades

// 设置第一个过滤条件，将 trades 表中 sym 列对应元素为 A 且时间在09:30:00.001:09:30:00.010和09:29:00.000:09:30:00.000的数据输入状态引擎进行处理
filter1 = dict(STRING,ANY)
filter1['condition']=`A
filter1['handler']=engine2
filter1['timeRange']=(09:30:00.001:09:30:00.010,09:29:00.000:09:30:00.000)

// 设置第二个过滤条件，将 trades 表时间范围在09:30:00.002:09:30:00.005里的数据全部输出到st2表里
filter2 = dict(STRING,ANY)
filter2['handler']=st2
filter2['timeRange']=09:30:00.002:09:30:00.005

// 设置第三个过滤条件，将 trades 表中 sym 列对应元素为 A 和 C 的数据输入时序引擎进行处理
filter3 = dict(STRING,ANY)
filter3['condition']=`C`A
filter3['handler']=engine1

// 订阅分发引擎，根据以上三个过滤条件，对 trades 表中的数据进行分发处理
streamFilter2=streamFilter(name="streamFilterDemo",dummyTable=trades,filter=[filter1,filter2,filter3], timeColumn=`time, conditionColumn=`sym)
subscribeTable(tableName="trades", actionName="sub1", offset=0, handler=streamFilter2, msgAsTable=true)
trades.append!(t)
select * from output1
```

| time | sym | sum\_vol |
| --- | --- | --- |
| 09:30:00.003 | A | 101 |
| 09:30:00.003 | C | 103 |
| 09:30:00.006 | A | 104 |
| 09:30:00.006 | C | 106 |
| 09:30:00.009 | A | 107 |
| 09:30:00.009 | C | 101 |
| 09:30:00.012 | A | 102 |
| 09:30:00.012 | C | 104 |
| 09:30:00.015 | A | 105 |
| 09:30:00.015 | C | 107 |
| 09:30:00.018 | A | 108 |

```
select * from output2
```

| time | avg\_vol |
| --- | --- |
| 00:00:00.001 |  |
| 00:00:00.001 |  |
| 00:00:00.001 | 104 |
| 00:00:00.001 | 104 |

```
select * from st2
```

| date | time | sym | name | vol |
| --- | --- | --- | --- | --- |
| 2012.12.08 | 09:30:00.002 | C | 6 | 103 |
| 2012.12.09 | 09:30:00.003 | A | 8 | 104 |
| 2012.12.10 | 09:30:00.004 | B | 10 | 105 |
| 2012.12.11 | 09:30:00.005 | C | 10 | 106 |
| 2012.12.12 | 09:30:00.006 | A | 10 | 107 |
| 2012.12.13 | 09:30:00.007 | B | 1 | 108 |
| 2012.12.14 | 09:30:00.008 | C | 3 | 101 |
| 2012.12.15 | 09:30:00.009 | A | 4 | 102 |
| 2012.12.16 | 09:30:00.010 | B | 9 | 103 |

可以为 condition 指定表达式，以支持更复杂的过滤逻辑，将上例中 filter2 的 *condition* 指定为条件表达式，同时对 vol 和
date 列进行过滤。

```
filter2 = dict(STRING,ANY)
filter2['condition'] = <sym==`A and 101<vol<105 and date<2012.12.15>
filter2['handler'] = st2
filter2['timeRange'] = 09:30:00.002:09:30:00.010

select * from st2
```

| date | time | sym | name | vol |
| --- | --- | --- | --- | --- |
| 2012.12.09 | 09:30:00.003 | A | 7 | 104 |
