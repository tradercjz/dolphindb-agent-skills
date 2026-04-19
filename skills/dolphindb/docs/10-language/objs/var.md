<!-- Auto-mirrored from upstream `documentation-main/progr/objs/var.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 变量

变量可以存储任何类型的数据。

## 命名规则

1. 可以用字母，数字或者下划线定义变量名称。
2. 必须以字母开头。

有效变量名：

```
x1 = 5;

varName = `TEST;

file_name = "text.txt";
```

无效变量名：

```
x.1 = 5;

var~2 = 7;

file-name = 6;

1x = 5;
```

## 变量举例

```
m=matrix(INT,3,3);

z = dict(INT,DOUBLE);

x = 1..10;

x = true;
```

变量的值可修改。在下列例子中，x被定义为整型向量，但是也能变成双精度向量。

```
x=1 2 3;
x;
// output
[1,2,3]

x=3.5 4.5;
x;
// output
[3.5,4.5]
```

## 变量和变量名称

变量和变量名称是不同的概念。变量是对象的占位符。变量名称是字符串。要引用变量，我们不需要引用变量名。DolphinDB提供了几个内置函数来操作变量。例如，undef 用于取消一个或多个变量定义，而 defined 用于检查是否存在一个或多个变量。这些函数是以变量名作为输入参数，而不是变量引用的对象。

一些内置函数的参数是数据类型，例如，定义数组、矩阵、字典、集合、函数等。DolphinDB有三种表示数据类型的方式。第一种是类型枚举，如INT,
DOUBLE和BOOL。它们使用大写字母并作为系统的保留字符（即这些字符不能作为列名、变量名或函数名使用），我们推荐使用这种方法； 第二种是使用类型函数名，如int,
long, string, double,
bool等，这些词汇可以用作变量名。如果数据类型名称被用作局部变量，我们应该避免使用这种方法。第三种是引用类型名称（如字符串）。

系统保留字与关键字

保留字在DolphinDB系统中有特殊的意义，不可用作变量名。保留字有以下几类：

1. 数据类型： VOID, BOOL, CHAR, SHORT, INT, LONG, DATE, MONTH, TIME, MINUTE, SECOND,
   DATETIME, TIMESTAMP, NANOTIME, NANOTIMESTAMP, FLOAT, DOUBLE, SYMBOL, STRING,
   UUID, FUNCTIONDEF, HANDLE, CODE, DATASOURCE, RESOURCE, ANY, IPADDR, INT128,
   BLOB, COMPLEX, POINT, DURATION
2. 数据形式： SCALAR, PAIR, VECTOR, MATRIX, SET, DICT, TABLE
3. 图表类型： LINE, PIE, COLUMN, BAR, AREA, HISTOGRAM, SCATTER
4. 分区类型： VALUE, RANGE, HASH, LIST, COMPO
5. 用于函数 undef： VAR, SHARED, DEF
6. 用于函数 seek： HEAD, CURRENT, TAIL
7. 特殊数值： NULL, pi, e

关键字在DolphinDB脚本语言中有特定含义，成为语法中一部分，亦不可用作变量名。关键字包括以下几类：

1. 循环语句： for, do, if, continue, break
2. SQL语句： select, exec, delete, update
3. Boolean值：true, false
4. 函数定义： def, return
5. 模块： module, use
6. 异常信息： try, throw
7. 其它： assert, const, share, timer
