# histogram

首发版本：3.00.5，3.00.4.1，3.00.3.2

## 语法

`histogram(X, [bins=10], [range], [density=false], [weights])`

## 详情

计算数据样本的直方图。

## 参数

**X** 数值型向量，表示数据样本。

**bins** 可选参数，正整数，或严格单调递增的数值型向量：

* 正整数代表等宽的箱的个数，默认值为 10。
* 数值型向量代表箱的边界，包括最右侧边界。

**range** 可选参数，数据对或长度为 2 的向量，表示箱的上下界，超出范围的值会被忽略。默认值为 `[X.min(),
X.max()]`。

**density** 可选参数，布尔值：

* false（默认值），结果是每个箱中样本的计数。
* true，结果是归一化后概率密度函数在每个箱中的值。

**weights** 可选参数，长度与 *X* 相同的数值向量，表示样本的权重。注意，当 *density* 为 false
时，返回加权计数值。

## 返回值

一个字典，键值对包括：

* H：直方图的值，具体可参考参数 *density* 和 *weights*。
* edges：箱的边界数组。

## 例子

*bins* 可为整数标量。

```
X = [3,4,5,6,7,8,9]
bins = 3
histogram(X, bins)
/*
H->[2,2,3]
edges->[3,5,7,9]
*/
```

*bins* 可为数值向量。

```
X = [3,4,5,6,7,8,9]
bins = [3,6,9]
histogram(X, bins)
/*
H->[3,4]
edges->[3,6,9]
*/
```

*range* 限定范围。

```
X = [3,4,5,6,7,8,9]
bins = [3,6,9]
range = [4,8]
histogram(X, bins, range)
/*
H->[2,3]
edges->[3,6,9]
*/
```

若 *density* 为
true，返回概率密度函数在箱中的值。

```
X = [3,4,5,6,7,8,9]
bins = [3,6,9]
range = [4,8]
histogram(X, bins, range, true)
/*
H->[0.133333333333333,0.2]
edges->[3,6,9]
*/
```

*weights* 设置样本权重。

```
X = [3,4,5,6,7,8,9]
bins = [3,6,9]
weights = [2,2,5,5,1,2,3]
histogram(X, bins, , false, weights)
/*
H->[9,11]
edges->[3,6,9]
*/
```
