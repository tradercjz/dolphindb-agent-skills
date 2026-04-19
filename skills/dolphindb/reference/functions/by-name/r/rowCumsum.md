# rowCumsum

## 语法

`rowCumsum(X)`

row 系列函数通用参数说明和计算规则请参考：rowFunctions

## 详情

逐行计算 *X* 中元素的累计和。

## 返回值

返回一个数据类型与 *X* 相同的对象。

## 例子

```
m=matrix([4.5 2.6 1.5, 1.5 4.8 5.9, 4.9 2.0 NULL])
rowCumsum(m)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 4.5 | 6 | 10.9 |
| 2.6 | 7.4 | 9.4 |
| 1.5 | 7.4 | 7.4 |

```
a=array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8]);
rowCumsum(a)
// output
[[1,3,6],[4,9],[6,13,21]]

tp = [[1.3,2.5,2.3], [4.1,5.3,6.2]]
tp.setColumnarTuple!()
rowCumsum(tp)
// output
[[1.3,3.8,6.1],[4.1,9.4,15.6]]
```
