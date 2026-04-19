<!-- Auto-mirrored from upstream `documentation-main/rn/compact_report_3_00_2.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.2

## 3.00.2.5

### 缺陷修复带来的系统影响

在创建流数据日级时间序列引擎 (`createDailyTimeSeriesEngine`) 时：

* 若配置了 session 时段*，*则 *roundTime* 不再生效，*mergeLastWindow* 不再规整
  session 时段*。*
* 采用如下方式指定跨天 session
  时段时：

  ```
  sessionBegin = [00:00:00, 09:00:00, 13:00:00, 21:00:00]
  sessionEnd = [01:00:00, 11:30:00, 15:00:00, 00:00:00]
  //即 session 时段为21:00:00-次日01:00:00，09:00:00-11:30:00， 13:00:00-15:00:00。
  ```

  *keyPurgeDaily*
  的行为发生变化：
  + 在之前版本中，*keyPurgeDaily* 在 21:00:00 之前不生效，15:00:00-21:00:00
    之间的数据会并入 21:00:00的窗口。
  + 在新版本中，*keyPurgeDaily* 在 21:00:00 之前生效，15:00:00-21:00:00
    之间的数据会被丢弃。
* 函数 `getUserAccess` 的返回结果中，原 “COMPUTE\_GROUP\_allowed”
  字段名自新版本起改为 “COMPUTE\_GROUP\_EXEC\_allowed”。

### 涉及保持一致性或兼容行业惯例的修改

对 `bondCashflow`
函数的参数结构进行了调整，部分参数名已修改，接口更为统一，功能更强大。原有参数结构将不再兼容，请根据新接口进行适配。

## 3.00.2.0

### 缺陷修复带来的系统影响

* 使用 `append!`追加元组数据的行为发生变化。新版本中建议使用新增函数
  `memberModify!` 来修改元组数据。

  + 在之前版本中，`append!`可以向元组追加数据，并会改变元组成员的数据。
  + 在当前版本中，不支持使用 `append!` 向元组追加数据。

```
//创建一个元组 tp
a = [1, 2, 3, 4]
b = [6, 7, 8]
tp = [a, b]
tp
//output: [[1, 2, 3, 4], [6, 7, 8]]

//修改元组数据
tp[0].append!(5)
tp
//老版本：[[1, 2, 3, 4, 5], [6, 7, 8]]，修改成功
//新版本：[[1, 2, 3, 4], [6, 7, 8]]，修改失败
a
//老版本：[1, 2, 3, 4, 5]，a的值也被修改
//新版本：[1, 2, 3, 4]，a的值不变

