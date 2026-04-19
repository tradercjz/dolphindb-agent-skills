<!-- Auto-mirrored from upstream `documentation-main/progr/objs/undef_var.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 取消变量

有时，我们需要取消一个变量或一个函数的定义，以便它可以在其他地方使用，或者节省内存。

## 语法

`undef(obj, [objType=VAR])`

或

`undef all`

## 参数

**obj** 是需要取消定义的对象名。如果想要取消所有变量、所有全局变量或所有用户自定义函数的定义，obj可以使用 "all"。

**objType** 需要取消定义的对象的类型。可以是以下取值之一：VAR（本地变量）,SHARED（共享变量） 或 DEF（函数定义）。默认值是VAR。

## 详情

释放变量或函数定义。

## 例子

```
undef all;

x=1
undef(`x, VAR);

x=1
y=2
undef(`x`y, VAR);

def f(a){return a+1}
undef(`f, DEF);
```

undef
函数是在代码运行阶段释放一个变量，而不是在代码解析阶段释放。
