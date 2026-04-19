<!-- Auto-mirrored from upstream `documentation-main/plugins/hdf5/hdf5.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# HDF5

HDF5 (Hierarchical Data Format) 是一种常见的跨平台数据储存文件，可以表示非常复杂、异构的数据对象。DolphinDB 提供了 HDF5 插件，可以查看 HDF5 文件元数据，读写 HDF5 文件并自动转换数据类型。

## 在插件市场安装插件

### 版本要求

* DolphinDB Server: 2.00.10 及更高版本
* OS: x86-64 Linux, Windows

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   ```
   login("admin", "123456");
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("hdf5");
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("hdf5");
   ```

## 用户接口

### ls

**语法**

```
ls(fileName)
```

**参数**

**fileName** STRING 类型标量，HDF5 文件名。

**详情**

列出一个 HDF5 文件中的所有对象(数据集(dataset)和组(group))以及对象类型(objType)。在对象类型中，数据集会包括其列数及行数。例如 DataSet{(7,3)}代表 7 列 3 行。

**例子**

```
ls("/smpl_numeric.h5")
/*
output:
        objName	     objType
        --------------------
        /            Group
        /double	     DataSet{(7,3)}
        /float	     DataSet{(7,3)}
        /schar	     DataSet{(7,3)}
        /sint	     DataSet{(7,3)}
        /slong	     DataSet{(7,3)}
        /sshort	     DataSet{(7,3)}
        /uchar	     DataSet{(7,3)}
        /uint	     DataSet{(7,3)}
        /ulong	     DataSet{(1,1)}
        /ushort	     DataSet{(7,3)}
*/

ls("/named_type.h5")
/*
output:
        objName      objType
        ----------------------
        /            Group
        /type_name   NamedDataType
*/
```

### lsTable

**语法**

```
lsTable(fileName)
```

**参数**

**fileName** STRING 类型标量，HDF5 文件名。

**详情**

列出一个 HDF5 文件中的所有 table 信息，即 HDF5 数据集(dataset)对象信息，包括表名、列数及行数、表的类型。

**例子**

```
lsTable("/smpl_numeric.h5")

/*
output:
       tableName    tableDims	 tableType
       /double        7,3       H5T_NATIVE_DOUBLE
       /float	      7,3       H5T_NATIVE_FLOAT
       /schar	      7,3       H5T_NATIVE_SCHAR
       /sint	      7,3       H5T_NATIVE_INT
       /slong	      7,3       H5T_NATIVE_LLONG
       /sshort	      7,3       H5T_NATIVE_SHORT
       /uchar	      7,3       H5T_NATIVE_UCHAR
       /uint	      7,3       H5T_NATIVE_UINT
       /ulong	      1,1       H5T_NATIVE_ULLONG
       /ushort	      7,3       H5T_NATIVE_USHORT

*/
```

### extractHDF5Schema

**语法**

```
extractHDF5Schema(fileName, datasetName)
```

**参数**

**fileName** STRING 类型标量，HDF5 文件名。

**datasetName** STRING 类型标量，dataset 名称，即表名。可通过 ls 或 lsTable 获得。

**详情**

生成 HDF5 文件中指定数据集的结构，包括两列：列名和数据类型。

**例子**

```
extractHDF5Schema("/smpl_numeric.h5","sint")
/*
output:
        name	type
        col_0	INT
        col_1	INT
        col_2	INT
        col_3	INT
        col_4	INT
        col_5	INT
        col_6	INT
*/

