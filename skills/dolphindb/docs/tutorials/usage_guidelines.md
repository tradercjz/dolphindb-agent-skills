<!-- Auto-mirrored from upstream `documentation-main/tutorials/usage_guidelines.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# DolphinDB 使用须知

## 1. 介绍

DolphinDB 脚本语言兼容 SQL-92 标准的常用语法和关键字，并提供了大量内置函数。同时，它在设计上区别于 SQL 和 Python 等脚本语言。对于习惯使用
SQL、Python 或其他语言的开发人员，在初学 DolphinDB 时可能会遇到一些常见误区。本文总结了 DolphinDB
脚本开发与运维中的基础知识，便于开发者快速查阅。

## 2. 常见问题

本章整理了 DolphinDB 使用过程中常见的问题，涵盖数据库与表管理、SQL
使用、脚本语言语法、集群运维及其它实用功能。用户可根据分类快速定位问题并查阅解答，提升开发与运维效率。

### 2.1 库表类

本节将介绍在数据库和表操作中的常见问题，如修改数据库名称、建库建表注意事项、获取数据库建库建表 SQL
、查看或修改表结构、建表策略（小数据表、主键、自增长列、唯一索引等），以及 TSDB 存储引擎的使用要点。

#### 2.1.1 如何修改数据库名称？

分布式数据库一旦创建成功， **数据库名称不可修改** 。所以在建库的时候，需为数据库指定合适的名称，避免后续想要修改库名的操作。

#### 2.1.2 数据库分区有哪些注意事项？

在创建分布式数据库时，需为数据库选择合适的分区方案，分区方案一经确定无法调整，同时该库下的所有表都将采用相同的分区方案。以下细节也需关注：

1. 分区层级：最少1级，最多3级。
2. 范围分区： **只能向后扩展且无法自动扩展** ，用户需要手动调用函数
   `addRangePartitions` 进行分区拓展。随着数据量增长，默认
   *allowMissingPartitions*=true
   时会自动舍弃分区范围外的数据且并不会报错，如果需要报错，需要设置这个参数为 false。
3. 值分区：可自动扩展， **不宜初始化过多空分区** 。

#### 2.1.3 如何获取建库建表的 SQL？

可使用 ops 运维函数 `getDatabaseDDL` ， `getDBTableDDL`
分别获取建库建表的 SQL 。参见 ops
运维函数库。

```
use ops
getDatabaseDDL("dfs://stock_lv2_snapshot")
getDBTableDDL("dfs://stock_lv2_snapshot", "snapshot")
```

#### 2.1.4 如何获取数据库句柄 dbHandle？

可通过 `database` 函数获取指定数据库的句柄。

```
db = database("dfs://stock_lv2_snapshot")
```

#### 2.1.5 如何查看集群中有哪些数据库或表？

可以通过以下函数获取库表信息：

`getClusterDFSDatabases`：获取集群上所有数据库。

`getClusterDFSTables`：获取集群上所有数据表。

`getTables`：获取指定数据库下所有表。

```
getClusterDFSDatabases()
getClusterDFSTables()
getTables(database("dfs://stock_lv2_snapshot"))
```

#### 2.1.6 如何查看库表结构？

可以通过 `schema` 查看指定数据库或数据表的结构信息。

```
db = database("dfs://stock_lv2_snapshot")
db.schema()
tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
tb.schema()
tb.schema().colDefs
```

#### 2.1.7 如何修改表结构？

* **修改表名称**

  可以通过 `renameTable` 将给定分布式数据库内的数据表改名。

  ```
  db = database("dfs://stock_lv2_snapshot")
  tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
  select count(*) from tb
  renameTable(db, "snapshot", "newSnapshot")
  tbn = loadTable("dfs://stock_lv2_snapshot", "newSnapshot")
  select count(*) from tbn
  renameTable(db, "newSnapshot", "snapshot")
  ```
* **修改表注释**

  可以通过 `setTableComment` 设置表的注释。

  ```
  tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
  setTableComment(tb, "测试表snapshot")
  tb.schema().tableComment
  ```
* **修改列注释**

  可以通过 `setColumnComment` 设置列的注释。

  ```
  tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
  setColumnComment(tb,{SecurityID:"股票代码",OpenPrice:"开盘价",ClosePrice:"收盘价"})
  schema(tb).colDefs;
  ```
* **新增列**

  可以通过 `addColumn` 或 `alter..add` 增加列。
  **新增列只能在原有列之后，不支持添加到指定列之后** 。

  ```
  tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
  addColumn(tb, ["insertTime"], [TIMESTAMP])
  alter table tb add updateTime TIMESTAMP
  tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
  tb.schema().colDefs
  ```
* **删除列**

  可以通过 `dropColumns!` 或 `alter..drop`
  删除列。 **仅支持 OLAP 存储引擎，且不支持删除分区列**。

  ```
  tb = loadTable("dfs://k_minute_level", "k_minute")
  tb.schema().engineType
  dropColumns!(tb, "val")
  alter table tb drop vwap
  ```
* **修改列名称**

  可以通过 `rename!` 或 `alter..rename` 修改列名。
  **仅支持 OLAP 存储引擎，且不支持修改分区列名**。

  ```
  tb = loadTable("dfs://k_minute_level", "k_minute")
  rename!(tb, "open", "openPrice")
  alter table tb rename close to closePrice
  tb = loadTable("dfs://k_minute_level", "k_minute")
  tb.schema().colDefs
  ```
* **修改列类型**

  可以通过 `replaceColumn!` 修改列类型。 **仅支持 OLAP
  存储引擎，且不支持修改分区列类型** 。

  ```
  tb = loadTable("dfs://k_minute_level", "k_minute")
  replaceColumn!(tb, "vol", array(LONG, 0, 1))
  tb.schema().colDefs
  ```
* **修改列顺序**

  分布式表不支持修改列顺序。

#### 2.1.8 存放数据量很小的静态信息或配置，该如何建表？

在分布式数据库中创建一个维度表。维度表是分布式数据库中没有进行分区的表，查询时会将表中所有数据加载到内存，适用于存储不频繁更新的小数据集。参见 createDimensionTable。

```
db = database("dfs://stock_lv2_snapshot")
colNames = ["param_key", "param_value", "param_flag", "param_desc",
"insert_time","update_time"]
colTypes =  [STRING, STRING, STRING, STRING, TIMESTAMP, TIMESTAMP]
tb = table(1:0, colNames, colTypes);
params_cfg =db.createDimensionTable(tb,`params_cfg,
sortColumns = `param_key`insert_time)
params_cfg.tableInsert(table(["CONN_TIME_OUT"] as param_key,
["60"] as param_value, ["1"] as param_falg,
["timeout"] as param_desc ,
[now()] as insert_time, [now()] as update_time))
select * from params_cfg;
```

#### 2.1.9 可以设置表主键吗？可以定义自增长列吗？

与传统数据库有所差异，在传统数据库上建表时，我们会为每张表建立一个主键，即使没有主键列也会虚拟出一个自增长的 id 列做为主键。在 DolphinDB
中不支持创建主键，不支持定义自增长列。对于需要从 OLTP 数据库的主键表 CDC 到 DolphinDB 中进行数据分析的需求，参见 主键存储引擎。

#### 2.1.10 可以设置表唯一索引吗？

与传统数据库有所差异，在传统数据库上建表时，我们可能会在每张表上为除主键列外仍具有唯一性的列建立唯一索引，为提升查询效率的列建立索引。在
DolphinDB 中不支持创建唯一索引或普通索引。

#### 2.1.11 TSDB 存储引擎 sortColumns 可以选择具有唯一约束的列吗？

在 DolphinDB TSDB 引擎中，sortColumns 不仅用于排序，还会参与去重：相同 sortKey
的数据只保留一条记录。因此，不建议将上游数据的主键或唯一索引列作为 sortColumns。由于这类字段具有唯一性，会导致每一行数据都形成独立的
sortKey，既无法发挥去重效果，还会造成索引膨胀，从而影响查询性能。建库建表注意事项可参见 建库建表最容易忽略的十个细节。

### 2.2 SQL类

本节将介绍在使用 DolphinDB 过程中一些常见的 SQL 操作，如查询表数据、查询表中除某些列之外的列、通过 select top 或 select
limit 限制查询返回的记录数、查看查询计划、查询列名包含特殊符号的处理方式、使用 select 与 exec 的区别、group by 及 append
使用应该注意的事项。

#### 2.2.1 如何查询表数据？

使用分布式表前，需先通过 `loadTable` 加载表元数据，再使用 select 查询结果。注意，
`loadTable` 不会直接返回数据。

```
tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
t1 = select * from tb
t2 = select * from loadTable("dfs://stock_lv2_snapshot", "snapshot")
```

#### 2.2.2 如何查询表中某些列之外的其它列？

可以通过 SQL 元编程实现。

```
tb = table(rand(10.,100) as col1,rand(10.,100) as col2,rand(10.,100) as col3,
rand(10.,100) as col4,rand(10.,100) as col5)
exceptColNames = `col1`col5
filterColNames = tb.columnNames()[!(tb.columnNames() in exceptColNames)]
res = <select _$$filterColNames from tb>.eval()
```

#### 2.2.3 如何限制查询结果返回的行数？

可以通过 select top 或 select limit 子句实现。（在与 context by 子句一同使用时，limit
子句标量值可以为负整数，返回每个组最后指定数目的记录。）

```
tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
select top 1 * from tb
select * from tb limit 1
select top 1:5 * from tb
select * from tb limit 1, 4
select * from tb where TradeDate = 2022.01.04
context by SecurityID order by TradeTime limit -1;
```

#### 2.2.4 如何查看 SQL 执行计划？

可以通过 [HINT\_EXPLAIN] 查看 select 语句执行计划。

```
select [HINT_EXPLAIN] * from  loadTable("dfs://stock_lv2_snapshot", "snapshot")
```

#### 2.2.5 select 的结果为什么要赋给一个变量

直接执行 select 查询时，返回结果集会受到 *memLimitOfQueryResult*
参数的限制，若结果数据量超过该阈值，将返回错误。同时，查询结果会一次性通过网络传输至客户端并进行渲染，数据量较大时会导致较高的耗时和资源开销。

相比之下，将 select
查询结果赋值给变量时，结果会先保存在服务端的内存表中；用户在客户端点击变量查看数据时，系统采用分页加载机制，仅返回部分数据，从而显著降低数据传输量和查询耗时。

#### 2.2.6 select 的列名包含特殊符号或以数字开头

在 SQL 中引用包含特殊符号或以数字开头的列名时，需将列名用双引号引用，并在其之前使用下划线作为标识

```
tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
//add特殊列
addColumn(tb, ["exec"], [INT])
addColumn(tb, ["1_col"], [STRING])
tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
select _"1_col" from tb
select _"exec" from tb
```

#### 2.2.7 select 和 exec 的区别

select 子句总是生成一张表，即使只选择一列亦是如此。若需要生成一个标量或者一个向量，可使用 exec 子句。

#### 2.2.8 group by 子句有哪些注意事项？

group by 子句默认会返回分组列，如果 select 聚合函数(分组列) as 分组列时，会返回错误 Duplicated column
name（如下示例代码4）；group by 子句 必须使用聚合函数，否则会返回 All columns must be of the same
length（如下示例代码5）。

```
tb = loadTable("dfs://stock_lv2_snapshot", "snapshot")
//示例代码1：正确
select sum(TotalVolumeTrade) as tot from tb
where tradeDate = 2022.01.05 group by SecurityID
//示例代码2：正确
select SecurityID  , sum(TotalVolumeTrade) as tot from tb
where tradeDate = 2022.01.05 group by SecurityID
//示例代码3：正确
select min(SecurityID) as sid , sum(TotalVolumeTrade) as tot from tb
where tradeDate = 2022.01.05 group by SecurityID
//示例代码4：错误
select min(SecurityID) as SecurityID , sum(TotalVolumeTrade) as tot from tb
where tradeDate = 2022.01.05 group by SecurityID
//示例代码5：错误
select SecurityID as sid , sum(TotalVolumeTrade) as tot from tb
where tradeDate = 2022.01.05 group by SecurityID
```

#### 2.2.9 where 条件中如何过滤数组向量？

可以通过 `byRow` 函数，实现在 where 条件中过滤数组向量。

```
t = table(fixedLengthArrayVector([1, 2, 3, 4], [3, 4, 5, 6], [5, 6, 7, 8]) as ids,
[1.0, 2.0, 3.0, 4.0] as value);
select * from t where rowAnd(byRow(eq{[4, 6, 8]}, ids))
```

#### 2.2.10 插入数据（append!）有哪些注意事项？

该函数不会检查两表中各列列名与顺序，只要两表中对应位置的列的数据类型一致，即可执行。所以，对数据表进行 `append!`
操作时，请检查两表中各列列名与顺序，以免出错。

### 2.3 DLang 语言语法类

本节将介绍在使用 DLang 语言中的一些常见语法及功能特点，如单双引号和反引号的区别、CHAR 类型和SYMBL 转换、除法运算中斜杠与反斜杠的区别、 NULL
和空字符串及 NaN 的区别、如何查看变量类型、如何取消变量定义、时间类型数据转换、浮点数据精度及比较、字符串格式化等相关问题。

#### 2.3.1 单引号、双引号和反引号的区别

| 符号 | 主要用途 | 主要区别或注意事项 |
| --- | --- | --- |
| 单引号 | 定义字符串或字符 | 当单引号内为单个字符时，为字符类型 CHAR，如 ‘A’ 为 CHAR 类型，而非 STRING 类型。  当单引号内为多个字符时，为字符串类型 STRING，与双引号没有区别。 |
| 双引号 | 定义字符串 | 能包含特殊字符。 |
| 反引号 | 定义字符串 | 不能包含特殊字符。 |

#### 2.3.2 CHAR 类型不会自动转换到 SYMBOL 类型

错误代码示例：

```
symVec = [`a, `b, `c, `d]$SYMBOL
c = 'a'
symVec.append!(c) // append!(symVec, c) => Failed to append data
```

而 STRING 类型会自动转换到 SYMBOL 类型。如下为更改后的正确代码示例：

```
symVec.append!(c.string())
```

#### 2.3.3 除法运算中，斜杠 / 和反斜杠 \ 的区别

当被除数和除数，有任意一个类型为浮点型时，二者没有区别。

当被除数和除数，都为整型时，反斜杠 \ 除法运算的结果为浮点型，保留小数部分；而斜杠 / 会对除法运算的结果取整，所得结果为整型。

代码示例：

```
100 / 2.1 // 47.61904761904762
100 \ 2.1 // 47.61904761904762
100.0 / 3 // 33.333333333333336
100.0 \ 3 // 33.333333333333336
100 \ 3   // 33.333333333333336
100 / 3   // 33
```

#### 2.3.4 NULL、空字符串和 NaN 的区别

| 概念 | 类型 | 表示方法 |
| --- | --- | --- |
| NULL | VOID 或有类型空值 | NULL、int()、00i 等 |
| 空字符串 | STRING 类型 | "" |
| NaN | FLOAT 或 DOUBLE 类型 | 计算溢出，表示无效的数值计算结果 |

#### 2.3.5 如何查看变量的数据类型

通过 `typestr` 函数查看任意数据类型。

```
symVec = [`a, `b, `c, `d]$SYMBOL
t = table(1 2 3 as id, symVec as symbol, 1 2 3 as value)
d = dict(`a`b`c, 1 2 3)
typestr symVec // FAST SYMBOL VECTOR
typestr t // IN-MEMORY TABLE
typestr d // STRING->INT DICTIONARY
```

#### 2.3.6 如何取消变量的定义

| 变量类型 | 取消它的函数 |
| --- | --- |
| 本地变量 | undef(`var) |
| 共享变量 | undef(`var, SHARED) |
| 函数定义 | undef(`def, DEF) |
| 流数据表 | dropStreamTable(`streamTableDemo) |
| 流式引擎 | dropStreamEngine(`streamEngineDemo) |

