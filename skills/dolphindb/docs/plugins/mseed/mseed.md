<!-- Auto-mirrored from upstream `documentation-main/plugins/mseed/mseed.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# mseed

miniSEED 是SEED 格式的子集，一般用于地震学时间序列数据的归档和交换。DolphinDB 的 mseed 插件可以读取 miniSEED 文件的数据到 DolphinDB 的内存表中，且可以将 DolphinDB 的一段连续时间的采样值写入到 miniSEED 格式的文件中。本插件使用了 IRIS 的 [libmseed 开源库](https://github.com/iris-edu/libmseed) 的读写接口。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本，支持 Linux x86-64, Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   **注意**：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("mseed")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("mseed")
   ```

## 接口说明

### read

**语法**

```
read(filePath)
```

**详情**

读取一个 miniSEED 文件。

返回一个内存表，包含如下字段：

* value：列类型为 INT, FLOAT 或 DOUBLE，读取到的采样值。
* time：列类型为 TIMESTAMP，采样值对应的时间戳。
* id：列类型为 SYMBOL，采样值所在块的 sid。

**参数**

**filePath** STRING 类型标量，表示需要读取的 miniSEED 文件所在的绝对路径。

**例子**

```
ret=read("<FileDir>/SC.JZG.00.BHZ.D.2013.001");
```

### write

**语法**

```
write(filePath, sid, startTime, sampleRate, value, [overwrite=false])
```

**详情**

将一段连续的采样值写入到 miniSEED 文件。

返回一个布尔标量，返回 true 时表示是否成功写入。

**参数**

**filePath** STRING 类型标量，表示需要写入的 miniSEED 文件所在的绝对路径。

**sid** STRING 类型标量，表示写入到 miniSEED 文件的一个块的 sid。

**startTime** TIMESTAMP 类型标量，表示写入到 miniSEED 文件一个块的 startTime。

**sampleRate** INT, LONG, FLOAT 或 DOUBLE 类型标量，表示写入到 miniSEED 文件的 sampleRate。

**value** INT, FLOAT, DOUBLE 类型向量，写入 miniSEED 文件的采样值的向量。

**overwrite** BOOL 类型标量，表示是否覆盖之前写入的数据。默认为 false，代表不覆盖。

**例子**

```
time=timestamp(2013.01.01);
sampleRate=100.0;
vec=rand(100, 100);
ret=write("/home/zmx/aaa", "XFDSN:SC_JZG_00_B_H_Z", time, sampleRate, vec);
```

### parse

**语法**

```
parse(data)
```

**详情**

解析 miniseed 格式的字节流。

返回一个内存表，包含如下字段：

* value：列类型为 INT, FLOAT 或 DOUBLE，读取到的采样值。
* time：列类型为 TIMESTAMP，采样值对应的时间戳。
* id：列类型为 SYMBOL，采样值所在块的 sid。

**参数**

**data** STRING 或 CHAR 类型的向量，表示 miniseed 格式的字节流。

**例子**

```
fin=file("/media/zmx/aaa");
buf=fin.readBytes(512);
ret=parse(buf);

stringBuf=concat(buf);
ret=parse(stringBuf);
```

### parseStream

**语法**

```
parseStream(data)
```

**详情**

解析 miniseed 格式的字节流，返回一个字典，包含一个内存表和成功解析的字节流长度。如果解析失败，返回一个仅包含成功解析的字节流长度的字典。字典包含如下键值:

* "data"： 一个内存表，包含如下字段：
  + value：列类型为 INT, FLOAT 或 DOUBLE，读取到的采样值。
  + time：列类型为 TIMESTAMP，采样值对应的时间戳。
  + id：列类型为 SYMBOL，采样值所在块的 sid。
* "size"：LONG 类型标量，表示成功解析的字节流的长度。
* "metaData"： 一个内存表，包含如下字段
  + id：列类型为 SYMBOL，采样值所在块的 sid。
  + startTime：列类型为 TIMESTAMP，采样开始时间。
  + receivedTime：列类型为 TIMESTAMP，接收数据时间。
  + actualCount：列类型为 INT，实际解析出来的数据个数。
  + expectedCount：列类型为 INT，miniSEED 包头指定的采样值个数。
  + sampleRate：列类型为 DOUBLE，miniSEED 采样率。

**参数**

**data** STRING 或 CHAR 类型的向量，表示 miniseed 格式的字节流。

**例子**

```
fin=file("/media/zmx/aaa");
buf=fin.readBytes(512);
ret=parseStream(buf);

stringBuf=concat(buf);
ret=parseStream(stringBuf);
```

### parseStreamInfo

**语法**

```
parseStreamInfo(data)
```

**详情**

解析 miniseed 格式的字节流的块信息，返回一个字典，包含一个内存表和成功解析的字节流长度。

字典包含如下键值:

* "data":
  一个内存表，包含如下字段：
  + sid：列类型为 STRING 类型，读取到的 mseed 块的分量名称。
  + blockLen：列类型为 INT，读取到的 mseed 块的长度。
* "size":
  INT 类型标量，表示成功解析的字节流的长度。

**参数**

**data** STRING 或 CHAR 类型的向量，表示 miniseed 格式的字节流。

**例子**

```
fin=file("/media/zmx/aaa");
buf=fin.readBytes(512);
ret=parseStreamInfo(buf);

stringBuf=concat(buf);
ret=parseStreamInfo(stringBuf);
```

### streamize

**语法**

```
streamize(data, sampleRate, [blockSize])
```

**详情**

按照所在行数的顺序将表中的采样数据转换成 miniseed 格式的 CHAR Vector。需要提前对 sid 列、时间戳进行排序。

**参数**

**data** 采样数据信息的一张表，必须包含如下列：

* 第一列类型为 SYMBOL 或 STRING，表示 sid。
* 第二列类型为 TIMESTAMP，表示时间戳。
* 第三列类型为 INT, FLOAT 或 DOUBLE，表示采样数值。
* 只会取前三列作为输入参数，第四列及其以后不做处理。

**sampleRate** INT, LONG, FLOAT, DOUBLE 类型标量，表示采样频率。

**blockSize** INT 类型标量，表示 miniSEED 格式的块大小，单位为字节。默认值是 512。

**例子**

```
sidVec = take("XFDSN:SN_C0059_40_E_I_E", 1000).symbol()
tsVec = now() + 1..1000
dataVec = 1..1000
data = table(sidVec as sid, tsVec as ts, dataVec as data)
ret = streamize(data, 1000)
```
