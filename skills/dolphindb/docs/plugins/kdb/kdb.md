<!-- Auto-mirrored from upstream `documentation-main/plugins/kdb/kdb.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Kdb+

Kdb+ 是可以用于存储、分析、处理和检索大型数据集的列式关系型时间序列数据库。为便于从 Kdb+ 迁移数据，DolphinDB 提供了 kdb+ 插件，支持导入 kdb+ 数据库存储在磁盘上的数据。通过 loadTable 和 loadFile 接口导入 DolphinDB 内存表。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本，支持 Linux x86-64, Linux JIT, Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   **注意**：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("kdb")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("kdb")
   ```

## 接口说明

### connect

**语法**

```
kdb::connect(host, port, [credentials])
```

**详情**

建立与 kdb+ 服务器之间的连接。返回一个连接句柄。

如果建立连接失败，则会抛出异常。包括以下三种情况：

1. 身份认证异常，用户名或密码错误。
2. 连接端口异常，对应主机的端口不存在。
3. 超时异常，建立连接超时。

**参数**

**host** STRING 类型标量，表示要连接的 kdb+ 数据库所在的主机地址。

**port** INT 类型标量，表示要连接的 kdb+ 数据库所在的监听端口。

**credentials** STRING 类型标量，表示所要连接的 kdb+ 数据库的登录用户名和密码。格式为 "username:password"。若启动 kdb+ 时没有指定用户名和密码，则该参数为空或任意字符串。

**例子**
假设登录 kdb+ 数据库的用户名和密码（admin:123456）存储在 `../passwordfiles/usrs` 中，且 kdb+ 服务器和 DolphinDB server 都位于同一个主机上。

kdb+ 终端执行：

```
kdb shell：         q -p 5000 -U ../passwordfiles/usrs   // 注意 -U 一定需要大写
```

DolphinDB 客户端执行：

```
// 若开启 kdb+ 时指定了用户名和密码
handle = kdb::connect("127.0.0.1", 5000, "admin:123456")

// 若开启 kdb+ 时未指定用户名和密码
handle = kdb::connect("127.0.0.1", 5000)
```

### execute

**语法**

```
kdb::execute(conn, qScript)
```

**详情**

连接 kdb+ 数据库，通过 kdb+ 数据库执行语句获取数据。返回内存表、向量或者标量。

**参数**

**conn** RESOURCE 类型标量，是 kdb+ 数据库的连接句柄。

**qScript** STRING 类型标量，表示需要执行的 kdb+ q 语言语句。

**例子**

```
Txns = kdb::execute(conn, "select * from txn")
```

### loadTable

**语法**

```
kdb::loadTable(conn, tablePath, [symPath])
```

**详情**

连接 kdb+ 数据库，通过 kdb+ 数据库加载数据，再将数据导入 DolphinDB 内存表。

在 kdb+ 数据库中，symbol 类型可以通过枚举存入 sym 文件，在表中使用 int 类型代替字符串进行存储，以减少字符串重复存储所占的空间。因此如果需要读取的表包含了枚举的 symbol 列，则需要读入 sym 文件才能正确读取表内的 symbol 列。

**参数**

**conn** `connect` 返回的连接句柄。

**tablePath** STRING 类型标量，表示需要读取的表文件路径。如果是 splayed table, partitioned table 或 segmented table，则指定为表文件目录；如果是 single object，则指定为表文件。

**symPath** STRING 类型标量，表示表文件对应的 sym 文件路径。为可选参数，默认为空。此参数省略时，必须保证表内不包含被枚举的 symbol 列。

**注意**：路径中建议使用'/'分隔。

**例子**

```
// 表中存在被枚举的 symbol 列
DATA_DIR="/path/to/data/kdb_sample"
Txns = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Txns", DATA_DIR + "/sym")

// 拓展表中不存在 symbol 类型，或者单张表中的 symbol 列未进行枚举
DATA_DIR="/path/to/data/kdb_sample"
Txns = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Txns", DATA_DIR)
```

### loadFile

**语法**

```
kdb::loadFile(tablePath, symPath)
```

**详情**

直接读取磁盘上的 kdb+ 数据文件，将其存入 DolphinDB 内存表。

