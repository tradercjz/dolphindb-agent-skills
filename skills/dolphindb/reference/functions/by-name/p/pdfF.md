# pdfF

## 语法

`pdfF(numeratorDF, denominatorDF, X)`

## 详情

计算指定 F 分布在 X 处的概率密度。

其功能和用法同 scipy.stats.f.pdf 。

## 参数

**numeratorDF** 数值型标量，代表分子自由度。

**denominatorDF** 数值型标量，代表分母自由度。

**X** 数值型标量或向量，代表要计算概率密度的点。

## 返回值

DOUBLE 类型标量或向量，表示在 *X* 处计算的概率密度。

## 例子

```
pdfF(numeratorDF=2, denominatorDF=19, X=[1,2,3])
// output: [0.34963122778983, 0.134514942963846, 0.056045754350634]
```
