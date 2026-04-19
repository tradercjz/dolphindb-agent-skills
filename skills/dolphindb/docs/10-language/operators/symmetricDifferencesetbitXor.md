<!-- Auto-mirrored from upstream `documentation-main/progr/operators/symmetricDifferencesetbitXor.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# symmetricDifference(set)/bitXor(^)

## 语法

* 集合运算：`X ^ Y`或`X symmetricDifference
  Y`或`symmetricDifference(X,Y)`
* 位运算： `X ^ Y`或`X bitXor Y`或`bitXor(X,
  Y)`

## 参数

* 集合运算： **X** 和 **Y** 是集合。
* 位运算： **X** 和 **Y** 是长度相同的向量，或 **Y** 是标量。

## 详情

* 集合运算：返回两个集合的并集减去交集后的集合。
* 位运算：返回异或运算的结果。

## 例子

```
// 对称差集
x=set([5,3,4]);
y=set(8 9 4 6);
y^x;
// output
set(5,8,3,9,6)
x^y;
// output
set(8,5,3,6,9)

// 按位异或
x=1 0 1;
y=0 1 1;
x^y;
// output
[1,1,0]
```