在 kdb+ 数据库中，symbol 类型可以通过枚举存入 sym 文件，在表中使用 int 类型代替字符串进行存储，以减少字符串重复存储所占的空间。因此如果需要读取的表包含了被枚举的 symbol 列，则需要读入 sym 文件才能正确读取表内的 symbol 列。

**参数**

**tablePath** STRING 类型标量，表示需要读取的表文件路径。只能是 splayed table, partitioned table 或 segmented table 的表文件目录。

**symPath** STRING 类型标量，表示表文件对应的 sym 文件路径。此参数省略时，必须保证表内不包含被枚举的 symbol 列。

**注意**：路径中建议使用'/'分隔。

**例子**

```
//表中存在 symbol 类型，并进行了枚举
DATA_DIR="/path/to/data/kdb_sample"
Txns = kdb::loadFile(handle, DATA_DIR + "/2022.06.17/Txns", DATA_DIR + "/sym")

表中不存在 symbol 类型
DATA_DIR="/path/to/data/kdb_sample"
Txns = kdb::loadFile(handle, DATA_DIR + "/2022.06.17/Txns", DATA_DIR)
```

### loadTableEx

**语法**

```
kdb::loadTableEx(dbHandle, tableName, partitionColumns, conn, tablePath|qScript, [symPath], [schema], [batchSize=1024], [transform], [sortColumns])
```

**详情**

连接 kdb+ 数据库，通过 kdb+ 数据库加载数据，再将数据导入 DolphinDB 数据库中。

* 如果要将数据文件加载到分布式数据库中，必须指定 *tableName*，并且不能为空字符串。
* 如果要将数据文件加载到内存数据库中，那么 *tableName* 为空字符串或者不指定 *tableName*。

如果指定了 *transform* 参数，需要先创建分区表，再加载数据。系统会对数据文件中的数据执行 *transform* 参数指定的函数，再将得到的结果保存到数据库中。

**参数**

**dbHandle** 是数据库的句柄，可以是内存数据库或分布式数据库。

**tableName** STRING 类型标量，表示表的名称。

**partitionColumns** STRING 类型标量或向量，表示分区列。对于顺序分区类型的数据库，*partitionColumns* 为空字符串””。对于组合分区类型的数据库，*partitionColumns* 是字符串向量。

**conn** RESOURCE 类型标量，是 kdb+ 数据库的连接句柄。

**tablePath**|**qScript** STRING 类型标量，用于指定如何获取 kdb+数据库中的数据。

* **tablePath** 表示需要读取的表文件路径，适用于直接从kdb+数据库的表文件中加载数据。如果是 splayed table, partitioned table 或 segmented table，则指定为表文件目录；如果是 single object，则指定为表文件。注意：路径中建议使用 '/' 分隔。
* **qScript** 表示用于查询表内容的 kdb+ q 语言语句，适用于需要执行kdb+ q语言查询来获取数据。注意，如果不指定 *transform*，则 *qScript* 在 kdb+ 端的执行结果必须是一个表，否则会报错。

**symPath** STRING 类型标量，其具体含义取决于*tablePath|qScript* 参数的指定情况：

* 若指定 *tablePath*，*symPath* 表示表文件对应的 sym 文件路径。此时，若表内不包含被枚举的 symbol 列，该参数可以为空。
* 若指定 *qScript*，该参数无效。

**schema** 可选参数，是一个表，用于指定各列的数据类型。具体请参考 loadText 的 *schema* 参数。若不指定该参数，系统将会根据数据特征自动判断各列数据类型。

**batchSize** 可选参数，整型标量，默认值为 1024。会每次分批取 *batchSize* 大小的 kdb+ 表格数据写入 DolphinDB 直到所有数据写入完成。指定 *batchSize* 是为了避免所有数据都被加载进内存导致 OOM 的问题。

**transform** 可选参数，一元函数，导入到 DolphinDB 数据库前对 kdb+ 表进行自定义转换处理，例如替换表中的列。若不指定该参数，系统将会直接导入原始数据。

**sortColumns** 可选参数，STRING 类型标量或向量，用于指定每一分区内的排序列，写入的数据在每一分区内将按 *sortColumns* 进行排序。创建新表时，若 DolphinDB 数据库存储引擎为 TSDB 引擎，必须指定 *sortColumns* 参数。

