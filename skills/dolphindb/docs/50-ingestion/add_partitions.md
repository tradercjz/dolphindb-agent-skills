<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db_oper/add_partitions.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 增加分区

DolphinDB 目前支持给值分区或范围分区的数据库，或者包含值分区或范围分区的组合分区数据库添加分区。

## 增加值分区

这里首先创建一个数据库，采用范围分区和值分区的组合分区方案，二级分区包含从 2024.08.07 到 2024.08.11
共五个分区。

```
n=1000000
ID=rand(50..59, n)
dates=2024.08.07..2024.08.11
date=rand(dates, n)
x=rand(10.0, n)
t=table(ID, date, x);

dbID=database(, RANGE, 50 100);
dbDate = database(, VALUE, 2024.08.07..2024.08.11)
db = database("dfs://compoDB", COMPO, [dbID, dbDate]);
pt = db.createPartitionedTable(t, `pt, `ID`date)
pt.tableInsert(t);
```

当写入现有值分区以外的数据时（日期不属于 2024.08.07 到 2024.08.11），有两种方式增加分区进而存储这些数据：

1. 将配置参数 *newValuePartitionPolicy* 设定为 add 。（单机模式中在 dolphindb.cfg
   中配置，集群模式在 cluster.cfg 中配置）这会使得值分区自动增加以适应现有分区外的数据。此外，该配置参数还有两个可选值：
   * skip（默认值）：此时仅存储属于现有分区以内的数据。
   * fail：当写入现有分区以外的数据时抛出异常。
2. 使用addValuePartitions 函数手动增加对应分区。

   下例是给组合分区的数据库的日期分区层增加分区：

   * 在第一个现有数据分区前面新增 2024.08.01 到 2024.08.06 分区
   * 在最后一个现有数据分区后面新增 2024.08.12 到 2024.08.20 分区

   ```
   // 查看当前二级分区结构
   schema(database("dfs://compoDB")).partitionSchema[1]
   //output: [2024.08.07,2024.08.08,2024.08.09,2024.08.10,2024.08.11]

   // 新增 2024.08.06 分区
   addValuePartitions(database("dfs://compoDB"),2024.08.06,1);
   // 查看当前二级分区结构
   schema(database("dfs://compoDB")).partitionSchema[1]
   // output:[2024.08.06,2024.08.07,2024.08.08,2024.08.09,2024.08.10,2024.08.11]

   // 新增 2024.08.12 分区
   addValuePartitions(database("dfs://compoDB"),2024.08.12,1);
   // 查看当前二级分区结构
   schema(database("dfs://compoDB")).partitionSchema[1]
   // output:[2024.08.06,2024.08.07,2024.08.08,2024.08.09,2024.08.10,2024.08.11,2024.08.12]
   ```

注：

这里使用 `database("dfs://compoDB")` 获取数据库
dfs://compoDB 的句柄，参数 *dbHandle* 也可指定为创建数据库时返回的句柄`db`。

## 增加范围分区

对于范围分区的数据库，无法像值分区数据库那样根据设置参数来自动增加分区，默认会舍弃现有分区之外的数据。可以通过 addRangePartitions
函数扩展分区方案，但只能在最后一个现有数据分区后面添加分区，不能在第一个现有数据分区前面添加分区。例如：

* 可以给上例中的数据库的 ID 分区层新增 [100,150), [150,200) 和 [200,250) 这三个分区
* 但无法增加 [0,50) 这个分区

```
// 增加 [100,150), [150,200) 和 [200,250) 分区
addRangePartitions(database("dfs://compoDB"),100 150 200 250,0);
// 查看当前一级分区结构
schema(database("dfs://compoDB")).partitionSchema[0]
//output:[50,100,150,200,250]

// 增加 [0,50) 分区
addRangePartitions(database("dfs://compoDB"),0 50,0);
// 报错
```

**相关信息**

* [addRangePartitions](../../funcs/a/addRangePartitions.html "addRangePartitions")
* [addValuePartitions](../../funcs/a/addValuePartitions.html "addValuePartitions")
