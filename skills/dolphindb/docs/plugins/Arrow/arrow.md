<!-- Auto-mirrored from upstream `documentation-main/plugins/Arrow/arrow.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# Arrow

[Apache Arrow](https://arrow.apache.org/) 是一种跨平台的内存数据格式，被设计为一种内存中的列式数据格式，可以高效地存储和传输大规模数据集，同时提供了高性能的数据操作功能。在引入 Arrow 插件之前，DolphinDB 与 API 进行数据交互时可以通过 PICKLE 或者 DDB 协议进行序列化。引入 Arrow 插件后，DolphinDB 数据，可以通过 ARROW 协议转换为 Arrow 格式进行传输，从而使得 DolphinDB 与 API 之间的数据传输更高效。

**注意：**

1. 自 DolphinDB 2.00.11 版本起，formatArrow 插件更名为 Arrow。
2. 自 2.00.12 版本起，Arrow 插件可从插件市场直接下载，允许执行 `loadPlugin` 函数加载。2.00.11 及之前版本必须调用 `loadFormatPlugin` 函数才能正常加载。`loadFormatPlugin` 函数使用方式同 `loadPlugin` 函数，但只能用来加载数据格式插件。

## 安装插件

### 版本要求

DolphinDB Server：2.00.12 及更高版本。支持 Linux x86-64，Windows x86-64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可[自行编译](https://gitee.com/dolphindb/DolphinDBPlugin)（请自行选择对应分支下的插件）或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("arrow")
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("arrow")
   ```

## 接口说明

Arrow 插件不提供用户可调用函数接口。

`loadPlugin` 函数返回的接口仅供 DolphinDB 内部调用，不支持用户通过脚本调用。

## 数据类型转换说明

Arrow 插件目前仅支持向 API 单向传输数据，不支持接收从 API 发送的 Arrow 格式数据。

目前仅 Python API 可以通过 PROTOCOL\_ARROW 协议下载 Arrow 格式数据。

### DolphinDB → Arrow

目前仅支持序列化传输 DolphinDB Table 为 Arrow Table。DolphinDB 与 Arrow 数据类型转换关系如下：

| **DolphinDB** | **Arrow** |
| --- | --- |
| BOOL | boolean |
| CHAR | int8 |
| SHORT | int16 |
| INT | int32 |
| LONG | int64 |
| DATE | date32 |
| MONTH | date32 |
| TIME | time32(ms) |
| MINUTE | time32(s) |
| SECOND | time32(s) |
| DATETIME | timestamp(s) |
| TIMESTAMP | timestamp(ms) |
| NANOTIME | time64(ns) |
| NANOTIMESTAMP | timestamp(ns) |
| DATEHOUR | timestamp(s) |
| FLOAT | float32 |
| DOUBLE | float64 |
| SYMBOL | dictionary(int32, utf8) |
| STRING | utf8 |
| IPADDR | utf8 |
| UUID | fixed\_size\_binary(16) |
| INT128 | fixed\_size\_binary(16) |
| BLOB | large\_binary |
| DECIMAL32(X) | decimal128(38, X) |
| DECIMAL64(X) | decimal128(38, X) |

注意：

* 同时支持以上除了 DECIMAL 外的 ArrayVector 类型。
* 自 2.00.11 版本起，下载 UUID / INT128 后的字节顺序从反转修正为和上传时的顺序保持一致。

## 使用示例

### DolphinDB server

```
login("admin", "123456");
loadPlugin("arrow");
```

### Python API

```
import dolphindb as ddb
import dolphindb.settings as keys
s = ddb.session("192.168.1.113", 8848, "admin", "123456", protocol=keys.PROTOCOL_ARROW)
pat = s.run("table(1..10 as a)")

print(pat)
-------------------------------------------
pyarrow.Table
a: int32
----
a: [[1,2,3,4,5,6,7,8,9,10]]
```

**注意**：现版本中 DolphinDB 服务器不支持使用 Arrow 协议时开启压缩。
