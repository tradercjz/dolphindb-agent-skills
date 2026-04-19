# StreamGraph::setLocalConfigOnce

首发版本：3.00.3.1

## 语法

`StreamGraph::setLocalConfigOnce(dict)`

## 详情

设置流图中相邻节点之间的订阅配置。调用该函数后，配置将覆盖通过 `StreamGraph::setConfigMap`
设置的全局配置，或新增之前未设置的配置。配置仅在调用节点与其直接连接的下游节点之间生效一次；若两个节点之间存在级联关系，则配置不生效。

注意：由于 `sink` 和 `map` 操作不生成新的节点，配置会延续生效至下一个实际节点。

## 参数

**dict** 一个字典，目前支持如下键值对：

| 键名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| subscription.batchSize | INT | 0 | 设置该流图中相邻节点间订阅的 *batchSize* 参数 |
| subscription.throttle | INT | 1 | 设置该流图中相邻节点间订阅的 *throttle* 参数 |
| subscription.timeTrigger | BOOL | false | 设置该流图中相邻节点间订阅的 *timeTrigger* 参数 |
| subscription.sourceOffset | INT | -3 | 设置流图中由 `StreamGraph::source` 创建的节点与其相邻的下游节点之间订阅的 *offset* 参数。 |

## 返回值

一个 DStream 对象。

## 例子

下例将流图中用于计算 1分钟 K 线的订阅参数 *batchSize* 设置为100，其余节点订阅参数 *batchSize* 仍然为默认值。

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}

use catalog orca

g = createStreamGraph("indicators")
sourceStreams = g.source("trade", `symbol`datetime`price`volume, [SYMBOL, TIMESTAMP,DOUBLE, INT])
    .fork(2)
stream_1min = sourceStreams[0]
    .setLocalConfigOnce({
      "subscription.batchSize": 100
    })
    .timeSeriesEngine(60*1000, 60*1000, <[first(price),max(price),min(price),last(price),sum(volume)]>, "datetime", false, "symbol")
    .reactiveStateEngine(<[datetime, first_price, max_price, min_price, last_price, sum_volume, mmax(max_price, 5), mavg(sum_volume, 5)]>, `symbol)
    .sink("output_1min")
stream_5min = sourceStreams[1]
    .timeSeriesEngine(5*60*1000, 5*60*1000, <[first(price),max(price),min(price),last(price),sum(volume)]>, "datetime", false, "symbol")
    .reactiveStateEngine(<[datetime, first_price, max_price, min_price, last_price, sum_volume, mmax(max_price, 5), mavg(sum_volume, 5)]>, `symbol)
    .sink("output_5min")
```
