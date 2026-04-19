<!-- Auto-mirrored from upstream `documentation-main/plugins/zlib/zlib.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Zlib

DolphinDB 的 zlib 插件，支持文件到文件的 zlib 压缩与解压缩。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本。

目前支持 x86-64 的 Linux, Linux\_JIT、Linux ARM。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/) 进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins("zlib")
   ```
2. 使用 installPlugin 命令完成插件安装。

   ```
   installPlugin("zlib")
   ```
3. 使用 loadPlugin 命令加载插件。

   ```
   loadPlugin("zlib")
   ```

## 接口说明

### compressFile

**语法**

```
compressFile(filePath, [compressionLevel])
```

**参数**

**filePath** STRING 类型标量，表示输入文件名及路径。

**compressionLevel** 可选参数，属于[-1,9] 的整数，表示压缩等级。默认值为 -1（等同于级别 6），1 提供最佳速度，9 提供最佳压缩比，0 不提供压缩。

**详情**

将输入文件压缩为 .gz 文件，返回压缩后的文件名。

**例子**

将 /home/jccai/data.txt 压缩为 /home/jccai/data.txt.gz，若输出路径下有同名文件，则旧文件会被覆盖。

```
compressFile("/home/jccai/data.txt")
```

### decompressFile

**语法**

```
decompressFile(filePath)
```

**参数**

**filePath** STRING 类型标量，表示压缩文件的文件名及路径，应以 .gz 结尾。

**详情**

将输入文件解压缩，并返回加压缩后的文件名。

**例子**

将 /home/jccai/data.txt.gz 解压为 /home/jccai/data.txt，若输出路径下有同名文件，则旧文件会被覆盖。

```
decompressFile("/home/jccai/data.txt.gz");
```
