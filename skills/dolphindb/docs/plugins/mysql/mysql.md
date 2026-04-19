<!-- Auto-mirrored from upstream `documentation-main/plugins/mysql/mysql.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# MySQL

DolphinDB MySQL 插件可将 MySQL 中的数据表或语句查询结果高速导入 DolphinDB，同时支持数据类型转换。本插件的部分设计参考了来自 Yandex.Clickhouse 的 mysqlxx 组件。

## 在插件市场安装插件

### 版本要求

支持 DolphinDB Server 2.00.10 及更高版本；支持 Shark；支持 Linux x86-64，Linux ABI，Windows x64。

### 安装步骤

1. 在DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("mysql")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("mysql")
   ```

## 函数接口

注意：使用插件函数前需使用`loadPlugin` 函数导入插件。

### connect

**语法**

```
mysql::connect(host, port, user, password, db, [config])
```

**详情**

与 MySQL 服务器建立一个连接。返回一个 MySQL 连接的句柄，用于 `load` 与 `loadEx` 等操作。

**参数**

**host** MySQL 服务器的地址，类型为 string。

**port** MySQL 服务器的端口，类型为 int。

**user** MySQL 服务器的用户名，类型为 string。

**password** MySQL 服务器的密码，类型为 string。

**db** 要使用的数据库名称，类型为 string。

**config** 可选参数，指定连接配置项的字典。字典的 key 是 STRING 类型，代表配置名称，value 是配置内容。

* "SSL\_ENFORCE" 表示是否开启 SSL 功能，类型为 bool，默认是 true。
* "SSL\_VERIFY\_SERVER\_CERT" 表示是否验证证书，类型为 bool，默认为 false。

**示例**

```
conn = mysql::connect(`127.0.0.1, 3306, `root, `root, `DolphinDB)
```

### showTables

**语法**

```
mysql::showTables(conn)
```

**详情**

列出建立 MySQL 连接时指定的数据库中包含的所有表。

**参数**

**conn** 通过 `mysql::connect` 获得的 MySQL 连接句柄。

**示例**

```
conn = mysql::connect(`192.168.1.16, 3306, `root, `root, `DolphinDB)
mysql::showTables(conn)

output:
  Tables_in_DolphinDB
  -------------------
  US
```

### extractSchema

**语法**

```
mysql::extractSchema(conn, tableName)
```

**详情**

生成指定数据表的结构。

**参数**

**conn** 通过 `mysql::connect` 获得的 MySQL 连接句柄。

**tableName** MySQL 表名，类型为 string。

**示例**

```
conn = mysql::connect(`192.168.1.16, 3306, `root, `root, `DolphinDB)
mysql::extractSchema(conn, `US)

output:
        name    type   DolphinDBType
        PERMNO  int(11)     INT
        date    date        DATE
        SHRCD   int(11)     INT
        TICKER  varchar(10) STRING
        ...
        PRC     double      DOUBLE
