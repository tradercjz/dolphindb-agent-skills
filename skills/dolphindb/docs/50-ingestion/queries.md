<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db_oper/queries.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 查询数据

DolphinDB SQL 兼容标准 SQL 的语法：

```
SELECT column1, column2
FROM table_name
WHERE condition
```

**查询内存表**

如下例所示，内存表可直接查询：

```
t = table([1,2,3] as id, ["AA","BB","CC"] as sym, [100,200,300] as val)
select * from t where id = 1
select * from t where sym in ["AA","BB"]
select * from t where val between 150 and 300
```

**查询分布式表**

DolphinDB 中，数据库和表跟向量、矩阵、字典等一样，是一个数据对象。通过 DolphinDB SQL 查询分布式库表时，不能直接引用库表的名称，而是需要使用
`loadTable` 等内置函数加载库表为一个对象。

例如数据库 dfs://querydb 下有一个分布式表 querytb，先将其加载为变量 pt。在后续查询中，即可使用变量 pt 来引用该数据库表。

```
pt = loadTable(database="dfs://querydb", tableName="querytb")
select * from pt where date = 2024.10.10
select * from pt where date between 2024.10.10 and 2024.10.12
```

## 关联查询

关联查询指的是在 SQL 中通过 JOIN 操作，从多个相关联的表中检索数据的查询方式。

对于内存表的连接，DolphinDB 既支持使用内置函数实现，也可以通过 SQL 语句实现。而分布式表连接仅支持在 SQL 语句中完成。

下面将重点介绍分布式表连接。有关分布式连接支持的连接方式，参考 表连接 及其下属连接方式页面。

当分布式表与维度表或内存表连接时，系统会将维度表或内存表复制到分布式表所在的各个节点上执行连接操作。如果本地表数据量非常庞大，表的传送将非常耗时。为了提高性能，系统在数据复制之前用
where 条件尽可能多地过滤内存表。如果右表数据量太大，会影响查询速度，所以在实际应用中，右表的数据量最好比较小。

以下为连接分布式表的示例，创建数据库的脚本如下：

```
dates=2019.01.01..2019.01.31
syms="A"+string(1..30)
sym_range=cutPoints(syms,3)
db1=database("",VALUE,dates)
db2=database("",RANGE,sym_range)
db=database("dfs://stock",COMPO,[db1,db2])
n=10000
datetimes=2019.01.01T00:00:00..2019.01.31T23:59:59
t=table(take(datetimes,n) as trade_time,take(syms,n) as sym,rand(1000,n) as qty,rand(500.0,n) as price)
trades=db.createPartitionedTable(t,`trades,`trade_time`sym).append!(t)

