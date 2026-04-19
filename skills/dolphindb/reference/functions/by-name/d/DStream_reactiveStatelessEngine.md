# DStream::reactiveStatelessEngine

首发版本：3.00.3

## 语法

`DStream::reactiveStatelessEngine(metrics, [filter], [keyColumn],
[timeColumn])`

## 详情

创建流计算响应式无状态引擎。参考：createReactiveStatelessEngine。

## 参数

**metrics** 可以是表或字典数组，表示规则集合。

* 当 *metrics* 为表时：必须以下四列：

  + formula：STRING 类型，表示计算逻辑。其中的变量采用 *keyColumn*
    指定的列中的值标识，*keyColumn* 如不止一列，则使用 `:`
    连接各值。
  + outputMetricKey：STRING 类型，为该计算指定指标名。
  + triggerOn：STRING 类型，表示触发该计算的数据标识，即 *keyColumn*
    指定的列为该值时触发计算，*keyColumn* 如不止一列，则使用 `:`
    连接各值 。
  + filter：一个数据对，表示计算结果的限定范围，属于该范围的结果才会被输出。
* 当 *metrics* 为字典数组时：每个字典表示一条规则，包含键值 *outputName*，formula 以及可选键值
  triggerOn，filter。

**filter** 可选参数，一个数据对，表示引擎级整体输出过滤范围。仅当 *metrics*
中没有设置为空时才使用该整体过滤。

**keyColumn** 可选参数，字符串标量或向量，表示输入表中用于标识数据的列名。

**timeColumn**
可选参数，字符串标量或向量，表示输入表的时间戳列名。配置后输出表包含对应时间列，其值为触发本次计算的数据时间；若多个计算触发同时触发，取最大时间。

## 返回值

返回一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')

g = createStreamGraph('engine')

metrics = array(ANY, 0, 0)
metric1 = dict(STRING,ANY)
// 依赖关系 product_B:value=product_A:factor1+product_A:factor2+product_B:factor1
metric1["outputName"] = `product_B:`value
metric1["formula"] = <A+B+C>
metric1["A"] = `product_A:`factor1
metric1["B"] = `product_A:`factor2
metric1["C"] = `product_B:`factor1
metrics.append!(metric1)
// 依赖关系 product_C:value=product_B:value*product_C:factor1
metric2 = dict(STRING, ANY)
metric2["outputName"] =`product_C:`value
metric2["formula"] = <A*B>
metric2["A"] = `product_B:`value
metric2["B"] = `product_C:`factor1
metrics.append!(metric2)

g.source("input", `product`factor`value, [STRING, STRING, DOUBLE])
.reactiveStatelessEngine(metrics)
.sink("output")
g.submit()
go

products = take("product_A", 2)
factors = ["factor1", "factor2"]
values = [1.0, 2.0]
tmp = table(products as product, factors as factor, values as value)
appendOrcaStreamTable("input", tmp)

products = take("product_B", 1)
factors = take("factor1", 1)
values = take(1.0, 1)
tmp = table(products as product, factors as factor, values as value)
appendOrcaStreamTable("input", tmp)

select * from orca_table.output
```

| productName | metricName | metricsResults |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
