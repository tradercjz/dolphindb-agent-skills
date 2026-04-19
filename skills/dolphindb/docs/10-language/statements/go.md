<!-- Auto-mirrored from upstream `documentation-main/progr/statements/go.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# go

## 语法

`go`

## 详情

DolphinDB 对提交执行的代码首先进行语法解析，代码全部解析成功后才开始执行。`go`
语句的作用是对代码分段进行解析和执行，即先解析并执行 go 语句之前的代码，然后再解析并执行其后的代码。

解析时，一个变量或函数必须被显式定义，后续才可引用。share, enableTableShareAndPersistence, loadPlugin，run 等函数在执行过程中会动态注册一些变量或函数，但是解析这些函数的过程中，
并不会注册新的变量或函数。因此，`share` 等函数之后的代码若需要引用这些函数动态注册的变量或函数，必须使用 go
语句，否则解析后续代码时会抛出未定义变量或函数等异常。

注意：

DolphinDB
的语句或函数必须经过完整的解析后才能执行。因此，`go` 语句无法应用在一个判断语句、循环语句及其他嵌套语句或者函数体中。

## 例1：动态注册的变量

执行以下代码时，系统会抛出变量未定义的异常。

```
t=table(rand(`WMI`PG`TSLA,100) as sym, rand(1..10, 100) as qty, rand(10.25 10.5 10.75, 100) as price);
share(t,`st); // 试图将表 t 共享为会话中可见的共享表 st
insert into st values(`AAPL,50,10.25); // 试图向共享表 st 中插入数据
```

返回错误：`Syntax Error: [line #3] Can't recognize table st`。这说明 DolphinDB
对以上代码语法解析时认为共享表 st 未定义。尽管第二行中试图使用 `share` 函数将已定义的表 t 共享为 st，但在语法解析 st
时，st 并未注册，因此系统抛出异常，不执行任何代码。

因此，为确保动态注册的变量或函数能够被语法解析，需要在 `share` 语句后加一个
`go` 语句：

```
t=table(rand(`WMI`PG`TSLA,100) as sym, rand(1..10, 100) as qty, rand(10.25 10.5 10.75, 100) as price);
share(t,`st);
go;
insert into st values(`AAPL,50,10.25);
```

在运行以上脚本时：

1. DolphinDB 首先解析并执行前两行代码，将表 t 共享为表 st；
2. 接着执行 `go` 语句使共享表 st 得到显示定义；
3. 然后解析并执行第四行代码，向共享表 st 中插入数据。

## 例2：在脚本中定义的变量

下例中在 *test.txt* 文件中定义了变量 a=100，通过 `run`
函数执行该文件后使用 `print()` 调用变量 a，若不使用 go 语句，后续代码中若引用变量 a，编译阶段会报未定义变量 a
的错误。

```
run("/home/DolphinDB/test.txt");
print(a);
```

返回：`Syntax Error: [line #2] Cannot recognize the token a`。

因此需要将 `go` 语句添加在 `run` 函数所在行之后，再运行
`print()` 调用变量 a：

```
run("/home/DolphinDB/test.txt");
go;
print(a);
```

## 例3：动态注册的命名函数

在以下例子中，第一行中定义了变量 fs，其中三次使用了命名函数 f2()，在第二行中试图使用 `runScript` 函数本地执行
fs[2]，并在第三行打印 f2()，返回：`Syntax Error: [line #3] Cannot recognize the token
f2`。

这是因为在以下代码块解析阶段，只注册了变量 fs，函数体 f2() 解析时并未注册。因此，在语法解析阶段 f2()
被认为未定义从而报错。

```
fs = ["def f2(){return 'haha1';}", "def f2(){return 'haha2';}", "def f2(){return 'haha3';}"];
runScript(fs[2]);
print(f2());
```

可以使用 `go` 语句，先解析执行第一行和第二行代码，可以生成动态变量 f2()。

```
fs = ["def f2(){return 'haha1';}", "def f2(){return 'haha2';}", "def f2(){return 'haha3';}"];
runScript(fs[2]);
go
print(f2());
```

返回：haha3。

## 例4：`for` 循环语句中的 `go`

`go` 在 `for` 循环语句中不能生效。

```
fs = ["def f2(){return 'haha1';}", "def f2(){return 'haha2';}", "def f2(){return 'haha3';}"];
for(s in fs){runScript(s); go; print(f2());}
```

返回：`Syntax Error: [line #2] Cannot recognize the token f2`。

出现该报错的原因在于，在上述脚本中，虽然函数 f2() 在 fs 中被定义了三次，但实际上每次定义都是在全局范围内，而不是在循环体内。因此，每次定义 f2()
函数时都会覆盖前面的定义，最终只有一个 f2() 函数被保留在全局作用域内。而当在第二行的 for 循环中运行这些定义时，每次调用 runScript(s)
时都会重新解析并执行字符串 s 中的代码，包括对 f2() 函数的定义，导致最后一次定义的 f2() 函数覆盖了前面的定义。

当程序执行到 `print(f2())` 时，由于f2() 函数在最后一次迭代中的定义无法被正确识别，因此报错 'Syntax Error:
[line #2] Cannot recognize the token f2'。

## 例5：取消定义后的 `go`

以下例子在第一次将 a 定义为向量后尝试通过 `undef` 取消 a 的定义：

```
a = [1,2,3,4,5];
b = typestr(a); // typestr 函数以字符串的形式返回对象 a 的数据类型
b; // 如果只运行到这一步，b 将返回：FAST INT VECTOR
undef "a";  // 取消第一行 a 的定义
a = 1; // 为 a 赋予整数值 1
b = typestr(a); // 再次运行 typestr 获取 a 的数据类型
b; // 预期返回 INT 但此时报错
```

返回：`'a = 1 => Assignment statement failed probably due to invalid indices [a =
1]'`。

在上述脚本的第 4 行中，尽管 `undef “a“` 的执行意图在于取消变量 a 的原有定义。但由于 DolphinDB
脚本语言先解析后执行这一特征，在上面这段脚本中，第 4 行解析结束时所有 7 行代码并未解析完成，无法立即执行 `undef
“a“`。这使得第 5 行尝试对 a 重新赋值失效，因为此时运行环境中 a 的实际值依然是第 1 行的定义。因此在执行第 6 和 7 行时报错。

如果需要达到预期的结果，就需要在 `undef “a“` 后使其立刻生效。所以，需要加入 go 将前 4 行作为一个代码块整体执行。go
执行后，`a = 1` 的重新赋值才有意义。

```
a = [1,2,3,4,5];
b = typestr(a);
b;
undef "a";
go; // 将以上代码执行完毕后，再执行以下对 a 的重定义
a = 1;
b = typestr(a);
b;
```

使用 `go` 命令后，a 的定义在第 4 行运行结束后被取消；此后再通过 `a = 1`
将其重新赋值，这样第 7 行的 `b = typestr(a)` 就能够获取到重新定义的 a 的数据类型并返回 INT。
