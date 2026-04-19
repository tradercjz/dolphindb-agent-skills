# warmupOrcaStreamEngine

首发版本：3.00.3

## 语法

`warmupOrcaStreamEngine(name, data)`

## 详情

将指定表写入目标流引擎中进行预热处理，但不会产生任何输出。这么做的目的是利用这批预热数据提前计算中间状态，下一批次数据写入此流数据引擎，可以利用已计算的结果来加速计算。

目前仅支持响应式状态引擎，时间序列聚合引擎和日级时间序列引擎。

与现有 warmupStreamEngine
不同，`warmupOrcaStreamEngine` 支持在集群任意节点上调用，其本质是在引擎所在节点上远程执行
`warmupStreamEngine`。

## 参数

**name** 表示引擎名称。字符串标量，可以传入完整的全限定名（如
"catalog\_name.orca\_engine.engine\_name"）；或引擎名（如 "engine\_name"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**data** 数据表对象。

## 返回值

无。

## 例子

下例中，`warmupOrcaStreamEngine("rse", t)` 先将数据表 t 写入响应式状态引擎 rse 进行预热，由此确保
`<ema(value, 100)>` 指标在预热阶段窗口内已有完整历史数据。

```
if (!existsCatalog("test")) {
	createCatalog("test")
}
go;
use catalog test

t = table(1..100 as id, 1..100 as value, take(09:29:00.000..13:00:00.000, 100) as timestamp)
g = createStreamGraph("factor")
baseStream = g.source("snapshot",  schema(t).colDefs.name, schema(t).colDefs.typeString)
  .reactiveStateEngine([<ema(value, 100)>, <timestamp>])
  .setEngineName("rse")
  .buffer("end")

g.submit()

warmupOrcaStreamEngine("rse", t)
appendOrcaStreamTable("snapshot", t)
```
