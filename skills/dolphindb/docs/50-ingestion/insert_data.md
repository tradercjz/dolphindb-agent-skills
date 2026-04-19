<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db_oper/insert_data.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 插入数据

DolphinDB 支持通过 `INSERT INTO` 语句、 `append!` 和
`tableInsert` 函数向表中插入数据。本页面将介绍这些方法的使用方式以及常见问题。

## 插入方法

DolphinDB 提供了三种方法，向分布式表和内存表插入数据：

* `INSERT INTO` 语句
* `append!` 函数
* `tableInsert` 函数

### INSERT INTO 语句

通过 INSERT INTO 语句的
`VALUES` 子句可以插入数据。此方法默认仅支持内存表，不适用于分布式表。要对分布式表中使用此方法，可以启用配置项
enableInsertStatementForDFSTable，详细信息请参考 数据库与数据表。

#### 插入所有列

如果不指定列，默认插入所有列。此时在 `VALUES` 关键字后的括号中按照表的列顺序提供相应的值。

```
// 插入所有列
INSERT INTO <tableName> VALUES (val1, val2, val3, ...);
```

#### 插入指定列

如果只想插入表的某几列，可以在表名后的括号中指定列名，`VALUES`
关键字后的括号中按照指定列的顺序提供相应的值，未指定列的对应值将填充为 NULL。如果插入的是分区表，则指定的列中必须包含分区列。

```
// 插入指定列 col1,col2,col3...
INSERT INTO <tableName> (col1, col2, col3, ...) VALUES (val1, val2, val3, ...);
```

向表 t 中插入1 行只包含 id 和 sym 两列的数据，val 列为空。

```
t = table(1:0,`id`sym`val,[INT,STRING,DOUBLE])
// 插入 1 行只包含 id, vale 两列的数据
INSERT INTO t (id,val) VALUES (1,7.6)
```

向表中插入多行数据有两种写法：

* 逐行定义数据，values 关键字后每个括号代表一行

  ```
  insert into t values (2, "A02", 2.2),(3, "B03", 3.3)
  ```
* 按列定义数据，values 关键字后的括号内为等长向量，对应表 t 的各列

  ```
  insert into t values ([5,6], ["C05","D06"], [5.5,6.6])
  ```

### append! 函数

append!函数可将一个与原表结构相同的表整体追加到原表中。

```
t = table(1:0,`id`sym`val,[INT,SYMBOL,DOUBLE])
tmp = table(1..10 as id, take(`A001`B001,10) as sym, rand(10.0,10) as val)
append!(t,tmp)
```

注：

`append!`
函数并不会检查两表的列名和顺序，只要两表每列的数据类型一致即可执行，也不会根据列名进行对齐。因此，对数据表进行 `append!`
操作时，需要仔细检查表结构是否一致，以免出错。

### tableInsert 函数

tableInsert
可用于将表、元组、字典，或多个向量或元组加入原表中。

不同于 `append!` 的是，`tableInsert` 会返回此次插入成功的条数。

例如，向一个分区内存表中插入 10 条数据，此分区内存表只有 5 个分区，在这 5 个分区内的数据成功插入，其余数据被舍去。

```
db = database("", VALUE, 1..5)
schemaTb = table(1:0, `id`sym`val, [INT,SYMBOL,DOUBLE])
t = db.createPartitionedTable(schemaTb, `mpt, `id)

