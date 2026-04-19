# StreamGraph::dropGraph

首发版本：3.00.4

## 语法

`StreamGraph::dropGraph([includeTables])`

## 详情

销毁流图。销毁成功后，流图状态转为 destroyed，但流图记录不会被删除。

* 如果 *includesTables*=true，则在删除流图的同时，也会删除该流图中用户显式创建的流表（如 source、sink
  等）。必须保证该流图中的流表未被其它流图引用。可通过 getStreamTableMeta 查看流流表的引用情况。
* 否则，仅删除流图本身，不会影响这些流表。

在集群部署模式下，执行该操作的用户必须是管理员用户，或拥有流图创建时所用计算组的 COMPUTE\_GROUP\_EXEC
权限。若在单节点部署环境中使用，则无需进行权限校验。

## 参数

**includesTables** 可选参数，布尔值，表示在删除流图时是否同时删除该流图中用户显式创建的流表（如
source、sink 等），默认为 false。

## 例子

```
// 提交流图
createCatalog("test")
use catalog test

t = table(1..100 as id, 1..100 as value, take(09:29:00.000..13:00:00.000, 100) as timestamp)
g = createStreamGraph("factor")
baseStream = g.source("snapshot",  schema(t).colDefs.name, schema(t).colDefs.typeString)
  .reactiveStateEngine([<cumsum(value)>, <timestamp>])
  .setEngineName("rse")
  .buffer("end")

g.submit()

// 删除流图
g.dropGraph()
```

相关函数：dropStreamGraph, createStreamGraph
