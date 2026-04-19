<!-- Auto-mirrored from upstream `documentation-main/progr/operators/sub.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# sub(-)

## 语法

`X - Y`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量、矩阵或集合。当X和Y都是向量或矩阵时，它们的长度必须相同。

## 详情

返回X和Y逐个元素相减的结果。如果X和Y都是集合，则sub返回X减去X和Y的交集的结果。

## 例子

```
4:5-2;
// output
2 : 3

4:5-1:2;
// output
3 : 3

x=1 2 3;
x-1;
// output
[0,1,2]

1 sub x;
// output
[0,-1,-2]

y=4 5 6;
sub(x,y);
// output
[-3,-3,-3]

m1=1..6$2:3;
m1;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 3 | 5 |
| 2 | 4 | 6 |

```
m-2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| -1 | 1 | 3 |
| 0 | 2 | 4 |

```
m2=6..1$2:3;
m2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 6 | 4 | 2 |
| 5 | 3 | 1 |

```
m1-m2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| -5 | -1 | 3 |
| -3 | 1 | 5 |

```
x=set([5,3,4]);
y=set(8 9 4 6);
x-y;
// output
set(3,5)
y-x;
// output
set(6,9,8)
```
