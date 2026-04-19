# rowCummin

## 语法

`rowCummin(X)`

row 系列函数通用参数说明和计算规则请参考：rowFunctions

## 详情

逐行计算 *X* 元素的累积最小值。

## 返回值

返回一个数据类型与 *X* 相同的对象。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowCummin(m)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 4.5 | 1.5 | 1.5 |
| 2.6 | 2.6 | 2 |
| 1.5 | 1.5 | 1.5 |

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8]);
rowCummin(a)
// output
[[1,1,1],[4,4],[6,6,6]]

tp = [[1.3,2.5,2.3], [4.1,5.3,6.2]]
tp.setColumnarTuple!()
rowCummin(tp)
// output
[[1.3,1.3,1.3],[4.1,4.1,4.1]]
```
