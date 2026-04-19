<!-- Auto-mirrored from upstream `documentation-main/progr/data_types_forms/columnarTuple.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 列式元组（columnar tuple）

## 概述

列式元组是一种特殊的元组类型，列式元组的元素可以是标量也可以是向量，且其值的类型必须保持一致。列式元组的取数规则和数组向量一致。

注：

2.00.9 版本后，DolphinDB 支持将列式元组存储为表的一列（分布式表暂不支持）。

## 创建列式元组

* 通过函数 setColumnarTuple! 可以将一个普通元组转换成列式元组。
* 通过函数 isColumnarTuple 可以判断一个元组是否为列式元组。

  ```
  tp = [[1.3,2.5,2.3], [4.1,5.3], 6.3]
  isColumnarTuple(tp)
  // output
  false

  tp.setColumnarTuple!()
  isColumnarTuple(tp)
  // output
  true
  ```

## 访问列式元组

普通元组按索引取出的是对应下标的元素值，而列式元组和数组向量则是返回每个元素对应下标的值组成的向量。

```
tp = [[1.3,2.5,2.3], [4.1,5.3], 6.3]
ctp = [[1.3,2.5,2.3], [4.1,5.3], 6.3].setColumnarTuple!()
av = array(DOUBLE[], 0, 20).append!([[1.3,2.5,2.3], [4.1,5.3], 6.3])

// 按索引取数
tp[0]
// output
[1.3,2.5,2.3]

ctp[0]
// output
[1.3,4.1,6.3]

av[0]
// output
[1.3,4.1,6.3]
```

按 slice 取数时（即 x[start:end]），若 slice 范围超过了列式元组中元素的长度，会自动填充空值。

当元素类型不为 STRING, SYMBOL 且 slice 的 end 不为空时，列式元组 slice 后的返回结果是一个数组向量，否则返回的仍然时列式元组。

```
//按 slice 取数
a = ctp[0:3]
a
// output
[[1.3,2.5,2.3],[4.1,5.3,00F],[6.3,6.3,6.3]]

b = ctp[0:]
b
// output
([1.3,2.5,2.3],[4.1,5.3],6.3)
```

和数组向量一致，若要单独取出每个元素的值可以通过 `row` 函数实现。

```
ctp.row(0)
// output
[1.3,2.5,2.3]
```

## 追加数据到列式元组

```
ctp = [[1.3,2.5,2.3], [4.1,5.3], 6.3].setColumnarTuple!()
ctp.append!([3.3,2.1])
ctp
// output
([1.3,2.5,2.3],[4.1,5.3],6.3,[3.3,2.1])
```

## 修改列式元组中的数据

列式元组中的数据可以通过指定行和列的方式进行修改：`obj[rowIndex, colIndex] = newValue`

rowIndex 是标量或数据对，若是数据对，当不指定开始的索引时，表示第 0 行开始；当结束的索引不指定时，表示到最后一行结束。rowIndex
可以省略。省略时代表所有行中对应的 colIndex 位置的数据都要修改。

colIndex 是标量或数据对，不可省略。当是数据对时，数据对的开始和结束索引不可省略。

newValue 是标量、向量或元组：

* newValue 是一个标量时，所有通过 rowIndex 和 colIndex 指定的数据都会修改为 newValue；
* newValue 是与 colIndex 相同长度的标量或元组时，每一行中由 colIndex 指定的数据都会对应替换为该向量或元组的值；
* newValue 是长度与 rowIndex 相同的向量或元组时，其中 newValue 的元素为标量或者长度与 colIndex
  相同的数组，每一行中的数据会替换为 newValue 中对应位置的元素。

```
// 创建列式元组 ctp
ctp = [1 2 3 4, 5 6 7 8 , 9 10 11 12].setColumnarTuple!()
print ctp
// output
([1,2,3,4],[5,6,7,8],[9,10,11,12])

// 修改第0行、第1列的数据为 50
ctp[0,1] = 50
print ctp
// output
([1,50,3,4],[5,6,7,8],[9,10,11,12])

// 修改第0到1行中第1到2列的数据为 100 200
ctp[0:2, 1:3] = 100 200
print ctp
// output
([1,100,200,4],[5,100,200,8],[9,10,11,12])

// 修改第0到1行中第1到2列的数据为 300 400，省略行索引的起始索引值
ctp[:2, 1:3] = 300 400
print ctp
// output
([1,300,400,4],[5,300,400,8],[9,10,11,12])

// 修改第0行中第1到2列的数据为 500 600，修改第1行中第1到2列的数据为 700 800
ctp[0:2, 1:3] = (500 600, 700 800)
print ctp
// output
([1,500,600,4],[5,700,800,8],[9,10,11,12])

// 修改所有行中第1到2列的数据为 900 1000
ctp[, 1:3] = 900 1000
print ctp
// output
([1,900,1000,4],[5,900,1000,8],[9,900,1000,12])
```

## 列式元组按行计算

```
ctp = [[1.3,2.5,2.3], [4.1,5.3], 6.3].setColumnarTuple!()
rowSum(ctp)
// output
[6.1,9.4,6.3]
```

## 创建一个列为列式元组的内存表

创建内存表时，DolphinDB 支持将元素不等长的普通元组存储为列式元组。

```
sym = `st1`st2`st3
price = [[3.1,2.5,2.8], [3.1,3.3], [3.2,2.9,3.3]]
t = table(sym, price)
t;
```

| sym | price |
| --- | --- |
| st1 | [3.1,2.5,2.8] |
| st2 | [3.1,3.3] |
| st3 | [3.2,2.9,3.3] |

注：

对于元素等长的普通元组，必须调用 setColumnarTuple!() 转换为列式元组 。

```
id = 1 2 3
val = [[1,2,3], [4,5,6],[7,8,9]]
table(id, val)
```

| id | col1 | col2 | col3 |
| --- | --- | --- | --- |
| 1 | 1 | 4 | 7 |
| 2 | 2 | 5 | 8 |
| 3 | 3 | 6 | 9 |

```
table(id, val.setColumnarTuple!())
```

| id | val |
| --- | --- |
| 1 | [1,2,3] |
| 2 | [4,5,6] |
| 3 | [7,8,9] |
