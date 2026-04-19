<!-- Auto-mirrored from upstream `documentation-main/tutorials/Debezium_Kafka_PostgreSQL_sync.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# REPLICATION
wal_level = logical             # minimal, archive, hot_standby, or logical (change requires restart)
max_wal_senders = 4             # max number of walsender processes (change requires restart)
#wal_keep_segments = 4          # in logfile segments, 16MB each; 0 disables
#wal_sender_timeout = 60s       # in milliseconds; 0 disables
max_replication_slots = 4       # max number of replication slots (change requires restart)
```

PostgreSQL 中的数据库访问权限需要在 /var/lib/pgsql/12/data/pg\_hba.conf 中进行配置。可以如下配置 IP4
的所有主机的 md5 加密访问权限。

```
host all all 0.0.0.0/0  md5
```

修改配置文件需要重启数据库生效。

**第二步： 创建数据库和用户**

在使用数据库时，通常会为业务数据创建专门的用户和数据库进行数据管理。这里我们创建业务数据的存储数据库和业务用户，再创建一个专门进行逻辑复制的用户。

使用超级用户 postgres，创建业务数据用户和数据库，并授予权限。

```
CREATE USER factoruser WITH PASSWORD '111111';
CREATE DATABASE factordb;
GRANT ALL PRIVILEGES ON DATABASE factordb TO factoruser ;
```

创建逻辑复制用户，并授予该用户逻辑复制权限和连接业务数据库权限。

```
CREATE USER datasyn WITH PASSWORD '111111';
ALTER USER datasyn WITH REPLICATION;
GRANT CONNECT ON DATABASE factordb TO datasyn;
```

接下来我们创建业务数据库的 schema 并授予逻辑复制用户对业务数据库的数据访问权限，这需要登录数据库，并切换到业务数据库（database）后执行。切换
database，使用 psql 连接可以按 图 3-1 操作。

![](images/Debezium_Kafka_PostgreSQL_sync/3-1.png)

图 2. 图 3-1 PostgreSQL 切换 database 操作

创建业务数据 schema，需要当前数据库是 factordb。

```
create schema factorsch authorization factoruser;
```

授予 datasyn 用户对业务数据库 factordb 的 factorsch 的具体使用权限。

```
GRANT USAGE ON SCHEMA factorsch TO datasyn;
GRANT SELECT ON ALL TABLES IN SCHEMA factorsch TO datasyn;
```

配置逻辑复制用户的逻辑复制访问权限，修改文件 /var/lib/pgsql/12/data/pg\_hba.conf。

```
host replication datasyn 0.0.0.0/0 md5
```

重启数据库，并测试逻辑解码插件。

```
--创建复制槽
SELECT * FROM pg_create_logical_replication_slot('pgoutput_demo', 'pgoutput');
--查看相应复制槽是否存在
SELECT * FROM pg_replication_slots;
--删除复制槽
SELECT * FROM pg_drop_replication_slot('pgoutput_demo');
```

### 3.2 安装 Debezium-PostgreSQL 连接器插件

PostgreSQL 的 Debezium 数据同步插件需要安装在 Kafka Connect 程序部署文件路径下。

配置启动 Debezium-PostgreSQL 连接器，需要以下两步：

* 下载 Debezium-PostgreSQL-Connector 插件，将插件解压并放到 Kafka Connect 的插件路径下
* 重新启动 Kafka Connect 程序，以加载插件

**第一步： 下载安装 Debezium-PostgreSQL 插件**

