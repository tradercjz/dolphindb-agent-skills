<!-- Auto-mirrored from upstream `documentation-main/plugins/input.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# input

input 插件基于 libarchive 开发，用于解压缩内存数据或文件内容，并返回解压后的文本。插件能够自动识别压缩格式（目前支持 zstd 和
gzip）并解压数据。

## 安装插件

### 版本要求

DolphinDB Server：2.00.14/3.00.2 及更高版本，且部署于 Linux x86-64 系统。

1. 在 DolphinDB 客户端中使用 listRemotePlugins
   函数查看可供安装的插件。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 installPlugin
   函数安装插件。

   ```
   installPlugin("input")
   ```
3. 使用 loadPlugin
   函数加载插件。

   ```
   loadPlugin("input")
   ```

## 接口说明

### readMemory

**语法**

```
input::readMemory(data)
```

**详情**

从内存中读取二进制数据（BLOB），自动识别其压缩格式（支持 zstd 和 gzip）并完成解压。

**参数**

**data** BLOB 类型标量，指定待解压的数据。

**返回值**

解压后的文本内容，STRING 类型标量。

### readFile

**语法**

```
input::readFile(path)
```

**详情**

从指定路径下读取文件，自动识别其压缩格式（支持 zstd 和 gzip）并完成解压。

**参数**

**path** STRING 类型标量，指定待解压文件的路径。

**返回值**

解压后的文本内容，STRING 类型标量。

### blobToLong

**语法**

```
input::blobToLong(data)
```

**详情**

将小于 8 字节的二进制数据转换为一个 LONG 类型数据。

**参数**

**data** BLOB 类型标量，指定待转换的数据。

**返回值**

LONG 类型标量。

## 使用示例

### 示例一：从二进制文件读取记录表

假设某外部系统周期性生成一个二进制文件，每条记录依次包含：交易时间、代码、价格和数量，均为定长字段。可通过如下方式在 DolphinDB 中读取文件：

```
// 加载插件
loadPlugin("input")

// 从指定路径中读取文件并解压
path = "./trade.bin"
content = readFile(path)

// 转换为表格
table = parseJsonTable(content)
```

上述示例中，trade.bin 是一个压缩后的 JSON 文件。`readFile` 读取整个文件并解压为 STRING 类型数据，后续可以通过 DolphinDB 字符串解析与处理函数执行数据转换。

### 示例二：从共享内存读取数据

在某些高频场景中，外部进程将最新数据写入共享内存区域。`readMemory` 直接读取内存地址中的数据，减少磁盘 IO 和数据复制带来的延迟。

```
// 加载插件
loadPlugin("input")

// 从消息队列中接收数据
// content = ...
content = readMemory(content)

// 转换为表格
table = parseJsonTable(content)
```

上述示例中，content 是通过消息队列接收的压缩数据。`readMemory` 将其解压为 STRING 类型数据，后续可以通过 DolphinDB 字符串解析与处理函数执行数据转换。
