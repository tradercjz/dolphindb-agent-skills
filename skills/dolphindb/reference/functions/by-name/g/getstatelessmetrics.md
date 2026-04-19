# getStatelessMetrics

## 语法

`getStatelessMetrics(name)`

## 详情

获取响应式无状态引擎的计算逻辑。

## 参数

**name** STRING 类型标量，表示响应式无状态引擎的名字。

## 返回值

一个表，包含四列： formula， outputMetricKey，triggerOn，filter。

## 例子

```
getStatelessMetrics("engine1")
```

| formula | outputMetricKey | triggerOn | filter |
| --- | --- | --- | --- |
| "factor1" + "factor2" + "factor3" | value1 | factor3 | void() |
| "value1"\*"factor3" | value2 |  | pair<double>(10, 40) |
| "factor1" \* "factor2" | value3 | factor1 | pair<int>(10, 20) |
