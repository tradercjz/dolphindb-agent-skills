# 复合函数

复合函数是由两个函数组合在一起的函数，相当于 `f(g(x))`。其中 *x*
是输入参数，可以有一个或多个。复合函数的基本思想是将一个函数的输出作为另一个函数的唯一输入，从而形成一个新的函数。复合函数可以有效提高代码的可读性、可维护性，并简化复杂的逻辑表达。

在 DolphinDB 中，可以通过 compose
函数来创建复合函数。`compose(first,second)` 接受两个函数作为参数，首先调用 *first*函数，传入参数并获取返回结果，然后将结果传递给 *second* 函数，最终返回 `second(first(...))`
的结果。返回的新函数参数与 *first* 函数一致。

假设我们有两个函数 `doubleValue` 和
`increment`。我们可以将这两个函数组合成一个新的复合函数，首先执行
`doubleValue`，然后再对结果执行 `increment`，最终返回结果。

```
// 定义两个简单函数
doubleValue = x -> x * 2
increment = x -> x + 1

// 使用 compose 创建复合函数
composedFunc = compose(doubleValue, increment)

composedFunc([3,4,5])  // output: [7,9,11]
```
