# loadTextEx

## 语法

`loadTextEx(dbHandle, tableName, partitionColumns,
filename, [delimiter], [schema], [skipRows=0], [transform], [sortColumns], [atomic=false], [arrayDelimiter],
[containHeader], [arrayMarker])`

## 详请

将数据文件加载到数据库中。

* 如果要将数据文件加载到分布式数据库中，必须指定 *tableName*，并且不能为空字符串。
* 如果要将数据文件加载到内存数据库中，那么 *tableName* 为空字符串或者不指定
  *tableName*。

如果指定了 *transform* 参数，需要先创建分区表，再加载数据。系统会对数据文件中的数据执行
*transform* 参数指定的函数，再将得到的结果保存到数据库中。

`loadTextEx` 函数与 loadText 函数有很多共同之处，例如第一行数据是否判断为列名，如何确定各列的数据类型，列名的要求及自动调整等。细节请参见 loadText 函数文档。

## 参数

**dbHandle** 是数据库的句柄，可以是内存数据库或分布式数据库。

**tableName** 是一个字符串，表示表的名称。

**partitionColumns**
是字符串标量或向量，表示分区列。对于顺序分区类型的数据库，*partitionColumns*
为空字符串""。对于组合分区类型的数据库，*partitionColumns* 是字符串向量。

**filename** 是字符串，表示数据文件的路径。仅支持 CSV
格式的文件。若传入其他格式文件，则无法保证数据准确性。

**delimiter** 字符串标量，表示数据文件中各列的分隔符。分隔符可以是一个或多个字符，默认是逗号（","）。

**schema** 是一个表，用于指定各列的数据类型。具体请参考 loadText 的 *schema* 参数。

**skipRows** 是0到1024之间的整数，表示从文件头开始忽略的行数。它是一个可选参数。默认值为0。

**transform** 是一元函数，并且该函数接受的参数必须是一个表。

**sortColumns** 字符串标量或向量，用于指定每一分区内的排序列，每次写入磁盘的数据在每一分区内将按 *sortColumns*
进行排序。系统默认 *sortColumns* （指定多列时） 除最后一列外的列字段作为排序的索引列，称作 sort key。每一分区内，同一个 sort
key 组合值对应的数据将按最后一列的值顺序连续存放在一起。查询时，若查询条件包含索引列，可以快速定位数据所在的数据块位置，提高查询性能。

* 仅当 dbHandle 指示的数据库采用 "TSDB" 引擎（engine="TSDB"）时，本参数才生效。
* *sortColumns* 只能是 INTEGER, TEMPORAL, LITERAL 类别（除 BLOB） 或 DECIMAL 类型。
  + 若 *sortColumns* 指定为多列，则 *sortColumns*
    的最后一列必须为时间类型或整型，其余列为索引列，且索引列不能为为 TIME, TIMESTAMP, NANOTIME,
    NANOTIMESTAMP 类型。
  + 若 *sortColumns* 仅指定一列，则该列作为 sort key，其类型可以是除 TIME, TIMESTAMP,
    NANOTIME, NANOTIMESTAMP 之外的任意类型。若 *sortColumns* 为时间类型 （非分区列），且同时指定了
    *sortKeyMappingFunction*，则查询的过滤条件中 *sortColumns*
    只能与相同时间类型的值进行比较。
* 频繁查询的字段适合设置为 *sortColumns*（建议不超过 4 列），且建议优先把查询频率高的字段作为 *sortColumns*
  中位置靠前的列。
* 为保证性能最优，建议每个分区内索引列的组合数（sort key）不超过 2000 个。
* *sortColumns* 是每个分区内部 level file 内数据的排序依据，与其是否为分区字段无关。

**atomic** 是一个布尔值，表示开启 Cache Engine
的情况下，是否保证文件加载的原子性。设置为 true，一个文件的加载过程视为一个完整的事务；设置为 false，加载一个文件的过程分为多个事务进行。

注：

如果要加载的文件超过 Cache Engine 大小，必须设置
*atomic* = false。否则，一个事务可能卡住（既不能提交，也不能回滚）。

**arrayDelimiter**
是数据文件中数组向量列的分隔符。默认是逗号。由于不支持自动识别数组向量，必须同步修改 *schema* 的 type 列为数组向量类型。

**containHeader**
布尔值，表示数据文件是否包含标题行，默认为空。具体请参考 loadText 的
*containHeader* 参数。

**arrayMarker**  包含两个字符的字符串或或 CHAR
类型数据对，两个字符分别表示数组向量左右边界的标识符。默认标识符为双引号（"）。

