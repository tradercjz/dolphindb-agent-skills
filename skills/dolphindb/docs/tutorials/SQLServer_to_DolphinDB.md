<!-- Auto-mirrored from upstream `documentation-main/tutorials/SQLServer_to_DolphinDB.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 安装 unixODBC 库
yum install unixODBC-devel
```

1. 在 / etc/freetds.conf 中添加 SQL Server 的 ip 和 port
2. 在 / etc/odbcinst.ini 中完成以下配置

```
[SQLServer]
Description = ODBC for SQLServer
Driver = /usr/lib64/libtdsodbc.so.0.0.0
Setup = /usr/lib64/libtdsodbc.so.0.0.0
FileUsage = 1
```

#### 同步数据

1. 运行以下命令加载 ODBC 插件

```
loadPlugin("/home/Linux64_V2.00.8/server/plugins/odbc/PluginODBC.txt")
```

1. 运行以下命令建立与 SQL Server 的连接

```
conn =odbc::connect("Driver={SQLServer};Servername=sqlserver;Uid=sa;Pwd=DolphinDB;database=historyData;;");
```

1. 运行以下脚本执行同步

```
def transform(mutable msg){
	msg.replaceColumn!(`LocalTime,time(temporalParse(msg.LocalTime,"HH:mm:ss.nnnnnn")))
    msg.replaceColumn!(`Price,double(msg.Price))
	msg[`SeqNo]=int(NULL)
	msg[`DataStatus]=int(NULL)
	msg[`BizIndex]=long(NULL)
	msg[`Market]="SZ"
	msg.reorderColumns!(`ChannelNo`ApplSeqNum`MDStreamID`SecurityID`SecurityIDSource`Price`OrderQty`Side`TransactTime`OrderType`LocalTime`SeqNo`Market`DataStatus`BizIndex)
    return msg
}

def synsData(conn,dbName,tbName){
    odbc::query(conn,"select ChannelNo,ApplSeqNum,MDStreamID,SecurityID,SecurityIDSource,Price,OrderQty,Side,TransactTime,OrderType,LocalTime from data",loadTable(dbName,tbName),100000,transform)
}

