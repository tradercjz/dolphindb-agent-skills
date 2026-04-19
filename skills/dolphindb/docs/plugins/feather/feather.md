<!-- Auto-mirrored from upstream `documentation-main/plugins/feather/feather.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Feather

Apache Arrow Feather 文件采用列式存储格式，可用于高效存储与提取数据。DolphinDB 提供的 Feather 插件支持高效地将 Feather 文件导入 DolphinDB，或从 DolphinDB 导出 Feather 文件。在导入导出过程中会自动进行数据类型转换。本插件使用了 Arrow 的 [arrow 开源库](https://github.com/apache/arrow)的 feather 读写接口。

## 在插件市场安装插件

### 版本要求

DolphinDB Server: 2.00.10及更高版本。支持 Linux x86-64，Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("feather")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("feather")
   ```

## 接口说明

### extractSchema

**语法**

```
feather::extractSchema(filePath)
```

**详情**

读取 Feather 文件数据的表结构。返回一张包含三列的表，第一列 name 是列名，第二列 type 是 Arrow 的数据类型，第三列 DolphinDBType 是转换为 DolphinDB 的数据类型。
注意：如果 DolphinDBType 的某一行是 VOID，则说明 Feather 文件对应的列数据无法导入 DolphinDB。

**参数**

**filePath** STRING 类型标量，表示 Feather 文件路径。

**例子**

```
feather::extractSchema("path/to/data.feather");
feather::extractSchema("path/to/data.compressed.feather");
```

### load

**语法**

```
feather::load(filePath, [columns])
```

**详情**

将 Feather 文件数据加载到 DolphinDB 的内存表。Feather 文件中的 Arrow 数据类型与 DolphinDB 数据类型的转化规则，参见[数据类型](#%E6%94%AF%E6%8C%81%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B) 。

**注意**：

1. 由于 DolphinDB 整数类型的最小值表示空值，因此，Arrow int8, Arrow int16, Arrow int32, Arrow int64 类型对应的最小值无法导入 DolphinDB。
2. 浮点数的正负无穷、nan 值都会被转换为 DolphinDB 中的空值。

**参数**

**filePath** STRING 类型标量，表示 Feather 文件路径。

**columns** 可选参数，STRING 类型向量，表示要读取的列名集合。

**例子**

```
table = feather::load("path/to/data.feather");
table_part = feather::load("path/to/data.feather", [ "col1_name","col2_name"]);
```

### save

**语法**

```
feather::save(table, filePath, [compressMethod], [compressionLevel])
```

**详情**

将 *table* 以 Feather 格式保存到文件中。该函数会自动进行数据类型转换，关于 Feather 文件中的 Arrow 数据类型与 DolphinDB 数据类型的转化规则，参见[数据类型](#%E6%94%AF%E6%8C%81%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B) 。

**参数**

**table** 一个表对象。

**filePath** STRING 类型标量，表示保存的文件路径。

**compressMethod** 可选参数，STRING 类型标量，用于指定压缩类型。包含以下三种类型："uncompressed", "lz4", "zstd"，不区分大小写。默认开启 lz4 压缩方式。

**compressionLevel** 可选参数，整型标量，用于指定压缩级别。仅在 *compression*="zstd" 时有效。

**例子**

```
feather::save(table, "path/to/save/data.feather");
feather::save(table, "path/to/save/data.feather", "lz4");
feather::save(table, "path/to/save/data.feather", "zstd", 2);
```

**完整示例**

```
loadPlugin("feather")
feather::extractSchema("path/to/data.feather");
table = feather::load("path/to/data.feather");
table_part = feather::load("path/to/data.feather", [ "col1_name","col2_name"]);
feather::save(table, "path/to/save/data.feather");
feather::save(table, "path/to/save/data.feather", "lz4");
feather::save(table, "path/to/save/data.feather", "zstd", 2);
```

## 支持的数据类型

### 导入支持的数据类型

DolphinDB 导入 Feather 文件时，Arrow 与 DolphinDB 数据类型转换关系如下：

| Arrow | DolphinDB |
| --- | --- |
| bool | BOOL |
| int8 | CHAR |
| uint8 | SHORT |
| int16 | SHORT |
| uint16 | INT |
| int32 | INT |
| uint32 | LONG |
| int64 | LONG |
| uint64 | LONG |
| float | FLOAT |
| double | DOUBLE |
| string | STRING |
| date32 | DATE |
| date64 | TIMESTAMP |
| timestamp(ms) | TIMESTAMP |
| timestamp(ns) | NANOTIMESTAMP |
| time32(s) | SECOND |
| time32(ms) | TIME |
| time64(ns) | NANOTIME |

不支持转换以下 Arrow 类型：binary, fixed\_size\_binary, half\_float, timestamp(us), time64(us), interval\_months, interval\_day\_time, decimal128, decimal, decimal256, list, struct, sparse\_union, dense\_union, dictionary, map, extension, fixed\_size\_list, large\_string, large\_binary, large\_list, interval\_month\_day\_nano, max\_id

### 导出支持的数据类型

从 DolphinDB 导出 Feather 文件时，DolphinDB 与 Arrow 数据类型的对应关系如下：

| DolphinDB | Arrow |
| --- | --- |
| BOOL | bool |
| CHAR | int8 |
| SHORT | int16 |
| INT | int32 |
| LONG | int64 |
| DATE | date32 |
| TIME | time32(ms) |
| SECOND | time32(s) |
| TIMESTAMP | timestamp(ms) |
| NANOTIME | time64(ns) |
| NANOTIMESTAMP | timestamp(ns) |
| FLOAT | float |
| DOUBLE | double |
| STRING | string |
| SYMBOL | string |

不支持转换以下 DolphinDB 类型：MINUTE, MONTH, DATETIME, UUID, FUNCTIONDEF, HANDLE, CODE, DATASOURCE, RESOURCE, ANY, COMPRESS, ANY DICTIONARY, DATEHOUR, IPADDR, INT128, BLOB, COMPLEX, POINT, DURATION

### Python 读取 Feather 文件

本节介绍通过 Python 读取 Feather 文件时，可能遇到的问题，并给出了相应的解决方案：

1. Feather 文件中如果包含 time64(ns) 类型的数据，通过 `pyarrow.feather.read_feather()` 方法读取可能会报错 `Value XXXXXXXXXXXXX has non-zero nanoseconds`。这是因为 pyarrow.lib.Table 在转换为 DataFrame 时，time64(ns) 类型会被转换为 datetime.time 类型，而后者不支持纳秒精度的时间数据。建议使用 `pyarrow.feather.read_table()` 方法进行读取。
2. 通过 `pyarrow.feather.read_feather()` 读取的 Feather 文件若存在包含空值的整型列，则会把该整型列转成浮点类型。建议先将 Feather 读到 pyarrow table 里，通过指定 types\_mapper 转换类型。

   ```
   pa_table = feather.read_table("path/to/feather_file")
   df = pa_table.to_pandas(types_mapper={pa.int64(): pd.Int64Dtype()}.get)
   ```
