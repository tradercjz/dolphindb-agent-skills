<!-- Auto-mirrored from upstream `documentation-main/progr/data_types.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 数据类型

## 数据类型表

| 分类 | 名称 | ID | 举例 | 符号 | 字节数 | 范围 |
| --- | --- | --- | --- | --- | --- | --- |
| VOID | VOID | 0 | NULL |  | 1 |  |
| LOGICAL | BOOL | 1 | 1b, 0b, true, false | b | 1 | 0~1 |
| INTEGRAL | CHAR | 2 | ‘a’, 97c | c | 1 | -2 7 +1~2 7 -1 |
| SHORT | 3 | 122h | h | 2 | -2 15 +1~2 15 -1 |
| INT | 4 | 21 | i | 4 | -2 31 +1~2 31 -1 |
| LONG | 5 | 22l | l | 8 | -2 63 +1~2 63 -1 |
| COMPRESSED | 26 |  |  | 1 | -2 7 +1~2 7 -1 |
| TEMPORAL | DATE | 6 | 2013.06.13 | d | 4 |  |
| MONTH | 7 | 2012.06M | M | 4 |  |
| TIME | 8 | 13:30:10.008 | t | 4 |  |
| MINUTE | 9 | 13:30m | m | 4 |  |
| SECOND | 10 | 13:30:10 | s | 4 |  |
| DATETIME | 11 | 2012.06.13 13:30:10 or 2012.06.13T13:30:10 | D | 4 | [1901.12.13T20:45:53, 2038.01.19T03:14:07] |
| TIMESTAMP | 12 | 2012.06.13 13:30:10.008 or 2012.06.13T13:30:10.008 | T | 8 |  |
| NANOTIME | 13 | 13:30:10.008007006 | n | 8 |  |
| NANOTIMESTAMP | 14 | 2012.06.13 13:30:10.008007006 or 2012.06.13T13:30:10.008007006 | N | 8 | [1677.09.21T00:12:43.145224193, 2262.04.11T23:47:16.854775807] |
| DATEHOUR | 28 | datehour(2012.06.13 13:30:10) |  | 4 |  |
| FLOATING | FLOAT | 15 | 2.1f | f | 4 | 有效位数: 06~09 位 |
| DOUBLE | 16 | 2.1 | F | 8 | 有效位数: 15~17 位 |
| LITERAL | SYMBOL | 17 |  | S | 4 |  |
| STRING | 18 | “Hello” or ‘Hello’ or `Hello | W | 不超过 65,535 |  |
| BLOB | 32 |  |  |  |  |
| BINARY | INT128 | 31 | e1671797c52e15f763380b45e841ec32 |  | 16 | -2 127 +1~2 127 -1 |
| UUID | 19 | 5d212a78-cc48-e3b1-4235-b4d91473ee87 |  | 16 |  |
| IPADDR | 30 | 192.168.1.13 |  | 16 |  |
| POINT | 35 | (117.60972, 24.118418) |  | 16 |  |
| SYSTEM | FUNCTIONDEF | 20 | def f1(a,b) {return a+b;} |  |  |  |
| HANDLE | 21 | file handle, socket handle, and db handle |  |  |  |
| CODE | 22 | <1+2> |  |  |  |
| DATASOURCE | 23 |  |  |  |  |
| RESOURCE | 24 |  |  |  |  |
| DURATION | 36 | 1s, 3M, 5y, 200ms |  | 4 |  |
| INSTRUMENT | 42 | ``` bond = {     "productType": "Cash",     "assetType": "Bond",     "bondType": "DiscountBond",     "instrumentId": "259924.IB",     "start": 2025.04.17,     "maturity": 2025.07.17,     "issuePrice": 99.664,     "dayCountConvention": "ActualActual" } instrument = parseInstrument(bond) ``` |  |  |  |
| MKTDATA | 43 | ``` eqSpot = {     "mktDataType": "Spot",     "referenceDate": 2025.06.07,     "spotType": "EqSpot",     "value": 3461.66,     "unit": "CNY" } mktData=parseMktData(eqSpot) ``` |  |  |  |
| MIXED | ANY | 25 | (1,2,3) |  |  |  |
| ANY DICTIONARY | 25 | {a:1,b:2} |  |  |  |
| OTHER | COMPLEX | 34 | 2.3+4.0i |  | 16 |  |
| DECIMAL | DECIMAL32(S) | 37 | 3.1415926$DECIMAL32(3) |  | 4 | (-1\*10^(9-S), 1\*10^(9-S)) |
| DECIMAL64(S) | 38 | 3.1415926$DECIMAL64(3), , 3.141P | P | 8 | (-1\*10^(18-S), 1\*10^(18-S)) |
| DECIMAL128(S) | 39 | 3.1415926$DECIMAL128(3) |  | 16 | (-1\*10^(38-S), 1\*10^(38-S)) |
| ARRAY | 基础类型+方括号 “[]“，如 INT[]，DOUBLE[]，DECIMAL32(3)[] 等，表示数组类型 | 基础类型 ID+64 | array(INT[], 0, 10).append!([1 2 3, 4 5, 6 7 8, 9 10]) |  |  |  |

