# getSlaveReplicationExecutionStatus

## 语法

`getSlaveReplicationExecutionStatus()`

## 详情

由管理员在从集群的数据节点调用，获取该节点上每个线程执行队列的状态。

## 返回值

返回一个表对象，包含以下字段：

* executionSet：任务所属的执行集 ID。
* worker：线程 ID。
* taskId：异步复制任务 ID。
* state：任务的状态。可能的取值有 TRANSMITTED（数据传输完成等待执行），EXECUTING（正在执行）。

## 例子

```
getSlaveReplicationExecutionStatus()
```

| executionSet | worker | taskId | state |
| --- | --- | --- | --- |
| 0 | 3 | 25 | EXECUTING |
