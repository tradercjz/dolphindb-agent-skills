<!-- Auto-mirrored from upstream `documentation-main/progr/operators/neg.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# neg(-)

## 语法

`X`

## 参数

**X** 可以是标量、数据对、向量或矩阵。

## 详情

返回X的负数。

## 例子

```
x=1:2;
-x;
// output
-1 : -2

x=1 0 1;
-x;
// output
[-1,0,-1]

m=1 1 1 0 0 0 $ 2:3;
m;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 1 | 0 |
| 1 | 0 | 0 |

```
-m;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| -1 | -1 | 0 |
| -1 | 0 | 0 |
