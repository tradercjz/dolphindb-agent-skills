<!-- Auto-mirrored from upstream `documentation-main/plugins/odbc/odbc.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 安装 unixODBC 库
apk add unixodbc
apk add unixodbc-dev
```

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本。

支持 Linux x86, Linux ABI, Linux JIT, Windows, Windows JIT、Linux ARM。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("odbc")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("odbc")
   ```

**注意**：若在 Alpine Linux 环境中使用插件，加载时可能会出现无法找到依赖库的报错，需要在 DolphinDB 的 server 目录下添加软链接：`ln -s /usr/lib/libodbc.so.2 libodbc.so.1`

## 接口说明

### connect

**语法**

```
odbc::connect(connectionString, [database])
```

**详情**

创建与数据库服务器的连接，返回数据库连接句柄，该句柄将在以后用于访问数据库服务器。

**参数**

**connectionString** ODBC 连接字符串。有关连接字符串格式的更多信息，请参阅 [连接字符串参考](https://www.connectionstrings.com)。ODBC DSN 必须由系统管理员创建。

有关 DSN 连接字符串的更多信息，请参阅 [DSN连接字符串](https://www.connectionstrings.com/dsn/)。我们还可以创建到数据库的 DSN-Less 连接。

如果不通过 DSN 配置方式，可以在连接字符串中指定驱动程序名称和所有特定于驱动程序的信息，例如：[SQL server 的 DSN-less 连接字符串](https://www.connectionstrings.com/sql-server/)或 [MySQL 的 DSN-less 连接字符串](https://www.connectionstrings.com/mysql/)。

**database** 数据库类型。如 "MySQL", "SQLServer", "PostgreSQL", "ClickHouse", "SQLite", "Oracle" 不区分大小写。建议连接时指定该参数，否则写入数据时可能出现报错。

**注意**：

* 驱动程序名称可能会有所不同，具体取决于安装的 ODBC 版本。
* 若数据库连接的端口指定错误，则会出现 server crash。
* 必须通过 DSN 方式连接 Oracle 数据源，否则连接时用户名和密码可能校验失败；若修改 */etc/odbc.ini* 中 DSN 配置的 database 和 password，则需要在 Oracle 命令行中 commit 后才能通过新配置进行连接（也可通过 isql 命令行工具验证配置是否生效）。
* 通过 freeTDS 访问数据库时，必须保证 *freetds.conf* 中的 DSN 配置信息正确，否则可能出现 freeTDS crash 的情况。

**例子**

```
conn1 = odbc::connect("Dsn=mysqlOdbcDsn")  //mysqlOdbcDsn is the name of data source name
conn2 = odbc::connect("Driver={MySQL ODBC 8.0 UNICODE Driver};Server=127.0.0.1;Database=ecimp_ver3;User=newuser;Password=dolphindb123;Option=3;")
conn3 = odbc::connect("Driver=SQL Server;Server=localhost;Database=zyb_test;User =sa;Password=DolphinDB123;")
```

### close

**语法**

```
odbc::close(conn)
```

**详情**

关闭一个 ODBC 连接。

**参数**

**conn** 由 `odbc::connect` 创建的连接句柄。

**例子**

```
conn1 = odbc::connect("Dsn=mysqlOdbcDsn")
odbc::close(conn1)
```

### query

**语法**

```
odbc::query(conn, sqlQuery, [resultTable], [batchSize], [transform])
```

**详情**

通过 *conn* 查询数据库并返回 DolphinDB 表。

**参数**

**conn** 连接句柄或连接字符串。

**sqlQuery** 表示查询的 SQL 语句。

**resultTable** 表对象。若指定，查询结果将保存到该表中。请注意，resultTable 的各字段类型必须与 ODBC 返回的结果兼容（见“类型支持”一节），否则将引发异常。

**batchSize** 从 ODBC 查询到的数据行数到达 *batchSize* 后，会将当前已经读到的数据追加到表 *t* 中。默认值为 262,144。

**transform** 一元函数，且入参必须是一个表。如果指定了 *transform* 参数，需要先创建分区表，再加载数据。程序会对数据文件中的数据应用 *transform* 参数指定的函数后，将得到的结果保存到数据库中。

**例子**

```
t=odbc::query(conn1,"SELECT max(time),min(time) FROM ecimp_ver3.tbl_monitor;")
```

### execute

**语法**

```
odbc::execute(conn, sqlStatement)
```

**详情**

执行 SQL 语句。

**参数**

**conn** 连接句柄或连接字符串。

**sqlStatement** SQL 语句。

**例子**

```
odbc::execute(conn1,"delete from ecimp_ver3.tbl_monitor where `timestamp` BETWEEN '2013-03-26 00:00:01' AND '2013-03-26 23:59:59'")
```

### append

**语法**

```
odbc::append(conn, ddbTable, tableName, [createTableIfNotExists], [ignoreDuplicates])
```

**详情**

将 DolphinDB 表追加到连接的数据库。

**参数**

**conn** 连接句柄。

**ddbTable** DolphinDB 表。

**tableName** 连接的数据库中表的名称。

**createTableIfNotExists** 布尔值，表示是否创建一个新表，默认值是 true。

**ignoreDuplicates** 布尔值，表示在插入时是否忽略重复数据，默认值是 false。

**例子**

```
t=table(1..10 as id,take(now(),10) as time,rand(1..100,10) as value)
odbc::append(conn1, t,"ddbtale", true)
odbc::query(conn1,"SELECT * FROM ecimp_ver3.ddbtale")
```

### setLogLevel

**语法**

```
odbc::setLogLevel(logLevel)
```

**详情**

设置插件的日志等级，系统将打印当前日志等级及以上级别的插件日志，默认为 INFO。注意，该函数仅设置插件的日志等级，不会改变 DolphinDB server 的日志等级。

**参数**

**logLevel** 日志等级，从低到高可选值为：DEBUG, INFO, WARNING, ERROR。

**例子**

设置 odbc 插件的 log level 为 WARNING，此时只输出 WARNING 和 ERROR 级别的 log。

```
odbc::setLogLevel(WARNING)
```

### getLogLevel

**语法**

```
odbc::getLogLevel()
```

**详情**

获取当前当前的日志等级。返回值为一个字符串。

## 类型支持

### 查询时的数据类型转换

查询外部数据库时，数据的类型会自动转换为 DolphinDB 中支持的类型。如果自动转换的结果不符合预期，可以执行以下操作得到目标数据类型：

**步骤一**：调用 `query` 接口查询少量数据并存储到内存表中，检查内存表中各列的数据类型是否符合预期。

```
conn = odbc::connect("Dsn=PostgreSQL")
tb = odbc::query(conn, "SELECT * FROM stocks WHERE symbol=`IBM")