* 不能包含空格、Tab(`\t`)
  和换行符(`\t`和`\n`)。
* 不能包含数字或字母。
* 如果其中一个为双引号(")，另一个也必须为双引号。
* 如果标识符为 `'`，`"` 或`\`
  ，需视情况添加转义符。例如 `arrayMarker="\"\""`。
* 如果 *delimiter* 是单个字符，则 *arrayMarker* 不能包含与其相同的字符。
* 如果 *delimiter* 是多个字符，则 *arrayMarker* 左边界不能与 *delimiter*的首个字符相同。

## 返回值

一个表对象。

## 例子

例1. 使用以下脚本生成模拟的数据文件：

```
n=10000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
vol=rand(1..10 join int(), n)
t=table(ID, date, vol)
saveText(t, "/home/DolphinDB/Data/t.txt");
```

例 2. 把 t.txt 文件加载到范围分区类型的分布式数据库中，分区列为 ID。

```
db = database(directory="dfs://rangedb", partitionType=RANGE, partitionScheme=0 51 101)
pt=loadTextEx(dbHandle=db,tableName=`pt, partitionColumns=`ID, filename="/home/DolphinDB/Data/t.txt");
```

例 3. 将文本文件加载到使用 TSDB 存储引擎创建的分布式数据库中。

```
db = database(directory="dfs://rangedb", partitionType=RANGE, partitionScheme=0 51 101, engine='TSDB')
pt=loadTextEx(dbHandle=db, tableName=`pt, partitionColumns=`ID, filename="/home/DolphinDB/Data/t.txt", sortColumns=`ID`date);
```

例 4. 把 t.txt 文件加载到组合分区类型的分布式数据库中，分区列为 date 和 ID。

```
dbDate = database(directory="", partitionType=VALUE, partitionScheme=2017.08.07..2017.08.11)
dbID=database(directory="", partitionType=RANGE, partitionScheme=0 51 101)
db = database(directory="dfs://compoDB", partitionType=COMPO, partitionScheme=[dbDate, dbID])
pt = loadTextEx(dbHandle=db,tableName=`pt, partitionColumns=`date`ID, filename="/home/DolphinDB/Data/t.txt");
```

例 5. 把 t.txt 加载到值分区类型分内存数据库中，分区列为 date。

```
db = database(directory="", partitionType=VALUE, partitionScheme=2017.08.07..2017.08.11)
pt = db.loadTextEx(tableName="", partitionColumns=`date, filename="/home/DolphinDB/Data/t.txt");

pt.sortBy!(`ID`x);
```

例 6. 加载包含数组向量列的数据

导入包含数组向量的数据文件时，由于系统无法自动识别数组向量，因此需要通过 *schema*
参数修改数组向量列的类型，并使用 *arrayDelimiter* 参数指定数据文件中数组向量列的分隔符。

首先，使用以下脚本模拟生成一个 csv 文本文件：

```
bid = array(DOUBLE[], 0, 20).append!([1.4799 1.479 1.4787, 1.4796 1.479 1.4784, 1.4791 1.479 1.4784])
ask = array(DOUBLE[], 0, 20).append!([1.4821 1.4825 1.4828, 1.4818 1.482 1.4821, 1.4814 1.4818 1.482])
TradeDate = 2022.01.01 + 1..3
SecurityID = rand(`APPL`AMZN`IBM, 3)
t = table(SecurityID as `sid, TradeDate as `date, bid as `bid, ask as `ask)
t;
saveText(t,filename="/home/DolphinDB/Data/t.csv",delimiter=',',append=true)
```

然后，调用 loadTextEx 导出该文件，本例通过 *schema*
参数指定数组向量列 bid 和 ask 的数据类型为 DOUBLE[]。

```
db = database(directory="dfs://testDB", partitionType=VALUE, partitionScheme=`APPL`AMZN`IBM)
path = "/home/DolphinDB/Data/t.csv"
schema = extractTextSchema(path);
update schema set type = "DOUBLE[]" where name="bid" or name ="ask"
t = loadTextEx(dbHandle=db, tableName=`t, partitionColumns=`sid, filename=path, schema=schema, arrayDelimiter=",");
select * from t;
```

| sid | date | bid | ask |
| --- | --- | --- | --- |
| APPL | 2022.01.02 | [1.4799,1.479,1.4787] | [1.4821,1.4825,1.4828] |
| IBM | 2022.01.03 | [1.4796,1.479,1.4784] | [1.4818,1.482,1.4821] |
| IBM | 2022.01.04 | [1.4791,1.479,1.4784] | [1.4814,1.4818,1.482] |

例 7. 使用 *transform* 参数处理导入的数据，再将其写入数据库。

示例文件（由例 1 生成）的 vol 列包含空值。通过*transform* 将空值填充为0后再加载到组合分区类型的分布式数据库中。

```
dbDate = database(directory="", partitionType=VALUE, partitionScheme=2017.08.07..2017.08.11)
dbID=database(directory="", partitionType=RANGE, partitionScheme=0 51 101)
db = database(directory="dfs://compoDB", partitionType=COMPO, partitionScheme=[dbDate, dbID]);

pt=db.createPartitionedTable(table=t, tableName=`pt, partitionColumns=`date`ID)
pt=loadTextEx(dbHandle=db, tableName=`pt, partitionColumns=`date`ID, filename="/home/DolphinDB/Data/t.txt", transform=nullFill!{,0});
```

例 8. 通过 *schema* 修改待导入字段的数据类型，同时通过 *transform* 参数，添加新的字段且调整列的顺序。

在实际场景中，通常是一个股票的数据保存到一个文件，该文件以标的名称命名，且不包含标的名称列。导入需求如下：

* 在导入数据时，需要将在数据表中添加一列以存储标的名称。
* 调整数据文件中的字段顺序和待导入表中字段顺序一致。

本例以导入一个标的的文件为例进行说明。

* [sz000001.csv](https://cdn.dolphindb.cn/zh/tutorials/data/import_data_06/sz000001.csv)
  文件中字段顺序是 tradetime，open，close，high，low，vol。
* 待导入表的字段顺序是 symbol（需要添加的列），datetime，vol，open，close，high，low。

```
dir = "/home/data/sz000001.csv"
sym = dir.split('/').tail(1).split('.')[0]

// 调整 tradetime 列的类型为 DATETIME
schema = extractTextSchema(dir)
update schema set type="DATETIME" where name="tradetime"

if(existsDatabase("dfs://stock_data")) {
	dropDatabase("dfs://stock_data")
}

db=database(directory="dfs://stock_data", partitionType=VALUE, partitionScheme=2000.01M..2019.12M)

colNames=`sym`tradetime`vol`open`close`high`low
colTypes=[SYMBOL, DATETIME, INT, DOUBLE, DOUBLE, DOUBLE, DOUBLE]
t = table(1:0, colNames, colTypes)
pt = db.createPartitionedTable(t, `pt, `tradetime);
def mytrans(mutable t, sym, colNames){
        t.replaceColumn!(`tradetime, datetime(t.tradetime))
        //在中添加第一列 sym
        t1 = select sym, * from t
        //通过 reorderColumns! 调整表中各列的顺序
        t1.reorderColumns!(colNames)
        return t1
}

