# setHaMvccColumnNullability

## 语法

`setHaMvccColumnNullability(table, colName,
allowNull)`

## 详情

设置高可用 MVCC 表的部分列是否允许为 NULL。

此函数必须在该表所属 Raft 组的 Leader 节点上执行。

## 参数

**table** 高可用 MVCC 表对象，表示要修改的表。

**colName** 字符串标量或向量，表示要设置的列名（单列或多列）。

**allowNull** 布尔标量或向量，表示是否允许为 NULL，true 代表允许为 NULL。若为向量，其长度必须与 *colName*
一致。

## 例子

```
//创建高可用 MVCC 表
schemaTb = table(1:0, `name`id`value, [STRING, INT, DOUBLE])
hmvcct = haMvccTable(1:0, schemaTb, "demoHaMvcc", 5)

//不允许 name 为空值
setHaMvccColumnNullability(hmvcct, "name", false)
//设置 id 不允许为 NULL, value 可以为 NULL
setHaMvccColumnNullability(hmvcct, ["id","value"], [true,false])
```

**相关函数**：haMvccTable
