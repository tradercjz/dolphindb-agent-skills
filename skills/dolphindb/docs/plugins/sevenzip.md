<!-- Auto-mirrored from upstream `documentation-main/plugins/sevenzip.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SevenZip

7Zip 是一个开源压缩库，可用于文件解压缩。DolphinDB 的 SevenZip 插件基于 P7Zip 开源库开发，支持压缩和解压缩多种格式：

压缩 7z、bzip2、gzip、tar、wim、xz、zip 文件。

解压缩 7z、bzip2、gzip、tar、wim、xz、zip、rar 文件。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.11及更高版本，支持 Linux x86, Linux ABI, Linux JIT, Linux Arm。

### 安装步骤

1. 在 DolphinDB 客户端中使用 listRemotePlugins 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 installPlugin 命令完成插件安装。

   ```
   installPlugin("SevenZip")
   ```
3. 使用 loadPlugin 命令加载插件。

   ```
   loadPlugin("SevenZip")
   ```

## 接口说明

### unzip

**语法**

```
SevenZip::unzip(filePath, [outputPath], [password], [callback])
```

**详情**

提取一个 7Zip 压缩文件里的所有文件。支持通过回调函数，对解压出的文件进行处理。当 7Zip 文件中包含多个文件时，可以实现每解压出一个文件，便被回调函数处理。

返回一个 STRING 类型的向量，表示解压后的文件路径。

**参数**

**filePath** STRING 类型的标量，表示需要解压缩的 7Zip 文件的文件路径。

**outputPath** 可选参数，STRING 类型的标量，表示解压文件的输出目录。省略该参数表示输出目录即为压缩包所在目录。

**password** 可选参数，STRING 类型的标量，表示 7Zip 压缩文件的密码。

**callback** 可选参数，一个一元函数，参数为 STRING 类型的标量，传入解压后的文件路径。

**例子**

```
def handler1(filePath){
  print(filePath)
}
path = "/hdd1/commit/DolphinDBPlugin"
extractPath = "/hdd1/commit/DolphinDBPlugin/tmp"
SevenZip::unzip(path + "/data.7z", extractPath, "123456", handler1)
```

### zip

**语法**

```
SevenZip::zip(archivePath, sourcePath, [level], [method], [password])
```

**详情**

压缩一个文件夹或者一个文件到指定 7Z 文件中。

**参数**

**archivePath** STRING 类型的标量，表示压缩后的 7Z 文件的文件路径。

**sourcePath** STRING 类型的标量，表示需要压缩的文件夹或文件的文件路径。

**level** 可选参数，INT 类型的标量，表示压缩等级，默认为 5，大小可以为 1 到 9，其中 9 代表最高压缩等级。

**method** 可选参数，STRING 类型的标量，表示压缩方法。支持的压缩方法如下：

| **文件格式** | **文件后缀** | **支持压缩方法** |
| --- | --- | --- |
| 7z | 7z | LZMA2, LZMA, PPMd, BZip2。默认为 LZMA2。 |
| bzip2 | bzip2, bz2, bzip2, tbz2 | 不支持指定压缩方法。 |
| gzip | gzip, gz, tgz | 不支持指定压缩方法。 |
| tar | tar, ova | 不支持指定压缩方法。 |
| wim | wim, swm, esd | 不支持指定压缩方法。 |
| xz | xz, txz | 不支持指定压缩方法。 |
| zip | zip01, zipx, jar, xpi, odt, ods, docx, xlsx, epub | Deflate, Deflate64, BZip2, LZMA, PPMd。默认为 Deflate。 |

**password** 可选参数，STRING 类型的标量，表示压缩文件的密码。

**例子**

```
path = "/hdd1/commit/DolphinDBPlugin"
SevenZip::zip(path + "/data.7z", path + "/7ZipData", 5, "lzma2", "123456")
```
