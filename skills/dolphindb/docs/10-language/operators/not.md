<!-- Auto-mirrored from upstream `documentation-main/progr/operators/not.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# not(!)

## 语法

`!(X)`

## 参数

**X** 可以是标量、数据对、向量或矩阵。

## 详情

返回X的逻辑非运算结果。返回值为0，1或NULL。 0的NOT为1；NULL的NOT仍为NULL；所有其他值的NOT为0。

## 例子

```
!1.5;
// output
0

not 0;
// output
1

x=1 0 2;
not x;
// output
[0,1,0]

m=1 1 1 1 1 0 0 0 0 0$2:5;
m;
```

| #0 | #1 | #2 | #3 | #4 |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 | 0 |

```
not m;
```

| #0 | #1 | #2 | #3 | #4 |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 1 | 1 | 1 |

```
(1).not();
// output
0

(!NULL)==NULL;
// output
1
```

not 运算符支持与 SQL 中的谓词搭配使用，如：not in, not between, not exists 等。

```
t = table(`a`a`b`c`b as sym, 3.1 2.2 3.3 2.8 3.0 as val)
select * from t where sym not in `a`c
```

| sym | val |
| --- | --- |
| b | 3.3 |
| b | 3 |

相关函数: and, or
