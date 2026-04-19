<!-- Auto-mirrored from upstream `documentation-main/progr/named_func.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 命名函数

一个函数含有一组语句，调用该函数时，将执行该组语句。通常函数返回一个或多个值。在 DolphinDB 中，系统内置函数不允许被改变定义。

内置函数与用户自定义函数均支持指定默认参数值。需要注意的是，默认值必须为常量，且可变参数（ mutable
类型）不支持指定默认值。如果一个参数设置了默认值，后续参数都必须设置默认值。注意：若在嵌套函数中使用 mutable
修饰外层函数的某个参数，那么所有内层需要调用该参数的函数也必须使用 mutable 修饰该参数，否则在多线程情况下可能会出现报错：`Read only
object can't be applied to mutable function xxx`。

## 语法

`def <functionName> ([parameters])
{statements}`

或

`def <functionName> ([parameters]):
statement`

注：

第二种用法中只能使用一个 statement。

我们将在本节末尾提及用户自定义聚合函数，其语法和命名函数基本一致，区别在于用户自定义聚合函数是以 **defg** 开头，而不是 **def**。

## 函数参数

* 函数参数通过引用传递。
* 当输入参数没有限定符时，在函数体中则不能修改该参数。
* 当参数用 mutable 修饰时，在函数体中可以修改该参数。

## 例子

定义一个命名函数：

```
def f(a){return a+1};
f(2);
// output
3

def f(a):a+1;
f(3);
// output
4
def f(a=1, b=2){return a + b}
f(,3)
// output
4
```

将一个函数或者一组函数赋给变量：

```
g=sin;
g(3.1415926);
// output
5.358979e-008

g=[sin, cos, log];
g(1 2);
```

| sin | cos | log |
| --- | --- | --- |
| 0.841471 | 0.540302 | 0 |
| 0.909297 | -0.416147 | 0.693147 |

```
//当一个函数和一个变量名字相同时，可以使用&来表示函数。
sum=15;
g=sum;
g;
// output
15

g=&sum;
g;
// output
sum

g(1..4);
// output
10
```

不可变参数在函数体中不能被修改。

```
def f(a){a+=1; return a};
// output
Syntax Error: [line #1] Constant variable [a] can't be modified.
```

可变参数在函数体中可以被修改。

```
def f(mutable a){a+=1; return a};
x=1;
f(x);
// output
2

f(x);
// output
3

x;
// output
3

x=1..6$3:2;
x;
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
def f(mutable a){if(a.rows()>=2 && a.cols()>=2){a[1,1]=0}; return a};
f(x);
```

| #0 | #1 |
| --- | --- |
| 1 | 4 |
| 2 | 0 |
| 3 | 6 |

先声明函数再定义。

```
def f2(a,b)
def f1(a,b){return f2(a,b)}
def f2(a,b){a pow b};
// 这里在各行之间不应该添加";" ，否则系统会由于没有看到定义而无法识别出 f2 是一个声明。
f1(2,3);
// output
8
```

多个返回值：

```
def summary(a){return sum(a), avg(a), std(a)};
x=1..11;
summary(x);
// output
[66, 6, 3.316625]
```

## 更复杂的例子：

我们写一个函数，计算相同长度的向量之间的协方差。

(1) 如果 a 和 b 都不含有 NULL 元素，计算协方差。

(2) 如果 a 或 b 含有 NULL 元素，首先取得不含 NULL 元素的子向量，然后再计算协方差。

```
def calcovar(a, b){
    aNull=hasNull a;                                                 // 如果输入向量含有 NULL 值，返回 true；否则返回 false
    bNull=hasNull b;
    if(!aNull && !bNull){                                            // 如果 a 和 b 都不含 null 值
            am=avg a;                                                // 使用 avg 函数计算向量 a 的均值
            bm=avg b;                                                // 使用 avg 函数计算向量 b 的均值
            ab=a ** b;                                               // 计算向量 a 和 b 的内积
            n=count a;                                               // 取得非 null 值数
            return (ab-n*am*bm) \ (n-1);                             // 返回协方差
   }
        else{                                                         // 取得 a, b 中所有不为 null 值的元素位置
               if(!aNull)                                             // 如果 a 不包含任何 null 值
                       index=!isNull b;                               // 取得所有 b 中非 null 值的下标
                   else {
                           if(!bNull)                                  // 如果 b 不包含任何 null 值
                               index=!isNull a;                        // 取得所有 a 中非 null 值的下标
                           else
                               index=!((isNull a) || (isNull b));      // 取得所有 a 和 b 中同时为非 null 值的下标
                           }
                    c=a[index];
                    d=b[index];
                    am=avg c;
        bm=avg d;
        ab=c ** d;
        n=count c;
        return (ab-n*am*bm) \ (n-1);
      }
}
```

## 用户自定义聚合函数

用户自定义聚合函数返回的数据格式为标量。有时候我们想确保一个函数返回的是一个标量，使用聚合函数就可以达到这个目的。

用户自定义聚合函数和命名函数语法基本一致，不同之处在于用户自定义聚合函数的定义以 "defg" 开头而不是 "def"。

```
defg f(x, y){
    a = sum(abs(x+y))
    b=sum(abs(x))+sum(abs(y))
    return a\b
};
x=-5..5; y=0..10;
f(x,y);
// output
0.858824
```

有关自定义聚合函数的详细用法，参考：自定义聚合函数。