#### 2.3.7 时间类型及转换相关问题

**DATETIME 类型日期的年份为什么变成了 1970 ？**

这通常是由于时间值发生整型溢出所致。在 DolphinDB 中，DATETIME 底层采用 32 位 INT 表示，其可表示的时间范围为
[1901.12.13T20:45:53, 2038.01.19T03:14:07]。当时间超出该上限时，会发生整数溢出，最终显示为 1970
年的异常值。

对于超出该范围的时间数据，建议使用 TIMESTAMP 类型以避免溢出问题。

**如何转换 DATE 类型为 DATETIME 或 TIMESTAMP 类型？**

使用 `datetime` 或 `timestamp` 函数进行转换。代码示例：

```
datetime(2025.07.09)
timestamp(2025.07.09)
```

**如何合并 DATE 类型和 TIME 类型为 DATETIME 或 TIMESTAMP 类型?**

使用 `concatDateTime` 函数进行转换。代码示例：

```
concatDateTime(2025.07.09, 09:30:00)
concatDateTime(2025.07.09, 09:30:00).timestamp()
```

**如何转换 LONG 类型为 DATETIME 或 TIMESTAMP 类型**

使用 `datetime` 或 `timestamp` 函数进行转换。代码示例：

```
datetime(1752053400)
timestamp(1752062327626)
```

