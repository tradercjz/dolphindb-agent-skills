<!-- Auto-mirrored from upstream `documentation-main/tutorials/backup-restore-new.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 将“备份单张表”中备份的数据恢复到 testdb 的 quotes_restore 表中。
dbPath="dfs://testdb"
tbName=`quotes_2
backupDir="/home/$USER/backupTb"
restoreTb="quotes_restore"
submitJob("restoreTable3","restore quotes_2 to quotes_restore in testdb",restoreTable,backupDir,dbPath,tbName,,restoreTb)
```

`restoreTable` 和`restoreDB`有类似的特性，只不过`restoreTable`是针对分布式表的，而`restoreDB`是针对数据库的。

#### 6.3. 恢复单个分区

要恢复同一个表的部分分区，可以使用 `restore` 函数。和backup备份分区时略有不同，restore中的partition参数只支持传入一个标量，这个标量中可以使用通配符，去匹配多个分区。比如，`%/Key4/tp/%` 可以匹配 `/Key4/tp/20120101`，`/Key4/tp/20120103`，`/Key4/tp/20120104`...等分区。

用例：将[备份分区](#%E5%A4%87%E4%BB%BD%E5%88%86%E5%8C%BA)中备份的分区恢复到新数据库中

```
dbPath="dfs://testdb"
backupDir="/home/$USER/backupPar"
tbName=`quotes_2
pars=["/testdb/Key3/tp/20120101","/testdb/Key4/tp/20120101"]
for (par in pars){
	restore(backupDir,dbPath,tbName,par,false,,true,true)
}
```

#### 6.4. 恢复整个集群

如果需要将整个集群的数据进行迁移，可以先将各个数据库备份至同一个目录下，然后通过`migrate`函数进行恢复。

用例：备份两个数据库`testdb`和`testdb_tsdb`至目录下，然后使用migrate在新集群恢复

```
//旧集群备份testdb和testdb_tsdb
dbPath="dfs://testdb"
dbPath2="dfs://testdb_tsdb"
backupDir="/home/$USER/migrate"
submitJob("backupForMigrate","backup testdb for migrate",backupDB,backupDir,dbPath)
submitJob("backupForMigrate2","backup testdb_tsdb for migrate",backupDB,backupDir,dbPath2)

//备份完成后，在新集群恢复这两个数据库
backupDir="/home/$USER/migrate"
submitJob("migrate","migrate testdb and testdb_tsdb to new cluster",migrate,backupDir)
```

`migrate`和`restoreDB`类似，但是有如下两个区别：

1. migrate可以恢复多个数据库，而restoreDB只能恢复单个数据库。
2. 当恢复后的数据库名称、表名称与原数据库、原表一致时，migrate 要求原数据库、原表已经被删除，否则无法恢复，而 restoreDB 无此限制。所以migrate无法用于增量恢复和断点续恢复，而一般用于新的集群刚部署完成的时候的数据迁移。

#### 6.5. 判断恢复任务是否正常完成

恢复的任务信息也可以通过`getBackupStatus`查询。若要判断恢复任务是否完成，可以参考 [判断备份任务是否正常完成](#%E5%88%A4%E6%96%AD%E5%A4%87%E4%BB%BD%E4%BB%BB%E5%8A%A1%E6%98%AF%E5%90%A6%E6%AD%A3%E5%B8%B8%E5%AE%8C%E6%88%90)。

### 7. 备份恢复的性能

本次性能测试使用的机器 CPU 为Intel(R) Xeon(R) Silver 4314 CPU @ 2.40GHz

使用的DolphinDB集群为 DolphinDB 普通集群，1个 controller，3个 datanode，每个 datanode 挂载1个普通SSD盘，读写速度约为500MB/s。备份文件所在的磁盘也是SSD盘，读写速度也为500MB/s。

cluster.cfg配置如下：

```
maxMemSize=256
maxConnections=512
workerNum=8
chunkCacheEngineMemSize=16
newValuePartitionPolicy=add
maxPubConnections=64
subExecutors=4
subPort=8893
lanCluster=0
enableChunkGranularityConfig=true
diskIOConcurrencyLevel=0
```

运行备份时，落库为50G大小的数据，观察备份文件所在的磁盘IO，写入速度为490MB/s左右，基本达到了磁盘的性能瓶颈。

运行恢复时，因为是写入多个磁盘，我们用数据量/时间来估算写入速度。备份文件大小为50G，恢复花费了2分20秒，速度约为365MB/s，低于备份速度。

### 8. 常见问题

#### 8.1. 是否支持恢复到某个时间点？

不支持，DolphinDB的增量备份并不是添加新的binlog，而是直接覆盖原文件。所以，增量备份功能只是跳过了不需要备份的分区，从而加速了备份，而不支持恢复到某个时间点。在 DolphinDB 中，如果你需要恢复到到一周前的任意一天，那么你需要在一周前的每一天都备份一份数据，并且放在不同的目录中。

#### 8.2. 备份时所有分区的时间点是否一致？

一致。

#### 8.3. 是否支持断点续备/恢复?

支持。具体见[备份单个数据库](#%E5%A4%87%E4%BB%BD%E5%8D%95%E4%B8%AA%E6%95%B0%E6%8D%AE%E5%BA%93)。

#### 8.4. 是否支持增量备份/恢复？

支持。具体见[备份单个数据库](#%E5%A4%87%E4%BB%BD%E5%8D%95%E4%B8%AA%E6%95%B0%E6%8D%AE%E5%BA%93)。

#### 8.5. 如何查看备份进度？

使用 `getBackupStatus` 函数。具体见[getbackupstatus](#getbackupstatus)

#### 8.6. 如何检查备份是否完成？

见[判断备份任务是否正常完成](#%E5%88%A4%E6%96%AD%E5%A4%87%E4%BB%BD%E4%BB%BB%E5%8A%A1%E6%98%AF%E5%90%A6%E6%AD%A3%E5%B8%B8%E5%AE%8C%E6%88%90)。

#### 8.7. 如何检查恢复是否完成？

见[判断恢复任务是否正常完成](#%E5%88%A4%E6%96%AD%E6%81%A2%E5%A4%8D%E4%BB%BB%E5%8A%A1%E6%98%AF%E5%90%A6%E6%AD%A3%E5%B8%B8%E5%AE%8C%E6%88%90)
