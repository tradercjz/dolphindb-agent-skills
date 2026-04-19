# lpad

## 语法

`lpad(str, length, [pattern])`

## 详情

在 *str* 的左边填充指定字符串。

当 *str* 是表时，函数仅作用于其中字符串列，其他类型的列将被忽略。

## 参数

**str** 是字符串类型的标量、向量，或表。它表示目标字符串。

**length** 是一个不超过 65536 的非负整数，表示填充之后的字符串长度。如果 *length* 小于
*str* 的长度，*lpad* 函数相当于 left (str,
length). 如果 *length* 大于 65536，则系统会自动调整为 65536。

**pattern** 是填充字符串。它是一个可选参数。如果 *pattern* 没有指定，则在
*str* 的左边填充空格。

## 返回值

返回与 *str* 形式一致的字符串类型。

## 例子

```
lpad("Hello",2);
// output
He

lpad(`Hello, 10);
// output
Hello

lpad(`Hello, 12, `0);
// output
0000000Hello
```
