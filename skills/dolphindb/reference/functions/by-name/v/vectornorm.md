# vectorNorm

## 语法

`vectorNorm(x, [ord], [axis], [keepDims])`

## 详情

计算矩阵/向量的范数。

注意：该函数在 SQL 中的行为未定义，故不建议在 SQL 中使用。

## 参数

**x** 传入除 DECIMAL 以外数值类型的向量或矩阵。注意：不可为空。

**ord** 可选参数，整数、浮点数或者字符串类型的标量，用来指定计算的范数类型。注意：

* *ord* 是字符串时，必须是 inf, -inf, nuc, fro 中的一个。
* *ord* 小于 1 时，本函数的计算结果不符合严格数学意义上的“范数”，但对其他计算可能仍然有意义。

如下为传入不同参数 *x* 和 *ord* 时，计算范数的方式说明：

| *ord* | *x* 为向量 | *x* 为矩阵 |
| --- | --- | --- |
| 不传入 | 2-norm | Frobenius norm |
| 0 | sum(x != 0) | 不支持计算 |
| -1 | sum(abs(x)^ord)^(1/ord) | min(sum(abs(x), axis=0)) |
| 1 | sum(abs(x)^ord)^(1/ord) | max(sum(abs(x), axis=0)) |
| -2 | sum(abs(x)^ord)^(1/ord) | 2-norm (largest sing. value) |
| 2 | sum(abs(x)^ord)^(1/ord) | smallest singular value |
| 其他整数或浮点数 | sum(abs(x)^ord)^(1/ord) | 不支持计算 |
| inf | max(abs(x)) | max(sum(abs(x), axis=1)) |
| -inf | min(abs(x)) | min(sum(abs(x), axis=1)) |
| nuc | 不支持计算 | nuclear norm |
| fro | 不支持计算 | Frobenius norm |

**axis** 可选参数，整型向量或标量，表示求范数的方向。注意：不可包含空元素。

* 当 *x* 为向量时，*axis* 只能传入标量 0。
* 当 *x* 为矩阵时，*axis*：

  + 长度不能超过 2。
  + 元素不能重复。
  + 元素值的大小不能超过 1，即只能为 0 或 1。

**keepDims** 可选参数，布尔标量，表示返回结果是否和 *x* 的形式保持一致，默认为 false。

## 返回值

返回值的类型和形式由参数共同决定，可能为 INT 、LONG 或 DOUBLE 类型的标量、向量或矩阵。

## 例子

若 *x* 为向量，计算传入不同参数后的范数。

```
x = 1..4

vectorNorm(x) //Output: 5.477225575051661

vectorNorm(x, keepDims=true) //Output: 5.477225575051661

vectorNorm(x, ord=1) //Output: 10
vectorNorm(x, ord=1, axis=0) //Output: 10

vectorNorm(x, ord=-1) //Output 0.4800000000000001
vectorNorm(x, ord=-1, axis=0) //Output double: 10

vectorNorm(x, ord="inf", axis=0) //Output: 4
vectorNorm(x, ord="-inf", axis=0) //Output: 1

vectorNorm(x, ord=3) //Output: 4.641588833612778
vectorNorm(x, ord=-20.689) //Output: 0.9999999714010688

vectorNorm(x, ord="fro") // throw exception
vectorNorm(x, ord="nuc") // throw exception
```

若 *x* 为矩阵，计算传入不同参数后的范数。

```
x = 1..4$2:2

vectorNorm(x) //Output: 5.477225575051661
vectorNorm(x, keepDims=true) //Output: 5.477225575051661

vectorNorm(x, ord=1) //Output: 7
vectorNorm(x, ord=1, axis=0) //Output: 3 7
vectorNorm(x, ord=1, axis=1) //Output: 4 6

vectorNorm(x, ord=-1, axis=0) //Output: 0.6666666666666666 1.7142857142857144
vectorNorm(x, ord=-1, axis=1) //Output: 0.75 1.3333333333333333

vectorNorm(x, ord=1, axis=(0 1)) //Output: 7
vectorNorm(x, ord=1, axis=(1 0)) //Output: 6

vectorNorm(x, ord=-1, axis=(0 1)) //Output: 3
vectorNorm(x, ord=-1, axis=(1 0)) //Output: 4

vectorNorm(x, ord="inf", axis=(0 1)) //Output: 4
vectorNorm(x, ord="inf", axis=(1 0)) //Output: 3

vectorNorm(x, ord="-inf", axis=(0 1)) //Output: 6
vectorNorm(x, ord="-inf", axis=(1 0)) //Output: 7

vectorNorm(x, ord="fro", axis=(1 0)) //Output: 5.477225575051661
vectorNorm(x, ord="fro", axis=(0 1)) //Output: 5.477225575051661

vectorNorm(x, ord=-2, axis=(1 0)) //Output: 0.3659661906262574
vectorNorm(x, ord=-2, axis=(0 1)) //Output: 0.3659661906262574

vectorNorm(x, ord=2, axis=(1 0)) //Output: 5.464985704219043
vectorNorm(x, ord=2, axis=(0 1)) //Output: 5.464985704219043

vectorNorm(x, ord="nuc", axis=(1 0)) //Output: 5.8309518948453
vectorNorm(x, ord="nuc", axis=(0 1)) //Output: 5.8309518948453

vectorNorm(x, ord=3) // throw exception
```
