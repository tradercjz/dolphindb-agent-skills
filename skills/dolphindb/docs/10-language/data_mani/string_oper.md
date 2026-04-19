<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/string_oper.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 字符串操作

(1) strReplace 函数和 regexReplace 函数都能够替换字符串中的一部分。两者的区别在于，*regexReplace*
函数可以用正则表达式表示替换内容，并且能够指定开始搜索的位置。

```
strReplace("this computer is faster than that computer", "computer", "desktop");
// output
this desktop is faster than that desktop

regexReplace("this computer is faster than that computer", "computer", "desktop", 8);
// output
this computer is faster than that desktop

regexReplace("this computer is faster than that computer", "\\b(comp)([^ ]*)", "desktop");
// output
this desktop is faster than that desktop
```

(2) left 函数和 right 函数能够分别截取左边和右边指定长度的字符串。substr 和 substru 函数能够指定开始截取的位置和长度。

```
left("Hello World", 5);
// output
Hello

right("Hello World", 5);
// output
World

substr("This is a test", 5, 2);
// output
is
```

(3) ltrim 函数和 rtrim 函数能够分别去除字符串左边和右边的空格，trim 函数能够去除字符串首尾的空格。strip 函数不仅能够去除字符串首尾的空格，还能去除字符串首位的制表符、换行符和回车符。

```
ltrim("     Hello World   ");
// output
Hello World

rtrim("Hello World   ")+"!";
// output
Hello World!

trim("     Hello World   ")+"!";
// output
Hello World!

strip("   \t  Hello World   ");
// output
Hello World
```

(4) lpad 函数和 rpad 函数能够分别在字符串左侧和右侧填充指定字符串。

```
lpad("Hello",7);
// output
Hello

lpad("Hello",7,"0");
// output
00Hello

rpad("Hello",7,"0");
// output
Hello00
```

(5) repeat 函数能够返回字符串重复多次后的结果。

```
repeat("ABC",3);
// output
ABCABCABC

repeat(`ABC`DE,3);
// output
["ABCABCABC","DEDEDE"]
```

(6) lower 函数能够把字符串中的字母转换成小写形式，upper 函数能够把字符串中的字母转换成大写形式。

```
lower `Chloe;
// output
chloe

upper 'Christmas';
// output
CHRISTMAS
```

(7) concat 函数可以连接两个字符串。

```
concat (`hello, `world);
// output
helloworld
```

我们也可以使用运算符(+)来连接多个字符串。

```
var1="Hello"
var2='World'
var1+", "+var2+"!";
// output
Hello, World!
```

(8) split 函数可以分割字符串。

```
split("xyz 1 ABCD 3241.32"," ");
// output
["xyz","1","ABCD","3241.32"]

split("XOM|2018.02.15|76.21", "|");
// output
["XOM","2018.02.15","76.21"]
```

(9) strlen 函数能够计算字符串的长度。

```
strlen("Hello World!");
// output
12

strlen(`XOM`MSFT`F`GM);
// output
[3,4,1,2]
```

wc 函数能够计算字符串中的单词数。

```
wc(`apple);
// output
1

wc("This is a 7th generation iphone!");
// output
6

wc("This is a 7th generation iphone!" "I wonder what the 8th generation looks like");
// output
[6,8]
```

regexCount 函数能够计算一个子字符串在字符串中出现的次数。子字符串可以用正则表达式表示。

```
regexCount("FB IBM FB IBM AMZN IBM", `IBM);
// output
3

regexCount("FB IBM FB IBM AMZN IBM", `IBM, 7);
// output
2

regexCount("this subject has a submarine as subsequence", "\\b(sub)([^ ]*)");
// output
3
```

(10) startsWith 函数和 endsWith 函数能够检查字符串是否以某个字符串开头和结尾。

```
startsWith('ABCDEF!', "ABC");
// output
1

startsWith('ABCDEF!', "ABD");
// output
0

endsWith('ABCDEF!', "F!");
// output
1

endsWith('ABCDEF!', "E!");
// output
0
```

(11) convertEncode 函数能够转换字符串编码，fromUTF8 函数能够将UTF-8编码的字符串转换成其他编码，toUTF8 函数能够将其他编码的字符串转换成UTF-8编码。

```
convertEncode(["hello","DolphinDB"],"gbk","utf-8");
// output
["hello","DolphinDB"]

fromUTF8(["hello","DolphinDB"],"gbk");
// output
["hello","DolphinDB"]

toUTF8(["hello","DolphinDB"],"gbk");
// output
["hello","DolphinDB"]
```

(12) charAt 函数可以获取字符串中指定位置的字符。

```
s=charAt("abc",2);
s;
// output
'c'

typestr(s);
// output
CHAR

charAt(["hello","world"],[3,4]);
// output
['l','d']
```

(13) isAlpha 函数可以判断字符串是否全为字母，isUpper 函数可以判断字符串中的字母是否全为大写，isLower 函数可以判断字符串中的字母是否全为小写，isTitle 函数可以判断字符串中每个单词是否为首字母大写，其他字母小写。

```
isAlpha(["hello","hello world","1And1",string()]);
// output
[true,false,false,false]

isUpper("123456ABC");
// output
true

isLower("123456abc");
// output
true

isTitle("Hello World");
// output
true
```

(14) isNumeric, isDigit 可以判断字符串是否全部为数字，isAlNum 函数可以判断字符串是否全部为字母或数字。

```
isNumeric("123456");
// output
true

isDigit("1And1");
// output
false

isAlNum("123456abc");
// output
true
```

(15) isSpace 可以判断字符串是否由空格类字符（包括空格、回车符、换行符、跳格符）组成。

```
isSpace(" \t ");
// output
true
```
