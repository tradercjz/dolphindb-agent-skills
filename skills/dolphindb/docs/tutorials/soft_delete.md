<!-- Auto-mirrored from upstream `documentation-main/tutorials/soft_delete.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 软删除

为满足近来用户对某些场景下删除性能的更高要求，我们在 2.00.11 版本的 DolphinDB Server 中特别支持了软删除的功能。本文作为该功能的使用教程，将详细介绍软删除的实现原理与应用场景，同时提供性能测试案例以供参考。

## 1 概述

软删除（Soft Delete）是一种在数据库中处理数据删除的方法，这种删除方式并不是直接从数据库中移除数据，而是通过特定的标记方式在查询的时候将此记录过滤掉，在后台合并数据文件时才真正删除数据。相对于硬删除（Hard Delete），即直接从数据库中永久删除数据，软删除以追加方式进行数据删除，可大幅度提升列式数据库删除的效率。

## 2 原理介绍

相比于常见的硬删除，软删除是一种新的设计方案。本节将先对硬删除和软删除的原理进行详细介绍，然后对比两种删除方式的特点。

### 2.1 硬删除的删除和查询逻辑

#### 2.1.1 删除逻辑

直接从文件中删除数据。

1. **分区剪枝**：根据删除条件进行分区剪枝，确定删除涉及的分区。
2. **查到内存删除**：取出对应分区所有数据到内存后，根据条件删除数据。
3. **写回删除后的分区数据到新目录**：将删除后的数据重新写入数据库，系统会使用一个新的 CHUNK 目录（默认是“*物理表名\_cid*”）来保存写入的数据，旧的文件将被定时回收（默认 30 min）。

#### 2.1.2 查询逻辑

从文件中读取查询结果。

1. **分区剪枝**：根据查询条件进行分区剪枝，确定查询涉及的分区。
2. **读到内存**：根据查询条件在分区的文件中读取查询结果。

### 2.2 软删除的删除和查询逻辑

#### 2.2.1 删除逻辑

追加写入带删除标记的数据。

1. **分区剪枝**：根据查询语句进行分区剪枝，缩窄查询范围。
2. **读到内存获取待删除数据**：根据查询条件，查询出需要删除的数据。
3. **追加写入待删除数据**：给需要删除的数据打上删除标记（deletion flag），并将排序列（sort column）和分区列（partition column）外字段值设置为空值，以 `append` 方式将数据追加写入 TSDB。

#### 2.2.2 查询逻辑

读取查询结果，过滤带删除标记的数据。

1. **分区剪枝**：根据查询条件进行分区剪枝，确定查询涉及的分区。
2. **读到内存**：根据查询条件在分区内读取查询结果（包含删除前的数据和带删除标记的数据）到内存中。
3. **过滤数据**：删除内存中带删除标记的数据。

### 2.3 软删除的特点

从上面的原理介绍可以看出，软删除相比硬删除有如下特点：

1. 删除少量数据快，删除大量数据慢：软删除写入的是待删除数据，硬删除写入的是未删除数据。如果删除的数据量少，软删除需要写入的数据就比硬删除少，性能更好；反之则更差。
2. 查询性能差：查询时，软删除相比硬删除，除了读取未删除的数据，还需要读取删除前的数据和带删除标记的数据，最后还需要在内存中做一次过滤，综合性能比硬删除差。

## 3 使用介绍

使用软删除时必须满足以下条件：

1. `database` 创建库时指定 TSDB 引擎。
2. `createTable` 或者 `createPartitionedTable` 函数创建表时，指定 *softDelete* 为 true 且 *keepDuplicates*=LAST。
3. 使用 `delete` 删除且 SQL 语句中包含 `where` 条件。

### 3.1 软删除使用条件

|  |  |  |  |
| --- | --- | --- | --- |
| **步骤** | **条件** | **示例语句** | **说明** |
| 创建数据库 | *engine* 参数值为 TSDB | `db = database("dfs://softDelete",VALUE,[2023.01.01],,"TSDB")` | 创建一个 TSDB 引擎，以值分区的数据库。 |
| 创建数据表 | *keepDuplicates* 参数值为 LAST；创建表时 *softDelete* 参数值为 true，即开启软删除。参数值为 TSDB | `t = table(1:0,"Time""Symbol""Price",[TIMESTAMP,STRING,DOUBLE])` |  |
| 创建维度表：`` createTable(dbHandle=db,table=t, tableName="memTable",sortColumns=`Symbol`Time,keepDuplicates=LAST, softDelete=true) `` | [DolphinDB-createTable](https://docs.dolphindb.cn/zh/funcs/c/createTable.html?hl=createtable) |
| 创建分区表：`` createPartitionedTable(dbHandle=db,table=t, tableName="parTable",partitionColumns=`Time,sortColumns=`Symbol`Time,keepDuplicates=LAST, softDelete=true) `` | [DolphinDB-createPartitionedTable](https://docs.dolphindb.cn/zh/funcs/c/createPartitionedTable.html?hl=createpartitionedtable) |
| 创建数据表 | 必须指定 where 过滤条件 | 维度表删除数据：`delete from loadTable("dfs://softDelete", "memTable") where Date = 2024.01.02 and Price > 50` | 维度表：查出符合 `Price > 50`条件的数据，将数据除 sortColumns 列外的数据设置为空，在数据上打上删除标记，写回数据表。 |
| 分区表删除数据：`delete from loadTable("dfs://softDelete", "parTable") where Date = 2024.01.02 and Price > 50` | 分区表：先进行分区剪枝，选择 2024.01.02 这个分区的数据，查出符合 `Price > 50`条件的数据，将数据除 sortColumns 列外的数据设置为空，在数据上打上删除标记，写回数据表。 |

## 4 性能测试

### 4.1 环境配置

测试共使用三台配置相同的服务器，具体硬件配置如表所示。

| 处理器 | 核数 | 内存 | 操作系统 | 硬盘 | 网络 |
| --- | --- | --- | --- | --- | --- |
| Intel(R) Xeon(R) Silver 4216 CPU @ 2.10GHz | 64 | 512 GB | CentOS Linux release 7.6 | HDD | 10000 Mb/s |

基于 DolphinDB Server 2.00.11 版本部署了双副本高可用集群。

### 4.2 模拟数据

首先，创建数据库和数据表，并启用软删除功能。

```
//创建数据库， 使用 TSDB 引擎
db1 = database(,VALUE,[2023.01.01])
db2 = database(,HASH,[SYMBOL, 25])
db = database("dfs://softDelete.level2_tl",COMPO,[db1,db2],,"TSDB")
//创建数据表
colName = `ChannelNo`ApplSeqNum`MDStreamID`SecurityID`SecurityIDSource`Price`OrderQty`Side`TradeTIme`OrderType`OrderIndex`LocalTime`SeqNo`Market`DataStatus`BizIndex
colType = [INT,LONG,INT,SYMBOL,INT,DOUBLE,INT,SYMBOL,TIMESTAMP,SYMBOL,INT,TIME,LONG,SYMBOL,INT,LONG]
tbSchema = table(1:0, colName, colType)
//softDelete设置为true，启用软删除
db.createPartitionedTable(table=tbSchema,tableName=`entrust,partitionColumns=`TradeTIme`SecurityID,sortColumns=`Market`SecurityID`TradeTIme,keepDuplicates=LAST,softDelete=true)
```

构造模拟数据并写入分布式表。

```
n = 500000
Symbol = `000021`000155`000418`000673`000757`000759`000851`000856`000909`000961
TradeTime = array(timestamp)
for(i in 0:Symbol.size()){
    TradeTime.append!(2015.07.01 09:15:00.160..((2015.07.01 09:15:00.160+n/10)-1))
}
t = table(
    take(int(),n) as ChannelNo,
    take(long(),n) as ApplSeqNum,
    take(int(),n) as MDStreamID,
    take(Symbol,n) as SecurityID,
    take(int(),n) as SecurityIDSource,
    rand(100.0,n) as Price,
    rand(20,n)*100 as OrderQty,
    rand(`S`B,n) as Side,
    TradeTime as TradeTIme,
    take(["0","1","2"],n) as OrderType,
    take(int(),n) as OrderIndex,
    take(time(),n) as LocalTime,
    take(long(),n) as SeqNo,
    take(`sz,n) as Market,
    take(int(),n) as DataStatus,
    take(long(),n) as BizIndex
)
loadTable("dfs://softDelete.level2_tl","entrust").append!(t)
```

具体测试代码请下载附录的 .txt 文件。

### 4.3 性能分析

| 数据删除百分比 | 软删除/硬删除 delete 耗时比例 | 软删除（level file 合并前）/硬删除（level file 合并前）select 耗时比例 | 软删除（level file 合并后）/硬删除（level file 合并后）select 耗时比例 |
| --- | --- | --- | --- |
| 10 | 0.236 | 1.502 | 1.219 |
| 20 | 0.318 | 1.831 | 1.22 |
| 30 | 0.446 | 1.88 | 1.254 |
| 40 | 0.578 | 1.947 | 1.309 |
| 50 | 0.76 | 2.163 | 1.243 |
| 60 | 1.093 | 2.541 | 1.297 |
| 70 | 1.273 | 3.028 | 1.22 |
| 80 | 1.856 | 3.38 | 1.172 |
| 90 | 2.921 | 4.319 | 0.935 |

通过对比不同数据删除百分比下的删除时间，可以得出结论：删除的数据量越少，软删除的性能越好。

这是因为硬删除在删除少量百分比的数据时需要写回剩余大量的原数据，而软删除仅需要写少量百分比的待删除数据。以 10% 数据删除百分比为例，此时软删除的性能是硬删除的七倍左右。随着数据删除的数量不断上升，硬删除需要写回的数据量就不断减少，软删除需要写回的数据量在不断增加，所以在删除一个分区的大量数据时硬删除优于软删除的性能。

通过对比不触发 level file 合并和触发 level file 合并的查询时间，可以得出不触发 level file 合并查询的性能会略微下降，在触发 level file 合并后，查询的性能影响不大。因为硬删除会把数据全部重写成一个 level file；而软删除之后最终会生成两个 level file，会增加去重的消耗。但在触发 level file 合并之后，两者性能基本相同。

## 5 小结

相较于硬删除，虽然软删除支持的范围更小，但软删除可以大幅度提升删除的性能。不过在具体使用中须注意，用户需要定时触发 level file 的合并来避免查询性能的损耗。

## 6 附录

### 6.1 常见问题

| **问题** | **回答** |
| --- | --- |
| `createPartitionedTable(dbHandle, table, tableName, partitionColumns, \[compressMethods], \[sortColumns], \[keepDuplicates=ALL], \[sortKeyMappingFunction], \[softDelete=false]). The softDelete parameter is available only when engineType is specified as "TSDB" and keepDuplicates as "LAST".` | 在 *softDelete* 指定为 true 时，*keepDuplicates* 需要指定为 LAST |
| `The softDelete parameter is available only when engineType is specified as "TSDB" and keepDuplicates as "LAST".` | 软删除仅在 TSDB 引擎支持，需要在建库时指定 *engine* 为 TSDB |

### 6.2 相关脚本

性能测试的脚本：[软删除性能测试.txt](https://cdn.dolphindb.cn/zh/tutorials/script/soft_delete_test.txt)
