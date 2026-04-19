# cosh

## 语法

`cosh(X)`

## 详情

返回 *X* 的双曲余弦。

注：

与 numpy.cosh 函数的功能相同，区别在于 DolphinDB 的
`cosh` 函数只接受一个参数 *X*，不支持 `numpy.cosh` 中的
*out*、*where* 等参数。

## 参数

**X** 可以是标量、向量或矩阵。

## 返回值

DOUBLE 类型标量、向量或矩阵。

## 例子

```
cosh 0 1 2;
// output
[1,1.543081,3.762196]
```

相关函数：asin, acos, atan, sin, cos, tan, asinh, acosh, atanh, sinh, tanh
