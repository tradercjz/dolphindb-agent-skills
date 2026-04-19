# getPKEYCompactionTaskStatus

## 语法

`getPKEYCompactionTaskStatus([count])`

## 详情

查询 PKEY 引擎 level file 合并操作任务的状态。该函数只能在数据节点调用。

## 参数

**count** 可选参数，非负整数。设置后，将返回配置项 volumes 中的每一个 volume 的最近的
*count* 个已结束的合并任务的记录（包括成功和失败），以及所有正在执行或尚未开始的任务的记录。默认值为
0，表示返回所有合并任务的状态信息。

## 返回值

返回一个表，包含以下几列：

| 列名 | 含义 |
| --- | --- |
| volume | 发生合并的文件所在的磁盘卷路径。由配置项 *volumes* 进行配置。 |
| level | STRING 类型，当前合并的 level file 层级。一次合并最多涉及两个层级。如果此列为空，说明该合并任务尚未开始、正在执行，或执行失败。 |
| chunkId | 发生合并操作的 chunk 的 ID。 |
| tableName | 发生合并操作的数据表的物理表名。 |
| files | 参与当前合并任务的 level file。如果此列为空，说明该合并任务尚未开始、正在执行，或执行失败。 |
| force | 是否由 `triggerPKEYCompaction` 强制触发。 |
| receivedTime | 当前合并任务进入任务队列的时间戳。 |
| startTime | 当前合并任务开始执行的时间戳。 |
| endTime | 当前合并任务执行结束的时间戳。 |
| errorMessage | 报错信息。如果失败，则显示失败的原因；否则显示空。 |

## 例子

```
getPKEYCompactionTaskStatus()
```

| volume | level | chunkId | tableName | files | force | receivedTime | startTime | endTime | errorMessage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| /home/dolphindb/server/local8848/storage | 2 | ac872f06-abed-339c-8642-ce7dcf415691 | pt1\_2 | 2-000000046-002 | true | 2024.09.24 13:52:37.746 | 2024.09.24 13:52:37.746 | 2024.09.24 13:52:37.816 |  |
| /home/dolphindb/server/local8848/storage | 1 | ac872f06-abed-339c-8642-ce7dcf415691 | pt1\_2 | 1-000000046-001 | true | 2024.09.24 13:52:32.431 | 2024.09.24 13:52:32.431 | 2024.09.24 13:52:32.437 |  |
| /home/dolphindb/server/local8848/storage | 0 | ac872f06-abed-339c-8642-ce7dcf415691 | pt1\_2 | 0-000000046-000 | true | 2024.09.24 11:58:42.006 | 2024.09.24 11:58:42.006 | 2024.09.24 11:58:42.011 |  |
| /home/dolphindb/server/local8848/storage | 0 | 62ab7ebb-03f2-10a5-5445-c537512aee06 | pt1\_2 | 0-000000045-000 | true | 2024.09.24 11:57:13.596 | 2024.09.24 11:57:13.596 | 2024.09.24 11:57:13.601 |  |
