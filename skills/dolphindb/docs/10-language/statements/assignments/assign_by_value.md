<!-- Auto-mirrored from upstream `documentation-main/progr/statements/assignments/assign_by_value.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 按值赋值

我们使用"="来表示值赋值，它拷贝一份对象的值并赋予新的变量。

## 语法

变量：

`<variable>=<object>`

或

`<variable>[index]=<object>`

常量：

`const <variable>=<object>`

## 例子

```
y=6 4 7
// output
[6,4,7]

x=y;
x;
// output
[6,4,7]
y[1]=0;
// output
[6,0,7]
x;
// output
[6,4,7]
//修改y不影响x

const a=10;
```

释放对象： <variable>=NULL 或使用 undef 命令。在某些情况下，我们想要从系统内存中释放一些变量来减少程序的内存使用量。

```
x=6 4 7;
x;
// output
[6,4,7]
x=NULL;
x;
// output
NULL

x=6 4 7;
undef(`x, VAR);
x;
// output
Syntax Error: [line #1] Cannot recognize the token x
```

除了基本的赋值方式(=)，DolphinDB还支持以下扩展的赋值方式：+=, -=, \*=, /=和=，例如：

```
x=0;
x+=5;
x;
// output
5
// 等同于 x = x + 5

x=5;
x-=2;
x;
// output
3
// 等同于 x = x - 2

x=5
x*=5;
x;
// output
25
// 等同于 x = x * 5

x=5;
x/=2;
x;
// output
2
// 等同于 x = x / 5. 注意：/表示整除。

x=5;
x\=2;
x;
// output
2.5

x=1 2 3 4 5;
x[1 3]+=10;
// 将10同时加到x[1]和x[3]上
x;
// output
[1,12,3,14,5]
```
