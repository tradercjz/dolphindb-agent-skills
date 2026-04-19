# setRaftElectionTick

## 语法

`setRaftElectionTick(groupId, tickCount)`

## 详情

通过该命令可以动态实现配置项 *raftElectionTick* 的功能。 由 *tickCount*
确定一个时间区间：[*tickCount*, 2 \* *tickCount*]。在指定的 raft 组内， follower
在该区间内的一个随机时刻之后仍然没有收到 leader 的心跳，则会发出竞选 leader 的请求。

注：

1. 必须由管理员在 raft 组内的所有控制节点上执行该命令，保证它们的
   *raftElectionTick* 设置值相同。
2. 该命令不会修改配置文件，重启后会恢复成默认配置或 *raftElectionTick*
   指定的配置。

相关函数： getRaftElectionTick, getControllerElectionTick

## 参数

**groupId** 是一个正整数，表示 raft 组的 ID，目前只能是1，表示控制节点组成的 raft 组 ID。

**tickCount** 是一个不小于800的整数，单位为10ms。
