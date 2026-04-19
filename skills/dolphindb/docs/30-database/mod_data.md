<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/mod_data.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 更新数据

DolphinDB 支持多种方式更新数据，包括 SQL 语句、update! 、upsert! 、replaceColumn!
以及赋值等方法。以下是各种方法适用的对象：

|  | **分布式表** | **普通内存表** | **键值内存表** | **索引内存表** | **mvcc 内存表** | **内存分区表** |
| --- | --- | --- | --- | --- | --- | --- |
| SQL 语句 | √ | √ | √ | √ | √ | √ |
| update! | × | √ | √ | √ | √ | √ |
| upsert! | √ | × | √ | √ | × | × |
| replaceColumn! | 仅支持 OLAP 更改数据类型 | √ | √ | √ | √ | × |
| 赋值 | × | √ | √ | √ | √ | √ |

本节示例脚本中，内存表 t 、键值内存表 kt 、索引内存表 it 、mvcc 内存表 mvcct、内存分区表 mpt、分布式分区表 pt 和维度表 dt
及其数据由以下脚本生成：

```
// 内存表
t = table(2023.10.01 + take(0..9,100) as date, take(["A001","B001","C001","D001"],100) as sym, 1..100 as val)
// 键值内存表
kt = keyedTable(`date,1:0,`date`sym`val,[DATE,SYMBOL,INT])
kt.tableInsert(t)
// 索引内存表
it = indexedTable(`date,1:0,`date`sym`val,[DATE,SYMBOL,INT])
it.tableInsert(t)
// mvcc 内存表
mvcct = mvccTable(1:0,`date`sym`val,[DATE,SYMBOL,INT])
mvcct.tableInsert(t)
// 内存分区表
db1 = database(directory="", partitionType=VALUE, partitionScheme=2023.10.01..2023.10.10)
mpt = createPartitionedTable(dbHandle=db1, table=t, tableName=`pt, partitionColumns=`date)
mpt.tableInsert(t)
// 分布式分区表 pt 和维度表 dt
db = database("dfs://olapdemo",partitionType=VALUE, partitionScheme=2023.10.01..2023.10.10)
pt = createPartitionedTable(dbHandle=db, table=t, tableName=`pt, partitionColumns=`date)
pt.tableInsert(t)
dt = createDimensionTable(dbHandle=db, table=t, tableName=`dt)
dt.tableInsert(t)
```

下文中，如不明确说明内存表的具体类型，则内存表指代除流数据表外其他类型的内存表，包括普通内存表、键值内存表、索引内存表、mvcc 内存表和内存分区表。

## SQL 语句

UPDATE 语句用于修改内存表或分布式表的数据。

例如，将表 t 中 2023.10.01 的数据 val 值更新为 101，将表 pt 中 2023.10.2 的数据 val 值更新为102 ：

```
// 更新内存表
UPDATE t SET val=101 WHERE date=2023.10.01

// 更新分布式分区表
UPDATE pt SET val=102 WHERE date=2023.10.02
```

注：

在分布式表多版本控制机制下，更新操作在短时间内可能导致磁盘占用率上升。

## upsert!

upsert! 函数可用于更新键值内存表、索引内存表和分布式表数据。

下例中，使用表 t1 中的数据更新键值内存表、索引内存表。若 t1 表中 date 列的值在待更新的表中已存在，则更新该主键值的数据；否则添加数据：

```
t1 = table(2023.10.03..2023.10.05 as date, ["X001","Y001","Z001"] as sym, 66 77 88 as val)
upsert!(obj=kt, newData=t1, keyColNames=`date)
upsert!(obj=it, newData=t1, keyColNames=`date)
```

对于分布式表，由于分布式分区表和维度表都没有键值，必须指定参数 *keyColNames*，且参数 *keyColNames*
会与分区列一起组成键值列：

```
t1 = table(2023.10.03..2023.10.05 as date, ["X001","Y001","Z001"] as sym, 66 77 88 as val)
upsert!(obj=pt, newData=t1, keyColNames=`sym)
upsert!(obj=dt, newData=t1, keyColNames=`sym)
```

注：

upsert!
在更新分布式表时，如果在参数 *keyColNames* 指定的列上存在重复值，仅会更新第一个值所在行，其余行不会更新。

## update!

update! 函数可用于更新内存表数据。

通过指定表中已有的列，将该列数据更新。以下脚本将表 t 中时间为 2023年10月03日，sym 为 ”A001“ 对应的 val 改为原值加 2：

```
update!(table=t, colNames="val", newValues=<val+2>, filter=[<date=2023.10.03>,<sym="A001">])
```

通过指定表中不存在的列，为表增加该列。以下脚本为表 t 增加一列 val2，其值为从 1 到 100：

```
update!(table=t, colNames="val2", newValues=1..100)
```

## replaceColumn!

`replaceColumn!` 函数可用于更新普通内存表、键值内存表、索引内存表、mvcc
表数据。此方法可以通过列替换更新表中某一整列数据，替换的新向量必须与表的现有行数一致。

对采用 OLAP 存储引擎的分布式表，`replaceColumn!`
函数可用于改变非分区列的数据类型。此时不要求新向量的长度与表的行数一致，新向量仅用于指示转换后的类型。

```
// 更新普通内存表，共 100 行
replaceColumn!(table=t, colName="val", newCol=101..200)

// 更新键值内存表和索引内存表，共 10 行
replaceColumn!(table=kt, colName="val", newCol=101..110)
replaceColumn!(table=it, colName="val", newCol=101..110)

// 将分布式分区表 pt 中为 INT 类型的 val 列改为 DOUBLE 类型
replaceColumn!(table=pt, colName="val", newCol=array(DOUBLE,0))
```

## 赋值

对内存表的已有列进行整列赋值，更新此列的数据：

```
t[`val] = 66
```

对某一条数据的某个字段进行赋值，例如更新 val
列第一行的值：

```
t[`val,0] = 100
```

**相关信息**

* [UPDATE](../progr/sql/update.html "UPDATE")
* [update!](../funcs/u/update_.html "update!")
* [upsert!](../funcs/u/upsert_.html "upsert!")
* [replaceColumn!](../funcs/r/replaceColumn_.html "replaceColumn!")