n=200
t2=table(take(datetimes,n) as trade_time,take(syms,n) as sym,rand(500.0,n) as bid,rand(500.0,n) as offer)
quotes=db.createPartitionedTable(t2,`quotes,`trade_time`sym).append!(t2)

t3=table(syms as sym,take(0 1,30) as type)
infos=db.createTable(t3,`infos).append!(t3)
```

### 连接两个分布式表

通过以下语句等值连接两个分布式表 trades 和
quotes：

```
select * from ej(trades,quotes,`trade_time`sym)
```

| trade\_time | sym | qty | price | bid | offer |
| --- | --- | --- | --- | --- | --- |
| 2019.01.01T00:00:00 | A1 | 39 | 7.366735 | 37.933525 | 446.917644 |
| 2019.01.01T00:00:09 | A10 | 15 | 461.381014 | 405.092702 | 26.659516 |
| 2019.01.01T00:00:10 | A11 | 987 | 429.981704 | 404.289413 | 347.64917 |
| 2019.01.01T00:00:11 | A12 | 266 | 60.466206 | 420.426175 | 83.538043 |
| 2019.01.01T00:00:12 | A13 | 909 | 362.057769 | 324.886047 | 162.502655 |
| 2019.01.01T00:00:13 | A14 | 264 | 113.964472 | 497.598722 | 103.114702 |
| 2019.01.01T00:00:14 | A15 | 460 | 347.518325 | 24.584629 | 357.854207 |
| 2019.01.01T00:00:15 | A16 | 196 | 258.889177 | 49.467399 | 13.974672 |
| 2019.01.01T00:00:16 | A17 | 198 | 403.564922 | 428.539984 | 208.410852 |
| 2019.01.01T00:00:17 | A18 | 30 | 288.469046 | 41.905556 | 378.080141 |
| ... |  |  |  |  |  |

### 连接分布式表和维度表

通过以下语句左连接分布式表和维度表：

```
select * from lj(trades,infos,`sym)
```

| trade\_time | sym | qty | price | type |
| --- | --- | --- | --- | --- |
| 2019.01.01T00:00:00 | A1 | 856 | 359.809918 | 0 |
| 2019.01.01T00:00:09 | A10 | 368 | 305.801702 | 1 |
| 2019.01.01T00:00:10 | A11 | 549 | 447.406744 | 0 |
| 2019.01.01T00:00:11 | A12 | 817 | 115.613373 | 1 |
| 2019.01.01T00:00:12 | A13 | 321 | 298.317481 | 0 |
| 2019.01.01T00:00:13 | A14 | 3 | 2.289171 | 1 |
| 2019.01.01T00:00:14 | A15 | 586 | 91.841629 | 0 |
| 2019.01.01T00:00:15 | A16 | 745 | 43.256142 | 1 |
| 2019.01.01T00:00:16 | A17 | 60 | 0.153205 | 0 |
| ... |  |  |  |  |

### 连接分布式表和内存表

通过以下语句等值连接分布式表和内存表：

```
tmp=table("A"+string(1..15) as sym,2019.01.11..2019.01.25 as date)
select * from ej(trades,tmp,`sym)
```

| trade\_time | sym | qty | price | date |
| --- | --- | --- | --- | --- |
| 2019.01.01T00:00:00 | A1 | 856 | 359.809918 | 2019.01.11 |
| 2019.01.01T00:00:09 | A10 | 368 | 305.801702 | 2019.01.20 |
| 2019.01.01T00:00:10 | A11 | 549 | 447.406744 | 2019.01.21 |
| 2019.01.01T00:00:11 | A12 | 817 | 115.613373 | 2019.01.22 |
| 2019.01.01T00:00:12 | A13 | 321 | 298.317481 | 2019.01.23 |
| 2019.01.01T00:00:13 | A14 | 3 | 2.289171 | 2019.01.24 |
| 2019.01.01T00:00:14 | A15 | 586 | 91.841629 | 2019.01.25 |
| 2019.01.01T00:00:30 | A1 | 390 | 325.407485 | 2019.01.11 |
| ... |  |  |  |  |

## 分组子句

### group by

group by 是一种用于将数据进行分组并对每个组应用聚合函数的 SQL 语句。

例如，在下面脚本中，按照日期进行分组，并计算所有股票每天的订单数量总和。

```
orders = table(`SH0001`SH0001`SH0002`SH0002`SH0002 as code,
2024.03.06 2024.03.07 2024.03.06 2024.03.07 2024.03.08 as date,
13100 15200 3700 4800 3500 as orderQty)

select sum(orderQty) as sum_orderQty from orders group by date
```

更多细节请参考 group by。

### context by

context by 是 DolphinDB 的独有功能，是对标准 SQL 语句的拓展。与 `group by`
类似，都对数据进行分组。但是，用 `group by` 时，每一组返回一个标量值，而用 `context
by` 时，每一组返回一个和组内元素数量相同的向量。`group by` 只能配合聚合函数使用，而
`context by` 既可以配合聚合函数使用，也可以与移动窗口函数或累积函数等其它函数结合使用。

下例中，对于原表的每一行， `context by` 子句都生成了分组内的计算结果。需要注意的是，在使用 `group
by` 子句时，返回的结果中会自动添加分组列，而在使用 `context by` 子句时，则需要在
`select`
语句中手动指定分组列。

```
orders = table(`SH0001`SH0001`SH0002`SH0002`SH0002 as code,
2024.03.06 2024.03.07 2024.03.06 2024.03.07 2024.03.08 as date,
13100 15200 3700 4800 3500 as orderQty)
select date, sum(orderQty) as sum_orderQty from orders context by date
```

`context by` 子句的应用场景非常广泛。它可以与滑动窗口系列函数结合使用，按照特定的分组进行滑动计算；也可与 limit
子句一起使用，以获取表中每个分组中的前 n 条或最后 n 条记录。如果 limit 后面为正数，则表示获取前 n 条记录；如果 limit
后面为负数，则表示获取最后 n 条记录。

更多细节请参考 context by。

### pivot by

`pivot by` 是 DolphinDB 的独有功能，是对标准 SQL
语句的拓展。它将表中一列或多列的内容按照两个维度重新排列，亦可配合数据转换函数使用。

与 `select` 子句一起使用时返回一个表，而和 `exec`
语句一起使用时返回一个矩阵。若重新排列后行维度存在多个相同值，则会进行去重，只保留最后一个值。

当因子以窄表模式存储，可使用 `pivot by`
在查询时将数据转换为面板数据，进而用于量化交易中的程序计算。例如，对一个包含时间戳、股票代码、因子名和因子值四列的窄表，可使用以下查询转化为面板数据：

```
t = select factorValue
from loadTable("dfs://factordb","factortb")
where tradetime >= 2023.12.01
  and tradetime <= 2023.12.31
  and factorname = specificFactorName
