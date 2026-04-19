<!-- Auto-mirrored from upstream `documentation-main/tutorials/ClickHouse_to_DolphinDB.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 安装 unixODBC 库
apt-get install unixodbc unixodbc-dev
```

#### 下载 ClickHouse 的 ODBC 驱动并安装

第一步，下载 [clickhouse-odbc](https://github.com/ClickHouse/clickhouse-odbc/releases/download/v1.2.1.20220905/clickhouse-odbc-linux.zip) 并解压至自定义目录中，假设安装目录为 <savedir>。

```
mkdir <savedir>
cd <savedir>
wget https://github.com/ClickHouse/clickhouse-odbc/releases/download/v1.2.1.20220905/clickhouse-odbc-linux.zip
unzip clickhouse-odbc-linux.zip
```

第二步，在 **/etc/odbcinst.ini** 文件中，添加以下内容：

**注意**：需要替换 <savedir> 为实际的安装目录。

```
[ODBC Drivers]
ClickHouse ODBC Driver (ANSI)    = Installed
ClickHouse ODBC Driver (Unicode) = Installed

[ClickHouse ODBC Driver (ANSI)]
Description = ODBC Driver (ANSI) for ClickHouse
Driver      = <savedir>/clickhouse-odbc-1.2.1-Linux/lib64/libclickhouseodbc.so
Setup       = <savedir>/clickhouse-odbc-1.2.1-Linux/lib64/libclickhouseodbc.so
UsageCount  = 1

[ClickHouse ODBC Driver (Unicode)]
Description = ODBC Driver (Unicode) for ClickHouse
Driver      =<savedir>/clickhouse-odbc-1.2.1-Linux/lib64/libclickhouseodbcw.so
Setup       =<savedir>/clickhouse-odbc-1.2.1-Linux/lib64/libclickhouseodbcw.so
UsageCount  = 1
```

第三步，在 **/etc/odbc.ini** 文件中，添加以下内容：

**注意**：若不存在该文件可自行创建。

```
[ODBC Data Sources]
ClickHouse DSN (ANSI)=ClickHouse ODBC Driver (ANSI)
ClickHouse DSN (Unicode)=ClickHouse ODBC Driver (Unicode)

[ClickHouseAnsi]
Driver=ClickHouse ODBC Driver (ANSI)
Description=DSN (localhost) for ClickHouse ODBC Driver (ANSI)
Server = localhost
Database = default
UID = default
PWD = 123456
Port = 8123
Proto = http

[ClickHouseUni]
Driver=ClickHouse ODBC Driver (Unicode)
Description=DSN (localhost) for ClickHouse ODBC Driver (Unicode)
Server = localhost
Database = default
UID = default
PWD = 123456
Port = 8123
Proto = http
```

#### 同步数据

1. 运行以下命令加载 ODBC 插件（ `ServerPath` 请自行修改）

   ```
   loadPlugin("ServerPath/plugins/odbc/PluginODBC.txt")
   ```
2. 运行以下命令建立与 ClickHouse 的连接（ Dsn 的名称请自行修改）

   ```
   conn = odbc::connect("Dsn=ClickHouseAnsi", `ClickHouse)
   ```
3. 运行以下命令开始同步数据

   ```
   def syncData(conn, dbName, tbName, dt){
       sql = "select SecurityID, TradeTime, TradePrice, TradeQty, TradeAmount, BuyNo, SellNo, ChannelNo, TradeIndex, TradeBSFlag, BizIndex from migrate.ticksh"
       if(!isNull(dt)) {
           sql = sql + " WHERE toDate(TradeTime) = '"+temporalFormat(dt,'yyyy-MM-dd')+"'"
       }
       odbc::query(conn,sql, loadTable(dbName,tbName), 100000)
   }
   dbName="dfs://TSDB_tick"
   tbName="tick"
   syncData(conn, dbName, tbName, NULL)
   ```

   数据共 27211975 条，同步数据耗时约 158 秒。
4. 同步增量数据

   ```
   def scheduleLoad(conn,dbName,tbName){
       sqlQuery = "select SecurityID, TradeTime, TradePrice, TradeQty, TradeAmount, BuyNo, SellNo, ChannelNo, TradeIndex, TradeBSFlag, BizIndex from migrate.ticksh"
       sql = sqlQuery + " WHERE toDate(TradeTime) = '"+temporalFormat(today()-1,'yyyy-MM-dd')+"'"
       odbc::query(conn,sql, loadTable(dbName,tbName), 100000)
   }
   scheduleJob(jobId=`test, jobDesc="test",jobFunc=scheduleLoad{conn,dbName,tbName},scheduleTime=00:05m,startDate=2023.11.03, endDate=2024.11.03, frequency='D')
   ```

### 通过 DataX 迁移

#### 部署DataX

从 [DataX 下载地址](https://datax-opensource.oss-cn-hangzhou.aliyuncs.com/202309/datax.tar.gz) 下载 DataX 压缩包后，解压至自定义目录。

**注意**：2023 年 9 月后发布的 datax 中才有 clickhousereader 插件，如已安装老版本 datax，则只需下载安装包中的 clickhousereader 复制到 *DataX/plugin/reader* 目录下，即可使用。

#### 部署 DataX-DolphinDBWriter 插件

将 [DataX-DolphinDBWriter](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fdolphindb%2Fdatax-writer)中源码的 *./dist/dolphindbwriter* 目录下所有内容拷贝到 *DataX/plugin/writer* 目录下，即可使用。

#### 执行 DataX 任务

1. 配置 json 文件

   配置文件 *ClickHouseToDDB.json* 的具体内容如下，并将 json 文件置于自定义目录下，本教程中方放置于 *datax-writer-master/ddb\_script/* 目录下。

   ```
   {
           "job": {
                   "content": [{
                           "writer": {
                                   "parameter": {
                                           "dbPath": "dfs://TSDB_tick",
                                           "userId": "admin",
                                           "tableName": "tick",
                                           "host": "127.0.0.1",
                                           "pwd": "123456",
                                           "table": [
                                               {
                                                       "type": "DT_SYMBOL",
                                                       "name": "SecurityID"
                                               },
                                               {
                                                   "type": "DT_TIMESTAMP",
                                                   "name": "TradeTime"
                                               },
                                               {
                                                   "type": "DT_DOUBLE",
                                                   "name": "TradePrice"
                                               },
                                               {
                                                   "type": "DT_INT",
                                                   "name": "TradeQty"
                                               },
                                               {
                                                   "type": "DT_DOUBLE",
                                                   "name": "TradeAmount"
                                               },
                                               {
                                                   "type": "DT_INT",
                                                   "name": "BuyNo"
                                               },
                                               {
                                                   "type": "DT_INT",
                                                   "name": "SellNo"
                                               },
                                               {
                                                   "type": "DT_INT",
                                                   "name": "TradeIndex"
                                               },
                                               {
                                                   "type": "DT_INT",
                                                   "name": "ChannelNo"
                                               },
                                               {
                                                   "type": "DT_SYMBOL",
                                                   "name": "TradeBSFlag"
                                               },
                                               {
                                                   "type": "DT_INT",
                                                   "name": "BizIndex"
                                               }
                                           ],
                                           "port": 10001
                                   },
                                   "name": "dolphindbwriter"
                           },
                           "reader": {
                                   "parameter": {
                                           "username": "default",
                                           "column": ["SecurityID", "toString(TradeTime)", "TradePrice", "TradeQty", "TradeAmount", "BuyNo", "SellNo", "ChannelNo", "TradeIndex", "TradeBSFlag", "BizIndex"],
                                           "connection": [{
                                                   "table": ["ticksh"],
                                                   "jdbcUrl": ["jdbc:clickhouse://127.0.0.1:8123/migrate"]
                                           }],
                                           "password": "123456",
                                           "where": ""
                                   },
                                   "name": "clickhousereader"
                           }
                   }],
                   "setting": {
                           "speed": {
                                   "channel": 1
                           }
                   }
           }
   }
   ```

   **注**：当前 clickhousereader 无法识别 DateTime64 类型，故需转为字符串（`"toString(TradeTime)"`）取数。
2. Linux 终端中执行以下命令以执行 DataX 任务

   ```
   python datax.py ../../datax-writer-master/ddb_script/ClickHouseToDDB.json
   ```
3. 查看 DataX 同步结果

   ```
   任务启动时刻                    : 2023-11-03 17:11:26
   任务结束时刻                    : 2023-11-03 17:14:57
   任务总计耗时                    :                210s
   任务平均流量                    :            8.93MB/s
   记录写入速度                    :         129580rec/s
   读出记录总数                    :            27211975
   读写失败总数                    :                   0
   ```
4. 同步增量数据

   使用 DataX 同步增量数据，可在 `ClickHouseToDDB.json` 的 ”reader“ 中增加 where 条件对数据日期进行筛选，如此每次执行同步任务时至同步 where 条件过滤后的数据，以同步前一天的数据为例，示例如下：

   ```
   "reader": {
       "parameter": {
           "username": "default",
           "column": ["SecurityID", "toString(TradeTime)", "TradePrice", "TradeQty", "TradeAmount", "BuyNo", "SellNo", "ChannelNo", "TradeIndex", "TradeBSFlag", "BizIndex"],
           "connection": [{
               "table": ["ticksh"],
               "jdbcUrl": ["jdbc:clickhouse://127.0.0.1:8123/migrate"]
           }],
           "password": "123456",
           "where": "toDate(TradeTime) = date_sub(day,1,today())"
       },
       "name": "clickhousereader",
   }
   ```

## 基准性能

分别使用 ODBC 插件和 DataX 驱动进行数据迁移， 数据量 2721 万条，迁移耗时对比如下表所示：

| **ODBC 插件** | **DataX** |
| --- | --- |
| 158s | 210s |

综上，ODBC 插件与 DataX 均能实现将 Oracle 中数据迁移到 DolphinDB 中，但是各有优缺点：

* ODBC 使用简单，适合灵活导入数据，但是运维管理不便。
* DataX 需要编写复杂的导入配置，但是其扩展灵活，方便监控，社区支持丰富。

用户可以根据需要自行选择合适的导入方式。

## 附录

### DataX DolphinDB-Writer 配置项

| **配置项** | **是否必须** | **数据类型** | **默认值** | **描述** |
| --- | --- | --- | --- | --- |
| host | 是 | string | 无 | Server Host |
| port | 是 | int | 无 | Server Port |
| userId | 是 | string | 无 | DolphinDB 用户名导入分布式库时，必须要有权限的用户才能操作，否则会返回 |
| pwd | 是 | string | 无 | DolphinDB 用户密码 |
| dbPath | 是 | string | 无 | 需要写入的目标分布式库名称，比如 "dfs://MYDB"。 |
| tableName | 是 | string | 无 | 目标数据表名称 |
| batchSize | 否 | int | 10000000 | datax 每次写入 dolphindb 的批次记录数 |
| table | 是 |  |  | 写入表的字段集合，具体参考后续 table 项配置详解 |
| saveFunctionName | 否 | string | 无 | 自定义数据处理函数。若未指定此配置，插件在接收到 reader 的数据后，会将数据提交到 DolphinDB 并通过 `tableInsert` 函数写入指定库表；如果定义此参数，则会用指定函数替换 `tableInsert` 函数。 |
| saveFunctionDef | 否 | string | 无 | 数据入库自定义函数。此函数指 用 dolphindb 脚本来实现的数据入库过程。 此函数必须接受三个参数：*dfsPath*（分布式库路径）、*tbName*（数据表名）、*data*（从 datax 导入的数据，table 格式） |

### table 配置详解

table 用于配置写入表的字段集合。内部结构为

```
 {"name": "columnName", "type": "DT_STRING", "isKeyField":true}
```

请注意此处列定义的顺序，需要与原表提取的列顺序完全一致。

* *name*：字段名称。
* *isKeyField*：是否唯一键值，可以允许组合唯一键。本属性用于数据更新场景，用于确认更新数据的主键，若无更新数据的场景，无需设置。
* *type* 枚举值以及对应 DolphinDB 数据类型如下

| DolphinDB 类型 | 配置值 |
| --- | --- |
| DOUBLE | DT\_DOUBLE |
| FLOAT | DT\_FLOAT |
| BOOL | DT\_BOOL |
| DATE | DT\_DATE |
| MONTH | DT\_MONTH |
| DATETIME | DT\_DATETIME |
| TIME | DT\_TIME |
| SECOND | DT\_SECOND |
| TIMESTAMP | DT\_TIMESTAMP |
| NANOTIME | DT\_NANOTIME |
| NANOTIMETAMP | DT\_NANOTIMETAMP |
| INT | DT\_INT |
| LONG | DT\_LONG |
| UUID | DT\_UUID |
| SHORT | DT\_SHORT |
| STRING | DT\_STRING |
| SYMBOL | DT\_SYMBOL |

### 完整代码及测试数据

[ClickHouseToDDB.zip](script/ClickHouse_to_DolphinDB/ClickHouseToDDB.zip) 附件中包含以下脚本及测试数据：

* DataX: *ClickHouseToDDB.json*
* DolphinDB: *createTable.dos*、*ClickHouseToDDB\_ODBC.dos*
* 模拟数据：*gendata.dos*
