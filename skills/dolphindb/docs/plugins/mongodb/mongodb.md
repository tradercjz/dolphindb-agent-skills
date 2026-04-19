<!-- Auto-mirrored from upstream `documentation-main/plugins/mongodb/mongodb.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# MongoDB

MongoDB 是一个基于分布式文件存储的数据库。DolphinDB 的 MongoDB 插件可以建立与 MongoDB 服务器的连接，导出 MongoDB 数据库中的数据到 DolphinDB 的内存表中。mongodb 插件基于 mongodb-c-driver 开发。

## 在插件市场安装插件

### 版本要求

DolphinDB Server: 2.00.10及更高版本。支持 Linux x86，Linux JIT，Windows，Window JIT。

### 安装步骤

1. 在DolphinDB 客户端中使用 listRemotePlugins 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 installPlugin 命令完成插件安装。

   ```
   installPlugin("mongodb")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("mongodb")
   ```

## 接口说明

### mongodb::connect

**语法**

```
mongodb::connect(host, port, user, password, [db])
```

**详情**

与 MongoDB 服务器建立一个连接。返回一个 MongoDB 连接的句柄，用于load。

**参数**

**host** STRING 类型标量，表示 MongoDB 服务器的地址。

**port** INT 类型标量，表示 MongoDB 服务器的端口。

**user** STRING 类型标量，表示 MongoDB 服务器的用户名。如果没有开启 MongoDB 用户权限认证，则填写空字符串""。

**password** STRING 类型标量，表示 MongoDB 服务器的密码。如果没有开启 MongoDB 用户权限认证，则填写空字符串""。

**db** STRING 类型标量，表示验证登录用户的数据库。在 MongoDB 中存储对应登录用户的数据库。如果不填写，将以参数 `host =` 指定的 MongoDB 服务器的 `admin` 数据库进行登录用户验证。

**例子**

```
conn = mongodb::connect(`localhost, 27017, `root, `root, `DolphinDB)
conn2 = mongodb::connect(`localhost, 27017, `root, `root)
```

### mongodb::load

**语法**

```
mongodb::load(conn, collcetionName, query, findOptions, [schema])
```

**详情**

将 MongoDB 的查询结果导入 DolphinDB 中的内存表。支持的数据类型以及数据转化规则参见用户手册`数据类型`章节。

**参数**

**conn** 通过 `mongodb::connect` 获得的 MongoDB 连接句柄。

**collcetionName** 一个 MongoDB 中集合的名字。有两种参数模式( *collectionName* 和 *databaseName:collectionName* )，第一种会查询在调用 `mongodb::connect` 时指定的数据库 *db* 中的 collection，第二种是查询指定数据库中的 collection。

**query** MongoDB 查询条件，JSON 字符串，例如：{ "aa" : { "gt" : {"$date":"2019-02-28T00:00:00.000Z" }} }。

**findOptions** MongoDB 查询选项，JSON 字符串，例如：{"limit":123}对查询结果在MongoDB中进行预处理再返回。详见 MongoDB 官方文档.

**schema** 包含列名及其数据类型的表。如果我们想要改变由系统自动决定的列的数据类型，需要在schema表中修改数据类型，并且把它作为load函数的一个参数。

**例子**

```
conn = mongodb::connect(`localhost, 27017, `root, `root, `DolphinDB)
query='{ "datetime" : { "$gt" : {"$date":"2019-02-28T00:00:00.000Z" }} }'
findOptions='{"limit":1234}'
tb=mongodb::load(conn, `US,query,findOptions)
select count(*) from tb
tb2 = mongodb::load(conn, 'dolphindb:US',query,findOptions)
select count(*) from tb
schema=table(`item`type`qty as name,`STRING`STRING`INT as type)
tb2 = mongodb::load(conn, 'dolphindb:US',query,findOptions,schema)
```

### mongodb::aggregate

**语法**

```
mongodb::aggregate(conn, collectionName, pipeline, aggregateOptions, [schema])
```

**详情**

将 MongoDB 的（聚合）查询结果导入 DolphinDB 中的内存表。支持的数据类型以及数据转化规则参见用户手册`数据类型`章节。

**参数**

**conn** 通过 `mongodb::connect`获得的 MongoDB 连接句柄。

**collcetionName** 一个 MongoDB 中集合的名字。有两种参数模式( *collectionName* 和 *databaseName:collectionName* )，第一种会查询在调用 `mongodb::connect` 时指定的数据库 *db* 中的 collection，第二种是查询指定数据库中的collection。

**pipeline** MongoDB 聚合管道，JSON 字符串，例如：{by\_user", num\_tutorial : {$sum : 1}}}。

**aggregateOptions** MongoDB 查询选项，JSON 字符串，例如：`{"maxTimeMS": 10000}'`对查询结果在MongoDB中进行预处理再返回。详见 MongoDB 官方文档.

