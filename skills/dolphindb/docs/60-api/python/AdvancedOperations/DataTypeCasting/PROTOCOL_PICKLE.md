<!-- Auto-mirrored from upstream `documentation-main/api/python/AdvancedOperations/DataTypeCasting/PROTOCOL_PICKLE.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# PROTOCOL\_PICKLE

Pickle 协议是一种对 Python 对象进行序列化和反序列化的方式，允许使用者将复杂的 Python 对象转换为可以存储或传输的字节流，再将该字节流转换为原始的 Python 对象。DolphinDB 中提供了基于 Python Pickle 协议特化的反序列化方案 PROTOCOL\_PICKLE，该协议仅限在 DolphinDB Python API 中进行使用，其支持的**数据形式**和**数据类型**相对较少。

**注1：** 数据形式指 DolphinDB 类型系统中的 DATAFORM，通常包含 Scalar、Vector、Table 等，表示数据结构的形式。

**注2：** 数据类型指 DolphinDB 类型系统中的 DATATYPE，通常包含 INT、DOUBLE、DATETIME 等，表示数据的具体类型。

**注3：** 以下简称 Python 库 NumPy 为 **np**，pandas 为 **pd**。

## 启用 PROTOCOL\_PICKLE

在以下示例中，Session 和 DBConnectionPool 通过设置参数 *protocol* 指定启用 PROTOCOL\_PICKLE 协议。在当前版本中 PROTOCOL\_DEFUALT 等同于 PROTOCOL\_PICKLE，故默认使用 PROTOCOL\_PICKLE 作为序列化、反序列化协议。

```
import dolphindb as ddb
import dolphindb.settings as keys

s = ddb.Session(protocol=keys.PROTOCOL_PICKLE)
s.connect("localhost", 8848, "admin", "123456")

pool = ddb.DBConnectionPool("localhost", 8848, "admin", "123456", 10, protocol=keys.PROTOCOL_PICKLE)
```

## PROTOCOL\_PICKLE 数据形式支持表

PROTOCOL\_PICKLE 支持的数据形式如下表展示：

| 附加参数 | 数据形式 | 序列化 | 反序列化 |
| --- | --- | --- | --- |
| pickleTableToList=False | Matrix | 不支持 | 支持 |
| pickleTableToList=False | Table | 不支持 | 支持 |
| pickleTableToList=True | Table | 不支持 | 支持 |

## 反序列化 DolphinDB -> Python(设置 pickleTableToList=False)

### Matrix

DolphinDB 中的 Matrix 对应 Python 中的 np.ndarray，不同数据类型与 np.dtype 的对应关系如下表所示：

| DolphinDB类型 | np.dtype |
| --- | --- |
| BOOL（不含空值） | bool |
| CHAR（不含空值） | int8 |
| SHORT（不含空值） | int16 |
| INT（不含空值） | int32 |
| LONG（不含空值） | int64 |
| DATE、MONTH、TIME、TIMESTAMP、MINUTE、SECOND、DATETIME、NANOTIME、NANOTIMESTAMP、DATEHOUR | datetime64[ns] |
| FLOAT | float32 |
| DOUBLE、CHAR（含空值）、SHORT（含空值）、INT（含空值）、LONG（含空值） | float64 |
| BOOL（含空值） | object |

和 PROTOCOL\_DDB 一致，API 通过 PROTOCOL\_PICKLE 协议下载的 Matrix 对应着包含三个元素的 list。list 中的第一个元素为 np.ndarray，表示实际数据；第二、三个元素分别对应 Matrix 的行名和列名，如果未设置行名、列名，则用 None 替代。如下为示例代码：

```
>>> s.run("date([2012.01.02, 2012.02.03])$1:2")
[array([['2012-01-02T00:00:00.000000000', '2012-02-03T00:00:00.000000000']],
      dtype='datetime64[ns]'), None, None]
```

**注意** ：若指定协议为 PROTOCOL\_DDB，则下载时间类型 Matrix 对应的 dtype 为 datetime64[D]/datetime64[ms]/datetime64[M]/...；若指定协议为 PROTOCOL\_PICKLE，则下载时间类型 Matrix 对应的 dtype 都为 datetime64[ns]。

### Table

PROTOCOL\_PICKLE 协议中 Table 列类型对应的 np.dtype 如下表所示：

| DolphinDB 类型 | np.dtype |
| --- | --- |
| BOOL（不含空值） | bool |
| CHAR（不含空值） | int8 |
| SHORT（不含空值） | int16 |
| INT（不含空值） | int32 |
| LONG（不含空值） | int64 |
| DATE、MONTH、TIME、TIMESTAMP、MINUTE、SECOND、DATETIME、NANOTIME、NANOTIMESTAMP、DATEHOUR | datetime64[ns] |
| FLOAT | float32 |
| DOUBLE、CHAR（含空值）、SHORT（含空值）、INT（含空值）、LONG（含空值） | float64 |
| BOOL（含空值）、SYMBOL、STRING、UUID、IPADDR、INT128、Array Vector | object |

**注1：** PROTOCOL\_PICKLE 暂不支持 BLOB、DECIMAL32、DECIMAL64 类型的数据列。

**注2：** PROTOCOL\_PICKLE 暂不支持 UUID、IPADDR、INT128 类型的 Array Vector 数据列。

下载 Table 型数据的相关代码示例：

```
>>> re = s.run("table([1, NULL] as a, [2012.01.02, 2012.01.05] as b)")
>>> re
     a          b
0  1.0 2012-01-02
1  NaN 2012-01-05
>>> re['a'].dtype
float64
>>> re['b'].dtype
datetime64[ns]
```

## 反序列化 DolphinDB -> Python(设置 pickleTableToList=True)

### Table

指定使用 PROTOCOL\_PICKLE 协议，在执行 run 方法时，若指定额外参数 `pickleTableToList=True`，则下载 Table 型数据将得到一个 list 数据，且 list 的每个元素都是 np.ndarray。如果下载 Table 型数据的数据列为 Array Vector 列，须确保每个元素的长度一致，其对应数据类型为二维 np.ndarray。

本节详细的类型转换规则和 PROTOCOL\_DDB 中 第5小节一致。
开启附加参数 pickleTableToList 后，如果执行脚本的返回值数据形式为 Table，则对应的 Python 对象为 list 而非 pd.DataFrame。其中，list 中的每一元素（np.ndarray）都表示 Table 中的一列。

和 PROTOCOL\_DDB 协议的附加参数稍有不同，PROTOCOL\_DDB 协议的附加参数会作为flag的一部分发送至服务端。
