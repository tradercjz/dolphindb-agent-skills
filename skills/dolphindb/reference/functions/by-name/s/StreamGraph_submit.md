# StreamGraph::submit

首发版本：3.00.3

## 语法

`StreamGraph::submit([checkpointConfig])`

## 详情

提交流图。

在集群部署模式下，必须在计算节点上执行该函数，且执行用户必须是管理员用户或具备 COMPUTE\_GROUP\_EXEC
权限的用户，才能成功提交任务。若在单节点部署环境中使用，则无需进行权限校验，可直接提交。

## 参数

**checkpointConfig** 可选参数，一个字典，指定了流图 checkpoint 相关配置。可用配置如下：

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

提交流图 g 并通过参数指定 checkpoint 设置。

关于提交与使用流图的详细说明，请参见主题页。

```
if (!existsCatalog("demo")) {
	createCatalog("demo")
}
go
use catalog demo

// 配置参数字典
ckptConfig = {
    "enable":true,
    "interval": 10000,
    "timeout": 36000,
    "maxConcurrentCheckpoints": 1
};

// 指定要计算的指标，此处仅作简单示意
aggregators = [
    <first(price) as open>,
    <max(price) as high>,
    <min(price) as low>,
    <last(price) as close>,
    <sum(volume) as volume>
]
indicators = [
    <time>,
    <high>,
    <low>,
    <close>,
    <volume>
]

// 定义流图
g = createStreamGraph("indicators")
g.source("trade", `time`symbol`price`volume, [DATETIME,SYMBOL,DOUBLE,LONG])
    .timeSeriesEngine(windowSize=60, step=60, metrics=aggregators, timeColumn=`time, keyColumn=`symbol)
    .buffer("one_min_bar")
    .reactiveStateEngine(metrics=indicators, keyColumn=`symbol)
    .buffer("one_min_indicators")

// 提交流图，同时配置 checkpoint
g.submit(ckptConfig)
```

**相关函数：**getOrcaCheckpointConfig, setOrcaCheckpointConfig （更多相关函数，请参见主题页）
