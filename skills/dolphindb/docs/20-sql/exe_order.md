<!-- Auto-mirrored from upstream `documentation-main/progr/sql/exe_order.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 执行顺序

在 DolphinDB 中，SQL 语句各部分的执行顺序大致与其它系统中 SQL 一致。特别需要注意的是当使用
`context by` 子句时，`csort` 关键字或 `limit` /
`top` 子句的执行顺序。

以下为 DolphinDB 中 SQL 语句各部分的执行顺序：

1. `from` 子句

   `from` 子句中的表对象或者 lj，ej，aj 等表连接，会最先被执行。
2. `on` 子句

   `on` 子句会对 `from` 子句应用 `on`
   筛选，只保留符合连接条件的行。如果指定了 `left join(lj)`，`right join`
   等外连接，那么保留表中未匹配的行作为外部行添加到 `on` 子句产生的临时表中。
3. `where` 条件

   不符合 `where` 过滤条件的行会被舍弃。

   注：

   * 仅可处理 `from` 子句中的数据，不可使用 `select` 子句中不属于
     `from` 子句对象的新列名，例如通过 `as`
     进行重命名的列、计算结果列。
   * `where` 子句中使用 "," 或 "and" 时，执行顺序不同：由 ","
     连接的条件，将从左到右依次进行过滤，即先过滤最左边的条件，然后对临时结果表继续过滤下一个相邻的条件，直至过滤完最后一个条件，得到最终的结果表；而由
     "and" 连接的条件，将对所有条件基于原表过滤后再将结果取交集。
4. `group by` / `context by` /
   `pivot by` 子句

   经过 `where` 条件过滤的行会依据 `group by`
   / `context by` / `pivot by` 子句进行分组。
5. `csort` 关键字（仅为 `context by`
   子句提供）

   `context by` 通常与时间序列函数一起使用，每个分组中行的顺序对结果有直接影响。在
   `context by` 子句后使用 `csort`
   关键字，对每个组内的数据进行排序。
6. `having` 条件（若使用了`group by` /
   `context by` 子句）

   若使用了`group by` / `context by`
   子句，则对每组使用 `having` 条件过滤，不满足条件的组被舍弃。与 `where`
   条件相同，`having` 条件中亦不可使用 `select` 子句中不属于
   `from` 子句对象的新列名，例如计算结果。
7. `select` 子句

   若 `select` 子句指定了计算，此时才执行。
8. `distinct` 子句

   去除 `select` 子句中重复的记录。
9. `limit` / `top` 子句
   （若使用了`context by` 子句）

   若使用了`context by` 子句，`limit` /
   `top` 子句应用于每组。若有 n 组且 `limit` m 或
   `top` m，则最多返回 n\*m 行。 此情况下 `limit` /
   `top` 子句的执行顺序是在 `order by` 子句之前；其它情况下的
   `limit` / `top` 子句的执行顺序是在 `order
   by` 子句之后。
10. `order by` 子句

    由于 `order by` 子句的执行顺序在 `select`
    子句之后，`order by` 子句可使用 `select` 子句中不属于
    `from` 子句对象的新列名，例如计算结果。
11. `limit` / `top` 子句 （若未使用
    `context by` 子句）

    若未使用 `context by` 子句，则 `limit` /
    `top` 子句应用于前一步的全体结果，其指定范围之外的行被丢弃。

    *特殊情况*：`cgroup by` 子句

    若 SQL 语句使用 `cgroup by`
    子句，其执行顺序如下：首先使用过滤条件（若有），然后根据 `cgroup by` 的列与 `group
    by` 的列（若有），对 `select` 子句中的项目进行分组计算，然后根据 `order
    by` 的列（必须使用，且必须属于 `group by` 列或 `cgroup
    by` 列）对分组计算结果进行排序，最后计算累计值。若使用 `group by`，则在每个
    `group by` 组内计算累计值。

## 例子

```
t = table(1 1 1 1 1 2 2 2 2 2 as id, 09:30:00+1 3 2 5 4 5 2 4 3 1 as time, 1 2 3 4 5 6 5 4 3 2 as x);
t;
```

| id | time | x |
| --- | --- | --- |
| 1 | 09:30:01 | 1 |
| 1 | 09:30:03 | 2 |
| 1 | 09:30:02 | 3 |
| 1 | 09:30:05 | 4 |
| 1 | 09:30:04 | 5 |
| 2 | 09:30:05 | 6 |
| 2 | 09:30:02 | 5 |
| 2 | 09:30:04 | 4 |
| 2 | 09:30:03 | 3 |
| 2 | 09:30:01 | 2 |

```
select *, deltas(x) from t context by id;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:01 | 1 |  |
| 1 | 09:30:03 | 2 | 1 |
| 1 | 09:30:02 | 3 | 1 |
| 1 | 09:30:05 | 4 | 1 |
| 1 | 09:30:04 | 5 | 1 |
| 2 | 09:30:05 | 6 |  |
| 2 | 09:30:02 | 5 | -1 |
| 2 | 09:30:04 | 4 | -1 |
| 2 | 09:30:03 | 3 | -1 |
| 2 | 09:30:01 | 2 | -1 |

