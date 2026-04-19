# cos

## 语法

`cos(X)`

## 详情

返回 *X* 的余弦。

注：

与 numpy.cos 函数的功能相同，区别在于 DolphinDB 的
`cos` 函数只接受一个参数 *X*，不支持 `numpy.cos` 中的
*out*、*where* 等参数。

## 参数

**X** 可以是标量、向量或矩阵。

## 返回值

DOUBLE 类型标量、向量或矩阵。

## 例子

```
cos 0 1 2;
// output
[1,0.540302,-0.416147]
```

相关函数：asin, acos, atan, sin, tan, asinh, acosh, atanh, sinh, cosh, tanh
