# revoke

## 语法

`revoke(userId|groupId, accessType, [objs])`

## 详情

`revoke` 函数执行以下操作：

（1）撤销某个用户或某个组的之前被赋予或禁止的权限。

（2）撤销 `grant` 给某个用户的内存约束，包含：查询返回结果的内存上限（指定
*accessType* = QUERY\_RESULT\_MEM\_LIMIT）和发送的批量子查询占用的内存上限（指定 *accessType*
= TASK\_GROUP\_MEM\_LIMIT）。撤销后，将恢复为系统的默认值。

管理员可以通过该命令撤销用户所有权限（*accessType*），但普通用户在拥有相关的 OWNER 权限后，只能通过该命令撤销以下权限：TABLE\_READ,
TABLE\_WRITE, TABLE\_INSERT, TABLE\_UPDATE, TABLE\_DELETE, DB\_READ, DB\_WRITE, DB\_INSERT,
DB\_UPDATE, DB\_DELETE, DBOBJ\_DELETE, DBOBJ\_CREATE 和 VIEW\_EXEC。

可被撤销的权限类型，参见 grant。Orca 流图和流表相关权限：详见
Orca 实时计算平台 6.3
节。

注：

该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 参数

**userId** | **groupId** 是表示用户名或组名的字符串。

**accessType** 权限类型/内存限制。

**objs** 标量或向量，表示权限类型的应用对象/约束规则。也可以指定为 \*，表示全局。当 *accessType* 指定为 COMPUTE\_GROUP\_EXEC 时，*objs*
必须为对应的计算组名。

注：

* 管理共享内存表、流数据表或流计算引擎的权限时，*objs* 必须为 "tableName@nodeAlias"
  或"nodeAlias:tableName"。
* 管理 IMOLTP 引擎库表权限时，*objs* 必须为
  "oltp://database/table@nodeAlias" 或 "oltp://database@nodeAlias"。

*accessType* 和 *objs* 的取值请参照 用户权限管理
权限类型表。

## 例子

撤销组 "production" 的所有成员读取所有数据库表的权限：

```
revoke(`production, TABLE_READ, "*")
```

撤销组 "research" 的所有成员读写表 dfs://db1/t1 的权限：

```
revoke(`research, TABLE_WRITE, "dfs://db1/t1")
```

撤销组 "research" 的所有成员在数据库 dfs://db1 和 dfs://db2 创建表的权限：

```
revoke("research", DBOBJ_CREATE, ["dfs://db1","dfs://db2"])
```

撤销用户 "AlexSmith" 创建和删除数据库的权限：

```
revoke("AlexSmith", DB_MANAGE)
```

撤销用户 "AlexSmith" 执行脚本的权限：

```
revoke("AlexSmith", SCRIPT_EXEC)
```

撤销用户 "AlexSmith" 测试脚本的权限：

```
revoke("AlexSmith", TEST_EXEC)
```
