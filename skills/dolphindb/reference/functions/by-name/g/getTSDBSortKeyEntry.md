# getTSDBSortKeyEntry

## 语法

`getTSDBSortKeyEntry(chunkId, [tableName])`

## 详情

获取 TSDB 引擎已经写入磁盘的每个 chunk 分区的 sort key（详见 sortColumns 参数介绍）信息。

## 参数

**chunkId** 字符串标量或向量，表示 chunk 的 ID。注意：不可超过 1024。

**tableName** 可选参数，是字符串标量，表示分布表的名称。若不指定该参数，则表示该 chunk 下所包含的所有表。

## 返回值

返回一个表，包含以下字段：

* chunkId：chunk 的唯一标识。
* chunkPath：chunk 数据所存储的路径。
* tableName：分布式表表名。
* file：level file 文件名。
* key：sort key 的组合值。sort key 之间以下划线 “\_” 分隔。
* size：当前 sort key 组合值对应的记录数。

注：

该函数不支持查询 Cache Engine 中的分区数据，因此，调用该函数前，需要先调用 flushTSDBCache，将
cacheEngine 中已完成的分区数据写入磁盘。

## 例子

```
n = 10000
SecurityID = rand(`st0001`st0002`st0003`st0004`st0005, n)
sym = rand(`A`B`C`D`E, n)
TradeDate = 2022.01.01 + rand(100,n)
TotalVolumeTrade = rand(1000..3000, n)
TotalValueTrade = rand(100.0, n)
schemaTable_snap = table(SecurityID, sym, TradeDate, TotalVolumeTrade, TotalValueTrade).sortBy!(`SecurityID`sym`TradeDate)

dbPath = "dfs://TSDB_STOCK"
if(existsDatabase(dbPath)){dropDatabase(dbPath)}
db_snap = database(dbPath, VALUE, 2022.01.01..2022.01.05, engine='TSDB')

snap=createPartitionedTable(dbHandle=db_snap, table=schemaTable_snap, tableName="snap", partitionColumns=`TradeDate, sortColumns=`SecurityID`sym`TradeDate, keepDuplicates=ALL, sortKeyMappingFunction=[hashBucket{,3}, hashBucket{,2}])
snap.append!(schemaTable_snap)

snap1=createPartitionedTable(dbHandle=db_snap, table=schemaTable_snap, tableName="snap1", partitionColumns=`TradeDate, sortColumns=`SecurityID`sym`TradeDate, keepDuplicates=ALL)
snap1.append!(schemaTable_snap)

flushTSDBCache()

getChunksMeta()
```

输出返回：

| site | chunkId | path | dfsPath | type | flag | size | version | state | versionList | resolved |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| server11352 | fe93077a-5a05-34a8-554c-67467415bf68 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220410/yv | /TSDB\_STOCK/20220410/yv | 1 | 0 | 0 | 1 | 0 | cid : 2134,snap1=>2134:89; # | false |
| server11352 | 5c30ef71-3e51-c5ac-6b4d-4458feb8454a | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220407/yv | /TSDB\_STOCK/20220407/yv | 1 | 0 | 0 | 1 | 0 | cid : 2134,snap1=>2134:95; # | false |
| server11352 | 4216dbe9-c238-49a9-4d45-66829c98a7b5 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220406/yv | /TSDB\_STOCK/20220406/yv | 1 | 0 | 0 | 1 | 0 | cid : 2134,snap1=>2134:92; # | false |
| server11352 | 47ea0d35-7ea9-c3b3-cc4b-cc6cd1fe039d | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220401/yv | /TSDB\_STOCK/20220401/yv | 1 | 0 | 0 | 1 | 0 | cid : 2134,snap1=>2134:100; # | false |
| server11352 | aafd71c5-a197-63a9-2d4c-b65cbced3d21 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220330/yv | /TSDB\_STOCK/20220330/yv | 1 | 0 | 0 | 1 | 0 | cid : 2134,snap1=>2134:97; # | false |

```
getTSDBSortKeyEntry("fe93077a-5a05-34a8-554c-67467415bf68")
```

输出返回：

| chunkId | chunkPath | tableName | file | key | size |
| --- | --- | --- | --- | --- | --- |
| fe93077a-5a05-34a8-554c-67467415bf68 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220410/yv | snap1 | 0\_00000058 | st0001\_A | 2 |
| fe93077a-5a05-34a8-554c-67467415bf68 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220410/yv | snap1 | 0\_00000058 | st0001\_B | 3 |
| fe93077a-5a05-34a8-554c-67467415bf68 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220410/yv | snap1 | 0\_00000058 | st0001\_C | 2 |
| fe93077a-5a05-34a8-554c-67467415bf68 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220410/yv | snap1 | 0\_00000058 | st0001\_D | 6 |
| fe93077a-5a05-34a8-554c-67467415bf68 | /dolphindb/server/server11352/storage/CHUNKS/TSDB\_STOCK/20220410/yv | snap1 | 0\_00000058 | st0002\_A | 4 |
