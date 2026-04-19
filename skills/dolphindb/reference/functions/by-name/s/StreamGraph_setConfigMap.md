# StreamGraph::setConfigMap

首发版本：3.00.3

## 语法

`StreamGraph::setConfigMap(dict)`

## 详情

用于设置流图中私有流表和订阅的相关配置。在生成流图的过程中，系统会自动添加用于数据重分布（shuffle）的私有流表及订阅关系，这些组件无需用户手动声明。若需修改这些自动生成组件的运行参数，可通过
`setConfigMap` 传入配置项。

## 参数

**dict** 一个字典，目前支持如下键值对：

| **键名** | **类型** | **默认值** | **说明** |
| --- | --- | --- | --- |
| subscription.batchSize | INT | 0 | 设置该流图中所有订阅的 *batchSize* 参数 |
| subscription.throttle | INT | 1 | 设置该流图中所有订阅的 *throttle* 参数 |
| subscription.timeTrigger | BOOL | false | 设置该流图中所有订阅的 *timeTrigger* 参数 |
| subscription.sourceOffset | INT | -3 | 设置流图中所有由 `StreamGraph::source` 创建的流表订阅的 *offset* 参数。 |
| privateTable.cacheSize | INT | 1000 | 设置该流图中所有启用持久化的私有流表的 *cacheSize* 参数 |

## 返回值

一个 DGraph 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

g = createStreamGraph("orca")
  .setConfigMap({
    "subscription.throttle": 1,
    "privateTable.cacheSize": 1000
  })
```
