# dropHaMvccTable

首发版本：3.00.5

## 语法

`dropHaMvccTable(tableName)`

## 详情

删除指定名称的高可用 MVCC 表。

此函数必须在该表所属 Raft 组的 Leader 节点上执行。

## 参数

**tableName** 字符串标量，表示要删除的高可用 MVCC 表的名称。

## 例子

```
dropHaMvccTable("demoHaMvcc")
```

**相关函数**：haMvccTable, loadHaMvccTable
