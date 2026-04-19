# DStream::haKeyedSink

首发版本：3.00.3

## 语法

`DStream::haKeyedSink(name, keyColumn, raftGroup, cacheLimit,
[retentionMinutes=1440])`

## 详情

将流数据输出到高可用键值流数据表。

有关最新高可用流数据表的更多信息，请参阅 haStreamTable
手册。

## 参数

**name** 字符串，指定目标表名。

**keyColumn** 字符串标量或向量，指定主键列。

**raftGroup** 是一个大于1的整数，或者字符串。

* 当为整数时，表示 Raft 组的 ID。
* 当为字符串时，表示 Raft 组的别名（需事先通过 *streamingRaftGroupAliases* 配置 ）。

**cacheSize** 是一个正整数，用于指定高可用流数据表在内存中最多保留多少行。如果 *cacheSize*
是小于1000的正整数，它会被自动调整为1000。

**retentionMinutes** 可选参数，整数，用于指定保留大小超过 1GB 的 log
文件的时间（从文件的最后修改时间开始计算），单位是分钟。默认值是1440，即一天。

## 返回值

DStream 对象。
