# getStreamingSQLSubscriptionInfo

首发版本：3.00.5

## 语法

`getStreamingSQLSubscriptionInfo(queryId)`

## 详情

查询指定流式 SQL 的元数据信息。

## 参数

**queryId**
字符串，表示流式 SQL 的 ID。

## 返回值

一个字典，包含以下键值：

* leadingRecordInsertTime：触发最近一次更新的数据中最早插入行的插入时间。
* lastRecordInsertTime：触发最近一次更新的数据中最晚插入行的插入时间。
* lastUpdateTime：当前结果集的更新时间。

## 例子

```
// 声明流式 SQL 输入表
share keyedTable(`id, 1:0, `id`value, [INT, DOUBLE]) as leftTable;
share keyedTable(`id, 1:0, `id`value, [INT, DOUBLE]) as rightTable;
go;
declareStreamingSQLTable(leftTable);
declareStreamingSQLTable(rightTable);
// 注册流式 SQL
queryId = registerStreamingSQL("select id, leftTable.value + rightTable.value from leftTable left join rightTable on leftTable.id=rightTable.id");
// 订阅流式 SQL 查询结果
result = subscribeStreamingSQL(,queryId)
t = table(1 2 3 4 5 as id, 0.1 0.2 0.3 0.4 0.5 as value);
leftTable.append!(t);
t = table(1 2 3 4 5 as id, 0.1 0.2 0.3 0.4 0.5 as value)
rightTable.append!(t)
// 查询该流式 SQL 的元信息
getStreamingSQLSubscriptionInfo(queryId)
/*
output:
leadingRecordInsertTime->2026.01.29T17:42:08.297
lastRecordInsertTime->2026.01.29T17:42:08.297
lastUpdateTime->2026.01.29T17:42:08.297
*/
```
