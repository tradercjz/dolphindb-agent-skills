# addColumn

## 语法

`addColumn(table, colNames, colTypes)`

## 详情

给数据表添加新的列。若对分布式表、维度表或流数据表添加新列，不能使用 SQL update 语句，只能使用
`addColumn` 命令。

注：

* 分布式表或维度表通过 `addColumn` 命令添加新列后，需要使用
  `loadTable` 后，才能更新追加的新列。
* 高可用流表不支持新增列。

## 参数

**table** 内存表、流数据表、分布式表或维度表。

**colNames** 是字符串标量或向量，表示要添加的列的名称。

**colTypes** 是表示数据类型的标量或向量。

## 例子

例1： 给分布式表增加列

```
ID=1..6
x=1..6\5
t1=table(ID, x)
db=database("dfs://rangedb",RANGE,  1 4 7)
pt = db.createPartitionedTable(t1, `pt, `ID)
pt.append!(t1);
addColumn(pt,["price", "qty"],[DOUBLE, INT]);
```

增加列后，在插入新结构数据之前，仍然可以插入原来结构的数据。

```
t2=table(1 as ID, 1.2 as x)
pt.append!(t2)
select * from pt;
```

| ID | x | price | qty |
| --- | --- | --- | --- |
| 1 | 0.2 |  |  |
| 2 | 0.4 |  |  |
| 3 | 0.6 |  |  |
| 1 | 1.2 |  |  |
| 4 | 0.8 |  |  |
| 5 | 1 |  |  |
| 6 | 1.2 |  |  |

一旦插入了新结构的数据，就不能插入原来结构的数据。

```
t3=table(1 as ID, 1.6 as x, 10.0 as price, 6 as qty)
pt.append!(t3)
select * from pt;
```

| ID | x | price | qty |
| --- | --- | --- | --- |
| 1 | 0.2 |  |  |
| 2 | 0.4 |  |  |
| 3 | 0.6 |  |  |
| 1 | 1.2 |  |  |
| 1 | 1.6 | 10 | 6 |
| 4 | 0.8 |  |  |
| 5 | 1 |  |  |
| 6 | 1.2 |  |  |

```
t4=table(2 as ID, 2.2 as x)
pt.append!(t4);
// output
The data to append contains fewer columns than the schema.
```

例2：给流数据表增加列

```
n=10
ticker = rand(`MSFT`GOOG`FB`ORCL`IBM,n)
x=rand(1.0, n)
t=streamTable(ticker, x)
share t as st
addColumn(st,["price", "qty"],[DOUBLE, INT])
insert into st values("MSFT",12.0,25.46,256)
select * from st;
```

| ticker | x | price | qty |
| --- | --- | --- | --- |
| MSFT | 0.743241031421349 |  |  |
| FB | 0.254624255700037 |  |  |
| FB | 0.947473830310628 |  |  |
| FB | 0.904140035156161 |  |  |
| MSFT | 0.193251194199547 |  |  |
| MSFT | 0.416090324753895 |  |  |
| MSFT | 0.479371337918565 |  |  |
| ORCL | 0.69910929678008 |  |  |
| GOOG | 0.131539688445628 |  |  |
| MSFT | 0.472390263108537 |  |  |
| MSFT | 12 | 25.46 | 256 |
