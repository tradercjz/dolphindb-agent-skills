# getOrcaCheckpointConfig

首发版本：3.00.3

## 语法

`getOrcaCheckpointConfig(name)`

## 详情

查看指定流图的 Checkpoint 的配置。

## 参数

**name** 字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

返回一个字典，包含以下字段：

| **key** | **解释** |
| --- | --- |
| enable | 是否开启 Checkpoint |
| checkpointMod | 流图中除 sink 节点以外的一致性级别：  * exactly\_once：数据精确执行一次 * at\_least\_once：数据至少执行一次 |
| interval | 触发 Checkpoint 的时间间隔，单位为毫秒 |
| timeout | Checkpoint 的超时时间，即在指定时间内无法完成的 Checkpoint 将判定为失败，单位毫秒 |
| alignedTimeout | Barrier 对齐的超时时间，即在指定时间内无法完成 Barrier 对齐的Checkpoint 将被判定为失败，单位毫秒 |
| minIntervalBetweenCkpt | 从上一个 Checkpoint 完成到下一个 Checkpoint 发起之间的最小时间间隔 |
| consecutiveFailures | Checkpoint 最大连续失败次数。超过该次数后会导致整个流图的状态转换为 ERROR。 |
| maxConcurrentCheckpoints | 允许 Checkpoint 并发个数。请注意，允许并发Checkpoint可能会对运行中的流计算任务产生影响。 |
| maxRetainedCheckpoints | 系统会定期清理历史 Checkpoint 的数据，该配置项用于设置最多保留多少个最新的 Checkpoint 数据。 |

## 例子

```
getOrcaCheckpointConfig("streamGraph1") // name 是流图名称
getOrcaCheckpointConfig("catalog1.orca_graph.streamGraph1") // name 是全限定名
```
