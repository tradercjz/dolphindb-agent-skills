# randBinomial

## 语法

`randBinomial(trials, p, count)`

## 详情

生成指定个数的二项分布随机数。

## 参数

**trials** 是正整数。

**p** 是0到1之间的浮点数。

**trials** 和 **p** 是形状参数。

**count** 是正整数，表示生成的随机数个数。

## 返回值

长度为 *count* 的 DOUBLE 类型向量。

## 例子

```
randBinomial(2, 0.627, 2);
// output
[1, 1]
```