tmp = table(1..10 as id, take(`A`B,10) as sym, rand(10.0,10) as val)
tableInsert(t, tmp)
// output:5
```

## 向分布式表插入数据注意事项

### 数据大小限制

* 插入 STRING 类型数据时，每个 STRING 不能超过 64KB，超过 64KB 的部分会被截断。
* 插入 BLOB 类型数据时，每个 BLOB 不能超过 64MB，超过 64MB 的部分会被截断。
* 插入 SYMBOL 类型数据时，每个 SYMBOL 不能超过 255B，超出时会抛出异常。

### 特殊字符处理

如果数据库为 VALUE 分区，且分区列为 STRING 类型或 SYMBOL 类型，那么插入的分区列数据不能包含空格、"\n"、"\r" 和
"\t"，否则会插入失败并报错 `A STRING or SYMBOL column used for value-partitioning
cannot contain invisible characters.`

### 无序数据写入

存储引擎对数据的排序是异步的，因此插入有序和乱序数据对写入性能几乎没有影响。

数据在数据库中按照分区存储。其每个分区内部的顺序与选择的存储引擎有关：

* OLAP：分区内数据的顺序与插入的顺序相同。
* TSDB：在 levelfile 内会根据 *sortColumns* 进行排序。
* PKEY：在 levelfile 内会根据 *primaryKey* 进行排序。

### 原子性事务

向分布式表的多个分区插入数据，是否支持事务取决于创建数据库时的指定的参数 *atomic*：

* *atomic* 设置为
  'TRANS'，则支持事务。如果某个分区写入失败，例如被其他写入事务锁定而出现写入冲突，则本次写入事务全部失败。

  ```
  // 创建一个原子性层级为 TRANS 的数据库
  if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
  db1 = database("",VALUE,2024.01.01..2024.01.03)
  db2 = database("",HASH,[SYMBOL,4])
  db = database("dfs://test", COMPO, [db1,db2],,"TSDB","TRANS")
  tmp = table(1:0, `date`time`sym`val, [DATE,SECOND,SYMBOL,INT])
  pt = db.createPartitionedTable(tmp,`pt,`date`sym,,`time,ALL)

  // 后台提交任务模拟并发写入场景
  n =  100
  t1 = table(take(2024.01.01..2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
  t2 = table(take(2024.01.01..2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
  t3 = table(take(2024.01.01..2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
  submitJob("writeData1", "writeData1", tableInsert, pt, t1)
  submitJob("writeData2", "writeData2", tableInsert, pt, t2)
  submitJob("writeData3", "writeData3", tableInsert, pt, t3)

  // 任务完成后执行查询
  select count(*) from pt
  // output: 100
  ```

  通过 `getRecentJobs()`
  方法可以看到，有两个写入任务因为涉及的分区被其他事务锁定导致写入失败：`The openChunks operation
  failed because the chunk '/test/20240101/Key1/OQ' is currently
  locked and in use by transaction 3153.`
* 当此数据库事务的原子性层级为
  CHUNK，若某分区被其它写入事务锁定而出现冲突，系统会完成其他分区的写入，同时对之前发生冲突的分区不断尝试写入，尝试数分钟后仍冲突才放弃写入。此设置下，允许并发写入同一个分区，但由于不能完全保证事务的原子性，可能出现部分分区写入成功而部分分区写入失败的情况。同时由于采用了重试机制，写入速度可能较慢。

  ```
  if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
  db1 = database("",VALUE,2024.01.01..2024.01.03)
  db2 = database("",HASH,[SYMBOL,4])
  db = database("dfs://test", COMPO, [db1,db2],,"TSDB","CHUNK")
  tmp = table(1:0, `date`time`sym`val, [DATE,SECOND,SYMBOL,INT])
  pt = db.createPartitionedTable(tmp,`pt,`date`sym,,`time,ALL)

  n =  100
  t1 = table(take(2024.01.01..2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
  t2 = table(take(2024.01.01..2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
  t3 = table(take(2024.01.01..2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)

  submitJob("writeData1", "writeData1", tableInsert, pt, t1)
  submitJob("writeData2", "writeData2", tableInsert, pt, t2)
  submitJob("writeData3", "writeData3", tableInsert, pt, t3)

  // 任务完成后执行查询
  select count(*) from pt
  // output: 300
  ```

### 向分布式表插入大量数据

在已知分区结构的情况下，最好的方式是将数据按照分区划分后分别提交后台作业，如此既可以充分利用多线程并发写入，提高写入效率，又可以确保不会因为写入冲突而造成写入失败。

下例简单模拟了少量数据进行性能对比，当处理大批量的历史数据时，性能差距更加明显。

```
// 建库建表
if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
db1 = database("",VALUE,2024.01.01..2024.01.03)
db2 = database("",HASH,[SYMBOL,4])
db = database("dfs://test", COMPO, [db1,db2],,"TSDB")
tmp = table(1:0, `date`time`sym`val, [DATE,SECOND,SYMBOL,INT])
pt = db.createPartitionedTable(tmp,`pt,`date`sym,,`time,ALL)

// 模拟一亿条数据一次性写入
n = 100000000
t = table(take(2024.01.01..2024.01.03,n*3) as date,00:00:00 + 1..(n*3) as time, rand(`A`B`C`D`E`F,n*3) as sym, rand(100,n*3) as val)
timer pt.tableInsert(t)
// Time elapsed: 49329.098 ms

// 模拟一亿条数据，按照分区划分，分别提交三个后台作业
t1 = table(take(2024.01.01,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
t2 = table(take(2024.01.02,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
t3 = table(take(2024.01.03,n) as date, 00:00:00 + 1..n as time, rand(`A`B`C`D`E`F,n) as sym, rand(100,n) as val)
submitJob("writeData1", "writeData1", tableInsert, pt, t1)
submitJob("writeData2", "writeData2", tableInsert, pt, t2)
submitJob("writeData3", "writeData3", tableInsert, pt, t3)
// 通过 getRecentJobs() 查看耗时约为28秒。
```

### 插入现有分区以外的数据

对于 VALUE 分区或含有 COMPO 分区的 VALUE 层级，可通过设置配置参数
*newValuePartitionPolicy=add*，实现自动创建对应分区并写入数据。更多细节请参考增加分区。

## 常见问题解答

1. **问题1：如果列的数据类型不匹配，数据能成功插入吗？**

   这取决于插入列与目标列的数据类型之间能否进行隐式转换：如果能够进行隐式类型转换，会转换为目标类型后插入，但这可能会造成数据精度的损失；如遇到不能隐式转换的类型，则本次插入失败。

   例如存在一个表
   *t*，其中列 id 为 INT 类型，当向其写入 DOUBLE、CHAR 类型的数据时，会进行数据类型转换后写入；而向其写入
   STRING
   类型的数据，会因为无法进行类型转换导致插入失败。

   ```
   t = table(3:0,[`id],[INT])
   t.tableInsert(table(1.2 as id)) // 返回1
   t.tableInsert(table('a' as id)) // 返回1
   t.tableInsert(table("str" as id)) // Failed to append data to column 'id' with error: Incompatible type. Expected: INT, Actual: STRING
   ```
2. **问题2：如果列的顺序与目标表的列顺序不一致，数据能成功插入吗？**

   如果采用 `INSERT INTO`
   指定插入的列，则数据会按照列名，插入对应的列。

   ```
   t = table(1:0,`id`sym,[INT,STRING])
   INSERT INTO t (sym,id) VALUES ("AAA",1)
   ```

   其他情况下，会按照顺序依次写入，即尝试将待插入数据的第
   n 列插入到目标表的第 n
   列，与列名无关。此时如果存在数据类型不匹配的问题，插入能否成功取决于数据类型能否进行转换，详情参考**问题1**。
3. **问题3：如果插入的列数与目标表的列数不一致，数据能成功插入吗？**

   当插入的列数大于目标表时，插入总是失败。

   ```
   t = table(1:0,[`id],[INT])
   t.tableInsert(table(1 as id, 2 as val)) // The number of columns of the table to insert must be the same as that of the original table.
   ```

   当插入的列数小于目标表时：

   （1）对内存表：
   * 使用 `INSERT INTO` 语句指定插入的列
     + 如果插入分区表，则必须包含分区列；否则无法插入，且系统不会报错并丢弃对应数据。

       ```
       db = database("",VALUE,1..3)
       t = db.createPartitionedTable(table(1:0,`id`price`qty,[INT,DOUBLE,INT]),`pt,`id)
       INSERT INTO t (price,qty) VALUES (3.6,100)
       ```
     + 插入其它类型内存表，则插入成功。

       ```
       t = table(1:0,`id`price`qty,[INT,DOUBLE,INT])
       INSERT INTO t (price,qty) VALUES (3.6,100)
       ```
   * 使用 INSERT INTO 语句未指定插入的列，或使用 `tableInsert` 或
     `append!`
     插入，则插入失败，此时系统会报错。

     ```
     t = table(1:0,`id`price`qty,[INT,DOUBLE,INT])
     INSERT INTO t VALUES (3.6,100) //The number of table columns doesn't match the number of columns to append.
     t.append!(table(3.6 as price,100 as qty)) //The number of columns of the table to insert must be the same as that of the original table.
     t.tableInsert(table(3.6 as price,100 as qty)) //The number of columns of the table to insert must be the same as that of the original table.
     ```

   （2）对分布式表：
   * 插入分区表的数据必须包含分区列，否则插入失败。

     ```
     // 建库建表
     if(existsDatabase("dfs://test")) dropDatabase("dfs://test")
     db = database("dfs://test",VALUE,1..5)
     t = table(1:0,`sym`id`price`qty,[SYMBOL,INT,DOUBLE,INT])
     pt = db.createPartitionedTable(t,`pt,`id)
     ​
     // 插入数据
     pt.tableInsert(table("A" as sym)) //不包含分区列，失败报错 The number of columns of the current table must match that of the target table.
     pt.tableInsert(table("A" as sym, 1 as id)) // 包含分区列，返回1，插入成功。
     ```
   * 如果某一个分区内成功插入过 n 列数据，则不允许再向该分区插入 m（m<n）列数据，可以继续插入大于等于 n
     列的数据。

     ```
     // 创建库表
     if(existsDatabase("dfs://test1")) dropDatabase("dfs://test1")
     db = database("dfs://test1", VALUE, 1..5)
     t = table(1:0,`id`sym`price`qty,[INT,SYMBOL,DOUBLE,INT])
     pt = db.createPartitionedTable(t,`pt,`id)
     ​
     //插入数据
     pt.tableInsert(table(1 as id, "A" as sym)) // 返回1，成功向分区1中插入包含2列的数据
     pt.tableInsert(table(1 as id)) // 无法向分区1中插入包含1列的数据，报错 The data to append contains fewer columns than the schema.
     pt.tableInsert(table(1 as id, "A" as sym, 3.6 as price)) // 返回1，成功向分区1中插入包含3列的数据
     pt.tableInsert(table(2 as id)) // 返回1，成功向分区2中插入包含1列的数据
     ```
4. **问题4：tableInsert 返回结果不符合预期，可能是什么原因？**

   * 分区表写入分区范围外的数据，且分区不满足自动创建的条件，此时分区之外的数据没有写入。
   * 当写入键值表或者索引表时，如果要写入的数据在数据表中已经存在对应键值，则会更新该键值对应的数据，但写入成功的统计结果不会包含此条更新。因为写入成功的条数只包括新增的数据条数。
     下例中，一个键值表 *kt* 中，存在键值为 1 的数据，此时插入三条键值为 1、2、3 的数据，此时会更新键值为 1
     的数据，并插入键值为 2、3 的数据，而 `tableInsert` 返回 2，是指新插入了键值为
     2、3 的数据。

   ```
   kt = keyedTable(`id,1 as id, 1 as val)
   kt.tableInsert(table(1..3 as id, 7..9 as val)) // 返回2
   ```

**相关信息**

* [append!](../../funcs/a/append%21.html "append!")
* [INSERT INTO](../../progr/sql/insertInto.html "INSERT INTO")
* [tableInsert](../../funcs/t/tableInsert.html "tableInsert")
