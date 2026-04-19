# shapiroTest

## 语法

`shapiroTest(X)`

## 详情

对样本数据进行 Shapiro-Wilk 检验。

## 参数

**X** 是一个数值向量，表示样本。

## 返回值

一个字典，包含以下 key：

* method ：字符串 "Shapiro-Wilk normality test"
* pValue ：p 值
* W ：W 统计量

## 例子

```
x = norm(0.0, 1.0, 50)
shapiroTest(x);

// output
method->Shapiro-Wilk normality test
pValue->0.621668
W->0.981612
```