说明：

1. 上表除以下类型外，都支持作为表字段：VOID, FUNCTIONDEF, HANDLE, CODE, DATASOURCE,
   RESOURCE, COMPRESS, DURATION。
2. DolphinDB 中字符串类型包含 STRING, BLOB 与 SYMBOL 类型。
   * BLOB 类型不支持任何计算。其在内存中大小不受限制，但写入分布式数据库时存在大小上限。
   * SYMBOL 是特殊的字符串类型。某个表字段定义为 SYMBOL
     类型时，必须保证每个分区内该字段的不同取值小于2097152(221)个，否则会报错
     `"One symbase's size can't exceed 2097152"`。
   * 自 1.30.23/2.00.11 版本起，向分布式数据库写入数据时对这三种 类型数据增加了大小限制：
     + 写入的 STRING 类型数据应小于 64 KB，否则系统会截断到 65,535 字节（即 64 KB - 1
       字节）；
     + 写入的 BLOB 类型数据应小于 64 MB，否则系统会截断到 67,108,863 字节（即 64 MB - 1
       字节）；
     + 写入的 SYMBOL 类型数据超过 255 字节时，系统会抛出异常。

     注：

     已存在数据库中超出范围限制的数据仍然可以正常读取使用。
3. ANY DICTIONARY 是 DolphinDB 中表示 JSON 的数据类型。
4. COMPRESS 类型目前只能通过 compress 函数生成。
5. BLOB 类型不支持任何计算。
6. DURATION 类型可以通过 duration 函数生成或直接使用整数数字加以下时间单位（区分大小写）： y, M, w, d, B, H, m, s, ms,
   us, ns。DURATION 数据的范围为-2 31 +1~2 31
   -1，如果数据溢出，则溢出的数据处理为空值。DURATION
   类型数据之间不能进行任何运算。例如，不能进行比较运算：`duration('20ms') >=
   duration('10ms')`。
