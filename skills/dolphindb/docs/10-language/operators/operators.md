<!-- Auto-mirrored from upstream `documentation-main/progr/operators/operators.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 运算符

运算符是表达式的两个基本构建元素之一（另一个基本元素是上一章讨论的对象）。作用于单个对象的运算符称为一元运算符；作用于两个对象的运算符被称为二元运算符；作用于三个对象的运算符被称为三元运算符。DolphinDB支持许多类型的基本运算符，包括算术运算符、布尔运算符、关系运算符、成员运算符等。此外，所有具有一个\两个、或三个参数的内置函数或用户定义函数，都可以写成一元、两元、或三元运算符的形式。

## 运算符一览

| 名字 | 运算符 | 例子 | 优先级 | 元数 | 运算数据类型 |
| --- | --- | --- | --- | --- | --- |
| or | || | 1||0; [2,3]|| [4,5]; 0||[4,5] | 1 | binary | A, V, S, M |
| and | && | 1&&0; [2,3]&&[4,5]; | 2 | binary | A, V, S, M |
| lt | < | 1<2; [2,3]<[4,5]; 2<[4,5]; 2<4 5 | 3 | binary | A, V, S, M |
| le | <= | 1<=2; [2,3]<=[4,5]; 2<=[4,5]; 2<4 5 | 3 | binary | A, V, S, M |
| equal | == | 1==2; [2,3]==[4,5];2==4 5 | 3 | binary | A, V, S, M |
| gt | > | 1>2; [2,3]>[4,5]; 2>4 5 | 3 | binary | A, V, S, M |
| ge | >= | 2>=1; [2,3]>=[4,5]; 2>=4 5 | 3 | binary | A, V, S, M |
| ne | != 或 <> | 1!=2; [2,3]!=[2,5]; 2!=4 5; 2<>5 | 3 | binary | A, V, S, M |
| bitOr (union) | | | 0 | 1 | 4 | binary | A, V, S, M |
| bitXor | ^ | 0 | 1 | 5 | binary | A, V, S, M |
| bitAnd (intersection) | & | 0 & 1 | 6 | binary | A, V, S, M |
| lshift | << | 1<<2 | 7 | binary | A, V, M |
| rshift | >> | 10>>2 | 7 | binary | A, V, M |
| add | + | 1+2; [1,2]+[3,4] | 8 | binary | A, V, S, M |
| sub | - | 1-2; [3,4]-[1,2]; 5-[3,4] | 8 | binary | A, V, S, M |
| mul | \* | 2\*3; [1,2]\*[3,4]; 3\*[4,5,6] | 10 | binary | A, V, S, M |
| dot | \*\* | [1,2]\*\*[3,4] | 10 | binary | V, M |
| div | / | 2/3; 2.0/3; [2,3,4]/2 | 10 | binary | A, V, M |
| ratio | \ | 1\2; [2,3,4]\2 | 10 | binary | A, V, M |
| mod | % | 1%2; [2,3,4]%2 | 10 | binary | A, V, M |
| cast | $ | 1..8$4:2; cast(1..8, 4:2); cast(1.1,`int) | 10 | binary | A, V, M |
| join | <- | 1 2 3 <- 4 | 10 | binary | A, V, M, T |
| pair | : | 1:3; | 15 | binary | A |
| seq | .. | 5..9, 9..5; | 15 | binary | A |
| not | ! | !0; ! 3 4 0; | 18 | unary | A, V, M |
| neg | - | -x; - 4 5 6; | 18 | unary | A, V, M |
| at | [] | x[0], x[3 5 6], x[2,3], x[1:2,4:3] | 20 | binary | V, M, T, D |
| member | . | x.price, d.2 | 20 | binary | T, D |
| function operator | () | x(1, 2) | 20 | binary | A, V |
| ternary operator | ? : | (1+1>2)?1:0 | 25 | ternary | A, V, S, M, D, T |

注：

在运算数据类型列中，符号A, V, S, M, D, T分别表示标量，向量，集合，矩阵，字典和表。

## 运算符使用示例

运算符用于连接表达式中的运算数。我们选择常用的符号来表示各种操作。为了方便记住运算符，我们给每个运算符定义一个名字。运算符的名称可以在任何表达式中使用。下面以"+"为例。

```
x=1;
y=2;

// 运算符 "+"
x+y;
// output
3

// 函数作为运算符
x add y;
// output
3

add(x,y);
// output
3

// 函数写成面向对象的形式
x.add(y);
// output
3
```

在调用用户定义函数时，函数也可以写成运算符的形式。这样的函数的参数值不能被修改。

```
def f(a, b){return a*a + b*b - 2*a*b};
3 f 4;
// output
1
```
