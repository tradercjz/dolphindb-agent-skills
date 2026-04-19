# rowCovarp

首发版本：3.00.5

## 语法

`rowCovarp(X, Y)`

row 系列函数通用参数说明和计算规则请参考：rowFunctions

## 详情

逐行计算 *X* 和 *Y* 之间的总体协方差。

## 返回值

返回一个长度与输入参数行数相同的向量。

## 例子

```
m1=matrix(2 8 9 12, 9 14 11 8,-3 NULL NULL 9)
m2=matrix(11.2 3 5 9, 7 -10 8 5,17 12 18 9)
rowCovarp(m1, m2)
// output: [-19.82,-19.5,1.5,2.22]

a= 110 112.3 44 98
b= 57.9 39 75 90
c= 55 64 37 78
x=array(DOUBLE[],0, 10).append!([a, b, c])
y=array(DOUBLE[],0, 10).append!([b, a, c])

rowCovarp(x, y)
// output: [-245.96,-245.96,221.25]
```

相关函数：covarp
