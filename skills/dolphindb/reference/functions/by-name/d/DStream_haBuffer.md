# Dstream::haBuffer

首发版本：3.00.3

## 语法

`DStream::haBuffer(name, raftGroup, cacheLimit,
[retentionMinutes=1440])`

## 详情

创建一个高可用流数据表，用于存储流计算中间结果。参考 haStreamTable。

## 参数

**name** 表示流表的名称。字符串标量，可以传入完整的流表全限定名（如
"trading.orca\_table.trades"）；也可以仅提供流表名（如 "trades"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

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
login(`admin,`123456)

if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

g = createStreamGraph("indicators")

g.source("trade", `time`symbol`price`volume, [DATETIME,SYMBOL,DOUBLE,LONG])
    .timeSeriesEngine(windowSize=60, step=60, metrics=[<first(price) as open>, <max(price) as high>, <min(price) as low>, <last(price) as close>, <sum(volume) as volume>], timeColumn=`time, keyColumn=`symbol)
    .haBuffer(name="ha_Table", raftGroup=3, cacheLimit=5)
```
