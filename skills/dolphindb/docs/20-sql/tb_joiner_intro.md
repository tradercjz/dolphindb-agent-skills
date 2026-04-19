<!-- Auto-mirrored from upstream `documentation-main/progr/sql/tb_joiner_intro.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 表连接

## 概述

表连接是将数据库中多个表的数据关联起来的操作。通过表连接条件的指定，可以在查询中获取来自不同表的相关信息，从而实现更复杂的检索。本节介绍 DolphinDB
中表连接的基础用法，帮助用户更好地利用数据库中的数据。

注：

* 数组向量（ARRAY VECTOR）、元组（ANY VECTOR）以及 BLOB 类型的列不可作为连接列。
* 执行任意类型的表连接操作时，所有参与连接的表或子查询结果都必须具有唯一的名称或别名，否则会报错。

从 2.00.9 版本开始，在连接一个表或 SQL 查询的结果（包括嵌套连接）时，可以为表或 SQL 查询的结果指定别名。DolphinDB
也支持在连接时为维度表设置别名。例如：

```
t1= table(1 2 3 3 as id, 7.8 4.6 5.1 0.1 as value)
t2 = table(5 3 1 as id, 300 500 800 as qty);
select * from t1 a inner join t2 b on a.id = b.id
select * from t1 as a inner join t2 as b on a.id = b.id
select * from t1 a inner join (select * from t2 where id=3) b on a.id = b.id
```

以上查询语句用于表连接操作，其中：

1. ```
   select * from t1 a inner join t2 b on a.id = b.id
   ```

   这条查询语句根据 t1 表（别名：a）和 t2 表（别名：b）中 id 列的匹配来连接这两个表，然后使用 `select
   *` 查询所有列的数据，返回符合连接条件的记录。连接条件是 t1 表中的 id 列等于 t2 表中的 id 列。
2. ```
   select * from t1 as a inner join t2 as b on a.id = b.id
   ```

   这条查询语句与上一个查询语句是等价的，只是使用了别名代指表 t1 和 t2。
3. ```
   select * from t1 a inner join (select * from t2 where id=3) b on a.id = b.id
   ```

   这条查询与前两条不同，它使用了子查询：
   1. ```
      select * from t2 where id=3
      ```

      先从 t2 表中选择 id 等于 3 的行
   2. 再将结果与表 t1 进行连接，连接条件为 `a.id = b.id`

## 表连接类型

inner join（内连接）
:   内连接是最基本的连接类型之一。它返回两个表中满足连接条件的行，即两个表中连接列的值相等的行。内连接排除了不匹配的行，只返回匹配的结果。

    ```
    select * from table1 inner join table2 on table1.column = table2.column;
    ```

left join/left outer join（左连接/左外连接）
:   左连接返回左表中的所有行，以及与右表匹配的行。如果右表中没有匹配的行，将返回 NULL 值。

    ```
    select * from table1 left join table2 on table1.column = table2.column;
    ```

right join/right outer join（右连接/右外连接）
:   右连接返回右表中的所有行，以及与左表匹配的行。如果左表中没有匹配的行，将返回 NULL 值。

    ```
    select * from table1 right join table2 on table1.column = table2.column;
    ```

full join/full outer join（全连接/全外连接）
:   全连接返回两个表中的所有行，如果没有匹配的行，将返回 NULL 值。

    ```
    select * from table1 full join table2 on table1.column = table2.column;
    ```

equi join（等值连接）
:   等值连接是基于相等条件进行的连接，通常使用等号 (=) 连接两个表的列。

    ```
    select * from table1 join table2 on table1.column = table2.column;
    ```

cross join（交叉连接）
:   交叉连接返回两个表的所有可能的组合，它不依赖于任何条件。

    ```
    select * from table1 cross join table2;
    ```

asof join（时序连接）
:   asof join是一种特殊的连接，通常用于处理时间序列数据，连接条件是时间列。

    ```
    aj(leftTable, rightTable, matchingCols, [rightMatchingCols])
    ```

window join（窗口连接）
:   窗口连接是一种通过窗口函数进行的连接，通常涉及到对窗口内的数据进行聚合或分析。

    ```
    wj(leftTable, rightTable, window, aggs, matchingCols, [rightMatchingCols])
    ```

    等效于：

    ```
    select * from table1 join table2 on table1.column = table2.column over (partition by table1.partition_column order by table1.column);
    ```

prefix join（前缀连接）
:   前缀连接是一种基于列名前缀匹配的连接，通常在列名相似但不完全相同的情况下使用。

    ```
    pj(leftTable, rightTable, matchingCols, [rightMatchingCols])
    ```

    等效于：

    ```
    select * from table1 join table2 on table1.column_prefix = table2.column_prefix;
    ```

有关表连接的详细用法，请浏览以下各节。
