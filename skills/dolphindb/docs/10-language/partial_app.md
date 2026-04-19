<!-- Auto-mirrored from upstream `documentation-main/progr/partial_app.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 部分应用

部分应用是指固定一个函数的部分参数，产生一个参数较少的函数。

## 语法

`<functionName>{parameters}`

通过对象方法调用的方式生成部分应用：

`obj.method{parameters...}(newArgs...)` 等价于
`method{obj, parameters}`

`obj.{method{parameters...}}(newArgs...)` 等价于
`method{parameters...}(obj, newArgs...)`

其中，最后一个语法通过 {} 包裹 *method* 和
*parameters*，将它们组合并生成一个部分应用，将 *obj* 作为这个部分应用的第一个参数。

## 详情

使用位置参数时，如果只是想固定前几个参数，那么不需要指明剩余的参数；如果在已被固定的参数前有未固定参数，无论这些未固定参数是必须的还是可选的，都必须指明它们的位置。

使用关键字参数时，只需指明需要固定的参数即可。

生成部分应用时，可以使用常量 DFLT 将参数固定为默认值。特别注意当需要固定默认值为空值的可选参数时，应使用 DFLT 固定而非
NULL。而当需要固定默认值不为空值的可选参数时，可以使用默认值，也可以使用 DFLT。

部分应用可与对参数有特定要求的高阶函数配合使用。

## 例子

```
a=100
g=add{a*a};
g(8);
```

返回：10008

```
add{a*a}(88);
```

返回：10088

```
def f(a,b):a*exp(b)
g=f{10};  // g(b)==f(10,b)

g(0);
```

返回：10

```
g(1);
```

返回：27.182818

```
k=f{,1};  // k(a)==f(a,1)
k(10);
```

返回：27.182818

若已被固定的参数前面包含了可选参数，且没指明位置，则需要在调用部分应用函数时传入：

```
//计算矩阵 m 的奇异分解
m=matrix([[2,1,0],[1,3,1],[0,1,4],[1,2,3]]);
//svd 的语法为 svd(obj, [fullMatrices=true], [computeUV=true])，如下定义的 f1，因没有对可选参数 fullMatrices 进行固定，所以在执行 f1 时需要传入 fullMatrices，否则会报错
f1 = svd{m, computeUV=true}
f1(false)   //成功执行
f1()  //报错：The function [svd] expects 1 argument(s), but the actual number of arguments is: 0
```

以下例子介绍如何通过对象方法调用的方式，生成自定义函数
`myFunc`
的部分应用。

```
//自定义函数 myFunc
def myFunc(a,b,c){
    return a*10+b*5+c*2
}

a1=[1,2,3]
b1=5
c1=9

//固定第1个参数为 a1，生成2个参数的部分应用
a1.myFunc{}(c1,b1)  //等价于 myFunc{a1}(c1,b1)
```

输出：[65,75,85]

固定第1和第3个参数，生成只有1个参数的部分应用

```
b1.myFunc{,a1}(c1)  //等价于 myFunc{b1,,a1} (c1)
```

输出：[97,99,101]

固定第2个参数，生成部分应用 myFunc{,a1}(b1,c1)，参数将依次传入

```
b1.{myFunc{,a1}}(c1)    // 等价于 myFunc(b1,a1,c1)
```

输出：[73,78,83]

通过对象方法调用方式生成的部分应用与函数模式结合使用

```
a1.myFunc{b1}:E([4,5,6]) //等价于 each(a1.myFunc{b1},[4,5,6])
```

输出一个矩阵：

| 4 | 5 | 6 |
| --- | --- | --- |
| 43 | 45 | 47 |
| 53 | 55 | 57 |
| 63 | 65 | 67 |

通过 {} 将固定参数和函数包裹，*obj* 作为部分应用的第一个入参。这种方式通常和函数模式结合使用。下例通过函数模式
:V
实现数组向量按列计算倾斜度。

```
av = array(INT[],0,10).append!([2 6 6 9 3, 0 7 4 7 1, 4 2 4 8 7,0 9 8 9 7])
av.{skew{,false}}:V()　//等价于 skew{,false}:V(av)，也等价于 byColumn(skew{,false},av)
```

得到结果：[0.8545,-0.9406,0.8545,-0.8545,-0.3703]

如果不使用 {} 包裹，则 *obj* 将成为部分应用的第一个固定参数。下例中因为
`skew`
无法接受3个参数而出现报错：

```
av.skew{,false}:H() //等价于 skew{av,,false}:H()
// 抛出异常
```

内置函数 rank 的语法为`rank(X, [ascending=true], [groupNum], [ignoreNA=true],
[tiesMethod='min'], [percent=false], [precision])`

当需要固定参数 percent=true 时，可以使用位置参数：

```
f1 = rank{,,,,,true}
```

也可以使用关键字参数

```
f2 = rank{percent=true}
```

当需要固定参数 groupNum 为默认值时，须使用常量 DFLT

```
f3 = rank{groupNum=DFLT,percent=true}
```