**如何转换 STRING 类型为 DATETIME 或 TIMESTAMP 类型**

使用 `temporalParse` 函数。代码示例：

```
dateStr = "2025.07.09"
temporalParse(dateStr, "yyyy.MM.dd").date()  // 解析为日期
dateStr = "2025.07.09 11:58:47.626"
temporalParse(dateStr, "yyyy.MM.dd HH:mm:ss.SSS").timestamp()  // 解析为时间戳
```

#### 2.3.8 浮点数相关问题

**浮点数的小数点后为什么有很多位？源库里面为 1115.52，同步至 DolphinDB 后变成了 1115.520000000000200000
。**

由于二进制存储机制与十进制转换的不可调和性‌，计算机在存储浮点型数据时总是会存在精度问题。如何解决该问题：

* 可以使用 `round` 函数按照指定小数位数进行四舍五入运算。
* 可以使用 DECIMAL 类型替代 FLOATING 类型。

**浮点数导出到 csv 时如何控制小数点后的有效位数？**

使用 `round` 函数按照指定小数位数进行四舍五入运算。

**浮点数如何比较大小？**

使用 `eqFloat` 函数。

**浮点数如何向下取整、向上取整、四舍五入取整？**

`floor` 函数用于向下取整， `ceil` 函数用于向上取整，
`round` 函数用于四舍五入取整。

