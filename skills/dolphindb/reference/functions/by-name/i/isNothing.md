# isNothing

## 语法

`isNothing(X)`

## 详情

`isNothing` 用于检查一个函数被调用时，函数的参数是否被传了值进来。

在 DolphinDB 中，Nothing 是 VOID 类型的两个特殊对象之一，用于表示“未传入参数”。

## 参数

**X** 可以是任何数据类型或形式。

## 返回值

布尔型标量或向量。

## 例子

```
f=def(x,y): isNothing(y);
f(5,);
// output: true

f(5, NULL);
// output: false
```
