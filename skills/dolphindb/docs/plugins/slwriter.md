<!-- Auto-mirrored from upstream `documentation-main/plugins/slwriter.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SchemalessWriter

在物联网场景中，日志型数据是一种常见的数据类型。它的特点是不同的数据可能包含不同的字段，因此在存储日志型数据时，需要根据数据的结构动态创建数据表，而不能事先确定数据表的结构再存储数据。为了应对这种数据存储需求，DolphinDB 开发了 SchemalessWriter 插件，通过 userDefinedAppend 函数将 InfluxDB Line protocol、海康 json 格式、海康 key/value 格式的数据写入 DolphinDB 的分布式数据表。其中，对于 InfluxDB Line protocol 格式数据，无需事先确定数据表结构，userDefinedAppend 在写入时会自动创建表结构；而对于海康 json 格式、海康 key/value 格式的数据，则需要事先确定表结构。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本。目前仅支持 Linux 的 X86-64 位版本。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("SchemalessWriter")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("SchemalessWriter")
   ```

## 接口说明

### userDefinedAppend

**语法**

```
userDefinedAppend(protocol, data, [userDefinedArg1], [userDefinedArg2])
```

**详情**

将 protocol 格式数据 data 写入 DolphinDB 的分布式表中。其中，当 protocol=“INFLUXDB” 时，无需预先创建表结构，`userDefinedAppend` 将在写入时自动创建表结构；当 protocol=”HKJSON” 或 ”HKLINE” 时，需要用户预先创建一个列数比 data 包含的字段更多的表，`userDefinedAppend` 会将 data 写入该表对应的列字段中，若 data 中不包含某个（些）列字段，则这个（些）列字段置空。

**参数**

**protocol** STRING 类型标量，表示协议类型。可以取值为 “INFLUXDB”, ”HKJSON”, ”HKLINE”。

**data** STRING 类型标量，表示对应协议的数据。*data* 将被写入到自动创建或预先创建的库表中。

**userDefinedArg1** STRING 类型标量，表示数据库名称。protocol 为 “INFLUXDB” 时不需要指定该参数，否则必须指定该参数。

**userDefinedArg2** STRING 类型标量，表示分布式表名称。protocol 为 “INFLUXDB” 时不需要指定该参数，否则必须指定该参数。

下面根据 *protocol* 的取值分情况讨论：

* InfluxDB Line protocol，即指定 protocol 为 "INFLUXDB"。此时，data 为一行或多行 [InfluxDB Line protocol](https://docs.influxdata.com/influxdb/cloud/reference/syntax/line-protocol/) 格式数据。写入数据时，插件会创建一个包含 timestamp，location，group，metric Name，metricValue 列的数据表。如果一个 InfluxDB 的数据字符串包含多个测点的数据，则会写入多行数据。

**示例**

```
userDefinedAppend("INFLUXDB", "measurement1,location=cn,group=system field1=123,field2=456 1680130350899000000")
```

以上代码创建一个以 measurement1 为库名和表名，包含以下列：timestamp（NANOTIMESTAMP 类型）、location（tag 名称 ）、group（tag 名称）、metricName（field 名称） 和 metricValue（filed 值） 为列名的库表 。 同时写入了两条数据：

| timestamp | location | group | metricName | metricValue |
| --- | --- | --- | --- | --- |
| 1680130350899000000 | cn | system | field1 | 123 |
| 1680130350899000000 | cn | system | field2 | 456 |

* 海康 json 格式，即指定 *protocol* 为 "HKJSON"。此时，*data* 为 海康 json 数据格式的数据（字符串类型）。在写入该格式数据时，插件不会自动创建数据库和表。因此，在使用写入数据前，需要事先创建数据库及表，并通过 *userDefinedArg1* 指定库名 (不带 "dfs://")，通过 *userDefinedArg2* 指定表名。

**示例**

建库建表:

```
db = database("dfs://test_hkjson", VALUE, 1..3)
dummy = table(array(INT,0) as a, array(INT,0) as b, array(INT,0) as c , array(INT,0) as d)
db.createPartitionedTable(dummy,"test",[`a])
```

调用 `userDefinedAppend` 写入数据

```
lines = "{\"a\":1,\"b\":2,\"Values\":[{\"c\":3,\"d\":4},{\"c\":5,\"d\":6}]}"
userDefinedAppend("HKJSON",lines, "test_hkjson", "test")
```

* 海康 key/value line 格式，即指定 *protocol* 为 "HKLINE"。此时，*data* 为 海康 key/value line 数据格式的数据（字符串类型）。在写入该格式数据时，插件不会自动创建数据库和表。因此，在使用写入数据前，需要事先创建数据库及表，并通过 *userDefinedArg1* 指定库名 (不带 "dfs://")，通过 *userDefinedArg2* 指定表名。

**示例**

建库建表

```
if (existsDatabase("dfs://test_hkline")){ dropDatabase("dfs://test_hkline")}
db = database("dfs://test_hkline", HASH, [STRING,3])
dummy = table(array(STRING, 0) as "__name__",
array(STRING, 0) as path,
array(INT, 0) as count,
array(DOUBLE, 0) as temp,
array(STRING, 0) as method ,
array(STRING, 0) as instance)
db.createPartitionedTable(dummy,"test_line",["__name__"])
```

调用 `userDefinedAppend` 写入数据

```
hklines = array(STRING,0)
hklines.append!("{__name__=\"requests_total\", path=\"/status\", method=\"GET\", instance=\"10.0.0.1:80\"}")
hklines.append!("{__name__=\"requests_total\",path=\"/status\",method=\"POST\",instance=\"10.0.0.1:80\"}")
hklines.append!("{__name__=\"requests_total\",path=\"/status\",count=1,temp=1.2,method=\"POST\",instance=\"10.0.0.1:80\"}")
i = 0
for (hkline in hklines){
    print("i:",i)
    SchemalessWriter::HKLineWriter(hkline, "test_line", "test_line")
    i += 1
}
```

### configWriter

**语法**

```
SchemalessWriter::configWriter(config)
```

**详情**

配置建库的参数，分区的规则在写数据的接口中配置。

**参数**

**config** 一个字典，key 和 value 都是 STRING 类型标量。key 和 value 的取值如下：

| **key 的取值** | **含义** | **value 取值** |
| --- | --- | --- |
| "dbEngineType" | 表示数据库引擎的类型。 | 可以是 "OLAP" 或者 "TSDB"，默认为 “OLAP”。 |
| "dbNamePreStr" | 表示无模式写入所创建的数据库的库名前缀。用于区分系统中其他场景下创建的库。 | 自定义的字符串 |

**使用示例**

```
cfg = dict(["dbEngineType"],["OLAP"])
SchemalessWriter::configWriter(cfg)
```
