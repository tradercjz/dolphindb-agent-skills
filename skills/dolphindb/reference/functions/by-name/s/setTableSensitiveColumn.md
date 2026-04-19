# setTableSensitiveColumn

首发版本：3.00.3

## 语法

`setTableSensitiveColumn(table, colName, option,
[func])`

## 详情

将表 *table* 的 *colName* 列设置或取消设置为敏感列。

设置为敏感列后，仅该表的创建者、管理员和具有 DB\_SENSITIVE\_VIEW 或 TABLE\_SENSITIVE\_VIEW
权限的用户可以访问该列的明文数据，其他用户仅可访问经 *func* 脱敏处理后的数据。

## 参数

**table** 一个 DFS 表对象。

**colName** STRING 类型标量，表示列名。

**option** BOOL 类型标量，true 表示将 *colName* 设置为敏感列，false 表示取消设置该列为敏感列。

**func** 可选参数，是一个一元函数，表示脱敏算法。仅当 *option =* true
时支持设置此参数。默认算法为将目标列数据处理为空值。当该算法需要作用于不同类型时，UDF 内部应定义对不同类型的处理逻辑。

## 例子

```
// 建库建表
login(`admin,`123456)
db = database(directory="dfs://sensitive", partitionType=VALUE, partitionScheme=1..5)
t = table(1..5 as tag, ["John","Emily","Michael","James","Tommy"] as userId, format(rand(100000,5),"000000") as password)
pt = createPartitionedTable(dbHandle=db, table=t, tableName="pt", partitionColumns="tag")
pt.tableInsert(t)

// 设置敏感列
def encryptId(str){
    return str[0]+"******"
}
setTableSensitiveColumn(table=loadTable("dfs://sensitive","pt"), colName="userId", option=true, func=encryptId)

def encryptPw(str) {
    return regexReplace(str, "[0-9]+", "#")
}
setTableSensitiveColumn(table=loadTable("dfs://sensitive","pt"), colName="password", option=true, func=encryptPw)

// 创建用户 user1
createUser(`user1,`123456)
grant(userId="user1", accessType=TABLE_READ, objs="dfs://sensitive/pt")

// user1 读取脱敏数据
login(`user1,`123456)
select * from loadTable("dfs://sensitive","pt")

// 为 user1 赋权
login(`admin,`123456)
grant(userId=user1, accessType=TABLE_SENSITIVE_VIEW, objs="dfs://sensitive/pt")

// user1 读取敏感数据
login(`user1,`123456)
select * from loadTable("dfs://sensitive","pt")
```
