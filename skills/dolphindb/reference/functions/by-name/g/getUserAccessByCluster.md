# getUserAccessByCluster

首发版本：3.00.3

## 语法

`getUserAccessByCluster(users, cluster, finalAccess)`

## 详情

查询指定用户在多集群系统中的权限信息。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

## 参数

**users** 字符串向量，表示要查询的用户名称。

**cluster** 字符串标量，表示要查询的用户所在集群的名称。

**finalAccess** 布尔标量，表示是否获取用户及其所属组权限叠加的结果。

## 返回值

一个表，字段与 `getUserAccess` 函数的返回结果一致。

## 例子

```
getUserAccessByCluster(["admin"], "masterOfMaster", true)
```

| userId | groups | isAdmin | ACCESS\_READ | ACCESS\_INSERT | ACCESS\_UPDATE | ACCESS\_DELETE | VIEW\_EXEC | SCRIPT\_EXEC | TEST\_EXEC | DBOBJ\_CREATE | ... |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| admin |  | 1 | allow | allow | allow | allow | allow | allow | allow | allow | ... |

相关函数：getUserAccess
