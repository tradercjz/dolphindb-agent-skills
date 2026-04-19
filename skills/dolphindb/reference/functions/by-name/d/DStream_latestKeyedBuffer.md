# Dstream::latestKeyedBuffer

首发版本：3.00.3

## 语法

`DStream::latestKeyedBuffer(name, keyColumn, timeColumn, [asyncWrite=true],
[compress=true], [cacheSize], [retentionMinutes=1440], [flushMode=0],
[preCache], [cachePurgeTimeColumn], [cachePurgeInterval],
[cacheRetentionTime])`

## 详情

创建一个最新值键值流数据表，用于存储流计算中间结果。参考 latestKeyedStreamTable。

## 参数

**name** 表示流表的名称。字符串标量，可以传入完整的流表全限定名（如
"trading.orca\_table.trades"）；也可以仅提供流表名（如 "trades"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**keyColumn** 是一个字符串或向量，表示主键。主键的数据类型必须属于以下类别：INTEGRAL,
TEMPORAL, LITERAL 或 FLOATING。

**timeColumn** 字符串标量或长度为 2 的向量，分别用于指定 1 个或 2 个时间列。当仅指定 1 个时间列时，该列可以为整型或时间类型；当指定 2
个时间列时，第 1 列必须是 DATE 类型，第 2 列则是 TIME, SECOND 或 NANOTIME 类型。通过这两列，可以共同确定唯一的时间值。

**asyncWrite** 可选参数，是一个布尔值，表示是否异步持久化数据到磁盘。默认值为
true，流数据写入内存即为写入成功，持久化到磁盘的操作将会由另一个线程执行。

注：

持久化数据到磁盘包含两个步骤：

* 写内存数据到操作系统缓存
* 写缓存数据到磁盘（是否开启同步刷盘由参数 *flushMode* 决定）

**compress** 可选参数，是一个布尔值，表示是否以压缩模式模式保存至磁盘。默认值为 true。

**cacheSize** 可选参数，整数，表示流数据表在内存中最多保留多少行。如果未指定该参数，则所有记录行都会保存在内存中。如果
*cacheSize* 小于 1000，它会被自动调整为 1000。

**retentionMinutes** 可选参数，是一个整数，表示文件大小超过 1GB的 log
文件的保留时间(从文件的最后修改时间开始计算)，单位是分钟。默认值是 1440，即一天。如果 log 文件未达 1GB，则会一直保留至大小达到 1GB。

**flushMode** 可选参数，是一个整数，表示是否开启同步刷盘，取值只能为 0 或 1。默认值是
0，表示异步刷盘，内存中的流数据写入操作系统缓存即为写入成功，并进行下一批数据的写入。 若为
1，则表示同步刷盘，当前批次的流数据必须落盘完成，才会进行下一批数据的写入。

**preCache** 可选参数，是一个整数，表示从磁盘加载到内存的记录条数。如果没有指定该参数，重启后实际加载到内存的数据量受
*cacheSize* 限制。

**cachePurgeTimeColumn** 可选参数，字符串标量，需要指定为持久化流表中的时间列名称。

**cachePurgeInterval** 可选参数，DURATION 类型标量，表示触发清理内存中数据的时间间隔。

**cacheRetentionTime** 可选参数，DURATION 类型标量，表示内存中数据的最长保留期限。

## 返回值

返回一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

g = createStreamGraph("indicators")

g.source("trade", `time`symbol`price`volume, [DATETIME,SYMBOL,DOUBLE,LONG])
    .timeSeriesEngine(windowSize=60, step=60, metrics=[<first(price) as open>, <max(price) as high>, <min(price) as low>, <last(price) as close>, <sum(volume) as volume>], timeColumn=`time, keyColumn=`symbol)
    .latestKeyedBuffer(name="bufferTable", keyColumn="symbol", timeColumn=`time)
```
