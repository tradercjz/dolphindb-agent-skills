# strReplace

## 语法

`strReplace(str, pattern, replacement)`

## 详情

返回 *str* 的副本。如果 *str* 包含 *pattern*，则将
*pattern* 替换为 *replacement*。

## 参数

**str** 是目标字符串。它可以是标量或向量。

**pattern** 是被替换的字符串。

**replacement** 是替换的字符串。

## 返回值

STRING 类型标量或向量。

## 例子

```
strReplace("The ball is red.", "red", "green");
// output
The ball is green.

strReplace(["The ball is red.", "The car is red too."], "red", "yellow");
// output
["The ball is yellow.","The car is yellow too."]
```
