<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db/limits.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 使用限制

本节介绍 DolphinDB 的常见使用限制，包括用户与权限管理、网络连接、数据库对象、数据类型、查询事务以及系统资源等方面的数量和大小限制。

| 限制项 | 上限 |
| --- | --- |
| 用户（User）数量 | 无 |
| 用户组（Group）数量 | 无 |
| 同一用户组内的用户数量 | 无 |
| 网络连接数 | 取决于配置项 *maxConnections*（如果调用 `setMaxConnections` 动态修改，上限为 65,536） |
| 单个会话（Session）内变量（Variable）的数量 | 无 |
| 共享（shared）变量的数量 | 65,536 |
| 函数视图（FunctionView）数量 | 无 |
| 定时任务（scheduleJob）数量 | 无 |
| 数据库数量 | 无 |
| 表数量 | 无 |
| 组合分区（COMPO）的层级数 | 3 |
| 分区个数 | 无 |
| 分区内行数 | 2,147,483,648 |
| 表行数 | 内存表：2,147,483,648  分布式表：无 |
| 表列数 | 无 |
| STRING 类型长度 | 分布式表：65,536 字节（64KB）  OLTP 引擎表：若作为索引字段，限制 4,096 字节  内存表：无 |
| BLOB 类型长度 | 分布式表：67,108,864 字节（64MB）  其它：无 |
| SYMBOL 类型长度 | 分布式表：256 字节  其它：无 |
| 单个分区 SYMBOL 列不同值的数量 | 2,097,152 |
| 单个 SQL 查询的结果大小 | 分布式表：总内存的 80%  其它：无 |
| 单个 SQL 查询涉及的分区数 | 取决于配置项 *maxPartitionNumPerQuery* |
| 单个事务允许执行的时间 | 无 |
| 单个查询允许执行的时间 | 无 |
| 可用内存大小 | 由 license 、物理内存和配置项 *maxMemSize* 限制 |
| 可用 CPU 核数 | 由 license、物理 CPU 核数和配置项*workerNum* 限制 |
| 集群包含的节点数量 | 由 license 限制 |
