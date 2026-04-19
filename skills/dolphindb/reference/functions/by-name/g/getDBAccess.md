# getDBAccess

## 语法

`getDBAccess(dbUrl)`

## 详情

查看哪些用户和组具有与数据库 *dbUrl* 相关（包括 ALLOW 和 DENY 权限状态）的权限。

该函数仅限 admin 和对数据库 *dbUrl* 具有 DB\_OWNER 或 DB\_MANAGE 权限的用户调用。

## 参数

**dbUrl** 字符串标量，表示分布式数据库的地址。

## 返回值

返回一个表：

* name 具有相关权限的对象的名称。
* type 该对象的类型，可选值为 user 和 group，分别对应用户和组。
* DB\_READ, DB\_INSERT, DB\_UPDATE, DB\_DELETE, DBOBJ\_CREATE, DBOBJ\_DELETE, DB\_MANAGE
  分别指代对应权限，权限状态包括 ALLOW, DENY, NONE。关于用户权限的更多信息可参考用户权限管理。

## 例子

用户 user1 具有 DB\_OWNER 权限，创建了数据库 `dfs://testDB`，并为用户 user2 授予 DB\_READ
权限，禁止用户 user3 的 DB\_INSERT 权限，为组 group1 授予 DBOBJ\_CREATE 权限。此时，用户 user1 可通过
`getDBAccess` 函数查看哪些用户具有 "dfs://testDB" 相关的权限。

```
login(`user1, `123456)
getDBAccess("dfs://testDB")
```

| name | type | DB\_READ | DB\_INSERT | DB\_UPDATE | DB\_DELETE | DBOBJ\_CREATE | DBOBJ\_DELETE | DB\_MANAGE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| group1 | group | NONE | NONE | NONE | NONE | ALLOW | NONE | NONE |
| user3 | user | NONE | DENY | NONE | NONE | NONE | NONE | NONE |
| user2 | user | ALLOW | NONE | NONE | NONE | NONE | NONE | NONE |
| admin | user | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW | ALLOW |

**相关信息**

* [getTableAccess](gettableaccess.html "getTableAccess")
