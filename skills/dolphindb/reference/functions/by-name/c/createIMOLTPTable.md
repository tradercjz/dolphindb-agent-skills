# createIMOLTPTable

## 语法

`createIMOLTPTable(dbHandle, table, tableName, primaryKey, [secondaryKey],
[uniqueFlag])`

## 详情

在 IMOLTP 数据库中创建 IMOLTP 表。

## 参数

**dbHandle** 函数 database 返回的 IMOLTP
数据库句柄。

**table** 一个表，系统将根据该表的结构在数据库中创建一个空的 IMOLTP 表。

**tableName** 字符串标量，表示 IMOLTP 表的名字。

**primaryKey**字符串标量或向量，表示主键索引的键包含的字段（字段即为列名）。为标量时，表示只包含一个字段；为向量时，表示包含多个字段。

**secondaryKey** 可选参数，字符串标量或向量，表示每一个二级索引的键包含的字段。

**uniqueFlag** 可选参数，布尔类型标量或向量，表示每一个二级索引是否是唯一的：

* uniqueFlag 为标量或 size 为 1 的向量，表示只有一个二级索引。此时 secondaryKey
  可以为字符串标量（表示一个字段）或向量（表示多个字段）。
* uniqueFlag 为长度大于 1 的向量，表示有多个二级索引。此时 secondaryKey 的长度必须与 uniqueFlag
  相同，secondaryKey 的每一个元素表示一个键。

## 返回值

一个表。

## 例子

创建 IMOLTP 数据库

```
dbName = "oltp://test_imoltp"
db = database(directory=dbName, partitionType=VALUE, partitionScheme=1..100, engine="IMOLTP")
```

创建表 test\_table\_1，以 id 为主键，没有二级索引

```
pt1 = createIMOLTPTable(
    dbHandle=db,
    table=table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    tableName="test_table_1",
    primaryKey=`id
)
```

创建表 test\_table\_2，以 id，sym 为主键，val2，sym 作为 unique 二级索引

```
pt2 = createIMOLTPTable(
    dbHandle=db,
    table=table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    tableName="test_table_2",
    primaryKey=`id`sym,
    secondaryKey=`val2`sym,
    uniqueFlag=true
)
```

创建表 test\_table\_3，以 id 为主键，有一个非 unique 二级索引：以 val1 为键；一个 unique 二级索引：以 sym 为键

```
pt3 = createIMOLTPTable(
    dbHandle=db,
    table=table(1:0, ["id", "val1", "val2", "sym"], [LONG, INT, LONG, STRING]),
    tableName="test_table_3",
    primaryKey=`id,
    secondaryKey=[`val1, `sym],
    uniqueFlag=[false, true]
)
```
