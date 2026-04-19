<!-- Auto-mirrored from upstream `documentation-main/progr/lambda.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Lambda 表达式

Lambda 表达式是只有一个语句的函数。

## 语法

`def <functionName>(parameters):
expression`

或

`def (parameters): expression`

或

`def (parameters) -> expression`

或

`parameter -> expression`

## 详情

Lambda 函数既可以是命名函数，也可以是匿名函数。它可以接收任意数量的参数，但只能有一个表达式。在以上语法中，第二、三、四种语法定义了匿名的 Lambda
函数，但第四种语法仅适用于只有一个参数的情况。匿名的 Lambda 函数有以下用法：

* 赋值给一个变量，如 `f=def(x):x*x`。
* 作为函数的参数，如 `each(def(a,b):a+b, 1..10, 2..11)`。
* 作为函数的返回值，如 `def(x){return def(k): k*x}`。
* 使用 {} 封装后，除以上用法外还支持：

  + 作为函数，接收一个参数，如 `{x->x*x}(10)`
  + 作为运算符。单目运算符的优先级低于双目运算符，如 `{x->x*x} 10 {x,y->x+y} 1`
    的执行顺序是先执行 `10 {x,y->x+y} 1`，得到结果11后，再执行
    `{x->x*x}` 11，结果为121。
  + 与高阶函数模式符号搭配使用，如`{x->x*x + x}:E matrix(1 2 3, 4 5
    6)`。
  + 以 `object.method()` 的方式调用。

## 例子

```
def f(x):x pow 2 + 3*x + 4.0;
f(2);
```

返回：14

```
def orderby(x,y): x[isort y];
t=table(3 1 7 as id, 7 4 9 as value);
orderby(t, t.id);
```

得到：

| id | value |
| --- | --- |
| 1 | 4 |
| 3 | 7 |
| 7 | 9 |

以 `object.method()` 的方式调用 lambda 函数：

```
v = 1..6
v.{x->x*x+1}()
// output: [2,5,10,17,26,37]
```

此方式也可与高阶函数搭配使用。如下例中，需要对矩阵按行应用 lambda 函数，可搭配高阶函数 byRow(:H)
来实现。

```
m = matrix(1 2 3, 4 5 6, 7 8 9)
m.{x->cumavg(x)*x+x}:H()
```

结果为：

|  |  |  |
| --- | --- | --- |
| #0 | #1 | #2 |
| 2 | 14 | 35 |
| 6 | 22.5 | 48 |
| 12 | 33 | 63 |

```
each(def(a,b):a+b, 1..10, 2..11);
// output
[3,5,7,9,11,13,15,17,19,21]

g = def (x,y) -> log(x) + y pow 2;
g(e,0);
// output
1

each(x->x+1,1 3 5)
// output
[2,4,6]
```

作为函数的返回值时：

```
def f1(x){return def(k): pow(x,k)}
f1(1)
//output: {def (x, k)->power(x, k)}{1}

f1(1)(10)
//output: 1
```

通过 {} 封装后直接作为函数使用：

```
{x->x*x}(2)
//output: 4

//封装一个聚合函数
{defg(x)-> sum(x)/max(x)}(2 5 6)
//output: 2
```

通过 {} 封装后也可作为运算符使用：

```
{def(x):x*x} 4
//output: 16
```

当 lambda 函数作为运算符时，双目运算符的优先级与乘法和除法相同，单目运算符具有最低优先级：

```
2 *{x->x*x} 10 {x,y->x+y} 1
//output: 242
```

作为单目运算符时，可以多个运算符连用：

```
{x->x*x}{x->x+1}{x->x*2} 10
//output: 441
```
