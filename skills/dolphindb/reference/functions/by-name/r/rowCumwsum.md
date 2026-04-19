# rowCumwsum

## 语法

`rowCumwsum(X, Y)`

row 系列函数通用参数说明和计算规则请参考：rowFunctions

## 详情

逐行计算 *X* 和 *Y* 的累积内积。

## 返回值

返回一个数据类型与 *X* 相同的对象。

## 例子

```
m1=matrix(2 -1 4, 8 3 2, 9 0 1)
m2=matrix(8 11 10, 8 17 4, 14 6 4)
rowCumwsum(m1, m2)
```

| col1 | col2 | col3 |
| --- | --- | --- |
| 16 | 80 | 206 |
| -11 | 40 | 40 |
| 40 | 48 | 52 |

```
a= -10 12.3 4 -8
b= 17.9 9 7.5 -4
c= 5.5 6.4 -7 8
x=array(DOUBLE[],0, 10).append!([a, b, c])
y=array(DOUBLE[],0, 10).append!([b, a, c])
rowCumwsum(x, y)
// output
[[-179,-68.30,-38.30,-6.29],[-179,-68.30,-38.30,-6.29],[30.25,71.21,120.21,184.21]]

tp1 = [[3,4,5],[4,5,6]]
tp1.setColumnarTuple!()

tp2 = [[13,41,25],[21,30,10]]
tp2.setColumnarTuple!()
rowCumwsum(tp1, tp2)
// output
[[39,203,328],[84,234,294]]
```
