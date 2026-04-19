# runExternalQuery

首发版本：3.00.5

## 语法

`runExternalQuery(config, query, [preExecuteQueries])`

## 详情

将指定的 SQL 语句发送到远程数据库，在远程数据库执行该语句并返回执行结果。

注：

* 调用函数前必须安装和加载 ODBC 插件。
* 支持的远程数据库包括 MySQL、PostgreSQL、SQLServer、ClickHouse、SQLite、Oracle、Hive 和
  GaussDB。此外，建议将数据库安装于 CentOS 7。

## 参数

**config** 字典，设置连接远程数据库的参数。字典键为 "connectionString"，字典值为 ODBC 连接字符串。示例：`config =
dict(["connectionString"], ["Dsn=MyOracleDB"])`。

**query** 字符串标量，指定需要执行的 SQL 语句。该语句需要符合远程数据库的 SQL 语法规则。

**preExecuteQueries** 可选参数，字符串向量。如果在执行 *query* 参数指定的 SQL 语句前，需要预执行某些 SQL
语句，可以设置该参数。系统会按照向量中的顺序依次执行 SQL 语句，但预执行的 SQL 语句不会返回执行结果。

## 返回值

一个内存表。

## 例子

```
oracle_cfg = dict(["connectionString"], ["Dsn=MyOracleDB"])

t1 = createExternalTable("t1", "oracle", oracle_cfg)

t2 = runExternalQuery(oracle_cfg, "select * from t1 inner join t2 on t1.id = t2.id;")

t3 = select * from t1, t2, runExternalQuery(oracle_cfg, "select * from t3;") as t3;
```

**相关函数**：createExternalTable
