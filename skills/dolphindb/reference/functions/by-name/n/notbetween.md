# notBetween

首发版本：3.00.3

## 语法

`notBetween(X, Y)`

## 详情

检查 *X* 的每个元素是否在 Y 确定的范围之外。

## 参数

**X** 可以是标量、数据对、向量或矩阵；

**Y** 是一个表示范围的数据对（包含两个边界）。

## 返回值

布尔类型，标量或维度与 *X* 相同的向量/矩阵。

## 例子

```
notBetween([1, 5.5, 6, 8], 1:6);
// output: [false,false,false,true]

notBetween(1 2.4 3.6 2 3.9, 2.4:3.6);
// output: [true,false,false,true,true]
```

`notBetween` 可以搭配 `select` 使用，检查值是否不在指定的范围之内。

```
t = table(`abb`aac`aaa as sym, 1.8 2.3 3.7 as price);
select * from t where price notBetween 1:3;
```

| sym | price |
| --- | --- |
| aaa | 3.7 |

`notBetween` 亦可应用于对分布式表的查询中：

```
login(`admin,`123456)
dbName="dfs://database1"
if(existsDatabase(dbName)){
	dropDatabase(dbName)
}
db=database(dbName,VALUE,2019.01.01..2019.01.03)
n=100
datetime=take(2019.01.01 +0..100,n)
sym = take(`C`MS`MS`MS`IBM`IBM`IBM`C`C$SYMBOL,n)
price= take(49.6 29.46 29.52 30.02 174.97 175.23 50.76 50.32 51.29,n)
qty = take(2200 1900 2100 3200 6800 5400 1300 2500 8800,n)
t=table(datetime, sym, price, qty)
trades=db.createPartitionedTable(t,`trades,`datetime).append!(t)

select * from trades where qty notBetween 1300:6800
```

| datetime | sym | price | qty |
| --- | --- | --- | --- |
| 2019.01.09 | C | 51.29 | 8,800 |
| 2019.01.18 | C | 51.29 | 8,800 |
| 2019.01.27 | C | 51.29 | 8,800 |
| 2019.02.05 | C | 51.29 | 8,800 |
| 2019.02.14 | C | 51.29 | 8,800 |
| 2019.02.23 | C | 51.29 | 8,800 |
| 2019.03.04 | C | 51.29 | 8,800 |
| 2019.03.13 | C | 51.29 | 8,800 |
| 2019.03.22 | C | 51.29 | 8,800 |
| 2019.03.31 | C | 51.29 | 8,800 |
| 2019.04.09 | C | 51.29 | 8,800 |

相关函数：between
