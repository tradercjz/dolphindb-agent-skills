<!-- Auto-mirrored from upstream `documentation-main/progr/anonym_func.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 匿名函数

匿名函数是一个没有名字的函数。可以在以下场景使用 ：

* 作为参数传递给另一个函数
* 赋值给一个变量，以后使用
* 作为函数的返回值返回
* 原地调用

## 语法

`def (parameters){statements}`

或

`def (parameters): expression`

## 例子

作为参数传递给另一个函数。

```
each(def(a,b):a+b, 1..10, 2..11);
// output
[3,5,7,9,11,13,15,17,19,21]
// 详情请查看函数each
```

赋值给一个变量，用于后续使用。

```
g=def(x):2*x;
g(2);
// output
4
```

作为函数的返回值返回。

```
def f(x){return def(k): k*x};
f(7)(8);
// output
56
```

原地调用。

```
def(a,b){return (a+1)*(b+1)} (4,5);
// output
30
```

除了支持自定义聚合函数(详情见 NamedFunction)外，DolphinDB 支持自定义匿名聚合函数。 其语法和匿名函数语法基本一致。

```
f = defg (x, y){
a = sum(abs(x+y))
b=sum(abs(x))+sum(abs(y))
return a\b
};
x = 1..5;
y = 1 -1 1 -2 2;
f(x, y);
// output
0.727273
```

匿名函数可作为函数的返回值。

```
f = defg (x){return defg(k): sum(k*x)}
x = 1..5
y = 6..10
f(x)(y)
// output
130
```