extractHDF5Schema("/compound.h5","com")
/*
output:
        name	type
        fs	STRING
        vs	STRING
        d	DOUBLE
        t	TIMESTAMP
        l	LONG
        f	FLOAT
        i	INT
        s	SHORT
        c	CHAR
*/
```

### loadHDF5

**语法**

```
loadHDF5(fileName,datasetName,[schema],[startRow],[rowNum])
```

**参数**

**fileName** STRING 类型标量，HDF5 文件名。

**datasetName** STRING 类型标量，dataset 名称，即表名。可通过 ls 或 lsTable 获得。

**schema** 包含列名和列的数据类型的表。若要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为`loadHDF5`函数的一个参数。

**startRow** INT 类型标量，从哪一行开始读取 HDF5 数据集。若不指定，默认从数据集起始位置读取。

**rowNum** INT 类型标量，读取 HDF5 数据集的行数。若不指定，默认读到数据集的结尾。

**详情**

将 HDF5 文件中的指定数据集加载为 DolphinDB 数据库的内存表。读取的行数为 HDF5 文件中定义的行数，而不是读取结果中的 DolphinDB 表的行数。支持的数据类型，以及数据转化规则可见[数据类型](#%E6%94%AF%E6%8C%81%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B)章节。

**例子**

```
loadHDF5("/smpl_numeric.h5","sint")
/*
output:
        col_0	col_1	col_2	col_3	col_4	col_5	col_6
        (758)	8	(325,847)	87	687	45	90
        61	0	28	77	546	789	45
        799	5,444	325,847	678	90	54	0

scm = table(`a`b`c`d`e`f`g as name, `CHAR`BOOL`SHORT`INT`LONG`DOUBLE`FLOAT as type)
loadHDF5("../hdf5/h5file/smpl_numeric.h5","sint",scm,1,1)
/*
output:
        a	b	c	d	e	f	g
        '='	false	28	77	546	789	45
*/
```

> **请注意：数据集的 dataspace 维度必须小于等于 2。只有一维或二维表可以被解析。**

### loadPandasHDF5

**语法**

```
loadPandasHDF5(fileName,groupName,[schema],[startRow],[rowNum])
```

**参数**

**fileName** STRING 类型标量，由 Pandas 保存的 HDF5 文件名。

**groupName** STRING 类型标量，group 的标识符，即 key 名。

**schema** 包含列名和列的数据类型的表。若要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为 `loadPandasHDF5` 函数的一个参数。

**startRow** INT 类型标量，从哪一行开始读取 HDF5 数据集。若不指定，默认从数据集起始位置读取。

**rowNum** INT 类型标量，读取 HDF5 数据集的行数。若不指定，默认读到数据集的结尾。

**详情**

将由 Pandas 保存的 HDF5 文件中的指定数据表加载为 DolphinDB 数据库的内存表。读取的行数为 HDF5 文件中定义的行数，而不是读取结果中的 DolphinDB 表的行数。支持的数据类型，以及数据转化规则可见[数据类型](#%E6%94%AF%E6%8C%81%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B)章节。

**例子**

```
hdf5::loadPandasHDF5("../hdf5/h5file/data.h5","/s",,1,1)
/*
output:
        A	 B	C  D  E
        28 77	54 78 9
*/
```

### loadHDF5Ex

**语法**

```
loadHDF5Ex(dbHandle, tableName, [partitionColumns], fileName, datasetName, [schema], [startRow], [rowNum], [transform])
```

**参数**

**dbHandle** 数据库句柄

**tableName** STRING 类型标量，表名。

**partitionColumns** 字符串标量或向量，表示分区列。当分区数据库不是 SEQ 分区时，我们需要指定分区列。在组合分区中，partitionColumns 是字符串向量。

**fileName** HDF5 文件名，类型为字符串标量。

**datasetName** dataset 名称，即表名，可通过 ls 或 lsTable 获得，类型为字符串标量。

**schema** 包含列名和列的数据类型的表。如果我们想要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为`loadHDF5Ex`函数的一个参数。

**startRow** INT 类型标量，读取 HDF5 数据集的起始行位置。若不指定，默认从数据集起始位置读取。

**rowNum** INT 类型标量，读取 HDF5 数据集的行数。若不指定，默认读到数据集的结尾。

**transform** 一元函数，并且该函数接受的参数必须是一个表。如果指定了 transform 参数，需要先创建分区表，再加载数据，程序会对数据文件中的数据执行 transform 参数指定的函数，再将得到的结果保存到数据库中。

**详情**

将 HDF5 文件中的数据集转换为 DolphinDB 数据库的分布式表，然后将表的元数据加载到内存中。读取的行数为 HDF5 文件中定义的行数，而不是读取结果中的 DolphinDB 表的行数。支持的数据类型,以及数据转化规则可见[数据类型](#%E6%94%AF%E6%8C%81%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B)章节。

**例子**

* 磁盘上的 SEQ 分区表

```
db = database("seq_on_disk", SEQ, 16)
loadHDF5Ex(db,`tb,,"/large_file.h5", "large_table")
```

* 内存中的 SEQ 分区表

```
db = database("", SEQ, 16)loadHDF5Ex(db,`tb,,"/large_file.h5", "large_table")
```

* 磁盘上的非 SEQ 分区表

```
db = database("non_seq_on_disk", RANGE, 0 500 1000)
loadHDF5Ex(db,`tb,`col_4,"/smpl_numeric.h5","sint")
```

* 内存中的非 SEQ 分区表

```
db = database("", RANGE, 0 500 1000)
t0 = loadHDF5Ex(db,`tb,`col_4,"/smpl_numeric.h5","sint")
```

* 内存中的非 SEQ 分区表

```
db = database("", RANGE, 0 500 1000)
t0 = loadHDF5Ex(db,`tb,`col_4,"/smpl_numeric.h5","sint")
```

* 指定 transform 将数值类型表示的日期和时间(比如:20200101)转化为指定类型(比如:日期类型)

```
dbPath="dfs://DolphinDBdatabase"
db=database(dbPath,VALUE,2020.01.01..2020.01.30)
dataFilePath="/transform.h5"
datasetName="/SZ000001/data"
schemaTB=hdf5::extractHDF5Schema(dataFilePath,datasetName)
update schemaTB set type="DATE" where name="trans_time"
tb=table(1:0,schemaTB.name,schemaTB.type)
tb1=db.createPartitionedTable(tb,`tb1,`trans_time);
def i2d(mutable t){
    return t.replaceColumn!(`trans_time,datetimeParse(string(t.trans_time),"yyyyMMdd"))
}
t = hdf5::loadHDF5Ex(db,`tb1,`trans_time,dataFilePath,datasetName,,,,i2d)
```

### HDF5DS

**语法**

```
HDF5DS(fileName,datasetName,[schema],[chunkSize=1])
```

**参数**

**fileName** STRING 类型标量，HDF5 文件名。

**datasetName** STRING 类型标量，数据集名，即表名。可通过`ls`或`lsTable`获得。

**schema** 包含列名和列的数据类型的表。若要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型，并且把它作为`HDF5DS`函数的一个参数。

**chunkSize** INT 类型标量，需要生成的数据源数量。整个表会被均分为 dsNum 份。如果不指定，默认生成 1 个数据源。

**详情**

根据输入的文件名和数据集名创建数据源列表。

**例子**

```
ds = hdf5::HDF5DS(smpl_numeric.h5","sint")
size ds;
// output：1
ds[0];
// output：DataSource< loadHDF5("/smpl_numeric.h5", "sint", , 0, 3) >

ds = hdf5::HDF5DS(smpl_numeric.h5","sint",,3)
size ds;
// output：3
ds[0];
// output：DataSource< loadHDF5("/smpl_numeric.h5", "sint", , 0, 1) >
ds[1];
// output：DataSource< loadHDF5("/smpl_numeric.h5", "sint", , 1, 1) >
ds[2];
// output：DataSource< loadHDF5("/smpl_numeric.h5", "sint", , 2, 1) >
```

> **请注意：HDF5 不支持并行读入。以下例子是错误示范和正确示范**

错误示范

```
ds = HDF5DS("/smpl_numeric.h5", "sint", ,3)
res = mr(ds, def(x) : x)
```

正确示范，将 mr parallel 参数设为 false

```
ds = HDF5DS("/smpl_numeric.h5", "sint", ,3)
res = mr(ds, def(x) : x,,,false)
```

### saveHDF5

**语法**

```
saveHDF5(table, fileName, datasetName, [append=false], [maxStringLength=16])
```

**参数**

**table** 要保存的内存表。

**fileName** HDF5 文件名，类型为字符串标量。

**datasetName** STRING 类型标量，dataset 名称，即表名。可通过 ls 或 lsTable 获得。

**append** BOOL 类型标量，默认为 false。是否追加数据到已存在 dataset。

**maxStringLength** 字符串最大长度，类型为数值类型，默认为 16。仅对 table 中的 string 和 symbol 类型起作用。

**详情**

将 DolphinDB 数据库的内存表保存到 HDF5 文件中的指定数据集。支持的数据类型，以及数据转化规则可见[数据类型](#%E6%94%AF%E6%8C%81%E7%9A%84%E6%95%B0%E6%8D%AE%E7%B1%BB%E5%9E%8B)章节。
注意，目前 HDF5 插件无法存储列数过多的表格，如果列数超过 900 列则有可能会存储失败。

**例子**

```
saveHDF5(tb, "example.h5", "dataset name in hdf5")
```

## 支持的数据类型

浮点和整数类型会被先转换为 H5T\_NATIVE\_\*类型。

### integer

| Type in HDF5 | Default Value in HDF5 | Type in C | Type in DolphinDB |
| --- | --- | --- | --- |
| H5T\_NATIVE\_CHAR | ‘\0’ | signed char / unsigned char | char/short |
| H5T\_NATIVE\_SCHAR | ‘\0’ | signed char | char |
| H5T\_NATIVE\_UCHAR | ‘\0’ | unsigned char | short |
| H5T\_NATIVE\_SHORT | 0 | short | short |
| H5T\_NATIVE\_USHORT | 0 | unsigned short | int |
| H5T\_NATIVE\_INT | 0 | int | int |
| H5T\_NATIVE\_UINT | 0 | unsigned int | long |
| H5T\_NATIVE\_LONG | 0 | long | int/long |
| H5T\_NATIVE\_ULONG | 0 | unsigned long | long |
| H5T\_NATIVE\_LLONG | 0 | long long | long |
| H5T\_NATIVE\_ULLONG | 0 | unsigned long long | long |

* DolphinDB 中数值类型都为有符号类型。为了防止溢出，除 64 位无符号类型外，所有无符号类型会被转化为高一阶的有符号类型。特别的，64 位无符号类型转化为 64 位有符号类型，若发生溢出则返回 64 位有符号类型的最大值。
* H5T\_NATIVE\_CHAR 对应 C 中的 char 类型，而 char 是否有符号依赖与编译器及平台。若有符号依赖，则在 DolphinDB 中转化为 char，否则为 short。
* H5T\_NATIVE\_LONG 以及 H5T\_NATIVE\_ULONG 对应 C 中的 long 类型。
* 所有整数类型皆可以转化为 DolphinDB 中的数值类型(bool, char, short, int, long, float, double)，若进行转化会发生溢出。例如 LONG->INT 会返回一个 int 的最值。

### float

| Type in HDF5 | Default Value in HDF5 | Type in C | Type in DolphinDB |
| --- | --- | --- | --- |
| H5T\_NATIVE\_FLOAT | +0.0f | float | float |
| H5T\_NATIVE\_DOUBLE | +0.0 | double | double |

注意：IEEE754 浮点数类型皆为有符号数。

* 所有浮点数类型皆可以转化为 DolphinDB 中的数值类型(bool, char, short, int, long, float, double)，若进行转化会发生溢出。例如 DOUBLE->FLOAT 会返回一个 float 的最值。

### time

| type in hdf5 | Default Value in HDF5 | corresponding c type | corresponding dolphindb type |
| --- | --- | --- | --- |
| H5T\_UNIX\_D32BE | 1970.01.01T00:00:00 | 4 bytes integer | DT\_TIMESTAMP |
| H5T\_UNIX\_D32LE | 1970.01.01T00:00:00 | 4 bytes integer | DT\_TIMESTAMP |
| H5T\_UNIX\_D64BE | 1970.01.01T00:00:00.000 | 8 bytes integer | DT\_TIMESTAMP |
| H5T\_UNIX\_D64LE | 1970.01.01T00:00:00.000 | 8 bytes integer | DT\_TIMESTAMP |

* HDF5 预定义的时间类型为 32 位或者 64 位的 posix 时间。HDF5 的时间类型缺乏官方的定义，在此插件中，32 位时间类型代表距离 1970 年的秒数，而 64 位则精确到毫秒。所有时间类型会被插件统一转化为一个 64 位整数，然后转化为 DolphinDB 中的 timestamp 类型。
* 以上类型皆可以转化为 DolphinDB 中的时间相关类型(date, month, time, minute, second, datetime, timestamp, nanotime, nanotimestamp)。

### string

| type in hdf5 | Default Value in HDF5 | corresponding c type | corresponding dolphindb type |
| --- | --- | --- | --- |
| H5T\_C\_S1 | “” | char\* | DT\_STRING |

* H5T\_C\_S1 包括固定长度(fixed-length)字符串和可变长度(variable-length)字符串。
* string 类型可以转化为 DolphinDB 中的字符串相关类型(string, symbol)。

### enum

| type in hdf5 | corresponding c type | corresponding dolphindb type |
| --- | --- | --- |
| ENUM | enum | DT\_SYMBOL |

* 枚举类型会被转化为 DolphinDB 中的一个 symbol 变量。请注意，每个字符串所对应的枚举值以及大小关系并不会被保存。例如，枚举类型 HDF5\_ENUM{"a"=100，"b"=2000,"c"=30000}可能会被转化为 SYMBOL{"a"=3,"b"=1"c"=2}。
* enum 类型可以转化为 DolphinDB 中的字符串相关类型(string, symbol)。

### compound and array

| type in hdf5 | corresponding c type | corresponding dolphindb type |
| --- | --- | --- |
| H5T\_COMPOUND | struct | \ |
| H5T\_ARRAY | array | \ |

* 复合(compound)类型以及数组(array)类型只要不包含不支持的类型，就可以被解析，而且支持嵌套。
* 复杂类型的转化取决于其内部子类型。

## 表结构

### 简单类型

简单类型导入 DolphinDB 后的 table 与 HDF5 文件中的 table 完全一致。

#### HDF5 中的简单类型表

|  | 1 | 2 |
| --- | --- | --- |
| 1 | int(10) | int(67) |
| 2 | int(20) | int(76) |

#### 导入 DolphinDB 后的简单类型表

|  | col\_1 | col\_2 |
| --- | --- | --- |
| 1 | 10 | 67 |
| 2 | 20 | 76 |

### 复杂类型

复杂类型导入 DolphinDB 后的类型取决于复杂类型的结构。

#### HDF5 中的复合类型表

|  | 1 | 2 |
| --- | --- | --- |
| 1 | struct | struct |
| 2 | struct | struct |

导入 DolphinDB 后：

|  | a | b | c |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 3.7 |
| 2 | 11 | 21 | 31.7 |
| 3 | 12 | 22 | 32.7 |
| 4 | 13 | 23 | 33.7 |

#### HDF5 中的数组类型表

|  | 1 | 2 |
| --- | --- | --- |
| 1 | array(1,2,3) | array(4,5,6) |
| 2 | array(8,9,10) | array(15,16,17) |

导入 DolphinDB 后：

|  | array\_1 | array\_2 | array\_3 |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 3 |
| 2 | 4 | 5 | 6 |
| 3 | 8 | 9 | 10 |
| 4 | 15 | 16 | 17 |

#### HDF5 中的嵌套类型表

对嵌套的复杂类型，结果中会添加'A'前缀代表数组，'C'前缀代表复合类型。

|  | 1 | 2 |
| --- | --- | --- |
| 1 | struct{a:array(1,2,3) b:2 c:struct{d:"abc"}} | struct{a:array(7,8,9) b:5 c:struct{d:"def"}} |
| 2 | struct{a:array(11,21,31) b:0 c:struct{d:"opq"}} | struct{a:array(51,52,53) b:24 c:struct{d:"hjk"}} |

导入 DolphinDB 后：

|  | Aa\_1 | Aa\_2 | Aa\_3 | b | Cc\_d |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | 2 | abc |
| 2 | 7 | 8 | 9 | 5 | def |
| 3 | 11 | 21 | 31 | 0 | opq |
| 4 | 51 | 52 | 53 | 24 | hjk |

## 性能

### 环境

* CPU: i7-7700 3.60GHZ
* SSD: 连续读取 最多每秒 460~500MB

### 数据集导入性能

* 单一类型(int)
  + 行数 1024 \* 1024 \* 16
  + 列数 64
  + 文件大小 4G
  + 耗时 8 秒
* 单一类型(unsigned int)
  + 行数 1024 \* 1024 \* 16
  + 列数 64
  + 文件大小 4G
  + 耗时 9 秒
* 单一类型(variable-length string)
  + 行数 1024 \* 1024
  + 列数 64
  + 文件大小 3.6G
  + 耗时 17 秒
* 复合类型
  + 子类型共 9 列：(str,str,double,int,long,float,int,short,char)
  + 行数 1024 \* 1024 \* 62
  + 文件大小 3.9G
  + 耗时 10 秒
* 数组复合类型
  + 子类型共 72 列：(str,str,double,int,long,float,int,short,char) \* 8
  + 行数 1024 \* 128 \* 62
  + 文件大小 3.9G
  + 耗时 15 秒
