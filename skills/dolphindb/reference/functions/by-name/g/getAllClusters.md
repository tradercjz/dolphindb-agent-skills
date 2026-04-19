# getAllClusters

首发版本：3.00.3

## 语法

`getAllClusters()`

## 详情

获取所有集群名称。只能由管理员在 MoM（Master of Master，管理集群）上执行该函数。

## 参数

无

## 返回值

一个表，包含以下字段：

* clusterName：集群名称，字符串。
* clusterType：集群类型，字符串。“momCluster” 代表多集群的管理集群；”memberCluster” 代表普通集群，即被 MoM
  管理的集群。
* status：集群存活状态，整型。 0 代表异常，1 代表存活。

## 例子

```
getAllClusters()
```

| clusterName | clusterType | status |
| --- | --- | --- |
| ShangHai\_cluster2 | memberCluster | 1 |
| Hangzhou\_cluster1 | momCluster | 1 |
| ShangHai\_cluster1 | memberCluster | 1 |
