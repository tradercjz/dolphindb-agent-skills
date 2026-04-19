# listTables

## 语法

`listTables(dbUrl)`

## 详情

返回一个表对象，包含两列，分别为数据库中的表名和物理索引名。

注：

只有表级分区具有物理索引。

## 参数

**dbUrl** 是一个字符串，表示分布式数据库的路径。

## 例子

```
listTables(dbPath)
```

| tableName | physicalIndex |
| --- | --- |
| pt1 | 1By |
| pt | 1Bw |
