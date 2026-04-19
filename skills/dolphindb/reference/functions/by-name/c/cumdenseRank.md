# cumdenseRank

## 语法

`cumdenseRank(X, [ascending=true],
[ignoreNA=true], [percent=false], [norm='max'])`

## 详情

注：

* 该函数首发于1.30.22.3版本。
* 若要使用参数 *norm*，*percent* 应为 true

若 *X* 是向量，对 *X* 中的每一个元素，返回其在累计窗口内的密集排名。

* 基于 *ascending* 指定的方式排序。
* 如果 *ignoreNA* = true，则 NULL 值不参与排序，结果中 NULL 值的排名为空。

若 X 是矩阵或内存表，在每列内进行上述计算，返回一个与 *X* 维度相同的矩阵或内存表。

## 参数

**X** 可以是向量、矩阵或内存表。

**ascending** 是一个布尔值，表示是否按升序排序。默认值是 true。

**ignoreNA** 是一个布尔值，表示是否忽略 NULL 值，true 表示忽略 NULL 值，false 表示 NULL 作为最小值参与排名。默认值为
true。

**percent** 是一个布尔值，表示是否以百分比形式显示返回的排名，默认值为 false。

**norm** 是一个字符串，可为 'max' 或 'minmax' ，在计算百分比时，不同设置值决定了排名的起始值，进而可决定了百分比的计算结果。当
*norm*='max' 时，排名从1开始；当 *norm*='minmax' 时，排名从0开始。以返回 [3, 1, 2]
的密集排名百分比为例进行说明：

* 当 *norm*='max' 时，最后一个累计窗口中2的排名为2，窗口中的最大排名数为3，因此结果为2\3。
* 当 *norm*='minmax' 时，最后一个累计窗口中2的排名为1，窗口中的最大排名数为2，因此结果为1\2。

## 返回值

INT/DOUBLE 类型，其数据形式同 *X*。

## 例子

```
a = 1 3 2 3 4
cumdenseRank(X=a, ascending=true, ignoreNA=true, percent=false)
// output
[0,1,1,2,3]

cumdenseRank(X=a, ascending=true, ignoreNA=true, percent=true, norm="max")
// output
[1,1,0.6667,1,1]

cumdenseRank(X=a, ascending=true, ignoreNA=true, percent=true, norm="minmax")
// output
[1,1,0.5,1,1]

m = matrix(1 6 2 NULL, 3 0 1 6, 7 3 NULL 2)
cumdenseRank(X=m, ascending=true, ignoreNA=true, percent=false)
#0 #1 #2
-- -- --
0  0  0
1  0  0
1  1
   3  0

t = table([4,10,3,4,8,1] as val1, [10,8,1,8,5,2]  as val2)
cumdenseRank(X=t, ascending=true, ignoreNA=true, percent=false)
```

| val1 | val2 |
| --- | --- |
| 0 | 0 |
| 1 | 0 |
| 0 | 0 |
| 1 | 1 |
| 2 | 1 |
| 0 | 1 |