//新版本中建议使用 memberModify! 修改元组数据
//修改第一个元组元素的数据
memberModify!(tp, append!, 0, 5)
tp
//output: [[1, 2, 3, 4, 5], [6, 7, 8]]
//继续修改第二个元组元素的数据
memberModify!(tp, append!, 1, 9)
tp
//output: [[1, 2, 3, 4, 5], [6, 7, 8, 9]]
```

* `dropPartition` 函数的 *partitionPaths* 参数为空时：

  + 在之前版本中，删除整表。
  + 在当前版本中，报错：Please use truncate instead of dropPartition to delete
    the entire table.

```
//建库建表
n = 1000000;
t = table(2020.01.01T00:00:00 + 0..(n-1) as timestamp, rand(`IBM`MS`APPL`AMZN,n) as symbol, rand(10.0, n) as value)
db = database("dfs://rangedb_tradedata", RANGE, `A`F`M`S`ZZZZ)
Trades = db.createPartitionedTable(table=t, tableName="Trades", partitionColumns="symbol", compressMethods={timestamp:"delta"});
Trades.append!(t)
t1 = loadTable(db, "Trades")
select count(*) from t1
//返回为100万

//删除库中指定分区数据，不传入partitionPaths参数
dropPartition(db, , tableName="t")
//老版本：报错，None of the specified partitions exist. RefId: S01056'
//新版本：报错，Please use truncate instead of dropPartition to delete the entire table.

//查看表 Trades 数据量
select count(*) from t1
//老版本：返回为0，整表被删除
//新版本：返回为100万，表无删减
```

* `unsubscribeTable` 函数增加订阅不存在情况下的检查：

  + 在之前版本中，执行不报错。
  + 在当前版本中，将根据具体情况报错。

```
//创建输入表并写入模拟数据
n = 1000
sym = take(`IBM,n)
date = take(2012.06.12,n)
time = take(temporalAdd(09:30:12.000,1..500,'s'),n)
volume = rand(100,n)
trades = table(sym, date, time, volume)
trades.sortBy!(`time)
//创建流表
share streamTable(100:0,`sym`date`time`volume,[SYMBOL, DATE, TIME, INT]) as st

unsubscribeTable(,"st1","sub1")
//老版本：正常执行
//新版本：报错，The shared table st1 doesn't exist.
```

* `poly1d` 函数修改函数名和参数名：

  + 在之前版本中，语法为 `poly1d(z,x)` 。
  + 在当前版本中，语法为 `polyPredict(model,X)`，且
    `poly1d(model,X)` 将作为别名函数。
* `kroghInterpolate` 修改参数名：

  + 在之前版本中，语法为
    `kroghInterpolate(Xi,Yi,X,[der=0])`。
  + 在当前版本中，语法为
    `kroghInterpolate(X,Y,newX,[der=0])`。
* `percentChange`在 X 为标量时：

  + 在之前版本中，执行不报错。
  + 在当前版本中，报错 X must be a vector or a matrix.

```
percentChange(1,1)
// 之前版本返回：[NULL]
// 当前版本报错：Usage: move(X, steps). X must be a vector or a matrix.
```

* `keyedTable` 的 *keyColumns* 多于一列时，若插入的数据中
  *keyColumns* 列的数据类型与表字段类型不一致：

  + 在之前版本中，相同组合的 key 不会去重。
  + 在当前版本中，相同组合的 key 会去重。

```
sym = `A`B`C
id = 1 2 3
val = 11 22 33
t=keyedTable(`id`sym,sym,id,val)
insert into t values ("A", 1.0, 55)
t
```

之前版本结果：

| sym | id | val |
| --- | --- | --- |
| A | 1 | 11 |
| B | 2 | 22 |
| C | 3 | 33 |
| A | 1 | 55 |

当前版本结果：

| sym | id | val |
| --- | --- | --- |
| A | 1 | 55 |
| B | 2 | 22 |
| C | 3 | 33 |

* `wj` 函数的 *aggs 中包含*`sum` 嵌套
  `first`、`last` 等顺序相关的函数时：

  + 在之前版本中：sum(first(col)) 取 col 分组中第一个元素参与 sum 计算。
  + 在当前版本中：sum(first(col)) 取 col 分组中每个窗口的第一个元素参与 sum 计算。

```
t = table(["A","B","A","B","B","A"] as sym,[1,2,3,4,5,6] as id,[8, 2, 3, 6, 6, 4] as val)
wj(t, t, 1:10, <[first(val),sum((first(val))+val)]>,`sym`id)
```

之前版本结果：

| sym | id | val | first\_val | sum |
| --- | --- | --- | --- | --- |
| A | 1 | 8 | 3 | 23 |
| B | 2 | 2 | 6 | 16 |
| A | 3 | 3 | 4 | 12 |
| B | 4 | 6 | 6 | 8 |
| B | 5 | 6 |  |  |
| A | 6 | 4 |  |  |

第一行数据在计算 sum 时，first(val) 取值为分组 A 中的第一个值 8，窗口中的两条数据分别对应第 3 行（val=3）和第 6
行(val=4)，故 `sum=（8+3）+（8+4）= 23`。

当前版本结果：

| sym | id | val | first\_val | sum |
| --- | --- | --- | --- | --- |
| A | 1 | 8 | 3 | 13 |
| B | 2 | 2 | 6 | 24 |
| A | 3 | 3 | 4 | 8 |
| B | 4 | 6 | 6 | 12 |
| B | 5 | 6 |  |  |
| A | 6 | 4 |  |  |

第一行数据在计算 sum 时，first(val) 取值为分组 A 中该数据对应窗口的第一个值 3，窗口中的两条数据分别对应第 3 行（val=3）和第 6
行(val=4)，故 `sum=（3+3）+（3+4）= 13`。

* 使用 `group by` 进行分组时，若聚合函数作用于外部变量，结果发生变化：

  + 在之前版本中，会对该外部变量进行分组计算。
  + 在当前版本中，每个分组的结果相等，都是聚合函数直接计算的结果。

以 `avg` 为例

```
t = table( [1,2,1,2,3] as id, [1,3,5,7,9] as val)
v = [1,2,3,4,5]
select avg(v) from t group by id
```

之前版本结果如下，id 为 1 的组对应表 t 的第 1 行和第 3 行，故 avg\_v 为 v 的第 1 个与第 3 个元素之平均值；同理 id 为 2
的组对应 v 的第 2 个 和第 4 个元素之平均值。

| id | avg\_v |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 5 |

当前版本结果如下，avg(v) 的结果为 3，每个分组对应的 avg\_v 均为该值。

| id | avg\_v |
| --- | --- |
| 1 | 3 |
| 2 | 3 |
| 3 | 3 |

* 使用 `context by` 分组后计算 `isortTop` ，结果变化：

  + 在之前版本中，`context by` 未生效。
  + 在当前版本中，`context by` 分组后在组内计算
    `isortTop`。

```
t = table([1,1,2,2,3,3,4,4,5,5] as id, 1..10 as val)
select isortTop(val,2) from t context by id
```

之前版本结果：

| isortTop\_val |
| --- |
| 0 |
| 1 |

当前版本结果：

| isortTop\_val |
| --- |
| 0 |
| 1 |
| 0 |
| 1 |
| 0 |
| 1 |
| 0 |
| 1 |
| 0 |
| 1 |

* 分布式查询中，`subarray` 行为发生变化：

  + 在之前版本中，在每个分区内分别取 `subarray`，再将各分区结果合并组成最终结果。
  + 在当前版本中，将所有数据查询到内存计算一次 `subarray`。

```
db = database("dfs://test",VALUE,1..3)
t = table(take(1..3,15) as id,1..15 as val)
pt = db.createPartitionedTable(t,"pt",`id)
pt.append!(t)

select subarray(val,0:3) from pt
```

之前版本结果：

| result |
| --- |
| 1 |
| 4 |
| 7 |
| 2 |
| 5 |
| 8 |
| 3 |
| 6 |
| 9 |

当前版本结果：

| result |
| --- |
| 1 |
| 4 |
| 7 |

* 分布式查询中，聚合函数嵌套 `distinct` 时的行为发生变化：

  + 在之前版本中，可以执行，返回结果错误。
  + 在当前版本中，执行会报错。

```
dbName = "dfs://test_distinct"
if(existsDatabase(dbName)){
	dropDB(dbName)
}
db = database(dbName,RANGE,0 100 200 300 400,,`TSDB)
x = table(take(10..15 join 105..120 join 255..260 join 360..380,10000) as id,take(1 2 4 2 3,10000) as val)
pt = createPartitionedTable(db, x, 'pt', `id,,`id).append!(x)

select funcByName(`first)(distinct val) from pt

// 当前版本执行报错：
Cannot nest aggregate function. RefId: S02032
```

* 在 pivot by 查询中，使用除 `rowSum`, `rowMin`,
  `rowMax`, `rowCount`,
  `rowSum2`, `rowAnd`,
  `rowOr`, `rowXor`,
  `rowProd`, `rowWsum` 之外的 row
  系列函数时，行为发生变化：

  + 在之前版本中，可以执行，返回结果错误。
  + 在当前版本中，执行出现报错。

```
arr = 1..10
id = take(1..5,10)
type1 = take(1..2, 10)
type2 = take(1..3, 10)

t = table(arr, id, type1, type2)

select rowAvg(arr, id) from t pivot by type1, type2

// 当前版本，出现报错：
Row reduction operation [rowAvg] cannot be used with PIVOT BY. RefId: S02029
```

* equi join 引擎、时间序列聚合引擎和日级时间序列聚合引擎，在写入的列类型与 dummyTable
  指定的列类型不一致时，行为发生变化：

  + 在之前版本中，可以执行，不输出数据。
  + 在当前版本中，执行出现报错。

    ```
    share streamTable(1000:0, `time`sym`qty`price, [TIMESTAMP, SYMBOL, INT, INT]) as trades
    output1=streamTable(1:0,`time`sym`avg_qty`avg_price,[TIMESTAMP,SYMBOL,DOUBLE,DOUBLE])
    agg1=createTimeSeriesAggregator(name="agg1",windowSize=30000, step=30000, metrics=<[avg(qty),avg(price)]>,
    dummyTable=trades, outputTable=output1, timeColumn=`time, keyColumn=`sym)

    n = 10000
    insert into agg1 values(2024.02.01T00:00:00.000+1000*(1..n),take(`A,n),take(`A,n),take(`A,n))

    // 当前版本，出现报错：
    insert into agg1 values (2024.02.01T00:00:00.000 + 1000 * (1 .. n), take("A", n), take("A", n), take("A", n)) => Failed to append data to column 'price'
    ```
* 在指定 *chunkGranularity=”*TABLE” 的数据库中，在进行分布式表连接（仅 `ej`
  和 `lj`，且左右表都是分布式表）时删除表数据的行为发生变化：

  + 在之前版本中，可以执行，结果不正确。
  + 在当前版本中，执行出现报错。

    ```
    dbName ="dfs://test_pointManagement_append"
    if(existsDatabase(dbName)) {dropDB(dbName)}
    dbvalue = database(, VALUE, 1..10)
    dbtime = database(, VALUE, 2012.01.01..2012.01.10)
    db = database(dbName, COMPO, [dbvalue, dbtime],,`TSDB)
    create table "dfs://test_pointManagement_append"."pt1"(
    	par1 INT, par2 TIMESTAMP, intv INT
    )
    partitioned by par1, par2,
    sortColumns=[`par1, `par2],
    keepDuplicates = ALL
    go
    create table "dfs://test_pointManagement_append"."pt2"(
    	par1 INT, par2 TIMESTAMP, intv INT
    )
    partitioned by par1, par2,
    sortColumns=[`par1, `par2],
    keepDuplicates = ALL
    go

    t1 = table(1..10 as par1, 2012.01.01..2012.01.10 as par2, 1..10 as intv)
    t2 = table(1..10 as par1, 2012.01.01..2012.01.10 as par2, 1..10 as intv)

    pt1 = loadTable("dfs://test_pointManagement_append","pt1")
    pt2 = loadTable("dfs://test_pointManagement_append","pt2")
    pt1.append!(t1)
    pt2.append!(t2)

    delete pt1 from ej(pt1, pt2, `par1`par2)
    // 当前版本，出现报错：
    Joiner doesn't support both tables are distributed tables when left tablet type is SINGLE.
    ```

* 在分布式查询中，当 select 语句中某个列是局部变量，且该变量是向量时，查询的行为发生变化：

  + 在之前版本中，可以执行，结果不正确。
  + 在当前版本中，执行出现报错。

```
dbName = "dfs://test_analytical_function"
if(existsDatabase(dbName)){
	dropDatabase(dbName)
}
db=database(dbName, VALUE, 1..100)
n = 1000
t = table(take(1..10,n) as id,rand(100,n) as value)
pt = db.createPartitionedTable(t, "pt", ["id"]).append!(t)
m = 1
re = select *, row_number() OVER (partition by 1 order by m) as row_col from loadTable(dbName, "pt")
select *, 1..size(re)  from loadTable(dbName, "pt")
// 当前版本，出现报错：
All columns must be of the same length.
```
