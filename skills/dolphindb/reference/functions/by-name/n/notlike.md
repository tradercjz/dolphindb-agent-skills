# notLike

首发版本：3.00.3

## 语法

`notLike(X, pattern)`

## 详情

确定 *X* 是否与 *pattern* 指定的模式不匹配。比较操作区分大小写。

## 参数

**X** 可以是字符串类型的标量/向量。

**pattern** 是一个字符串，通常包含通配符（例如 "%"）。

## 返回值

布尔类型标量或向量。

## 例子

```
notLike(`DEFG, `DE);
// output: true

notLike(`DEFG, "%DE%");
// output: false

a=`IBM`ibm`MSFT`Goog;
notLike(a, "%OO%");
// output: [true,true,true,true]

print a[notLike(a, "%OO%")];
// output: ["IBM","ibm","MSFT","Goog"]
```

`notLike` 可以搭配 `select` 使用，用于排除符合某些条件的记录：

```
t = table(`abb`aac`aaa as sym, 1.8 2.3 3.7 as price);
select * from t where sym notLike "%aa%";
```

| sym | price |
| --- | --- |
| abb | 1.8 |

`notLike` 亦可应用于对分布式表的查询中：

```
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

select * from trades where sym notLike "%IBM%"
```

相关函数：like
