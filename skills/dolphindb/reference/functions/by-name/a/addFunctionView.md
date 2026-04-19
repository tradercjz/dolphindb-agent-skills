# addFunctionView

## 语法

`addFunctionView(udf|moduleName)`

## 详情

函数视图是封装了访问数据库以及相关计算语句的一种特殊的自定义函数。函数视图提供了一种灵活的方式来控制用户访问数据库和表。用户即使不具备读写数据库原始数据的权限，也可通过执行函数视图，间接访问数据库，得到所需计算结果。例如，用户不能查看个别患者的名称和年龄等原始数据，但是可以获取患者的总数与平均年龄。

与其他自定义函数会话隔离不同，函数视图可以实现会话之间的共享。函数视图的定义持久化存储在控制节点，因此如果 DolphinDB
集群重启，之前定义的函数视图仍然可以使用。

使用 grant, deny 或 revoke
命令对用户的 VIEW\_EXEC 权限进行操作时，用户自定义函数可以作为这些命令的 objs 参数。

`addFunctionView` 只能由管理员或拥有 VIEW\_OWNER
权限的普通用户执行。

## 参数

**udf** 是用户自定义函数。

**moduleName** 是一个字符串标量，代表模块名称。

注：

* 不支持匿名函数。
* 自定义函数只能接收标量、数据对或常规数组作为默认参数。
* *moduleName* 相应模块必须放置于节点的 modules 目录下
* 若 modules 目录下同时存在名为 *moduleName* 的 dos 和 dom 文件，则优先加载 dos 文件。
* 如果在当前节点使用use <moduleName> 的方式加载模块使用，即使同名模块和函数已通过
  addFunctionView 封装，也会优先使用最新加载的模块。

## 例子

下例中，自定义函数 `getSpread` 计算
`dfs://TAQ/quotes` 表中指定股票的平均买卖报价差。用户 user1 不具有读取
`dfs://TAQ/quotes` 表的权限。将函数 `getSpread` 定义为函数视图，
并赋予用户 user1 执行该视图的权限。虽然 user1 不具备读取 `dfs://TAQ/quotes` 表的权限，但可通过执行
`getSpread` 函数，对 `dfs://TAQ/quotes`
表的数据进行计算，来获得指定股票的买卖报价差。

由于 `dfs://TAQ/quotes`
是分布式数据库，以下代码需要由系统管理员在控制节点上执行。用户 user1 可在任意数据节点/计算节点运行 `getSpread`
函数。

```
def getSpread(s, d){
 return select avg((ofr-bid)/(ofr+bid)*2) as spread from loadTable("dfs://TAQ","quotes") where symbol=s, date=d
}

addFunctionView(getSpread)

// grant 操作需在控制节点执行
grant("user1", VIEW_EXEC, "getSpread")
```

确保在节点的 modules 下已存在 test.dos，模块 test 中定义了函数 f1 和
f2。

```
 addFunctionView("test")

//为用户 user1 授权执行模块 test 下的函数 f1
grant("user1", VIEW_EXEC, "test::f1")
//为用户 user1 授权执行模块 test 下的所有函数
grant(`user1, VIEW_EXEC, "test::*")

//用户可使用全限定名调用相应函数
test::f1()
```

相关函数： dropFunctionView、getFunctionViews