tb.schema()
```

假设 tb 的表结构如下：

| name | typeString | typeInt |
| --- | --- | --- |
| symbol | STRING | 18 |
| date | DATE | 6 |
| … | … | .. |

**步骤二**：如果 symbol 列需要为 SYMBOL 类型，可以在 `query` 接口中指定 *transform* 参数将 STRING 转换为 SYMBOL。以下示例代码中的 pt 需要为已创建好的 DolphinDB 分区表。有关创建分区表的详细内容请参考建库建表。

```
def typeTransform(mutable t){
    t.replaceColumn!("symbol", t["symbol"].symbol())  // STRING -> SYMBOL
    return t
}

converted_tb = odbc::query(conn=conn, sqlQuery="SELECT * FROM stocks WHERE symbol=`IBM", resultTable=pt, transform=typeTransform)
converted_tb.schema()
```

| name | typeString | typeInt |
| --- | --- | --- |
| symbol | SYMBOL | 17 |
| date | DATE | 6 |
| … | … | .. |

### 写入的数据类型对应表

| DolphinDB | PostgreSQL | ClickHouse | Oracle | SQL Server | SQLite | MySQL |
| --- | --- | --- | --- | --- | --- | --- |
| BOOL | boolean | Bool | char(1) | bit | bit | bit |
| CHAR | char(1) | char(1) | char(1) | char(1) | char(1) | char(1) |
| SHORT | smallint | smallint | smallint | smallint | smallint | smallint |
| INT | int | int | int | int | int | int |
| LONG | bigint | bigint | number | bigint | bigint | bigint |
| DATE | date | date | date | date | date | date |
| MONTH | date | date | date | date | date | date |
| TIME | time | time | time | time | time | time |
| MINUTE | time | time | time | time | time | time |
| SECOND | time | time | time | time | time | time |
| DATETIME | timestamp | datetime64 | date | datetime | datetime | datetime |
| TIMESTAMP | timestamp | datetime64 | timestamp | datetime | datetime | datetime |
| NANOTIME | time | time | time | time | time | time |
| NANOTIMESTAMP | timestamp | datetime64 | timestamp | datetime | datetime | datetime |
| FLOAT | float | float | float | float(24) | float | float |
| DOUBLE | double precision | double | binary\_double | float(53) | double | double |
| SYMBOL | varchar(255) | varchar(255) | varchar(255) | varchar(255) | varchar(255) | varchar(255) |
| STRING | varchar(255) | varchar(255) | varchar(255) | varchar(255) | varchar(255) | varchar(255) |

## 常见问题

1. 连接 Windows 系统的 ClickHouse，查询得到的结果显示中文乱码。

   **解决方法**： 请选择 ANSI 的 ClickHouse ODBC 驱动。
2. 连接 ClickHouse 并读取数据时，datetime 类型数据返回空值或错误值。

   **原因**：低于 1.1.10 版本的 ClickHouse 的 ODBC 驱动将 datetime 返回为字符串类型，且返回的数据长度错误（长度过短），导致 ODBC 插件无法读取正确的字符串。

   **解决方法**： 更新驱动到不小于1.1.10的版本。
3. 使用 `yum install mysql-connector-odbc` 命令下载并安装 MySQL ODBC 驱动后，因驱动与 MySQL 数据源版本不一致而导致连接 MySQL 数据源时发生错误。

   **原因**：Yum 仓库未及时更新，通过 `yum install mysql-connector-odbc` 下载及安装的 MySQL ODBC 驱动与 MySQL 数据源的版本不一致。使用 `yum install mysql-connector-odbc` 会根据 Yum 仓库 （Yum Repository）的配置情况下载对应版本的 MySQL ODBC 驱动。当 MySQL 数据源的版本较新，例如 8.0 版本时，请确保您本地的 Yum 仓库配置亦为最新。因此，为避免连接 MySQL 数据源时出现连接超时或无法找到 *libodbc.so.1* 文件等错误，可以通过以下方法获取最新版本的 MySQL ODBC 驱动。

   **解决方法**：

   **方法1**：在运行 `yum install mysql-connector-odbc` 命令前，运行以下命令以确保 MySQL Yum 仓库为最新：

   ```
   $> su root
   $> yum update mysql-community-release
   ```

   有关更多 MySQL Yum 仓库的使用教程， 参考：Installing Additional MySQL Products and Components with Yum。

   **方法2**：下载指定版本的 MySQL ODBC 驱动，修改 */etc/odbc.ini* 文件后，修改 `conn` 对应语句。例如，当 MySQL 数据源版本为 8.0 时：

   1. 运行以下命令下载对应 MySQL 8.0 版本的 ODBC 驱动：

      ```
      wget https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.32-1.el7.x86_64.rpm
      rpm -ivh mysql-connector-odbc-8.0.32-1.el7.x86_64.rpm
      rpm -ql mysql-connector-odbc-8.0.32-1.el7.x86_64
      ```
   2. 加载插件时，如遇到 `libodbc.so.1: cannot open shared object file: No such file or directory` 错误，说明依赖库无法找到，则在 *libodbc.so.2* 与 *libodbc.so.1* 之间建立软连接，然后重新加载插件。

      ```
      cd /usr/lib64
      ln -s libodbc.so.2 libodbc.so.1
      ```
   3. 复制 */etc/odbcinst.ini* 中 `[MySQL ODBC 8.0 Unicode Driver]` 下 `Driver` 的指定路径，例如：

      ```
      [MySQL ODBC 8.0 Unicode Driver]
      Driver=/usr/lib64/libmyodbc8w.so
      UsageCount=1
      ```
   4. 使用上一步复制的信息以及连接 MySQL 数据源所需的登录信息修改 */etc/odbc.ini*：

      ```
      [root@username/]# cat /etc/odbc.ini
      [mysql8]
      Description=ODBC for MySQL
      Driver=/usr/lib64/libmyodbc8w.so
      Server=172.17.0.10
      Port=3306
      Database=test1db
      User=root
      Password=123456
      ```
   5. 修改 `conn` 连接语句。

      ```
      conn = odbc::connect("Driver=MySQL ODBC 8.0 Unicode Driver;Server=172.17.0.10;Port=3306;Database=testdb;User=root;Password=123456;", "MySQL");
      ```
4. 使用 FreeTDS 驱动库连接 SQL Server 数据库时，读取字符串类型的数据出现乱码。

   **解决方法**：

   低版本的 FreeTDS 驱动库在连接使用非 UTF-8 字符集的数据库时，会出现这个问题。请升级到 1.4.22 及以上的 FreeTDS 驱动库。编译方法如下：

   ```
   wget -c https://www.freetds.org/files/stable/freetds-1.4.23.tar.gz
   tar -zxvf freetds-1.4.23.tar.gz
   cd freetds-1.4.23
   ./configure --prefix=/usr/local/freetds --enable-msdblib
   make -j
   make install
   ```
