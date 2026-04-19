<!-- Auto-mirrored from upstream `documentation-main/tools/datax_reader.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 基于 DataX 的 DolphinDB 数据读取工具

## DataX 离线数据同步

DataX 是在阿里巴巴集团内被广泛使用的离线数据同步工具/平台，实现包括 MySQL、Oracle、SqlServer、Postgre、HDFS、Hive、ADS、HBase、TableStore(OTS)、MaxCompute(ODPS)、DRDS 等各种异构数据源之间高效的数据同步功能，详情可查看 [DataX 已支持的数据源](https://github.com/alibaba/DataX/blob/master/README.md#support-data-channels)。

DataX 是可扩展的数据同步框架，将不同数据源的同步抽象为从源头数据源读取数据的 Reader 插件，以及向目标端写入数据的 Writer 插件。理论上 DataX 框架可以支持任意数据源类型的数据同步工作。每接入一套新数据源该新加入的数据源即可实现和现有的数据源互通。

### DataX 插件：DolphinDBReader

基于 DataX 的扩展功能，DolphinDBReader 插件实现了从 DolphinDB 读出数据。使用 DataX 官方s现有的 writer 插件结合 DolphinDBReader 插件，即可满足从 DolphinDB 向不同数据源同步数据。

DolphinDBReader 底层依赖 DolphinDB Java API，采用批量读出的方式将分布式数据库的数据读出。

注意：如果一次性读出的 DolphinDB 源表过大，会造成插件 OOM 报错，建议使用读出数据量在 200 万以下的表。

## 使用方法

详细信息请参阅 [DataX 指南](https://github.com/alibaba/DataX/blob/master/userGuid.md)，以下仅列出必要步骤。注意，dataX 的启动脚本基于 python2 开发，所以需要使用 python2 来执行 datax.py。

### 下载部署 DataX

[DataX 指南](https://github.com/alibaba/DataX/blob/master/userGuid.md)提供了两种部署方式，建议选择方式一，即直接下载 DataX 工具包进行部署。

### 部署 DolphinDBReader 插件

将源码的 `./dolphindbreader` 目录及下所有内容拷贝到 `datax/plugin/reader` 目录下，即可使用。

### 执行 DataX 任务

进入 `datax/bin` 目录下，用 python2 执行 `datax.py` 脚本，并指定配置文件地址，示例如下：

```
cd /root/datax/bin/
python2 datax.py /root/datax/myconf/BASECODE.json
```

### 2导出实例

使用 DataX 的绝大部分工作都是通过配置来完成，包括双边的数据库连接信息和需要同步的数据表结构信息等。

#### 示例：全量导入

下面以从 DolphinDB 向 Oracle 导入一张表 BASECODE 进行示例。

首先在导入前，需要在 Oracle 中预先创建好目标数据库和表；然后使用 DolphinDBReader 从 DolphinDB 读取 BASECODE 源表全量数据；再使用 oraclewriter 将读取到的 BASECODE 数据写入 Oracle 对应的目标表中。

编写配置文件 BASECODE.json，并存放到指定目录，比如 `/root/datax/myconf` 目录下，配置文件说明请参考附录一。

配置完成后，在 `datax/bin` 目录下执行如下脚本即可启动数据同步任务。

```
cd /root/datax/bin/
python2 datax.py /root/datax/myconf/BASECODE.json
```

## 附录

### 附录一：配置文件示例

BASECODE.json

```
{
    "job": {
        "setting": {
            "speed": {
                 "channel": 1
            },
            "errorLimit": {
                "record": 0,
                "percentage": 0.02
            }
        },
        "content": [
            {
                "reader": {
                    "name": "dolphindbreader",
                    "parameter": {
                        "userId": "admin",
                        "pwd": "123456",
                        "host": "47.99.175.197",
                        "port": 8848,
						"dbPath": "",
						"tableName": "stream5",
						"where": "",
						"table": [{
								"name": "bool"
							},
							{
								"name": "short"
							}
						]
                    }
                },
               "writer": {
                    "name": "oraclewriter",
                    "parameter": {
                        "username": "system",
                        "password": "DolphinDB123",
                        "column":["*"],
                        "connection":[
                            {
                            "jdbcUrl":"jdbc:oracle:thin:@192.168.0.9:1521/orcl",
                            "table":[
                                "wide_table"
                                ]
                            }
                        ]
                    }
                }
            }
        ]
    }
}
```

#### 配置文件参数说明

（仅介绍 DolphinDBReader 的参数，writer 参数根据写入目标数据库的不同而不同，详情参阅：[datax指南](https://github.com/alibaba/DataX/blob/master/userGuid.md) ）

* host
  + 描述：Server Host。
  + 必选：是。
  + 默认值：无。
* port
  + 描述：Server Port。
  + 必选：是。
  + 默认值：无。
* userId
  + 描述：DolphinDB 用户名。导出分布式库时，必须要有权限的用户才能操作，否则会返回。
  + 必选：是。
  + 默认值：无。
* pwd
  + 描述：DolphinDB 用户密码。
  + 必选：是。
  + 默认值：无。
* dbPath
  + 描述：需要读出的目标分布式库名称，比如 `dfs://MYDB`。
  + 必选：是。
  + 默认值：无
