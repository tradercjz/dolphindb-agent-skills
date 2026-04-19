# getGroupListOfAllClusters

首发版本：3.00.3

## 语法

`getGroupListOfAllClusters()`

## 详情

查询多集群系统中所有集群的用户组信息。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

## 参数

无

## 返回值

返回一个字典，其中：

* key：集群名称。
* value：用户组名称列表。

## 例子

```
getGroupListOfAllClusters()

/* Output:
masterOfMaster->["group1"]
MoMSender->["group2"]
*/
```
