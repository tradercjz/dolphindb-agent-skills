# objectType

## 语法

`objectType(obj)`

## 详情

判断给定对象的类型。

* 当 *obj* 不是 CODE 类型，返回 “CONSTOBJ”。
* 当 *obj* 是 CODE 类型，返回 *obj* 所表征对象的类型，可能的结果包括：

| 结果 | 含义 |
| --- | --- |
| CONSTOBJ | 常量 |
| VAR | 变量 |
| GLOBAL | 全局对象 |
| ATTR | 对象的属性 |
| DIM | 维度 |
| TUPLE | 元组 |
| FUNCTION | 函数 |
| EXPRESSION | 表达式 |
| COLUMN | 列 |
| COLUMNDEF | 列定义 |
| SQLQUERY | SQL 查询 |
| TABLEJOINER | 表连接 |
| VIRTUALCONST | 虚拟常量 |
| MAPPEDCOL | 经过映射的列 |
| GLOBALTALBE | 全局表 |
| GROUPTASK | 一组任务 |
| DIMTABLE | 维度表 |
| METHODCALL | 对象的方法调用 |
| SQLUPDATE | SQL 更新语句 |
| SQLDELETE | SQL 删除语句 |
| COLSELECTOR | 列选取器 |
| CASEWHEN | SQL 的条件判断语句 |
| SQLEXISTS | SQL 的存在判断语句 |
| SQLWITHQUERY | SQL 的公用表表达式 |
| OPTOBJ | 经过优化的对象 |
| MULTITABLEJOINER | 多表连接 |
| UNKNOWN | 未知（如不属于上述情况） |

## 参数

**obj** 任意数据类型的对象。

## 返回值

字符串标量。

## 例子

```
objectType(<select * from pt>)
// output: SQLQUERY

objectType(sqlColAlias(<col1>,`col))
// output: COLUMNDEF

objectType(<x+y>)
// output: EXPRESSION
```
