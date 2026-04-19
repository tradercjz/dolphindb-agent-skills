# mahalanobis

首发版本：3.00.5，3.00.4.3

## 语法

```
mahalanobis(X, Y, Z)
```

## 详情

计算两个数值向量（X 和 Y）之间的马氏距离，公式定义如下：

![](../../images/mahalanobis.png)

其中，*V* 是协方差矩阵，参数 *Z* 是 *V* 的逆。

## 参数

**X** 数值向量。

**Y** 数值向量。

**Z** 协方差矩阵的逆。

## 返回值

DOUBLE 类型标量。

## 例子

```
len = 50
X = array(DOUBLE, 0).append!(take([1.2, 3.9, 0.8], len))
Y = array(DOUBLE, 0).append!(take([5.6, 0.4, 2.7], len))
Z1 = diag(take(1, len))
Z = inverse(Z1)

mahalanobis(X, Y, Z)
//输出：24.395286429964294
```

**相关函数**

minkowski、seuclidean