```
DATA_DIR="/path/to/data/kdb_sample"
db = database(directory="dfs://rangedb", partitionType=RANGE, partitionScheme=0 51 101)
Txns = kdb::loadTableEx(db, `pt, `ID, handle, DATA_DIR + "/2022.06.17/Txns", DATA_DIR, 1000)
```

### loadFileEx

**语法**

```
kdb::loadFileEx(dbHandle, tableName, partitionColumns, tablePath, [symPath], [schema], [batchSize=1024], [transform], [sortColumns])
```

**详情**

读取磁盘上的 kdb+ 数据文件，将数据导入 DolphinDB 数据库中。

* 如果要将数据文件加载到分布式数据库中，必须指定 *tableName*，并且不能为空字符串。
* 如果要将数据文件加载到内存数据库中，那么 *tableName* 为空字符串或者不指定 *tableName*。

如果指定了 *transform* 参数，需要先创建分区表，再加载数据。系统会对数据文件中的数据执行 *transform* 参数指定的函数，再将得到的结果保存到数据库中。

**参数**

**dbHandle** 是数据库的句柄，可以是内存数据库或分布式数据库。

**tableName** STRING 类型标量，表示表的名称。

**partitionColumns** STRING 类型标量或向量，表示分区列。对于顺序分区类型的数据库，*partitionColumns* 为空字符串`""`。对于组合分区类型的数据库，*partitionColumns* 是字符串向量。

**tablePath** STRING 类型标量，可以表示需要读取的表文件路径。如果是 splayed table, partitioned table 或 segmented table，则指定为表文件目录；如果是 single object，则指定为表文件。注意：路径中建议使用 '/' 分隔。

**symPath** STRING 类型标量，表示需要读取的表文件对应的 sym 文件路径。该参数可以为空，此时必须保证表内不包含被枚举的 symbol 列。

**schema** 可选参数，是一个表，用于指定各列的数据类型。具体请参考 loadText 的 *schema* 参数。若不指定该参数，系统将会根据数据特征自动判断各列数据类型。

**batchSize** 可选参数，整型标量，默认值为 1024。会每次分批取 *batchSize* 大小的 kdb+ 表格数据写入 DolphinDB 直到写完所有数据。指定 *batchSize* 是为了避免所有数据都被加载进内存导致 OOM 的问题。

**transform** 可选参数，一元函数，导入到 DolphinDB 数据库前对 kdb+ 表进行转换，例如替换列。

**sortColumns** 可选参数，STRING 类型标量或向量，用于指定每一分区内的排序列，写入的数据在每一分区内将按 *sortColumns* 进行排序。创建新表时，若 DolphinDB 数据库存储引擎为 TSDB 引擎，必须指定 *sortColumns* 参数。

**例子**

```
DATA_DIR="/path/to/data/kdb_sample"
db = database(directory="dfs://rangedb", partitionType=RANGE, partitionScheme=0 51 101)
Txns = kdb::loadFileEx(db, `pt, `ID, DATA_DIR + "/2022.06.17/Txns", DATA_DIR, 1000)
```

### extractTableSchema

**语法**

```
kdb::extractTableSchema(conn, tablePath, [symPath])
```

**详情**

连接 kdb+ 数据库，通过 kdb+ 数据库获取需要加载的数据的 schema。返回一个表，包含三列 name、typeString、typeInt，代表列名、列类型以及列类型对应的 ID。

**参数**

**conn** RESOURCE 类型标量，是 kdb+ 数据库的连接句柄。

**tablePath** STRING 类型标量，表示需要获取 schema 的 kdb+ 表文件路径。

**symPath** 可选参数，STRING 类型标量，表示表文件对应的 sym 文件路径。

**例子**

```
DATA_DIR="/path/to/data/kdb_sample"
shcema = kdb::extractTableSchema(handle, DATA_DIR + "/2022.06.17/Txns")
```

### extractFileSchema

**语法**

`kdb::extractFileSchema(tablePath, [symPath])`

**详情**

读取磁盘上的 kdb+ 序列化文件，获取 schema。返回一个表，包含三列 name、typeString、typeInt，代表列名、列类型以及列类型对应的 ID。

**参数**

