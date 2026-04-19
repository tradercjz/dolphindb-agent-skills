# deleteSparseReactiveMetric

## 语法

`deleteSparseReactiveMetric(name, outputMetricKey)`

## 详情

删除指定 SparseReactiveStateEngine 中 `outputMetricKey` 对应的规则：若存在则删除并返回
true，否则返回 false。

## 参数

**name** 字符串标量，表示 SparseReactiveStateEngine 的名称。

**outputMetricKey** STRING 的标量或向量，表示要删除的规则对应的输出指标名 outputMetricKey。

## 返回值

BOOL 类型标量，true 代表删除成功。

## 例子

```
deleteSparseReactiveMetric("demoengine", "A002_2")
```

**相关函数**：createSparseReactiveStateEngine, addSparseReactiveMetrics, getSparseReactiveMetrics
