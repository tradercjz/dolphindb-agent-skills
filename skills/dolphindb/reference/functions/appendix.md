<!-- Auto-mirrored from upstream `documentation-main/funcs/appendix.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 附录

## 格式字符与类型

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

## 首字符字节顺序，大小和对齐方式

| 字符 | 字节顺序 | 大小 | 对齐方式 |
| --- | --- | --- | --- |
| > | 大端 | 标准 | 无 |
| = | 按原字节 | 标准 | 无 |
| < | 小端 | 标准 | 无 |
| @ | 按原字节 | 按原字节 | 按原字节 |
| ! | 网络（=大端） | 标准 | 无 |
|  |  |  |  |
