<!-- Auto-mirrored from upstream `documentation-main/plugins/hdfs/hdfs.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# HDFS

HDFS 是 Hadoop 的分布式文件系统（Hadoop Distributed File System），实现大规模数据可靠的分布式读写。DolphinDB 提供了 HDFS 插件，支持从 Hadoop 的 HDFS 之中读取文件的信息。目前支持从 HDFS 上读取 Parquet 或者 ORC 格式文件并写入 DolphinDB 内存表；同时支持将 DolphinDB 内存表以特定格式保存至 HDFS 中。

## 准备工作

执行 Linux 命令，指定插件运行时需要的动态库路径，注意必须在设置完共享库查找路径后再启动 DolphinDB。

1. 安装 JAVA 环境

   ```
   yum install java
   yum install java-1.8.0-openjdk-devel
   ```
2. 寻找系统的 libjvm.so，选择要使用的 JAVA 版本。

   ```
   find /usr/-name "libjvm.so" // 寻找 JAVA 环境
   export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.362.b08-1.el7_9.x86_64 // 需要更改为实际的 java 路径
   export LD_LIBRARY_PATH=$JAVA_HOME/jre/lib/amd64/server:$LD_LIBRARY_PATH // 指定查找共享库的路径，确保 DolphinDB 启动时可以找到 jvm 库
   ```
3. 下载 [hadoop-3.2.2](https://archive.apache.org/dist/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz) 并解压。

   ```
   cd hadoop-3.2.2
   tar -zxvf hadoop-3.2.2.tar.gz
   export HADOOP_PREFIX=/hdd1/DolphinDBPlugin/hadoop-3.2.2 // 需要设置为实际路径
   export CLASSPATH=$($HADOOP_PREFIX/bin/hadoop classpath --glob):$CLASSPATH
   export LD_LIBRARY_PATH=$HADOOP_PREFIX/lib/native:$LD_LIBRARY_PATH
   ```

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本。支持 Linux x86-64, Linux JIT。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("hdfs")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("hdfs")
   ```

## 接口说明

### connect

**语法**

```
hdfs::connect(nameNode, [port], [username], [kerbTicketCachePath], [keytabPath], [principal], [lifetime])
```

**详情**

创建和 HDFS 的连接，返回一个连接句柄。如果建立连接失败则会抛出异常。

**参数**

**nameNode** STRING 类型标量，是 HDFS 所在的 IP 地址。如果 HSFS 在本地，可以使用 “localhost”， 也可以填完整的集群地址。如果在这个参数中填写了完整的集群地址，则不需要再填写端口号，因为它会使用 hadoop 的集群配置项 fs.defaultFS 的值。

**port** 整型标量，可选，HDFS 开放的端口号，如果是本地，一般为 9000。如果 *nameNode* 填写的是完整的 HDFS server 地址，则不需要填写该参数。

**username** STRING 类型标量，可选，是登录的用户名。

**kerbTicketCachePath** STRING 类型标量，可选，连接到 HDFS 时要使用的 Kerberos 路径。为 HDFS 集群配置项的 hadoop.security.kerberos.ticket.cache.path 的值。
如果没有指定 *keytabPath*, *principal* 和 *lifetime*，则该位置是已经生成的 ticket 的路径。
如果指定 *keytabPath*, *principal* 和*lifetime*，则该路径是需要生成的 ticket 存储的路径。

**keytabPath** STRING 类型标量，可选，kerberos 认证过程中用于验证获得票据的 keytab 文件所在路径。

**principal** STRING 类型标量，可选，kerberos 认证过程中需要验证的 principal。

**lifetime** STRING 类型标量，可选，是生成的票据的生存期，D 代表天，H 代表小时，M 代表分钟，S 代表秒。"4h5m" 代表 4 小时 5 分钟，"1d2s" 表示 1 天 2 秒。默认生存期为 1 天。

**示例**

