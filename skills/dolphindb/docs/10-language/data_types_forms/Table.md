<!-- Auto-mirrored from upstream `documentation-main/progr/data_types_forms/Table.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 表

表是数据库的重要组成部分，用于表达数据以及这些数据之间的联系。表由许多列组成，每一列都必须指定列名和数据类型，并且存储了对应类型的数据。可以对表中的数据进行增加，删除，更新和查询操作。

DolphinDB 中数据表有以下几类：

* 内存表

  + 普通内存表（table），最基础的表结构，常用于临时数据存储。
  + 索引内存表（indexedTable），适用于存取键值对数据的场景，范围查询性能更优。
  + 键值内存表（keyedTable），适用于存取键值对数据的场景，单点查性性能更优。
  + 流数据表（streamTable, haStreamTable），用于流数据的实时接收和存储。
  + mvcc 内存表（mvccTable），适用于频繁查询，但写入、更新、删除频率不高的场景。
  + 分区内存表（createPartitionedTable），各分区可并行计算，适用于数据量较大且对性能有要求的场景。
  + 缓存表（cachedTable），提供了缓存并定时更新数据的功能，适用于同步实时性要求不高的数据。
  + 内存在线事务处理表（createIMOLTPTable），通过主键和索引加速查询，适用于对响应时间有严格要求的低延时场景。
* 分布式表

  + 分布式分区表（createPartitionedTable），最常见的分布式表结构，多用于大规模数据存储和高并发请求的场景。
  + 维度表（createDimensionTable），在分布式数据库中没有分区的表，适用于存储不频繁更新的小数据集。

## 创建表

本节介绍内存表的创建。创建内存表时，表名和列名必须由中文或英文字母、数字或下划线 (\_) 组成，且必须以中文或英文字母开头。

2.00.2 版本开始，由 pivot by, addColumn
操作产生的列名，支持包含特殊字符，或以数字开头。

请注意：

* 包含特殊符号或以数字开头的列名在 SQL 中引用时，需将列名用双引号引用，并在其之前使用下划线作为标识，例如：\_"IBM.N",
  \_"000001.SH"；
* 列名包含特殊符号或以数字开头的列亦可通过 tb["col"]，tb."col" 的方式访问。
* 进行 pivot by 需要对空数据赋予列名时，会赋予列名"NULL"，引用时需要遵循上述第一条规则（\_"NULL")。

为了与之前版本的代码兼容，引入了配置项 *removeSpecialCharInColumnName*，默认值是
false，表示允许列名包含特殊字符。如果要跟以前兼容，可以将该变量配置为 true。

例1：创建内存表的三种方式。

（1）`table(X as col, [X1 as col1], [X2 as col2],
.....)`

```
t0=table(1 2 3 as a, `x`y`z as b, 10.8 7.6 3.5 as c);
t0;
```

| a | b | c |
| --- | --- | --- |
| 1 | x | 10.8 |
| 2 | y | 7.6 |
| 3 | z | 3.5 |

（2）`table(X, [X1], [X2], .....)`

```
x=1 2 3;
y=4 5 6;
t1=table(x,y);
t1;
```

| x | y |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

（3）`table(capacity:size, colNames, colTypes)`

```
t2=table(200:10, `name`id`value, [STRING,INT,DOUBLE]);
t2;
```

| name | id | value |
| --- | --- | --- |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |
|  | 0 | 0 |

例2：列名包含特殊符号的内存表创建与查询。

```
t3=table(1 2 3 as `_a, 4 5 6 as "2 ab");
t3;
```

| \_a | 2 ab |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
select _"_a" as "_aa", _"2 ab" as "2ab" from t3;
```

| \_aa | 2ab |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

例3：将向量或矩阵转换为表。

```
a=([1,2],[3.2,4.3],[2019.01.02,2019.05.03]);
table(a);
```

| C0 | C1 | C2 |
| --- | --- | --- |
| 1 | 3.2 | 2019.01.02 |
| 2 | 4.3 | 2019.05.03 |

```
m=1..12$3:4;
table(m);
```

| C0 | C1 | C2 | C3 |
| --- | --- | --- | --- |
| 1 | 4 | 7 | 10 |
| 2 | 5 | 8 | 11 |
| 3 | 6 | 9 | 12 |

## 查看表

使用 rows 或 size 函数查看表的行数

```
rows(t1);
// output: 3
size(t1);
// output: 3
```

使用 cols 函数查看表的列数

```
cols(t1);
// output: 2
```

使用 schema 函数查看表的结构

```
schema(t1);
/*
chunkPath->
partitionColumnIndex->-1
colDefs->
name typeString typeInt extra comment
---- ---------- ------- ----- -------
x    INT        4
y    INT        4
*/
```

## 访问表

DolphinDB 访问表的方式很灵活，既可以使用 SQL 语句，也可以使用类似 python 的语法。SQL 访问表的具体例子详见
[SQL语句](../sql/sql_intro.html "DolphinDB 中 SQL 语句的基本语法和用法")，下例主要说明如何通过类似 python
的语法读取表数据。

例1：可使用 <tableName>[X,Y] 访问表，其中 X 和 Y 可以是标量或数据对。X 用于选择行，Y
用于选择列。表索引的范围从 0 开始，不包含上限值。例如，1:3 包括 1 和 2。类似地，2:0 表示 1 和 0。

```
t1[1:3, 1];
```

| y |
| --- |
| 5 |
| 6 |

```
t1[,t1.columns()-1];
```

| y |
| --- |
| 4 |
| 5 |
| 6 |

```
t1.keys();

["x","y"]

t1.values();

([1,2,3],[4,5,6])
```

例2：条件访问数据表。

```
t1[t1.x>2];      // 查询 x>2 的行

or
t1[t1[`x]>2];
```

| x | y |
| --- | --- |
| 3 | 6 |

```
t1[t1.x in (1 3)];       // 查询 x=1 或 x=3 的行
```

| x | y |
| --- | --- |
| 1 | 4 |
| 3 | 6 |

```
t1[t1.x>1 && t1.y<6];       // 查询 x>1 和 y<6 的行
```

| x | y |
| --- | --- |
| 2 | 5 |

## 更新表

例1：根据条件更新内存表。

```
t1[`x, t1[`x] < 2] = 3

or
t1[`x, <x < 2>] = 3
```

| x | y |
| --- | --- |
| 3 | 4 |
| 2 | 5 |
| 3 | 6 |

例2：通过赋值语句添加或更新表。

创建一个空表并插入数据：

```
t = table(100:0, `x`y`z, `STRING`DATE`DOUBLE);
// 创建一个具有三列 x, y, z 的表，数据类型分别为 STRING, DATE, DOUBLE。表的容量为 100，初始长度为 0。

t;
```

| x | y | z |
| --- | --- | --- |
|  |  |  |

```
insert into t values(take(`MS,3),2010.01.01 2010.01.02 2010.01.03, 1 2 3);
t;
```

| x | y | z |
| --- | --- | --- |
| MS | 2010.01.01 | 1 |
| MS | 2010.01.02 | 2 |
| MS | 2010.01.03 | 3 |

```
t=table(1 2 3 as id, 4 5 6 as value);
t;
```

| id | value |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
t[`id`name]=[7 8 9, `IBM`MSFT`GOOG];
t;
```

| id | value | name |
| --- | --- | --- |
| 7 | 4 | IBM |
| 8 | 5 | MSFT |
| 9 | 6 | GOOG |

例3：通过 SQL update 语句更新表。

```
n=10
colNames = `time`sym`id
colTypes = [DATE,SYMBOL,INT]
t = table(n:0, colNames, colTypes)
insert into t values(2020.01.05 13:30:10.008, `A1, 1)
insert into t values(2020.01.06 13:30:10.008, `A2, 2)
// 插入数据的时间类型与内存表时间类型不一致时，会自动转换为内存表时间列的类型。
insert into t values(2020.06M, `A3, 3)

update t set time=2020.06.13 13:30:10 where sym=`A1
select * from t
```

| time | sym | id |
| --- | --- | --- |
| 2020.06.13 | A1 | 1 |
| 2020.01.06 | A2 | 2 |
| 2020.06.01 | A3 | 3 |

## 删除表

* 通过函数 dropTable 和 truncate 可以一次性删除所有分布式表数据。
* 通过 delete
  语句可以删除指定条件的表（内存表或分布式表）数据。

详情参考 DropDatabaseandTable 页面的说明。
