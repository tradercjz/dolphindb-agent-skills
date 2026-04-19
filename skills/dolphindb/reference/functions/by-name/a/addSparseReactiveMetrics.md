# addSparseReactiveMetrics

## 语法

`addSparseReactiveMetrics(name, metrics)`

## 详情

为指定的 SparseReactiveStateEngine 增加稀疏状态计算规则。

## 参数

**name** 字符串标量，表示需要增加计算规则的 SparseReactiveStateEngine 的名称。

**metrics** 是一个表，表示需要新增的规则。表结构与 `createSparseReactiveStateEngine` 的
*metrics* 参数相同。

## 例子

```
newMetrics = table(
    ["A003"] as deviceID,
    ["mavg(value,3)"] as formula,
    ["A003_1"] as outputMetricKey
)
addSparseReactiveMetrics("demoengine", newMetrics)
```

**相关函数**：createSparseReactiveStateEngine, getSparseReactiveMetrics, deleteSparseReactiveMetric
