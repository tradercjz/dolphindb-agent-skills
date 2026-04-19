# getDatabaseClusterReplicationStatus

## 语法

`getDatabaseClusterReplicationStatus()`

## 详情

查看所有数据库是否启用集群间的异步复制。该函数只能由管理员在主集群的数据节点调用。

## 参数

无

## 返回值

返回一个表，包含以下字段：

* dbName：数据库的路径。
* enabled：布尔值，表示是否启用集群间的异步复制。
* executionSet：任务所属的执行集ID。

相关函数：setDatabaseForClusterReplication
