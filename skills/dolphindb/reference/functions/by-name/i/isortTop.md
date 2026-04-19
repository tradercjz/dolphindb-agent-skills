# isortTop

## 语法

`isortTop(X, top, [ascending=true])`

## 详情

返回 *X* 排序后前 *top* 个元素对应的索引。

## 参数

**X** 可以是一个向量或一个由多个等长向量组成的元组。

**top** 是一个正整数，它的值不能超过 *X* 的长度。

**ascending** 是一个布尔型的标量或向量，表示 *X* 按升序排序还是降序排序。它是可选参数，默认值为 true，表示按升序排序。

## 返回值

整型向量。

## 例子

```
isortTop(2 1 4 3 6 5, 3);
// output: [1,0,3]

isortTop(2 1 4 3 6 5, 3, false);
// output: [4,5,2]

x=1 1 2 2 3 3
y=1 2 1 2 1 2
isortTop([x,y], 3);
// output: [0,1,2]

x=1 1 2 2 3 3
y=1 2 1 2 1 2
isortTop([x,y], 3, [false, false]);
// 先基于 x 降序排序，对于 x 中相同的元素，再基于 y 降序排序后，取前3个元素对应的索引
// output: [5,4,3]
```
