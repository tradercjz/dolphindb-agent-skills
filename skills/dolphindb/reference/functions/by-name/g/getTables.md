# getTables

## 语法

`getTables(dbHandle)`

## 详情

查询指定数据库中的表：

* 管理员可以返回所有分布式表；
* 其他用户执行时仅返回：

  （1）拥有 DB\_OWNER, DB\_MANAGE, DB\_READ, DB\_WRITE, DB\_INSERT, DB\_UPDATE,
  DB\_DELETE 权限的数据库所对应的分布式表；

  （2）拥有 TABLE\_READ, TABLE\_WRITE, TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE
  权限的分布式表。

## 参数

**dbHandle** 是数据库句柄。

## 返回值

字符串向量。

## 例子

```
n=1000000
ID=rand(10, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
y=rand(10, n)
t1=table(ID, date, x)
t2=table(ID, date, y)
db = database("dfs://valueDB", VALUE, 2017.08.07..2017.08.11)
pt1 = db.createPartitionedTable(t1, `pt1, `date)
pt1.append!(t1)
pt2 = db.createPartitionedTable(t2, `pt2, `date)
pt2.append!(t2);
getTables(db);
```

输出返回：["pt1","pt2"]
