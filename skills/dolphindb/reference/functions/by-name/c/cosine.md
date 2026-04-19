# cosine

首发版本：3.00.5，3.00.4.3

## 语法

`cosine(X, Y)`

## 详情

计算 *X* 和 *Y* 之间的余弦相似度，即 (X · Y) / (||X|| × ||Y||)。

注：

与 SciPy 的 scipy.spatial.distance.cosine
函数的功能类似，区别在于：

* DolphinDB 的 `cosine` 函数计算余弦相似度（值越大越相似），SciPy 的
  `scipy.spatial.distance.cosine` 计算余弦距离（值越小越相似），两者的关系是余弦距离
  = 1 - 余弦相似度。
* `cosine` 只接受参数 *X*、*Y*，不支持
  `scipy.spatial.distance.cosine` 中的权重参数参数 *w*。

## 参数

**X** 和 **Y** 是长度相同的数值型向量。

## 返回值

DOUBLE 类型标量，取值范围为 [-1, 1]。

## 例子

```
x = [1, 2, 3]
y = [4, 5, 6]
cosine(x, y);
// 输出：0.9746318
```

相关函数：euclidean、minkowski、seuclidean、mahalanobis
