<!-- Auto-mirrored from upstream `documentation-main/progr/operators/chainingComparison.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 链式比较

## 语法

<, <=, >, >=, ==, !=, <>可以在同一行里使用。

## 参数

参数可以是标量、数据对、向量、矩阵或集合。当 **X** 和 **Y** 都是向量或矩阵时，它们的长度或维度必须相同。

## 例子

```
1<2<=3.5;
// output
1

NULL<1<3>=2<3!=1>=NULL;
// output
1

1<3>1==2<3!=1;
// output
0

1 2 3 >=2 ==1 2 3;
// output
[0,1,0]

1 2 3 <= 3 2 2 > 2 1 2;
// output
[1,1,0]
```