```
select *, deltas(x) from t context by id csort time;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:01 | 1 |  |
| 1 | 09:30:02 | 3 | 2 |
| 1 | 09:30:03 | 2 | -1 |
| 1 | 09:30:04 | 5 | 3 |
| 1 | 09:30:05 | 4 | -1 |
| 2 | 09:30:01 | 2 |  |
| 2 | 09:30:02 | 5 | 3 |
| 2 | 09:30:03 | 3 | -2 |
| 2 | 09:30:04 | 4 | 1 |
| 2 | 09:30:05 | 6 | 2 |

以上结果说明，使用 csort time 后，首先在每组中按照 time 排序，然后计算
`deltas(x)`。

```
select *, deltas(x) from t context by id csort time limit 3;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:01 | 1 |  |
| 1 | 09:30:02 | 3 | 2 |
| 1 | 09:30:03 | 2 | -1 |
| 2 | 09:30:01 | 2 |  |
| 2 | 09:30:02 | 5 | 3 |
| 2 | 09:30:03 | 3 | -2 |

以上结果说明，若使用了`context by` 与 `limit`
子句，`limit` 子句应用于每组，而非全体结果。

```
select *, deltas(x) from t context by id csort time order by id, deltas_x desc;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:04 | 5 | 3 |
| 1 | 09:30:02 | 3 | 2 |
| 1 | 09:30:03 | 2 | -1 |
| 1 | 09:30:05 | 4 | -1 |
| 1 | 09:30:01 | 1 |  |
| 2 | 09:30:02 | 5 | 3 |
| 2 | 09:30:05 | 6 | 2 |
| 2 | 09:30:04 | 4 | 1 |
| 2 | 09:30:03 | 3 | -2 |
| 2 | 09:30:01 | 2 |  |

以上结果说明，因为 `order by` 子句的执行顺序在
`select` 子句之后，所以 `order by` 子句中可以使用
`select` 子句中的计算结果 deltas\_x。

```
select *, deltas(x) from t context by id csort time order by id, deltas_x desc limit 3;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:02 | 3 | 2 |
| 1 | 09:30:03 | 2 | -1 |
| 1 | 09:30:01 | 1 |  |
| 2 | 09:30:02 | 5 | 3 |
| 2 | 09:30:03 | 3 | -2 |
| 2 | 09:30:01 | 2 |  |

以上结果说明，若使用了`context by` 子句，`limit`
子句限制每组内的行数，且在 `order by` 子句之前执行。

```
select * from t order by id, x desc limit 3;
```

| id | time | x |
| --- | --- | --- |
| 1 | 09:30:04 | 5 |
| 1 | 09:30:05 | 4 |
| 1 | 09:30:02 | 3 |

以上结果说明，若未使用 `context by` 子句，`limit`
子句限制全体结果的行数，且在 `order by` 子句之后执行。

```
select *, deltas(x) from t where x>=3 context by id;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:02 | 3 |  |
| 1 | 09:30:05 | 4 | 1 |
| 1 | 09:30:04 | 5 | 1 |
| 2 | 09:30:05 | 6 |  |
| 2 | 09:30:02 | 5 | -1 |
| 2 | 09:30:04 | 4 | -1 |
| 2 | 09:30:03 | 3 | -1 |

以上结果说明，`where` 条件的执行顺序在 `select`
子句之前。以上语句中，先执行 `where x>=3`，再计算
`deltas(x)`，所以每只股票结果中的第一行 deltas\_x 的结果为空。

```
select *, deltas(x) from t where x>=3 context by id having sum(x)<=12;
```

| id | time | x | deltas\_x |
| --- | --- | --- | --- |
| 1 | 09:30:02 | 3 |  |
| 1 | 09:30:05 | 4 | 1 |
| 1 | 09:30:04 | 5 | 1 |

以上结果说明，`having` 条件的执行顺序在 `where`
条件之后。
