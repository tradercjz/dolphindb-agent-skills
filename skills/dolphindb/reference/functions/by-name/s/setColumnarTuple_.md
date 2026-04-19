# setColumnarTuple!

## 语法

`setColumnarTuple!(X, [on=true])`

## 详情

用于 tuple 和 columnar tuple
的相互转化。

## 参数

`X` 相同类型的向量或标量组成的 tuple。

`on` 布尔值，表示 tuple 和 columnar tuple 之间的转换。默认为 true，表示将 tuple 转换成
columnar tuple；若为 false，表示将 columnar tuple 转换为 tuple。

## 返回值

元组或列式元组。

## 例子

```
tp = [[1,2,3], [4,5,6], [7,8]]
isColumnarTuple(tp)
// output
false

tp.setColumnarTuple!()
isColumnarTuple(tp)
// output
true

t = table(1..5 as id, [`a`a,`b`a,`c, `f`e, `g] as val)
isColumnarTuple(t.val)
// output
true

t1 = t.val.setColumnarTuple!(false)
isColumnarTuple(t1)
// output
false
```
