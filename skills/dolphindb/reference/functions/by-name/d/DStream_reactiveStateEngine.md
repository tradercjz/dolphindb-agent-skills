# DStream::reactiveStateEngine

首发版本：3.00.3

## 语法

`DStream::reactiveStateEngine(metrics, [keyColumn], [filter], [keepOrder],
[keyPurgeFilter], [keyPurgeFreqInSecond=0], [keyCapacity=1024],
[parallelism=1])`

## 详情

创建流计算响应式状态引擎。参考：createReactiveStateEngine。

## 参数

**metrics**
以元代码的形式表示计算公式，可以是一个或多个表达式、系统内置或用户自定义函数、一个常量标量/向量。当指定为常量向量时，对应的输出列应该设置为数组向量类型。有关元代码的详情可参考
Metaprogramming。若需使用用户自定义函数，请注意以下事项：

1. 需在定义前添加声明 "@state"。状态函数只能包含赋值语句和 return 语句。

   自 2.00.9 版本起，支持使用 if-else
   条件语句，且条件只能是标量。

   自2.00.11 版本起，支持使用 for 循环（包含 break, continue
   语句），请注意不支持嵌套 for 循环，且循环次数须小于 100 次。
2. 状态引擎中可以使用无状态函数或者状态函数。但不允许在无状态函数中嵌套使用状态函数。
3. 若赋值语句的右值是一个多返回值的函数（内置函数或自定义函数），则需要将多个返回值同时赋予多个变量。例如：两个返回值的函数 linearTimeTrend
   应用于自定义状态函数中，正确写法为：

   ```
   @state
   def forcast2(S, N){
         linearregIntercept, linearregSlope = linearTimeTrend(S, N)
         return (N - 1) * linearregSlope + linearregIntercept
   }
   ```
4. 在响应式状态引擎中，自定义状态函数不允许包含自赋值语句，如 `a=a+b`。以下示例中，当条件为 false
   时，`iif` 表达式会返回 out，从而导致自赋值（`out =
   out`）并报错。

   ```
   out = iif((p1 > 0) and (p2 == 0), p1, out)
   // An assignment statement in state function 'xxx' can't use self reference
   ```

**keyColumn** 可选参数，字符串标量或向量表示分组列名。若指定该参数，计算将在各分组进行。

**filter** 可选参数，以元代码的形式表示过滤条件。过滤条件只能是一个表达式，并且只能包含 *dummyTable*中的列。设置多个条件时，用逻辑运算符（and, or）连接。引擎会先计算指标，然后根据 *filter*指定的过滤条件，输出满足条件的输入数据对应的计算结果。

**keepOrder** 可选参数，表示输出表数据是否按照输入时的顺序排序。设置 *keepOrder* =
true，表示输出表按照输入时的顺序排序。当 *keyColumn* 包含有时间列时，*keepOrder* 默认值为 true，否则默认值为
false。

**keyPurgeFilter** 可选参数，是一个由布尔表达式组成的元代码，表示清理条件。各表达式只能引用
*outputTable* 中的字段。必须指定 *keyColumn* 才能使用该参数。

**keyPurgeFreqInSecond** 正整数，表示触发数据清理需要满足的时间间隔（以秒为单位）。必须指定
*keyColumn* 才能使用该参数。

**keyCapacity** 正整数，可选参数，表示建表时系统为该表预分配的 key 分组数量，用于调整状态表中 key
的函数。通过该参数的合理设置，能够降低在 key 分组较多时可能出现的延迟。

**parallelism** 不超过63的正整数，可选参数，表示并行计算的工作线程数，默认值为
1。在计算量较大时，合理地调整该参数能够有效利用计算资源，降低计算耗时。

注：

*parallelism* 不能超过 min(许可核数, 逻辑核数)-1。

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

g.source("trades", `date`time`sym`market`price`qty, [DATE, TIME, SYMBOL, CHAR, DOUBLE, INT])
.reactiveStateEngine(metrics=<mavg(price, 3)>, keyColumn=["date","sym"], filter=<date between 2012.01.01 : 2012.01.03>, keepOrder=true)
.sink("output")
g.submit()
go

n=100
tmp = table(rand(2012.01.01..2012.01.10, n) as date, rand(09:00:00.000..15:59:59.999, n) as time, rand("A"+string(1..10), n) as sym, rand(['B', 'S'], n) as market, rand(100.0, n) as price, rand(1000..2000, n) as qty)

appendOrcaStreamTable("trades", tmp)
```