// 指定 schema 和 transform 参数，对数据进行处理
loadTextEx(db, `pt, `tradetime, dir, schema=schema, transform=mytrans{,sym, colNames})

select top 10 * from loadTable("dfs://stock_data", `pt)
```

| sym | tradetime | vol | open | close | high | low |
| --- | --- | --- | --- | --- | --- | --- |
| sz000001 | 2010.01.01T00:00:00 | 10,732 | 35.9484 | 35.4385 | 36.3261 | 35.9569 |
| sz000001 | 2010.01.04T00:00:00 | 97,555 | 16.4653 | 13.6348 | 16.7255 | 14.9401 |
| sz000001 | 2010.01.05T00:00:00 | 43,992 | 51.3616 | 53.1199 | 52.2155 | 50.4782 |
| sz000001 | 2010.01.06T00:00:00 | 85,283 | 76.3469 | 80.0076 | 76.7017 | 74.9479 |
| sz000001 | 2010.01.07T00:00:00 | 78,837 | 38.9411 | 35.8283 | 39.5269 | 38.2178 |
| sz000001 | 2010.01.08T00:00:00 | 13,317 | 70.8803 | 67.9027 | 71.8693 | 70.8072 |
| sz000001 | 2010.01.11T00:00:00 | 22,958 | 96.3163 | 97.4031 | 96.5605 | 96.364 |
| sz000001 | 2010.01.12T00:00:00 | 45,621 | 17.2699 | 18.5016 | 17.7689 | 16.5028 |
| sz000001 | 2010.01.13T00:00:00 | 54,886 | 75.7999 | 77.0245 | 76.4588 | 75.7482 |
| sz000001 | 2010.01.14T00:00:00 | 3,132 | 49.8656 | 49.3416 | 50.7761 | 49.7972 |
