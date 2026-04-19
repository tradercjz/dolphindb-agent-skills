# purgeStreamGraphRecords

首发版本：3.00.3

## 语法

`purgeStreamGraphRecords(name)`

## 详情

删除指定流图在 DFS 表中的记录。仅当流图状态为 destroyed 时才允许执行该操作，否则将抛出异常。

在集群部署模式下，执行该操作的用户必须是管理员用户或拥有流图创建时所用计算组的 COMPUTE\_GROUP\_EXEC
权限。若在单节点部署环境中使用，则无需进行权限校验。

## 参数

**name** 字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

无。

## 例子

对 dropStreamGraph 函数的例子中已销毁的流图进行操作，删除其在
DFS 表中记录：

```
purgeStreamGraphRecords("demo.orca_graph.indicators")
getStreamGraphMeta("demo.orca_graph.indicators")["status"]

/*
id fqn status semantics checkpointConfig tasks createTime owner reason
-- --- ------ --------- ---------------- ----- ---------- ----- ------
*/
```