```
// 连接普通的 HDFS
conn=hdfs::connect("default",9000);

// 连接 kerberos 认证的 HDFS
keytabPath = "/path_to_keytabs/node.keytab"
cachePath = "/path_to_krb5Cache/cache"
principal = "user/example.com@DOLPHINDB.COM"
lifetime = "1d3h"
connKerb5=hdfs::connect(`kerb5_url, 9001, , cachePath, keytabPath, principal, lifetime)
```

### disconnect

**语法**

```
disconnect(conn)
```

**详情**

用以取消已经建立的连接。

**参数**

**conn** `connect` 函数返回的句柄。

### exists

**语法**

```
exists(conn, path)
```

**详情**

判断指定的路径（*path*）是否存在。如果不存在则报错。

**参数**

**conn** `connect` 函数返回的句柄。

**path** STRING 类型标量，表示一个 HDFS 系统中的路径。

### copy

**语法**

```
copy(sourceConn, sourcePath, targetConn, targetPath)
```

**详情**

将一个 HDFS 中指定路径的文件拷贝到另一 HDFS 的指定路径之中。如果拷贝失败则报错。

**参数**

**sourceConn** `connect` 函数返回的句柄。

**sourcePath** STRING 类型标量，是源文件的路径。

**targetConn** `connect` 函数返回的句柄。

**targetPath** STRING 类型标量，目标文件的路径。

### move

**语法**

```
move(sourceConn,sourcePath,targetConn,targetPath)
```

**详情**

将一个 HDFS 中指定路径的文件移动到另一 HDFS 的指定路径之中。如果移动失败则报错。

**参数**

**sourceConn** `connect` 函数返回的句柄。

**sourcePath** STRING 类型标量，表示源文件的路径。

**targetConn** `connect` 函数返回的句柄。

**targetPath** STRING 类型标量，表示目标文件的路径。

### delete

**语法**

```
delete(conn, path, recursive)
```

**详情**

删除指定目录或文件。如果删除失败则报错。

**参数**

**conn** `connect` 函数返回的句柄。

**path** STRING 类型标量，表示一个文件路径。

**recursive** INT 类型标量，表示是否递归删除目录。*path* 是一个文件夹时，如果该参数非 0，则 *recursive* 下的文件会被递归删除；否则，会出现报错。

### rename

**语法**

```
rename(conn, sourcePath, targetPath)
```

**详情**

将文件重命名，或移动文件。如果重命名或移动失败则报错。

**参数**

**conn** `connect` 函数返回的句柄。

**sourcePath** STRING 类型标量，表示重命名之前的文件路径。

**targetPath** STRING 类型标量，表示重命名之后的文件路径。

* 如果路径（*targetPath*）已经存在并且是一个目录，源文件（*sourcePath*中的文件）将被移动到其中。
* 如果路径（*targetPath*）存在并且是一个文件，或者缺少父级目录，则会报错。

### createDirectory

**语法**

```
createDirectory(conn, path)
```

**详情**

创建一个空文件夹。如果创建失败则报错。

**参数**

**conn** `connect` 函数返回的句柄。

**path** STRING 类型标量，表示文件夹的路径。

### chmod

**语法**

```
chmod(conn, path, mode)
```

**详情**

修改指定文件或指定文件夹的使用权限。如果修改失败则报错。

**参数**

**conn** `connect` 函数返回的句柄。

**path** STRING 类型标量，表示想要修改权限的文件路径。

**mode** INT 类型标量，表示希望修改为的权限值。

### getListDirectory

**语法**

```
getListDirectory(conn, path)
```

**详情**

返回一个包含目标目录所有信息的句柄。

**参数**

**conn** connect 函数返回的句柄。

**path** STRING 类型标量，表示目标目录。

### listDirectory

**语法**

```
listDirectory(dirHandle)
```

**详情**

列出目标目录下所有文件的详细信息。

**参数**

**dirHandle** `getListDirectory` 函数返回的句柄。

### freeFileInfo

**语法**

```
freeFileInfo(dirHandle)
```

**详情**

释放目录信息所占用的空间。

**参数**

**dirHandle** `getListDirectory` 函数返回的句柄.

### readFile

**语法**

```
readFile(conn, path, handler)
```

**详情**

从 HDFS 服务器中读取数据，并通过 *handler* 处理数据后写入 DolphinDB 的内存表并返回该内存表。

**参数**

**conn** `connect` 函数返回的句柄。

**path** 是想要读取的文件所在的路径。

**handler** 一个二元函数，第一个参数是文件字节流的 buf 地址，第二个参数是文件的长度。用于将 HDFS 中的文件反序列化为 DolphinDB 的 table。`readFile` 函数从 HDFS 中读取文件之后将文件的内容保存到 buf 指向的 buffer 中，并且缓存内容的长度。*handler* 根据长度从 buffer 读取内容，进行反序列化，并保存到 DolphinDB 内存表中。
目前 *handler* 仅支持 orc 插件中的 `orc::loadORCHdfs` 和 parquet 插件中的 `parquet::loadParquetHdfs`。如果需要序列化 HDFS 中其他格式文件，则需要定制开发。

**示例**

```
// 安装并加载 ORC 插件
installPlugin("orc");
loadPlugin("orc");

