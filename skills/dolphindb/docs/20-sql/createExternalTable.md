<!-- Auto-mirrored from upstream `documentation-main/progr/sql/createExternalTable.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# createExternalTable

随着企业数据源的多样化，用户需要在统一平台中便捷访问和查询多种数据库及文件系统中的数据。为此，我们推出了外部表功能，使外部数据像本地表一样使用，支持常用查询、部分谓词下推，提升易用性和查询效率。

目前已支持 Oracle、MySQL、SQL Server、S3、Parquet 等主流数据源。用户只需安装相应的连接插件（如
ODBC、AWS、Parquet）即可使用。

首发版本：3.00.4

## 外部表创建接口

### 语法

`createExternalTable(tableName, externalType, config, [columnNames],
[columnTypes])`

### 详情

创建一个外部表，并返回对应的表对象。之后，可以像操作本地表一样，直接用 DolphinDB 的脚本查询和处理外部数据源的数据。

通过 *externalType* 来识别是哪种类型的外部表。目前可选 'oracle', ‘s3', ‘parquet', ‘mysql',
‘sqlserver', 'dolphindb', 'hive', 'gauss', 'clickhouse',
'sqlite'。不同外部数据源的参数配置（*config*）不同。

* 如果是 'oracle'、‘mysql', ‘sqlserver', 'hive', 'gauss', 'clickhouse',
  'sqlite'，则需要配置 connectionString：连接字符串，例如 Dsn=MyOracleDB;Uid=user;Pwd=pass，参考
  ODBC。
* 如果是 S3，则需要配置：

| config 字典键 | config 字典值 |
| --- | --- |
| filePath | 字符串，S3 存储桶中的文件路径。目前只支持后缀名为 .csv 或者 .csv.gz 的文件。 |
| region | 字符串，AWS 区域名称（如 "us-east-1"）。 |
| bucket | 字符串，S3 存储桶名称。 |
| accessKeyId | 字符串，AWS 访问密钥 ID。 |
| secretAccessKey | 字符串，AWS 访问密钥。 |

* 如果是 Parquet，则需要配置：

| config 字典键 | config 字典值 |
| --- | --- |
| fileName | 字符串，parquet 的文件路径名，如果是 HDFS 系统，表示其在 HDFS 上的路径名。 |
| nameNode | 可选参数，字符串，表示 HDFS 的 IP 地址。 |
| port | 可选参数，整型，表示 HDFS 的端口号。 |
| username | 可选参数，字符串，表示 HDFS 的用户名。 |
| kerbTicketCachePath | 可选参数，字符串，连接到 HDFS 时要使用的 Kerberos 路径。 |
| keytabPath | 可选参数，字符串，Kerberos 认证过程中用于验证获得票据的 keytab 文件所在路径。 |
| principal | 可选参数，字符串，Kerberos 认证过程中需要验证的 principal。 |
| lifetime | 可选参数，字符串，生成票据的生存期。 |

* 如果是远程的 DolphinDB 节点，则需要配置：

| config 字典键 | config 字典值 |
| --- | --- |
| siteAlias | 是远程节点的别名。它需要在配置文件中定义。配置该参数后，则无需配置 host 与 port。 |
| host | 字符串，是远程节点的主机名（IP 地址或站点）。配置该参数后，无需配置 siteAlias。 |
| port | 整型，是远程节点的端口号。 |
| userId | 可选参数，字符串，远程用户名。 |
| password | 可选参数，字符串，表示用户密码。 |
| enableSSL | 可选参数，布尔值，是否使用 SSL 协议进行加密通信。默认值为 false。 |
| database | 可选参数，字符串，要读取的远程数据库名称。若不指定该参数，则表示 *tableName* 为共享内存表。 |

需要根据外部数据源安装并加载对应插件，例如：

* Oracle / MySQL / SQL Server / Hive / GaussDB / ClickHouse / SQLite：需加载 odbc
  插件。
* S3：需加载 aws 插件。
* 读取 Parquet 文件需加载 parquet 及 hdfs 插件（如果文件存于 HDFS）。

### 参数

**tableName** 字符串标量，表示目标外部表名称。

**externalType** 字符串标量，表示数据源类型。可选值为：'oracle', 's3', 'parquet', 'mysql',
'sqlserver', 'dolphindb', ‘hive', 'gauss', 'clickhouse', 'sqlite'。

**config** 一个字典，用于设置连接参数，不同数据源参数不同，见详情。

**columnNames** 可选参数，字符串向量，用于指定显示的列名。

* 若未指定，则默认使用外部表的原始列名。
* 若指定，则必须为所有列提供名称。

**columnTypes** 可选参数，与 *columnNames*
等长，用于指定列的类型。若不指定该参数，系统会根据外部表的类型自动转换。

### 例子

例1. 创建一个映射到 Oracle 中 aka\_name 表的外部表。之后可以在 DolphinDB 中查询 aka\_name 表数据。

```
loadPlugin("odbc")
oracle_cfg = dict(["connectionString"], ["Dsn=MyOracleDB"])
t = createExternalTable("aka_name", "oracle", oracle_cfg)

select t.name from t where t.id > 200 limit 50
```

例2. 创建一个外部表，该表映射到 S3 上的源数据文件。

```
loadPlugin("aws")
aws_cfg = dict(["filePath", "region", "bucket", "accessId", "secretKey"], ["demo.csv.gz", 'cn-north-1', 'tests3func', 'AKIAXTOOQXTLU44HF75E',
'S0OzvoQnlmFRSn1RzhK5b0yY4IpbrvYTyF5bwtyw'])
t = createExternalTable("test","s3", aws_cfg,`Open`High`OpenInt, [DOUBLE, DOUBLE, INT]);
select count(*) from t where Open > 0.5 and High < 0.6 limit 1;
```

例3. 创建一个外部表，用于映射远程 DolphinDB 节点中的分布式数据表 pt。

```
ddb_cfg = dict(["host", "port", "userId", "password", "database"], ["192.168.0.130", 8848, "admin", "123456", "dfs://textDB"])
t = createExternalTable("pt", "dolphindb", ddb_cfg2)
select min(vol) from t where qty > 1500
```

**相关函数**：runExternalQuery
