<!-- Auto-mirrored from upstream `documentation-main/stream/str_replay_n21.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# N 对 1 多表回放

N 对 1 多表回放包含同构回放和异构回放两种模式：

* 2.00.5 版本前，N 对 1 回放要求输入表结构必须相同，称为**同构回放**
* 自 2.00.5 版本起，N 对 1 回放开始支持输入结构不同的表，称为**异构回放**。

本文档介绍 N 对 1 多表回放的两种模式使用方法。

多表回放功能主要由 `replay` 函数提供。其语法如下：

```
replay(inputTables, outputTables, [dateColumn], [timeColumn], [replayRate], [absoluteRate=true], [parallelLevel=1], [sortColumns])
```

其参数的详细含义可以参考：replay。

## 应用例子 1

按不同回放模式进行回放：

* 模拟回放使用的输入表和输出表：

  ```
  //创建输入表1并写入模拟数据
  n = 1000
  sym = take(`IBM`GS,n)
  myDate = take(2021.01.02..2021.01.06, n).sort!()
  myTime = take(13:00:00..16:59:59,n)
  vol = array(INT[], 0, 10)
  for(i in 0:n){vol.append!([rand(100,3)])}
  t1 = table(sym,myDate,myTime,vol).sortBy!([`myDate, `myTime])
  //创建输入表2并写入模拟数据
  sym = take(`IBM`GS,n)
  date = take(2021.01.02..2021.01.06, n).sort!()
  time = take(13:00:00..16:59:59,n)
  vol = array(INT[], 0, 10)
  for(i in 0:n){vol.append!([rand(100,3)])}
  price = array(DOUBLE[], 0, 10)
  for(i in 0:n){price.append!([rand(10.0,3)])}
  t2 = table(sym, date,time,vol,price).sortBy!([`date, `time])
  //创建输出表
  share streamTable(100:0,`timestamp`sym`blob`vol, [DATETIME,SYMBOL, BLOB, INT[]]) as opt
  //输入表和表对象的映射字典
  input_dict  = dict(["msg1", "msg2"], [t1, t2])
  date_dict = dict(["msg1", "msg2"], [`myDate, `date])
  time_dict = dict(["msg1", "msg2"], [`myTime, `time])
  ```

  以下是输入表 *t1* 的结构以及数据预览

  ```
  t1.schema().colDefs
  ```

  | name | typeString | typeInt |
  | --- | --- | --- |
  | sym | STRING | 18 |
  | myDate | DATE | 6 |
  | myTime | SECOND | 10 |
  | vol | INT[] | 68 |

  ```
  select * from t1 limit 5
  ```

  | sym | myDate | myTime | vol |
  | --- | --- | --- | --- |
  | IBM | 2021.01.02 | 13:00:00 | [89,26,10] |
  | GS | 2021.01.02 | 13:00:01 | [52,30,59] |
  | IBM | 2021.01.02 | 13:00:02 | [45,11,87] |
  | GS | 2021.01.02 | 13:00:03 | [92,0,36] |
  | IBM | 2021.01.02 | 13:00:04 | [85,98,47] |
* 每秒回放 1000 条数据：

  ```
  timer replay(inputTables=input_dict, outputTables=opt, dateColumn = date_dict, timeColumn=time_dict,  replayRate=1000, absoluteRate=true)
  Time elapsed: 2010.107 ms
  ```

  两张输入表中一共有 2000 条数据，每秒回放 1000 条耗时大约 2 秒。
* 加速 100,000 倍时间回放：

  ```
  timer replay(inputTables=input_dict, outputTables=opt, dateColumn = date_dict, timeColumn=time_dict,  replayRate=100000, absoluteRate=false)
  Time elapsed: 3485.393 ms
  ```

  两张输入表中的最大时间与最小时间相差 346,600 秒，加速 100,000 倍时间回放耗时大约 3.5 秒。
* 以最快的速率回放：

  ```
  timer replay(inputTables=input_dict,outputTables=opt,dateColumn=date_dict,timeColumn=time_dict)
  Time elapsed: 9 ms
  ```

  以下是异构回放输出表 *opt* 的结构以及数据预览

  ```
  opt.schema().colDefs
  ```

  | name | typeString | typeInt |
  | --- | --- | --- |
  | timestamp | DATETIME | 11 |
  | sym | SYMBOL | 17 |
  | blob | BLOB | 32 |
  | vol | INT[] | 68 |

  ```
  select * from opt limit 5
  ```

  | timestamp | sym | blob | vol |
  | --- | --- | --- | --- |
  | 2021.01.02T13:00:00 | msg2 | IBM�Hж (X %cx�?�Q�� @��\_w�? | [19,40,88] |
  | 2021.01.02T13:00:00 | msg1 | IBM�Hж Y | [89,26,10] |
  | 2021.01.02T13:00:01 | msg2 | GS�HѶ M 8 e�Q@pƈ6@x �\ @ | [77,4,56] |
  | 2021.01.02T13:00:01 | msg1 | GS�HѶ 4; | [52,30,59] |
  | 2021.01.02T13:00:02 | msg2 | IBM�HҶ : ��V~@���@qi#@ | [58,22,32] |

## 应用例子 2

结合 `replayDS` 回放磁盘分区表数据：

* 将输入表写入数据库中：

  ```
  //将输入表写入数据库中
  if(existsDatabase("dfs://test_stock1")){
  dropDatabase("dfs://test_stock1")
  }
  db1=database("",RANGE, 2021.01.02..2021.01.07)
  db2=database("",VALUE,`IBM`GS)
  db=database("dfs://test_stock1",COMPO,[db1, db2], engine="TSDB")
  orders=db.createPartitionedTable(t1,`orders,`myDate`sym, sortColumns=`sym`myDate`myTime)
  orders.append!(t1)
  trades=db.createPartitionedTable(t2,`trades,`date`sym, sortColumns=`sym`date`time)
  trades.append!(t2)
  ```
* 使用 `replayDS` 对数据源进行划分：

  ```
  //获取数据源
  ds1 = replayDS(sqlObj=<select * from loadTable(db, `orders)>, dateColumn=`myDate, timeColumn=`myTime)
  ds1.size()
  ds2 = replayDS(sqlObj=<select * from loadTable(db, `trades)>, dateColumn=`date, timeColumn=`time)
  ds2.size()
  //输入表的表名及时间列映射字典
  input_dict  = dict(["msg1", "msg2"], [ds1, ds2])
  date_dict = dict(["msg1", "msg2"], [`myDate, `date])
  time_dict = dict(["msg1", "msg2"], [`myTime, `time])
  ```
* 使用 `replay` 对划分好的数据源进行全速回放：

  ```
  timer replay(inputTables=input_dict, outputTables=opt, dateColumn = date_dict, timeColumn=time_dict)
  Time elapsed: 9.972 ms
  ```

## 应用例子 3

异构回放：回放的输出表注入 streamFilter 引擎，进一步过滤分发处理

* 定义 streamFilter：

  ```
  //定义 streamFilter 输入表
  share streamTable(100:0,`timestamp`sym`blob`vol, [DATETIME,SYMBOL, BLOB, INT[]]) as streamFilter_input

  //定义 streamFilter 输出表
  filterOrder=table(100:0, `sym`date`time`volume, [SYMBOL, DATE, SECOND, INT[]])
  filterTrades=table(100:0, `sym`date`time`volume`price, [SYMBOL, DATE, SECOND, INT[], DOUBLE[]])
  //设置 streamFilter 的过滤和处理条件
  filter1=dict(STRING,ANY)
  filter1['condition']=`msg1
  filter1['handler']=filterOrder

  filter2=dict(STRING,ANY)
  filter2['condition']=`msg2
  filter2['handler']=filterTrades
  schema=dict(["msg1","msg2"], [filterOrder, filterTrades])

  //定义 streamFilter，对接收的数据进行处理，分别分发到表 filterOrder 和 filterTrades
  stEngine=streamFilter(name=`streamFilter, dummyTable=streamFilter_input, filter=[filter1,filter2], msgSchema=schema)
  ```
* 订阅表 *opt*，将结果注入 streamFilter

  ```
  subscribeTable(tableName="opt", actionName="sub1", offset=0, handler=stEngine, msgAsTable=true)
  ```
* 使用 `replay` 对划分好的数据源进行全速回放：

  ```
  timer replay(inputTables=input_dict, outputTables=opt, dateColumn = date_dict, timeColumn=time_dict)
  Time elapsed: 9.012 ms
  ```

  以下是 streamFilter 输出表 *filterOrder* 和 *filterTrades* 的结构以及数据预览

  ```
  filterOrder.schema().colDefs
  ```

  | name | typeString | typeInt |
  | --- | --- | --- |
  | sym | SYMBOL | 17 |
  | date | DATE | 6 |
  | time | SECOND | 10 |
  | volume | INT[] | 68 |

  ```
  select * from filterOrder limit 5
  ```

  | sym | myDate | myTime | vol |
  | --- | --- | --- | --- |
  | IBM | 2021.01.02 | 13:00:00 | [89,26,10] |
  | GS | 2021.01.02 | 13:00:01 | [52,30,59] |
  | IBM | 2021.01.02 | 13:00:02 | [45,11,87] |
  | GS | 2021.01.02 | 13:00:03 | [92,0,36] |
  | IBM | 2021.01.02 | 13:00:04 | [85,98,47] |

**相关信息**

* [replay](../funcs/r/replay.html "replay")
* [replayDS](../funcs/r/replayDS.html "replayDS")
* [database](../funcs/d/database.html "database")
* [dropDatabase](../funcs/d/dropDatabase.html "dropDatabase")
* [existsDatabase](../funcs/e/existsDatabase.html "existsDatabase")
* [streamTable](../funcs/s/streamTable.html "streamTable")
