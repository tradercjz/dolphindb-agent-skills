# setStreamTableTimestamp

## 语法

`setStreamTableTimestamp(streamTable, columnName)`

## 详情

为指定的流数据表设置一个时间戳列（支持所有时间类型）。设置后，每次向流表写入数据时，系统会记录写入时的系统时间到该时间戳列。这有助于用户统计实时数据写入流表时的延迟。

**注意**：

* 设置后不可更改和撤销时间戳列。
* 设置后的表不支持作为流引擎的输出表。

## 参数

**streamTable** 流数据表。可以是普通流表、共享流表、持久化流表和高可用流表。

**columnName** 一个字符串，是流数据表最后一列的列名。该列用于记录数据写入流表的系统时间。

## 例子

```
share streamTable(10000:0,`time`symbol`price`timestamp, [TIMESTAMP,SYMBOL,DOUBLE,TIMESTAMP]) as trades
//指定 timestamp 列为时间戳列
setStreamTableTimestamp(trades, `timestamp)

//插入的数据中不能包含 timestamp 列，系统会自动为其添加时间戳。
insert into trades values(2023.03.19T03:17:49, `A, 10.2)

select * from trades
```

| time | symbol | price | timestamp |
| --- | --- | --- | --- |
| 2023.03.19 03:17:49.000 | A | 10.2 | 2024.03.31 08:01:31.324 |

```
//高可用流表
colNames = `timestamp`sym`qty`price
colTypes = [TIMESTAMP,SYMBOL,INT,DOUBLE]
t=table(1:0,colNames,colTypes)
haStreamTable(2,t,`trades,100000);
setStreamTableTimestamp(trades, `timestamp)
```
