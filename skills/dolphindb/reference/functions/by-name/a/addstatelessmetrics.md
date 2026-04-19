# addStatelessMetrics

## 语法

`getStatelessMetrics(name)`

## 详情

向响应式无状态引擎中增加计算逻辑。

## 参数

**name** STRING 类型标量，表示响应式无状态引擎的名字。

**metrics** 一个表，表示增加的计算逻辑：

* formula：STRING 类型，表示计算逻辑。其中的变量采用 *keyColumn*
  指定的列中的值标识，*keyColumn* 如不止一列，则使用 `:`
  连接各值。
* outputMetricKey：STRING 类型，为该计算指定指标名。
* triggerOn：STRING 类型，表示触发该计算的数据标识，即 *keyColumn*
  指定的列为该值时触发计算，*keyColumn* 如不止一列，则使用 `:`
  连接各值 。
* filter：一个数据对，表示计算结果的限定范围，属于该范围的结果才会被输出。

## 例子

```
metricsTable = table(
    ['"factor1" * "factor2"'] as formula,
    ["value3"] as outputMetricKey,
    ["factor1"] as triggerOn,
    [10:20] as filter
)

addStatelessMetrics("engine1",metricsTable)
```
