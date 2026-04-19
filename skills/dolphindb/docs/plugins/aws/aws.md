<!-- Auto-mirrored from upstream `documentation-main/plugins/aws/aws.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# AWS

Amazon S3 是一种云存储服务，可以存储和检索大量数据。通过 DolphinDB 的 AWS 插件，用户可以与 Amazon S3 服务进行交互，将数据备份到云端或者从云端下载数据。

本插件依赖第三方库 libaws-cpp-sdk-core.so libaws-cpp-sdk-s3.so 以及 libcurl.so。

## 安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux x64, Windows x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("aws")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("aws")
   ```

## 接口说明

### listS3Object

**语法**

```
aws::listS3Object(account, bucket, prefix, [marker],[delimiter], [nextMarker], [maxKeys])
```

**详情**

列出 S3 中指定路径下的所有对象及相关属性。所有匹配对象的属性表，包括：

* index：索引号。
* bucket name：桶名。
* key name：对象名。
* last modified：最近一次修改时间，日期格式为 ISO\_8601。
* length：对象大小，单位为byte。
* ETag：标记。
* owner：所有者。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

* 账户信息包括：id, key，region 以及 endpoint。
* 连接配置包括：
  + requestTimeoutMs，可选，整数类型。表示请求超时时间，如果传输大量数据失败可以尝试调大该数值。

创建账户信息的字典说明如下：

* 连接公有云，此时需要提供 id key region：

  ```
  account=dict(string,string);
  account['id']=your_access_key_id;
  account['key']=your_secret_access_key;
  account['region']=your_region;
  ```
* 连接私有云，此时需要提供 id key endpoint isHttp：

  ```
  account=dict(STRING,ANY)
  account['id']="minioadmin";
  account['key']="minioadmin"
  account['endpoint'] = "127.0.0.1:9000";       //注意，endpoint中不能包含http://以及https://
  account['isHttp'] = true;
  ```
* 注意，若无法通过验证或 SSL 出错，可以尝试指定证书：

  ```
  account['caPath']=your_ca_file_path;     //e.g. '/etc/ssl/certs'
  account['caFile']=your_ca_file;          //e.g. 'ca-certificates.crt'
  account['verifySSL']=verify_or_not;      //e.g. false
  ```

**bucket** STRING 类型的标量，表示访问的桶名称。

**prefix** STRING 类型的标量，表示访问路径的前缀，可以传空字符串。

**marker** STRING 类型标量，可选参数，表示返回这个值以后的对象。

**delimiter** STRING 类型标量，可选参数，表示用于对键进行分组的字符。

**nextMarker** STRING 类型标量，可选参数，输出参数，表示可用于获取下一组对象的 marker。

**maxKeys** LONG 类型标量，可选参数，设置响应中返回的最大 key 数量，默认是 1000。

### getS3Object

**语法**

```
aws::getS3Object(account, bucket, key, [outputFile])
```

**详情**

获取 S3 中指定的一个对象，返回本地对象的文件名。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**key** STRING 类型的标量，表示对象名。

**outputFile** STRING 类型的标量，表示输出对象的文件名，可选参数，默认同访问的对象名 Key。

### readS3Object

**语法**

```
aws::readS3Object(account, bucket, key, offset, length)
```

**详情**

获取 S3 中指定对象的部分内容。返回由对象指定部分的内容构成的字符向量。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**key** STRING 类型的标量，表示对象名。

**offset** LONG 类型的标量，表示偏移量，即想要获取的内容的起始位置。

**length** LONG 类型的标量，表示长度，即想要获取的内容的长度，单位是 byte。

### deleteS3Object

**语法**

```
aws::deleteS3Object(account, bucket, key)
```

**详情**

删除 S3 中的指定对象（警告：删除操作无法撤销）。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**key** STRING 类型的标量，表示对象名。

### uploadS3Object

**语法**

```
aws::uploadS3Object(account, bucket, key, inputFile)
```

**详情**

向 S3 上传一个对象。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**key** STRING 类型的标量，表示对象名。

**inputFile** STRING 类型的标量，表示准备上传的对象的路径及名称。

### listS3Bucket

**语法**

```
aws::listS3Bucket(account)
```

**详情**

列出 S3 指定账户下的所有桶及创建的时间。包含所有桶名字和对应创建时间的表，时间的格式是 ISO\_8601。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

### deleteS3Bucket

**语法**

```
aws::deleteS3Bucket(account, bucket)
```

