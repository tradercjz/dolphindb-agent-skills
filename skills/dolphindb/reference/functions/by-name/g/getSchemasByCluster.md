# getSchemasByCluster

首发版本：3.00.3

## 语法

`getSchemasByCluster(clusterName, catalogName)`

## 详情

查询集群下指定 catalog 的所有的 schema。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

## 参数

**clusterName** 字符串标量，表示要查询的集群名称。

**catalogName** 字符串标量，表示要查询的 catalog 的名称。

## 返回值

一个表，包含以下字段：

* schema：字符串类型，schema 的名称。
* dbUrl：字符串类型，数据库路径。

## 例子

```
// MoMSender 的数据节点：
database(directory="dfs://db1", partitionType=RANGE, partitionScheme=0 5 10)
database(directory="dfs://db2", partitionType=RANGE, partitionScheme=0 5 10)
createSchema("catalog1", "dfs://db1", "schema1")
createSchema("catalog1", "dfs://db2", "schema2")

// MOM 节点：
getSchemasByCluster("MoMSender", "catalog1")
```

| schema | dbUrl |
| --- | --- |
| schema1 | dfs://db1 |
| schema2 | dfs://db2 |
