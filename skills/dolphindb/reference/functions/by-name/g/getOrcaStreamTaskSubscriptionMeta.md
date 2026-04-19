# getOrcaStreamTaskSubscriptionMeta

首发版本：3.00.3

## 语法

`getOrcaStreamTaskSubscriptionMeta(name)`

## 详情

获取指定流图中所有流任务的订阅信息。

## 参数

**name** 字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

返回一个表，包含以下字段：

* taskId：流任务 id
* tableName：流表的名称
* actionName：订阅任务的名称

## 例子

```
getOrcaStreamTaskSubscriptionMeta("streamGraph1") // name 是流图名称
getOrcaStreamTaskSubscriptionMeta("catalog1.orca_graph.streamGraph1") // name 是全限定名
```
