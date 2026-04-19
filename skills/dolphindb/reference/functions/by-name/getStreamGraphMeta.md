# getStreamGraphMeta

首发版本：3.00.3

## 语法

`getStreamGraphMeta([name])`

## 详情

返回指定流图的元信息。如果未指定 *name*，则返回所有流图的元信息。

## 参数

**name** 可选参数，字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 返回值

一个表，包含以下字段：

* id：流图 id
* fqn：该流图的全限定名
* status：流图运行状态，可能的值包括：
  + building：流图已且调度完毕，正在构建中。
  + running：流图构建完毕，正常运行，可以提供服务。
  + error：遇到可恢复故障（如节点 OOM），系统将重新调度此流图的任务。
  + failed：遇到不可恢复故障（如用户脚本逻辑有误），系统将保留现场，供后续分析。
  + destroying：流图正在销毁。
  + destroyed：流图已经销毁。
* semantics：一致性语义，可选值为：
  + exactly-once：精确执行一次
  + at-least-once：至少执行一次
* checkpointConfig：Checkpoint 相关配置，可通过接口 `setCheckpointConfig`
  修改。
* tasks：流图的调度元信息
  + id：任务 id
  + node：构建任务的节点名称
  + status：任务执行状态
  + reason：状态转移的原因
* createTime：创建时间
* owner：流图的创建者
* reason：状态转移的原因

## 例子

```
getStreamGraphMeta("streamGraph1") // name 是流图名称
getStreamGraphMeta("catalog1.orca_graph.streamGraph1") // name 是全限定名
```
