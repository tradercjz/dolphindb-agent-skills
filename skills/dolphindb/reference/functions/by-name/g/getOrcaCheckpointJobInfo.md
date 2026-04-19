# getOrcaCheckpointJobInfo

首发版本：3.00.3

## 语法

`getOrcaCheckpointJobInfo([name])`

## 详情

查看指定流图的 Checkpoint 运行情况。如果未指定 *name*，则返回 Orca 中所有流图的 Checkpoint 运行情况。

## 参数

**name** 可选参数，字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

返回一个表，包含以下字段：

* checkpointId：Checkpoint id
* jobId：流图 id
* createdTimeStamp：Checkpoint 任务的创建时间
* finishedTimeStamp：Checkpoint 任务完成的时间
* status：Checkpoint 任务的状态，
  + RUNNING：正在运行
  + ERROR：发生一般性错误，后续会重新发起新的 Checkpoint 任务进行重试
  + FAILED：发生严重错误，无法重试
  + SUCCESS：Checkpoint 成功，该 Checkpoint 处于可用状态
  + CANCELED：Checkpoint 任务被系统取消，此状态通产由于一个流图同时有多个 Checkpoint 任务在 RUNNING
    状态，当它们中最新的 Checkpoint 成功后，系统会自动取消旧的 Checkpoint。
  + PURGED：系统默认只保存最近成功的几个 Checkpoint（由配置项 maxRetainedCheckpoints
    管理），超出该参数，系统会自动清理旧的 Checkpoint 数据。
* extra：额外信息，例如 Checkpoint 的错误信息。
* partitionId：Checkpoint 元信息所在分区的 ID。

## 例子

```
getOrcaCheckpointJobInfo("streamGraph1") // name 是流图名称
getOrcaCheckpointJobInfo("catalog1.orca_graph.streamGraph1") // name 是全限定名
```
