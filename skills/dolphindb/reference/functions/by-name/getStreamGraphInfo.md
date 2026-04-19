# getStreamGraphInfo

首发版本：3.00.3

## 语法

`getStreamGraphInfo([name])`

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
* graph：流图的结构，JSON 格式：
  + version：流图结构的版本号，预防因版本升级引发的兼容性问题。
  + nodes：流图中的节点，包括以下结构：
    - id：节点 id
    - subgraphId：所属子图 id
    - taskid：流任务 id
    - parallelism：
      * keyName：划分并行任务的列名
      * count：并行任务数量
    - properties：节点的属性
    - inEdges：入边的 id 列表
    - outEdges：出边的 id 列表
  + edges：流图中的边，包括以下结构：
    - id：边 id
    - inNodeId: 入节点 id
    - outNodeId：出节点 id
    - partitionType：
      * FORWARD：将上游数据直接发送给下游
      * NESTED：将上游数据按照上下游并行度的嵌套关系分发给下游
      * SHUFFLE：将上游数据重新合并成一组数据后按照并行度分发给下游
    - filter：该边的过滤条件
    - handlers：处理上游数据的函数列表，系统将合并这些函数组成 `subscribeTable`
      的 *handler* 参数
  + config：流图的全局配置
* meta：流图的调度元信息，JSON 格式：
  + id：流图 id
  + status：流图运行状态，可能的值包括：
    - building：流图已调度完毕，正在构建中。
    - running：流图构建完毕，正常运行，可以提供服务。
    - error：遇到可恢复故障（如节点 OOM），系统将重新调度此流图的任务。
    - failed：遇到不可恢复故障（如用户脚本逻辑有误），系统将保留现场，供后续分析。
    - destroying：流图正在销毁。
    - destroyed：流图已经销毁。
  + semantics：一致性语义，可选值为：
    - exactly-once：精确执行一次
    - at-least-once：至少执行一次
  + tasks：流任务的调度信息
  + createTime：创建时间
  + reason：状态转移的原因

## 例子

```
getStreamGraphInfo("streamGraph1") // name 是流图名称
getStreamGraphInfo("catalog1.orca_graph.streamGraph1") // name 是全限定名
```
