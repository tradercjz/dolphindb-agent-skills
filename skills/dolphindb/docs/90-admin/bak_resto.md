<!-- Auto-mirrored from upstream `documentation-main/sys_man/bak_resto.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 数据备份与恢复

## 数据备份

DolphinDB以分区为单位进行数据备份，每个分区备份为一个数据文件。在DolphinDB中，我们使用backup 函数备份整个库，部分表或部分分区。

目前 DolphinDB 支持两种备份方式：拷贝文件或 SQL 语句。

* 备份文件方式，即调用 backup 函数时，指定为
  *dbPath*。此方式将备份文件拷贝至指定目录。备份后，系统会在 backupDir/dbName/tbName 目录下生成元数据文件
  \_metaData 和 domain，并将分区文件整体拷贝至 backupDir/dbName/tbName/chunkID 目录下。

  下例以拷贝文件方式备份 `dfs://compoDB/pt`
  数据表的所有数据。

  ```
  backup("/home/DolphinDB/backup","dfs://compoDB",true);
  ```

* SQL 语句，即调用 `backup` 函数时，指定为
  sqlObj。此方式将分区备份为一个二进制的数据文件。备份时需要指定存放二进制文件的路径、数据（用SQL语句表示）。备份后，系统会在
  backupDir/dbName/tbName 目录下生成元数据文件 \_metaData, domain 和数据文件
  <chunkID>.bin。

  下面的例子备份了 `dfs://compoDB/pt` 数据表的所有数据。

  ```
  backup("/home/DolphinDB/backup",<select * from loadTable("dfs://compoDB","pt")>,true);
  ```

为方便用户使用，DolphinDB 对 `backup` 进一步封装，提供了 backupDB 用于一键备份数据库下所有表，以及 backupTable 用于一键备份一个数据表。

| 区别 | backup | backupDB | backupTable |
| --- | --- | --- | --- |
| 备份对象 | 一次备份整个数据库及表、备份指定表的全部或部分数据 | 一次备份一个数据库下所有表 | 一次备份一个数据库下的一个表 |
| SQL 语句备份 | √ | × | × |
| 拷贝文件备份 | √ | √ | √ |

## 数据恢复

DolphinDB 数据恢复的方法：

* 使用 migrate 函数
* 使用 restore 函数
* 使用 restoreDB 函数
* 使用 restoreTable 函数

| 区别 | migrate | restore | restoreDB | restoreTable |
| --- | --- | --- | --- | --- |
| 恢复对象 | 一次可以恢复备份目录下的所有数据库及表 | 一次只能恢复一个表中部分或全部分区的数据 | 一次恢复一个数据库下的所有表 | 一次恢复一个数据库下的一个表 |
| SQL 语句备份 | √ | √ | × | × |
| 拷贝文件备份 | √ | √ | √ | √ |
| 跨引擎备份 | √ | √ | × | √ |
| 备份与原库名/表名相同时，是否需要删除原库/表 | √ | × | × | × |

## 其他相关函数

* getBackupList：查看某个分布式表的所有备份信息，返回一张表，每个分区对应一行记录。
* getBackupMeta：查看某张表，某个分区的备份的信息，返回一个字典，包含schema,
  cid, path等信息。
* loadBackup：加载指定分布式表中某个分区的备份数据。
* checkBackup：检查备份文件的的完整性和准确性。
* getBackupStatus：查看数据备份/恢复任务的具体信息。

## 示例

下面的例子创建了一个组合分区的数据库 `dfs://compoDB`。

```
n=1000000
ID=rand(100, n)
dates=2017.08.07..2017.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x);

dbDate = database(, VALUE, 2017.08.07..2017.08.11)
dbID=database(, RANGE, 0 50 100);
db = database("dfs://compoDB", COMPO, [dbDate, dbID]);
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);
```

备份表pt的所有数据：

```
backup("/home/DolphinDB/backup",<select * from loadTable("dfs://compoDB","pt")>,true);
```

SQL元代码中可以添加where条件。例如，备份date>2017.08.10的数据。

```
backup("/home/DolphinDB/backup",<select * from loadTable("dfs://compoDB","pt") where date>2017.08.10>,true);
```

查看表pt的备份信息：

```
getBackupList("/home/DolphinDB/backup","dfs://compoDB","pt");
```

加载20120810/0\_50分区的备份信息到内存：

```
x = getBackupMeta("/home/DolphinDB/backup","dfs://compoDB/20170810/0_50","pt");
```

加载20120810/0\_50分区的备份数据：

```
loadBackup("/home/DolphinDB/backup","dfs://compoDB/20170810/0_50","pt");
```

将表pt的数据恢复到新数据库dfs://db1的表pt中：

```
migrate("/home/DolphinDB/backup", "dfs://compoDB", "pt", "dfs://db1", "pt")
```

使用migrate函数无需自己创建新数据库，系统会自动创建新数据库。

在数据库 `dfs://compoDB` 中创建一个与pt结构相同的表temp：

```
temp=db.createPartitionedTable(t, `pt, `date`ID);
```

把pt中2017.08.10的所有分区的备份数据拷贝到与pt分区结构相同的temp表：

```
restore("/home/DolphinDB/backup","dfs://compoDB","pt","%20170810%",true,temp);
```
