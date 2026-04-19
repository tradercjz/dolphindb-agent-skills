<!-- Auto-mirrored from upstream `documentation-main/progr/metaProgr_func.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 函数元编程

函数元编程是指通过参数传递等手段动态获取函数定义和参数的方法。该方法通常应用于一些复杂的数据分析场景。

## 动态获取函数定义

函数定义在 DolphinDB 中是一种数据类型，FUNCTIONDEF。它可以通过内置函数
`funcByName`，根据输入的函数名称，来动态获取。下面的例子从变量 *name*
获取函数的名称，并通过该函数获取对应的函数定义，然后以 *v* 为参数，调用这个函数。如果函数定义在某个模块中，可以在名称前加上模块名称并用
namespace 符号 :: 分隔。

```
name = `sin
v = 1..10
funcByName(name)(v)

// output: [0.8415,0.9093,0.1411,-0.75688,-0.9589,-0.2794,0.657,0.9894,0.4121,-0.5440]
```

在某些场景下，动态获取的函数可能是一个匿名函数（包括匿名 `lambda` 函数）。此时可以通过字符串传入函数的定义，并通过
`parseExpr` 函数动态解析函数。`parseExpr` 返回的是一个 DolphinDB
的元编程对象，这个对象的类型是 CODE，表示一段可以通过 `eval`
函数执行的表达式代码。因此下面的例子中，`parseExpr` 返回的对象需要先执行 `eval`
函数，去获取解析后的函数。

```
funcDef = "x->1 + x + x*x"
parseExpr(funcDef).eval().call(2)
//output: 7
```

## 动态函数调用

DolphinDB 中可以通过以下3种方法来动态调用函数：

* 通过高阶函数 `call` 来调用函数定义。
* 通过运算符 () 来调用函数定义。
* 通过函数 `at`
  来调用函数定义。

  ```
  f = parseExpr("{x,y->(x - y)/(x + y)}").eval()
  //方法一
  call(f, 3.0, 2.0)
  //方法二
  f(3.0, 2.0)
  //方法三
  at(f, (3.0, 2.0))
  ```

这三种方法各有不同。前两种方法比较类似，参数个数是可变的，因此开发人员在调用时都需要知道参数的个数。使用 `at`
函数时，参数个数是明确的，只有两个参数，第一个是函数定义，第二个是函数定义需要的参数。这种参数个数固定的用法，更方便动态调用。如果 `f`
是一个多元函数，`at` 函数的第二个参数必须是一个元组，元组的每一个元素代表 `f`
的一个输入参数。考虑一个特殊的用例，`f` 函数是一个一元函数，可以接受一个元组 *x*
作为输入参数。如下例所示，要正确使用 `at` 函数，必须使用 `enlist` 函数，让 *x*
成为一个新元组的唯一参数，否则系统会报错：实际输入的参数个数与函数定义不符。这是因为 *x* 有三个元素，而 `f`
函数只接受一个参数。

```
f = {x->x.head()\x.tail()}
x = (1,2,3)
//错误用法, 参数个数与函数定义不匹配
at(f, x)
//正确用法
at(f, enlist x)
```

## 动态产生函数调用的代码

上一个小节中的动态函数调用跟普通的函数调用一样，都会直接执行该函数，得到函数的返回值。但有时我们需要用函数调用来表达一种逻辑关系，并在后续的场景中运行。譬如我们需要用函数来表示数据过滤条件，并作为一个
SQL 查询的 `where` 子句，后续当我们真正执行这个 SQL
语句时，这个函数才会被执行。这种延迟执行的场景下，其实我们需要动态产生函数调用的代码。DolphinDB 提供了 `makeCall` 和
`makeUnifiedCall` 两个函数来生成函数调用的代码。这两者的区别等同于 `call`
和 `at`
之间的区别，前者需要输入的参数个数取决于对应函数需要的参数个数，而后者只提供一个固定的参数，如果函数需要多个参数，则封装在一个元组中。

```
f = parseExpr("{x,y->(x - y)/(x + y)}").eval()
makeCall(f, sqlCol("qty1"), sqlCol("qty2"))
makeUnifiedCall(f, (sqlCol("qty1"), sqlCol("qty2")))
makeUnifiedCall(f, sqlTuple(`qty1`qty2))
```

上面的例子中，动态获得的 `lambda` 函数包含两个参数 *x* 和 *y*，表中的两个列 *qty1*
和 *qty2*，作为输入参数。在 `makeCall` 函数中使用 `sqlCol`
函数，将两列 *qty1* 和 *qty2* 分别作为两个参数输入。当使用 `makeUnifiedCall`
时，我们既可以使用 `sqlTuple` 函数产生多个列组成的元组，也可以手动地使用 () 来产生一个元组。

```
f = parseExpr("{x,y->(x-y)/(x+y)}").eval()
t = table(1.0 2.0 3.0 as qty1, 1.0 3.0 7.0 as qty2)
sql(select=makeCall(f, sqlCol("qty1"), sqlCol("qty2")), from=t).eval()
sql(select=makeUnifiedCall(f, (sqlCol("qty1"), sqlCol("qty2"))), from=t).eval()
sql(select=makeUnifiedCall(f, sqlTuple(`qty1`qty2)), from=t).eval()
// 三个表达式得到相同的结果
```

| \_qty1 |
| --- |
| 0 |
| -0.2 |
| -0.4 |
