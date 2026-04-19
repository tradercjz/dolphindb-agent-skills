# contextby

## 语法

`contextby(func, funcArgs, groupingCol, [sortingCol],
[semanticFilter=1], [containArgsOfHighOrderFunc=false])`

或

`funcArg func:X groupingCol`

或

`func:X(funcArgs, groupingCol, [sortingCol],
[semanticFilter=1])`

## 详情

根据 groupingCol 分组，并在组内进行指定计算。

如果func是聚合函数，每组内的所有结果相同。若指定了sortingCol，在计算前，依此列进行组内排序。

注：

当 func 为聚合函数时，用于定义该聚合函数的关键词为 defg。

## 参数

**func** 是一个函数。**注意**：对于第二种用法，func表示的函数只能有一个参数。

**funcArgs** 是函数func的参数。如果有多个参数，则用元组表示。可以是向量、矩阵或表格，且它们的长度必须相同。

**groupingCol** 是分组变量，可为一组或多组。

**sortingCol** 是可选参数，表示在应用函数func前，依此列进行组内排序。

**semanticFilter** 可选参数，当 *funcArgs* 指定为表时，用于指定表中参与计算的字段。它是一个正整数，可取以下值：

* 0：所有列。
* 1（默认值）：数值列（FLOATING/INTEGRAL/DECIMAL 分类，COMPRESSED 除外）。
* 2：时间列（TEMPORAL 类型）。
* 3：字符串列（LITERAL 类型，BLOB 除外）。
* 4：数值列和时间列。

*funcArgs*, *groupingCol* 和 *sortingCol*
中包含的向量长度相等。

**containArgsOfHighOrderFunc** 可选参数，BOOL 标量。当 *funcArgs*
为元组，且元组中某些元素也为元组时，若设置为 true，则对 *funcArgs* 中元组的每个元素分别进行处理；若设置为 false（默认），则将
*funcArgs* 中的嵌套元组作为一个整体（向量）处理，不展开嵌套结构。

## 返回值

一个与输入参数长度相同的向量。

## 例子

例1：声明 sym、price、qty、trade\_date 四个向量，分别代表股票代码、股价、交易量、交易日期；使用
`contextby` 进行分组计算。

```
sym=`IBM`IBM`IBM`MS`MS`MS
price=172.12 170.32 175.25 26.46 31.45 29.43
qty=5800 700 9000 6300 2100 5300
trade_date=2013.05.08 2013.05.06 2013.05.07 2013.05.08 2013.05.06 2013.05.07;
```

按股票代码分组，计算各组内股价的平均值。

```
contextby(avg, price, sym);
// 等价于 price avg :X sym;
// 输出返回：[172.563,172.563,172.563,29.113,29.113,29.113]
```

选出每只股票中价格高于该股票平均价格的所有股价。

```
price at price>contextby(avg, price,sym);
// 输出返回：[175.25,31.45,29.43]
```

选出每只股票中价格高于该股票平均价格的所有股票代码。

```
sym at price>contextby(avg, price,sym);
// 输出返回：["IBM","MS","MS"]
```

按股票代码分组，计算各组内以交易量为权重的加权平均价格。

```
contextby(wavg, [price, qty], sym);
// 输出返回：[173.856,173.856,173.856,28.374,28.374,28.374]
```

按股票代码分组，在各组的时间序列内计算每日价格相对于前一日价格的变化率。以下示例中设置了
*sortingCol*=trade\_date，确保每只股票组内的数据按 trade\_date 升序排列后再计算价格变化率。

```
contextby(ratios, price, sym, trade_date) - 1;
// 输出返回：[-0.01786,,0.028946,-0.100917,,-0.064229]
```

例2：将 groupingCol 指定为多个向量，按股票代码和交易日期进行双重分组，计算每只股票在每个交易日内的累计成交量。

```
sym=`IBM`IBM`IBM`IBM`IBM`IBM`MS`MS`MS`MS`MS`MS
date=2020.12.01 + 0 0 0 1 1 1 0 0 0 1 1 1
qty=5800 700 9000 1000 3500 3900 6300 2100 5300 7800 1200 4300
contextby(cumsum, qty, [sym,date]);
// 输出返回：[5800,6500,15500,1000,4500,8400,6300,8400,13700,7800,9000,13300]
```

例3：当 *funcArgs* 是表时，*semanticFilter* 用于控制哪些字段参与函数计算。本例分别演示：

* *semanticFilter*=1：仅对数值列计算；
* *semanticFilter*=2：仅对时间列计算。

```
dailyOps = table(
    [2024.06.01, 2024.06.01, 2024.06.02, 2024.06.02] as bizDate,
    [2024.06.01T20:00:00.000, 2024.06.01T20:05:00.000, 2024.06.02T20:00:00.000, 2024.06.02T20:05:00.000] as snapshotTime,
    `East`East`South`South as region,
    ["store_101","store_102","store_201","store_202"] as storeId,
    [23500.5, 19880.0, 30210.3, 28760.4] as salesAmt,
    [128, 103, 156, 149] as orderCount
)
dailyOps;
```

dailyOps 的原始数据如下：

