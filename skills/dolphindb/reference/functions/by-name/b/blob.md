# blob

## 语法

`blob(X)`

## 详情

将一个字符串转为 BLOB 类型。

注意：

* BLOB 类型不支持任何计算。

## 参数

**X** 是一个字符串标量或向量。

## 返回值

BLOB 类型标量或向量。

## 例子

```
str="hello"
blob(str)
// output
hello

t=table(1..10 as id, "A"+string(1..10) as sym, 2012.01.01..2012.01.10 as date, rand(100.0, 10) as val, rand(uuid(), 10) as uid)
str=toJson(t)
blob(str)
```

通过 `blob` 将超长字符串转为 BLOB 类型后，可作为内存表的一个字段使用：

```
d = dict(1..10000,  rand(1.0, 10000))
str=toStdJson(d);
t=table(blob(str) as jsonStr)
```

TSDB 引擎的分布式表也支持变长字符 BLOB 类型：

```
dbPath="dfs://testBlobDB"
if(existsDatabase(dbPath)){
dropDatabase(dbPath)
}
n=2000000
t=table(n:0,`date`id`type`num`blob,[DATETIME,INT,SYMBOL,DOUBLE,BLOB])
db1=database("",VALUE,2020.01.01..2020.01.10)
db2=database("",HASH,[INT,10])

db=database(directory=dbPath,partitionType=COMPO,partitionScheme=[db1,db2],engine='TSDB')
pt1=createPartitionedTable(dbHandle=db,table=t,tableName=`pt1,partitionColumns=`date`id,sortColumns=`type)

date=concatDateTime(take(2020.01.01..2020.01.10,n),take(00:00:00..23:23:59,n))
id=rand(1..1000,n)
type=rand(`A`B`C`D`E,n)
num=rand(100.0,n)

blob=take(blob(string(1..10)),n)

t1=table(date,id,type,num,blob)
pt1.append!(t1)
select *  from pt1
```
