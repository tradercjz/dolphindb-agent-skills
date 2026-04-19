# enableActivePartition

## 语法

`enableActivePartition(db, activeDate,
siteAlias)`

## 详情

创建活动数据库和历史数据库之间的连接。

## 参数

**db** 是历史数据库的句柄。

**activeDate** 是活动数据库的日期。

**setAlias** 是活动数据库所在节点的别名。

## 返回值

无。

## 例子

```
histdb = database("C:\DolphinDBDemo\example\data\dbspace\historical-A\Trades2ndDomain")
activeNodeAlias = getNodeAlias()
activeDate = today()
enableActivePartition(histdb, activeDate, activeNodeAlias);
```
