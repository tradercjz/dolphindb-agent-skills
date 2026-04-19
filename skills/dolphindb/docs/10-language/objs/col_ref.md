<!-- Auto-mirrored from upstream `documentation-main/progr/objs/col_ref.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 列引用

列对象属于表并保存了数据。当需要引用表中某列时，可以使用<table>.<column>。请注意，<table>.<column>是一个只读的对象，不能被修改。

```
t=table(2 3 4 as x, 5 6 7 as y);
t;
```

| x | y |
| --- | --- |
| 2 | 5 |
| 3 | 6 |
| 4 | 7 |

```
t.x;
// output
[2,3,4]

a=t.x;
a+=1;
a;
// output
[3,4,5]

t.x;
// output
[2,3,4]
// 列t.x的值不变。

t.x+=1;
// output
Syntax Error: [line #1] Can't use assignment in expression.
// 这是因为t.x是只读的。要修改列x的值，我们可以用t[`x]或者update语句
```

在 SQL 语句中，可以忽略在变量名前面的表名。

```
select x from t;
```

| x |
| --- |
| 2 |
| 3 |
| 4 |

系统如何判断变量是列引用、变量名还是函数名？系统在运行时会按照列引用、变量名和函数名的顺序动态地消除歧义的。具体来说，在 SQL
语句中，如果表中的列和定义的变量具有相同的名称，则系统始终将该名称解释为表中的列。如果我们想在 SQL
语句中引用定义的变量，我们必须重命名变量。如果函数与表中的列或变量具有相同的名称，并且希望在 SQL
语句中使用函数名称，那么可以在函数名称之前使用“&”或模块名来限定它。

```
x=1..3
z=7..9
t1=select x, y, z from t;

t1;
// 因为表t里面包含了列x，所以系统在 SQL 语句里将x解释为t.x，尽管另外还有一个单独定义的变量x
// 虽然z不在t1表中，但系统发现z的长度和t.x和t.y一致，所以将z和t.x ，t.y来组成一张新表。
```

| x | y | z |
| --- | --- | --- |
| 2 | 5 | 7 |
| 3 | 6 | 8 |
| 4 | 7 | 9 |

下例中同时存在名为 avg 的列、变量和函数。系统会按以下顺序解析：首先尝试解析为 t.avg，若失败则解析为变量
avg，仍失败则解析为函数。因此，`contextby` 的第一个参数被解析为函数，其余位置解析为 t.avg。用户也可以通过显式写为
`&avg` 或 `::avg` 来指定解析为函数。

```
avg=12.5
t1=table(1 2 2 3 3 as id, 1.5 1.8 3.2 1.7 2.5 as avg)
select * from t1 where avg > contextby(avg,avg,id);
// 或 select * from t1 where avg > contextby(&avg,avg,id);
// 或 select * from t1 where avg > contextby(::avg,avg,id);
```

得到：

| id | value |
| --- | --- |
| 2 | 3.2 |
| 3 | 2.5 |

```
t=table(1 2 3 as ID, 4 5 6 as check)

check=1
check1=10
def check(x):x*10
def check1(x):x*100
def check2(x,y):x+2*y;

t;
```

| ID | check |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

```
select ID+check from t;
//将表t中的列ID和check相加
```

| add\_ID |
| --- |
| 5 |
| 7 |
| 9 |

```
select ID+check1 from t;
//列ID加上变量check1.
```

| add\_ID |
| --- |
| 11 |
| 12 |
| 13 |

```
select accumulate(check2, check) as y from t;
//这里的check2是函数，check是表t中的列，将两者用高阶函数accumulate计算。
```

| y |
| --- |
| 4 |
| 14 |
| 26 |
