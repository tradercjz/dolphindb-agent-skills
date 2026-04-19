<!-- Auto-mirrored from upstream `documentation-main/plugins/hbase/hbase.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# HBase

本插件通过 Thrift 接口连接到 HBase，并读取数据。推荐版本：HBase 版本为 1.2.0，Thrift 版本为 0.14.0。

## 在插件市场安装

### 版本要求

* Linux x64 要求 DolphinDB Server 2.00.10 及更高版本。
* Linux ARM 要求 DolphinDB Server 200.14.2/300.2.2 及更高版本。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("hbase")
   ```

   返回：<path\_to\_HBase\_plugintxt>/pluginHBase.txt
3. 使用 `loadPlugin` 命令加载插件（即上一步返回的.txt 文件）。

   ```
   loadPlugin("hbase")
   ```

### 开启 Thrift server

通过以下命令开启 Thrift server，并指定端口 9090：

```
$HBASE_HOME/bin/hbase-daenom.sh start thrift -p 9090
```

通过以下命令关闭 Thrift：

```
$HBASE_HOME/bin/hbase-daemon.sh stop thrift
```

## 用户接口

### hbase::connect

**语法**

```
connect(host, port, [isFramed=false], [timeout=5000])
```

**参数**

* host：要连接的 Thrift server 的 IP 地址，类型为 STRING。
* port：要连接 Thrift server 的端口号，类型为 INT。
* isFramed：可选，布尔值，默认为 false，表示通过 TBufferedTransport 进行传输。若设置为 true，则表示通过 TFramedTransport 进行传输。
* timeout：可选，表示建立连接（ConnTimeout）与接收回复（RecvTimeout）的最长等待时间，单位为毫秒，默认为 5000ms，类型为 INT。

**详情**

通过 Thrift server 与 HBase 建立一个连接，返回一个 HBase 连接的句柄。

**例子**

```
conn = hbase::connect("192.168.1.114", 9090)
```

**注意** ：如果该连接长时间（默认为 1min）没有操作，HBase 会自动关闭这个连接。此时再通过该连接进行后续操作时，会报 `No more data to read` 的错误，需要执行 `hbase::connect` 重新进行连接。通过 HBase 的配置文件（*conf/hbase-site.xml*）可修改超时时间。若添加如下配置，则表示一天没有操作时将自动关闭连接：

修改 `hbase.thrift.server.socket.read.timeout` 和 `hbase.thrift.connection.max-idletime`

```
<property>
         <name>hbase.thrift.server.socket.read.timeout</name>
         <value>86400000</value>
         <description>eg:milisecond</description>
</property>
```

```
<property>
         <name>hbase.thrift.connection.max-idletime</name>
         <value>86400000</value>
</property>
```

### hbase::showTables

**语法**

```
hbase::showTables(conn)
```

**参数**

* conn：通过 hbase::connect 获得的 HBase 句柄。

**详情**

显示已连接的数据库中所有表的表名。

**例子**

```
conn = hbase::connect("192.168.1.114", 9090)
hbase::showTables(conn)
```

### hbase::deleteTable

**语法**

```
hbase::deleteTable(conn, tableNames)
```

**参数**

* conn：通过 hbase::connect 获得的 HBase 句柄。
* tableNames：要删除的表的名字，类型为 STRING 或者 STRING vector。

**详情**

删除数据库中存在的表。

**例子**

```
conn = hbase::connect("192.168.1.114", 9090)
hbase::deleteTable(conn, "demo_table")
```

### hbase::getRow

**语法**

```
hbase::getRow(conn, tableName, rowKey, [columnNames])
```

**参数**

* conn：通过 hbase::connect 获得的 HBase 句柄。
* tableName：需要读取数据的表的名字，类型为 STRING
* rowKey：需要读取的 row 的索引，类型为 STRING。
* columnNames：可选，表示需要获取的列名，若不指定默认读取所有列数据，类型为 STRING 或者 STRING vector。

**详情**

读取 rowKey 所对应的数据。

**例子**

```
conn = hbase::connect("192.168.1.114", 9090)
hbase::getRow(conn, "test", "row1")
```

### hbase::load

**语法**

```
hbase::load(conn, tableName, [schema])
```

**参数**

* conn：通过 hbase::connect 获得的 HBase 句柄。
* tableName：需要读取数据的表的名字，类型为 STRING。
* schema：可选，表示包含列名和列的数据类型的表。由于 HBase 中数据以字节形式存储，没有指定数据类型。若不指定 schema，插件会尝试以第一行数据为基准进行建表，返回的 DolphinDB 表中每列数据类型都为 STRING。请注意，需要保证表中每行数据具有相同的列数，否则会出错。指定 schema 则可以指定每列的数据类型。此时，schema 中的列名需要与 HBase 中所要读取的列名完全一致。

**详情**

将 HBase 的查询结果导入 DolphinDB 中的内存表。schema 中支持的数据格式见**支持的数据格式**章节。

**例子**

```
conn = hbase::connect("192.168.1.114", 9090)
t =  table(["cf:a","cf:b", "cf:c", "cf:time"] as name, ["STRING", "INT", "FLOAT", "TIMESTAMP"] as type)
t1 = hbase::load(conn, "test", t)
```

## 支持的数据格式

schema 中支持的数据类型如下表所示。HBase 中存储的数据格式需要与下表相同，才能将 HBase 中的数据转成 DolphinDB 中对应数据类型，否则无法转换，且会返回空值。

| Type | HBase 数据 | DolphinDB 数据 |
| --- | --- | --- |
| BOOL | true, 1, FALSE | true, true, false |
| CHAR | a | a |
| SHORT | 1 | 1 |
| INT | 21 | 21 |
| LONG | 112 | 112 |
| FLOAT | 1.2 | 1.2 |
| DOUBLE | 3.5 | 3.5 |
| SYMBOL | s0 | "s0" |
| STRING | name | "name" |
| DATE | 20210102, 2021.01.02 | 2021.01.02, 2021.01.02 |
| MONTH | 201206, 2012.12 | 2012.06M, 2021.12M |
| TIME | 052013140, 05:20:01.999 | 05:20:13.140, 05:20:01.999 |
| MINUTE | 1230, 13:30 | 12:30m, 13:30m |
| SECOND | 123010, 13:30:10 | 12:30:10, 13:30:10 |
| DATETIME | 20120613133010, 2012.06.13 13:30:10, 2012.06.13T13:30:10 | 2012.06.13T13:30:10, 2012.06.13T13:30:10, 2012.06.13T13:30:10 |
| TIMESTAMP | 20210218051701000, 2012.06.13 13:30:10.008, 2012.06.13T13:30:10.008 | 2021.02.18T05:17:01.000, 2012.06.13T13:30:10.008, 2012.06.13T13:30:10.008 |
| NANOTIME | 133010008007006, 13:30:10.008007006 | 13:30:10.008007006, 13:30:10.008007006 |
| NANOTIMESTAMP | 20120613133010008007006, 2012.06.13 13:30:10.008007006, 2012.06.13T13:30:10.008007006 | 2012.06.13T13:30:10.008007006, 2012.06.13T13:30:10.008007006, 2012.06.13T13:30:10.008007006 |
