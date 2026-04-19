# syntax

## 语法

`syntax(X)`

## 详情

返回 *X* 表示的函数或命令的语法。

## 参数

**X** 是 DolphinDB 函数或命令。

## 返回值

STRING 类型标量。

## 例子

```
syntax(createPartitionedTable);
// output
createPartitionedTable(dbHandle, table, tableName, [partitionColumns], [compressMethods])
```
