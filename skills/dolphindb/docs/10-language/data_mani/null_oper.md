<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/null_oper.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 空值操作

空值处理在数据分析中很常见。为达到最优性能，DolphinDB
对空值进行了优化处理。本章中，我们会解释如何表示、初始化和处理空值。我们还会讨论空值在普通向量函数、聚合函数以及高阶函数中的使用方法。

DolphinDB 内有两种类型的空值：VOID 类型空值和其它类型的空值（如int(), double(),
string(NULL)等）。通常，在赋值语句或表达式中使用无返回值的函数时，将会得到一个 VOID 类型的空值。通过函数 isVoid 判断是否为 VOID 类型的空值， 通过函数 isNull 和 isValid 可以检查所有空值，包括 VOID
和有类型的空值。对于不关心空值类型的用户，建议使用 isNull 或 isValid 进行条件判断。

从 版本开始，支持全部小写形式的 null。

```
typestr(NULL);
//output
VOID

isNull(null)
//output
true

def f(){
   1+2
}
typestr(f())
//output
VOID

typestr(int());
//output
INT

isVoid(NULL)
//output
true

isVoid(int())
//output
false

isNull(NULL)
//output
true

isNull(00i)
//output
true
```

不同类型的空值进行运算时，会将 VOID 类型的空值转换为对应的类型，再进行操作。

```
int()==NULL
//output
true

in(1 00f NULL 1.3, 00f) == [false, true, true, false]
//output
[true,true,true,true]
```
