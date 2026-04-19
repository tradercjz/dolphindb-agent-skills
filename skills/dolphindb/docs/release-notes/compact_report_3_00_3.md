<!-- Auto-mirrored from upstream `documentation-main/rn/compact_report_3_00_3.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.3

## 缺陷修复带来的系统影响

* 修改函数 `elasticNetCV`, `lassoCV`,
  `ridgeCV` 参数校验：

  + 旧版本中，参数 *yColName*, *xColNames* 可以指定时间类型的列。
  + 新版本起，参数 *yColName*, *xColNames* 仅支持数值类型列，否则会报错。
* 修改 `iif` 函数和三元运算符 `?:` 返回值类型：

  + 旧版本中，优先根据 *trueResult* 和 *falseResult* 数据形式确定返回值的形式。
  + 新版本起，返回值与 *cond* 的数据形式一致。

  ```
  iif([true,false],1:2,(3..4$1:2))
  true false?(1:2):(3..4$1:2)
  // 旧版本返回 INT PAIR 1:4
  // 新版本返回 FAST INT VECTOR [1,4]
  ```
* 修改函数 `seq` 对 NULL 值的处理行为。当 *start* 或 *end* 任一为 NULL
  时：

  + 旧版本会返回不符合预期的结果。
  + 新版本会直接报错。
* 若建表时为 LONG 或 NANOTIMESTAMP 类型的列指定 delta of delta
  压缩算法（即`compressMethods="delta"`），当 delta-of-delta
  值溢出时：

  + 旧版本中，数据刷盘失败且持续重试，导致系统阻塞。
  + 新版本起，溢出数据会转换为空值。

  ```
  dbName = "dfs://test"
  if(existsDatabase(dbName)) {
      dropDatabase(dbName)
  }
  db = database(dbName,HASH, [INT, 1])
  t = table(10:0,[`id, `data],[INT, LONG])
  pt = db.createPartitionedTable(t, `pt, `id,  {data:"delta"})
  t =  table(1..5 as id, [1,1,8704332179800340403, 105, 27162335252578330] as data)
  pt.append!(t)
  purgeCacheEngine()
  sleep(1000)
  select * from pt
  ```

  新版本查询结果：

  | id | data |
  | --- | --- |
  | 1 | 1 |
  | 2 | 1 |
  | 3 | 8,704,332,179,800,340,403 |
  | 4 |  |
  | 5 |  |
* 当 SQL CASE 语句的 THEN 和 ELSE 子句中使用 `string` 函数且返回标量时，旧版本返回
  STRING 类型，新版本改为 SYMBOL 类型。

  ```
  t = table(0 NULL 1 as id)
  re = select case when id=0 then string("a")  else  string("b") end from t
  select name,typeString from schema(re).colDefs
  // 旧版本 col1 列为 STRING 类型
  // 新版本 col1 列为 SYMBOL 类型
  ```
* 修改 `varma` 函数输入数据源时的排序逻辑：

  + 旧版本中，模型会根据数据源第一列对数据自动排序。
  + 新版本起，仅当第一列是时间列时，模型才会对数据排序。
* 修改非管理员用户执行 `getClusterDFSDatabases` 时的可见范围：

  + 旧版本中，返回用户拥有 DB\_MANAGE 权限或自己创建的分布式数据库。
  + 新版本起，新增返回用户拥有DB\_READ/DB\_INSERT/DB\_UPDATE/DB\_DELETE/DBOBJ\_CREATE/DBOBJ\_DELETE
    权限的分布式数据库。

* 在 SQL EXEC 语句中若使用了 DISTINCT
  和聚合函数，并且查询涉及表连接，旧版本的查询结果为一个标量，新版本中则返回一个向量。

  ```
  sym = `C`MS`MS`MS`IBM`IBM`C`C`C$SYMBOL
  price= 49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29
  qty = 2200 1900 2100 3200 6800 5400 1300 2500 8800
  t1 = table(sym, qty);
  t2 = table(sym, price);

  x = exec distinct count(price) from t1 full outer join t2 on t1.sym=t2.sym;
  typestr x;
  //老版本返回 INT
  //新版本返回 FAST INT VECTOR
  ```
* 在创建流数据日级时间序列引擎 (`createDailyTimeSeriesEngine`) 时：
  + 若配置了 session 时段*，*则 *roundTime* 不再生效，*mergeLastWindow*不再规整 session 时段*。*
  + 采用如下方式指定跨天 session
    时段时：

    ```
    sessionBegin = [00:00:00, 09:00:00, 13:00:00, 21:00:00]
    sessionEnd = [01:00:00, 11:30:00, 15:00:00, 00:00:00]

    //即 session 时段为21:00:00-次日01:00:00，09:00:00-11:30:00， 13:00:00-15:00:00。
    ```

    *keyPurgeDaily*
    的行为发生变化：
    - 在之前版本中，*keyPurgeDaily* 在 21:00:00 之前不生效，15:00:00-21:00:00
      之间的数据会并入 21:00:00的窗口。
    - 在新版本中，*keyPurgeDaily* 在 21:00:00 之前生效，15:00:00-21:00:00
      之间的数据会被丢弃。
* 当用户的权限发生变化：
  + 在旧版本中，该用户可以在当前会话中通过切换为其他用户后再次登录（`login`）的方式来生效新权限。
  + 在新版本中，权限变更后必须显式执行登出（`logout`）操作，并重新登录，才能获取最新的权限设置。