// 使用其中的 orc::loadORCHdfs 函数读取存在 HDFS 系统上的 ORC 格式的文件
re=hdfs::readFile(conn,'/tmp/testFile.orc',orc::loadORCHdfs)
```

### writeFile

**语法**

```
writeFile(conn, path, table, handler)
```

**详情**

将 DolphinDB 内存表以特定格式保存在 HDFS 中。

**参数**

**conn** `connect` 函数返回的句柄。

**path** 是想要读取的文件所在的路径。

**table** 要保存的内存表。

**handler** 一个一元函数，其参数是 DolphinDB 内存表。*handler* 的返回值是一个向量，第一个元素是序列化后的 buffer 地址，第二个元素是 buffer 中内容的长度。它用于将 DolphinDB 的内存表序列化成字节流，并保存到 HDFS 文件中。它是 `readFile` 中的 *handle* 的反操作。`writeFile` 函数会先调用 *handler* 将 *tb* 进行序列化，并获取 buffer 地址和长度，然后将 buffer 中的内容写入 HDFS 中的 buffer 里。

目前 *handler* 只支持 parquet 插件中的 `parquet::saveParquetHdfs` 函数，如果将内存表保存为其它数据格式，则需要定制开发。

**示例**

```
// 安装并加载 Parquet 插件
installPlugin("parquet")
loadPlugin("parquet")

// 使用其中的 parquet::saveParquetHdfs 函数将内存表以 Parquet 格式写入给定的 HDFS 路径
hdfs::writeFile(conn,'/tmp/testFile.parquet',re,parquet::saveParquetHdfs)
```

## 完整示例

```
// 加载 HDFS 插件
loadPlugin("hdfs")

// 连接 HDFS server
fs=hdfs::connect("default",9000);

// 判断指定的路径是否存在
hdfs::exists(fs,"/user/name");
hdfs::exists(fs,"/user/name1");

// 复制文件进行备份
hdfs::copy(fs,"/tmp/testFile.txt",fs,"/tmp/testFile.txt.bk");
hdfs::copy(fs,"/tmp/testFile1.txt",fs,"/tmp/testFile.txt.bk");

// 移动文件
hdfs::move(fs,"/tmp/testFile.txt.bk",fs,"/user/name/input/testFile.txt");
hdfs::move(fs,"/user/name/input/testFile.txt",fs,"/user/name1/testFile.txt");

// 将文件进行重命名
hdfs::rename(fs,"/user/name1/testFile.txt","/user/name1/testFile.txt.rename");

// 创建一个空文件夹
hdfs::createDirectory(fs,"/user/name");

// 修改权限为 600
hdfs::chmod(fs,"/user/name",600);

// 删除创建的文件夹
hdfs::delete(fs,"/user/name",1);

// 获取包含目标目录所有信息的句柄
fileInfo=hdfs::getListDirectory(fs,"/user/name/input/");

// 列出目标目录下所有文件的详细信息
hdfs::listDirectory(dirHandle);

// 用来释放目录信息所占用的空间
hdfs::freeFileInfo(dirHandle);

// 将原本存在 HDFS 系统上的 ORC 格式的文件读到内存表中
loadPlugin("orc")
re=hdfs::readFile(conn,'/tmp/testFile.orc',orc::loadORCHdfs)

// 将内存表以 Parquet 格式写入给定的 HDFS 路径
loadPlugin("parquet")
hdfs::writeFile(conn,'/tmp/testFile.parquet',re,parquet::saveParquetHdfs)

// 断开 HDFS 的连接
hdfs::disconnect(fs);
```
