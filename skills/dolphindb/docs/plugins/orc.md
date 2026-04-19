<!-- Auto-mirrored from upstream `documentation-main/plugins/orc.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# ORC

ORC 是一种自描述列式文件格式，专门为 Hadoop 生态设计，可用于高效存储与提取数据，因此适合大批量流数据读取场景。

DolphinDB 的 ORC 插件支持将 ORC 文件导入和导出 DolphinDB，并且在导入导出过程中自动进行数据类型转换。

## 安装插件

### 版本要求

DolphinDB Server：2.00.10 及更高版本。支持 Linux x86-64, Linux JIT。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("orc")
   ```
3. 使用 `loadPlugin` 命令加载插件 。

   ```
   loadPlugin("orc")
   ```

## 接口说明

### extractORCSchema

**语法**

```
orc::extractORCSchema(filePath)
```

**详情**

解析指定 ORC 文件中数据集的结构。返回一个表，包括 name 和 type 两列，分别表示列名和数据类型。

**参数**

**filePath** STRING 类型标量，表示 ORC 文件名。

**例子**

```
orc::extractORCSchema("userdata1.orc")
```

### loadORC

**语法**

```
orc::loadORC(filePath,[schema],[column],[rowStart],[rowNum])
```

**详情**

将 ORC 文件数据加载为 DolphinDB 的内存表。返回一个将 ORC 文件导入后的内存表。支持的 ORC 数据类型，以及数据转化规则可见数据类型章节。

**参数**

**filePath** STRING 类型标量，表示 ORC 文件名。

**schema** 包含列名和列的数据类型的表。若要改变列的数据类型，需要在 schema 表中修改数据类型。

**column** 整型向量，表示读取的列的索引。若不指定，读取所有列。

**rowStart** INT 类型标量，表示从哪一行开始读取 ORC 文件。若不指定，默认从文件起始位置读取。

**rowNum** INT 类型标量，表示读取的行数。若不指定，默认读到文件的结尾。

**例子**

```
orc::loadORC("userdata1.orc")
```

**注意**：DolphinDB 中不支持以下划线开头的列名。若 ORC 文件中含有以下划线开头的列名，系统自动增加字母 "Z" 作为前缀。

### loadORCEx

**语法**

```
orc::loadORCEx(dbHandle,tableName,[partitionColumns],filePath,[schema],[column],[rowStart],[rowNum],[transform])
```

**详情**

将 ORC 文件数据转换为 DolphinDB 数据库的分布式表，然后将表的元数据加载到内存中。返回一个包含分布式表元数据的表对象。支持的 ORC 数据类型，以及数据转化规则可见数据类型章节。

**参数**

**dbHandle** 与 **tableName** 分别表示数据库句柄和表名。

**partitionColumns** STRING 类型标量或向量，表示分区列。当分区数据库不是 SEQ 分区时，我们需要指定分区列。在组合分区中，*partitionColumns* 是字符串向量。

**filePath** STRING 类型标量，表示 ORC 文件名。

**schema** 包含列名和列的数据类型的表。若要改变列的数据类型，需要在 schema 表中修改数据类型。

**column** 整型向量，表示读取的列的索引。若不指定，读取所有列。

**rowStart** INT 类型标量，表示从哪一行开始读取 ORC 文件。若不指定，默认从文件起始位置读取。

**rowNum** INT 类型标量，表示读取的行数。若不指定，默认读到文件的结尾。

**transform** 一元函数，并且该函数接受的参数必须是一个表。如果指定了 *transform* 参数，需要先创建分区表，再加载数据，程序会对数据文件中的数据执行 *transform* 参数指定的函数，再将得到的结果保存到数据库中。

**例子**

* 不指定 *transform*，数据不经过处理，直接入库。

  ```
  db = database("dfs://db1", RANGE, 0 500 1000)
  orc::loadORCEx(db,`tb,`id,"userdata1.orc")
  ```
* 指定 *transform* 将数值类型表示的日期和时间 (比如：20200101) 转化为指定类型 (比如：日期类型)。

  ```
  dbPath="dfs://db2"
  db=database(dbPath,VALUE,2020.01.01..2020.01.30)
  dataFilePath="userdata1.orc"
  schemaTB=orc::extractORCSchema(dataFilePath)
  update schemaTB set type="DATE" where name="date"
  tb=table(1:0,schemaTB.name,schemaTB.type)
  tb1=db.createPartitionedTable(tb,`tb1,`date);
  def i2d(mutable t){
      return t.replaceColumn!(`date,datetimeParse(t.date),"yyyy.MM.dd"))
  }
  t = orc::loadORCEx(db,`tb1,`date,dataFilePath,datasetName,,,,i2d)
  ```

### orcDS

**语法**

```
orc::orcDS(filePath,chunkSize,[schema],[skipRows])
```

**详情**

根据输入的文件名创建数据源列表，数量由文件中的行数与 chunkSize 决定。返回由数据源组成的向量。

**参数**

**filePath** STRING 类型标量，表示 ORC 文件名。

**chunkSize** INT 类型标量，表示每个数据源包含的行数。

**schema** 包含列名和列的数据类型的表。若要改变由系统自动决定的列的数据类型，需要在 *schema* 表中修改数据类型，并且把它作为 `loadORC` 函数的一个参数。

**skipRows** INT 类型标量，表示从文件头开始忽略的行数，默认值为 0。

**例子**

```
>ds = orc::orcDS("userdata1.orc", 1000)
>size ds;
1
>ds[0];
DataSource<loadORC("userdata1.orc", , 0, 1000) >
```

### saveORC

**语法**

```
orc::saveORC(table, fileName)
```

**参数**

**table** 要保存的内存表对象。

**fileName** STRING 类型标量，保存的 ORC 文件名。

**详情**

将 DolphinDB 内存表保存为 ORC 格式文件。
请注意，若向一个已存在的 ORC 文件中保存表数据，则会覆盖 ORC 文件原有内容。

**例子**

```
orc::saveORC(tb, "example.orc")
```

## 支持的数据类型

ORC 的数据类型转换为 DolphinDB 数据类型对照表：

| Type in ORC | Type in DolphinDB |
| --- | --- |
| boolean | BOOL |
| tinyint | CHAR |
| smallint | SHORT |
| int | INT |
| bigint | LONG |
| float | FLOAT |
| double | DOUBLE |
| string | STRING |
| char | STRING |
| varchar | STRING |
| binary | not support |
| timestamp | NANOTIMESTAMP |
| date | DATE |
| struct | not support |
| list | not support |
| map | not support |
| union | not support |

## 使用示例

```
// 读取 orc 文件中数据集的结构
orcSchema = orc::extractORCSchema("userdata1.orc")

// 读取 orc 文件数据内容到内存表
orcData = orc::loadORC("userdata1.orc")

// 读取 orc 文件到数据库中
db = database("dfs://db1", RANGE, 0 500 1000)
orc::loadORCEx(db,`tb,`id,"userdata1.orc")

// 根据输入的 orc 文件名创建数据源列表
ds = orc::orcDS("userdata1.orc", 1000)

// 将内存表存为 orc 文件
orc::saveORC(orcData, "example.orc")
```