```

### load

**语法**

```
mysql::load(conn, table|query, [schema], [startRow], [rowNum], [allowEmptyTable])
```

**详情**

将 MySQL 表或者 SQL 查询结果导入 DolphinDB 中的内存表。支持的数据类型以及数据转化规则可见用户手册数据类型章节。

**参数**

**conn** 通过 `mysql::connect` 获得的 MySQL 连接句柄。

**table|query** 一张 MySQL 中表的名字，或者类似 `select * from table limit 100` 的合法 MySQL 查询语句，类型为 string。

**schema** 是一个包含列名和列类型信息的表，两列均为 string 类型，第一列是列名，用于创建结果表，第二列是要转换成的列类型。该表可以有更多列，只要前两列满足要求。如果想要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为 `load` 函数的一个参数。除了手动创建，该参数还可以通过 `extractSchema` 接口来获取。

**startRow** 读取 MySQL 表的起始行数，若不指定，默认从数据集起始位置读取。若 'table|query' 是查询语句，则这个参数不起作用。

**rowNum** 读取 MySQL 表的行数，若不指定，默认读到数据集的结尾。若 'table|query' 是查询语句，则这个参数不起作用。

**allowEmptyTable** 一个布尔值，表示是否允许从 MySQL 读取空表（没有数据），默认为不允许。该配置项用于管控对空表的加载限制。

**示例**

通过表名加载数据，并指定起始行和加载的行数。

```
conn = mysql::connect(`192.168.1.18, 3306, `root, `root, `DolphinDB)
tb = mysql::load(conn,`US,,1000,10000)
select count(*) from tb
```

通过 SQL 语句加载数据。

```
conn = mysql::connect(`127.0.0.1, 3306, `root, `root, `DolphinDB)
tb = mysql::load(conn, "SELECT PERMNO FROM US LIMIT 123456")
select count(*) from tb
```

如下是一个通过 `extractSchema` 接口获取 *schema* 参数，修改后调用 `load` 接口加载数据到内存表的示例：

```
// 通过 extractSchema 获取 example 表的结构，并用 update 将其中一列的类型改成 double
schema = mysql::extractSchema(conn, "example")
update schema set type = "double" where name = "column"

// 加载 example 表，此时 column 列的类型已被转换成 double
tb = mysql::load(conn, "example", schema)
```

### loadEx

**语法**

```
mysql::loadEx(conn, dbHandle,tableName,partitionColumns,table|query,[schema],[startRow],[rowNum],[transform],[sortColumns],[keepDuplicates],[sortKeyMappingFunction])
```

**详情**

将 MySQL 中的表或查询结果转换为 DolphinDB 数据库的分布式表，然后将表的元数据加载到内存中。支持的数据类型，以及数据转化规则可见数据类型章节。

**参数**

**conn** 通过 `mysql::connect` 获得的 MySQL 连接句柄。

**dbHandle** 与 **tableName** 若要将输入数据文件保存在分布式数据库中，需要指定数据库句柄和表名。

**partitionColumns** 字符串标量或向量，表示分区列。在组合分区中，partitionColumns是字符串向量。

**table|query** MySQL 中表的名字，或者类似 `select * from table limit 100` 的合法 MySQL 查询语句，类型为 string。需要注意查询的 MySQL 表的列顺序需要与 DolphinDB 分布式表的列顺序保持一致，否则会出现值错误或类型转换失败的问题。

**schema** 是一个包含列名和列类型信息的表，两列均为 string 类型，第一列是列名，用于创建结果表，如果分布式表已存在则无作用，第二列是要转换成的列类型。该表可以有更多列，只要前两列满足要求。若要修改由系统自动检测的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为 `load` 函数的一个参数。除了手动创建，该参数还可以通过 `extractSchema` 接口来获取。

**startRow** 读取 MySQL 表的起始行数，若不指定，默认从数据集起始位置读取。若 'table|query' 是查询语句，则这个参数不起作用。

**rowNum** 读取 MySQL 表的行数，若不指定，默认读到数据集的结尾。若 'table|query' 是查询语句，则这个参数不起作用。

**transform** 导入到 DolphinDB 数据库前对 MySQL 表进行转换，例如替换列。

**sortColumns** 字符串标量或向量，用于指定表的排序列，写入的数据将按 sortColumns 进行排序，只在创建 TSDB 引擎表时需要。

**keepDuplicates** 指定在每个分区内如何处理所有 sortColumns 之值皆相同的数据，ALL 用于保留所有数据，为默认值，LAST 仅保留最新数据，FIRST 仅保留第一条数据，只在创建 TSDB 引擎表时需要。

**sortKeyMappingFunction** 由一元函数对象组成的向量，其长度与索引列一致，即 sortColumns 的长度 - 1。用于指定应用在索引列中各列的映射函数，以减少 sort key 的组合数，该过程称为 sort key 降维，只在创建 TSDB 引擎表时需要。

**示例**

* 将数据导入磁盘上的分区表

  ```
  dbPath = "C:/..."
  db = database(dbPath, RANGE, 0 500 1000)
  mysql::loadEx(conn, db,`tb, `PERMNO, `US)
  tb = loadTable(dbPath, `tb)
  ```
* 将数据导入内存中的分区表

  **直接原表导入**

  ```
  db = database("", RANGE, 0 50000 10000)
  tb = mysql::loadEx(conn, db,`tb, `PERMNO, `US)
  ```

**通过SQL导入**

```
db = database("", RANGE, 0 50000 10000)
tb = mysql::loadEx(conn, db,`tb, `PERMNO, "SELECT * FROM US LIMIT 100");
```

* 将数据导入DFS分布式文件系统中的分区表

**直接原表导入**

```
db = database("dfs://US", RANGE, 0 50000 10000)
mysql::loadEx(conn, db,`tb, `PERMNO, `US)
tb = loadTable("dfs://US", `tb)
```

**通过SQL导入**

```
db = database("dfs://US", RANGE, 0 50000 10000)
mysql::loadEx(conn, db,`tb, `PERMNO, "SELECT * FROM US LIMIT 1000");
tb = loadTable("dfs://US", `tb)
```

**导入前对 MySQL 表进行转换**

```
db = database("dfs://US", RANGE, 0 50000 10000)
def replaceTable(mutable t){
	return t.replaceColumn!(`svalue,t[`savlue]-1)
}
t=mysql::loadEx(conn, db, "",`stockid, 'select  * from US where stockid<=1000000',,,,replaceTable)
```

**获取 schema 参数并加载数据到内存表**

```
// 通过 extractSchema 获取 example 表的结构，并用 update 将其中一列的类型改成 double
schema = mysql::extractSchema(conn, "example")
update schema set type = "double" where name = "column"

// 创建一个数据库，然后 loadEx 加载 example 表并保存到 dfs://example 数据库的 pt 表中
db = database("dfs://example", RANGE, 0 50000 1000000 1500000 2000000 2500000 3000001)
mysql::loadEx(conn, db, `pt, `partitionColumn, "example", schema)
```

### close

**语法**

```
mysql::close(conn)
```

**详情**

断开连接，关闭 MySQL 句柄。

**参数**

**conn** 通过 `mysql::connect` 获得的 MySQL 连接句柄。

**示例**

```
mysql::close(conn)
```

## 支持的数据类型

### 整型

| MySQL 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| bit(1)-bit(8) | CHAR |
| bit(9)-bit(16) | SHORT |
| bit(17)-bit(32) | INT |
| bit(33)-bit(64) | LONG |
| tinyint | CHAR |
| tinyint unsigned | SHORT |
| smallint | SHORT |
| smallint unsigned | INT |
| mediumint | INT |
| mediumint unsigned | INT |
| int | INT |
| int unsigned | LONG |
| bigint | LONG |
| bigint unsigned | (不支持) LONG |

* DolphinDB 中数值类型均为有符号类型。为了防止溢出，所有无符号类型会被转化为高一阶的有符号类型。例如，无符号 CHAR 转化为有符号 SHORT，无符号 SHORT 转化为有符号 INT，等等。64 位无符号类型不予支持。
* DolphinDB 不支持 unsigned long long 类型。若 MySQL 中的类型为 bigint unsigned, 可在 `load` 或者 `loadEx` 的 *schema* 参数中设置为 DOUBLE 或者 FLOAT。
* DolphinDB 中各类整形的最小值为 NULL 值，如 CHAR 的-128，SHORT 的-32,768，INT 的-2,147,483,648以及 LONG 的-9,223,372,036,854,775,808。

### 小数类型

| MySQL 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| double | DOUBLE |
| float | FLOAT |
| newdecimal/decimal(1-9 length) | DECIMAL32 |
| newdecimal/decimal(10-18 length) | DECIMAL64 |
| newdecimal/decimal(19-38 length) | DECIMAL128 |
| newdecimal/decimal(lenght < 1 || length > 38) | 抛出异常 |

注：

* IEEE754 浮点数类型皆为有符号数。
* 浮点类型 float 和 double 可转化为 DolphinDB 中的数值相关类型(BOOL, CHAR, SHORT, INT, LONG, FLOAT, DOUBLE)。
* newdecimal/decimal 类型目前仅可转化为 DOUBLE。

### 时间类型

| MySQL 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| date | DATE |
| time | TIME |
| datetime | DATETIME |
| timestamp | TIMESTAMP |
| year | INT |

以上类型皆可转化为 DolphinDB 中的时间相关类型(DATE, MONTH, TIME, MINUTE, SECOND, DATETIME, TIMESTAMP, NANOTIME, NANOTIMESTAMP)。

### 字符串类型

| MySQL 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| char (len <= 10) | SYMBOL |
| varchar (len <= 10) | SYMBOL |
| char (len > 10) | STRING |
| varchar (len > 10) | STRING |
| other string types | STRING |

长度不超过 10 的 char 和 varchar 将被转化为 SYMBOL 类型，其余转化为 STRING 类型。

string 类型可以转化为转化为 DolphinDB 中的字符串相关类型(STRING, SYMBOL)。

### 枚举类型

| MySQL 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| enum | SYMBOL |

enum 类型可以转化为 DolphinDB 中的字符串相关类型(STRING, SYMBOL)，默认转化为 SYMBOL 类型。

## 导入数据性能

### 硬件环境

* CPU：i7-7700 3.60GHZ
* 硬盘：SSD，读速为每秒 460~500MB。

### 数据集导入性能

美国股票市场从 1990 年至 2016 年的每日数据，共 50,591,907 行，22 列，6.5GB。 导入耗时 160.5秒。
