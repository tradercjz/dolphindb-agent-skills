# getMasterReplicationStatus

## 语法

`getMasterReplicationStatus([limit=-1])`

## 详情

获取主集群的异步复制状态。已完成的任务排列在前面，未完成的任务排列在后面。

* 如果未指定 *limit*，则返回的任务数量不受限制。
* 如果指定 *limit*，则返回最多 *limit* 个任务列表。

其中，已完成的任务最多显示最近的1万条记录；而未完成的任务只显示从最早时间开始，直到满足指定条数的记录。

该函数只能由管理员在主集群的控制节点调用。

## 参数

**limit** 一个整数，表示结果中最多可返回的任务数量。

## 返回值

返回一个表，包含以下字段：

* taskId：异步复制任务 id。
* tid：事务 id。
* groupId：异步复制任务所属的组 id。
* operationType：任务类型，参照异步复制支持性表。
* submitTime：任务提交的时间，类型为 NANOTIMESTAMP。
* dbName：任务对应的数据库的路径。
* tableName：任务对应的表名。
* srcIP：存储写任务数据的数据节点 ip。
* srcPort：存储写任务数据的数据节点 port。
* isTruncated：该任务是否已经完成并从发送队列回收。

## 例子

```
getMasterReplicationStatus();
```

输出返回：

| taskId | tid | groupId | operationType | submitTime | dbName | tableName | srcIP | srcPort | isTruncated |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | CREATE\_DB | 2022.11.08T10:50:35.442141722 | db://test\_dropPartition\_value |  | 127.0.0.1 | 8002 | true |
| 2 | 2 | 2 | CREATE\_PARTITIONED\_TABLE | 2022.11.08T10:50:35.447716190 | db://test\_dropPartition\_value | pt | 127.0.0.1 | 8002 | true |
| 3 | 3 | 3 | APPEND | 2022.11.08T10:50:35.584920262 | db://test\_dropPartition\_value | pt | 127.0.0.1 | 8002 | true |
| 4 | 4 | 4 | DROP\_PARTITION | 2022.11.08T10:50:35.632575800 |  | pt | 127.0.0.1 | 8002 | false |

相关函数：getSlaveReplicationStatus
