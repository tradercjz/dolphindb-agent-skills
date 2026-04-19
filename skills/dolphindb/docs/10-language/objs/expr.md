<!-- Auto-mirrored from upstream `documentation-main/progr/objs/expr.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 表达式

表达式由对象和运算符组成。表达式中的对象可以是常量、变量、函数、表达式等。

```
3>2;
// output
1

x=true;
!x;
// output
0

x=1 2 3
x*2;
// output
[2,4,6]

y = 4 5 6;
x+y;
// output
[5,7,9]

x+y*2;

(y-avg(y))*(y-avg(y));
// output
[1,0,1]

t1 = table(x,y);
t1.y[0]\sum(t1.y);
// output
0.266667
```

## 正则表达式

正则表达式（Regular
Expression）是一种用于匹配字符串模式的工具。它是由字符和特殊字符组成的序列，用于定义搜索模式。在文本处理和数据提取中，正则表达式是一种非常强大和灵活的工具，可以帮助我们快速、准确地搜索、替换和提取字符串。

DolphinDB 支持使用正则表达式进行文本匹配和处理。DolphinDB 在不同操作系统下采用不同的正则表达式标准，具体如下：

* 在 Linux 版本的 DolphinDB 中，使用基于 POSIX 标准的扩展正则表达式（Extended Regular Expressions,
  ERE）。
* 在 Windows 版本的 DolphinDB 中，使用 C++ 标准库的扩展正则表达式。

### Linux 版本（POSIX 扩展正则表达式支持）

POSIX 扩展正则表达式是基于 POSIX 标准的正则表达式，在此基础上增加了一些功能，使其更加强大和灵活。DolphinDB 的 Linux 版本使用
POSIX 扩展正则表达式作为默认的正则表达式标准。POSIX 扩展正则表达式提供了丰富的功能，可用于实现复杂的文本匹配和处理需求。

以函数 regexFind 为例，介绍正则表达式在 regexFind，regexCount 和 regexReplace 等函数中的应用：

POSIX 扩展正则表达式支持的功能包括但不限于：

### 元字符

* .：匹配除换行符外的任何单个字符。

匹配一个以 a 开头，紧接着是任意单个字符，然后是 c 结尾的字符串

```
regexFind(str="waabuamc", pattern="a.c")
```

* ^：匹配输入字符串的开始。

匹配字符串开始的字符 w

```
regexFind(str="waabuamc", pattern="^w")
```

* $：匹配输入字符串的结尾。

匹配字符串结束的字符 c

```
regexFind(str="waabuamc", pattern="c$")
```

* \*：匹配前一个字符零次或多次。

匹配字符 a 零次或多次

```
regexFind(str="waabuamc", pattern="a*")
```

* +：匹配前一个字符一次或多次。

匹配字符 a 一次或多次

```
regexFind(str="waabuamc", pattern="a+")
```

* ?：匹配前一个字符零次或一次。

匹配字符 a 零次或一次

```
regexFind(str="waabuamc", pattern="a?")
```

* \\：转义字符，用于取消元字符的特殊含义。

匹配字符 '.'

```
regexFind(str="abcdef.gh", pattern="\\.")
```

### 字符类

* [...]：字符类，匹配其中的任何一个字符。

匹配 a 到 e 之间的字符

```
regexFind(str="hello 123", pattern="[a-e]")
```

匹配任意数字字符

```
regexFind(str="hello 123", pattern="[0-9]")
```

* [^...]：否定字符类，匹配除其中字符之外的任何字符。

匹配 a-n 之外的字符

```
regexFind(str="hello 123", pattern="[^a-n]")
```

* \\w：匹配任何字母、数字或下划线字符。

```
regexFind(str="hello 123", pattern="\\w")
```

* \\s：匹配任何空白字符，空白字符包括空格，制表符(\t)，回车符(\t)，换行符(\n)，垂直换行符(\v)，换页符(\f)等

```
regexFind(str="hello 123", pattern="\\s")
```

* \\S：匹配任何非空白字符

```
regexFind(str="\thello 123", pattern="\\S")
```

### 量词

* {n}：匹配前一个字符恰好 n 次。

匹配字符 a 出现 3 次

```
regexFind(str="wwabcaaefgaaa", pattern="a{3}")
```

* {n,}：匹配前一个字符至少 n 次。

匹配字符 a 出现 2 次以上

```
regexFind(str="wwabcaaefgaaa", pattern="a{2,}")
```

* {n,m}：匹配前一个字符至少 n 次，但不超过 m 次。

匹配字符 a 出现 2 次到 3 次

```
regexFind(str="wwabcaaefgaaa", pattern="a{2,3}")
```

### 锚点

* \\<：匹配单词的开始。

匹配以 a 开头的单词

```
regexFind(str="eat an apple", pattern="\\<a")
```

* \\>：匹配单词的结尾。

匹配以 e 结尾的单词

```
regexFind(str="eat an apple", pattern="e\\>")
```

* \\b：匹配单词边界。

例如 \\ba 与 \\<a 等效，e\\> 与 e\\b 等效。

### POSIX 字符类

* [:alnum:]：匹配任何字母数字字符。

匹配一个任意字母或任意数字字符

```
regexFind(str="wX02.sz0x0X", pattern="[[:alnum:]]")
```

* [:alpha:]：匹配任何字母字符。

匹配一个任意字母字符

```
regexFind(str="wX02.sz0x0X", pattern="[[:alpha:]]")
```

* [:digit:]：匹配任何数字字符。

匹配一个任意数字字符

```
regexFind(str="wX02.sz0x0X", pattern="[[:digit:]]")
```

### Windows 版本（C++ 标准库扩展正则表达式支持）

Windows 版本的 DolphinDB 使用 C++ 标准库提供的正则表达式功能。

C++ 标准库扩展正则表达式支持的功能包括但不限于：

* 元字符：.、^、$、\*、+、?、\\ 等
* 字符类：[...]、[^...] 等
* 量词：{n}、{n,}、{n,m} 等
* 锚点：\\<、\\> 、\\b等

C++ 标准库的正则表达式功能在 Windows 平台上提供了强大的文本处理能力，支持更多的特性和语法。

例如，除了支持 Linux 版本已支持的语法，还支持
Lookaround，下面用到的表达式\+(?![^(\)]\*\))，用于找没被括号包围的加号。

```
trimedString = "200 + 1000(明天+0)"
volString = regexReplace(trimedString, "\\+(?![^(\\)]*\\))", " ")
print(volString)
```
