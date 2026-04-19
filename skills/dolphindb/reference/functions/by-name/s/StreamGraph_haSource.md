# StreamGraph::haSource

首发版本：3.00.3

## 语法

`StreamGraph::haSource(name, colNames, colTypes, raftGroup, cacheLimit,
[retentionMinutes=1440])`

## 详情

创建一个高可用流数据表。参考 haStreamTable。

## 参数

**name** 表示流表的名称。字符串标量，可以传入完整的流表全限定名（如
"trading.orca\_table.trades"）；也可以仅提供流表名（如 "trades"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**colNames** 是一个向量，表示列名。

**colTypes**
是一个向量，表示每列的数据类型，支持数组向量类型和元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

**raftGroup** 是一个大于1的整数，或者字符串。

* 当为整数时，表示 Raft 组的 ID。
* 当为字符串时，表示 Raft 组的别名（需事先通过 *streamingRaftGroupAliases* 配置 ）。

**cacheSize** 是一个正整数，用于指定高可用流数据表在内存中最多保留多少行。如果 *cacheSize*
是小于1000的正整数，它会被自动调整为1000。

**retentionMinutes** 可选参数，整数，用于指定保留大小超过 1GB 的 log
文件的时间（从文件的最后修改时间开始计算），单位是分钟。默认值是1440，即一天。

## 返回值

一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

g = createStreamGraph("indicators")
g.haSource("ha_table", `time`symbol`price`volume, [DATETIME,SYMBOL,DOUBLE,LONG], 3, 50000)
```
