# rowFilterAndSort

首发版本：3.00.5

## 语法

`rowFilterAndSort(sortVec, filterVec, orderedFilters, args...)`

## 详情

对数组向量或列式元组中的元素进行过滤和排序。

*sortVec*
、
*filterVec*
和
*args...*
的元素按位置一一对应。该函数先基于
*filterVec*
进行过滤，再基于
*sortVec*
和
*filterVec*
进行排序，过滤和排序标准由
*orderedFilters*
指定：

* **过滤**
  ：对
  *filterVec*
  遵照
  *orderedFilters*
  进行过滤，仅保留
  *orderedFilters*
  中指定的值。
* **排序**
  ：过滤后，对 sortVec 中的等值数据，根据对应
  *filterVec*
  的值遵照
  *orderedFilters*
  指定顺序进行排序。

## 参数

**sortVec**
数值类型或时间类型的数组向量或列式元组，表示排序列。或是一个元组，包含最多 3 个数组向量或列式元组。每一行中的元素必须为有序。

**filterVec**
STRING 类型的列式元组，表示过滤并用于排序的键列。或是一个元组，包含最多 3 个 STRING 类型的列式元组。

**orderedFilters**
STRING 向量或元组，表示过滤与排序的标准。过滤后
*filterVec*
中仅在
*orderedFilters*
中指定的元素将被保留。当
*filterVec*
是元组时，
*orderedFilters*
也必须是元组，且元组中元素个数与
*filterVec*
相等。

**args**
可选参数，可以是数组向量或列式元组，其数据形式必须与
*sortVec*
一致，表示同步过滤与重排的附加数据列。

## 返回值

返回一个元组，元素依次为过滤排序并展开的 *sortVec* 、 *filterVec* 和 *args* 。

注：

展开指当 *sortVec，filterVec* 和 *args* 是元组时，其每个元素独立作为返回结果元组的一个元素。例如，
*sortVec，filterVec* 都是包含两个元素的元组， *args* 包含三个元素，返回结果为包含 7
（=2+2+3）个元素的元组。

## 例子

例1. 对列式元组进行过滤排序：askPrices 中各档报价来自不同的渠道 srcs。现过滤出来自 SRC3 或 SRC1 的报价，相同报价按照 SRC3, SRC1 的顺序排列。相应的多档委托量 askVols 也一并过滤和排序。

```
orderedFilters = `SRC3`SRC1
srcs = [`SRC1`SRC2`SRC3`SRC1`SRC3, `SRC1`SRC3`SRC1`SRC2`SRC3`SRC1`SRC2].setColumnarTuple!(true)
askPrices = [900 900 900 901 901, 800 800 802 802 802 803 803].setColumnarTuple!(true)
askVols = [10 15 20 15 20, 20 15 30 40 20 15 30].setColumnarTuple!(true)
rowFilterAndSort(askPrices, srcs, orderedFilters, askVols)
/*
output:
(([900,900,901,901],[800,800,802,802,803]),
(["SRC3","SRC1","SRC3","SRC1"],["SRC3","SRC1","SRC3","SRC1","SRC1"]),
([20,10,20,15],[15,20,20,30,15]))
*/
```

例2. 对数组向量的元组：askPrices 中各档报价对应不同时间，来自不同的渠道 srcs，各渠道有不同的清算速度。现过滤出来自 SRC1 或 SRC3，且清算速度为 T0，T1 或 T2 的报价，结果将按照价格优先、时间优先，渠道按照 SRC1、SRC3，清算速度按照 T0，T1，T2 的顺序排列。相应的多档委托量 askVols 也一并过滤和排序。

```
orderedFilters = [`SRC1`SRC3, `T0`T1`T2]
srcs = [`SRC1`SRC1`SRC3`SRC3`SRC3, `SRC3`SRC3`SRC1`SRC2`SRC3`SRC1`SRC2].setColumnarTuple!(true)
speeds = [`T1`T2`T0`T2`T4, `T2`T0`T1`T0`T0`T0`T1].setColumnarTuple!(true)
askPrices = array(INT[], 0, 10).append!([900 900 900 901 901, 800 800 802 802 802 803 803])
quoteTimes = array(SECOND[], 0, 10).append!([09:30:00 09:30:00 09:30:00 09:30:01 09:30:02,
	09:30:00 09:30:00 09:30:00 09:30:00 09:30:00 09:30:00 09:30:00])
askVols = array(INT[], 0, 10).append!([10 15 20 15 20, 20 15 30 40 20 15 30])
rowFilterAndSort([askPrices,quoteTimes], [srcs,speeds], orderedFilters, askVols)
/*
output:
([[900,900,900,901],[800,800,802,802,803]],
[[09:30:00,09:30:00,09:30:00,09:30:01],[09:30:00,09:30:00,09:30:00,09:30:00,09:30:00]],
(["SRC1","SRC1","SRC3","SRC3"],["SRC3","SRC3","SRC1","SRC2","SRC3"]),
(["T1","T2","T0","T2"],["T0","T2","T1","T0","T0"]),
[[10,15,20,15],[15,20,30,20,15]])
*/
```

**相关函数：rowMergeAndSort**
