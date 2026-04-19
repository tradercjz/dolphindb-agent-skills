# getAuditLog

## 语法

`getAuditLog([userId], [startTime], [endTime], [opType])`

## 详情

查询用户 userId 在 startTime 到 endTime 这段时间内完成的，类型为 opType 的 DDL 操作记录。

opType 的所有取值及其对应的 opDetail 示例如下：

| opType | opDetail | Description |
| --- | --- | --- |
| CREATE\_DB |  | 创建数据库 |
| DROP\_DB |  | 删除数据库 |
| CREATE\_TABLE |  | 创建维度表 |
| CREATE\_PARTITIONED\_TABLE |  | 创建分区表 |
| DROP\_TABLE |  | 删除表 |
| DROP\_PARTITION | deletedPartitions=xxx | 删除分区 |
| RENAME\_TABLE | tableName=[xxx], newTableName=[xxx] | 给表重命名 |
| SQL\_DELETE | script=[xxx], deletedRows=xxx | SQL 语句 delete 数据 |
| SQL\_UPDATE | script=[xxx], updatedRows=xxx | SQL 语句 update 数据 |
| UPSERT | insertedRows=xxx, updatedRows=xxx | 调用函数 upsert! 更新数据 |
| ADD\_COLUMN | colName=[xxx], colType=[xxx] | 增加列 |
| SET\_COLUMN\_COMMENT | colName=[xxx], colComment=[xxx] | 给列添加注释 |
| TRUNCATE\_TABLE |  | 删除表所有数据并保留表结构 |
| RENAME\_COLUMN | colName=[xxx], newColName=[xxx] | 给列重命名 |
| REPLACE\_COLUMN | colName=[xxx], colType=[xxx], newColType=[xxx] | 调用函数 replaceColumn! 替换表中的列 |
| DROP\_COLUMN | columnName=[xxx] | 删除列 |
| ADD\_RANGE\_PARTITION |  | 调用 addRangePartitions 增加 RANGE 类型分区 |
| ADD\_VALUE\_PARTITION |  | 调用 addValuePartitions 增加 VALUE 类型分区 |
| APPEND | appendedRows=xxx | 向 atomic='TRANS’ 的库表或向 atomic='CHUNKS’ 的库里的维度表中写入数据 |
| APPEND\_CHUNK\_GRANULARITY | appendedRows=xxx | 向 atomic='CHUNKS’ 的库里的分区表中写入数据 |

## 参数

**userId** 字符串标量或向量，表示要查询的用户。默认为 NULL，表示查询所有用户的 DDL 操作日志。

**startTime** 整数标量或者时间标量，时间标量支持DATE, MONTH, DATETIME, TIMESTAMP, DATEHOUR,
NANOTIMESTAMP 类型。表示查询的起始时间点。默认值为 1970.01.01 。

**endTime** 整数标量或者时间标量，时间标量支持DATE, MONTH, DATETIME, TIMESTAMP, DATEHOUR,
NANOTIMESTAMP 类型。表示查询的结束时间点。默认值为空，表示结束时间为当前时间。endTime 必须大于 startTime。

**opType** 字符串标量或向量，表示查询的操作类型。默认为 NULL，表示查询所有 DDL 操作类型。

注：

startTime 和 endTime 规定的是 DDL 操作结束的时间范围。

## 返回值

返回一个表，其结构如下：

| 列名 | 类型 | 含义 |
| --- | --- | --- |
| userId | STRING | 执行操作的用户名称 |
| startTime | NANOTIMESTAMP | 事务的开始时间 |
| endTime | NANOTIMESTAMP | 事务的结束时间 |
| dbName | STRING | 数据库名 |
| tbName | STRING | 表名 |
| opType | STRING | 操作类型 |
| opDetail | STRING | 操作细节说明 |
| tid | LONG | 事务ID |
| cid | LONG | commit ID |
| remoteIp | IPADDR | 提交该操作的客户端 IP |
| remotePort | INT | 提交该操作的客户端端口 |
| nodeAlias | STRING | 接收该操作的节点别名 |

## 例子

```
// 用户 admin 进行一系列 DDL 操作
login("admin","123456")
n = 3
id = rand(`st0001`st0002`st0003`st0004`st0005, n)
sym = rand(`A`B, n)
tradeDate = take(2022.01.01..2022.01.10, 3)
val = 1..n
dummyTb = table(id, sym,tradeDate, val)

dbPath = "dfs://auditTest"
if(existsDatabase(dbPath)){dropDatabase(dbPath)}
db = database(directory=dbPath, partitionType=VALUE, partitionScheme=2022.01.01..2022.01.05, engine='TSDB')
pt = createPartitionedTable(dbHandle=db, table=dummyTb, tableName="snap", partitionColumns=`TradeDate, sortColumns=`id`tradeDate, keepDuplicates=ALL)
pt.append!(dummyTb)

renameTable(db, `snap, `snap_2)

// 查询 DDL 操作记录
getAuditLog()
```

返回：

| userId | startTime | endTime | dbName | tbName | opType | opDetail | tid | cid | remoteIp | nodeAlias |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| admin | 2024.03.26 14:40:43.659196080 | 2024.03.26 14:40:43.676082419 | dfs://auditTest |  | CREATE\_DB |  | 1 | 1 | 192.168.0.140 | datanode1 |
| admin | 2024.03.26 14:40:43.676154581 | 2024.03.26 14:40:43.687319577 | dfs://auditTest | snap | CREATE\_PARTITIONED\_TABLE |  | 2 | 2 | 192.168.0.140 | datanode1 |
| admin | 2024.03.26 14:40:45.135000207 | 2024.03.26 14:40:45.160530442 | dfs://auditTest | snap | RENAME\_TABLE | tableName=[snap], newTableName=[snap\_2] | 4 | 4 | 192.168.0.14 | datanode1 |
