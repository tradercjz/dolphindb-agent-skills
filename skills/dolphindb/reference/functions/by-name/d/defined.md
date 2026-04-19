# defined

## 语法

`defined(names, [type=VAR])`

## 详情

查询 *names* 中的每个元素是否已被定义。根据 *type* 参数的不同，可以检查本地变量、共享变量或函数定义。

## 参数

**names** 可以是字符串标量或向量，表示对象名。

**type** 可为 VAR（本地变量），SHARED（共享变量）或 DEF（函数定义）。默认值为 VAR。

## 返回值

返回一个布尔类型标量/向量，“true”表示已被定义，“false”表示未被定义。

## 例子

```
x=10
y=20
def f(a){return a+1}
share table(1..3 as x, 4..6 as y) as t1;

defined(["x","y","f",`t1]);
// output
[true,true,false,false]

defined(["x","y","f",`t1], DEF);
// output
[false,false,true,false]

defined(["x","y","f",`t1], SHARED);
// output
[false,false,false,true]
```
