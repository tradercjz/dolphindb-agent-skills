# triggerPKEYCompaction

## 语法

`triggerPKEYCompaction(chunkId, [async=true])`

## 详情

异步强制触发指定 chunk 进行 compaction，从而提升读取效率。

## 参数

**chunkId** STRING 类型标量或向量，表示 chunk 对应的 ID。

**async** BOOL 类型标量，表示是否异步触发：

* 默认为 true，表示异步触发，即不等待 compaction 任务完成直接返回；
* false 表示同步触发，即等待所有 compaction 任务完成后返回。

## 返回值

无。

## 例子

```
triggerPKEYCompaction(chunkId="1486f935-6f87-479c-b341-34c6a303d4f9", async=false)
```
