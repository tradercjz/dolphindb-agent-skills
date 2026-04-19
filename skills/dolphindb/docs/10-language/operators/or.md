<!-- Auto-mirrored from upstream `documentation-main/progr/operators/or.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# or(||)

## 语法

`X || Y`

## 参数

**X** 和 **Y** 可以是标量、数据对、向量或矩阵。当X和Y都是向量或矩阵时，它们的长度必须相同。

## 详情

返回X和Y中每一个元素逻辑或(||)的结果。若操作数包含 NULL，则返回的对应结果也是 NULL。

## 例子

```
1 || 0;
// output
1

x=1 0 1;
x || 0;
// output
[1,0,1]

y=0 1 0;
x or y;
// output
[1,1,1]

m1=1 1 1 0 0 0$2:3;
m1;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 1 | 0 |
| 1 | 0 | 0 |

```
m1 || 0;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 1 | 0 |
| 1 | 0 | 0 |

```
m2=1 0 1 0 1 0$2:3;
m2;
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 1 | 1 |
| 0 | 0 | 0 |

```
or(m1, m2);
```

| #0 | #1 | #2 |
| --- | --- | --- |
| 1 | 1 | 1 |
| 1 | 0 | 0 |

```
t=table(1..3 as id, 4..6 as value);
t;
```

| id | value |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
select id, value from t where id=2 or id=3;
```

| id | value |
| --- | --- |
| 2 | 5 |
| 3 | 6 |
