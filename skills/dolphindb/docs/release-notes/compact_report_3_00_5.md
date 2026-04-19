<!-- Auto-mirrored from upstream `documentation-main/rn/compact_report_3_00_5.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 3.00.5

## 涉及保持一致性或兼容行业惯例的修改

* 系统初始化脚本文件 dolphindb.dos 中新增了 `covarp` 及其对应的系列函数。升级 server
  时需要同步更新该文件。
* 流订阅 topic 格式发生变化：

  + 旧版本格式为 host:port:nodeAlias/tableName/actionName，如
    `localhost:8848:nodeA/trades/demo`
  + 新版本常规订阅普通流表格式保持不变，仍为 host:port:nodeAlias/tableName/actionName
  + 新版本常规订阅高可用流表格式为 clusterName\_RaftGroupId/tableName/actionName
  + 新版本高可用订阅普通流表格式为
    host:port:nodeAlias/tableName/actionName/subscriberNode
  + 新版本高可用订阅高可用流表格式为
    clusterName\_RaftGroupId/tableName/actionName/subscriberNode
* 弃用配置项 streamingHADiskLimit，streamingHAPurgeInterval。
* 配置项 streamingHADir 更名为 streamingHALogDir，默认值修改为 /log/streamingHALog。
* 启用流数据高可用前，必须在配置文件中设置配置项 clusterName，否则无法启用。
* 函数 `haStreamTable` 的参数 *cacheLimit* 更名为
  *cacheSize*。
* 高可用流表不再支持增加列（`addColumn`）。
* 取消高可用订阅时，必须指定 *raftGroup*，否则取消订阅失败。
* 流引擎暂不支持高可用，引擎的 *raftGroup* 参数暂不生效。
* 弃用函数
  `amortizingFixedRateBondDirtyPrice`，`convertibleFixedRateBondDirtyPrice`，`callableFixedRateBondDirtyPrice`，`floatingRateBondDirtyPrice`，`crmwCBond`，`cds`，`irs`。
* 配置项 OLAPCacheEngineSize 和 TSDBCacheEngineSize 不能超过该节点配置项 maxMemSize 的
  50%，超过会导致节点启动失败。函数 `setOLAPCacheEngineSize` 和
  `setTSDBCacheEngineSize` 在线调整超出限制时报错。
* 函数 `restoreSettings` 执行后，当前用户会被强制退出登录，需再次登录以获得对应权限。
* `createTimeSeriesEngine` 和
  `createDailyTimeSeriesEngine` 在指定 *fill*
  时，旧版本不会填充数组向量列，新版本会填充。
* `createTimeSeriesEngine` 和
  `createDailyTimeSeriesEngine` 在指定多个 *windowSize*
  时:

  + 旧版本仅在每个窗口都有数据时输出。
  + 新版本在最大窗口有数据时输出，没有数据的窗口对应的因子返回空值。

  ```
  metrics=[<last(col1)>, <last(col2)>]
  st1 = streamTable(1000000:0, `timestamp`col1`col2,[TIMESTAMP,DOUBLE,DOUBLE])
  st2 = streamTable(100:0,`timestamp`col1`col2,[TIMESTAMP,DOUBLE,DOUBLE]);
  demoEngine=createDailyTimeSeriesEngine(name="demoEngine",windowSize=[1000, 5000],step=1000,metrics=metrics,dummyTable=st1,outputTable=st2,timeColumn=`timestamp);

  timestampv = temporalAdd(2026.01.01T00:00:00.001, [0, 1, 2, 4, 8], "s")
  col1 = double(1..5)
  col2 = double(11..15)
  tmp = table(timestampv as timestamp,  col1 as col1, col2 as col2)
  demoEngine.append!(tmp)

  st2
  /*
  旧版本：
  timestamp               col1 col2
  ----------------------- ---- ----
  2026.01.01T00:00:01.000 1    11
  2026.01.01T00:00:02.000 2    12
  2026.01.01T00:00:03.000 3    13
  2026.01.01T00:00:05.000 4    14

  新版本：
  timestamp               col1 col2
  ----------------------- ---- ----
  2026.01.01T00:00:01.000 1    11
  2026.01.01T00:00:02.000 2    12
  2026.01.01T00:00:03.000 3    13
  2026.01.01T00:00:04.000      13
  2026.01.01T00:00:05.000 4    14
  2026.01.01T00:00:06.000      14
  2026.01.01T00:00:07.000      14
  2026.01.01T00:00:08.000      14
  */
  ```
* `createWindowJoinEngine` 和
  `createNearestJoinEngine` 当 *window* 不为 0:0 时：

  + 旧版本不支持输出非聚合结果，新版本支持
  + 当 *metric* 的计算结果不为数组向量而输出表对应的列为数组向量时，旧版本报错，新版本会自动将结果转换成数组向量
* `createWindowJoinEngine` 和
  `createNearestJoinEngine`
  旧版本左表数组向量列可作为接收向量为参数的聚合函数，新版本不再支持，但可通过函数 `byRow`
  实现，如下例所示。

  ```
  share streamTable(1:0, `timev`sym`id`price, [TIMESTAMP, SYMBOL, INT, DOUBLE[]]) as leftTable
  share streamTable(1:0, `timev`sym`id`val, [TIMESTAMP, SYMBOL, INT, INT]) as rightTable
  output = table(1:0, `timev`sym`price`val`factor, [TIMESTAMP, SYMBOL, DOUBLE[], INT[], DOUBLE])

  wjEngine=createWindowJoinEngine(name="testWindowJoin", leftTable=leftTable, rightTable=rightTable, outputTable=output, window=0:0, metrics=<[price, val, percentile(price, 20)]>, matchingColumn="sym", timeColumn="timev", useSystemTime=false, garbageSize=5000, maxDelayedTime=3000,outputElapsedMicroseconds=false, sortByTime=false)
  // 旧版本正常运行
  // 新版本报错 Invalid metric percentile(price, 20). Usage: percentile(X, percent, [interpolation='linear']). X must be a numeric vector.

  // 新版本可使用如下脚本实现原计算逻辑逻辑
  wjEngine=createWindowJoinEngine(name="testWindowJoin", leftTable=leftTable, rightTable=rightTable, outputTable=output, window=0:0, metrics=<[price, val, byRow(percentile{,20}, price)]>, matchingColumn="sym", timeColumn="timev", useSystemTime=false, garbageSize=5000, maxDelayedTime=3000,outputElapsedMicroseconds=false, sortByTime=false)
  ```
* 最近邻关联引擎 `createNearestJoinEngine` 旧版本 *metrics*
  不支持左表数组向量列直接作为计算指标，新版本支持。
* 多表 JOIN 中 ON 子句内不再支持使用聚合函数。
* 配置项 enableORCA 的默认值由 true 修改为 false。
* Orca 新增权限管理，操作需具备相应权限。
* 跨集群授权读取 Orca 中流表的权限类型由 TABLE\_READ 改为 ORCA\_TABLE\_READ。
* INSTRUMENT 类型对象中，notional 字段拆分为 notionalAmount 和 notionalCurrency。
* MKTDATA 类型中的 mktDataType 字段，原 Spot 类型更名为 Price。
* 函数 `getClusterDFSDatabases` 和
  `getClusterDFSTables` 不再允许非管理员用户查看系统创建的 Orca
  专用库表。管理员可通过设置参数 *includeSysDb* 和 *includeSysTable* 查看。
* `dropStreamTable` 不再支持 Orca 流表，如需删除请使用
  `dropOrcaStreamTable`；dropStreamEngine 不再支持 Orca
  引擎，如需删除请使用 `dropStreamGraph` 删除其所属流图。

## 缺陷修复带来的系统影响

* 内存表运算中，时间类型数据相加的结果类型发生变化：

  + 旧版本结果为时间类型
  + 新版本结果为整型

  ```
  t1 = table([2026.01.01,2026.01.02,2026.01.03] as timeCol)
  t2 = table([2026.02.01,2026.02.02,2026.02.03] as timeCol)
  t1 + t2

  /*
  旧版本结果：
  timeCol
  ----------
  2026.01.01
  2026.01.02
  2026.01.03

  新版本结果：
  timeCol
  -------
  40939
  40941
  40943
  */
  ```
* 对数组向量调用函数 `row` 和 `at` 时，行为发生变化：

  + row：旧版本以`row(start:end)`的方式获取连续多行结果错误，新版本修正
  + at：旧版本支持以`at([index1 index2])` 的方式获取指定行，新版本报错，可改写为
    `at([index1,index2])`

  ```
  a = array(INT[], 0, 15).append!([1 2 3, 5 6, 7 8 9, 10 11 12 15])
  a.row(0:2)
  /*
  旧版本 output:[1,5]
  新版本 output:[[1,2,3],[5,6]]
  */

  a.at([1 2])
  /*
  旧版本 output:[[5,6],[7,8,9]]
  新版本报错： Invalid index
  新版本修改为 a.at([1,2]),output:[[5,6],[7,8,9]]
  */
  ```
* 当发布订阅功能关闭（配置项 maxPubConnections=0）时，函数 `getStreamingStat`
  行为发生变化：

  + 旧版本正常执行
  + 新版本报错
* 当数据写入键值流表时，如果键值列的数据类型不一致，写入行为发生变化：

  + 旧版本先根据键值列的原始数据去重，再转换类型，最终写入
  + 新版本先转换数据类型，根据转换后的键值列数据去重，最终写入

  ```
  kt = keyedStreamTable(`date,1:0,`date`value,[DATE,DOUBLE])
  kt.append!(table(2026.01.01 12:00:00.000 as date, 1.1 as value))
  kt.append!(table(2026.01.01 12:00:01.000 as date, 2.2 as value))
  kt.size()
  /*
  旧版本 output：2
  新版本 output：1
  */
  ```
* 异常检测引擎 `createAnomalyDetectionEngine` 增加对 *metrics*
  的校验，当其不是布尔表达式时：

  + 旧版本正常执行
  + 新版本报错

## 升级注意事项

由于权限文件存在兼容性问题，升级前需要备份权限相关的 ACL 文件；若使用了 Raft 集群，还需备份 Raft 相关的文件。需要备份的文件列表如下：

| 部署环境 | HomeDir 路径参考 | 需要备份的文件 |
| --- | --- | --- |
| 单节点 | <YourPath>/server/local8848 | <homeDir>/sysmgmt /   * aclCheckPoint.meta * aclEditlog.meta |
| 普通集群 | <YourPath>/server/cluster/data/<controllerAlias> | <homeDir>/sysmgmt/   * aclCheckPoint.meta * aclEditlog.meta |
| 高可用集群 | <YourPath>/server/clusterDemo/data/<controllerAlias\_k>  Raft 组所有控制节点都需要备份 | <homeDir>/sysmgmt/   * aclCheckPoint.meta * aclEditlog.meta   <homeDir>/raft/   * raftHardstate * raftSnapshot * raftWAL |