前往官方网站 [Debezium](https://debezium.io/)，选择 2.5.1.Final 版本进行下载，程序名为
debezium-connector-postgres-2.5.1.Final-plugin.tar.gz，本教程测试时采用的此版本，也可以使用 2.5
系列的最新版本。如果想使用 Debezium 的最新稳定版本，需要仔细阅读对应的版本需求，并进行详细测试。

![](images/Debezium_Kafka_PostgreSQL_sync/3-2.png)

图 3. 图 3-2 Debezium 官网下载链接

在 confluent 的安装路径下创建插件路径，在此路径下解压 Debezium 的 PostgreSQL 插件包，请确保 kafka
用户对此路径具有读权限，如果下面代码中的下载链接失效，请按 图 3-2 官网示例位置下载。

```
sudo mkdir -p /opt/confluent/share/java/plugin
cd /opt/confluent/share/java/plugin
sudo wget https://repo1.maven.org/maven2/io/debezium/debezium-connector-postgres/2.5.1.Final/debezium-connector-postgres-2.5.1.Final-plugin.tar.gz
sudo tar -xvf ./debezium-connector-postgres-2.5.1.Final-plugin.tar.gz
sudo rm ./debezium-connector-postgres-2.5.1.Final-plugin.tar.gz
```

**第二步： 配置 Kafka Connect 加载插件**

修改 Kafka Connect 的配置文件，添加插件路径配置。若已配置插件路径，则跳过该步骤。

```
cd /KFDATA/kafka-connect/etc
vim kafka-connect.properties
```

添加或修改参数 *plugin.path* 如下。

```
plugin.path=/opt/confluent/share/java/plugin
```

重新启动 Kafka Connect。

```
sudo systemctl restart kafka-connect
```

查看 kafka connect 的日志输出，能查询到信息则说明插件加载成功。

```
cat /KFDATA/kafka-connect/logs/connect.log | grep PostgresConnector
```

![](images/Debezium_Kafka_PostgreSQL_sync/3-3.png)

图 4. 图 3-3 Debezium-PostgreSQL 插件加载成功信息

### 3.3 配置 PostgreSQL 数据同步连接任务

数据库基础配置和 PostgreSQL 同步插件安装好，我们就可以开始配置 PostgreSQL 的数据同步任务。配置同步任务及检查的很多命令都要带上 url
等参数。为了操作快捷，本教程封装了一些加载配置文件的操作脚本在 kafka-tools.tar 包中，详情参见附录。下载当前包，解压缩到
*/KFDATA* 目录下。后续的很多操作，包括检查 Kafka 的 topic、查看数据和配置同步任务等都会使用
kafka-tools.tar 包中的脚本。包中的脚本在无参数运行时会输出 help 文档。

```
cd /KFDATA
sudo tar -xvf kafka-tools.tar
sudo chown kafka:kafka kafka-tools
rm ./kafka-tools.tar
```

修改 */KFDATA/kafka-tools/config/config.properties* 配置参数。

按照本机的路径、IP 等对应修改 Kafka 和 Kafka Connect 的启动 IP 地址，以及安装目录。

示例如下：

```
#kafka parameters
kafka_home=/opt/kafka
confluent_home=/opt/confluent
bootstrap_server=192.168.189.130:9092

#kafka-connect parameters
connect_rest_url=192.168.1.178:8083
#rest_pd  means restful request  password,This is not necessary
#rest_pd=appsdba:passwd
schema_ip=192.168.189.130
schema_port=8081
```

**第一步：准备 PostgreSQL 数据库表**

本教程的同步方案支持 DolphinDB 的 TSDB 和 OLAP 两种存储引擎的数据同步。其中 TSDB
引擎对于单字段主键和多字段复合主键有不同的处理方式。所以这里我们创建三张表来展示不同的情况的配置操作。

* 单主键同步到 TSDB 引擎 : factorsch.stock\_example。
* 复合主键同步到 TSDB 引擎 : factorsch.index\_example\_tsdb。
* 复合主键同步到 OLAP 引擎 : factorsch.index\_example\_olap。

创建业务数据库表、数据，均使用 factoruser ，登录 factordb。

创建表 factorsch.stock\_example。

```
create table factorsch.stock_example (
    id bigint,
    ts_code varchar(20),
    symbol_id varchar(20),
    name varchar(20),
    area varchar(20),
    industry varchar(20),
    list_date date,
    primary key (id)
);
```

插入数据。

```
insert into factorsch.stock_example(id,ts_code,symbol_id,name,area,industry,list_date)
values (1,'000001.SZ','000001','平安银行','深圳','银行','1991-04-03'),
(2,'000002.SZ','000002','万科A','深圳','地产','1991-01-29'),
(3,'000004.SZ','000004','ST国华','深圳','软件服务','1991-01-14');
```

创建表 factorsch.index\_example\_tsdb。

```
create table factorsch.index_example_tsdb (
    trade_date date,
    stock_code varchar(20),
    effDate timestamp,
    indexShortName varchar(20),
    indexCode varchar(20),
    secShortName varchar(50),
    exchangeCD varchar(10),
    weight decimal(26,6),
    tm_stamp timestamp,
    flag integer,
    primary key (trade_date, stock_code, indexCode, flag)
);
```

插入数据。

```
insert into factorsch.index_example_tsdb
values(to_date('2006-11-30', 'YYYY-MM-DD'), '000759', to_date('2018-06-30 03:48:05', 'YYYY-MM-DD HH24:MI:SS'),
'中证500', '000905', '中百集团', 'XSHE', 0.0044, to_date('2018-06-30 05:43:05', 'YYYY-MM-DD HH24:MI:SS'), 1);

insert into factorsch.index_example_tsdb
values(to_date('2006-11-30', 'YYYY-MM-DD'), '000759', to_date('2018-06-30 04:47:05', 'YYYY-MM-DD HH24:MI:SS'),
'中证500', '000906', '中百集团', 'XSHE', 0.0011, to_date('2018-06-30 05:48:06', 'YYYY-MM-DD HH24:MI:SS'), 1);

insert into factorsch.index_example_tsdb
values(to_date('2006-11-30','YYYY-MM-DD'), '600031', to_date('2018-06-30 03:48:05', 'YYYY-MM-DD HH24:MI:SS'),
'上证180', '000010', '三一重工', 'XSHG', 0.0043, to_date('2018-06-30 05:48:05', 'YYYY-MM-DD HH24:MI:SS'), 1);
```

创建表 factorsch.index\_example\_olap。

```
create table factorsch.index_example_olap (
    trade_date date,
    stock_code varchar(20),
    effDate timestamp,
    indexShortName varchar(20),
    indexCode varchar(20),
    secShortName varchar(50),
    exchangeCD varchar(10),
    weight decimal(26,6),
    tm_stamp timestamp,
    flag integer,
    primary key (trade_date, stock_code, indexCode, flag)
);
```

插入数据。

```
insert into factorsch.index_example_olap
values(to_date('2006-11-30', 'YYYY-MM-DD'), '000759', to_date('2018-06-30 03:48:05', 'YYYY-MM-DD HH24:MI:SS'),
'中证500', '000905', '中百集团', 'XSHE', 0.0044, to_date('2018-06-30 05:43:05', 'YYYY-MM-DD HH24:MI:SS'), 1);

insert into factorsch.index_example_olap
values(to_date('2006-11-30', 'YYYY-MM-DD'), '000759', to_date('2018-06-30 04:47:05', 'YYYY-MM-DD HH24:MI:SS'),
'中证500', '000906', '中百集团', 'XSHE', 0.0011, to_date('2018-06-30 05:48:06', 'YYYY-MM-DD HH24:MI:SS'), 1);

insert into factorsch.index_example_olap
values(to_date('2006-11-30','YYYY-MM-DD'), '600031', to_date('2018-06-30 03:48:05', 'YYYY-MM-DD HH24:MI:SS'),
'上证180', '000010', '三一重工', 'XSHG', 0.0043, to_date('2018-06-30 05:48:05', 'YYYY-MM-DD HH24:MI:SS'), 1);
```

**第二步：配置订阅发布**

使用 PostgreSQL 的 pgoutput 插件进行逻辑复制，需要配置 publication 来定义哪些表的数据变更需要被逻辑复制。配置
publication 在 PostgreSQL 的不同版本支持的脚本写法不尽相同，本教程以 PostgreSQL 12
版本为例介绍通用的两种配置方式。

方式一：普通用户配置（推荐）

factoruser
是普通的业务数据用户，不具备超级用户权限。配置发布时需要逐一配置每张表，也可以对单一指定表进行取消配置，当有新增表时需要进行添加。这里我们将上文中创建的三张表全部配置。

创建一个发布，先发布两张表 factorsch.index\_example\_tsdb 和 factorsch.stock\_example。

```
CREATE PUBLICATION factordb_publication FOR TABLE factorsch.index_example_tsdb,factorsch.stock_example
```

查看发布和发布的具体表。

```
select * from pg_publication
select * from pg_publication_tables
```

![](images/Debezium_Kafka_PostgreSQL_sync/3-4.png)

图 5. 图 3-4 PostgreSQL 中发布列表查询

![](images/Debezium_Kafka_PostgreSQL_sync/3-5.png)

图 6. 图 3-5 PostgreSQL 中的发布表明细查询

对指定 publication，添加一张表 factorsch.index\_example\_olap。

```
ALTER PUBLICATION factordb_publication ADD TABLE factorsch.index_example_olap;
```

![](images/Debezium_Kafka_PostgreSQL_sync/3-6.png)

图 7. 图 3-6 查看增加的发布表

对指定 publication，删除一张表。

```
ALTER PUBLICATION factordb_publication DROP TABLE factorsch.index_example_olap;
```

删除发布。

```
drop publication factordb_publication
```

方式二：超级用户配置

需要先提升 factoruser 权限为超级用户，可以使用超级用户 postgres 操作。

```
ALTER USER factoruser WITH SUPERUSER;
```

使用超级用户 factoruser 创建全表发布。

```
CREATE PUBLICATION all_tables_publication FOR ALL TABLES;
```

如 图 3-7 所示，所有的表都会被发布，增加新表也会直接变成发布表。

![](images/Debezium_Kafka_PostgreSQL_sync/3-7.png)

图 8. 图 3-7 全表订阅发布表列表查看

对于以上两种方式，推荐使用方式一，可以精确进行逻辑复制，控制资源使用，控制用户权限。只有在确实需要整库同步，且表的数据量众多的场景可以使用方式二。

**第三步：准备连接器配置文件，并启动连接任务**

创建连接 PostgreSQL 的 source 连接器配置文件。

```
mkdir -p /KFDATA/datasyn-config
vim /KFDATA/datasyn-config/source-postgres.json
```

录入以下配置，*hostname* 和 kafka 启动地址需对应修改。注意这里的 *publication.name*参数要和配置发布名一致，且要提前配置好。

```
{
    "name": "postgresTask",
    "config": {
     "connector.class" : "io.debezium.connector.postgresql.PostgresConnector",
     "snapshot.mode" : "initial",
     "tasks.max" : "1",
     "topic.prefix" : "pg_factorDB",
     "database.hostname" : "192.168.189.130",
     "database.port" : 5432,
     "database.user" : "datasyn",
     "database.password" : "111111",
     "database.dbname" : "factordb",
     "table.include.list" : "factorsch.index_example_tsdb,factorsch.index_example_olap,factorsch.stock_example",
     "decimal.handling.mode": "string",
     "plugin.name": "pgoutput",
     "publication.name": "factordb_publication",
     "slot.name": "datasyn_slot",
     "heartbeat.interval.ms":"20000"
  }
}
```

重要参数说明：

表 3-1 source 连接器重要参数说明

| 参数名称 | 默认值 | 参数说明 |
| --- | --- | --- |
| connector.class | 无 | 连接器的 Java 类的名称。这里是 PostgreSQL 的连接器类名。 |
| tasks.max | 1 | 当前 connector 的最大并行任务数。PostgreSQL 的 source 连接器任务数只能是 1 。 |
| topic.prefix | 无 | 当前 connector 同步写入任务的命名空间。会被用于添加到同步表对应 topic 名称前等。 |
| database.hostname | 无 | PostgreSQL 数据库服务器的 IP 地址或主机名。 |
| database.port | 5432 | PostgreSQL 数据库服务器的整数端口号。 |
| database.user | 无 | PostgreSQL 数据库服务器连接用户。 |
| database.password | 无 | PostgreSQL 数据库服务器连接用户密码。 |
| database.dbname | 无 | PostgreSQL 数据库实例名称。 |
| table.include.list | 无 | 匹配的表名。可以多个，用逗号分割即可。 |
| schema.include.list | 无 | 匹配的模式名。可以多个，用逗号分割即可。 |
| time.precision.mode | adaptive | 针对 PostgreSQL 时态类型的处理模式。  * adaptive 表示根据列的数据类型定义确定文本类型和语义类型。 * adaptive\_time\_microseconds   表示根据列的数据类型定义确定时态类型的文本类型和语义类型，但所有字段都以微秒为单位捕获 connect 使用   Kafka Connect 逻辑类型。推荐设置为 adaptive。 |
| decimal.handling.mode | precise | 针对 PostgreSQL 的 NUMERIC、DECIMAL 和 MONEY 类型的处理模式。”precise” 表示转换成 java.math.BigDecimal ，”double” 表示转换成 double 值，”string” 表示转换成字符串。需设置为 string。 |
| slot.name | debezium | PostgreSQL 逻辑解码槽的名称，该槽是为从特定数据库/架构的特定插件流式传输更改而创建的。服务器使用此插槽将事件流式传输到您正在配置的 Debezium 连接器。插槽名称必须符合 PostgreSQL 复制插槽命名规则，该规则规定*：“每个复制插槽都有一个名称，该名称可以包含小写字母、数字和下划线字符。”* |
| slot.drop.on.stop | false | 当连接器正常停止时，是否删除逻辑复制槽。 |
| snapshot.mode | initial | 指定 connector 用来捕获表快照的形式。常用的是 ”initial” 和 ”schema\_only” 。“initial“ 在 connector 第一次启动时会获取表结构和表的快照数据，并继续获取新增的变更数据。”schema\_only” 表示只获取表结构，并只会获取新增的变更数据。其他形式请参考 debezium 官方文档。 |
| publication.name | dbz\_publication | 使用 pgoutput 时的发布名称。如果此发布尚不存在，则在启动时创建此发布，并且它包含**所有表**。 然后，Debezium 应用其自己的包含/排除列表过滤（如果已配置），以将发布限制为感兴趣的特定表的更改事件。 连接器用户必须具有超级用户权限才能创建此发布。 因此，通常最好在首次启动连接器之前创建发布。 |
| plugin.name | decoderbufs | 安装在 PostgreSQL 服务器上的 PostgreSQL 逻辑解码插件的名称，本教程使用的是 pgoutput 插件，需要明确配置该参数为 “*pgoutput*“。 |
| heartbeat.interval.ms | 0 | 控制连接器向 Kafka 主题发送心跳消息的频率。默认行为是连接器不发送心跳消息。配置调整该参数，则监视器指定的时间间隔内，接收到数据库任何改变事件都会记录偏移量到 Kafka。请将此属性设置为正整数，表示心跳消息之间的毫秒数。不配置调整该参数，则监视器只会在接收到需要同步写入 Kafka 的改变事件时才会记录偏移量到 Kafka。这种情况 Kafka 中记录的偏移量可能落后很多。这意味着不会向 Kafka 提交偏移更新的同时，连接器也没有机会将最新检索到的 LSN 发送到数据库。数据库保留 WAL 文件，其中包含连接器已处理的事件。发送心跳消息使连接器能够将最新检索到的 LSN 发送到数据库，这允许数据库回收不再需要的 WAL 文件所使用的磁盘空间。 |

更多详细参数说明可以参看 Debezium
2.5，不同Debezium版本的参数配置不同，若使用其他版本的Debezium，需找到对应文档做修改。

**第三步： 启动 PostgreSQL 的数据同步任务**

通过 REST API 启动 PostgreSQL 的 source 连接器。

```
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://192.168.189.130:8083/connectors/ -d @/KFDATA/datasyn-config/source-postgres.json
```

也可以通过 kafka-tools 中的脚本启动。

```
cd /KFDATA/kafka-tools/bin
./rest.sh create /KFDATA/datasyn-config/source-postgres.json
```

![](images/Debezium_Kafka_PostgreSQL_sync/3-8.png)

图 9. 图 3-8 source 连接器启动成功信息

**第四步：查看 PostgreSQL 数据同步任务状态**

查看同步任务列表。*list* 参数展示任务名列表，*showall* 参数会显示全部同步任务状态。

```
cd /KFDATA/kafka-tools/bin
./rest.sh showall
```

当前只有一个同步任务，如下图所示。

![](images/Debezium_Kafka_PostgreSQL_sync/3-9.png)

图 10. 图 3-9 查看全部同步任务状态信息

查看 kafka 中的 topic列表：

```
./kafka.sh tplist
```

![](images/Debezium_Kafka_PostgreSQL_sync/3-10.png)

图 11. 图 3-10 当前 kafka 中的 topic 列表

查看表 stock\_example、index\_example\_tsdb、index\_example\_olap 目前进入到 kafka 中的数据条数：

```
./kafka.sh get_offsets pg_factorDB.factorsch.stock_example
./kafka.sh get_offsets pg_factorDB.factorsch.index_example_tsdb
./kafka.sh get_offsets pg_factorDB.factorsch.index_example_olap
```

结果如图所示，当前配置的三张数据数据表的历史数据都已经写入了 kafka 中的对应 topic 中。

![](images/Debezium_Kafka_PostgreSQL_sync/3-11.png)

图 12. 图 3-11 对应 topic 中数据条数信息

## 4. 从Kafka 到 DolphinDB 的数据同步：部署程序与配置任务

### 4.1 安装 Kafka-DolphinDB 数据同步连接器插件

配置启动 Kafka-DolphinDB 连接器，需要以下两步：

* 下载 Kafka-DolphinDB-Connector 插件，将插件解压并放到 Kafka Connect 的插件路径下。
* 重新启动 Kafka Connect 程序，以加载插件。

**第一步：下载 Kafka-DolphinDB 插件**

* [jdbc-1.30.22.5-CDC.jar](https://cdn.dolphindb.cn/zh/tutorials/script/Debezium_Kafka_PostgreSQL_sync/jdbc-1.30.22.5-CDC.jar)：该包为 DolphinDB JDBC
  包为数据同步做了一些专门修改，为特殊版本。
* [kafka-connect-jdbc-4.00.jar](https://cdn.dolphindb.cn/zh/tutorials/script/Debezium_Kafka_PostgreSQL_sync/kafka-connect-jdbc-4.00.jar)：是基于kafka-connect-jdbc-10.7.4 开发的
  DolphinDB 连接器，后续会进行代码开源。

创建插件路径，在此路径下放置 Kafka-DolphinDB 插件包，将上述两个 jar 包放在此目录下。请确保 kafka
用户包含对这两个文件的读权限。

```
sudo mkdir -p /opt/confluent/share/java/plugin/kafka-connect-jdbc
sudo cp ~/jdbc-1.30.22.5-CDC.jar /opt/confluent/share/java/plugin/kafka-connect-jdbc/
sudo cp ~/kafka-connect-jdbc-10.7.4-ddb1.04.OLAP.jar /opt/confluent/share/java/plugin/kafka-connect-jdbc/
```

如果上面的操作碰到权限问题，则可以使用以下命令赋予权限。

```
sudo chmod o+rx /opt/confluent/share/java/plugin/kafka-connect-jdbc/*
```

**第二步： 重启 kafka-connect**

```
sudo systemctl restart kafka-connect
```

查看 kafka-connect 路径的日志输出

```
cat /KFDATA/kafka-connect/logs/connect.log | grep JdbcSinkConnector
```

如下图所示，则插件加载成功。

图 13. 图 4 -1 Kafka-DolphinDB 插件加载成功信息

![](images/Debezium_Kafka_PostgreSQL_sync/4-1.png)

### 4.2 配置 DolphinDB 的数据同步连接任务

**第一步：创建同步的 DolphinDB 库、表**

根据 PostgreSQL 表结构，创建与 PostgreSQL 表结构一致的表，PostgreSQL 数据类型转换为 DolphinDB 数据类型对照表可以参考
[5.2 节](#topic_szb_1bg_vfc)。

创建单主键表 stock\_example 的 DolphinDB 对应表：

```
//创建 dfs://stock_data 数据库
if (existsDatabase("dfs://stock_data"))dropDatabase("dfs://stock_data")
dbName = "dfs://stock_data"
db=database(directory=dbName, partitionType=HASH, partitionScheme=[LONG, 3], engine="TSDB", atomic="CHUNK")
//创建 stock_example 表
tbName = "stock_example"
colNames = `id`ts_code`symbol_id`name`area`industry`list_date`dummySortKey__
colTypes = `LONG`SYMBOL`SYMBOL`SYMBOL`SYMBOL`SYMBOL`DATE`INT
t = table(1:0, colNames, colTypes)
db.createPartitionedTable(t, tbName, partitionColumns=`id, sortColumns=`id`dummySortKey__, keepDuplicates=LAST, sortKeyMappingFunction=[hashBucket{,100}], softDelete=true)
```

创建复合主键表 index\_example\_olap 的 DolphinDB 对应表：

```
//创建 dfs://index_data_olap 数据库
if (existsDatabase("dfs://index_data_olap"))dropDatabase("dfs://index_data_olap")
dbName = "dfs://index_data_olap"
db = database(directory=dbName, partitionType=RANGE, partitionScheme=1990.01M+(0..80)*12,  atomic="CHUNK")
//创建 olap 引擎数据库下的 index_example
tbName = "index_example"
colNames = `trade_date`stock_code`effDate`indexShortName`indexCode`secShortName`exchangeCD`weight`tm_stamp`flag
colTypes = `DATE`SYMBOL`TIMESTAMP`SYMBOL`SYMBOL`SYMBOL`SYMBOL`DOUBLE`TIMESTAMP`INT
t = table(1:0, colNames, colTypes)
db.createPartitionedTable(t, tbName, partitionColumns=`trade_date)
```

创建复合主键表 index\_example\_tsdb 的 DolphinDB 对应表:

```
//创建 dfs://index_data_tsdb 数据库
if (existsDatabase("dfs://index_data_tsdb"))dropDatabase("dfs://index_data_tsdb")
dbName = "dfs://index_data_tsdb"
db = database(directory=dbName, partitionType=RANGE, partitionScheme=1990.01M+(0..80)*12, engine="TSDB", atomic="CHUNK")
//创建 tsdb 引擎数据库下的 index_example
tbName = "index_example"
colNames = `trade_date`stock_code`effDate`indexShortName`indexCode`secShortName`exchangeCD`weight`tm_stamp`flag
colTypes = `DATE`SYMBOL`TIMESTAMP`SYMBOL`SYMBOL`SYMBOL`SYMBOL`DOUBLE`TIMESTAMP`INT
t = table(1:0, colNames, colTypes)
db.createPartitionedTable(t, tbName, partitionColumns=`trade_date, sortColumns=`stock_code`indexCode`flag`trade_date, keepDuplicates=LAST, sortKeyMappingFunction=[hashBucket{,10},hashBucket{,10},hashBucket{,1}], softDelete=true)
```

注：建表时的软删除功能，即 *softDelete* 选项需要 DolphinDB 2.00.11 及以上的版本。旧版本 DolphinDB
建表时可以去除该选项。

**第二步： 配置同步配置表**

在DolphinDB 中创建一张配置表，记录 kafka topic 和 DolphinDB 库表之间的映射关系。配置表的库表名可以自行调整，并在
DolphinDB 的同步任务中设置相应的库表名称。配置表中字段名是固定的，需和示例保持一致。

数据库名：dfs://ddb\_sync\_config

表名：sync\_config

```
db = database("dfs://ddb_sync_config", HASH, [SYMBOL, 2])
t = table(1:0, `connector_name`topic_name`target_db`target_tab`add_sortcol_flag`primary_key,
[SYMBOL, SYMBOL, SYMBOL, SYMBOL, SYMBOL, SYMBOL])
db.createTable(t, "sync_config")
```

kafka topic 名可以通过之前介绍的 ./kafka.sh tplist 的命令查看，当前配置的三张表对应的 topic 如下：

* 单主键同步到 TSDB 引擎 : stock\_example -> pg\_factorDB.factorsch.stock\_example。
* 复合主键同步到 TSDB 引擎 :
  index\_example\_tsdb->pg\_factorDB.factorsch.index\_example\_tsdb
* 复合主键同步到 OLAP 引擎 : index\_example\_olap
  ->pg\_factorDB.factorsch.index\_example\_olap。

插入配置信息表，将 kafka 中的 topic 和 DolphinDB 库表名称一一对应。

```
def addSyncConfig(connector_name, topic_name, dbname, tbname, add_sortcol_flag="0",primary_key=NULL) {
    loadTable("dfs://ddb_sync_config", "sync_config").append!(
    table([connector_name] as col1,
    [topic_name] as col2,
    [dbname] as col3,
    [tbname] as col4,
    [add_sortcol_flag] as col5,
    [primary_key] as col6))
}

addSyncConfig("ddb-sink-postgres", "pg_factorDB.factorsch.stock_example", "dfs://stock_data", "stock_example", "1", "")
addSyncConfig("ddb-sink-postgres", "pg_factorDB.factorsch.index_example_tsdb", "dfs://index_data_tsdb", "index_example", "0", "")
addSyncConfig("ddb-sink-postgres", "pg_factorDB.factorsch.index_example_olap", "dfs://index_data_olap", "index_example", "0", "stock_code,indexCode,flag,trade_date")
```

以下是配置表的各个字段说明：

表 4-1 同步配置表字段说明

| 字段名 | 类型 | 字段作用 |
| --- | --- | --- |
| connector\_name | SYMBOL | 配置的 DolphinDB Sink 同步任务名 |
| topic\_name | SYMBOL | 要同步的 kafka topic 名称 |
| target\_db | SYMBOL | 对应的 DolphinDB 分布式库名 |
| target\_tab | SYMBOL | 对应的 DolphinDB 分布式表名 |
| add\_sortcol\_flag | SYMBOL | 是否需要添加 dummySortKey\_\_ 列，需要则设置为 ”1”，否则设置为 ”0”。主要应对单主键表同步到 DolphinDB 的 TSDB 引擎数据表的场景。具体原因详见 [4.1 节的DolphinDB 同步须知](#topic_ksw_z1g_vfc)。 |
| primary\_key | SYMBOL | 设置来源表的主键。当数据同步到 OLAP 引擎时，必须指定该字段。数据同步到 TSDB 引擎时，无须指定。复合主键按来源库顺序逗号分隔。 |

**第三步： 准备连接器配置文件，并启动连接任务**

创建 DolphinDB 数据同步任务配置文件。

```
cd /KFDATA/datasyn-config
vim ddb-sink-postgres.json
```

配置如下：

```
{
    "name": "ddb-sink-postgres",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": "1",
        "topics": "pg_factorDB.factorsch.stock_example,pg_factorDB.factorsch.index_example_tsdb,pg_factorDB.factorsch.index_example_olap",
        "connection.url": "jdbc:dolphindb://192.168.189.130:8848?user=admin&password=123456",
        "transforms": "unwrap",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
        "transforms.unwrap.drop.tombstones": "false",
        "auto.evolve": "false",
        "insert.mode": "upsert",
        "delete.enabled": "true",
        "batch.size":"10000",
        "pk.mode": "record_key",
        "ddbsync.config.table":"dfs://ddb_sync_config,sync_config",
        "ddbsync.addSortColFlag":"true",
        "ddbsync.config.engineTypes" :"TSDB,OLAP"
    }
}-
```

表 4-2 sink 连接器重要参数说明

| 参数名称 | 默认值 | 参数说明 |
| --- | --- | --- |
| name | 无 | 同步任务名称，不可重复。 |
| connector.class | 无 | 连接器的 Java 类的名称。这里是 JdbcSink 的通用连接器类名。 |
| tasks.max | 1 | 当前 connector 的最大并行任务数。可以调节增大，会创建多 consumer 并行消费读取 Kafka 中数据。一般的数据同步场景设置到 10 基本可以满足同步速度上的需求。 |
| topics | 无 | 配置要同步的 Kafka 中的 topic 名称，配置多个 topic 时用逗号分割。 |
| connection.url | 无 | DolphinDB 数据库服务器的 IP 地址或主机名。 |
| transforms | 无 | 声明数据转换操作，请设置为 unwrap。 |
| transforms.unwrap.type | 无 | 声明数据转换器类别。请设置为 false。 |
| transforms.unwrap.drop.tombstones | false | 声明是否删除 Kafka 中的墓碑数据。请设置为 false。 |
| auto.evolve | true | 当 DolphinDB 中缺少列时，是否自动增加列。当前不支持自动增加列，必须配置为 false。 |
| insert.mode | insert | 数据插入模式。可设置为 insert 和 upsert。当使用 OLAP 引擎时必须设置为 upsert。 |
| pk.mode | none | 主键模式。必须设置为 record\_key。 |
| delete.enabled | false | 在主键模式为 record\_key 情况下。对于 null 值 record 是否按照 delete 进行操作。 |
| batch.size | 3000 | 设置在数据量足够大时。以每批最大多少条来写入到目标数据库。注意：当该值大于 Connect worker 中设置的 consumer.max.pol.records 时，每次提交数量会受 consumer.max.pol.records 的值限制。 |
| ddbsync.config.table | * dfs://ddb\_sync\_config, * sync\_config | Kafka 中的 topic 对应 DolphinDB 表的配置表名称。可以自行定义库、表名称。但表中的字段要保持一致。表结构见 [3.2 节](#topic_est_z1g_vfc)。 |
| ddbsync.addSortColFlag | false | 是否开启补充列。若部分表需要通过补充列 “dummySortKey\_\_” 字段来设置 sortColumns，则需要开启。主要应对单主键表同步到 TSDB 引擎的场景。具体原因见 [4.1 节](#topic_ksw_z1g_vfc)。 |
| ddbsync.config.engineTypes | 无 | 支持的引擎类型，多个不同的引擎类型以逗号分隔，如 “TSDB，OLAP”。当前支持的引擎有 TSDB 和 OLAP。TSDB 引擎默认开启无法关闭，若配置了 OLAP 引擎，表明支持 使用 upsert 语句同步数据到 OLAP 引擎的表，需要 DolphinDB 版本在 2.00.12.3 以上。 |

参数说明：以上参数项为同步 DolphinDB 所需参数。如果对 Confluent 的 JDBC Sink Connect 有经验可适当调节。

通过 REST API 启动 source 连接器：

```
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://183.134.101.144:8083/connectors/ -d @ddb-sink-postgres.json
```

也可以通过 kafka-tools 中的脚本启动：

```
cd /KFDATA/kafka-tools/bin
./rest.sh create /KFDATA/datasyn-config/ddb-sink-postgres.json
```

查看同步任务状态， ddb-sink-postgres 是 DolphinDB 的数据同步任务，可以看到现在我们有两个同步任务，这样构成了从 PostgreSQL
到 DolphinDB 的数据同步链。

```
./rest.sh showall
```

![](images/Debezium_Kafka_PostgreSQL_sync/4-2.png)

图 14. 图 4-2 同步任务状态信息

**第四步： 查看表初始数据同步进度**

在设置 PostgreSQL 同步任务时，将 *snapshot.mode* 选项值设置为 *”initial”* ，该选项意味着
PostgreSQL 会同步表的初始数据到 Kafka 中，设置完下游的 DolphinDB 任务后，可以检查初始数据的同步情况。

通过 kafka.sh 脚本查看消费者列表：

```
./kafka.sh cm_list
```

![](images/Debezium_Kafka_PostgreSQL_sync/4-3.png)

图 15. 图 4-3 Kafka 消费者列表信息

查看 DolphinDB 同步任务对应的 Kafka 消费组中的每一个 consumer 的消费进度，通过此命令可以查看同步程序中每一张的表同步进度。 Lag 为
0 则表示 Kafka 中 topic 当前没有未消费的数据，即 Kafka 中的数据与对应表的数据是一致的。

```
./kafka.sh cm_detail connect-ddb-sink-postgres
```

![](images/Debezium_Kafka_PostgreSQL_sync/4-4.png)

图 16. 图 4-4 connect-ddb-sink 中每张表同步进度

如 图 4-4 显示，数据已被 DolphinDB 同步任务消费完毕，此时在 DolphinDB 的 web 界面查看表中数据，表数据和 PostgreSQL
表中数据是一致的。

![](images/Debezium_Kafka_PostgreSQL_sync/4-5.png)

图 17. 图 4-5 DolphinDB中 index\_example 表数据

![](images/Debezium_Kafka_PostgreSQL_sync/4-6.png)

图 18. 图 4-6 DolphinDB 中 stock\_example表数据

### 4.3 实时同步验证

**第一步：插入数据**

向 PostgreSQL 中 factorsch.index\_example\_tsdb 表中插入两条新数据：

```
insert into factorsch.index_example_tsdb
values (to_date('2006-11-30', 'YYYY-MM-DD'), '600054',
to_date('2018-06-30 05:48:05', 'YYYY-MM-DD HH:MI:SS'), '上证180', '000010', '三一重工',
'XXXB', 0.0043, to_date('2018-06-30 05:48:05', 'YYYY-MM-DD HH24:MI:SS'), 1);

insert into factorsch.index_example_tsdb
values (to_date('2006-11-30', 'YYYY-MM-DD'), '600055
',
to_date('2018-06-30 06:48:02', 'YYYY-MM-DD HH:MI:SS'), '沪深300', '000300', '三一重工',
'XSHG', 0.0029, to_date('2018-06-30 05:48:05', 'YYYY-MM-DD HH24:MI:SS'), 1);
```

查看 DolphinDB 对应的表数据：

```
select * from loadTable("dfs://index_data_tsdb","index_example")
```

可以看到新数据已写入：

![](images/Debezium_Kafka_PostgreSQL_sync/4-7.png)

图 19. 图4-7 数据写入成功

**第二步：更新数据**

更新 PostgreSQL 中 factorsch.index\_example\_olap 表的 tmp\_stamp 和 secshortname 的值。

```
update factorsch.index_example_olap
set tm_stamp = to_date('2025-02-28 16:00:00', 'YYYY-MM-DD HH24:MI:SS'),
secshortname ='测试修改名称'
where stock_code='000759'
```

查看 DolphinDB 中数据，数据已被修改：

```
select * from loadTable("dfs://index_data_olap","index_example")
```

![](images/Debezium_Kafka_PostgreSQL_sync/4-8.png)

图 20. 图4-8 数据更新成功

**第三步：删除数据**

在 PostgreSQL 中的 factorsch.stock\_example 删除一条数据：

```
delete from factorsch.stock_example where ts_code='000004.SZ'
```

再查看 DolphinDB 中数据，数据已被删除：

```
select * from loadTable("dfs://index_data_tsdb","index_example")
```

![](images/Debezium_Kafka_PostgreSQL_sync/4-9.png)

图 21. 图4-9 数据删除成功

## 5. 部署注意事项

### 5.1 实时同步须知

DolphinDB 是一款支持海量数据的分布式时序数据库。针对不同的数据处理需求，在底层架构上天然上与通常的关系型数据库不同，所以需要有以下限制：

* DolphinDB 的表没有主键设计，若使用 TSDB 引擎，需将主键设置为 sortColumn 字段，并设置 keepDuplicates=LAST
  来进行去重，以确保数据唯一性。TSDB 引擎的 sortColumn 是分区内去重，如果使用的是分区表，需要至少将其中一个主键列设置为分区列。若使用
  OLAP 引擎，需在同步配置表中设置目标库的主键。
* PostgreSQL 表的主键可能不满足 TSDB 引擎的 sortColumn 设置规则，有以下三种情况：
  + PostgreSQL 表中有两个及以上的主键，其中一个主键为整数类型或时间类型，但末尾列不是整数类型或时间类型：
    - 该情况需要调整 sortColumn 设置的顺序，将整数类型或时间类型的主键移动到末尾。
  + PostgreSQL 表中只有一个主键，或者 PostgreSQL 表中的主键的数据类型均不包含整数类型或时间类型：
    - 该情况需要建表时在末尾补充一个 dummySortKey\_\_ 列，值均设置为0，对应同步程序的配置表中需要将
      add\_sortcol\_flag 列的值设置为 “1”，并将 DolphinDB 同步连接任务中
      “ddbsync.addSortColFlag” 设置为 “true”。若使用 DataX
      等工具进行初始全表同步，则需要做数据转换，提供该字段对应初始值。
  + PostgreSQL 表中的主键类型包含 DolphinDB 不支持的类型。
    - DolphinDB TSDB 引擎的 sortColumns
      支持整数、日期或时间、字符串类型，暂时不支持小数类型，但在后续的版本里可能提供支持，请关注版本更新。

DDL 语句相关：

* 当前不支持 DDL 语句同步。
* 若表结构发生更改，需进行单表修复，具体操作后续会在实时同步的运维手册文档中给出。

其他：

* 表字段命名时，请尽量规避一些简单的名字，比如 code, timestamp 等，这种命名与 DolphinDB
  内关键字重复，可能会导致无法正确同步。

### 5.2 PostgreSQL-DolphinDB 数据类型对应表

以下的类型对应表为推荐设置的 DolphinDB 类型，注意两者数据类型表示的精度范围，确保 DolphinDB 数据类型的精度可以覆盖原 PostgreSQL
类型。

表 5-1 PostgreSQL-DolphinDB 数据类型对应表

| PostgreSQL 类型 | DolphinDB 类型 |
| --- | --- |
| NUMERIC[(M[,D])]/DECIMAL[(M[,D])]/MONEY[(M[,D])] | DOUBLE / DECIMAL |
| REAL | FLOAT |
| DOUBLE PRECISION | DOUBLE |
| SMALLINT, SMALLSERIAL | SHORT |
| INTEGER, SERIAL | INT |
| BIGINT, BIGSERIAL, OID | LONG |
| CHAR[(M)]/VARCHAR[(M)]/CHARACTER[(M)]/CHARACTER VARYING[(M)] | SYMBOL / STRING |
| DATE | DATE（仅日期） |
| TIME(1-3)，TIMETZ | TIME |
| TIME（4-6） | NANOTIME |
| TIMESTAMP(0 - 3)，TIMESTAMPTZ | TIMESTAMP（毫秒级时间戳） |
| TIMESTAMP, TIMESTAMP(4 - 6)，TIMESTAMP | NANOTIMESTAMP（纳秒级时间戳） |
| BOOLEAN/BIT（1） | BOOL |

在浮点数数据处理上，PostgreSQL 的 DECIMAL 类型是精确值，DolphinDB 的 DOUBLE 类型的精度为15-16 位有效数字，如果转换成
DolphinDB 的 DOUBLE 类型，会存在浮点数精度丢失问题。因此推荐用户转换成 DolphinDB 的 DECIMAL 类型，确保浮点数精度。

在时间类型转换上，请参照表中的类型映射，以保证 DolphinDB 中的时间类型字段在精度上可以覆盖 PostgreSQL
中时间类型字段的精度。对于带有时区信息的时间类型，DolphinDB 统一以 UTC 时区存储。

## 6. 同步性能测试

### 6.1 性能测试配置

**建表语句**

PostgreSQL 建表，并生成测试数据代码：

```
DROP TABLE if EXISTS factorsch.performance_test1;
CREATE TABLE factorsch.performance_test1 (
    dt date,
    id varchar(20),
    str1 char(10),
    val DECIMAL,
    qty varchar(20),
    tm TIMESTAMP
);
-- 生成100w行数据，每天1000行
INSERT INTO factorsch.performance_test1 (dt,id,str1,val,qty,tm)
SELECT ('2020-01-01'::date + (gs - 1) / 1000),
    ((gs-1)%1000+1),'aa',
    1.234,
    1000,
    '2024-01-01 15:00:00'::timestamp
FROM generate_series(1, 1000000) gs;

ALTER TABLE factorsch.performance_test1
ADD CONSTRAINT pk_performance_test1 PRIMARY KEY (id, dt);

DROP TABLE if EXISTS factorsch.performance_test2;
CREATE TABLE debezium.performance_test2 (
    dt date,
    id varchar(20),
    str1 char(10),
    val DECIMAL,
    qty varchar(20),
    tm TIMESTAMP
);
-- 生成1亿行数据，每天100000行
INSERT INTO factorsch.performance_test2 (dt,id,str1,val,qty,tm)
SELECT ('2020-01-01'::date + (gs - 1) / 100000),
    ((gs-1)%100000+1),'aa',
    1.234,
    1000,
    '2024-01-01 15:00:00'::timestamp
FROM generate_series(1, 100000000) gs;

ALTER TABLE factorsch.performance_test2
ADD CONSTRAINT pk_performance_test2 PRIMARY KEY (id, dt);

grant select on factorsch.performance_test1 to datasyn;
grant select on factorsch.performance_test2 to datasyn;
```

DolphinDB 建表代码：

```
dbName = "dfs://performance_test1"
tbName = "performance_test1"
colNames = `dt`id`str1`val`qty`tm
colTypes = `DATE`SYMBOL`SYMBOL`DOUBLE`LONG`TIMESTAMP
t = table(1:0, colNames, colTypes)
pkColumns = `id`dt
db = database(dbName, HASH, [SYMBOL, 2], , 'TSDB', 'CHUNK')
db.createTable(t, tbName, sortColumns=pkColumns, keepDuplicates=LAST, softDelete=true)

dbName = "dfs://performance_test2"
tbName = "performance_test2"
colNames = `dt`id`str1`val`qty`tm
colTypes = `DATE`SYMBOL`SYMBOL`DOUBLE`LONG`TIMESTAMP
t = table(1:0, colNames, colTypes)
pkColumns = `id`dt
partitionCols = `dt`id
db1 = database(, RANGE, date(datetimeAdd(1990.01M, 0..100*12, 'M')))
db2 = database(, HASH, [SYMBOL, 50])
db = database(dbName, COMPO, [db1, db2], , `TSDB, `CHUNK)
db.createPartitionedTable(t, tbName, partitionColumns=partitionCols, sortColumns=pkColumns, keepDuplicates=LAST, softDelete=true)
```

### 6.2 性能测试结果

性能测试结果如下表所示，其中总耗时等于 DolphinDB 更新完成时间减去 PostgreSQL 更新完成时间，因此总耗时包含了以下数据同步的完整链路：

* Debezium 挖掘 PostgreSQL 日志到 Kafka
* Kafka 推送数据给相应 topic 的消费者
* 下游的 DolphinDB Connector 消费 Kafka 中数据，解析为相应的 DolphinDB 更新语句，并执行写入 DolphinDB
  完成

Kafka 每次推送的变更数据在 3000-4000 条，具体条数和 Kafka 的日志大小配置相关。对于 insert 和 update
类型的操作，DolphinDB 的处理效率很高。对于 delete 类型操作，由于 delete 操作涉及数据查找，DolphinDB
的处理效率和具体表的数据行数、分区方式相关。

表 6-1 使用 pgoutput 插件进行数据同步性能测试结果

| 测试表 | 原始数据行数 | 测试表大小 | 操作类型 | 操作行数 | 总耗时 |
| --- | --- | --- | --- | --- | --- |
| 表1 performance\_test1 | 100万 | 65MB | insert | 1 | 2s |
| 10,000 | 2s |
| 1,000,000 | 18s |
| update | 1 | 2s |
| 10,000 | 4s |
| 1,000,000 | 20s |
| delete | 1 | 2s |
| 10,000 | 9s |
| 1,000,000 | 3min15s |
| 表2 performance\_test2 | 1亿 | 7224MB | insert | 1 | 1s |
| 10,000 | 2s |
| 1,000,000 | 30s |
| update | 1 | 1s |
| 10,000 | 4s |
| 1,000,000 | 25s |
| delete | 1 | 3s |
| 10,000 | 7s |
| 1,000,000 | 4min15s |

## 7. 常见问题解答（FAQ）

### 7.1 创建同步任务时报错

**（1）json 文件格式错误**

![](images/Debezium_Kafka_PostgreSQL_sync/7-1.jpg)

图 22. 图 7-1 json文件格式错误报错信息

造成上述问题的原因可能是多了逗号、少了逗号或者括号不正确，需要检查并修订 json 文件。

**（2）Failed to find any class that implements Connector**

![](images/Debezium_Kafka_PostgreSQL_sync/7-2.png)

图 23. 图 7-2 PostgreSQL 数据库无法正常连接报错信息

该报错提示意味着 PostgreSQL 数据库无法正常连接。造成上述问题的可能原因：

* 未将 debezium-connector-postgres-2.5.1.Final.jar 包放置到插件目录下
* Kafka 用户对 debezium-connector-postgres-2.5.1.Final.jar 文件没有读权限

**（3）Can’t find JdbcSinkConnector**

查看日志提示没有 JdbcSinkConnector 包的加载。JdbcSinkConnector 是包含在
kafka-connect-jdbc-4.00.jar 包内，需要确认该 jar 包是否放置在 kafka connect 的插件路径下，确认 kafka
对该文件的读权限。再通过 `java --version` 查看 Java 版本是否是17，Java
版本较低时，可能无法正确加载插件。目前已知使用 Java 8 时无法正确加载该插件。

### 7.2 数据未同步或者未正确同步

当数据未同步或者未正确同步时，请先按以下两步进行检查。然后对照后面的提供的错误列表进行参考调整。

**step1 查看同步任务状态**

先查看同步任务是否报错：

```
cd /KFDATA/kafka-tools/bin
./rest.sh showall
```

再看 kafka connect 的日志中是否出现 ERROR：

```
cd /KFDATA/kafka-connect/logs
cat connect.log | grep ERROR
```

如果有出现 ERROR，看 ERROR 显示的日志是 PostgreSQL 报错还是 ddb-sink 报错，查看具体的报错信息。如果同步任务未报错，也没有
ERROR，再通过以下方式排查。

**step2 查看 PostgreSQL 数据是否同步到 Kafka**

查看 Kafka 所有的 topic：

```
cd /KFDATA/kafka-tools/bin
./kafka.sh tplist
```

![](images/Debezium_Kafka_PostgreSQL_sync/7-3.png)

图 24. 图 7-3 kafka 中 topic 信息

在查看该 topic 对应的数据条数：

```
./kafka.sh get_offsets postgres_service.debezium.index_example
```

* **一张表出现两个 topic 名字**

这说明 PostgreSQL source 任务的 topic.prefix 或 DolphinDB sink 任务的 topics
配置项拼写有误，请检查这两项。DolphinDB sink 任务的 topics 必须为 {topic.prefix}.{schema}.{tablename}
的格式。创建 sink 任务时，如果 topic 不存在，则会自动创建 topic，因此拼写错误会导致出现两个 topic 。

* **没有表对应的 topic / 有对应的 topic，但数据条数为0**

这说明 PostgreSQL 数据未正常同步到 Kafka 中，请在同步任务的 table.include.list 中检查 PostgreSQL
表名的拼写,或者检查用户是否拥有 REPLICATION 和 LOGIN 权限和对对应表的 SELECT 权限。

* **有对应的 topic，有数据条数，但 DolphinDB 未同步**

检查 DolphinDB Sink 任务中 topics 配置项中的拼写，检查同步任务配置表中是否有相同的条数。

查看 Kafka 中数据是否与 PostgreSQL 变更数据一致：

```
./tpconsumer.sh --op=2 --topic=postgres_service.debezium.index_example --offset=0 --max-messages=20
```

在显示的结果中，初始数据同步的消息数据 op = r，新插入数据 op = c，更新数据 op = u。

### 7.3 同步任务运行报错

* **Java.lang.OutOfMemoryError**

Kafka Connect 的默认内存为 1 GB，当数据更新量较大时会出现 JVM 内存不足，需要调整 JVM 大小。根据之前配置的安装路径，修改 kafka
connect 的配置文件：

```
vim /KFDATA/kafka-connect/etc/kafka-connect.env
```

在末尾加入 JVM 选项，内存大小根据实际需要调整：

```
KAFKA_HEAP_OPTS="-Xms10G -Xmx10G"
```

* **permission denied for database postgres at
  io.debezium.connector.postgresql.connection.PostgresReplicationConnection.initPublication(PostgresReplicationConnection**

使用 pgoutput 插件同步时未预先创建发布，会报此错误。

```
CREATE PUBLICATION dbz_publication FOR TABLE debezium.index_example,debezium.stock_example;
```

* **Creation of replication slot failed; when setting up multiple connectors
  for the same database host, please make sure to use a distinct
  replication slot name for each**

每个 Debezium
连接器需要使用唯一的复制槽名称。如果多个连接器使用相同的复制槽名称，就会导致冲突。可以为每个连接器使用不同的复制槽名称或者删除原先复制槽。

```
SELECT * FROM pg_drop_replication_slot('your_slot_name');
```

## 8. 附录

* DolphinDB 的 Kafka-Connect 插件包：[kafka-connect-jdbc-4.00.jar](https://cdn.dolphindb.cn/zh/tutorials/script/Debezium_Kafka_PostgreSQL_sync/kafka-connect-jdbc-4.00.jar)
* DolphinDB 的 JDBC 包：[jdbc-1.30.22.5-CDC.jar](https://cdn.dolphindb.cn/zh/tutorials/script/Debezium_Kafka_PostgreSQL_sync/jdbc-1.30.22.5-CDC.jar)
* 运维脚本包 kafka-tools：[kafka-tools.tar](https://cdn.dolphindb.cn/zh/tutorials/script/Debezium_Kafka_PostgreSQL_sync/kafka-tools.tar)