pivot by tradetime, securityid, factorname
```

更多细节请参考 pivot by。

## 查询优化

### 分区剪枝

绝大多数分布式查询只涉及分布式表的部分分区。当数据量较大时，过滤条件的不同写法会造成查询耗时的巨大差异。若过滤条件满足以下要求，则可以进行分区剪枝，缩小查询范围：

* 当查询采用 VALUE 分区、RANGE 分区或 LIST 分区的分布式表时，若 where
  子句中某个过滤条件同时满足以下条件，则系统只加载与查询相关的分区，以节省查询耗时：

  + 仅包含分布式表的原始分区字段、使用关系运算符（<, <=,=, ==, >, >=, in,
    between）或逻辑运算符（or, and），以及常量（包括常量与常量的运算）。
  + 不包括链式条件（链式条件形如 100 <x <200）。
  + 过滤逻辑可以缩窄相关分区范围（下面的例子中有说明）。
* 当查询采用 HASH 分区的分布式表时，若 where
  子句中某个过滤条件满足以下条件，则系统会进行分区剪枝：包含分布式表的原始分区字段，使用关系运算符（=, ==, in,
  between）或逻辑运算符（or, and），以及常量（包括常量与常量的运算）。注意：当分区字段是 STRING 类型时，使用 between
  运算符不能针对这一字段进行剪枝。

若不满足上述要求，则会遍历所有分区进行查询，CPU、内存、磁盘IO的资源都会迅速耗尽。

如果分布式表使用 TSDB 存储引擎，在 WHERE 子句中指定分区字段后，进一步指定 *sortKey* 可以提升查询效率。

如果分布式表使用 PKEY 存储引擎，查询条件中指定索引字段可以提升查询效率。

下面的例子可以帮助理解 DolphinDB
如何缩窄相关分区范围。

```
n=10000000
id=take(1..1000, n).sort()
date=1989.12.31+take(1..365, n)
announcementDate = date+rand(5, n)
x=rand(1.0, n)
y=rand(10, n)
t=table(id, date, announcementDate, x, y)
db=database("dfs://rangedb1", RANGE, [1990.01.01, 1990.03.01, 1990.05.01, 1990.07.01, 1990.09.01, 1990.11.01, 1991.01.01])
pt = db.createPartitionedTable(t, `pt, `date)
pt.append!(t);
```

以下类型的查询可以在加载和处理数据前缩小分区范围：

```
select max(x) from pt where date>1990.12.01-10;
// 系统确定，只有一个分区与查询相关：1990.11.01, 1991.01.01)。
```

```
select max(x) from pt where date between 1990.08.01:1990.12.01 group by date;
// 系统确定，只有三个分区与查询相关：[1990.07.01, 1990.09.01)、[1990.09.01, 1990.11.01)和[1990.11.01, 1991.01.01)。
```

```
select max(x) from pt where y<5 and date between 1990.08.01:1990.08.31;
// 系统确定，只有一个分区与查询相关：[1990.07.01, 1990.09.01)。注意，系统忽略了y<5的条件。加载了相关分区后，系统会根据y<5的条件进一步筛选数据。
```

对于时间类型的分区列应用时间精度更低的函数，也可以缩小分区范围。时间精度由高到低的排序为：

* NANOTIMESTAMP > TIMESTAMP > DATETIME> DATEHOUR> DATE> MONTH> YEAR
* TIME> SECOND > MINUTE> HOUR

上例的时间类型是 DATE，则对其应用 `month`，`year`
函数后，也可以进行分区剪枝，见如下代码：

```
select max(x) from pt where month(date)>=1990.12M;
// 系统确定，只有一个分区与查询相关：[1990.11.01, 1991.01.01)。
```

以下查询不能确定相关分区。如果 pt 是数据量非常大的分区表，查询会耗费大量时间，因此应该尽量避免以下写法。

```
select max(x) from pt where date+30>2019.12.01;
//不可对分区字段进行运算

