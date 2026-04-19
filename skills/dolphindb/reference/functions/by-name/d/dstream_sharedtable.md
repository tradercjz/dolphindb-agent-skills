# DStream::sharedTable

## 语法

`DStream::sharedTable(name, X, [X1], [X2], .....)`

或

`DStream::sharedTable(name, capacity:size, colNames, colTypes)`

## 详情

在 Orca 中创建一个共享内存表，仅支持在 `DStream::udfEngine` 中使用。关于内存表的说明参见 table。

## 参数

**name** 字符串标量，表示共享键值内存表的名称。

第一种用法中，**X**, **X1**, **X2** ...
可以是向量、数组向量、矩阵或元组。每个向量、元组、数组向量的长度，以及矩阵中每列长度都必须相同。**当 Xk 是元组时：**

* 若 Xk 的元素是等长的向量，**元组的每个元素将作为表的一列。**元组的长度必须等于表的行数。
* 若 Xk 包含不同类型或不等长元素，**则将单独作为表的一列（列类型为 ANY），其每个元素将作为该列每行的元素值。**Xk
  的长度仍然必须和表的行数保持一致。

第二种用法中：

* **capacity** 是正整数，表示建表时系统为该表分配的内存（以记录数为单位）。当记录数超过
  *capacity* 时，系统首先会分配 *capacity*
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
  是一个向量，表示每列的数据类型，支持数组向量类型和元组（ANY）类型。可使用表示数据类型的系统保留字或相应的字符串。

## 返回值

一个表。

## 例子

本例结合 `DStream::sharedTable` 与
`DStream::udfEngine`，实现实时计算并输出当前平均值的功能。`DStream::sharedTable`
用于持续保存每次计算得到的历史平均值。每次处理新数据时，UDF 会基于最新数据重新计算平均值，将其追加到
`DStream::sharedTable` 中，并仅将最新一行（即当前最新的平均值）输出至下游。

```
if(existsCatalog("orcaCatalog")) dropCatalog("orcaCatalog")
createCatalog("orcaCatalog")
go
use catalog orcaCatalog

// 创建流图
g = createStreamGraph("avgCalc")
g.sharedTable("stats", 1:0, `sum`count, [DOUBLE, LONG])

g.source("numbers", ["value"], [DOUBLE])
  .udfEngine(def(msg) {
    stats = orcaObj("stats")

    // 读取历史统计值
    if(stats.size() > 0) {
        lastSum = exec last(sum) from stats
        lastCount = exec last(count) from stats
    } else {
        lastSum = 0.0
        lastCount = 0
    }

    // 计算新值
    newSum = lastSum + sum(msg.value)
    newCount = lastCount + msg.size()
    if (newCount > 0) {
        avgValue = newSum / newCount
    } else {
        avgValue = 0.0
    }

    // 写入新值
    newRow = table(newSum as sum, newCount as count)
    stats.append!(newRow)

    // 返回计算结果
    return table(newSum as total, newCount as count, avgValue as avg)
  })
  .sink("output")

g.submit()
go
// 生成模拟数据
mockData1 = table(rand(10.0, 3) as value)
mockData2 = table(rand(10.0, 5) as value)
mockData3 = table(rand(10.0, 2) as value)

// 插入数据,等待处理并查看结果
appendOrcaStreamTable("orcaCatalog.orca_table.numbers", mockData1)
select * from orcaCatalog.orca_table.numbers;
select * from orcaCatalog.orca_table.output;
appendOrcaStreamTable("orcaCatalog.orca_table.numbers", mockData2)
select * from orcaCatalog.orca_table.numbers;
select * from orcaCatalog.orca_table.output;
appendOrcaStreamTable("orcaCatalog.orca_table.numbers", mockData3)
select * from orcaCatalog.orca_table.numbers;
select * from orcaCatalog.orca_table.output;
```
