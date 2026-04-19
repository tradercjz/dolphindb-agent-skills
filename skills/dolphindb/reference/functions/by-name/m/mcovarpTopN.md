# mcovarpTopN

首发版本：3.00.5

## 语法

`mcovarpTopN(X, Y, S, window, top, [ascending=true],
[tiesMethod='oldest'])`

参数说明和窗口计算规则请参考：mTopN

## 详情

在给定长度（以元素个数衡量）的滑动窗口内，根据 *ascending* 指定的排序方式将 *X* 和 *Y* 按照 *S*
进行稳定排序后，取前 *top* 个元素，然后计算 *Y* 和 *X* 的总体协方差。

## 返回值

计算结果为 DOUBLE 类型，形式同输入参数。

## 例子

```
x = NULL 3 8 4 0
y = 2 3 1 7 3
s = 5 NULL 8 9 4

mcovarpTopN(x, y, s, 3, 2)
// output: [ , , 0, -6, -4]

s2=2026.01.01 2026.02.03 2026.01.23 2026.04.06 2026.12.29
mcovarpTopN(x, y, s2, 3, 2)
// output: [ , 0, 0, -2.5, -6]

x1 = matrix(x, 4 3 6 2 3)
y1=matrix(3 7 9 3 2, y)
s1=matrix(2 3 1 7 3, s)

mcovarpTopN(x, y1, s1, 3, 2)
```

| 0 | 1 |
| --- | --- |
|  |  |
| 0 |  |
| 0 | 0 |
| 2.5 | -6 |
| 14 | -4 |

```
mcovarpTopN(x1, y1, s, 3, 2)
```

| 0 | 1 |
| --- | --- |
|  | 0 |
|  | 0 |
| 0 | -0.5 |
| 6 | -6 |
| 14 | -1.5 |

```
mcovarpTopN(x1, y1, s1, 3, 2)
```

| 0 | 1 |
| --- | --- |
|  | 0 |
| 0 | 0 |
| 0 | -0.5 |
| 2.5 | -6 |
| 14 | -1.5 |

相关函数：covarp
