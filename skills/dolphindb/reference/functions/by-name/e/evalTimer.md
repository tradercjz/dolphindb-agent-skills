# evalTimer

## 语法

`evalTimer(funcs, [count=1])`

## 详情

返回执行指定函数耗费的时间，单位是毫秒。如果 *funcs*
包含多个函数，`evalTimer` 返回的是顺序执行这些函数耗费的时间。

timer 语句和
`evalTimer` 函数的功能类似，两者的区别是：

* `timer` 语句的输入是代码块；
  `evalTimer` 函数的输入是函数。如果要用 `evalTimer`
  函数计算执行一段代码的时间，需要把代码写成自定义函数。
* `timer` 语句的返回结果是一条消息，不能赋值给一个变量；
  `evalTimer` 函数的返回结果是一个标量，可以赋值给变量。

## 参数

**funcs** 是一个或多个没有参数的函数。如果有多个函数，使用元组表示。

**count** 是一个整数，表示执行的次数。它是可选参数，默认值为1。

## 返回值

DOUBLE 类型标量。

## 例子

```
x=rand(10.0, 1000000)
evalTimer(dot{x,2},10);
// output
39.609375

evalTimer(sort{x},10);
// output
837.542702

evalTimer([dot{x,2},sort{x}],10)
// output
870.065348
```

从上面的例子可以看出，`evalTimer`
返回的是顺序执行这些函数耗费的时间，而不是并行执行。
