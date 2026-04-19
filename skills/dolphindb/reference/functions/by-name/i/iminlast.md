# iminLast

## 语法

`iminLast(X)`

## 详情

返回最小元素的位置。如果有多个相同的最小值，返回右起第一个最小值的位置。与所有其它聚合函数一致，计算时忽略 NULL 值。

## 参数

**X** 可以是标量、向量、矩阵或表。

## 返回值

* 若 *X* 是标量或向量，返回一个整型标量。
* 若 *X* 为矩阵，返回一个向量。
* 若 *X* 为表，返回一个表。

## 例子

```
x = 1.2 2 NULL -1 6 -1
iminLast(x);
// output: 5

m=matrix(3 2 2 4 2, 1 4 2 1 3);
iminLast(m)
// output: [4,3]

t=table(3 2 2 as c1, 1 1 4 as c2)
iminLast(t)
/* output:
c1       c2
2	1
*/
```

相关函数：imin
