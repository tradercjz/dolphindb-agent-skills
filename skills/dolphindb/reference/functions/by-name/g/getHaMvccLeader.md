# getHaMvccLeader

首发版本：3.00.5

## 语法

`getHaMvccLeader(groupId)`

## 详情

获取指定 MVCC Raft 组的 Leader 节点别名。

## 参数

**groupId** 是一个整数，表示 MVCC Raft 组 ID。

## 返回值

STRING 类型标量。

## 例子

```
getHaMvccLeader(5)
// output
"dnode1"
```

**相关函数**：haMvccTable
