# rowMergeAndSort

首发版本：3.00.5

## 语法

`rowMergeAndSort(sortVec, asc, args...)`

## 详情

将数组向量或列式元组的多行合并为一行，并对合并结果进行排序。

*sortVec*
和
*args*
的元素按位置一一对应，
*args*
的元素跟随 sortVec 同步合并和排序。

## 参数

**sortVec**
可以是数组向量或列式元组，表示合并后的排序列。
*sortVec*
也可以是一个元组，包含最多 2 个数组向量或列式元组。

**asc**
是一个布尔值或布尔向量，表示合并后的
*sortVec*
是否按升序排列，true 代表升序。当
*sortVec*
为元组时，
*asc*
可以为向量，长度与
*sortVec*
元素个数相等，分别指示 sortVec 的每一个元素在合并后的排序规则。

**args**
可选参数，可以是数组向量或列式元组，表示需要随
*sortVec*
同步合并并按相同排序重排的附加列。

## 返回值

* 指定 args 时，返回一个元组，元素数量为 args 长度加一，每个元素均为向量。
* 未指定 args 时，返回一个向量。

## 例子

例1. 合并数组向量，并按照升序排序。返回一个向量

```
askPrices = array(INT[], 0, 10).append!([900 900 900 901 901, 800 800 802 802 802 803 803])
rowMergeAndSort(askPrices, true)
//output: ([800,800,802,802,802,803,803,900,900,900,901,901])
```

例2. 合并列式元组，多个排序列按照不同顺序排列：askPrices 中各档报价对应不同时间 、不同委托量，来自不同的渠道 srcs。现将数据合并，并按照 askPrices 降序，quoteTimes 升序的顺序排列。返回一个元组。

```
srcs = [`SRC1`SRC1`SRC3`SRC3`SRC3, `SRC3`SRC3`SRC1`SRC2`SRC3`SRC1`SRC2].setColumnarTuple!(true)
askPrices = array(INT[], 0, 10).append!([900 900 900 901 901, 800 800 802 802 802 803 803])
quoteTimes = array(SECOND[], 0, 10).append!([09:30:00 09:30:00 09:30:00 09:30:01 09:30:02,
	09:30:00 09:30:00 09:30:00 09:30:00 09:30:00 09:30:00 09:30:00])
askVols = array(INT[], 0, 10).append!([10 15 20 15 20, 20 15 30 40 20 15 30])
rowMergeAndSort([askPrices,quoteTimes], false true, srcs, askVols)
/*
output:
([901,901,900,900,900,803,803,802,802,802,800,800],
[09:30:01,09:30:02,09:30:00,09:30:00,09:30:00,09:30:00,09:30:00,09:30:00,09:30:00,09:30:00,09:30:00,09:30:00],
["SRC3","SRC3","SRC1","SRC1","SRC3","SRC1","SRC2","SRC1","SRC2","SRC3","SRC3","SRC3"],
[15,20,10,15,20,15,30,30,40,20,20,15])
*/
```

**相关函数：rowFilterAndSort**
