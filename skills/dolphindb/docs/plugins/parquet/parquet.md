<!-- Auto-mirrored from upstream `documentation-main/plugins/parquet/parquet.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Parquet

Apache Parquet 文件采用列式存储格式，可用于高效存储与提取数据。DolphinDB 提供的 Parquet 插件支持将 Parquet 文件导入和导出 DolphinDB，并进行数据类型转换。

## 在插件市场安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本；支持 Shark。

支持 Linux、Linux JIT、Linux ABI、Linux ARM。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("parquet")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("parquet")
   ```

## 用户接口

### extractParquetSchema

**语法**

```
parquet::extractParquetSchema(fileName)
```

**参数**

**fileName** Parquet 文件名，类型为字符串标量。

**详情**

获取 Parquet 文件的结构，返回两列：列名和数据类型。

**例子**

```
parquet::extractParquetSchema("userdata1.parquet")
```

### loadParquet

**语法**

```
parquet::loadParquet(fileName,[schema],[columnsToLoad],[startRowGroup],[rowGroupNum])
```

**参数**

**fileName** Parquet 文件名，类型为字符串标量。

**schema** 可选参数，必须是包含列名和列数据类型的表。通过设置该参数，可改变系统自动生成的列数据类型。

**columnsToLoad** 可选参数，表示要读取的列索引。若不指定，读取所有列。

**startRowGroup** 可选参数，是一个非负整数。从哪一个 row group 开始读取 Parquet 文件。若不指定，默认从文件起始位置读取。

**rowGroupNum** 可选参数，要读取 row group 的数量。若不指定，默认读到文件的结尾。

**详情**

将 Parquet 文件数据加载为 DolphinDB 数据库的内存表。关于 Parquet 数据类型及在 DolphinDB 中的转化规则，参见下文支持的数据类型章节。

**例子**

```
parquet::loadParquet("userdata1.parquet")
```

### loadParquetEx

**语法**

```
parquet::loadParquetEx(dbHandle,tableName,partitionColumns,fileName,[schema],[columnsToLoad],[startRowGroup],[rowGroupNum],[transform])
```

**参数**

**dbHandle** 数据库句柄。

**tableName** 一个字符串，表示表的名称。

**partitionColumns** 字符串标量或向量，表示分区列。在组合分区中，该参数是字符串向量。

**fileName** Parquet 文件名，类型为字符串标量。

**schema** 可选参数，必须是包含列名和列数据类型的表。通过设置该参数，可改变系统自动生成的列数据类型。

**columnsToLoad** 可选参数，整数向量，表示读取的列索引。若不指定，读取所有列。

**startRowGroup** 可选参数，从哪一个 row group 开始读取 Parquet 文件。若不指定，默认从文件起始位置读取。

**rowGroupNum** 可选参数，要读取 row group 的数量。若不指定，默认读到文件的结尾。

**transform** 可选参数，为一元函数，且该函数接受的参数必须是一个表。如果指定了 *transform* 参数，需要先创建分区表，再加载数据，程序会对数据文件中的数据执行 *transform* 参数指定的函数，再将得到的结果保存到分区表中。

**详情**

将 Parquet 文件数据加载到 DolphinDB 数据库的分区表，返回该表的元数据。

* 如果要将数据文件加载到分布式数据库或本地磁盘数据库中，必须指定 *dbHandle*，并且不能为空字符串。
* 如果要将数据文件加载到内存数据库中，那么 *dbHandle* 为空字符串或者不指定 *dbHandle*。

关于 Parquet 数据类型及在 DolphinDB 中的转化规则，参见下文支持的数据类型章节。

**例子**

* dfs 分区表

  ```
  db = database("dfs://rangedb", RANGE, 0 500 1000)
  parquet::loadParquetEx(db,`tb,`id,"userdata1.parquet")
  ```
* 分区内存表

  ```
  db = database("", RANGE, 0 500 1000)
  parquet::loadParquetEx(db,`tb,`id,"userdata1.parquet")
  ```
