# StreamGraph::name

首发版本：3.00.3

## 语法

`StreamGraph::name()`

## 详情

获取流图的全限定名（Fully Qualified Name, FQN）。

## 返回值

STRING 类型标量。

## 例子

获取 StreamGraph::submit 函数文档的例子中所提交流图 g
的全限定名：

```
g.name()
// Output: 'demo.orca_graph.indicators'
```