**tablePath** STRING 类型标量，表示需要获取 schema 的 kdb+ 表文件路径。

**symPath** 可选参数，STRING 类型标量，表示表文件对应的 sym 文件路径。

**例子**

```
DATA_DIR="/path/to/data/kdb_sample"
shcema = kdb::extractFileSchema(DATA_DIR + "/2022.06.17/Txns")
```

### close

**语法**

```
kdb::close(conn)
```

**详情**

关闭与 kdb+ 服务器建立的连接。

**参数**

**conn** `connect` 返回的连接句柄。

**例子**

```
kdb::close(conn)
```

### 使用示例

```
loadPlugin("/home/DolphinDBPlugin/kdb/build/PluginKDB.txt")
go
// 连接 kdb+ 数据库
handle = kdb::connect("127.0.0.1", 5000, "admin:123456")

// 指定文件路径
DATA_DIR="/home/kdb/data/kdb_sample"

// 通过 loadTable，加载数据到 DolphinDB
Daily = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Daily/", DATA_DIR + "/sym")
Minute = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Minute", DATA_DIR + "/sym")
Ticks = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Ticks/", DATA_DIR + "/sym")
Orders = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Orders", DATA_DIR + "/sym")
Syms = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Syms/", DATA_DIR + "/sym")
Txns = kdb::loadTable(handle, DATA_DIR + "/2022.06.17/Txns", DATA_DIR + "/sym")
kdb::close(handle)

// 直接读磁盘文件，加载数据到 DolphinDB
Daily2 = kdb::loadFile(DATA_DIR + "/2022.06.17/Daily", DATA_DIR + "/sym")
Minute2= kdb::loadFile(DATA_DIR + "/2022.06.17/Minute/", DATA_DIR + "/sym")
Ticks2 = kdb::loadFile(DATA_DIR + "/2022.06.17/Ticks/", DATA_DIR + "/sym")
Orders2 = kdb::loadFile(DATA_DIR + "/2022.06.17/Orders/", DATA_DIR + "/sym")
Syms2 = kdb::loadFile(DATA_DIR + "/2022.06.17/Syms/", DATA_DIR + "/sym")
Txns2 = kdb::loadFile(DATA_DIR + "/2022.06.17/Txns/", DATA_DIR + "/sym")
```

## 导入方法说明

### 通过 loadTable 导入

操作顺序：connect() -> loadTable() -> close()

注意事项：

1. 待导入的表中不应包含除 char 类型以外的 nested column。
2. loadTable 指定的加载路径应为单个表文件，或表路径（表为拓展表、分区表或分段表时）。

### 通过 loadFile 导入

操作顺序：loadFile()

注意事项：

1. 无法读取单个表（single object）。
2. 只能读取采用 gzip 压缩方法持久化的数据。
3. 待导入的表中不应包含除 char 类型以外的 nested column。
4. `loadFile` 指定的加载路径分区下的表路径。
5. 如果导入的表中存在 sorted、unique 、partitioned 、true index 等列属性，建议使用 `loadTable`，减少出错的可能

## kdb+ 各类表文件加载方式说明

分别说明 kdb+ 四种表文件的导入方式：

* 单张表（single object）

  只能使用 `loadTable` 导入。

  举例：

  ```
  目录结构：
  path/to/data
  ├── sym
  └── table_name
  ```

  ```
  handle = kdb::connect("127.0.0.1", 5000, "username:password");
  table = kdb::loadTable(handle, "path/to/data/table_name", "path/to/data/sym");
  ```
* 拓展表（splayed table）

  使用 `loadTable` 或 `loadFile` 导入。

  如果未压缩或使用 gzip 压缩，则推荐使用第二种方法，导入效率会更高。

  举例：

  ```
  目录结构：
  path/to/data
  ├── sym
  └── table_name
      ├── date
      ├── p
      └── ti
  ```

  ```
  handle = kdb::connect("127.0.0.1", 5000, "username:password");
  table1 = kdb::loadTable(handle, "path/to/data/table_name/", "path/to/data/sym");

  table2 = kdb::loadTable("path/to/data/table_name/", "path/to/data/sym");
  ```
