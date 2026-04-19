<!-- Auto-mirrored from upstream `documentation-main/plugins/EncoderDecoder.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# EncoderDecoder

DolphinDB 提供 EncoderDecoder 插件用于高效解析、转换 JSON 以及 protobuf 数据为 DolphinDB table 格式数据。

## 在插件市场安装插件

### 版本要求

DolphinDB Server 2.00.10 及更高版本。

支持 Linux x86-64、支持 Linux ARM。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.cn/)进行反馈。

   ```
   login("admin", "123456");
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("EncoderDecoder");
   ```
3. 使用 `loadPlugin` 命令加载插件。

   ```
   loadPlugin("EncoderDecoder");
   ```

## 用户接口

### JSON

#### jsonDecoder

**语法**

```
EncoderDecoder::jsonDecoder(colNames, colTypes, [handler], [workerNum=1], [batchSize=0], [throttle=1], [isMultiJson=false])
```

**参数**

**colNames** string 类型的 vector，指定要解析的 JSON 数据中的 key 的名称，是 JSON 中的键。

**colTypes** int 类型的 vector，指定要解析的 JSON 数据中的 value 的类型，是 JSON 中的值类型。

**handler** 可以是一个表，用于输出解析结果；也可以是一个函数对象，当前 decoder 的输出将作为该函数的输入进行处理。

**workerNum** int 类型，处理解析运算的工作线程数量。默认值是 1。

**batchSize** 整数。若为正数，表示未处理消息的数量达到 *batchSize* 时，*handler* 才会处理消息。若未指定或为非正数，每一批次的消息到达之后，*handler* 就会马上处理。默认值是 0。

**throttle** 浮点数，单位为秒，默认值为 1。表示继上次 handler 处理消息之后，若 *batchSize* 条件一直未达到，多久后再次处理消息。

**isMultiJson** 布尔值，默认为 false。表示一行内是否存在多个 JSON 字符串。如果设置为 true, 会先进行字符串分割再进行解析。注意，设置为 true 时要求 JSON 内字符串格式的 value 不能带字符 `}` 、 `{`。

**返回值**

解析 JSON 数据的 coder 对象。

**jsonDecoder 对象函数 parseAndHandle**

**语法**

```
coder.parseAndHandle(obj)
```

**详情**

`parseAndHandle` 方法用于解析 JSON 数据，并将结果输出到 handler 中。

**参数**

输入参数可以为 scalar，vector 或者内存表。

* 如果输入 scalar 或 vector，则必须为 string 类型。
* 如果是内存表，则必须只有一列，且列类型为 string 类型。

**报错信息**

* 如果 schema 不匹配，抛出异常 Usage: coder.parseAndHandle(obj). Obj must be a table with one STRING column。
* 如果其中的 JSON 数据格式非法，则会在 log 中输出 syntax error while parsing value (具体异常信息) 相关行，但仍然会输出字段全为空的结果到目标表中。

**jsonDecoder 对象函数 parse**

**语法**

```
coder.parse(obj)
```

**详情**

解析输入的数据。

**参数**

同 `parseAndHandle`。

**返回值**

返回 table。

**异常说明**

* 如果 JSON 输入非法，会输出字段全为空的结果。
* 如果某个字段不出现，则会被自动赋空值。

**数据类型与转换**

*colTypes* 支持填写 BOOL、CHAR、INT、LONG、FLOAT、DOUBLE、STRING、BLOB 以及 arrayVector 类型 BOOL[]、INT[]、LONG[]、FLOAT[]、DOUBLE[]。

**转换规则**

| DolphinDB 类型 \ JSON 类型 | bool | number | string | bool array | number array | string array |
| --- | --- | --- | --- | --- | --- | --- |
| BOOL | √ | √ | √ 非空即为 true | X | X | X |
| CHAR | √ | X | 长度 <= 1的 string 支持 | X | X | X |
| INT | √ | √ | X | X | X | X |
| LONG | √ | √ | X | X | X | X |
| FLOAT | √ | √ | X | X | X | X |
| STRING | √ | √ | √ | X | X | X |
| BLOB | √ | √ | √ | X | X | X |
| BOOL[] | X | X | X | √ | √ | √ 非空即为 true |
| INT[] | X | X | X | √ | √ | X |
| LONG[] | X | X | X | √ | √ | X |
| FLOAT[] | X | X | X | √ | √ | X |
| DOUBLE[] | X | X | X | √ | √ | X |

注：

* 不在表格中出现的类型转换均为不支持。
* 超出 double、long 等上限的数据，可以转为 STRING 类型保留精度。

#### **示例**

下面介绍使用插件解析 JSON 数据的例子。

创建数据：

```
str={"int": -637811349, "long": 637811349473772538,"float":-0.004 ,"double": 12133.938,"string": "2022-02-22 13:55:47.377"}
data = [str.toStdJson(),str.toStdJson(),str.toStdJson(),str.toStdJson()]
appendData = table(data as `string)
```

使用未指定输出的 jsonDecoder 调用 `parse` 进行解析，结果会直接输出：

```
colNames = ["int", "long","float","double","string"]
colTypes = [INT, LONG, FLOAT , DOUBLE, STRING]
coder1 = EncoderDecoder::jsonDecoder(colNames, colTypes)
coder1.parse(appendData)
```

输出如下：

```
int        long               float  double                string
---------- ------------------ ------ --------------------- -----------------------
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
```

使用指定输出及其他参数的 jsonDecoder 调用 `parseAndHandle` 进行解析：

```
handler = table(1:0, colNames, colTypes)
coder2 = EncoderDecoder::jsonDecoder(colNames, colTypes, handler, 4, 100, 0.01)
coder2.parseAndHandle(appendData)
```

handler 内容如下：

```
int        long               float  double                string
---------- ------------------ ------ --------------------- -----------------------
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
-637811349 637811349473772538 -0.004 12133.938000000000101 2022-02-22 13:55:47.377
```

使用指定 handler 为函数的 jsonDecoder 调用 `parseAndHandle` 进行解析，结果会输出到 dest 表中：

```
colNames2 = ["int", "long","float","double","date", "time"]
colTypes2 = [INT, LONG, FLOAT , DOUBLE, TIMESTAMP, TIMESTAMP]
dest = table(1:0, colNames2, colTypes2)

def parserDef(msg, mutable dest) {
    t = table(msg[`int] as `int, msg[`long] as `long, msg[`float] as `float, msg[`double] as `double, temporalParse(msg[`string] ,"yyyy-MM-dd HH:mm:ss.SSS")  as `date);
    t.update!(`name, now());
    dest.append!(t);
}
coder3 = EncoderDecoder::jsonDecoder(colNames, colTypes, parserDef{, dest}, 4, 100, 1)
coder3.parseAndHandle(appendData)
```

dest 表格内容如下：

```
int        long               float  double                date                    time
---------- ------------------ ------ --------------------- ----------------------- -----------------------
-637811349 637811349473772538 -0.004 12133.938000000000101 2022.02.22T13:55:47.377 2023.10.26T11:22:00.140
-637811349 637811349473772538 -0.004 12133.938000000000101 2022.02.22T13:55:47.377 2023.10.26T11:22:00.140
-637811349 637811349473772538 -0.004 12133.938000000000101 2022.02.22T13:55:47.377 2023.10.26T11:22:00.140
-637811349 637811349473772538 -0.004 12133.938000000000101 2022.02.22T13:55:47.377 2023.10.26T11:22:00.140
```

### protobuf

**注意：** 本插件支持的 protobuf 格式为 3.0，该格式不支持设定默认值，因此各个类型的空值与默认值都会当作默认值进行处理。详见 [Protocol Buffers: Default Values](https://developers.google.com/protocol-buffers/docs/proto3#default)。

#### extractProtobufSchema

**语法**

```
EncoderDecoder::extractProtobufSchema(filePath, [toArrayVector=false], [messageName])
```

**参数**

**filePath** STRING，指定要解析的 protobuf 数据格式，为一个 *.proto* 文件的路径。
如果路径不存在则抛出异常：file 路径名 does not exist.
如果该 proto 无法解析也抛出异常：Failed to parse .proto definition

**toArrayVector** BOOL，可选参数，默认为 false。决定是否需要将部分 repeated 关键字修饰的字段解析为 ARRAY VECTOR。true 则解析为 arrayVector。如果存在嵌套 repeat 字段，则仅将最内部 repeat 字段转换为 ARRAY VECTOR，非最内层的 repeat 字段仍作拍平处理。
**注意**：如果存在 repeated message 字段，且字段内部只有一层原始类型，则整个 repeated message 中的字段都会被处理为 ARRAY VECTOR。

**messageName** STRING，可选参数，指需要被解析的 Message Type 名字，如果没有指定，则默认需要被解析的是 *.proto* 文件中出现的第一个 Message Type。

**返回值**

返回一个由列名 name (类型 STRING) 、数据类型名称 typeString (类型 STRING)、数据类型枚举值 typeInt (类型 INT) 三列组成的表。

* 字段名：如果存在字段嵌套，则通过下划线将嵌套的字段名连接起来，作为 DolphinDB 表的列名。
* 数据类型：根据类型转换表转换为 DolphinDB 类型。如果遇到不支持的类型，类型列填为 "Unsupported" 类型转换表如下：
  + arrayVector 为 false 时，出现了有多个非嵌套关系的 repeated 字段，这些字段类型全部填为 "Unsupported" 。
  + arrayVector 为 true 时，出现了多个非嵌套关系的重复嵌套 repeated 字段，这些字段全部填为 "Unsupported" 。

**例子**

```
syntax = "proto3";

