# saveText

## 语法

`saveText(obj, filename, [delimiter=','], [append=false],
[header=true], [bom=''])`

## 详情

将 DolphinDB 变量或 SQL 读取的数据存为磁盘上的文本文件。与 saveTable 命令相比，`saveText` 需要更多的磁盘空间且耗时更久。

## 参数

**obj** 可以是表、矩阵、向量或 SQL 元代码。*obj* 取 SQL
元代码时，系统将分配多个线程并发读取数据，并通过独立的写线程将数据写入文件。否则，数据查询和写入将由当前 worker 处理。

**filename** 是在服务器端输出文件的绝对路径或相对路径。不支持指定保存文件的格式，目前仅支持保存为 CSV
格式的文本。

**delimiter** 是表中的列分隔符。系统的默认分隔符是逗号(,)。

**append** 是一个布尔值，表示输出文件能够被追加。默认值为 false。

**header** 是一个布尔值，表示 *obj* 为数据表时，是否在文件中保留列名。默认值为
true。

注：

向已存在的非空文件中追加数据（即 *append* = true
时），该参数将失效。

**bom** 字符串标量（大小写不敏感），表示是否输出 BOM 头格式。目前仅支持”UTF-8“。默认为空，表示不输出 BOM 头。若用户需要用 Excel
打开导出的 CSV 文件（且数据包含中文），建议传入”UTF-8“，否则可能出现乱码。

## 例子

例1.

```
n=20000000
syms=`IBM`C`MS`MSFT`JPM`ORCL`GE`EBAY`GOOG`FORD`GS
timestamp=09:30:00+rand(18000,n)
sym=rand(syms,n)
qty=100*(1+rand(100,n))
price=5.0+rand(100.0,n)
t1=table(timestamp,sym,qty,price);

timer saveText(t1, "/home/DolphinDB/trades.txt");
// output
Time elapsed: 191488 ms
```

例2.

```
n=100
t1=table(1..n as id, rand(1000, n) as x)
saveText(t1, "/home/DolphinDB/t.csv",,1)
t2=table((n+1)..(2*n) as id, rand(1000, n) as x)
saveText(t2, "/home/DolphinDB/t.csv",,1)
t = loadText("/home/DolphinDB/t.csv")
select count(*) from t;
// output
200
```

例3. 将分布式表的数据存储为文本文件。

```
if(existsDatabase("dfs://testdb")){
  dropDatabase("dfs://testdb")
}
n=3000
ticker = rand(`MSFT`GOOG`FB`ORCL`IBM`PPT`AZH`ILM`ANZ,n);
id = rand(`A`B`C, n)
x=rand(1.0, n)
t=table(ticker, id, x)
db=database(directory="dfs://testdb", partitionType=HASH, partitionScheme=[STRING, 5])
pt = db.createPartitionedTable(t, `pt, `ticker)
pt.append!(t)

saveText(<select * from pt>, "/home/DolphinDB/pt.txt")
```
