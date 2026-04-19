# getDiskIOStat

## 语法

`getDiskIOStat()`

## 详情

获取磁盘 I/O 统计信息。

## 参数

无

## 返回值

返回包含两个键值对的字典：

* diskIOQueueDepths 是一个向量，表示每个 IO 队列的深度。在同一个 DolphinDB
  实例中的所有 IO 任务都属于同一个 IO 队列。
* diskIOConcurrencyLevel 是一个整数，表示 IO 队列的数量。

## 例子

```
getDiskIOStat()

// output
diskIOQueueDepths->[0]
diskIOConcurrnecyLevel->1
```
