<!-- Auto-mirrored from upstream `documentation-main/progr/operators/precedence.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 运算优先级

DolphinDB
的运算符优先级顺序符合常识。经常使用的运算符的优先级与大多数编程语言相似。表达式中优先级最高的运算符首先被执行，具有相同优先级的运算符则按从左到右的顺序执行。

```
a=5;
3+a*a;
// output
28
// 相当于 3+(a*a)
```

```
3*a..10;
// output
[15,18,21,24,27,30]
// 相当于 3*(a..10)
```

在一元运算符的右侧使用二元运算符可能会产生歧义。例如，abs x-10 可以解释为 abs(x-10) 或
abs(x)-10。我们使用第一个解释，即一元运算符将整个表达式视为一个运算数。这里我们建议使用括号以避免歧义。

另外举个例子，avg sin abs -100..100 等同于 avg(sin(abs(-100..100)))。

```
avg sin abs -100..100;
// output
-0.001265
```

```
avg(sin(abs(-100..100)));
// output
-0.001265
```

```
sum 1 2 3 == 6;
// output
0
// 相当于 sum(1 2 3 == 6)
```

```
x = 10
sin(x) + cos(x);
// output
-1.383093
```

```
sin x + cos x;
// output
0.260799
// 相当于 sin(x+cos x)
```

```
x = 1 NULL 1;
y = NULL 1 1;
(isNull x) || (isNull y);
// output
[1,1,0]
```

```
isNull x || isNull y;
// output
[0,1,0]
// 相当于 isNull (x || (isNull y))
```

初级一元运算符 neg(-) 和 not(!)
是上述一元运算符规则的两个例外。当与其他二元运算符混合时，它们按照运算符表中设置的优先级顺序执行。

例如，-n..n 等同于 (-n)..n 因为运算符 neg 的优先级高于 seq。

```
n=5;
-n..n;
// output
[-5,-4,-3,-2,-1,0,1,2,3,4,5]
```

```
(-n)..n;
// output
[-5,-4,-3,-2,-1,0,1,2,3,4,5]
```

```
-(n..n);
// output
[-5]
```

```
x=1 2 3;
!x-1;
// output
[-1,-1,-1]
```

用户定义函数用作运算符时，它的优先级与乘法和除法的优先级一样。

```
def f1(x,y):x+y
2 add 3 sub 5 f1 5;
// output
-5
```
