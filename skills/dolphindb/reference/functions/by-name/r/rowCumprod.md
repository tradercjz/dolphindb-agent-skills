# rowCumprod

## 语法

`rowCumprod(X)`

row 系列函数通用参数说明和计算规则请参考：rowFunctions

## 详情

逐行计算 *X* 元素的累积乘积。

## 返回值

返回一个数据类型与 *X* 相同的对象。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowCumprod(m)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 4.5 | 6.75 | 33.075 |
| 2.6 | 12.48 | 24.96 |
| 1.5 | 8.85 | 8.85 |

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8]);
rowCumprod(a)
// output
[[1,3,6],[4,9],[6,13,21]]

tp = [[1.3,2.5,2.3], [4.1,5.3,6.2]]
tp.setColumnarTuple!()
rowCumprod(tp)
// output
[[1.3,3.25,7.475],[4.1,21.73,134.726]]
```
