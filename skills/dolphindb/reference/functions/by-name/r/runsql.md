# runSQL

首发版本：3.00.3

## 语法

`runSQL(X, [sqlStd='ddb'], [variables])`

## 详情

`runSQL` 函数根据指定的语法环境解析并执行脚本。同时，支持通过用户输入的变量作为参数动态传递给 SQL 语句，从而避免手动拼接
SQL 字符串，降低注入风险，确保代码安全性和易维护性。

**注意**：`runSQL` 在自定义函数内调用时，无法读取到完整的上下文，不建议在自定义函数中使用
`runSQL` 函数。

目前仅支持 Oracle 和 MySQL 的部分功能和函数，见下表：

| SQL 方言 | 支持功能 | 支持函数（无分大小写） |
| --- | --- | --- |
| Oracle | * 注释符：--、/\*\*/ * 字符串拼接符：|| | asciistr, concat, decode, instr, length, listagg, nvl, nvl2, rank, regexp\_like, replace, to\_char, to\_date, to\_number, trunc, wm\_concat 注： to\_char 只接收数值类型和 DATE, DATEHOUR, DATETIME 类型的参数。有关 Oracle SQL 函数的语法参考，请访问：SQL Language Reference |
| MySQL |  | sysdate 注： 有关 MySQL 函数的语法参考，请访问：MySQL :: MySQL 8.0 Reference Manual :: 12 Functions and Operators |

**注：**在 Oracle 或 MySQL 模式下，同样支持解析使用 DolphinDB 语言编写的脚本。

## 参数

**X** 字符串，表示需要执行的脚本。*X* 不支持 SQL DDL 操作；此外，当*sqlStd* 指定为 'oracle' 和
'mysql' 时，*X* 也不支持DML 操作。

**sqlStd** 可选参数。字符串，用于指定脚本的解析方言。可选值包括：'ddb'（默认值），'oracle'，'mysql'。

**variables**
可选参数。用于动态传递参数的字典。字典的键为字符串，表示变量名称（可以包含字母，数字和下划线，但必须以字母开头）；值为对应的对象。

## 返回值

*X* 查询的结果。

## 例子

例 1：使用 DolphinDB 语法进行解析，并指定 *variables* 用于动态传递参数。

假设有以下订单表 t。

```
n=10
customerId="DB00"+string(1..5)
orderDate=2025.01.01..2025.01.10
t=table(take(orderDate, n) as orderDate, 1..10 as orderId, take(customerId,n) as customerId, rand(1000,n) as volume)
t
```

| **orderDate** | **orderId** | **customerId** | **volume** |
| --- | --- | --- | --- |
| 2025.01.01 | 1 | DB001 | 435 |
| 2025.01.02 | 2 | DB002 | 134 |
| 2025.01.03 | 3 | DB003 | 483 |
| 2025.01.04 | 4 | DB004 | 867 |
| 2025.01.05 | 5 | DB005 | 708 |
| 2025.01.06 | 6 | DB001 | 291 |
| 2025.01.07 | 7 | DB002 | 663 |
| 2025.01.08 | 8 | DB003 | 254 |
| 2025.01.09 | 9 | DB004 | 386 |
| 2025.01.10 | 10 | DB005 | 653 |

我们需要查询某个客户 （DB001）最近 10 天内的订单（假设查询当天为 2025.01.14）。

```
sql_script ="SELECT orderId,customerId, orderDate, volume FROM t WHERE customerId==customer AND orderDate>=(date(now())- days)"
variables={"customer":`DB001,"days": 10}
re=runSQL(sql_script, , variables)
print(re)
```

返回：

| **orderId** | **customerId** | **orderDate** | **volume** |
| --- | --- | --- | --- |
| 6 | DB001 | 2025.01.06 | 291 |

例 2：使用 Oracle 语法进行解析

```
runSQL("concat(CONCAT(`14`mysql, `22`oracle),`11`33)", 'oracle')
// output: ["142211","mysqloracle33"]

runSQL("string(1 2 3) || string(4 5 6)", 'oracle')
// output: ["14","25","36"]

runSQL("TO_DATE('2023-05-18', 'YYYY-MM-DD')", 'oracle')
// output: 2023.05.18
```

例 3：使用 MySQL 语法进行解析

```
runSQL("SYSDATE() + 1", 'mysql')
// output: 2025.01.15
```
