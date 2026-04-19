# changelogStreamTable

首发版本：3.00.5

## 语法

`changelogStreamTable(keyColumn, X, [X1], [X2],
.....)`

或

`changelogStreamTable(keyColumn, capacity:size, colNames,
colTypes)`

## 详情

创建包含状态列的键值流数据表。

* 该表包含一个内部状态列（statusColumn，不展示），CHAR 类型，用于跟踪数据变更状态，目前支持两种状态：

  1. 'N'：NEW，表示 key 不存在时的新增记录；
  2. 'U'：UPDATE，表示 key 已存在时的更新记录。
* 状态列的状态也支持用户自行写入。
* 查询时只返回每个 key 的最新一条记录。

注：

目前 TimeSeriesEngine 和 ReactiveStateEngine 处理 *dummyTable*
为包含状态列的流数据表时，仅支持部分算子，具体如下：

* **TimeSeriesEngine** 在设置了 *keyColumn* 且 *updateTime*=0
  时，支持以下算子：

  + sum、avg、sum2、sum3、sum4、count、std、stdp、var、varp
* **ReactiveStateEngine** 支持以下算子：

  + cumavg、cumsum、cumstd、cumstdp、cumvar、cumvarp、cumprod、cumcount、mcount、msum、mavg、mstd、mstdp、mvar、mvarp
    以及无状态算子（表达式、无状态函数等）

## 参数

**keyColumn** 是一个字符串或向量，表示主键。主键的数据类型必须属于以下类别：INTEGRAL,
TEMPORAL, LITERAL 或 FLOATING。

第一种用法中，**X**, **X1**, **X2** ...
可以是向量、数组向量、矩阵或元组。每个向量、元组、数组向量的长度，以及矩阵中每列长度都必须相同。**当 Xk 是元组时：**

* 若 Xk 的元素是等长的向量，**元组的每个元素将作为表的一列。**元组的长度必须等于表的行数。
* 若 Xk 包含不同类型或不等长元素，**则将单独作为表的一列（列类型为 ANY），其每个元素将作为该列每行的元素值。**Xk
  的长度仍然必须和表的行数保持一致。

第二种用法中：

* **capacity** 是正整数，表示建表时系统为该表分配的内存（以记录数为单位）。当记录数超过 *capacity*
  时，系统首先会分配 *capacity*
  1.2~2倍的新的内存空间，然后复制数据到新的内存空间，最后释放原来的内存。对于规模较大的表，此类操作的内存占用会很高。因此，建议建表时预先分配一个合理的
  *capacity*。
* **size** 是整数，表示该表新建时的行数。若 *size* =0，创建一个空表。 若
  *size*>0，则建立一个只包含 size 条记录的表，记录初始值如下：

  + BOOL 类型默认值为 false；
  + 数值类型、时间类型、IPADDR、COMPLEX、POINT 的默认值为 0；
  + Literal, INT128 类型的默认值为 NULL。

  注：

  如果
  *colTypes* 指定为数组向量， *size* 必须为0。
* **colNames** 是一个向量，表示列名。
* **colTypes**
  是一个向量，表示每列的数据类型，允许主键外的其它列指定为数组向量类型或元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

## 返回值

一个表。

## 例子

```
share changelogStreamTable(`sym`time, 100:0, `sym`time`price, [STRING,DATETIME,DOUBLE]) as tickStream
n=4
data1 = table(take("000001.SH", n) as sym, take(2021.02.08T09:30:00 + 1..2, n) as time, 10+rand(100.0, n) as price)
tickStream.append!(data1)
select * from tickStream
```

|  | sym | time | price |
| --- | --- | --- | --- |
| 0 | 000001.SH | 2021.02.08 09:30:01 | 89.723076797026 |
| 1 | 000001.SH | 2021.02.08 09:30:02 | 69.34098429496888 |

**相关函数**：keyedStreamTable、getStreamTableChangelog