7. DOUBLE 和 FLOAT 类型精度遵循 IEEE 754 标准；该类型数据溢出时，会被处理为 NULL。
8. DECIMAL32(S)，DECIMAL64(S) 及 DECIMAL128(S) 中的 S
   表示保留的小数位数，其中，DECIMAL32(S) 中 S 的有效范围为[0, 9]，DECIMAL64(S) 中 S 的有效范围为[0,
   18]，DECIMAL128(S) 中 S 的有效范围为 [0,38]。DECIMAL32 底层存储使用 int32\_t 类型，占用4个字节；DECIMAL64
   底层存储使用 int64\_t 类型，占用8个字节；DECIMAL128 底层存储使用 int128\_t 类型，占用16个字节。DECIMAL32(0)
   可以表示的有效整数范围为 [-999999999, 999999999]， 而 4 字节整数（INT32）的范围为 [-2,147,483,648,
   2,147,483,647]。因此将数值型数据强制转换为 DECIMAL32 时，若该数值的整数部分超过 DECIMAL32 的有效数值范围， 但仍属于
   [-2147483648, 2147483647] 范围，可以转换成功。而将字符串强制转换成 DECIMAL32
   时，会进行位数校验，若字符串长度超过有效位数，则抛出异常。

   ```
   decimal32(1000000000, 0)
   ```

   得到：1000000000

   ```
   decimal32(`1000000000, 0)
   ```

   得到：`Can't
   convert STRING to DECIMAL32(0): parse 1000000000 to
   DECIMAL32(0) failed: decimal overflow`
9. INSTRUMENT 和 MKTDATA 是 DolphinDB
   中用于表示金融工具和市场数据的类型。具有以下限制:
   * 创建包含 INSTRUMENT或 MKTDATA 类型的分布式表时，仅支持 TSDB 存储引擎。
   * INSTRUMENT 和 MKTDATA 类型列不支持作为
     `keyedTable`/`indexedTable`/`keyedStreamTable`/`latestKeyedTable`/`latestIndexedTable`/`latestKeyedStreamTable`
     的主键列。
   * INSTRUMENT 和 MKTDATA 类型不支持一元或二元运算符。

## 类型检查

typestr 和 type 这两个函数用于检查数据类型。**typestr**
返回的是数据类型的名称（字符串常量）；**type** 返回的是数据类型 ID（整数）。

```
typestr 3l;
```

得到：LONG

```
type 3l;
```

得到：5

```
x=3;
if(type(x) == INT){y=10};
y;
```

得到：10

## 数据范围

整型的数据范围在上面表格中已经列出。对于整数类型的数据，DolphinDB 使用允许最小值-1来表示其相应的 NULL
值。例如，-128c 是一个 NULL 字符。对于 NULL 值，参考： NULL
值。

```
x=-128c;
x;
```

得到：00c

```
typestr x;
```

返回：CHAR

## 数据类型符号

数据类型符号用于声明常量的数据类型。在下面的第一个例子中，没有为3指定数据类型符号。在这种情况，3被默认作为整数存储在内存中。如果要保存为浮点数，则应声明为
3f(float) 或 3F(double)。

```
typestr 3;
```

返回：INT

```
typestr 3f;
```

返回：FLOAT

```
typestr 3F;
```

返回：DOUBLE

```
typestr 3l;
```

返回：LONG

```
typestr 3h;
```

返回：SHORT

```
typestr 3c;
```

返回：CHAR

```
typestr 3b;
```

返回：BOOL

```
typestr 3P;
```

返回：DECIMAL64

## 字符串

我们可以在 DolphinDB 中把字符串保存为 symbol 类型数据。一个 symbol 类型数据被 DolphinDB
系统内部存储为一个整数，因此数据排序和比较更有效率。因此，使用 symbol
类型有可能提高系统性能，同时也可节省存储空间。但是，将字符串映射到整数（hash）需要时间，哈希表也会占用内存。以下规则可以帮助您决定是否使用 symbol
类型：

* 如果字符串数据较少重复，应当避免使用 symbol 类型。
* 如果字符串数据不会被排序、搜索或比较，应当避免使用 symbol 类型。

两个例子：

* 股票交易数据中的股票代码应该使用 symbol
  类型，因为股票代码的数量基本是固定的，在数据中重复极多；另外，股票代码经常被搜索和比较。
* 描述性字段不应该使用 symbol 类型，因为描述性字段很少重复，而且很少被搜索、排序或比较。

例1：排序比较：同样排序 300 万条记录，排序 SYMBOL 向量比 STRING 快 26 倍。

```
n=3000000
strs=array(STRING,0,n)
strs.append!(rand(`IBM`C`MS`GOOG, n))
timer sort strs;
```

返回：Time elapsed: 184.642 ms

```
n=3000000
syms=array(SYMBOL,0,n)
syms.append!(rand(`IBM`C`MS`GOOG, n))
timer sort syms;
```

返回：Time elapsed: 7.001 ms

例2：布尔运算比较：同样是 300 万条记录的运算，SYMBOL 向量几乎是 STRING 向量的 9 倍。

```
timer(100){strs>`C};
```

返回：Time elapsed: 1463.841 ms

```
timer(100){syms>`C};
```

返回：Time elapsed: 157.962 ms

## 整数溢出

DolphinDB 的整型是有符号的。对于有符号整型，在进行运算时，如果结果超出了其类型的正数范围或负数范围，将会发生溢出。DolphinDB
采用二进制补码溢出：计算机系统中使用补码表示有符号整数。当溢出发生时，系统会将结果的高位截断，保留低位作为最终结果。

下例中，变量 x 的数据类型为 INT，它被赋予 INT 类型允许的最大值，为 2 31-1。

```
x=(pow(2,31)-1)$INT;
x+1
// x+1 的结果超出 INT 类型的上限，二进制补码后得到 INT 类型的负数最小值，它在 DolphinDB 中被处理为 NULL。
// output
null

x+3;
// x+3 的结果超出 INT 类型的上限，二进制补码后得到 -2147483646。
// output
-2147483646
```
