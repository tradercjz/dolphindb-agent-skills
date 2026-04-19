# setOrcaCheckpointConfig

首发版本：3.00.3

## 语法

`setOrcaCheckpointConfig(name, configMap)`

## 详情

动态修改 checkpoint 的配置。

## 参数

**name** 字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**configMap** 一个字典，表示具体配置。键值设置如下表所示。

| **key** | **解释** | **value 取值** | **默认值** |
| --- | --- | --- | --- |
| enable | 是否开启 Checkpoint | true/false | false |
| interval | 触发 Checkpoint 的时间间隔，单位为毫秒 | [10秒, 1年] | 1小时 |
| timeout | Checkpoint 的超时时间，即在指定时间内无法完成的 Checkpoint 将判定为失败，单位毫秒 | [1秒，1小时] | 10分钟 |
| alignedTimeout | Barrier 对齐的超时时间，即在指定时间内无法完成 Barrier 对齐的Checkpoint 将被判定为失败，单位毫秒 | [100毫秒，1小时] | 10分钟 |
| minIntervalBetweenCkpt | 从上一个 Checkpoint 完成到下一个 Checkpoint 发起之间的最小时间间隔 | [0，1年] | 0 |
| consecutiveFailures | Checkpoint 最大连续失败次数。超过该次数后会导致整个流图的状态转换为 ERROR。 | [0, 102400] | 3 |
| maxConcurrentCheckpoints | 允许 Checkpoint 并发个数。请注意，允许并发Checkpoint可能会对运行中的流计算任务产生影响。 | [1, 102400] | 1 |
| maxRetainedCheckpoints | 系统会定期清理历史 Checkpoint 的数据，该配置项用于设置最多保留多少个最新的 Checkpoint 数据。 | [1， 1024] | 3 |

## 例子

```
ckptConfig = {
    "enable":true,
    "interval": 10000,
    "timeout": 36000,
    "maxConcurrentCheckpoints": 1
};
setOrcaCheckpointConfig("streamGraph1", ckptConfig)
```
