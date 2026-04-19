<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db/rebalance.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 数据平衡

数据平衡是指在一个集群中，数据在各个节点之间存储均匀。数据平衡直接关系到系统的性能、可用性和稳定性，因此在分布式架构设计中需要充分考虑如何进行数据平衡。DolphinDB
的分布式架构对数据存储进行了全局优化，可以将集群内的数据均匀地存储到不同地节点上，充分利用集群中的物理资源。但在某些情况下，例如集群中节点/磁盘数量发生了变化，这些变化可能导致数据在节点之间分布不均，进而使得部分节点负载沉重，而其他节点相对空闲。这可能导致集群无法充分利用新增节点的计算资源，无法充分利用新增磁盘的
I/O。为提升 DolphinDB 集群服务能力，DolphinDB 提供了水平扩缩容和垂直扩缩容的负载均衡能力。

水平扩缩容是一个集群通过增加或减少数据节点的数量来调整集群的资源和处理能力。在集群进行了水平扩缩容后，需要进行数据的重分布，以确保数据在所有节点之间均匀分布。

垂直扩缩容是指在数据节点数量不变的情况下，通过增加或减少单个数据节点上的磁盘空间来调整资源。同样，在完成垂直扩缩容后，也需要进行数据重分布，以确保数据在该节点的各个磁盘上均匀分布。

## 实现机制

通过监控集群的存储容量、占用情况以及各磁盘的占用率，动态选择源路径（待平衡的数据的物理路径）和目标路径（优先使用本机磁盘），将数据从高占用率的磁盘迁移到低占用率的磁盘，实现负载均衡。整个数据平衡过程包括以下几个阶段：

1. 预处理：验证相关权限和参数，包括用户是否具有管理员权限及请求是否来自控制节点。检查是否存在其它正在进行中的平衡任务。只有在通过校验和检查时，才进入下一阶段。
2. 信息收集：收集磁盘信息，统计源磁盘和目标磁盘列表、并收集所有数据（chunk）信息，包括
   chunkId，chunkGranularity，数据大小等。
3. 任务分配：优先将待平衡数据分配给本机目标磁盘；若本机目标磁盘容量不足，则分配给其他机器上的磁盘占用率最低的磁盘，最终确定所有平衡任务对应的源路径和目标路径。
4. 任务执行：以数据的物理路径为单位进行数据迁移。根据第 3 步的平衡任务数量，针对不同的源路径和目标路径，并行迁移任务。

## 数据再平衡方法

DolphinDB 提供 rebalanceChunksWithinDataNode 和 rebalanceChunksAmongDataNodes 函数进行数据再平衡。

* `rebalanceChunksWithinDataNode`：通过该函数对节点内数据进行再平衡。
* `rebalanceChunksAmongDataNodes`：

  1. 对于 2.00.12/3.00.0 之前版本，通过该函数对节点间数据进行再平衡。而 2.00.12/3.00.0
     及之后版本，可以通过该函数实现集群内所有磁盘间的数据再平衡。
  2. 当配置分区粒度为表级分区时，同一个分区的所有表将分布在相同的节点下。当调用函数
     `rebalanceChunksAmongDataNodes`
     进行数据平衡时，若出现节点宕机或离线，可能出现同一个分区里部分表的数据转移成功，部分表的数据转移失败的情况，即同一个分区下的不同表会分布在不同的节点。此时需要调用
     `restoreDislocatedTablet` 将同一个分区里的表转移到同一个节点下。

`rebalanceChunksWithinDataNode` 和
`rebalanceChunksAmongDataNodes` 函数允许用户通过参数
*updatedBeforeDays* 设置平衡数据的时间范围，或者通过参数 *exec* 选择是否仅生成平衡计划。建议首先设置
*exec*=false 仅生成平衡计划，在确认数据平衡计划正确后，再次执行函数同时设置 *exec*=true 以执行平衡计划。

需要注意的是，因为磁盘可能存储除 DolphinDB 数据库以外的数据，或者 DolphinDB
数据分区大小不相等，这些差异可能会导致出现再平衡结果不符合预期。可以通过多次执行再平衡，进一步优化再平衡的效果。也可以通过配置项
*dfsRebalanceConcurrency* 设置再平衡任务执行的并发度，提高再平衡衡任务的执行效率。

## 常见问题

以下是在数据平衡过程中可能发生的常见情况：

* 数据迁移和再平衡任务可能会消耗大量资源，正在被写入、修改或删除的分区可能由于分区锁定而无法迁移。
* 对于耗时的计算任务，当缓存指向旧分区路径时可能会抛出异常。

因此，建议在没有执行写入或查询任务时执行数据再平衡操作，以避免潜在的失败。

有关数据再平衡的更多操作详情，请参考数据迁移与平衡 和运维手册中的《数据迁移与平衡》。

**相关信息**

* [rebalanceChunksAmongDataNodes](../../funcs/r/rebalanceChunksAmongDataNodes.html "rebalanceChunksAmongDataNodes")
* [rebalanceChunksWithinDataNode](../../funcs/r/rebalanceChunksWithinDataNode.html "rebalanceChunksWithinDataNode")