#### 2.3.9 如何对字符串格式化、对齐或填充？

使用 `stringFormat` 函数。代码示例：

```
// 右对齐（宽度10，空格填充）
stringFormat("%10W", "DolphinDB") // 输出 " DolphinDB"
// 左对齐（宽度10，零填充）
stringFormat("%010l", 123l) // 输出 "0000000123"
```

#### 2.3.10 如何判断字符串是否包含了某个字符或字符串？

使用 `strpos` 或 `strFind` 函数。代码示例：

```
strpos("Hello, DolphinDB!", "Dolphin")  // 输出 7
```

#### 2.3.11 如何从字符串中提前指定字符或字符串？

通过 `regexFindStr` 或 `substr` 等函数。以
AP210\_ZCE\_20220701.txt 为例，如何提取 20220701。代码示例：

```
fileName = "AP210_ZCE_20220701.txt"
regexFindStr(fileName, "[0-9]{8}")  // 输出 '20220701'
substr(fileName, 10, 8)  // 输出 '20220701'
split(fileName, "_").last().split(".").first() // 输出 '20220701'
```

#### 2.3.12 向量中，如何获取大于指定值的元素的索引？

代码示例：

```
v = 1 2 3 4 5 6 7 8 9 10
index = 1..v.size()
index[v > 3]
```

