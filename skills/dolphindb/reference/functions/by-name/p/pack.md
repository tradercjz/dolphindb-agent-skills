# pack

## 语法

`pack(format, args...)`

## 详情

将数据按照 *format* 指定的格式打包成二进制字节流。

## 参数

**format** 格式字符串，用于指定数据格式。指定方式参见附录。关于格式字符串的说明：

* 格式字符之前可以带有整数表示重复计数。 例如，格式字符串 '4h' 的含义与 'hhhh' 完全相同。
* 格式之间的空白字符会被忽略；但是计数及其格式字符中不可有空白字符。
* 对于 's' 格式字符，计数会被解析为字节的长度，而不是重复计数；例如，'10s' 表示一个 10 字节的字节串，而 '10c' 表示 10 个字符。
  若未给出计数，则默认值为1。字节串会被适当地截断或填充空字节以符合要求。

**args...** 表示需要进行打包的数据。参数个数与 *format* 的长度一致。每个参数的类型与对应位置的
*format* 类型一致。

## 返回值

一个 bytes 对象，包含 *args* 数据按照格式字符串 *format* 打包后的值。

## 例子

```
res = pack("N",1);
res1 = unpack("N", res);
print(res1)
// output
(1)

res = pack("iii", 1, 2, 3)
res1 = unpack("iii",  res);
print(res1)
// output
(1,2,3)

res = pack("x",NULL)
res = unpack("x",pack("x",NULL))
typestr(res[0])
// output
VOID

res = pack("3si", `123, 3)
res1 = unpack("3si",  res);
print(res1)
// output
("123",3)
```

相关函数：unpack

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
