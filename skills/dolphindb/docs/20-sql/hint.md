<!-- Auto-mirrored from upstream `documentation-main/progr/sql/hint.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# HINT 关键字

HINT 关键字是一种特殊的 SQL 指令，旨在提供一种直接指导数据库优化器执行策略的机制。在特定场景下，使用不同的 HINT 关键字，能够有效优化 SQL 查询的执行计划与效率
。

以下是 DolphinDB 支持的 HINT 关键字列表。

| 关键字 | flag | 使用说明 | 例子 |
| --- | --- | --- | --- |
| [HINT\_LOCAL] | [1] | 在分布式集群环境下， 仅获取在本地所有节点数据的查询结果。 | `select [HINT_LOCAL] sum(*) from pt` |
| [HINT\_HASH] | [32] | `group by` 分组时优先采用哈希算法。 | `select [HINT_HASH] count(*) from t group by sym` |
| [HINT\_SNAPSHOT] | [64] | 使用 `registerSnapshotEngine` 注册快照引擎后，从分布式表的快照引擎中查询数据。 | `select [HINT_SNAPSHOT] * from loadTable(dbName,tableName)` |
| [HINT\_KEEPORDER] | [128] | 确保 `context by` 分组后计算的输出结果顺序和输入保持一致。 | `select [HINT_KEEPORDER] cumsum(vol) from t context by date, sym` |
| [HINT\_SEQ] | [512] | 内存资源紧缺时，使分区查询串行执行，节约并发的资源开销。 | `timer select [HINT_SEQ] avg(vol) from t` |
| [HINT\_NOMERGE] | [1024] | 对无需返回查询结果的中间步骤，省略查询结果的合并步骤，直接返回分区表的句柄。 | `select [HINT_NOMERGE] price from pt context by ticker` |
| [HINT\_PRELOAD] | [4096] | 仅 TSDB引擎支持，在 `where` 语句进行条件过滤前预加载相关数据。 | `select [HINT_PRELOAD] sum(price) from t where volume > 100000` |
| [HINT\_EXPLAIN] | [32768] | 用于 SQL 查询性能调优，执行 SQL 语句时系统将打印执行过程，以实时监测查询速度和执行顺序。详见[[HINT\_EXPLAIN]](hint_explain.html)。 | `select [HINT_EXPLAIN] * from tb where id > 20` |
| [HINT\_SORT] | [524288] | `group by` 分组时使用排序算法进行数据处理。 | `select [HINT_SORT] avg(price) from trades group by sym` |
| [HINT\_VECTORIZED] | [4194304] | `group by` 分组时采用向量化运算（vectorization）。 | `select [HINT_VECTORIZED] sum(price) from trades group by sym` |
