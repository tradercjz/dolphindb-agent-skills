<!-- Auto-mirrored from upstream `documentation-main/progr/file_io/tb_io.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 表输入输出

## 保存数据

* 可以使用 saveTable 函数将一个表对象以二进制形式保存到一个文件中；
* 亦可使用 saveText 函数将其保存到一个文本文件中。

和saveTable函数相比，saveText的速度较慢并且需要更多的磁盘空间。但是如果用户需要快速查看数据的话，saveText函数更加方便，
因此建议保存小数据集的时候使用该函数。

如果要把表保存至分区数据库中，需要先使用`createPartitionedTable`函数创建分区表，再使用`append!`函数或`tableInsert`函数把数据保存至分区表中。

下面的例子展示了saveTable函数，其高效地保存了一个含有2000万记录的表，并跟saveText做了比较。

```
n=20000000
syms=`IBM`C`MS`MSFT`JPM`ORCL`BIDU`SOHU`GE`EBAY`GOOG`FORD
timestamp=09:30:00+rand(18000,n)
sym=rand(syms,n)
qty=100*(1+rand(100,n))
price=5.0+rand(100.0,n)
t1=table(timestamp,sym,qty,price);
```

```
timer saveTable("C:/DolphinDB/Data", t1, `trades);
Time elapsed: 208.963 ms
saveText(t1, "C:/DolphinDB/Data/trades.csv");
Time elapsed: 3231.914 ms
```

## 加载数据

* 可以使用 loadTable 函数来导入之前保存的表
* 或者使用 loadText 函数来导入一个文本文件

loadText要比loadTable更花时间。

下面的例子比较了loadTable函数与loadText函数的效率。

```
n=20000000
syms=`IBM`C`MS`MSFT`JPM`ORCL`BIDU`SOHU`GE`EBAY`GOOG`FORD
timestamp=09:30:00+rand(18000,n)
sym=rand(syms,n)
qty=100*(1+rand(100,n))
price=5.0+rand(100.0,n)
t1=table(timestamp,sym,qty,price)
saveTable("C:/DolphinDB/Data", t1, `trades);
timer tt1 = loadTable("C:/DolphinDB/Data",`trades,,true);

Time elapsed: 179.423 ms

saveText(t1, "C:/DolphinDB/Data/trades.txt");
timer tt2=loadText("C:/DolphinDB/Data/trades.txt");

Time elapsed: 7609.7 ms
```
