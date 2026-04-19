<!-- Auto-mirrored from upstream `documentation-main/progr/objs/func_call.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 函数

函数是完成特定任务的独立代码模块，包括内置函数和用户定义的函数。

## 函数定义

要定义一个函数，可以使用关键字 "def"。详情请参考 函数化编程。内置函数与用户自定义函数均支持指定默认参数值。需要注意的是，默认值必须为常量，且可变参数（mutable
类型）不支持指定默认值。如果一个参数设置了默认值，后续参数都必须设置默认值。注意：若在嵌套函数中使用 mutable
修饰外层函数的某个参数，那么所有内层需要调用该参数的函数也必须使用 mutable 修饰该参数，否则在多线程情况下可能会出现报错：`Read only
object can't be applied to mutable function xxx`。

```
//用户自定义函数
def f(a):a*a;
f(5);
// output
25

def f(a=1, b=2){return a + b}
f(b=3, a=2)
// output
5

f(,3)
// output
4
```

## 函数调用

所有函数的参数通过引用进行传递。默认所有参数都是不可修改，除非另有显式声明。

通常函数的语法可以采用以下3种形式：

* 标准函数调用格式：<func>(parameters)。
* 调用对象方法格式：x.<func>(parameters)，其中 x 是第一个参数。
* 如果括号内只有一个参数，也可使用 <func> 参数，或者 x.<func>()。

请注意，当调用包含多个参数的函数时，传参时如果一个参数指定了 keyword，其后的参数也必须指定 keyword。

## 例子

```
x=1..10;
sum(x);
// output
55
x.sum();
// output
55
sum x;
// output
55

x=2;
y=3;
add(x,y);
// output
5
x.add(y);
// output
5
x add y;
// output
5
```

参数的值默认不可修改：

```
x=1..10;
add(x,1);
// output
[2,3,4,5,6,7,8,9,10,11]
x;
// output
[1,2,3,4,5,6,7,8,9,10]

def f(x){x+=1 return x};
// output
Syntax Error: [line #1] Constant variable [x] can't be modified.
```

使用 mutable 声明可变参数：

```
x=1..10;
def f(mutable x){x+=1 return x};
f(x);
x;
// output
[2,3,4,5,6,7,8,9,10,11]        // 更改向量 x 的值。
```

DolphinDB 提供1000多个内置函数，其中包括绝大多数常用的计算函数如:

* avg
* sum
* log
* add
* sub
* prod

```
avg(1.5 2.5 2 2);
// output
2

log(10);
// output
2.302585

prod(1 2 3)
// output
6
```
