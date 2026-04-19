<!-- Auto-mirrored from upstream `documentation-main/progr/objs/const.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 常量

只有两种数据形式可以直接用常量来表示：标量和向量。其他数据类型，数据对、矩阵、集合、字典和表，必须通过函数调用的形式返回。函数定义和句柄属于常量。

```
3;
// 一个整数常量

3.9;
// 一个双精度浮点常量

1 2 3;
// 一个整数向量常量

(1, 2, 3)
// 一个元组常量

`IBM`YAHOO`MS`GOOG
// 一个字符串向量常量

true;
// 一个布尔值常量

NULL;
// 特殊的常量NULL
```

有两个内置常量：pi和e。内置常量不能被重定义。

```
pi*2;
// output
6.283185

log e;
// output
1

e=1;
// output
Syntax Error: [line #1] Please use '==' rather than '=' as equal operator in non-sql expression.
```

## 整数常量

整数常量是指没有小数或指数部分的常量。

1. 数据形式： SCALAR, PAIR, VECTOR, MATRIX, SET, DICT, TABLE.

   ```
   x=set(1 2 3)
   if(form(x) == SET){y=10};

   y;
   // output
   10

   form x;
   // output
   4
   ```
2. 数据类型： VOID, BOOL, CHAR, SHORT, INT, LONG, DATE, MONTH,
   TIME, MINUTE, SECOND, DATETIME, TIMESTAMP, NANOTIME, NANOTIMESTAMP, FLOAT,
   DOUBLE, SYMBOL, STRING, UUID, FUNCTIONDEF, HANDLE, CODE, DATASOURCE,
   RESOURCE, ANY, ANY DICTIONARY, DATEHOUR, IPADDR, INT128, BLOB, COMPLEX,
   POINT, DURATION.

   ```
   x=(`ABC, 123);
   type x;
   // output
   24

   (type x) == ANY;
   // output
   1
   ```
3. 图表类型： LINE, PIE, COLUMN, BAR, AREA, HISTOGRAM,
   SCATTER.

   ```
   plot(1..5 as value, `IBM`MSFT`GOOG`XOM`C, `rank, BAR)
   ```
4. 在函数 seek
   中，表示内部游标的位置：HEAD, CURRENT, TAIL。

   ```
   // 写一个函数来显示文件的长度
   def fileLength(f): file(f).seek(0, TAIL)
   fileLength("test.txt");
   // output
   14
   ```
5. 在函数 undef
   中定义的对象类型： VAR, SHARED, DEF.

   ```
   x=1 2 3;
   undef(`x, VAR);
   ```

可以用以下语句声明常量： const variableName = value.

常量不可变。在声明一个常量后，不能将另一个对象绑定到常量，也不能修改绑定对象的值。

```
const a = 1 2 3;
a=4 5 6;
// output
Syntax Error: [line #1] Constant variable [a] can't be modified.

const a = 10;
a+=1;
// output
Syntax Error: [line #1] Constant variable [a] can't be modified.

const x = 1..10;
x[5]=0;
// output
Syntax Error: [line #1] Constant variable [x] can't be modified.
```
