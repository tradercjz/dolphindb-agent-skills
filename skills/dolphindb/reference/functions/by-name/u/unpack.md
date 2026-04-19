# unpack

## 语法

`unpack(format, buf)`

## 详情

根据 *format* 指定的格式，将 *buf* 解包成 DolphinDB
中的数据。返回一个元组，其元素为解包后的数据。

## 参数

**format** 格式字符串，用于指定数据格式。指定方式参见附录。关于格式字符串的说明：

* 格式字符之前可以带有整数表示重复计数。 例如，格式字符串 '4h' 的含义与 'hhhh' 完全相同。
* 格式之间的空白字符会被忽略；但是计数及其格式字符中不可有空白字符。
* 对于 's' 格式字符，计数会被解析为字节的长度，而不是像其他格式字符那样的重复计数；例如，'10s' 表示一个 10 字节的字节串，而
  '10c' 表示 10 个字符。 若未给出计数，则默认值为1。返回结果的字节对象长度必须恰好等于指定的字节数量。 作为特殊情况，'0c' 表示
  0 个字符。

**buf** 二进制字节流，可以是 STRING 或 BLOB 类型。*buf* 中各元素的字节大小和类型必须匹配
*format* 所要求的大小和类型。

## 返回值

一个元组，其元素为解包后的数据。

## 例子

```
res = pack("N",1);
res1 = unpack("N", res);
print(res1)
// output: (1)

res = pack("3s i", `123, 3)
res1 = unpack("3s i",  res);
print(res1)
// output: ("123",3)
```

相关函数：pack

## 附录

### 格式字符与类型

| 格式 | C 类型 | Python 类型 | DolphinDB 类型 | 范围 |
| --- | --- | --- | --- | --- |
| x | 填充字节 | 无 | VOID |  |
| c | char | 长度为1的字节串 | CHAR | -27 +1 ~ 27 -1 |
| b | signed char | integer | LONG | -27 ~ 27 -1 |
| B | unsigned char | integer | LONG | 0 ~ 28 -1 |
| ? | \_Bool | bool | LONG | -263 ~ 263 -1 |
| h | short | integer | LONG | -215 ~ 215 -1 |
| H | unsigned short | integer | LONG | 0 ~ 216 -1 |
| i | int | integer | LONG | -231 ~ 231 -1 |
| I | unsigned int | integer | LONG | 0 ~ 232 -1 |
| l | long | integer | LONG | -231 ~ 231 -1 |
| L | unsigned long | integer | LONG | 0 ~ 232 -1 |
| q | long long | integer | LONG | -263 ~ 263 -1 |
| Q | unsigned long long | integer | LONG | 0 ~ 263 -1 |
| n | ssize\_t | integer | LONG | -263 ~ 263 -1 |
| N | size\_t | integer | LONG | 0 ~ 263 -1 |
| f | float | float | LONG | -3.40E+38 ~ +3.40E+38 |
| d | double | float | LONG | -1.79E+308 ~ +1.79E+308 |
| s | char[] | bytes | STRING |  |
| p | char[] | bytes | STRING |  |
| P | void\* | integer | LONG | -263 ~ 263 -1 |

### 首字符字节顺序，大小和对齐方式

| 字符 | 字节顺序 | 大小 | 对齐方式 |
| --- | --- | --- | --- |
| > | 大端 | 标准 | 无 |
| = | 按原字节 | 标准 | 无 |
| < | 小端 | 标准 | 无 |
| @ | 按原字节 | 按原字节 | 按原字节 |
| ! | 网络（=大端） | 标准 | 无 |

默认情况下，C 类型以本机格式和字节顺序表示，在必要时通过跳过填充字节进行正确对齐（根据 C 编译器使用的规则）。

格式字符串的第一个字符可用于指示打包数据的字节顺序，大小和对齐方式，见首字符字节顺序，大小和对齐方式部分内容。
如果第一个字符不是其中之一，则按 '@' 处理。
