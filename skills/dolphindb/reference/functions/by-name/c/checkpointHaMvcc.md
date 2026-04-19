# checkpointHaMvcc

首发版本：3.00.5

## 语法

`checkpointHaMvcc(groupId)`

## 详情

手动触发指定 MVCC Raft 组的 checkpoint。

## 参数

**groupId** 是一个整数，表示 MVCC Raft 组 ID。

## 例子

```
checkpointHaMvcc(5)
```

**相关函数**：haMvccTable
