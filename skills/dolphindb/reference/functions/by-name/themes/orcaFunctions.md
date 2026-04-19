# Orca 系列

Orca 实时计算平台构建于 DolphinDB 流数据框架之上，提供了更高层次的抽象。通过声明式
API，用户无需关注底层的并行调度、订阅机制及资源管理等实现细节，可专注于业务逻辑开发。

| 分类 | 接口 | 功能简述 |
| --- | --- | --- |
| 定义 | createStreamGraph | 创建一个 StreamGraph 对象 |
| StreamGraph::setConfigMap | 设置图的私有流表和订阅的配置项 |
| StreamGraph::source / keyedSource / latestKeyedSource / haSource / haKeyedSource | 定义流图输入源流表 |
| StreamGraph::sourceByName | 获取一个 Orca 创建的公共流表 |
| DStream::anomalyDetectionEngine | 定义异常检测引擎 |
| DStream::asofJoinEngine | 定义 asof join 引擎 |
| DStream::crossSectionalEngine | 定义横截面计算引擎 |
| DStream::cryptoOrderBookEngine | 定义数字货币实时订单簿引擎 |
| DStream::dailyTimeSeriesEngine | 定义日级时间序列引擎 |
| DStream::dualOwnershipReactiveStateEngine | 定义 Dual Ownership 响应式状态引擎 |
| DStream::narrowReactiveStateEngine | 定义生成窄表的响应式状态引擎 |
| DStream::orderBookSnapshotEngine | 定义订单簿引擎 |
| DStream::reactiveStateEngine | 定义响应式状态引擎 |
| DStream::reactiveStatelessEngine | 定义响应式无状态引擎 |
| DStream::ruleEngine | 定义规则引擎 |
| DStream::sessionWindowEngine | 定义会话窗口引擎 |
| DStream::timeBucketEngine | 定义自定义窗口长度（长度相同或不同）的时间序列聚合引擎 |
| DStream::timeSeriesEngine | 定义时间序列聚合引擎 |
| DStream::equalJoinEngine | 定义等值连接引擎 |
| DStream::leftSemiJoinEngine | 定义左半等值连接引擎 |
| DStream::lookupJoinEngine | 定义 lookup join 引擎 |
| DStream::snapshotJoinEngine | 定义快照连接引擎 |
| DStream::windowJoinEngine | 定义窗口连接引擎 |
| DStream::buffer / keyedBuffer / latestKeyedBuffer | 定义中间结果流表 |
| DStream::sink / keyedSink / latestKeySink / haSource / haKeyedSource | 定义数据输出流表 |
| DStream::map | 定义数据转换逻辑 |
| DStream::udfEngine | 创建支持副作用和状态持久化的自定义函数 |
| DStream::fork | 定义流图分叉 |
| DStream::parallelize | 设置并行度 |
| DStream::sync | 汇总上游计算结果 |
| DStream::setEngineName | 设置当前引擎名称 |
| DStream::getOutputSchema | 获取表结构用于下游定义 |
| DStream::timerEngine | 定义一个时间触发引擎 |
| DStream::sharedDict | 创建一个共享字典 |
| DStream::sharedKeyedTable | 创建一个共享键值内存表 |
| DStream::sharedTable | 创建一个共享内存表 |
| 流图管理 | StreamGraph::submit | 提交流图以启动运行 |
| getStreamGraph | 获取流图对象 |
| dropStreamGraph / StreamGraph::dropGraph | 销毁流图 |
| purgeStreamGraphRecords | 删除流图记录 |
| startStreamGraph / stopStreamGraph | 启、停流图 |
| DStream::timerEngine / stopTimerEngine / resumeTimerEngine | 提交、暂停、恢复基于时间触发的任务 |
| 流表操作 | appendOrcaStreamTable | 向流表插入数据 |
| useOrcaStreamTable | 远程调用并操作指定流表 |
| select \* from orca\_table.<name> 或select \* from <catalog>.orca\_table.<name> | 查询流表内容 |
| 引擎操作 | warmupOrcaStreamEngine | 预热流引擎以提升首批计算效率 |
| 监控运维 | getStreamGraphInfo/getStreamGraphMeta | 获取流图元信息 |
| getOrcaStreamTableMeta | 获取流表元信息 |
| getOrcaStreamEngineMeta | 获取流引擎元信息 |
| getOrcaStreamTaskSubscriptionMeta | 获取订阅元信息 |
| getOrcaStateMachineEventTaskStatus | 获取状态机任务状态 |
| StreamGraph::toGraphviz / str | 输出拓扑结构 |
| getUdfEngineVariable | 查询自定义函数中指定外部变量的当前值。 |
| stopTimerEngine | 暂停由 `DStream::timerEngine` 提交的任务 |
| resumeTimerEngine | 恢复执行由 `DStream::timerEngine` 提交的任务。 |
| updateStreamGraphUserTickets | 更新流图创建者的认证状态 |
| Checkpoint 管理 | setOrcaCheckpointConfig | 配置 Checkpoint 参数 |
| getOrcaCheckpointConfig | 查看 Checkpoint 配置 |
| getOrcaCheckpointJobInfo | 查看 Checkpoint Job 运行信息 |
| getOrcaCheckpointSubjobInfo | 查看 Checkpoint 子任务运行信息 |