* 指定参数 *transform*，将数值类型表示的日期和时间（如：20200101）转化为指定类型（比如：日期类型）

  ```
  dbPath="dfs://DolphinDBdatabase"
  db=database(dbPath,VALUE,2020.01.01..2020.01.30)
  dataFilePath="level.parquet"
  schemaTB=parquet::extractParquetSchema(dataFilePath)
  update schemaTB set type="DATE" where name="date"
  tb=table(1:0,schemaTB.name,schemaTB.type)
  tb1=db.createPartitionedTable(tb,`tb1,`date);
  def i2d(mutable t){
      return t.replaceColumn!(`date,datetimeParse(t.date),"yyyy.MM.dd"))
  }
  t = parquet::loadParquetEx(db,`tb1,`date,dataFilePath,datasetName,,,,i2d)
  ```

### parquetDS

**语法**

```
parquet::parquetDS(fileName,[schema])
```

**参数**

**fileName** Parquet 文件名，类型为字符串标量。

**schema** 可选参数，必须是包含列名和列数据类型的表。通过设置该参数，可改变系统自动生成的列数据类型。

**详情**

根据输入的 Parquet 文件名创建数据源列表，生成的数据源数量等价于 row group 的数量。

**例子**

```
ds = parquet::parquetDS("userdata1.parquet")
size ds;
//Output: 1
ds[0];
//Output:DataSource< loadParquet("userdata1.parquet",,,0,1) >
```

### saveParquet

**语法**

```
parquet::saveParquet(table, fileName, [compressMethod])
```

**参数**

**table** 要保存的表。

**fileName** 保存的文件名，类型为字符串标量

**compressMethod** 压缩格式。类型为字符串标量。支持 snappy, gzip, zstd，默认为不压缩。

**详情**

将 DolphinDB 中的表以 Parquet 格式保存到文件中。

**例子**

```
parquet::saveParquet(tb, "userdata1.parquet")
```

### setReadThreadNum

**语法**

```
parquet::setReadThreadNum(num)
```

**参数**

**num** 最大的读取线程数。说明如下：

* 默认为 1，表示不额外创建线程，在当前线程读取 parquet 文件。
* 如果大于 1，则会将读取 parquet 文件的任务分成 num 份，即最大的读取线程数为 num。
* 如果等于 0，则每一列的读取都会作为 ploop 的任务。

**详情**

用于设置是否需要并发读取 parquet 文件和读取 parquet 的最大线程数。

注意：因为 parquet 插件内部会调用 ploop 函数按列分组并行读取 parquet 文件，所以实际读取 parquet 文件的并发度也受 DolphinDB 的 *worker* 参数限制。

**例子**

```
parquet::setReadThreadNum(0)
```

### getReadThreadNum

**语法**

```
parquet::getReadThreadNum()
```

**详情**

获取 parquet 插件的最大读线程数。

**例子**

```
parquet::getReadThreadNum()
```

## 支持的数据类型

### 导入

DolphinDB 在导入 Parquet 数据时，优先按照源文件中定义的 LogicalType 转换相应的数据类型。如果没有定义 LogicalType 或 ConvertedType，则只根据原始数据类型（physical type）转换。同时，支持将 Parquet 文件的 repeated 类型读取为 DolphinDB 的 array vector。

| Logical Type in Parquet | TimeUnit in Parquet | Type in DolphinDB |
| --- | --- | --- |
| INT(bit\_width=8,is\_signed=true) | \ | CHAR |
| INT(bit\_width=8,is\_signed=false or bit\_width=16,is\_signed=true) | \ | SHORT |
| INT(bit\_width=16,is\_signed=false or bit\_width=32,is\_signed=true) | \ | INT |
| INT(bit\_width=32,is\_signed=false or bit\_width=64,is\_signed=true) | \ | LONG |
| INT(bit\_width=64,is\_signed=false) | \ | LONG |
| ENUM | \ | SYMBOL |
| DECIMAL | \ | DOUBLE |
| DATE | \ | DATE |
| TIME | MILLIS\MICROS\NANOS | TIME\NANOTIME\NANOTIME |
| TIMESTAMP | MILLIS\MICROS\NANOS | TIMESTAMP\NANOTIMESTAMP\NANOTIMESTAMP |
| INTEGER | \ | INT\LONG |
| STRING | \ | STRING |
| JSON | \ | not support |
| BSON | \ | not support |
| UUID | \ | not support |
| MAP | \ | not support |
| LIST | \ | not support |
| NIL | \ | not support |

| Converted Type in Parquet | Type in DolphinDB |
| --- | --- |
| INT\_8 | CHAR |
| UINT\_8\INT\_16 | SHORT |
| UINT\_16\INT\_32 | INT |
| TIMESTAMP\_MICROS | NANOTIMESTAMP |
| TIMESTAMP\_MILLIS | TIMESTAMP |
| DECIMAL | DOUBLE |
| UINT\_32\INT\_64\UINT\_64 | LONG |
| TIME\_MICROS | NANOTIME |
| TIME\_MILLIS | TIME |
| DATE | DATE |
| ENUM | SYMBOL |
| UTF8 | STRING |
| MAP | not support |
| LIST | not support |
| JSON | not support |
| BSON | not support |
| MAP\_KEY\_VALUE | not support |

| Physical Type in Parquet | Type in DolphinDB |
| --- | --- |
| BOOLEAN | BOOL |
| INT32 | INT |
| INT64 | LONG |
| INT96 | NANOTIMESTAMP |
| FLOAT | FLOAT |
| DOUBLE | DOUBLE |
| BYTE\_ARRAY | STRING |
| FIXED\_LEN\_BYTE\_ARRAY | STRING |

**注意：**

* 在 Parquet 中标注了 DECIMAL 类型的字段中，仅支持转化原始数据类型（physical type）为 INT32, INT64 和 FIXED\_LEN\_BYTE\_ARRAY 的数据。
* 由于 DolphinDB 不支持无符号类型，所以读取 Parquet 中的 UINT\_64 时若发生溢出，则会取 DolphinDB 中的 NULL 值。

### 导出

将 DolphinDB 数据导出为 Parquet 文件时，系统根据给出表的结构自动转换到 Parquet 文件支持的类型。同时，支持将 DolphinDB 的 array vector 转换为 Parquet 的 repeated 类型。

| Type in DolphinDB | Physical Type in Parquet | Logical Type in Parquet |
| --- | --- | --- |
| BOOL | BOOLEAN | \ |
| CHAR | FIXED\_LEN\_BYTE\_ARRAY | \ |
| SHORT | INT32 | INT(16) |
| INT | INT32 | INT(32) |
| LONG | INT64 | INT(64) |
| DATE | INT32 | DATE |
| MONTH | INT32 | DATE |
| TIME | INT32 | TIME\_MILLIS |
| MINUTE | INT32 | TIME\_MILLIS |
| SECOND | INT32 | TIME\_MILLIS |
| DATETIME | INT64 | TIMESTAMP\_MILLIS |
| TIMESTAMP | INT64 | TIMESTAMP\_MILLIS |
| NANOTIME | INT64 | TIME\_NANOS |
| NANOTIMESTAMP | INT64 | TIMESTAMP\_NANOS |
| FLOAT | FLOAT | \ |
| DOUBLE | DOUBLE | \ |
| STRING | BYTE\_ARRAY | STRING |
| SYMBOL | BYTE\_ARRAY | STRING |
