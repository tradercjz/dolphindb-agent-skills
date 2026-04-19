<!-- Auto-mirrored from upstream `documentation-main/db_distr_comp/db_oper/FunctionView.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 函数视图

函数视图提供了一种灵活的方式来控制用户访问数据库和表。函数视图是封装了访问数据库以及相关计算语句的自定义函数。用户即使不具备读写数据库原始数据的权限，也可通过执行函数视图，间接访问数据库，得到所需计算结果。

## 封装自定义函数

DolphinDB 支持将用户自定义函数封装为函数视图。

### 定义

首先定义用户自定义函数。

```
def myFunc(){
    print "myFunc"
}
```

再通过 addFunctionView
函数将自定义函数封装为函数视图。

```
addFunctionView(udf=myFunc)
getFunctionViews()
```

| name | body |
| --- | --- |
| myFunc | def myFunc(){ print("myFunc") } |

### 删除

通过 dropFunctionView
函数可以删除已有的函数视图。

```
dropFunctionView(name="myFunc")
```

## 封装模块

DolphinDB 支持将模块添加为函数视图，用户可以按照命名空间管理函数视图。

### 定义

在 *[home]/modules/dir1/myModule* 文件中定义函数，并在文件第一行声明为模块，文件内容如下：

```
module dir1::myModule

def f1(){
    print "dir1::myModule::f1"
}
def f2(){
    print "dir1::myModule::f2"
}
```

使用 use 语句引用模块后，可通过 `addFunctionView` 函数将该模块中所有函数添加为函数视图。

```
login(userId=`admin, password=`123456)
use dir1::myModule
addFunctionView(moduleName="dir1::myModule")
getFunctionViews()
```

| name | body |
| --- | --- |
| dir1::myModule::f1 | def f1(){ print("dir1::myModule::f1") } |
| dir1::myModule::f2 | def f2(){ print("dir1::myModule::f2")} |

### 删除

通过 `dropFunctionView` 函数删除函数视图时，即可指定删除某一个视图，也可根据命名空间批量删除。

```
// 删除函数视图 dir1::myModule::f1
dropFunctionView(name="dir1::myModule::f1")

// 删除名称空间 dir1::myModule 下所有函数视图
dropFunctionView(name="dir1::myModule",isNamespace=true)
```

## 获取函数视图

管理员用户执行 getFunctionViews
函数可以获取当前系统的所有用户创建的函数视图，拥有 VIEW\_OWNER 权限的用户执行该函数只返回该用户创建的函数视图。

注：

如果 DolphinDB 集群重启，之前定义的函数视图仍然可以使用。但是 DolphinDB 不允许直接修改函数视图中的语句，如果要修改函数视图，需要先使用
`dropFunctionView` 函数删除函数视图。

## 示例

用户 user1 不具有读取分布式表 dfs://db1/pt 的权限。通过将函数`getAvg` 定义为函数视图，并赋予用户 user1
执行该视图的权限，user1 可以在没有读取分布式表 dfs://db1/pt1 的权限的情况下，得到该表中 value 列每天的平均值。

```
// 创建分布式表 dfs://db1/pt 并模拟数据
login(userId=`admin, password=`123456)
db = database(directory="dfs://db1", partitionType=VALUE,
  partitionScheme=2024.01.01..2024.01.10)
t = table(stretch(2024.01.01..2024.01.10,100) as date, rand(1000,100) as val)
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt",
  partitionColumns="date")
pt.tableInsert(t)

// 定义函数 getAvg ，并将其设置为函数视图
def getAvg(){
  return select avg(val) from loadTable(database="dfs://db1", tableName="pt") group by date
}
login(userId=`admin, password=`123456)
addFunctionView(udf=getAvg)

// 创建用户 user1，并赋予其执行函数视图 getAvg 的权限
createUser(userId=`user1, password=`123456)
grant(userId=`user1, accessType=VIEW_EXEC, objs="getAvg")

// 用户 user1 由于没有权限无法直接读取表中数据
login(userId=`user1, password=`123456)
select avg(val) from loadTable(database="dfs://db1", tableName="pt") group by date
// <NoPrivilege>Not granted to read table dfs://db1/pt

// 用户 user1 调用函数视图可以获取每天的平均值
getAvg()
```

| date | avg\_val |
| --- | --- |
| 2024.01.01 | 438 |
| 2024.01.02 | 447.6 |
| 2024.01.03 | 499.6 |
| 2024.01.04 | 355.2 |
| 2024.01.05 | 551.9 |
| 2024.01.06 | 330.2 |
| 2024.01.07 | 366.5 |
| 2024.01.08 | 547.9 |
| 2024.01.09 | 473 |
| 2024.01.10 | 369.2 |

注：由于 value 的值是随机生成的，多次执行的结果中 avg\_val 可能不一致，这符合预期。

**相关信息**

* [addFunctionView](../../funcs/a/addFunctionView.html "addFunctionView")
* [dropFunctionView](../../funcs/d/dropFunctionView.html "dropFunctionView")
* [getFunctionViews](../../funcs/g/getFunctionViews.html "getFunctionViews")
