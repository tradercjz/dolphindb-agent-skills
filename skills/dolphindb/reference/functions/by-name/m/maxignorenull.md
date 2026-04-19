# maxIgnoreNull

## 语法

```
maxIgnoreNull(X, Y)
```

## 详情

一个二元标量函数，返回两个数（*X* 和 *Y*）中的最大值。

它与 `max` 作为二元标量函数区别在于对空值的处理：

* `max`：当配置项 *nullAsMinValueForComparison=*true
  时，空值被视为最小值进行比较；否则空值不参与比较，结果返回空值。
* `maxIgnoreNull`：不受配置项 *nullAsMinValueForComparison*
  的影响。返回 *X* 或 *Y* 中的非空值，或者如果两者都非空，返回最大值。

## 参数

**X** 和 **Y** 是数值型、LITERAL 或 TEMPORAL 型的标量/数据对/向量/矩阵。

## 返回值

* 当输入是标量时，返回标量。
* 当输入是向量时，返回向量（逐元素比较）。
* 当输入是矩阵时，返回矩阵（逐元素比较）。
* 当输入是数据对时，返回数据对。

## 例子

```
maxIgnoreNull(2,matrix(1  NULL 4,-1 4  0))
```

| #0 | #1 |
| --- | --- |
| 2 | 2 |
| 2 | 4 |
| 4 | 2 |

```
maxIgnoreNull(matrix(10 3 NULL, 1 7 4),matrix(1  NULL 4,-1 4  0))
```

| #0 | #1 |
| --- | --- |
| 10 | 1 |
| 3 | 7 |
| 4 | 4 |

使用 `reduce` 结合
`maxIgNoreNull`，计算元组中存储的同形状矩阵每个位置的最小值，忽略空值。

```
n1 = matrix(1 1 1, 5 5 5)
n2 = matrix(10 11 12, 0 NULL -5)
n3 = matrix(-1 1 NULL, -3 0 10)
reduce(maxIgnoreNull, [n1,n2,n3])
```

| #0 | #1 |
| --- | --- |
| 10 | 5 |
| 11 | 5 |
| 12 | 10 |

相关函数：max, minIgnoreNull
