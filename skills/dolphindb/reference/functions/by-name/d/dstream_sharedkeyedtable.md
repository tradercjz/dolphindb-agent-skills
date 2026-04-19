# DStream::sharedKeyedTable

## 语法

`DStream::sharedKeyedTable(name, keyColumns, X, [X1], [X2],
.....)`

或

`DStream::sharedKeyedTable(name, keyColumns, capacity:size, colNames,
colTypes)`

或

`DStream::sharedKeyedTable(name, keyColumns, table)`

## 详情

在 Orca 中创建一个共享键值内存表，仅支持在 `DStream::udfEngine` 中使用。关于键值内存表的说明参见 keyedTable。

## 参数

**name** 字符串标量，表示共享键值内存表的名称。

**keyColumns** 是一个字符串标量或向量，表示主键。主键的数据类型必须属于以下类别： INTEGRAL,
TEMPORAL 或 LITERAL。

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

第三种用法中，`table` 是一个表。注意，*table* 中的
*keyColumns* 不能包含重复值。

## 返回值

一个键值内存表。

## 例子

下面通过 `DStream::sharedKeyedTable` 与 `DStream::udfEngine`
的结合，实现计算历史差值的功能。

在本示例中，使用 `DStream::sharedKeyedTable` 存储已处理数据的历史记录，对每个 id
仅保留最新的一条记录。当新数据到达时，若该 id 已存在于表中，则输出新值与历史值之间的差值；否则，仅将新数据存入表中，不输出。

```
if(existsCatalog("orcaCatalog")) dropCatalog("orcaCatalog")
createCatalog("orcaCatalog")
go
use catalog orcaCatalog
// 创建流图
g = createStreamGraph("compare")
g.sharedKeyedTable("history", "id", 1:0, `id`value, [INT, DOUBLE])
g.source("data", `id`value`time, [INT, DOUBLE, TIMESTAMP])
  .udfEngine(def(msg) {
    history = orcaObj("history")
    diffTable = table(100:0, `id`diff, [INT, DOUBLE])
    for(i in 0:msg.size()) {
        idVal = msg.id[i]
        valueVal = msg.value[i]
        // 读取历史值
        old = select value from history where id = idVal
        // 写入新值
        newRow = table(idVal as id, valueVal as value)
        history.append!(newRow)
        // 计算差值
        if(old.size() > 0) {
            diffTable.append!(table(idVal as id, (valueVal - old.value[0]) as diff))
        }
    }
    return diffTable
  })
  .sink("comparison")
g.submit()
go
// 生成模拟数据
mockData = table(1..5 as id, rand(100.0, 5) as value, now() + 1..5 as time)
// 插入数据
appendOrcaStreamTable("orcaCatalog.orca_table.data", mockData)
// 生成id重复的数据
mockData = table(1..5 as id, rand(100.0, 5) as value, now() + 1..5 as time)
// 插入数据
appendOrcaStreamTable("orcaCatalog.orca_table.data", mockData)
// 等待处理并查看结果
sleep(1000)
select * from orcaCatalog.orca_table.comparison
```

| id | diff |
| --- | --- |
| 1 | 35.55946895749296 |
| 2 | -3.4362593906550387 |
| 3 | 36.283468999034596 |
| 4 | 68.97968558337999 |
| 5 | -91.64246928217878 |
