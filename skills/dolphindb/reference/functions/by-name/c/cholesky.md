# cholesky

## 语法

`cholesky(obj, [lower=true])`

## 详情

对矩阵进行 Cholesky 分解。

注：

与 scipy.linalg.cholesky
函数的核心功能相同，区别如下：

* DolphinDB 中，`cholesky` 函数的 *lower* 参数默认值为 true；而
  `scipy.linalg.cholesky` 函数中 *lower* 参数默认值为
  false。
* DolphinDB 中， `cholesky` 函数不支持
  `scipy.linalg.cholesky` 函数中的 *overwrite\_a*
  和*check\_finite* 参数。

## 参数

**obj** 是一个对称正定矩阵。

**lower** 是一个布尔值，表示是否使用输入矩阵的下三角来计算分解。默认值为 true，表示使用下三角计算。如果 *lower* 为
false，表示使用上三角计算。

## 返回值

DOUBLE 类型矩阵。

## 例子

```
m=[1, 0, 1, 0, 2, 0, 1, 0, 3]$3:3
L=cholesky(m);
L;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 0 | 0 |
| 0 | 1.414214 | 0 |
| 1 | 0 | 1.414214 |

```
L**transpose(L);
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 0 | 1 |
| 0 | 2 | 0 |
| 1 | 0 | 3 |

```
cholesky(m, false);
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 0 | 1 |
| 0 | 1.414214 | 0 |
| 0 | 0 | 1.414214 |