#### 2.3.13 字典相关问题

**如何将字典 dict 转换为表 table？**

使用 transpose 函数。代码示例：

```
d = dict(`sym`val, [`a`b`c, 1 2 3])
transpose(d)
```

**如何删除字典中的某个 key？**

使用 erase! 函数。代码示例：

```
d = dict(`sym`val, [`a`b`c, 1 2 3])
erase!(d, `sym)
```

#### 2.3.14 module 相关问题

**如何通过 VSCode 上传 module？**

安装了 DolphinDB VSCode Extension 后，VSCode 右上角会有一个上传功能。首先，选择需要上传的 module
文件，然后依次点击“上传”、“DolphinDB: 上传模块”，并在弹出的对话框中选择是否加密，详细操作如下图所示。

![](image/usage_guidelines/1.PNG)

![](image/usage_guidelines/2.PNG)

**use module 提示无法找到该模块**

可能的原因：

1. module 上传的节点和客户端连接的节点是否为同一个。
2. dos 文件名称和 dos 文件内定义的 module 名称是否一致。
3. module 是否上传到了 Home 路径下。

**新的 module 重新上传后，为什么用的还是旧的 module？**

可能的原因：

1. 新的 module 上传的节点和客户端连接的节点是否为同一个。
2. module 有缓存，使用 `clearCachedModules` 函数清理一下，再次尝试。
3. 如果使用 VSCode 上传 module，可以断开当前连接，重新连接后，再次上传 module 即可引用新的 module。

### 2.4 运维类

本节将介绍在使用 DolphinDB 过程中一些常见的运维操作，如安全关机、磁盘空间、数据迁移、常用文件目录配置、系统故障排查、及需咨询 DolphinDB
技术人员并在其支持下完成的一些重要操作。

#### 2.4.1 关于安全关机

由于安全关机会在系统关闭前完成事务刷盘，关停服务时间有可能较慢，所以在安全关机后（stopSingle.sh/stopAllNode.sh）需确认是否关闭成功，再重启服务，否则可能会造成节点端口仍被绑定导致重启无法成功。参见
安全关机。

#### 2.4.2 关于磁盘空间

建议按照运维要求监控磁盘空间使用情况，在磁盘空间使用率达到设定的阈值时及时告警，否则一旦磁盘空间占满会导致无法写入数据、写入数据不完整、系统卡死等无法预料的问题，且因此无法及时快速恢复服务。

#### 2.4.3 关于数据迁移

数据迁移时，建议使用 `backup` 系列函数对数据进行备份，并通过 `restore`
系列函数完成数据恢复与导入。不建议直接拷贝底层数据文件进行迁移，以避免数据不一致或元数据缺失等问题。

#### 2.4.4 关于系统文件

DolphinDB 服务部署目录及配置的数据存储目录（包括
dfsMetaDir、chunkMetaDir、volumes、TSDBRedoLogDir、persistenceDir、computeNodeCacheDir
等）中的文件，均为系统运行所依赖的重要数据，禁止随意修改或删除。

建议在配置数据存储路径时统一包含 DolphinDB
子目录（例如：chunkMetaDir=/ssd/ssd1/DolphinDB/chunkMeta/<ALIAS>），以明确标识为
DolphinDB 相关数据目录，从而降低误操作风险。

#### 2.4.5 系统故障排查

参见 故障排查。

#### 2.4.6 危险操作谨醒

某些操作可能导致系统无法启动、数据丢失等严重问题。对于以下列举的常见操作场景，建议在执行前咨询 DolphinDB 技术人员，并在其指导下进行。

* 磁盘操作：挂载、卸载、扩容、缩容、更换。
* 修改 hostname。
* 修改 IP。
* 修改数据存储目录配置：volumes、dfsMetaDir、chunkMetaDi、redoLogDir、TSDBRedoLogDir。

### 2.5 其它类

本节将介绍在使用 DolphinDB 过程中常被问及的一些问题，如升级 server 或更新 license
是否必须重启集群、普通用户如何更改自身密码、如何统计库表所占磁盘空间，如何查看用户的内存使用情况。

#### 2.5.1 升级 server 或更新 license，必须重启 DolphinDB 集群吗？

升级 server，必须重启 DolphinDB 集群。而更新 license，有在线和离线两种方式。

在线更新 license，可以使用 `updateLicense` 函数，也可以使用封装过的 ops 运维函数库中的
`updateAllLicenses` 函数。在线更新 license 有一些限制条件，详见文档中心 高可用集群部署与升级
授权许可文件过期更新。

离线更新 license，替换原有的 license 后重启即可。

#### 2.5.2 普通用户如何更改自己的密码？

使用 `changePwd` 函数。

#### 2.5.3 如何统计数据库或数据表占用的磁盘空间？

使用 ops 运维函数库中的 `getTableDiskUsage` 函数。

#### 2.5.4 如何查看用户的内存使用情况？

使用 `getSessionMemoryStat` 函数。

## 3. 小结

本文总结了 DolphinDB 初学者在使用 DolphinDB 时常见的一些基础知识，涵盖库表类、SQL 类、DLang
语言语法类、运维类等方面，方便使用者快速查阅。更全面说明详见文档中心关于 DolphinDB。
