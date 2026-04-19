# isNumeric

## 语法

`isNumeric(X)`

## 详情

判断 *X* 是否只包含数字。如果 *X* 中的所有字符都是数字，该函数返回 true，反之返回
false。对于空字符串（STRING 类型的 NULL 值），该函数返回 false。

注：

该函数和 isDigit
等价，可任选其一使用。

## 参数

**X** 是字符或字符串类型的标量、向量或表。

## 返回值

* 当 *X* 是标量时，返回布尔标量。
* 当 *X* 是向量时，返回布尔向量。
* 当 *X* 是表时，返回一个表。

## 例子

```
isNumeric("123456");
// output: true

isNumeric("1And1");
// output: false

isNumeric("10.05");
// output: false

isNumeric(string());
// output: false
```
