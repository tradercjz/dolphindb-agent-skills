# getTableAccess

## 语法

`getTableAccess(dbUrl, table)`

## 详情

查看哪些用户和组具有与分布式数据表 *dbUrl/table* 相关（包括 ALLOW 和 DENY 权限状态）的权限。

该函数仅限 admin 和对数据库 *dbUrl* 具有 DB\_OWNER 或 DB\_MANAGE 权限的用户调用。

## 参数

**dbUrl** 字符串标量，表示分布式数据库的地址。

**table** 字符串标量，表示分布式表的表名。

## 返回值

返回一个表：

* name 具有相关权限的对象的名称。
* type 该对象的类型，可选值为 user 和 group，分别对应用户和组。
* TABLE\_READ, TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE 分别指代对应权限，权限状态包括 ALLOW,
  DENY, NONE。关于用户权限的更多信息可参考用户权限管理。

## 例子

具有 DB\_OWNER 权限的用户 user1 创建了分布式表 `dfs://testDB/pt`，并为用户 user2 授予
TABLE\_READ 权限，禁止用户 user3 的 TABLE\_INSERT 权限，为组 group1 授予 TABLE\_DELETE 权限。此时，用户 user1
可通过 `getTableAccess` 函数查看哪些用户具有 "dfs://testDB/pt" 相关的权限。

```
login(`user1, `123456)
getTableAccess("dfs://testDB", "pt")
```

| name | type | TABLE\_READ | TABLE\_INSERT | TABLE\_UPDATE | TABLE\_DELETE |
| --- | --- | --- | --- | --- | --- |
| group1 | group | NONE | NONE | NONE | ALLOW |
| user3 | user | NONE | DENY | NONE | NONE |
| user2 | user | ALLOW | NONE | NONE | NONE |
| admin | user | ALLOW | ALLOW | ALLOW | ALLOW |

**相关信息**

* [getDBAccess](getDBAccess.html "getDBAccess")
