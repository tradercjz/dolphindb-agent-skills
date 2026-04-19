<!-- Auto-mirrored from upstream `documentation-main/plugins/mat/mat.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# mat

DolphinDB 的 mat 插件支持读取 mat 文件的数据到 DolphinDB，或将 DolphinDB 变量写入 mat 文件，且在读取或写入时自动进行类型转换。mat 插件基于 MATLAB Runtime 运行库开发。

## 安装插件

### 版本要求

DolphinDB Server: 2.00.10 及更高版本。支持 Linux x86-64,Linux JIT。

### 安装步骤

1. 安装 MATLAB Runtime Installer。linux 终端中执行：

   ```
   wget <https://ssd.mathworks.com/supportfiles/downloads/R2016a/deployment_files/R2016a/installers/glnxa64/MCR_R2016a_glnxa64_installer.zip>
   unzip MCR_R2016a_glnxa64_installer.zip -d matlabFile
   cd matlabFile
   ./install -mode silent -agreeToLicense  yes  -destinationFolder  /home/Matlab
   ```
2. 启动 dolphindb 服务之前执行：

   ```
   export LD_LIBRARY_PATH=/home/Matlab/v901/bin/glnxa64:$LD_LIBRARY_PATH
   ```
3. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   **注意**：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
4. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("mat")
   ```
5. 使用 `loadPlugin` 命令加载插件。

   `loadPlugin("mat")`

## 接口说明

### extractMatSchema

**语法**

```
extractMatSchema(filePath)
```

**详情**

生成 mat 文件中指定数据集的结构。包括两列：字段名和数据类型。

**参数**

**filePath** STRING 类型标量，表示需要读取的 mat 文件所在的绝对路径。

**例子**

```
schema=extractMatSchema("<FileDir>/simple.mat");
```

### loadMat

**语法**

```
loadMat(filePath, [schema])
```

**详情**

读取一个 mat 文件。

返回一个字典：

* key 为STRING 类型，表示变量名称。
* value 是一个矩阵或向量，为 key 指定的变量对应的数据。如果一个变量是字符数组类型，对应返回值为 STRING 类型的向量。

**参数**

**filePath** STRING 类型标量，表示需要写入的 mat 文件所在的绝对路径。

**schema** 包含列名和列的数据类型的表，用于指定各字段的数据类型。若要改变由系统自动决定的列的数据类型，需要在 schema 表中修改数据类型。

**例子**

```
schema=extractMatSchema("<FileDir>/simple.mat");
ret=loadMat("<FileDir>/simple.mat",schema);
//simple 中 t_num 变量为 double 类型的时间变量
ret=convertToDatetime(ret[`t_num]);
```

### convertToDatetime

**语法**

```
convertToDatetime(data)
```

**详情**

把 matlab 中以 double 储存的时间变量转换为 DolphinDB 的 DATETIME。

返回值是对应于参数 data 的 DATETIME 类型的标量、向量或矩阵。

**参数**

**data** 需要转换的变量。为 double 类型的 scalar, vector, matrix。

**例子**

```
schema=extractMatSchema("<FileDir>/simple.mat");
ret=loadMat("<FileDir>/simple.mat",schema);
ret=convertToDatetime(ret);
```

### writeMat

**语法**

```
writeMat(filePath, varName, data)
```

**详情**

把一个矩阵写入到 mat 文件。

**参数**

**filePath** STRING 类型的标量，表示被写入文件的文件名。

**varName** STRING 类型的标量，表示 \*data \*写入文件后对应的变量名。

**data** 可以是 BOOL, CHAR, SHORT, INT, LONG, FLOAT, DOUBLE 类型矩阵，表示需要写入的矩阵。

**例子**

```
data = matrix([1, 1, 1], [2, 2, 2]).float()
writeMat("var.mat", "var1", data)
```

## 支持的数据类型

### 整型

| matlab 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| int8 | CHAR |
| uint8 | SHORT |
| int16 | SHORT |
| uint16 | INT |
| int32 | INT |
| uint32 | LONG |
| int64 | LONG |
| uint64 | 不支持 |

* DolphinDB 中数值类型都为有符号类型，为了防止溢出，所有无符号类型会被转化为高一阶的有符号类型。例如，无符号 CHAR 转化为有符号 SHORT，无符号 SHORT 转化为有符号 INT，等等。64 位无符号类型不予支持。
* DolphinDB 不支持 unsigned long long 类型，如果 matlab 中的类型为 bigint unsigned, 可在 `loadMat` 的 schema 参数里面设置为 DOUBLE 或者 FLOAT。
* DolphinDB 中各类整型的最小值为 NULL，如 CHAR 的 -128，SHORT 的 -32,768，INT 的 -2,147,483,648 以及 LONG 的 -9,223,372,036,854,775,808。
* Matlab 中的 NaN 和 Inf 会转换为 DolphinDB 的 NULL。

### 浮点数类型

| matlab 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| single | FLOAT |
| double | DOUBLE |

### 字符串类型

| matlab 类型 | 对应的 DolphinDB 类型 |
| --- | --- |
| character array | STRING |