* tableName
  + 描述: 读出数据表名称。
  + 必选: 是。
  + 默认值: 无。
* where
  + 描述: 可以通过指定 where 来设置条件，比如 "id >10 and name = `dolphindb"。
  + 必选: 是。
  + 默认值: 无。
* table
  + 描述：读出表的字段集合。内部结构为：`{"name": "columnName"}`。请注意此处列定义的顺序，需要与原表提取的列顺序完全一致。
  + 必选: 是。
  + 默认值: 无。
* name：
  + 描述：字段名称。
  + 必选: 是。
  + 默认值: 无。
* querySql:
  + 描述：在部分业务场景下，若配置项参数 where 无法描述筛选条件，用户可使用 querySql 以实现 SQL 自定义筛选。 注意，若用户配置了 querySql，则插件 DolphinDBReader 将忽略配置项参数 table, where 的筛选条件，即 querySql 的优先级大于table, where。
  + 必选：否。
  + 默认值：无。
  + 使用示例：

  ```
  {
    "job": {
        "setting": {
            "speed": {
                 "channel": 1
            },
            "errorLimit": {
                "record": 0,
                "percentage": 0.02
            }
        },
        "content": [
            {
                "reader": {
                    "name": "dolphindbreader",
                    "parameter": {
                        "userId": "admin",
                        "pwd": "123456",
                        "host": "192.168.1.167",
                        "port": 18921,
  						"dbPath": "dfs://test_allDateType3",
  						"tableName": "pt1",
                        "querySql": "select col1,col2,col3,col4,col5 ,col15,col16 as ttt from loadTable(\"dfs://test_allDateType3\",`pt1) "
                    }
                },
               "writer": {
                    "name": "oraclewriter",
                    "parameter": {
                        "username": "system",
                        "password": "DolphinDB123",
                        "column":["*"],
                        "connection":[
                            {
                            "jdbcUrl":"jdbc:oracle:thin:@192.168.0.9:1521/orcl",
                            "table":[
                                "reader_int"
                                ]
                            }
                        ]
                    }
                }
            }
        ]
    }
  }
  ```

### 附录二：数据对照表（其他数据类型暂不支持）

| DolphinDB类型 | 配置值 | DataX类型 |
| --- | --- | --- |
| DOUBLE | DT\_DOUBLE | DOUBLE |
| FLOAT | DT\_FLOAT | DOUBLE |
| BOOL | DT\_BOOL | BOOLEAN |
| DATE | DT\_DATE | DATE |
| DATETIME | DT\_DATETIME | DATE |
| TIME | DT\_TIME | STRING |
| TIMESTAMP | DT\_TIMESTAMP | DATE |
| NANOTIME | DT\_NANOTIME | STRING |
| NANOTIMETAMP | DT\_NANOTIMETAMP | DATE |
| MONTH | DT\_MONTH | DATE |
| BYTE | DT\_BYTE | LONG |
| LONG | DT\_LONG | LONG |
| SHORT | DT\_SHORT | LONG |
| INT | DT\_INT | LONG |
| UUID | DT\_UUID | STRING |
| STRING | DT\_STRING | STRING |
| BLOB | DT\_BLOB | STRING |
| SYMBOL | DT\_SYMBOL | STRING |
| COMPLEX | DT\_COMPLEX | STRING |
| DATEHOUR | DT\_DATEHOUR | DATE |
| DURATION | DT\_DURATION | LONG |
| INT128 | DT\_INT128 | STRING |
| IPADDR | DT\_IPADDR | STRING |
| MINUTE | DT\_MINUTE | STRING |
| MONTH | DT\_MONTH | STRING |
| POINT | DT\_POINT | STRING |
| SECOND | DT\_SECOND | STRING |
| DECIMAL32 | DT\_DECIMAL32 | STRING |
| DECIMAL64 | DT\_DECIMAL64 | STRING |
| DECIMAL128 | DT\_DECIMAL128 | STRING |
