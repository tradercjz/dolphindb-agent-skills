# getRaftLearnersStatus

## 语法

`getRaftLearnersStatus(groupId)`

## 详情

查询指定 Raft 组中所有 Learner 节点的状态。

## 参数

**groupId** 是一个大于 1 的整数，表示 Raft 组的 ID。

## 返回值

一个表，包含以下列：

* nodeName：节点名字。
* nodeId：节点的 ID。
* matchIndex：Leader 已确认复制到该 Learner 的最高日志索引。
* nextIndex：Leader 下一次要发送给该 Learner 的日志条目索引。
* replicationLag：​日志复制延迟条数，值越小表示延迟越低。
* lastActiveTime：Leader 与 Learner 之间最近一次成功通信的时间。
* snapshotProgress：快照传输进度，0表示当前没有进行快照传输。

## 例子

```
getRaftLearnersStatus(3)
```

| nodeName | nodeId | matchIndex | nextIndex | replicationLag | lastActiveTime | snapshotProgress |
| --- | --- | --- | --- | --- | --- | --- |
| datanode8922@cluster2 | 256 | 10,004 | 10,005 | 0 | 2025.08.18 14:00:15.349 | 0 |
