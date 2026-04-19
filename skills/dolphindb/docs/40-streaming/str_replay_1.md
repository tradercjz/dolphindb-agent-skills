<!-- Auto-mirrored from upstream `documentation-main/stream/str_replay_1.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 1 对 1 单表回放

1 对 1 单表回放功能主要由 `replay` 函数提供。

`replay` 函数的语法如下：

```
replay(inputTables, outputTables, [dateColumn], [timeColumn], [replayRate], [absoluteRate=true], [parallelLevel=1], [sortColumns])
```

其参数的详细含义可以参考：replay。

## 应用例子 1

* 定义回放使用的输入表和输出表并向输入表写入模拟数据：

  ```
  //创建输入表并写入模拟数据
  n=1000
  sym = take(`IBM,n)
  date = take(2012.06.12,n)
  time = take(temporalAdd(09:30:12.000,1..500,'s'),n)
  volume = rand(100,n)
  trades = table(sym, date, time, volume)
  trades.sortBy!(`time)
  //创建输出表
  share streamTable(100:0,`sym`date`time`volume,[SYMBOL, DATE, TIME, INT]) as st
  ```
* 每秒回放 100 条数据：

  ```
  timer replay(inputTables=trades, outputTables=st, dateColumn=`date, timeColumn=`time,replayRate=100, absoluteRate=true)
  Time elapsed: 10001.807 ms
  ```

  表 *trades* 中一共有 1,000 条数据，每秒回放 100 条耗时大约 10 秒。
* 加速 100 倍时间回放：

  ```
  timer replay(inputTables=trades,outputTables=st,dateColumn=`date,timeColumn=`time,replayRate=100,absoluteRate=false)
  Time elapsed: 5000.036 ms
  ```

  表 *trades* 中的最大时间与最小时间相差 500 秒，加速 100 倍时间回放耗时大约 5 秒。
* 以最快的速率回放：

  ```
  timer replay(inputTables=trades,outputTables=st,dateColumn=`date,timeColumn=`time)
  Time elapsed: 1.024 ms
  ```

## 应用例子 2

结合 `replayDS` 函数回放磁盘分区表数据。

* 模拟回放使用的输入表和输出表：

  ```
  //创建输入表并写入模拟数据
  n=int(60*60*6.5)
  sym = take(take(`IBM,n).join(take(`GS,n)), n*2*3)$SYMBOL
  date=take(2021.01.04..2021.01.06, n*2*3).sort!()
  time=take(09:30:00..15:59:59,n*2*3)$TIME
  volume = rand(100, n*2*3)
  t=table(sym,date,time,volume)
  //将输入表写入数据库中
  if(existsDatabase("dfs://test_stock")){
  dropDatabase("dfs://test_stock")
  }
  db1=database("",RANGE, 2021.01.04..2021.01.07)
  db2=database("",VALUE,`IBM`GS)
  db=database("dfs://test_stock",COMPO,[db1, db2])
  trades=db.createPartitionedTable(t,`trades,`date`sym)
  trades.append!(t)
  //创建输出表
  share streamTable(100:0,`sym`date`time`volume,[SYMBOL, DATE, TIME, INT]) as st
  ```
* 使用 `replayDS` 函数对数据源进行划分：

  ```
  ds = replayDS(sqlObj=<select * from loadTable(db, `trades)>, dateColumn=`date, timeColumn=`time)
  //查看划分出的数据源个数
  ds.size()

  // output
  3
  ```
* 使用 `replay` 函数对划分好的数据源进行全速回放：

  ```
  timer replay(inputTables=ds, outputTables=st, dateColumn=`date, timeColumn=`time)
  Time elapsed: 20.809 ms
  ```

**相关信息**

* [replay](../funcs/r/replay.html "replay")
* [replayDS](../funcs/r/replayDS.html "replayDS")
* [database](../funcs/d/database.html "database")
* [dropDatabase](../funcs/d/dropDatabase.html "dropDatabase")
* [existsDatabase](../funcs/e/existsDatabase.html "existsDatabase")
* [streamTable](../funcs/s/streamTable.html "streamTable")
