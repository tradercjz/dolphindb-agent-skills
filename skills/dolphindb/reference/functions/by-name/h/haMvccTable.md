# haMvccTable

首发版本：3.00.5

## 语法

`haMvccTable(capacity:size, table, tableName, raftGroup,
[defaultValues], [allowNull])`

## 详情

创建一个高可用多版本并发控制的表（MVCC 表）。

注：

高可用 MVCC 表的创建、删除及写入操作必须在该 Raft 组的 Leader 节点上执行。Raft 组的 Leader 节点可通过函数
`getHaMvccLeader` 获取。

## 参数

**capacity** 是正整数，表示表的容量，即建表时系统为该表分配的内存（以记录数为单位）。当记录数超过 *capacity*
时，系统会自动扩充容量。系统首先会分配当前容量1.2~2倍的内存，然后复制数据到新的内存空间，最后释放原来的内存。对于规模较大的表，扩容时的内存占用会很高。因此，建议创建内存表时预先分配一个合理的容量。

**size** 是正整数，表示该表新建时的行数。若 *size*=0，创建一个空表；若 *size*>0，则新建表中记录的初始值由
*defaultValues* 决定。

**table** 是一个表对象，高可用 MVCC 表的结构与其一致，它必须是用 `table` 函数创建的空表。

**tableName** 字符串标量，表示高可用 MVCC 表的名字。

**raftGroup** 是一个大于 1 的整数，表示高可用 MVCC 表使用的 Raft 组 ID。该 ID 必须预先在配置项
`mvccTableRaftGroups` 中配置。

**defaultValues** 可选参数，是与表列数等长的元组，表示建表时各列的默认值。默认不指定，此时各列的默认值为 NULL。

**allowNull** 可选参数，是与表列数等长的布尔向量，表示各列是否允许包含空值。默认值为 true，表示全部列允许包含空值。

## 返回值

返回高可用 MVCC 表的句柄。

## 例子

```
schemaTb = table(1:0, `name`id`value, [STRING, INT, DOUBLE])
hmvcct = haMvccTable(1:0, schemaTb, "demoHaMvcc", 2)
```

**相关函数**：loadHaMvccTable, dropHaMvccTable, setHaMvccColumnNullability,
setHaMvccColumnDefaultValue, getHaMvccRaftGroups, getHaMvccLeader, getHaMvccTableInfo, checkpointHaMvcc, isCheckpointingHaMvcc