* 函数 `getUserAccess` 的返回结果中，原 “COMPUTE\_GROUP\_allowed” 字段名自新版本起改为
  “COMPUTE\_GROUP\_EXEC\_allowed”。
* 在新版本中，设置了对 SQL 查询 WHERE 子句的限制：WHERE 子句中的条件数量（以逗号分隔）最多为 1024 个；每个条件表达式中最多允许 1024
  个运算符（包括 AND）。若超过限制，系统将报错。
* 自新版本起，将不再支持快照引擎（由 `registerSnapshotEngine`创建）。用户可使用IOTDB 引擎（通过
  CREATE 语句等方式指定）实现相同的功能，获取每个分组的最新记录。
* 旧版本中，单次事务写入的数据量无限制。新版本起，为提升系统稳定性，引入了单次事务写入大小限制，默认限制为存储引擎 Cache Engine 容量上限的
  20%。当写入数据量超过限制时，将会报错，例如：

  ```
  Memory size of append transaction 2000000216 exceeds max limit (429496729) for OLAP. Please split data into batches.
  ```

  如需保持旧版本行为，可通过以下方式取消或放宽该限制：
  + 设置配置参数 *maxTransactionRatio*=1，即将事务大小限制调整为 Cache Engine 上限的
    100%；
  + 或在运行时调用 `setMaxTransactionSize` 动态修改限制值。
* 在旧版本中：在内存表中，对于元素类型相同的元组（ANY）所创建的列，系统会自动将其转换为列式元组类型（ColumnarTuple）。转换后，该列不再允许插入其他类型的数据，若尝试插入将报错。

  从新版本起：系统不再自动执行上述转换，而是保持为普通的ANY类型列，因此允许插入不同类型的数据。

  ```
  id = 1 2 3
  val = [[1,2,3,4], [4,5,6],[7,8,9]]
  t = table(id, val)
  isColumnarTuple(t[`val])
  //老版本返回 true
  //新版本返回 false

  insert into t values(1, "a")  // 老版本报错：Failed to append data to column 'val'.
  insert into t values(1, "a") //新版本可以插入
  ```

  为保持对旧版本行为的兼容性，引入配置项
  *autoConversionToColumnarTuple*，默认值为
  false，表示默认采用新版本行为（不自动转换为列式元组）。如需兼容老版本行为，可将该配置项设置为 true。
* 增强了异常检测引擎的参数校验。当调用 `createAnomalyDetectionEngine` 函数时，如果传入非法的
  *metrics* 参数：
  + 在旧版本中，函数执行不会立即报错，而是在数据写入后，通过 `getStreamEngineStat`
    函数返回错误信息。
  + 在新版本中，系统会在创建引擎时直接抛出异常。
* 在 SQL 分布式查询中，如果 SELECT 语句中引用了 `tableName.colName`，且 FROM 子句包含了带
  JOIN 的子查询，新版本中必须为该子查询显式指定 AS 表名，否则会报错 `SQL context is not initialized
  yet`。

  ```
  dbName = "dfs://test"
  if(existsDatabase(dbName)){
          dropDatabase(dbName)
  }
  db = database(dbName, VALUE,  1..100)
  n = 100
  t = table(take(0..30, n) as id, rand(10 ,n) col1, rand(10 ,n) col2)
  pt1 = db.createPartitionedTable(t, `pt1, `id).append!(t)
  pt2 = db.createPartitionedTable(t, `pt2, `id).append!(t)
  // 旧版本中无需指定别名
  select pt1.id in 1..5 from (select * from pt1 full join pt2 on pt1.col1=pt2.col1)
  // 新版本必须显式指定别名
  select pt1.id in 1..5 from (select * from pt1 full join pt2 on pt1.col1=pt2.col1) as pt1
  ```

  在多表连接后执行
  SELECT \* 语句可能会导致较高的内存消耗。建议在 SELECT 子句中明确指定实际所需的列，以避免不必要的资源占用和潜在的性能问题。

修改 CEP monitor 相关接口：

* 新版本起，定义 monitor 类时必须显式继承
  `CEPMonitor`。

  ```
  // 旧版本
  class mainMonitor{
    ...
  }
  // 新版本
  class mainMonitor:CEPMonitor{
    ...
  }
  ```

修改 CEP monitor 相关接口：

* 在 CEP monitor 中使用 `getDataViewEngine` 获取 DataView
  引擎数据时，旧版本要求将 *CEPEngine* 参数置空。新版本起，支持直接传入 DataView
  引擎名称。

  ```
  // 旧版本
  getDataViewEngine(,'traderDV')
  // 新版本
  getDataViewEngine('traderDV')
  ```
* 旧版本中，在 CEP monitor 内部调用 `dropStreamEngine`
  可以删除外部流引擎。新版本起，该方法仅可删除当前 CEP 引擎内创建的流引擎。
* `spawnMonitor`接口新增 *name*
  参数：

  ```
  // 旧版本
  spawnMonitor(handler, args...)
  // 新版本
  spawnMonitor(name, handler, args...)
  ```

  *name* 为新生成 monitor
  的唯一标识。若与现有 monitor 重名，`spawnMonitor` 将失败并报错。
