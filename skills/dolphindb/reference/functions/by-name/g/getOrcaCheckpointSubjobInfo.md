# getOrcaCheckpointSubjobInfo

首发版本：3.00.3

## 语法

`getOrcaCheckpointSubjobInfo([name])`

## 详情

查看指定流图 Checkpoint 子任务的运行情况。如果未指定 *name*，则返回 Orca 中所有流图的 Checkpoint 运行情况。

## 参数

**name** 可选参数，字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

返回一个表，包括以下字段：

checkpointId：Checkpoint id

jobId：流图 id

subjobId：子任务 id

firstBarrierArrTs：Checkpoint 子任务收到第一个 Barrier 的时刻。

barrierAlignTs：Checkpoint 子任务的 Barrier 对齐的时刻。

barrierForwardTs：Checkpoint 子任务向下游转发 Barrier 的时刻。

status：Checkpoint 子任务状态，包括 running、success、failed。

snapshotChannelsId：Checkpoint 子任务的输入端 Channel 的 id。

downstreamSubscribeOffsets：下游订阅的 offset。

snapshotMeta：Checkpoint 数据的元信息。

extra：额外信息，例如 Checkpoint 的错误信息

## 例子

```
getOrcaCheckpointSubjobInfo("streamGraph1") // name 是流图名称
getOrcaCheckpointSubjobInfo("catalog1.orca_graph.streamGraph1") // name 是全限定名
```
