# isCheckpointingHaMvcc

首发版本：3.00.5

## 语法

`isCheckpointingHaMvcc(groupId)`

## 详情

检查指定 MVCC Raft 组当前是否正在执行 checkpoint。

## 参数

**groupId** 是一个整数，表示 MVCC Raft 组 ID。

## 返回值

BOOL 类型标量。

## 例子

```
isCheckpointingHaMvcc(5)
// output:false
```

**相关函数**：haMvccTable
