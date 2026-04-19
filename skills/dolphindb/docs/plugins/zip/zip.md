<!-- Auto-mirrored from upstream `documentation-main/plugins/zip/zip.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# zip

zip 是一种标准的压缩文件的格式。DolphinDB 的 zip 插件可以对 zip 文件进行解压、压缩文件到 zip 文件中。zip 插件基于 minizip 和 zipper 开发。

## 在插件市场安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本，支持 Linux、Linux JIT、Linux ABI、Windows、Windows JIT。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("zip")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("zip")
   ```

## 接口说明

### unzip

**语法**

```
zip::unzip(zipFilePath, [outputDir], [callback], [zipEncoding], [password])
```

**参数**

**zipFilePath** 字符串标量，表示 ZIP 文件路径。仅支持绝对路径。

**outputDir** 字符串标量，表示解压文件的输出路径，可选。仅支持绝对路径。若该参数不传或为 "" 时，则解压路径和压缩包路径相同。注意：指定路径下的同名文件将被覆盖。

**callback** 函数，仅接收一个 STRING 类型的参数，可选。

**zipEncoding** 字符串标量，可选。表示 zip 文件内部的文件名编码。目前仅支持 gbk 和 utf-8 两种编码。在 Windows 系统上，默认为 gbk 编码，Linux 系统上，默认为 utf-8 编码。例子：如在 Windows 上如果要解压以 utf-8 编码的 zip 文件则需要指定该参数为 "utf-8"。

**password** 字符串标量。压缩包的密码。

**详情**

用于解压指定的 ZIP 格式文件。

支持通过回调函数，对解压出的文件进行处理。当 ZIP 文件中包含多个文件时，可以实现每解压出一个文件，便被回调函数处理，提高 `unzip` 的处理效率。同时可以指定 zip 文件内部的文件名编码格式，确保解压后的文件路径编码正确。

**返回值**

返回一个由解压文件路径组成的字符串向量。

**示例**

```
filenames = zip::unzip("/path_to_zipFile/test.zip", "/path_to_output/", func)

print(filenames)
["/path_to_output/test.csv"]
```

### zip

**语法**

```
zip::zip(zipFilePath, fileOrFolderPath, [compressionLevel], [password])
```

**参数**

**zipFilePath** zip 文件的路径。类型为 STRING 的 SCALAR。

**fileOrFolderPath** 需要压缩的文件夹或者是文件的文件路径。类型为 STRING 的 SCALAR。

**compressionLevel** 压缩等级。目前支持”faster” 和 “better”。”faster“会以最快的压缩速度进行压缩，“better” 则会以最高的压缩率来进行压缩。类型为 STRING 的 SCALAR。

**password** 压缩密码。类型为 STRING 的 SCALAR。

**详情**

压缩一个文件夹或者一个文件。

**示例**

```
zip::zip("/hdd1/commit/DolphinDBPlugin/zip/test/test.zip", "/hdd1/commit/DolphinDBPlugin/zip/data")
```