* 分区表（partitioned table）

  本插件无法通过指定根目录，加载整个分区表、数据库。

  但是可以将 tablePath 指定为每个分区下的表，分别加载其中的数据，然后通过脚本在 DolphinDB 中组成一张完整的表。

  举例：

  ```
  目录结构：
  path/to/data
  ├── sym
  ├── 2019.01.01
  │   └── table_name
  │       ├── p
  │       └── ti
  ├── 2019.01.02
  │   └── table_name
  │       ├── p
  │       └── ti
  └── 2019.01.03
      └── table_name
          ├── p
          └── ti
  ```

  ```
  // 获取文件夹下的所有文件信息
  fileRes=files("path/to/data");

  // 删除 sym 条目，避免影响数据文件夹读取
  delete from fileRes where filename='sym';
  name='table_name';
  files = exec filename from fileRes;

  // 新建数据表，指定 schema
  table=table(10:0,`p`ti`date, [SECOND,DOUBLE,DATE])

  // 读取各个分区数据
  for (file in files) {
          t = kdb::loadFile("path/to/data" +'/' + file +'/' + tablename + '/');

          // 添加分区名所代表的数据
          addColumn(t, ["date"],[DATE])
          length=count(t)
          newCol=take(date(file), length)
          replaceColumn!(t, "date", newCol)

          // 追加数据到 table 中
          table.append!(t);
  }
  ```
* 分段表（segmented table）

  同 partitioned table，可以将各分段的各分区中的表读入，然后通过脚本在 DolphinDB 中组成一张完整的表。

## kdb+ 与 DolphinDB 数据类型转换表

**kdb+ 基本类型**

| kdb+ | DolphinDB | 字节长度 | 备注 |
| --- | --- | --- | --- |
| boolean | BOOL | 1 |  |
| guid | UUID | 16 |  |
| byte | CHAR | 1 | DolphinDB 中没有独立的 byte 类型，转换为长度相同的 CHAR |
| short | SHORT | 2 |  |
| int | INT | 4 |  |
| long | LONG | 8 |  |
| real | FLOAT | 4 |  |
| float | DOUBLE | 8 |  |
| char | CHAR | 1 | kdb+ 中 char 空值（""）当空格（" "）处理，因此不会转换为 DolphinDB CHAR 类型的空值 |
| symbol | SYMBOL | 4 |  |
| timestamp | NANOTIMESTAMP | 8 |  |
| month | MONTH | 4 |  |
| dat | DATE | 4 |  |
| datetime | TIMESTAMP | 8 |  |
| timespan | NANOTIME | 8 |  |
| minute | MINUTE | 4 |  |
| second | SECOND | 4 |  |
| time | TIME | 4 |  |

**kdb+ 其他类型**

* 由于 kdb+ 中常常使用 char nested list 存储字符串类型数据，因此 dolphindb kdb+ 插件支持了 char nested list 到 DolphinDB STRING 类型的转换。
* 对于其他类型的 nested list，将转换为对应类型的 arrayVector 类型。
* 对于 symbol 类型，由于 DolphinDB 内没有 STRING 类型的 arrayVector，因此会转换为 ANY vector。
* nested list 数据对应的 kdb+ 序列化文件可能存在无法判断数据类型的情况，这里也将会转换为 ANY vector。

| kdb+ | DolphinDB | 字节长度 | 备注 |
| --- | --- | --- | --- |
| char nested list | STRING | 不超过65535 | 转换为 STRING 而不是 CHAR[] |
| boolean nested list | BOOL[] |  |  |
| guid nested list | UUID[] |  |  |
| byte nested list | CHAR[] |  |  |
| short nested list | SHORT[] |  |  |
| int nested list | INT[] |  |  |
| long nested list | LONG[] |  |  |
| real nested list | FLOAT[] |  |  |
| float nested list | DOUBLE[] |  |  |
| symbol nested list | ANY |  |  |
| timestamp nested list | NANOTIMESTAMP[] |  |  |
| month nested list | MONTH[] |  |  |
| date nested list | DATE[] |  |  |
| datetime nested list | TIMESTAMP[] |  |  |
| timespan nested list | NANOTIME[] |  |  |
| minute nested list | MINUTE[] |  |  |
| second nested list | SECOND[] |  |  |
| time nested list | TIME[] |  |  |
