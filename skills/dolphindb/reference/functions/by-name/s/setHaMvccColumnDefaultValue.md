# setHaMvccColumnDefaultValue

## 语法

`setHaMvccColumnDefaultValue(table, colName,
defaultValue)`

## 详情

设置高可用 MVCC 表指定列的默认值。

此函数必须在该表所属 Raft 组的 Leader 节点上执行。

## 参数

**table** 高可用 MVCC 表对象，表示要修改的表。

**colName** 可以是字符串标量或向量，表示要设置默认值的列名。

**defaultValue** 标量或元组，表示列默认值。若 *colName* 为向量，则 *defaultValue*
必须为与其等长的元组。

## 例子

```
//创建高可用 MVCC 表
schemaTb = table(1:0, `name`id`value, [STRING, INT, DOUBLE])
hmvcct = haMvccTable(1:0, schemaTb, "demoHaMvcc", 5)

//设置 name 列的默认值为 A001
setHaMvccColumnDefaultValue(hmvcct, "name", "A001")
//设置 id 列的默认值为 1，value 列的默认值为 3.6
setHaMvccColumnDefaultValue(hmvcct, ["id","value"], (1, 3.6))
```

**相关函数**：haMvccTable
