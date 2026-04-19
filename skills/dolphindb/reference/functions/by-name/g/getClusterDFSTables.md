# getClusterDFSTables

## 语法

`getClusterDFSTables([includeSysTable=true])`

## 详情

返回集群中的分布式表。

2.00.9 版本起，

* 管理员可以返回当前集群中任一分布式表；
* 其他用户执行时仅返回：

  （1）拥有 DB\_OWNER, DB\_MANAGE, DB\_READ, DB\_WRITE, DB\_INSERT, DB\_UPDATE, DB\_DELETE
  权限的数据库所对应的分布式表；

  （2）拥有 TABLE\_READ, TABLE\_WRITE, TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE
  权限的分布式表。

2.00.10.2 版本起，该函数由拥有 DBOBJ\_CREATE 权限的用户执行时，还会返回其创建的分布式表。

## 参数

**includeSysTable** 可选参数，布尔值，用于控制返回的结果中是否包含系统表，默认值为
true。该参数仅对管理员用户生效。如果是普通用户，即便将 *includeSysTable* 设置为 true 也无法查看系统表。

## 返回值

字符串向量。

## 例子

```
getClusterDFSTables()
```

返回：["dfs://demohash/pt","dfs://myDataYesDB/tick","dfs://testDB/pt1","dfs://testDB/pt2"]
