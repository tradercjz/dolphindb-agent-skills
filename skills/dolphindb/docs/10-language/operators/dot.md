<!-- Auto-mirrored from upstream `documentation-main/progr/operators/dot.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# dot(\*\*)

## 语法

`X ** Y`

## 参数

**X** 和 **Y**
是可以标量、向量或矩阵。如果X和Y都是向量，则它们的长度必须相同。如果其中一个参数是矩阵，则另一个参数是向量或矩阵，并且它们的维数必须满足矩阵乘法的规则。

## 详情

返回X和Y的矩阵乘法结果。如果X和Y是相同长度的向量，则返回其内积。

## 例子

```
x=1..6$2:3;
y=1 2 3;
x dot y;
```

| #0 |
| --- |
| 22 |
| 28 |

```
x=1..6$2:3;
y=6..1$3:2;
x**y;
```

| #0 | #1 |
| --- | --- |
| 41 | 14 |
| 56 | 20 |

```
y**x;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 12 | 30 | 48 |
| 9 | 23 | 37 |
| 6 | 16 | 26 |

```
z=1 2 3;
shape z;
// output
3:1
x**z;
// 矩阵和向量乘法
```

| #0 |
| --- |
| 22 |
| 28 |

```
x=1 2 3;
y=4 5 6;
x ** y;
// output
32
// 两个向量的内积. 相当于 1*4 + 2*5 + 3*6

x ** 2;
// output
[2,4,6]

x=1..6$2:3
x ** 2;
// output
Use * rather than ** for scalar and matrix multiplication.
```
