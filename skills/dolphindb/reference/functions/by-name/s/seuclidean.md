# seuclidean

首发版本：3.00.5，3.00.4.3

## 语法

```
seuclidean(X, Y, Z)
```

## 详情

计算两个数值向量（X 和 Y）之间的标准化欧式距离，先将 X 和 Y 分别标准化处理后，再调用 euclidean。公式定义如下：

![](../../images/seuclidean.png)

## 参数

**X** 数值向量。

**Y** 数值向量。

**Z** 数值向量，表示各维度的方差，用于标准化。

注：

*X*
、*Y*、*Z* 三者的长度必须相等。

## 返回值

DOUBLE 类型标量。

## 例子

```
X = [2, 5]
Y = [3, 7]
Z = [1, 2]

seuclidean(X, Y, Z)
// 输出：1.7320508075688772
```

**相关函数**

euclidean、minkowski、mahalanobis
