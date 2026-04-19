# closeSessions

## 语法

`closeSessions(sessionId)`

## 详情

关闭一个或多个 session。

## 参数

**sessionId** 是一个 LONG 类型的标量或向量，表示一个或多个 session ID。

## 返回值

无。

## 例子

```
getSessionMemoryStat();
```

| userId | sessionId | memSize | remoteIP | remotePort | createTime | lastActiveTime |
| --- | --- | --- | --- | --- | --- | --- |
| \_DimensionalTable\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_SharedTable\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_OLAPTablet\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_OLAPCacheEngine\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_OLAPCachedSymbolBase\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_DFSMetadata\_ | 13,571 | 0.0.0.0 |  |  |  |  |
| \_TSDBCacheEngine\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_TSDBLevelFileIndex\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_TSDBCachedSymbolBase\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_StreamingPubQueue\_ | 0 | 0.0.0.0 |  |  |  |  |
| \_StreamingSubQueue\_ | 0 | 0.0.0.0 |  |  |  |  |
| guest | 1,769,725,800 | 16 | 36.27.51.13 | 63,133 | 1970.01.01T00:00:00.000 | 2023.08.31T22:35:27.385 |
| admin | 2,882,591,513 | 6,449 | 36.27.51.13 | 60,812 | 1970.01.01T00:00:00.000 | 2023.08.31T22:18:27.562 |

```
closeSessions(getSessionMemoryStat().sessionId[11]);
```
