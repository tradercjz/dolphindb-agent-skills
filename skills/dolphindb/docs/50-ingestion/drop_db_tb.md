<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db_oper/drop_db_tb.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 删除数据

删除数据需要执行用户具有相应权限，否则无法删除。关于删除权限，参考：用户权限管理。

DolphinDB 提供了多种方法删除数据，既可通过 SQL 语句或函数方法直接删除数据，也可通过设置数据保留方案定期删除过期数据。本文重点介绍 SQL
语句和函数方法，自动删除过期数据请参考分级存储。

注：

SQL 语句中关键字大小写不敏感。

## 通过 SQL 语句删除数据

可以使用 [DELETE](../../progr/sql/delete.dita) 语句从表中删除数据：

```
DELETE FROM <table> WHERE ...
```

下例删除内存表 t 中日期早于为 2023.10.05 的数据：

```
t = table(2023.10.01 + take(0..9,100) as date, take(["A01","B01","C01","D01"],100) as sym, 1..100 as val)
delete from t where date < 2023.10.05
```

下例删除分布式表 pt 中日期早于为 2023.10.05 的数据：

```
db = database("dfs://olapdemo",partitionType=VALUE, partitionScheme=2023.10.01..2023.10.10)
pt = createPartitionedTable(dbHandle=db, table=t, tableName=`pt, partitionColumns=`date)
pt.tableInsert(t)

delete from pt where date < 2023.10.05
```

注：

* 使用 `DELETE` 语句删除数据，会首先根据 `WHERE`
  子句过滤数据，将相关分区的数据加载到内存，然后删除特定数据，再将其余数据写回数据库。多版本并发控制机制会将此版本数据存储在磁盘上的另一个文件。这样可以确保在删除操作完成前，用户仍可以查询完整的删除前的数据。因此此时磁盘占用可能会高于删除前。当一段时间后旧版本回收删除时，磁盘空间就可以释放。因此使用
  `DELETE` 语句删除分布式表的数据，需要有足够的内存和磁盘空间。
* `WHERE`
  子句的过滤条件应包含分区字段，如果没有，则会将所有分区的数据加载到内存处理，容易造成内存资源紧张。

该函数在性能方面较 `DELETE` 语句以及 dropPartition 函数均有数倍提升。

```
truncate(dbUrl="dfs://olapdemo", tableName="pt")
```

## 通过函数删除数据

### truncate 函数

truncate
可以删除分布式表中的所有数据，并保留表结构。

该函数在性能方面较 `DELETE` 语句以及 `dropPartition`
均有数倍提升。

```
truncate(dbUrl="dfs://olapdemo", tableName="pt")
```

### clear! 函数

clear!
函数可以删除内存表中的所有数据。

```
t = table(2023.10.01 + take(0..9,100) as date, take(["A01","B01","C01","D01"],100) as sym, 1..100 as val)
clear!(t)
```

### erase! 函数

erase!
函数可以删除内存表中符合条件的数据。

```
t = table(2023.10.01 + take(0..9,100) as date, take(["A01","B01","C01","D01"],100) as sym, 1..100 as val)
erase!(obj=t,filter=<date<2023.10.05>)
```

### drop 函数

drop 函数删除内存表中前 n 条或后 n 条数据。

注：

由于 `drop`
函数不会修改原对象的值，用其删除数据时需使用赋值语句将其返回结果重新赋值给原对象。

```
t = table(2023.10.01 + take(0..9,100) as date, take(["A01","B01","C01","D01"],100) as sym, 1..100 as val)
t = drop(t,10)
```

## 不同删除方法的区别

* 当有一个查询正在进行时，使用 `DELETE`
  语句删除该表数据不会影响此查询，`truncate`会导致查询失败。
* `DELETE` 在执行过程中，可以通过 [cancelJob](../../funcs/c/cancelJob.dita) 或切断连接等方式中止删除；`truncate`
  一旦开始执行，除非遇到不可预见的错误导致删除失败，无法中止。
* 由于 `DELETE` 会占用额外的磁盘空间，因此当磁盘空间紧张需要删除数据释放空间时，应使用
  `truncate` 。
* 有一个包含大量数据的分布式表：

  + 如果要删除所有数据，应使用 `truncate`；
  + 如果要删除部分数据，应先分析需要删除的数据，尽可能结合使用 `dropPartiton` 和
    `DELETE`，或将某个分区中要保留的数据查到内存，`dropPartition`
    后再将保留的数据写回。

**相关信息**

* [cancelJob](../../funcs/c/cancelJob.dita "cancelJob")
* [clear!](../../funcs/c/clear_.html "clear!")
* [DELETE](../../progr/sql/delete.dita "DELETE")
* [drop](../../funcs/d/drop.html "drop")
* [dropPartition](../../funcs/t/truncate.html "dropPartition")
* [erase!](../../funcs/e/erase_.html "erase!")
* [truncate](../../funcs/t/truncate.html "truncate")