**schema** 包含列名及其数据类型的表。如果我们想要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为 `aggregate` 函数的一个参数。

**例子**

```
conn = mongodb::connect(`localhost, 27017, "", "", `DolphinDB)
pipeline = "{ \"pipeline\" : [ { \"$project\" : { \"str\" : \"$obj1.str\" } } ] }"
aggregateOptions="{}"
mongodb::aggregate(conn, "test1:collnetion1",pipeline,aggregateOptions)
```

### mongodb::close

**语法**

```
mongodb::close(conn)
```

**详情**

关闭一个MongoDB连接句柄。

**参数**

**conn** 通过 `mongodb::connect` 获得的 MongoDB 连接句柄。

**例子**

```
conn = mongodb::connect(`localhost, 27017, `root, `root, `DolphinDB)
query=`{ "datetime" : { "$gt" : {"$date":"2019-02-28T00:00:00.000Z" }} }
findOptions=`{"limit":1234}
tb = mongodb::load(conn, `US,query,findOptions)
select count(*) from tb
mongodb::close(conn)
```

### mongodb::parseJson

**语法**

```
mongodb::parseJson(jsonStrings, keys, colNames, colTypes)
```

**详情**

解析 JSON 类型的数据，转换到 DolphinDB 的内存表并返回该内存表。

**参数**

**jsonStrings** 需要解析的 JSON 格式的字符串，字符串向量。

**keys** 结果表 JSON 的键，字符串向量。

**colNames** 转换后内存表的列名，一一对应原 JSON 中的键，字符串向量。

**colTypes** 向量，表示结果表中的数据类型。

colTypes支持BOOL, INT, FLOAT, DOUBLE, STRING以及BOOL[], INT[], FLOAT[], DOUBLE[]类型的array vector。其中支持将JSON中的int, float, double类型转换为DolphinDB INT, FLOAT, DOUBLE类型中的任意一种。

**例子**

```
data = ['{"a": 1, "b": 2}', '{"a": 2, "b": 3}']
 mongodb::parseJson(data,
`a`b,
`col1`col2,
[INT, INT] )
```

### mongodb::getCollections

**语法**

```
mongodb::getCollections(conn, [databaseName])
```

**详情**

获取指定数据库的所有集合的名字。

**参数**

**conn** 通过 `mongodb::connect` 获得的 MongoDB 连接句柄。

**databaseName** 需要查询的数据库。如果不填，则为 `mongodb::connect` 所选的数据库。

**例子**

```
conn = mongodb::connect("192.168.1.38", 27017, "", "")
mongodb::getCollections(conn, "dolphindb")
```

## 查询数据示例

```
query='{"dt": { "$date" : "2016-06-22T00:00:00.000Z" } }';
query='{"bcol" : false }';
query='{"open" : { "$numberInt" : "13232" } }';
query='{"vol" : { "$numberLong" : "1242434"} }';
query=' {"close" : { "$numberDouble" : "1.2199999999999999734" }';
query='{"low" : { "$gt" : { "$numberDecimal" : "0.219711" } } }';
query='{"uid" : { "$oid" : "1232430aa00000000000be0a" } }';
query=' {"sid" : { "$symbol" : "fdf" } }';
query='{"symbol" : "XRPUSDT.BNC"}';
query='{"ts" : { "$date" : { "$numberLong" : "1600166651000" } }';
query='{}';
findOptions='{}';
con=mongodb::connect(`localhost,27017,`admin,`123456,`dolphindb);
res=mongodb::load(con,`collection1,query,findOptions);
mongodb::close(con);
t = select * from res
```

## 支持的数据类型

### 整型

| MongoDB类型 | 对应的DolphinDB类型 |
| --- | --- |
| int32 | INT |
| int64(long) | LONG |
| bool | BOOL |

DolphinDB中各类整型的最小值（例如：INT的-2,147,483,648以及LONG的-9,223,372,036,854,775,808）为NULL值。

### 浮点数类型

| MongoDB类型 | 对应的DolphinDB类型 |
| --- | --- |
| double | DOUBLE |
| decimal128 | DOUBLE |

### 时间类型

| MongoDB类型 | 对应的DolphinDB类型 |
| --- | --- |
| date | timestamp |

### 字符串类型

| MongoDB类型 | 对应的DolphinDB类型 |
| --- | --- |
| string | STRING |
| symbol | STRING |
| oid | STRING |
