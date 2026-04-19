<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/create_strings.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 创建字符串

可以通过以下方法来创建字符串：

(1) 使用双引号，单引号或反引号(`)。

注意：

* 不能使用反引号创建包含空格或标识符的字符串。
* 我们可以用反引号或双引号来创建只包含一个字符的字符串，不能使用单引号，否则会被识别为CHAR类型。

```
var1='DolphinDB version 1.1';
var2="This is DolphinDB";
var3=`DolphinDB;
var4=['IBM', 'MSFT', 'GOOG', 'FB'];
var5=["IBM","MSFT","GOOG","FB"];
var6=`IBM`MSFT`GOOG`FB;
typestr(`C);
// output
STRING

typestr("C");
// output
STRING

typestr('C');
// output
CHAR
```

(2) 使用函数 string.

```
var7=string(108.5);
```

(3) 使用函数 format。*format*
函数会把指定格式应用到对象，并生成一个字符串标量或向量。*format* 函数会根据输入数据的数据类型，来决定调用 decimalFormat 还是 temporalFormat.

```
t = table(1..100 as id, (1..100 + 2018.01.01) as date, rand(100.0, 100) as price, rand(10000, 100) as qty);
t;
```

| id | date | price | qty |
| --- | --- | --- | --- |
| 1 | 2018.01.02 | 70.832104 | 1719 |
| 2 | 2018.01.03 | 12.22557 | 6229 |
| 3 | 2018.01.04 | 8.695886 | 1656 |
| 4 | 2018.01.05 | 24.324535 | 2860 |
| 5 | 2018.01.06 | 0.443173 | 6874 |
| 6 | 2018.01.07 | 90.302176 | 3277 |
| 7 | 2018.01.08 | 78.556843 | 3424 |
| 8 | 2018.01.09 | 45.836447 | 8636 |
| 9 | 2018.01.10 | 57.416425 | 707 |
| 10 | 2018.01.11 | 98.879764 | 2267 |
| ... | ... | ... | ... |

```
t1=select id, date.format("MM/dd/yyyy") as date, price.format("00.00") as price, qty.format("#,###") as qty from t;
t1;
```

| id | date | price | qty |
| --- | --- | --- | --- |
| 1 | 01/02/2018 | 70.83 | 1,719 |
| 2 | 01/03/2018 | 12.23 | 6,229 |
| 3 | 01/04/2018 | 08.70 | 1,656 |
| 4 | 01/05/2018 | 24.32 | 2,860 |
| 5 | 01/06/2018 | 00.44 | 6,874 |
| 6 | 01/07/2018 | 90.30 | 3,277 |
| 7 | 01/08/2018 | 78.56 | 3,424 |
| 8 | 01/09/2018 | 45.84 | 8,636 |
| 9 | 01/10/2018 | 57.42 | 707 |
| 10 | 01/11/2018 | 98.88 | 2,267 |
| ... | ... | ... | ... |

```
t1.date.typestr();
// output
STRING VECTOR
```

下表展示了 *decimalFormat* 函数中使用到的符号的意义。详情请参考 ParsingandFormatofTemporalVariables.

| 符号 | 含义 | 备注 |
| --- | --- | --- |
| 0 | 强制数字位数 | 备注1 |
| # | 可选数字位数 | 备注2 |
| . | 小数点 |  |
| % | 百分号 | 备注3 |
| E | 科学计数法的符号 | 备注4 |
| , | 分隔符 | 备注5 |
| ; | 表示正数和负数的符号 | 备注6 |

* 备注1：小数点之前0的个数表示整数部分的位数。与之对比，小数点之后0的个数表示小数部分的位数。

  ```
  decimalFormat(123,"0");
  // output
  123

  decimalFormat(123,"00000");
  // output
  00123

  decimalFormat(123.45,"0");
  // output
  123

  decimalFormat(123.45,"0.0");
  // output
  123.5

  decimalFormat(123.45,"0.000");
  // output
  123.450

  decimalFormat(123.45, ".0");
  // output
  123.5

  decimalFormat(0.45, ".0");
  // output
  .5
  ```
* 备注2：如果0与#同时在小数点后使用，0必须在#前面。

  ```
  decimalFormat(123.45,"0.#");
  // output
  123.5

  decimalFormat(123.45,"0.###");
  // output
  123.45

  decimalFormat(123.456,"0.000###");
  // output
  123.456

  decimalFormat(123.456789110,"0.000###");
  // output
  123.456789

  decimalFormat(0.345, ".##");
  // output
  .35
  ```
* 备注3：%用于格式字符串的结尾。%和E在一个格式字符串中不能同时出现。

  ```
  decimalFormat(0.125,"0.00%");
  // output
  12.50%

  decimalFormat(0.125, "#.##%");
  // output
  12.5%

  decimalFormat(0.12567,"#.##%");
  // output
  12.57%
  ```
* 备注4：E后面只能为0，并且至少一个0。

  ```
  decimalFormat(1234567.89,"0.##E00");
  // output
  1.23E06

  decimalFormat(0.0000000000123456789,"0.000E0");
  // output
  1.235E-11
  ```
* 备注5：分隔符在一个格式字符串中只能出现一次。分隔符与小数点之间的位数或分隔符到结尾的位数即为分隔的间距。

  ```
  decimalFormat(123456789,"#,###");
  // output
  123,456,789

  decimalFormat(123456789.166,"#,###.##");
  // output
  123,456,789.17

  decimalFormat(123456789.166,"0,000.00");
  // output
  123,456,789.17
  ```
* 备注6：若希望变量为正与为负时格式不同，可使用";"来分隔正与负时的格式。

  ```
  decimalFormat(123.456,"0.00#E00;(0.00#E00)");
  // output
  1.235E02

  decimalFormat(-123.456,"0.00#E00;(0.00#E00)");
  // output
  (1.235E02)
  ```

(4) 使用转义字符。

| 转义字符 | 意义 |
| --- | --- |
| \n | 换行 |
| \r | 回车 |
| \t | Tab键 |
| \ \ | 反斜杠'' |
| ' | 单引号 |
| " | 双引号 |

```
x="ABC\\DEF";
x;
// output
ABC\DEF

x="ABC\"D\'EF";
x;
// output
ABC"D'EF
```

若字符串里只有一种引号，最简便的方式为使用另一种引号创建此字符串。

```
x="ABC'D'EF";
x;
// output
ABC'D'EF

x='ABC"DEF';
// output
4 x;
ABC"DEF
```
