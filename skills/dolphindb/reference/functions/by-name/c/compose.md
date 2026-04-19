# compose

首发版本：3.00.3

## 语法

`compose(first, second)`

## 详情

创建一个由两个函数组成的复合函数，效果等同于`second(first())`*。*该函数执行逻辑如下：

1. 先调用 *first* 函数，将传入的所有参数传给它；
2. 然后将 *first* 的返回结果作为唯一参数，传给 *second* 函数；
3. 最终返回 `second(first(...))` 的计算结果。

例如，对于复合函数 `f=compose(add,sin)`， `f(x,y)`
的返回值等同于`sin(add(x，y))`。

**函数使用场景**：将多个函数按顺序组合成一个新的函数，可用于数据处理流水线、函数复用、逻辑封装以及函数式编程等场景，提升代码的可读性、可维护性、简化复杂的逻辑表达。

## 参数

**first** 第一个被调用的函数，接受一个或多个参数。

**second** 第二个被调用的函数，只接受一个参数（即 *first* 的返回值）。

## 返回值

一个新的函数（FUNCTIONDEF 类型），入参与 *first* 函数一致。

## 例子

```
g=def(x,y,z){return x*y+z}
f=def(x){return abs(x*3)}
compo_func=compose(g, f) //等同于f(g(*))

compo_func(-1, 5, 3) // Output: 6
```
