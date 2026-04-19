# imaxLast

## 语法

`imaxLast(X)`

## 详情

返回最大值的位置。如果有多个相同的最大值，返回右起第一个最大值的位置。位置索引从 0 开始计数。空向量返回 -1。

## 参数

**X** 可以是标量、向量、矩阵或表。

## 返回值

* 若 *X* 是标量或向量，返回一个整型标量。
* 若 *X* 为矩阵，返回一个向量。
* 若 *X* 为表，返回一个表。

## 例子

```
x = 1.2 2 NULL -1 6 -1
imaxLast(x);
// output: 4

m=matrix(3 2 4 4 2, 1 4 2 4 3);
imaxLast(m)
// output: [3,3]

t=table(3 3 2 as c1, 1 4 4 as c2)
imaxLast(t)
/* output:
c1       c2
0	2
*/
```

相关函数：imax