**详情**

删除 S3 中指定的桶（警告：删除操作无法撤销）。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

### createS3Bucket

**语法**

```
aws::createS3Bucket(account, bucket)
```

**详情**

创建一个桶。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

### loadS3Object

**语法**

```
aws::loadS3Object(account, bucket, key, threadCount, dbHandle, tableName, partitionColumns, [delimiter],[schema], [skipRows], [transform], [sortColumns], [atomic], [arrayDelimiter])
```

**详情**

加载一批对象到表中，返回一个表，包含 object(STRING), errorCode(INT), errorInfo(STRING)三列，描述解压的每一个文件（object）加载的错误码（errorCode，0 表示没有错误）和错误信息（errorInfo）。

错误代码（errorCode）如下：

* 1-未知问题
* 2-解析文件并写入表中失败
* 3-下载文件失败
* 4-unzip文件失败
* 5-查找解压文件失败
* 6-抛出异常，有详细信息
* 7-抛出未知异常，没有详细信息

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**key** STRING 类型标量或向量，表示读取对象名或对象名的列表。支持文本文件，或Zip格式的压缩对象。

**threadCount** INT 类型标量，表示下载的线程数，必须为正整数。

**dbHandle** 数据库的句柄，可以是内存数据库或分布式数据库。

**tableName** STRING 类型的标量，表示表的名称。

**partitionColumns** STRING 类型标量或向量，表示分区列。对于顺序分区类型的数据库，partitionColumns 为空字符串""。对于组合分区类型的数据库，partitionColumns 是字符串向量。

**delimiter** STRING 类型的标量，表示数据文件中各列的分隔符。可选参数，默认是逗号。

**schema** 一个表对象，用于指定各列的数据类型。可选参数，它可以包含以下四列（其中，name 和 type 这两列是必需的）

| 列名 | 含义 |
| --- | --- |
| name | 字符串，表示列名 |
| type | 字符串，表示各列的数据类型。暂不支持 BLOB, COMPLEX, POINT, DURATION 类型。 |
| format | 字符串，表示数据文件中日期或时间列的格式 |
| col | 整型，表示要加载的列的下标。该列的值必须是升序。 |

**skipRows** 整型标量，表示从文件头开始忽略的行数。可选参数。默认值为 0，可取值为 0 到 1024 之间的整数。

**transform** 一元函数，并且该函数接受的参数必须是一个表。可选参数，插件会对数据文件中的数据执行该函数，并将得到的结果保存在数据库中

**sortColumns** 字符串标量或向量，表示表的排序列。可选参数，同一个排序列对应的数据在分区内部按顺序存放在一起。

**atomic** 布尔类型标量，表示开启 Cache Engine 的情况下，是否保证文件加载的原子性。可选参数，默认为false，设置为 true，一个文件的加载过程视为一个完整的事务；设置为 false，加载一个文件的过程分为多个事务进行。

注意：如果要加载的文件超过 Cache Engine 大小，必须设置 atomic = false。否则，一个事务可能卡住（既不能提交，也不能回滚）。

\*\*arrayDelimiter \*\*STRING类型的标量，表示数据文件中数组向量列的分隔符。可选参数，默认是逗号。由于不支持自动识别数组向量，必须同步修改 schema 的 type 列修为数组向量类型。

### headS3Object

**语法**

```
aws::headS3Object(account, bucket, key)
```

**详情**

获取某个文件的元数据，返回一个字典，包含如下字段："bucket name", "key name", "length", "last modified", "ETag", "content type"。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**key** STRING 类型的标量，表示对象名。

### copyS3Object

**语法**

```
aws::copyS3Object(account, bucket, srcPath, destPath)
```

**详情**

拷贝 S3 文件到同一个 bucket 的另一个位置。

**参数**

**account** 键为 STRING 类型的 ANY 字典，用于配置账户信息和连接参数。

**bucket** STRING 类型的标量，表示访问的桶名称。

**srcPath** STRING 类型的向量，表示源文件路径。

**destPath** STRING 类型的向量，表示目标文件路径。

## 使用示例

```
account=dict(string,string);
account['id']=your_access_key_id;
account['key']=your_secret_access_key;
account['region']=your_region;
db = database(directory="dfs://rangedb", partitionType=RANGE, partitionScheme=0 51 101)
aws::loadS3Object(account, 'dolphindb-test-bucket', 't2.zip', 4, db, `pt, `ID);
```
