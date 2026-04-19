# randWeibull

## 语法

`randWeibull(alpha, beta, count)`

## 详情

生成指定个数的 Weibull 分布随机数。

## 参数

形状参数 **alpha** 和 **beta** 都是正数。

**count** 是正整数，表示生成的随机数个数。

## 返回值

长度为 *count* 的 DOUBLE 类型向量。

## 例子

```
randWeibull(2.31,0.61, 2);

// output
[0.524197, 0.51402]
```
