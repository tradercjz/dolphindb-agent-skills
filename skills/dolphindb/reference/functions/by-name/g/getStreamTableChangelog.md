# getStreamTableChangelog

首发版本：3.00.5

## 语法

`getStreamTableChangelog(streamTable)`

## 详情

返回带状态标识的流表。

## 参数

**streamTable** 是流数据表。

## 返回值

一个表。

## 例子

```
getStreamTableChangelog(tickStream)
```

|  | changelog\_type | sym | time | price |
| --- | --- | --- | --- | --- |
| 0 | N | 000001.SH | 2021.02.08 09:30:01 | 14.666441912917989 |
| 1 | N | 000001.SH | 2021.02.08 09:30:02 | 105.60469803298001 |
| 2 | U | 000001.SH | 2021.02.08 09:30:01 | 89.723076797026 |
| 3 | U | 000001.SH | 2021.02.08 09:30:02 | 69.34098429496888 |

**相关函数**：changelogStreamTable
