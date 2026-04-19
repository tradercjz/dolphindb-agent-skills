# resubmitStreamGraph

首发版本：3.00.3

## 语法

`resubmitStreamGraph(name)`

## 详情

重新提交处于失败（failed）、销毁中（destroying）或已销毁（destroyed）状态的流图。

## 参数

**name** 字符串标量，表示流图的名字。可以传入完整的流图全限定名（如
"catalog\_name.orca\_graph.graph\_name"），也可以仅提供流图名（如 "factors"）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 例子

假设有已通过 dropStreamGraph 销毁的流图
demo.orca\_graph.indicators：

```
resubmitStreamGraph("demo.orca_graph.indicators")
getStreamGraphMeta("demo.orca_graph.indicators")["status"]
// Output: ["running"]
```
