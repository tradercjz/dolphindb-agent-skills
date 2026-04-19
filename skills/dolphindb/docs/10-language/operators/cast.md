<!-- Auto-mirrored from upstream `documentation-main/progr/operators/cast.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# cast($)

## 语法

`X $ Y`

## 参数

* **X** 可以是任何数据形式。
* **Y** 是数据类型或数据对。

## 详情

* 将数据类型转换为另一个数据类型
* 变换矩阵，或在矩阵和向量之间转换

## 例子

```
x=8.9$INT;
x;

9

x=1..10;
x;

[1,2,3,4,5,6,7,8,9,10]
typestr x;

FAST INT VECTOR
x/2;

[0,1,1,2,2,3,3,4,4,5]
x=x$DOUBLE;
typestr x;

FAST DOUBLE VECTOR
x/2;

[0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]

x=`IBM`MS;
typestr x;

STRING VECTOR
x=x$SYMBOL;
typestr x;

FAST SYMBOL VECTOR

x=`128.9;
typestr x;

STRING
x=x$INT;
x;

128
typestr x;

INT

// 把一个向量转换为矩阵
m=1..8$2:4;
m;
```

| #0 | #1 | #2 | #3 |
| --- | --- | --- | --- |
| 1 | 3 | 5 | 7 |
| 2 | 4 | 6 | 8 |

```
// 重新排列矩阵
m$4:2;
```

| #0 | #1 |
| --- | --- |
| 1 | 5 |
| 2 | 6 |
| 3 | 7 |
| 4 | 8 |

```
m$1:size(m);
```

| #0 | #1 | #2 | #3 | #4 | #5 | #6 | #7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
