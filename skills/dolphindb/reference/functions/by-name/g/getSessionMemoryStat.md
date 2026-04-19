# getSessionMemoryStat

## 语法

`getSessionMemoryStat()`

## 详情

获取当前节点所有连接会话的内存占用状态。

缓存类型说明:

| 缓存类型 | 含义 |
| --- | --- |
| \_\_DimensionalTable\_\_ | 维度表缓存，单位为字节。 |
| \_\_SharedTable\_\_ | 共享表缓存，单位为字节。 |
| \_\_OLAPTablet\_\_ | OLAP 引擎数据库表的缓存，单位为字节。 |
| \_\_OLAPCacheEngine \_\_ | OLAP 引擎 Cache Engine 的内存占用，单位为字节。 |
| \_\_OLAPCachedSymbolBase\_\_ | OLAP 引擎 SYMBOL 类型字典编码的缓存，单位为字节。 |
| \_\_DFSMetadata\_\_ | 分布式存储的元数据内存占用情况，单位为字节。 |
| \_\_TSDBCacheEngine\_\_ | TSDB 引擎 Cache Engine 的内存占用，单位为字节。 |
| \_\_TSDBLevelFileIndex\_\_ | TSDB 引擎 level file 索引的缓存，单位为字节。 |
| \_\_TSDBCachedSymbolBase\_\_ | TSDB 引擎 SYMBOL 类型字典编码的缓存，单位为字节。 |
| \_\_PKEYCachedSymbolBase\_\_ | PKEY 引擎 SYMBOL 类型字典编码的缓存，单位为字节。 |
| \_\_PKEYCacheEngine\_\_ | PKEY 引擎 Cache Engine 的内存占用，单位为字节。 |
| \_\_StreamingPubQueue\_\_ | 流数据发布队列里未处理的消息数。 |
| \_\_StreamingSubQueue\_\_ | 流数据订阅队列里未处理的消息数。 |
| \_\_IOTDBStaticTableCache\_\_ | 静态表缓存，单位为字节。 |
| \_\_IOTDBLatestKeyCache\_\_ | 最新值表缓存，单位为字节。 |

注：

* 此函数无法统计到会话中正在执行的任务所占用的内存情况。
* 对于返回表中的 createTime 和 lastActiveTime，2.00.9.4 之前版本的 DolphinDB，返回零时区时间；2.00.9.4 及之后版本的 DolphinDB，返回当前时区的时间。

## 返回值

返回一张表包含以下字段：

* userId：用户 ID 或缓存类型的标识符（形如：\_\_xxx\_\_）。
* sessionId：会话 ID。
* memSize：会话所占用的内存，单位为字节。
* remoteIP：发起会话的客户端的 IP。
* remotePort：发起会话的客户端的端口号。
* createTime：会话创建的时间，为 TIMESTAMP 类型。
* lastActiveTime：会话最近一次执行脚本的时间戳。

## 例子

```
t = getSessionMemoryStat();
t;
```

| userId | sessionId | memSize | remoteIP | remotePort | createTime | lastActiveTime |
| --- | --- | --- | --- | --- | --- | --- |
| \_\_DimensionalTable\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_SharedTable\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_OLAPTablet\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_OLAPCacheEngine\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_OLAPCachedSymbolBa... |  | 0 | 0.0.0.0 |  |  |  |
| \_\_DFSMetadata\_\_ |  | 2769 | 0.0.0.0 |  |  |  |
| \_\_TSDBCacheEngine\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_TSDBLevelFileIndex\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_TSDBCachedSymbolBa... |  | 0 | 0.0.0.0 |  |  |  |
| \_\_PKEYCachedSymbolBase\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_PKEYCacheEngine\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_StreamingPubQueue\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| \_\_StreamingSubQueue\_\_ |  | 0 | 0.0.0.0 |  |  |  |
| admin | 2882591513 | 1416 | 60.176.105.0 | 20861 | 2023.02.15T02:15:22.384 | 2023.02.15T02:24:16.307 |