submitJob("synsData","synsData",synsData,conn,dbName,tbName)
```

```
startTime                      endTime
2022.11.28 11:51:18.092        2022.11.28 11:53:20.198
```

耗时约 122 秒。

借助 DolphinDB 提供的 scheduleJob 函数，可以实现增量同步。

示例如下，每天 00:05 同步前一天的数据。

```
def synchronize(){
	login(`admin,`123456)
    conn =odbc::connect("Driver={SQLServer};Servername=sqlserver;Uid=sa;Pwd=DolphinDB;database=historyData;;")
    sqlStatement = "select ChannelNo,ApplSeqNum,MDStreamID,SecurityID,SecurityIDSource,Price,OrderQty,Side,TransactTime,OrderType,LocalTime from data where TradeDate ='" + string(date(now())-1) + "';"
    odbc::query(conn,sqlStatement,loadTable("dfs://TSDB_Entrust",`entrust),100000,transform)
}
scheduleJob(jobId=`test, jobDesc="test",jobFunc=synchronize,scheduleTime=00:05m,startDate=2022.11.11, endDate=2023.01.01, frequency='D')
```

**注意**：为防止节点重启时定时任务解析失败，预先在配置文件里添加 `preloadModules=plugins::odbc`

### 通过 DataX 驱动迁移

#### 部署 DataX

从 [DataX 下载地址](https://datax-opensource.oss-cn-hangzhou.aliyuncs.com/202210/datax.tar.gz) 下载 DataX 压缩包后，解压至自定义目录。

#### 部署 DataX-DolphinDBWriter 插件

将 [Github 链接](https://github.com/dolphindb/datax-writer) 中源码的 ./dist/dolphindbwriter 目录下所有内容拷贝到 DataX/plugin/writer 目录下，即可使用。

#### 执行 DataX 任务

配置文件 synchronization.json 置于 data/job 目录下：

```
{
    "core": {
        "transport": {
            "channel": {
                "speed": {
                    "byte": 5242880
                }
            }
        }
    },
    "job": {
        "setting": {
            "speed": {
                "byte":10485760
            }
        },
        "content": [
            {
                "reader": {
                    "name": "sqlserverreader",
                    "parameter": {
                        "username": "sa",
                        "password": "DolphinDB123",
                        "column": [
                            "ChannelNo","ApplSeqNum","MDStreamID","SecurityID","SecurityIDSource","Price","OrderQty","Side","TransactTime","OrderType","LocalTime"
                        ],
                        "connection": [
                            {
                                "table": [
                                    "data"
                                ],
                                "jdbcUrl": [
                                    "jdbc:sqlserver://127.0.0.1:1433;databasename=historyData"
                                ]
                            }
                        ]
                    }
                },
                "writer": {
                    "name": "dolphindbwriter",
                    "parameter": {
                        "userId": "admin",
                        "pwd": "123456",
                        "host": "127.0.0.1",
                        "port": 8888,
                        "dbPath": "dfs://TSDB_Entrust",
                        "tableName": "entrust",
                        "batchSize": 100000,
                        "saveFunctionDef": "def customTableInsert(dbName, tbName, mutable data) {data.replaceColumn!(`LocalTime,time(temporalParse(data.LocalTime,\"HH:mm:ss.nnnnnn\")));data.replaceColumn!(`Price,double(data.Price));data[`SeqNo]=int(NULL);data[`DataStatus]=int(NULL);data[`BizIndex]=long(NULL);data[`Market]=`SZ;data.reorderColumns!(`ChannelNo`ApplSeqNum`MDStreamID`SecurityID`SecurityIDSource`Price`OrderQty`Side`TransactTime`OrderType`LocalTime`SeqNo`Market`DataStatus`BizIndex);pt = loadTable(dbName,tbName);pt.append!(data)}",
                        "saveFunctionName" : "customTableInsert",
                        "table": [
                            {
                                "type": "DT_INT",
                                "name": "ChannelNo"
                            },
                            {
                                "type": "DT_LONG",
                                "name": "ApplSeqNum"
                            },
                            {
                                "type": "DT_INT",
                                "name": "MDStreamID"
                            },
                            {
                                "type": "DT_SYMBOL",
                                "name": "SecurityID"
                            },
                            {
                                "type": "DT_INT",
                                "name": "SecurityIDSource"
                            },
                            {
                                "type": "DT_DOUBLE",
                                "name": "Price"
                            },
                            {
                                "type": "DT_INT",
                                "name": "OrderQty"
                            },
                            {
                                "type": "DT_SYMBOL",
                                "name": "Side"
                            },
                            {
                                "type": "DT_TIMESTAMP",
                                "name": "TransactTime"
                            },
                            {
                                "type": "DT_SYMBOL",
                                "name": "OrderType"
                            },
                            {
                                "type": "DT_STRING",
                                "name": "LocalTime"
                            }
                        ]

                    }
                }
            }
        ]
    }
}
```

1. Linux 终端中执行以下命令执行 DataX 任务

```
cd ./DataX/bin/
python DataX.py ../job/synchronization.json
```

```
任务启动时刻                    : 2022-11-28 17:58:52
任务结束时刻                    : 2022-11-28 18:02:24
任务总计耗时                    :                212s
任务平均流量                    :            3.62MB/s
记录写入速度                    :          78779rec/s
读出记录总数                    :            16622527
读写失败总数                    :                   0
```

同样的，若需要增量同步，可在 synchronization.json 中的 "reader" 增加 "where" 条件，增加对交易日期的过滤，每次执行同步任务时只同步 where 条件中过滤的数据，例如这些数据可以是前一天的数据。

以下例子仅供参考：

```
"reader": {
                    "name": "sqlserverreader",
                    "parameter": {
                        "username": "sa",
                        "password": "DolphinDB123",
                        "column": [
                            "ChannelNo","ApplSeqNum","MDStreamID","SecurityID","SecurityIDSource","Price","OrderQty","Side","TransactTime","OrderType","LocalTime"
                        ],
                        "connection": [
                            {
                                "table": [
                                    "data"
                                ],
                                "jdbcUrl": [
                                    "jdbc:sqlserver://127.0.0.1:1433;databasename=historyData"
                                ]
                            }
                        ]
                        "where":"TradeDate=(select CONVERT ( varchar ( 12) , dateadd(d,-1,getdate()), 102))"
                    }
                }
```

## 性能比较

本案例中使用的软件版本为：

* DolphinDB: DolphinDB\_Linux64\_V2.00.8.6
* SQL Server: Microsoft SQL Server 2017 (RTM-CU31) (KB5016884) - 14.0.3456.2 (X64)

分别使用 ODBC 插件和 DataX 驱动进行数据迁移的耗时对比如下表所示：

| **ODBC 插件** | **DataX** |
| 122s | 212s |

由此可见，ODBC 插件的性能优于 DataX。当数据量增大，尤其时表的数量增多时，ODBC 插件的速度优势更为明显。而且即使不需要对同步数据进行处理，DataX 也需要对每一个表配置一个 json，而 ODBC 则只需要更改表名即可，实现难度明显低于 DataX。

| **迁移方法** | **适用场景** | **实现难度** |
| ODBC 插件 | 全量同步，增量同步 | 可完全在 DolphinDB 端实现 |
| DataX | 全量同步，增量同步 | 需要部署 DataX 并编写 json |
