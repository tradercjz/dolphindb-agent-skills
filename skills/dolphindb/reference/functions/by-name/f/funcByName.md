# funcByName

## 语法

`funcByName(name)`

## 详情

动态执行函数或运算符，主要用于元编程。

## 参数

**name** 是一个字符串，表示运算符或函数。函数可为内置函数或自定义函数。

## 返回值

FUNCTIONDEF 类型标量，表示函数定义。

## 例子

```
def f(x, a, b){
   return funcByName(x)(a, b)
}

f("+", 1 2 3, 4 5 6);
// output
[5,7,9]

f("sub", 1 8 3, 4 8 6);
// output
[-3,0,-3]

f("corr", 1 8 3, 4 8 6);
// output
0.970725

def cal(a,b){
   return pow(a\b,2)
}

f("cal", 4 8 10, 2 2 2);
// output
[4,16,25]

funcByName("call")(sum,1..10);
// output
55
```