message test_repeat_2{
    double col1 = 1;
    message repeatMsg {
        float col2 = 1;
    }
    repeated repeatMsg msg1 = 2;
}
```

该 protobuf schema 对应的 DolphinDB Table schema 为：

| name | typeString | typeInt |
| --- | --- | --- |
| col1 | DOUBLE | 16 |
| msg1\_col2 | FLOAT | 15 |

**转换规则**

类型转换表 protobuf to DolphinDB

| protobuf 类型 | DolphinDB 类型 | toArrayVector 为 true 时的 DolphinDB 类型 | 备注 |
| --- | --- | --- | --- |
| double | DOUBLE | DOUBLE[] |  |
| float | FLOAT | FLOAT[] |  |
| int32 | INT | INT[] |  |
| int64 | LONG | LONG[] |  |
| uint32 | LONG | LONG[] |  |
| uint64 | LONG | LONG[] | 溢出则转换为 LONG 最大值 |
| sint32 | INT | INT[] |  |
| sint64 | LONG | LONG[] |  |
| fixed32 | LONG | LONG[] |  |
| fixed64 | LONG | LONG[] | 溢出则转换为 LONG 最大值 |
| sfixed32 | INT | INT[] |  |
| sfixed64 | LONG | LONG[] |  |
| bool | BOOL | BOOL[] |  |
| string | STRING | BLOB | toArrayVector 为 true 时，可以根据 schema 转换为其他计算类型的 arrayVector，如果未指定，则拼接为 JSON 列表格式的字符串 |
| bytes | BLOB | BLOB | 同上，且如果 blob 中含有特殊字符，转换结果可能出现乱码（不推荐使用） |
| enum | INT | INT[] |  |
| map | 不支持 | 不支持 | 某些情况下，带有一个 map 的类型的消息可以被处理，但是不推荐使用 |
| group | 不支持 | 不支持 |  |

protobuf 格式要求：

1. 一个 *.proto* 文件中，最外层最好只有一个 message 定义。内部可以有多个子 message 定义。如果外层有多个 message 定义则取第一个 message 进行解析。
2. 推荐语法为 proto3。
3. 不支持 extension 字段，不推荐有 optional 字段。
4. 如果 toArrayVector 为 false，则不能有多个非嵌套关系的 repeated 字段，因为这无法拍平为一张表；如果 toArrayVector 为 true，则不能有多个非嵌套关系的 重复嵌套 repeated 字段，因为这无法在存在 arrayVector 时，拍平为一张表。
5. 不能含有 oneof 关键字，因为一旦 oneof 中存在多种类型将无法自动拍平进入一张表格。
6. 嵌套的 proto message 会以'\_'作为连接符相互连接，需要用户保证连接后的结果不重复。

#### protobufDecoder

**语法**

```
EncoderDecoder::protobufDecoder(filePath, [handler], [workerNum=1], [batchSize=0], [throttle=1], [toArrayVector=false], [schema], [messageName], [useNullAsDefault=false])
```

**参数**

**filePath** STRING，指定要解析的 protobuf 数据格式，为一个 *.proto* 文件的路径。

**handler** 是一元函数、或数据表，用于处理输出的数据。

**workerNum** INT，处理解析运算的工作线程数量。默认值是 1，内部调用 server ploop 进行批量解析。

**batchSize** INT。若为正数，表示未处理消息的数量达到 *batchSize* 时，*handler* 才会处理消息。若未指定或为非正数，每一批次的消息到达之后，*handler* 就会马上处理。默认值是 0。

**throttle** FLOAT，单位为秒，默认值为 1。表示继上次 *handler* 处理消息之后，若 *batchSize* 条件一直未达到，多久后再次处理消息。

**toArrayVector** BOOL，表示是否需要将 repeated 关键字修饰的字段解析为 ARRAY VECTOR。

**schema** 表对象，用于指定各字段的数据类型。有 name 和 typeString 两列。若不指定则以原类型读取所有字段。*handler* 如果是表，它的列名与列类型需要与 schema 中完全一致。
如果 string 类型的 repeated 字段没有指定转换，则存为 BLOB 格式，数据内容为所有字段放入一个 array 中，以 JSON 格式存储，如 "["n1", "n2"]"，在 DolphinDB 中也可以通过 `str.parseExpr().eval()` 的方式转换为 DolphinDB 的列表。

**messageName** STRING，指需要被解析的 Message Type 名字，如果没有指定，则默认需要被解析的是 *.proto* 文件中出现的第一个 Message Type。

**useNullAsDefault** BOOL，默认为 false，指代是否要将没有显示指定默认值的字段指定为 DolphinDB 空值。

* 如果为 true，所有的空字段的值都会被解析为 DolphinDB 的空值。注意：如果 Proto 序列化文件中有字段被显示指定为默认值（proto2 规则支持默认值被显示序列化），则该字段的值**不会**被解析为空值。
* 如果为 false，则会采用 protobuf 规定的默认值 INTEGER: 0; FLOAT: 0.0; LITERAL: ""。

**返回值**

解析 protobuf 数据的 coder 对象。

**protobufDecoder 对象函数 parseAndHandle**

**语法**

```
coder.parseAndHandle(obj)
```

**详情**

`parseAndHandle` 方法用于解析 protobuf 数据，并将结果输出到 handler 中。

**参数**

输入参数可以为 scalar，vector 或者内存表。

* 如果输入 scalar 或 vector，则必须为 string 类型。
* 如果是内存表，则必须只有一列，且列类型为 string 类型。

**报错信息**

如果解析失败会写入 log 中。如果根据创建 coder 时传入的 schema，仍然有 protobuf 格式要求中不支持的字段（即 protobuf Decoder 解析规则 中会返回 “Unsupported" 为 typeString 的字段）。则解析会失败，输出具体的解析失败原因：

* repeated 字段不可解析： Failed to parse the protobuf messages due to an excessive number of non-nested repeated fields.
* 重名问题： Failed to parse the protobuf messages due to duplicate column names in the parsed table
* 指定了不可解析的类型： Unsupported data type of field <字段名>
* 指定了错误的 MessageName，或数据与输入的 proto 文件不匹配：Failed to parse value in buffer

具体格式要求与类型转换见上文转换规则。

**protobufDecoder 对象函数 parse**

**语法**

```
coder.parse(obj)
```

**详情**

`parse` 方法用于解析 protobuf 数据，并将结果输出到 handler 中。

**参数**

输入参数可以为 scalar，vector 或者内存表。

* 如果输入 scalar 或 vector，则必须为 string 类型。
* 如果是内存表，则必须只有一列，且列类型为 string 类型。

**报错信息**

如果解析失败会跑出异常，具体原因同上一个 `parseAndHandle` 函数。

#### protobufEncoder

**语法**

```
EncoderDecoder::protobufEncoder(filePath, [messageName])
```

**参数**

**filePath** STRING，指定 .proto 文件的路径，用于定义待序列化的 protobuf 数据结构。

**messageName** STRING，指需要被解析的 Message 类型名称。如果未设置该参数，则默认解析 .proto 文件中定义的第一个 Message 类型。

**详情**

根据 .proto 文件中定义的结构生成一个用于序列化数据的 protobuf encoder 对象。

**encoder 对象的成员函数 serialize**

**语法**

```
encoder.serialize(obj)
```

**参数**

**obj** 目前仅支持表。表中的列名需要与 .proto 文件中定义的字段名相同；不一致的列将在序列化时被忽略。

**详情**

将 *obj* 按照 .proto 文件中定义的格式序列化为 protobuf 二进制数据。

**返回值：** 一个字符串向量，长度与 obj 的行数相同。每个元素为该行数据对应的 protobuf 序列化结果。

**注意：** 目前不支持 .proto 文件中定义的 repeat 字段，且不支持嵌套的 protobuf 消息。

#### protobuf 完整示例

例1. 解析 protobuf 数据，并将输出结果。

```
// 用法1
// 通过 proto 文件创建对应的 coder
coder = EncoderDecoder::protobufDecoder("path/to/proto");
// 会直接输出解析后的数据
coder.parse(data);