| bizDate | snapshotTime | region | storeId | salesAmt | orderCount |
| --- | --- | --- | --- | --- | --- |
| 2024.06.01 | 2024.06.01 20:00:00.000 | East | store\_101 | 23500.5 | 128 |
| 2024.06.01 | 2024.06.01 20:05:00.000 | East | store\_102 | 19880 | 103 |
| 2024.06.02 | 2024.06.02 20:00:00.000 | South | store\_201 | 30210.3 | 156 |
| 2024.06.02 | 2024.06.02 20:05:00.000 | South | store\_202 | 28760.4 | 149 |

设置 *semanticFilter*=1，为 salesAmt 和 orderCount 这两个数值列增加 100；其他列保持不变。

```
contextby(add{,100}, dailyOps, dailyOps.region,,1)
```

输出返回：

| bizDate | snapshotTime | region | storeId | salesAmt | orderCount |
| --- | --- | --- | --- | --- | --- |
| 2024.06.01 | 2024.06.01 20:00:00.000 | East | store\_101 | 23600.5 | 228 |
| 2024.06.01 | 2024.06.01 20:05:00.000 | East | store\_102 | 19980 | 203 |
| 2024.06.02 | 2024.06.02 20:00:00.000 | South | store\_201 | 30310.3 | 256 |
| 2024.06.02 | 2024.06.02 20:05:00.000 | South | store\_202 | 28860.4 | 249 |

设置 *semanticFilter*=2，为 bizDate 和 snapshotTime 两个时间列增加 1 天；其他列保持不变。

```
contextby(temporalAdd{,1d}, dailyOps, dailyOps.region,,2)
```

输出返回：

| bizDate | snapshotTime | region | storeId | salesAmt | orderCount |
| --- | --- | --- | --- | --- | --- |
| 2024.06.02 | 2024.06.02 20:00:00.000 | East | store\_101 | 23500.5 | 128 |
| 2024.06.02 | 2024.06.02 20:05:00.000 | East | store\_102 | 19880.0 | 103 |
| 2024.06.03 | 2024.06.03 20:00:00.000 | South | store\_201 | 30210.3 | 156 |
| 2024.06.03 | 2024.06.03 20:05:00.000 | South | store\_202 | 28760.4 | 149 |

例4：在 SQL 查询中使用 `contextby`。

```
sym=`IBM`IBM`IBM`MS`MS`MS
price=172.12 170.32 175.25 26.46 31.45 29.43
qty=5800 700 9000 6300 2100 5300
trade_date=2013.05.08 2013.05.06 2013.05.07 2013.05.08 2013.05.06 2013.05.07;
t1=table(trade_date,sym,qty,price);
t1;
```

| trade\_date | sym | qty | price |
| --- | --- | --- | --- |
| 2013.05.08 | IBM | 5800 | 172.12 |
| 2013.05.06 | IBM | 700 | 170.32 |
| 2013.05.07 | IBM | 9000 | 175.25 |
| 2013.05.08 | MS | 6300 | 26.46 |
| 2013.05.06 | MS | 2100 | 31.45 |
| 2013.05.07 | MS | 5300 | 29.43 |

选出股价高于组内平均价的交易记录。

```
select trade_date, sym, qty, price from t1 where price > contextby(avg, price,sym);
```

| trade\_date | sym | qty | price |
| --- | --- | --- | --- |
| 2013.05.07 | IBM | 9000 | 175.25 |
| 2013.05.06 | MS | 2100 | 31.45 |
| 2013.05.07 | MS | 5300 | 29.43 |

将所有交易日期增加一天。

```
contextby(temporalAdd{,1d}, t1, t1.sym,,2)
```

| trade\_date | sym | qty | price |
| --- | --- | --- | --- |
| 2013.05.09 | IBM | 5,800 | 172.12 |
| 2013.05.07 | IBM | 700 | 170.32 |
| 2013.05.08 | IBM | 9,000 | 175.25 |
| 2013.05.09 | MS | 6,300 | 26.46 |
| 2013.05.07 | MS | 2,100 | 31.45 |
| 2013.05.08 | MS | 5,300 | 29.43 |

例5：当 *funcArgs* 为元组时：

```
sym=`IBM`IBM`IBM`MS`MS`MS
price=172.12 170.32 175.25 26.46 31.45 29.43
qty=5800 700 9000 6300 2100 5300
trade_date=2013.05.08 2013.05.06 2013.05.07 2013.05.08 2013.05.06 2013.05.07;
t = table(sym, price, qty, trade_date)
t = select * from t order by trade_date
defg avgUdf(price, qty){
    return avg(price*qty)/sum(qty)
}
defg avgUdf1(price){
    return avg(price)
}
// 正常
select contextby(func=tmoving{avgUdf1,,,3d}, funcArgs=(trade_date, price) , groupingCol=sym) from t;

// 正常
select contextby(func=tmoving{avgUdf,,,3d}, funcArgs=(trade_date,(price, qty) ), groupingCol=sym, containArgsOfHighOrderFunc=true) from t;
```

此时 `(trade_date, (price, qty))` 是一个元组，包含两个元素：

* 第一个元素是 `trade_date`，表示交易日期列，是一个向量；
* 第二个元素是 `(price, qty)`，它也是一个元组，包含两个元素。如果
  containArgsOfHighOrderFunc=false，则将 `(price, qty)`
  当成一个整体（即一个向量）来处理。
