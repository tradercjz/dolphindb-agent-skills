<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/modify_table_structure.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 更新表结构

DolphinDB 支持使用 SQL 语句和内置函数对表结构进行修改，允许用户增加列、删除列、修改列名、修改列顺序以及修改数据类型。

本节示例脚本中，内存表 t 和 分布式表 pt 及其数据由以下脚本生成：

```
t = table(2023.10.01 + take(0..9,100) as date, take(["A01","B01","C01","D01"],100) as sym, 1..100 as val)
db = database("dfs://olapdemo",VALUE,2023.10.01..2023.10.10)
pt = db.createPartitionedTable(t,`pt,`date)
pt.append!(t)
```

## 增加列

addColumn 函数支持为内存表或分布式表增加列。

例如，为表 t 和 pt 增加一列 "new"

```
addColumn(t,`new,DOUBLE)
addColumn(pt,`new,DOUBLE)
```

`UPDATE` 语句和 update!
函数支持为内存表增加列。

例如，为表 t 增加列 "new\_1"

```
// SQL UPDATE
UPDATE t SET new_1 = 1..100

// 或 update! 函数
update!(t,"new_1",1..100)
```

为内存表增加列也可以通过赋值语句实现。

例如，为表 t 增加列 “new\_2”

```
t[`new_2] = string(NULL)
```

注：

* 为流表增加列，只能使用 `addColumn` 函数。
* 增加列后，在插入新结构数据之前，仍然可以插入原来结构的数据。一旦插入了新结构的数据，就不能插入原来结构的数据。

## 删除列

dropColumns! 函数可以删除内存表或分布式表（仅支持 OLAP
存储引擎）的列 val：

```
dropColumns!(t,`val)
dropColumns!(pt,`val)
```

注：

不支持删除分布式表的分区列。

## 修改列顺序

reorderColumns
函数可以修改非分区、非共享内存表的列顺序。

```
reorderColumns!(t,`date`val`sym)
```

如果指定新的列顺序时，只指定了部分列，则这些列将按照指定顺序作为表的前几列，其余列按照原有先后顺序依次排列在后。

例如，指定列 “date” 和 “val” 作为前两列。

```
reorderColumns!(t,`date`val)
```

## 修改列名

rename! 函数可以为内存表和分布式表（仅支持 OLAP
存储引擎）修改列名。

例如，将 “sym” 改名为 “sym\_new”

```
rename!(t,`sym,`sym_new)
```

## 修改列类型

通过 replaceColumn!
函数可以为非共享内存表和分布式表（仅支持 OLAP 存储引擎）修改列的数据类型。

对于

```
replaceColumn!(t,"val",double(t.val))
```

如果分布式表的数据量很大，整列替换会对内存带来很大压力，甚至超出内存容量，此时可以采用以下方法：

```
newType = array(DOUBLE,0,1)
replaceColumn!(pt,"val",newType)
```

## 修改表名

renameTable 函数可以修改分布式表的表名。修改后请执行
loadTable 重新加载表的元数据对象：

```
renameTable(db,"pt","pt_new")
pt = loadTable(db,"pt_new")
```

注：

执行函数 rename!、dropColumns! 和
replaceColumn! 前，可以先执行 flushOLAPCache
函数手动刷盘，减少等待时间避免超时。

**相关信息**

* [addColumn](../funcs/a/addColumn.html "addColumn")
* [dropColumns!](../funcs/d/dropColumns_.html "dropColumns!")
* [flushOLAPCache](../funcs/f/flushOLAPCache.html "flushOLAPCache")
* [loadTable](../funcs/l/loadTable.html "loadTable")
* [rename!](../funcs/r/rename_.html "rename!")
* [renameTable](../funcs/r/renameTable.html "renameTable")
* [replaceColumn!](../funcs/r/replaceColumn_.html "replaceColumn!")
* [reorderColumns](../funcs/r/reorderColumns_.html "reorderColumns")
* [update!](../funcs/u/update_.html "update!")
