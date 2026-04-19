# cancelPKEYCompactionTask

## 语法

`cancelPKEYCompactionTask(chunkId)`

## 详情

取消目标分区正在执行的 compaction 任务。

## 参数

**chunkId** STRING 类型标量，表示 chunk 对应的 ID。

## 返回值

无。

## 例子

```
triggerPKEYCompaction(chunkId="1486f935-6f87-479c-b341-34c6a303d4f9", async=false)
```
