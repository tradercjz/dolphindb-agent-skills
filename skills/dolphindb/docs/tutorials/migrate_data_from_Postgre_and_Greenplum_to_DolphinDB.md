<!-- Auto-mirrored from upstream `documentation-main/tutorials/migrate_data_from_Postgre_and_Greenplum_to_DolphinDB.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 这里的/datax/plugin/writer/应修改为实际目录
find /datax/plugin/reader/ -type f -name "._*er" | xargs rm -rf
find /datax/plugin/writer/ -type f -name "._*er" | xargs rm -rf
```

自检成功后，将 [DataX-DolphinDBWriter](https://github.com/dolphindb/datax-writer)中源码的 `./dist/dolphindbwriter` 目录下所有内容拷贝到 `DataX/plugin/writer` 目录下，即可使用。

#### **执行 DataX 任务**

**step1：配置 json 文件**

配置文件 *pgddb.json* 的具体内容如下，并将 json 文件置于自定义目录下，本教程中放置于 `datax/job` 目录下。

```
{
    "job": {
            "content": [{
                    "writer": {
                            "name": "dolphindbwriter",
                            "parameter": {
                                    "userId": "admin",
                                    "pwd": "123456",
                                    "host": "10.0.0.80",
                                    "port": 8848,
                                    "dbPath": "dfs://TSDB_tick",
                                    "tableName": "Tick",
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
                                    ]
                            }
                    },
                    "reader": {
                            "name": "postgresqlreader",
                            "parameter": {
                                    "username": "postgres",
                                    "column": ["SecurityID", "TradeTime", "TradePrice", "TradeQty", "TradeAmount", "BuyNo", "SellNo", "ChannelNo", "TradeIndex", "TradeBSFlag", "BizIndex"],
                                    "connection": [{
                                            "table": ["ticksh"],
                                            "jdbcUrl": ["jdbc:postgresql:postgres"]
                                    }],
                                    "password": "postgres",
                                    "where": ""
                            }
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

**step2：Linux 终端中执行以下命令以执行 DataX 任务**

```
cd ./datax
python bin/datax.py --jvm=-Xmx8g job/ddbtopg.json
```

**step3：查看 DataX 同步结果**

```
任务启动时刻                    : 2023-08-29 14:19:53
任务结束时刻                    : 2023-08-29 14:26:33
任务总计耗时                    :                400s
任务平均流量                    :            4.08MB/s
记录写入速度                    :          68029rec/s
读出记录总数                    :            27211975
读写失败总数                    :                   0
```

## 基准性能

分别使用 ODBC 插件和 DataX 驱动进行数据迁移， 数据量 2721 万条，迁移耗时对比如下表所示：

| **ODBC 插件** | **DataX** |
| --- | --- |
| 597.54s | 400s |

综上，ODBC 插件与 DataX 均能实现将 PostgreSql 中数据迁移到 DolphinDB 中，但是各有优缺点：

* ODBC 使用简单，适合定制数据的导入，但是运维管理不便。
* DataX 导入数据需要编写复杂的导入配置，但是其扩展灵活，适合批量导入，方便监控，社区支持丰富。

用户可以根据自己数据量的大小以及工程化的便捷性选择合适的导入方式。
