# movingValid

首发版本：3.00.5

## 语法

`movingValid(func, funcArgs, window, [minPeriods], [combined=true])`

## 详情

按最近
*window*
个有效数据（非空值）构造滑动窗口，对每个窗口调用聚合函数
*func*
计算结果。每计算一次，滑动窗口向右移动一个元素。

若
*funcArgs*
包含数组向量或列式元组，则按展开后的数据序列，从本行最后一个元素起向左追溯，取最近
*window*
个有效数据参与计算。

## 参数

**func** 是一个聚合函数。

注：

使用该参数时，用于定义相应聚合函数的关键词为
**defg**。有关 **defg** 的详细用法，参考：自定义聚合函数。

**funcArgs**
是函数 func 的参数。可为向量、数组向量、列式元组、字典或矩阵。如果有多个参数，则用元组表示，并且每个参数的长度（向量/字典的元素个数）必须相同。当
*combined*
为 true 时，同一行中每个参数的元素个数必须相同。

**window**
是正整型，表示窗口内非空元素个数。

**minPeriods**
是一个正整数。为滑动窗口中最少包含的观测值数据。如果滑动窗口中的观测值小于
*minPeriods*
，那么该窗口的结果为 NULL 值。默认值与
*window*
相等。

**combined**
可选参数，是一个布尔值，表示在
*func*
为多参数时有效数据的判定方式：

* true（默认值）：展开后相同位置均为非空值的参数组合才被认定为有效数据。
* false：各参数独立追溯，分别取其最近的
  *window*
  个有效数据参与计算

## 返回值

一个向量，长度与输入参数的长度相同。

## 例子

例1. 计算一个向量的移动有效平均值，窗口长度为3。

```
x = 1 2 NULL 3 4 NULL NULL NULL 5 6
movingValid(func=avg, funcArgs=x, window=3, minPeriods=3)
// output:[,,,2,3,3,3,3,4,5]
```

例2. 根据数组向量列，计算每个时刻过去 3 个有效数据的因子值。

```
defg myFactor(x){
    return (max(x)-min(x))*2
}
timeCol = 09:30:00 + 1..13
value = arrayVector(3 4 5 6 9 11 12 15 16 17 18 21 23,9 1 15 NULL NULL NULL 16 18 4 1 11 NULL 2 14 8 NULL NULL NULL 15 9 16 18 10)
t = table(timeCol, value)
```

| timeCol | value |
| --- | --- |
| 09:30:01 | [9, 1, 15] |
| 09:30:02 | [null] |
| 09:30:03 | [null] |
| 09:30:04 | [null] |
| 09:30:05 | [16, 18, 4] |
| 09:30:06 | [1, 11] |
| 09:30:07 | [null] |
| 09:30:08 | [2, 14, 8] |
| 09:30:09 | [null] |
| 09:30:10 | [null] |
| 09:30:11 | [null] |
| 09:30:12 | [15, 9, 16] |
| 09:30:13 | [18, 10] |

```
select movingValid(myFactor,value,3,3) from t
```

movingValid\_myFactor --- 28 28 28 28 28 20 20 24 24 24 24 14 16

例3. 不同
*minPeriods*
对结果的影响：

```
val = 1 2 4 NULL 5 NULL 7 9 10
movingValid(func=min, funcArgs=val, window=3, minPeriods=3)
// output: [,,1,1,2,2,4,5,7]
movingValid(func=min, funcArgs=val, window=3, minPeriods=2)
// output: [,1,1,1,2,2,4,5,7]
```

例4. 多参数时不同有效数据的判定方式对结果的影响：

combined=true 时

```
x = arrayVector(2 5 6 8 10 12, 10 20 30 40 NULL NULL 50 NULL NULL 60 70 80)
y = arrayVector(2 5 6 8 10 12, 1 NULL 2 3 NULL 5 1 NULL 2 7 8 5)
movingValid(func=covar, funcArgs=[x,y], window=2, minPeriods=2, combined=true)
```

| x | [10, 20] | [30, 40, null] | [null] | [50, null] | [null, 60] | [70, 80] |
| --- | --- | --- | --- | --- | --- | --- |
| y | [1, null] | [2, 3, null] | [5] | [1, null] | [2, 7] | [8, 5] |
| 窗口计算 |  | covar([30,40], [2,3]) | covar([30,40], [2,3]) | covar([40,50], [3,1]) | covar([50,60],[1,7]) | covar([70,80],[8,5]) |
| 结果 | null | 5 | 5 | -10 | 30 | -15 |

combined=false 时

```
x = arrayVector(2 5 6 8 10 12, 10 20 30 40 NULL NULL 50 NULL NULL 60 70 80)
y = arrayVector(2 5 6 8 10 12, 1 NULL 2 3 NULL 5 1 NULL 2 7 8 5)
movingValid(func=covar, funcArgs=[x,y], window=2, minPeriods=2, combined=false)
```

| x | [10, 20] | [30, 40, null] | [null] | [50, null] | [null, 60] | [70, 80] |
| --- | --- | --- | --- | --- | --- | --- |
| y | [1, null] | [2, 3, null] | [5] | [1, null] | [2, 7] | [8, 5] |
| 窗口计算 |  | covar([30,40], [2,3]) | covar([30,40],[3,5]) | covar([40,50],[5,1]) | covar([50,60],[2,7]) | covar([70,80],[8,5]) |
| 结果 | null | 5 | 10 | -20 | 25 | -15 |
