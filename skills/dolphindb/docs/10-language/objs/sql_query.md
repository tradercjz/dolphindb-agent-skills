<!-- Auto-mirrored from upstream `documentation-main/progr/objs/sql_query.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SQL 查询

本章中提到的所有类型的对象都可以作为SQL语句中的一部分。

```
// 创建一个表，其中的列x包含0-10000.0之间的2000万个随机单精度浮点数。
t1 = table(rand(10000.0, 20000000) as x);

// 计算列x的平均值
select avg(x) as avgx from t1;
```

| avgx |
| --- |
| 4999.549816 |

```
t = table(1..6 as x, 11..16 as y, 101..106 as z);
t;
```

| x | y | z |
| --- | --- | --- |
| 1 | 11 | 101 |
| 2 | 12 | 102 |
| 3 | 13 | 103 |
| 4 | 14 | 104 |
| 5 | 15 | 105 |
| 6 | 16 | 106 |

```
shape(select x, y from t where x>2);
// output
4 : 2
```

关于SQL语句，详情参见 [SQL语句](../sql/sql_intro.html "DolphinDB 中 SQL 语句的基本语法和用法")。