// 用法2
// 获取 schmea，建表
schema = EncoderDecoder::extractProtobufSchema("path/to/proto");
outputTable = table(1:0, schema[`name], schema[`typeString]);
// 通过 proto 文件创建对应的 coder，并指定输出
coder = EncoderDecoder::protobufDecoder("path/to/proto", outputTable,3,1,0.1);
//data 为只有一列 string 列的表，存储 proto 原始数据，输出到了 outputTable 表中
coder.parseAndHandle(data);
```

例2. 将表数据序列化为 protobuf 格式并进行反序列化。

```
encoder = EncoderDecoder::protobufEncoder("path/to/proto")
rt = table(1:0, `sequence`time`securityID`market`status`side`priceType`price`volume`consult`settlType`memo`partyTraderId`institutionCode`institutionName`type, [STRING, STRING, STRING, STRING, STRING, STRING, STRING, LONG, LONG, STRING, STRING, STRING, STRING, STRING, STRING, STRING])

insert into rt values("1", "2", "3" , "4", "5", "6", "7", 8, 9, "10", "11", "12", "13", "14", "15", "16")
insert into rt values("11", "12", "13" , "14", "15", "16", "17", 18, 19, "20", "21", "22", "23", "24", "25", "26")
// 序列化
text = encoder.serialize(rt)

// 反序列化
coder = EncoderDecoder::protobufDecoder("path/to/proto")
coder.parse(text)
```
