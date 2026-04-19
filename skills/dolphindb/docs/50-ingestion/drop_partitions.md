<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db_oper/drop_partitions.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 删除分区

DolphinDB 支持通过 dropPartition
函数删除分区：

```
dropPartition(dbHandle, partitionPaths, [tableName], [forceDelete=false], [deleteSchema=false])
```

其中：

* *dbHandle* 是数据库句柄。
* *partitionPaths* 指定删除哪些分区。
* *tableName* 指定表名。
* *forceDelete* 指定是否强制删除。
* *deleteSchema* 指定是否从分区结构中删除该分区。

## 删除分区结构

仅 VALUE 分区支持删除分区结构的操作。删除时应指定参数 *deleteSchema* = true。

支持删除分区结构的数据库须满足以下要求：

* 第一级分区为 VALUE 分区。
* 数据库中仅包括一个表。

本节示例中，数据库的第一级分区为 VALUE 分区，第二级分区为 RANGE
分区：

```
// 建库建表并模拟数据
n=1000000
ID=rand(150, n)
dates=2024.08.07..2024.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)
dbDate = database(, VALUE, 2024.08.07..2024.08.11)
dbID = database(, RANGE, 0 50 100 150)
db = database("dfs://compoDB", COMPO, [dbDate, dbID])
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);

// 删除 2024，08.07 数据及其分区结构
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=2024.08.07, tableName=`pt, deleteSchema=true);
```

注：

函数 `dropPartition` 的参数 *dbHandle*
也可指定为创建数据库时返回的句柄 `db`。

## 删除分区数据

要删除分区内数据同时保留分区结构，可在调用函数 dropPartition 时设置参数*deleteSchema*= false 实现。

本节以删除指定表的分区数据为例进行介绍。以下示例中使用的分布式表 pt
及其数据由以下脚本生成。组合分区的数据库第一层分区为基于日期的值分区，第二层分区为基于值的范围分区：

```
n=1000000
ID=rand(150, n)
dates=2024.08.07..2024.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x)
dbDate = database(, VALUE, 2024.08.07..2024.08.11)
dbID = database(, RANGE, 0 50 100 150)
db = database("dfs://compoDB", COMPO, [dbDate, dbID])
pt = db.createPartitionedTable(t, `pt, `date`ID)
pt.append!(t);
```

### 例 1. 删除某个分区

删除表 pt 的 "/20240807/0\_50" 分区，有以下两种方法：

* 指定路径：

  ```
  dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths="/20240807/0_50", tableName=`pt);
  ```
* 指定条件：

  ```
  dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=[2024.08.07, 0], tableName=`pt);
  ```

注：

"/20240807/0\_50" 分区中的 ID 的可取值范围是从 0 到 49，不包括
50。以上脚本中，可以使用 0 到 49 的任一数字来代表此分区。

### 例 2. 删除一级分区

删除表 pt 的一级分区 2024.08.08，有以下两种方法：

* 使用向量指定该一级分区之下所有分区的路径：

  ```
  partitions=["/20240808/0_50","/20240808/50_100","/20240808/100_150"]
  dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=partitions, tableName=`pt);
  ```
* 指定条件：

  ```
  dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=2024.08.08, tableName=`pt);
  ```

### 例 3. 删除二级分区

删除表 pt 的二级分区 [0,50)，有以下两种方法：

* 使用向量指定含有该二级分区的所有分区的路径：

  ```
  partitions=["/20240807/0_50","/20240808/0_50","/20240809/0_50","/20240810/0_50","/20240811/0_50"]
  dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=partitions, tableName=`pt);
  ```
* 指定条件，不过滤一级分区，所以 *partitionPaths* 的第一个元素为空；第二个元素中的
  0 可以是 [0,50) 之间的任意整数：

  ```
  dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=[,[0]], tableName=`pt);
  ```

### 例 4. 删除跨多个分区的数据

删除表 pt 的二级分区 [0,50) 和[100,150)：

```
dropPartition(dbHandle=database("dfs://compoDB"), partitionPaths=[,[0,100]], tableName=`pt);
```

existsPartition 函数可以检查某个分区是否存在。例如，检查数据库 "dfs://compoDB" 中表 pt 对应的
"/20240807/0\_50" 分区是否存在：

```
listTables("dfs://compoDB")
```

| tableName | physicalIndex |
| --- | --- |
| pt | 408 |

```
existsPartition("dfs://compoDB/20240807/0_50/408")
// output
false
```

**相关信息**

* [dropPartition](../../funcs/d/dropPartition.html "dropPartition")
* [existsPartition](../../funcs/e/existsPartition.html "existsPartition")
