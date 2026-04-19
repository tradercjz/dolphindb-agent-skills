# sqlUpdate

## 语法

`sqlUpdate(table, updates, [from], [where], [contextBy], [csort], [ascSort],
[having])`

## 详情

动态生成 SQL update 语句的元代码。若需执行生成的元代码，请配合使用 eval 函数。

## 参数

各参数对应 SQL update
语句中相应部分：

```
update
    table_name
    set col1=X1, [col2=X2,…]
    [from table_joiner(table_names)]
    [where condition(s)]
    [context by col_name(s)]
```

**table** 可以是内存表，亦可为分布式表。

**updates** 是元代码或元代码组成的元组，表示更新的操作。

**from** 是元代码，表示表连接操作。

**where** 是元代码，表示 where 条件。

**contextBy** 是元代码，表示 context by 子句。

**csort** 是 csort 后面的关键字（列名）。仅在使用 context by 子句时，才能指定该参数。如果有多个 csort
关键字，使用元组来表示，每个元素对应一个列名的元代码。

**ascSort** 是 csort 关键字按升序或降序排列的整型标量或向量。仅在使用 context by 子句时，才能指定该参数。1 表示升序，0
表示降序。默认值为 1。

**having** 是 having 条件。仅在使用 context by 子句时，才能指定该参数。如果有多个 having 条件，使用 ANY
向量来表示，每个元素对应一个条件的元代码。

## 返回值

CODE 类型标量。

## 例子

例1：更新内存表记录。

```
t1=table(`A`A`B`B as symbol, 2021.04.15 2021.04.16 2021.04.15 2021.04.16 as date, 12 13 21 22 as price)
t2=table(`A`A`B`B as symbol, 2021.04.15 2021.04.16 2021.04.15 2021.04.16 as date, 10 20 30 40 as volume);

sqlUpdate(t1, <price*2 as updatedPrice>).eval()
t1;
```

| symbol | date | price | updatedPrice |
| --- | --- | --- | --- |
| A | 2021.04.15 | 12 | 24 |
| A | 2021.04.16 | 13 | 26 |
| B | 2021.04.15 | 21 | 42 |
| B | 2021.04.16 | 22 | 44 |

```
sqlUpdate(table=t1, updates=[<price*10 as updatedPrice>,<price*20 as updatedPrice2>]).eval()
t1;
```

| symbol | date | price | updatedPrice | updatedPrice2 |
| --- | --- | --- | --- | --- |
| A | 2021.04.15 | 12 | 120 | 240 |
| A | 2021.04.16 | 13 | 130 | 260 |
| B | 2021.04.15 | 21 | 210 | 420 |
| B | 2021.04.16 | 22 | 220 | 440 |

```
sqlUpdate(table=t2, updates=<cumsum(volume) as cumVolume>, contextby=<symbol>).eval()

t2;
```

| symbol | date | volume | cumVolume |
| --- | --- | --- | --- |
| A | 2021.04.15 | 10 | 10 |
| A | 2021.04.16 | 20 | 30 |
| B | 2021.04.15 | 30 | 30 |
| B | 2021.04.16 | 40 | 70 |

```
sqlUpdate(table=t1, updates=<updatedPrice*volume as dollarVolume>, from=<lj(t1, t2, `symbol`date)>).eval()

t1;
```

| symbol | date | price | updatedPrice | dollarVolume |
| --- | --- | --- | --- | --- |
| A | 2021.04.15 | 12 | 120 | 1200 |
| A | 2021.04.16 | 13 | 130 | 2600 |
| B | 2021.04.15 | 21 | 42 | 1260 |
| B | 2021.04.16 | 22 | 44 | 1760 |

```
sqlUpdate(table=t2,updates=<cumsum(volume) as cumVolume>,contextBy=<symbol>,csort=<volume>,ascSort=0).eval()

t2;
```

| symbol | date | volume | cumVolume |
| --- | --- | --- | --- |
| A | 2021.04.15 | 10 | 30 |
| A | 2021.04.16 | 20 | 20 |
| B | 2021.04.15 | 30 | 70 |
| B | 2021.04.16 | 40 | 40 |

例2：更新分区表记录。

```
if(existsDatabase("dfs://db1")){
    dropDatabase("dfs://db1")
}
n=1000000
t=table(take(`A`B`C`D,n) as symbol, rand(10.0, n) as value)
db = database("dfs://db1", VALUE, `A`B`C`D)
Trades = db.createPartitionedTable(t, "Trades", "symbol")
Trades.append!(t)
x=exec sum(value) from Trades;

Trades=loadTable("dfs://db1", "Trades")
sqlUpdate(table=Trades, updates=<value+1 as value>, where=<symbol=`A>).eval()
y=exec sum(value) from Trades;

y-x;

// output
250000
```

例3：按门店分组、按日期排序，计算门店累计销售额，但只更新月累计销售额达到 50,000 的门店记录。

```
sales = table(
    `store101`store101`store101`store205`store205`store205 as storeId,
    2024.06.01 2024.06.02 2024.06.03 2024.06.01 2024.06.02 2024.06.03 as bizDate,
    18000.0 22000.0 15000.0 16000.0 12000.0 9000.0 as salesAmt,
    take(double(NULL), 6) as cumSalesAmt
)
​
sqlUpdate(
    table=sales,
    updates=<cumsum(salesAmt) as cumSalesAmt>,
    contextBy=<storeId>,
    csort=<bizDate>,
    having=<sum(salesAmt) >= 50000>
).eval()
​
sales
```

输出如下：

| storeId | bizDate | salesAmt | cumSalesAmt |
| --- | --- | --- | --- |
| store101 | 2024.06.01 | 18,000 | 18,000 |
| store101 | 2024.06.02 | 22,000 | 40,000 |
| store101 | 2024.06.03 | 15,000 | 55,000 |
| store205 | 2024.06.01 | 16,000 |  |
| store205 | 2024.06.02 | 12,000 |  |
| store205 | 2024.06.03 | 9,000 |  |

* *having* 只能和 *contextBy* 一起使用。
* store101 的组内销售额合计为 55000，满足 `sum(salesAmt) >= 50000`，所以该组的
  cumSalesAmt 被更新为按 bizDate 排序后的累计值。
* store205 的组内销售额合计为 37000，不满足 `sum(salesAmt) >=
  50000`，因此该组记录不会被本次更新命中，cumSalesAmt 保持空值。