select max(x) from pt where 2019.12.01<date<2019.12.31;
//不可使用链式比较

select max(x) from pt where y<5;
//至少有一个过滤条件需要使用分区字段

select max(x) from pt where date<announcementDate-3;
//与分区字段比较时仅可使用常量，不可使用其他列

select max(x) from pt where y<5 or date between 1990.08.01:1990.08.31;
//由于必须执行y<5，过滤逻辑无法缩窄相关分区范围
```

### 分组查询中使用 `map` 关键字

在分布式 SQL
中，对分组数据进行查询和计算时，通常先在各个分区内单独进行计算，然后将结果进行进一步的计算，以保证最终结果的正确性。如果分区的粒度大于或等于分组的粒度，则可以确保数据的查询和计算不会跨分区进行。在这种情况下，可以通过添加
`map` 关键字来避免进一步计算的开销，从而提升查询性能。 详见 [map 关键字。

### 使用 `HINT` 关键字

DolphinDB 提供了一系列的 `HINT` 关键字，这些关键字可以让 SQL 以一些特殊的方式来执行。 例如，通过
`[HINT_EXPLAIN]` 关键字，系统将在执行 SQL
语句时打印执行过程，以实时监测查询速度和执行顺序，帮助用户发现性能瓶颈，优化 SQL 语句。`[HINT_KEEPORDER]`
关键字可以保证`context by` 子句分组后的查询结果依然按照原本的数据顺序返回。 详见 HINT 关键字。

### 结果赋值

查询时，尽量将查询结果赋值给一个变量，即用 `data = select * from pt` 替代 `select
* from pt`，二者区别在于：

* 前者会将数据从分布式表查询到内存。
* 后者会将数据查出后返回给客户端。如果数据量很大，传输中可能会造成服务端网络拥塞，且会感觉查询很慢，这是由于大量时间耗费在网络传输过程中。

### 查询上限

每次查询的数据数量上限是 20 亿，如需查询超过 20 亿条的数据，应分批查询。

例如以下脚本超出上限：

```
t = select * from pt where date between 2010.01.01 and 2024.12.31
```

则可根据实际数据量分多批查询，例如分两批查询：

```
t1 = select * from pt where date between 2010.01.01 and 2017.12.31
t2 = select * from pt where date between 2018.01.01 and 2024.12.31
```

每次查询涉及的分区数默认上限为 65536。如果遇到涉及分区数超过此限制的情况，可以通过增加过滤条件减小涉及的分区数，也可以通过修改配置参数
maxPartitionNumPerQuery 的值放宽限制，通常更推荐前者。

**相关信息**

* [loadTable](../../funcs/l/loadTable.html "loadTable")
* [group by](../../progr/sql/groupby.html "group by")
* [context by](../../progr/sql/contextBy.html "context by")
* [pivot by](../../progr/sql/pivotBy.html "pivot by")
* [map 关键字](../../progr/sql/map.html "map 关键字")
* [HINT 关键字](../../progr/sql/hint.html "HINT 关键字")
