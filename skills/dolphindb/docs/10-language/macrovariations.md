<!-- Auto-mirrored from upstream `documentation-main/progr/macrovariations.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# SQL 元编程

SQL 元编程是指在代码执行时动态生成 SQL 语句的方法。这种方法方便用户通过程序脚本来生成 SQL 代码，达到动态生成和执行的目的。DolphinDB 提供了两种编写 SQL
元编程的方式：基于函数的元编程和基于宏变量的元编程。

## 基于函数的 SQL 元编程

基于函数的 SQL 元编程是指通过内置元编程函数的组合调用生成 SQL 元代码的方法。DolphinDB 提供了一系列基本函数，可以生成 SQL 元代码：

* `sqlCol`：支持生成单字段或多字段应用同一函数的表达式，支持指定别名。生成的表达式形如：

  ```
  sqlCol("col")
  // output: <col>

  sqlCol(["col0", "col1", ..., "colN"])
  // output: [<col0>, <col1>, ..., <colN>]

  sqlCol("col", func = sum, alias = "newCol")
  // output: <sum(col) as newCol>

  sqlCol(["col0", "col1"], func=sum, alias=["newCol0", "newCol1"])
  // output： [<sum(col0) as newCol0>, <sum(col1) as newCol1>]
  ```
* `sqlColAlias`：为复杂的列字段计算元代码指定别名。生成的表达式形如：

  ```
  sqlColAlias(sqlCol("col"), "newCol")
  // output: <col as newCol>

  sqlColAlias(makeCall(sum, sqlCol("col")), "newCol")
  // output: <sum(col) as newCol>

  sqlColAlias(makeCall(corr, sqlCol("col0"), sqlCol("col1")), "newCol")
  // output: <corr(col0, col1) as newCol>
  ```

  通常搭配下述函数使用：

  + `makeCall`, `makeUnifiedCall`：用于生成
    <func(cols.., args...)> 的元代码表达式。
  + `expr`, `unifiedExpr`,
    `binaryExpr`：生成多元算术表达式，例如 <a+b+c>,
    <a1\*b1+a2\*b2+... +an\*bn>
* `parseExpr`：从字符串生成元代码，将 API 上传或脚本读取的字符串，生成可执行的脚本。例如
  `parseExpr("select * from t")` 生成 `<select * from
  t>` 的元代码；parseExpr("vol>1000") 生成 `sql` 函数 where
  参数部分的元代码等。

使用 `sql` 函数，可以把这些元代码组装起来，得到一个完整的
select 元代码语句。例如，对以下 SQL 脚本：

```
// 创建表
securityID = take(`GE,3) join take(`MSFT,3) join take(`F,3)
time=09:00:00 09:30:00 10:00:00 10:28:00 11:00:00 12:00:00 13:00:00 14:00:00 14:29:00
price=31.82 31.69 31.92 63.12 62.58 63.12 12.46 12.59 13.24
volume=2300 3500 3700 1800 3800 6400 4200 5600 8900
t = table(securityID, time, price, volume);

//查询语句
select cumsum(price) as cumPrice from t
where time between 09:00:00 and 11:00:00
context by securityID csort time limit -1
```

可以使用上述函数生成各部分的元代码，并通过 `sql` 动态生成 SQL
语句：

```
selectCode = sqlColAlias(makeUnifiedCall(cumsum, sqlCol("price")), "cumPrice")
fromCode = "t"
whereCondition = parseExpr("time between 09:00:00 and 15:00:00")
contextByCol = sqlCol("securityID")
csortCol = sqlCol("time")
limitCount = -1
sql(select = selectCode, from = fromCode,
where = whereCondition, groupby = contextByCol,
groupFlag = 0, csort = csortCol, limit = limitCount)
```

得到的结果为：

```
< select cumsum(price) as cumPrice from objByName("t")
where time between pair(09:00:00, 15:00:00)
context by securityID csort time asc limit -1 >
```

若需要执行生成的元代码，请搭配使用 `eval` 函数。

通过以上代码，可以总结出出 `sql` 函数生成元代码的规则：

* 查询字段须以 `sqlCol` 或者 `sqlColAlias` 声明。
* 对表字段计算的元代码：

  + 单字段参与计算：`sqlCol` 函数指定 *func* 参数。
  + 多字段参与计算：`sqlColAlias` 函数 搭配 `makeCall`
    或者 `makeUnifiedCall` 函数。
* 表对象可以是一个表变量名字符串、表变量如 t 或 `loadTable` 返回的句柄。

除能够生成 SQL 查询语句的元代码外，DolphinDB 还提供函数来生成 SQL UPDATE 语句和 SQL DELETE
语句的元代码。若需要执行生成的元代码，请搭配使用 `eval` 函数。

* `sqlUpdate` 函数动态生成 SQL update 语句的元代码。例如：

  ```
  sqlUpdate(t, <price*2 as updatedPrice>)
  ```
* `sqlDelete` 函数动态生成 SQL delete 语句的元代码。例如：

  ```
  sqlDelete(t, <time = 10:00:00>)
  ```

## 基于宏变量的元编程

DolphinDB 自 2.00.12 版本起，支持了基于宏变量的 SQL 元编程。

宏变量在元编程中提供了一种更加简单和直观的方法。在 SQL 元代码中，根据变量定义的列是单列还是多列，动态获取宏变量的方式也会有所不同。

* 单列宏变量：指为变量赋值了表中一个列的字段名称，使用 “\_$“ 符号来动态获取该变量的值。例如，变量定义为
  `name="sym"`，元代码可写为 `<SELECT _$name FROM
  t>`，在执行时会替换为 `SELECT sym FROM t`。
* 多列宏变量：指为变量赋值了表中多个字段的名称，使用 “\_$$” 符号来动态获取该变量中的多个值。例如，变量定义为 `names=["sym",
  "time"]`，元代码可写为 `<SELECT _$$name FROM t>`，在执行时会替换为
  `SELECT sym, time FROM t`。

使用宏变量相较于函数生成的元代码，可以让脚本更加简洁和易于理解。然而，宏变量的使用也存在一些限制：

* 变量名类型必须是 STRING，且变量值需要符合 DolphinDB 数据表字段的命名规范，即不能以数字和符号开头。
* 宏变量仅能用于 SELECT，WHERE，GROUP BY，PIVOT BY，CONTEXT BY，CSORT，ORDER BY 等子句。不能用于 FROM
  子查询、UPDATE、DELETE 和 OVER 语句。而且在 CSORT 和 ORDER BY 子句中只能使用 “\_$”，不能使用 “\_$$”。以 FROM
  子查询为例，不支持类似这种写法 `<select * from select _$$names1 from
  t>`。
* 宏变量只能在列定义（包括获取列名和定义别名）、函数和表达式中使用。在函数或表达式中应用多列宏变量时，相当于提供了一个元组，其中每个元素对应一列。

若使用基于函数的元编程方法，一个复杂的 SQL
语句可能需要多个函数搭配使用。若使用基于宏变量的元编程方法，则编写方法更直观。例如，上一小节中基于函数的元编程构造多个部分的元代码，并使用
`sql` 拼装的例子，可使用宏变量改写为：

```
col = "price"
contextByCol = "securityID"
csortCol = "time"
a = 09:00:00
b = 15:00:00
<select cumsum(_$col) from t where _$csortCol between a and b
  context by _$contextByCol csort _$csortCol limit -1>
```

下例对一个表的多列分别求和，返回多列结果，基于函数的写法是：

```
x1 = 1 3 5 7 11 16 23
x2 = 2 8 11 34 56 54 100
x3 = 8 12 81 223 501 699 521
y = 0.1 4.2 5.6 8.8 22.1 35.6 77.2;
t = table(y, x1, x2, x3)
name = [`y,`x1]
alias = [`y1, `x11]
sql(select = sqlCol(name, sum, alias), from = t).eval()
```

基于宏变量的实现为：

```
name = [`y,`x1]
alias = [`y1, `x11]
<select sum:V(_$$name) as _$$alias from t>.eval()
```

关于 SQL 编程的更多应用案例，参考教程：基于 SQL 的元编程
