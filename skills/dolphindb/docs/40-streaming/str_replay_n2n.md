<!-- Auto-mirrored from upstream `documentation-main/stream/str_replay_n2n.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# N 对 N 多表回放

N 对 N 多表回放功能主要由 `replay` 函数提供。其语法如下：

```
replay(inputTables, outputTables, [dateColumn], [timeColumn], [replayRate], [absoluteRate=true], [parallelLevel=1], [sortColumns])
```

其参数的详细含义可以参考：replay。

## 应用例子 1

按不同回放模式进行回放：

* 定义回放使用的输入表和输出表并向输入表写入模拟数据：

  ```
  //创建输入表1并写入模拟数据
  n=50000
  sym = rand(symbol(`IBM`APPL`MSFT`GOOG`GS),n)
  date = take(2012.06.12..2012.06.16,n)
  time = take(13:00:00.000..16:59:59.999,n)
  volume = rand(100,n)
  t1 = table(sym,date,time,volume).sortBy!([`date, `time])
  //创建输入表2并写入模拟数据
  sym = rand(symbol(`IBM`APPL`MSFT`GOOG`GS),n)
  date = take(2012.06.12..2012.06.16,n)
  time = take(13:00:00.000..16:59:59.999,n)
  price = 100 + rand(10.0,n)
  t2 = table(sym,date,time,price).sortBy!([`date, `time])
  //创建输出表 outTable1 和 outTable2
  share streamTable(100:0,`sym`date`time`volume,[SYMBOL,DATE,TIME,INT]) as outTable1
  share streamTable(100:0,`sym`date`time`price,[SYMBOL,DATE,TIME,DOUBLE]) as outTable2
  ```
* 每秒回放 10,000 条数据：

  ```
  timer replay(inputTables=[t1,t2], outputTables=[outTable1, outTable2], dateColumn=`date, timeColumn=`time,replayRate=10000, absoluteRate=true)
  Time elapsed: 10001.807 ms
  ```

  两张输入表中一共有 100,000 条数据，每秒回放 10,000 条耗时大约 10 秒。
* 加速 10,000 倍时间回放：

  ```
  timer replay(inputTables=[t1,t2], outputTables=[outTable1, outTable2], dateColumn=`date, timeColumn=`time,replayRate=10000,absoluteRate=false)
  Time elapsed: 3484.047 ms
  ```

  两张输入表中的最大时间与最小时间相差 345,650 秒，加速 100,000 倍时间回放耗时大约 3.5 秒。
* 以最快的速率回放：

  ```
  timer replay(inputTables=[t1,t2], outputTables=[outTable1, outTable2], dateColumn=`date, timeColumn=`time)
  Time elapsed: 4.441 ms
  ```

## 应用例子 2

结合 `replayDS` 函数回放磁盘分区表数据。

* 将输入表写入数据库中：

  ```
  //将输入表写入数据库中
  if(existsDatabase("dfs://test_stock")){
  dropDatabase("dfs://test_stock")
  }
  db=database("dfs://test_stock",VALUE,2012.06.12..2012.06.16)
  pt1=db.createPartitionedTable(t1,`pt1,`date).append!(t1)
  pt2=db.createPartitionedTable(t2,`pt2,`date).append!(t2)
  ```
* 使用 `replayDS` 函数对数据源进行划分：

  ```
  ds1=replayDS(sqlObj=<select sym, date, time, volume from pt1>,dateColumn=`date,timeColumn=`time,timeRepartitionSchema=[13:00:00.000, 14:00:00.000, 15:00:00.000, 16:00:00.000, 17:00:00.000])
  ds2=replayDS(sqlObj=<select sym, date, time , price from pt2>,dateColumn=`date,timeColumn=`time,timeRepartitionSchema=[13:00:00.000, 14:00:00.000, 15:00:00.000, 16:00:00.000, 17:00:00.000])
  //查看 ds1 划分出的数据源个数（ds2 个数同 ds1）
  ds1.size()
  // output
  30
  ```
* 使用 `replay` 函数对划分好的数据源进行全速回放：

  ```
  timer replay(inputTables=[ds1,ds2], outputTables=[outTable1, outTable2], dateColumn=`date, timeColumn=`time)
  Time elapsed:  450.956 ms
  ```

**相关信息**

* [replay](../funcs/r/replay.html "replay")
* [replayDS](../funcs/r/replayDS.html "replayDS")
* [database](../funcs/d/database.html "database")
* [dropDatabase](../funcs/d/dropDatabase.html "dropDatabase")
* [existsDatabase](../funcs/e/existsDatabase.html "existsDatabase")
* [streamTable](../funcs/s/streamTable.html "streamTable")
