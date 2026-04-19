# getUserAccess

## 语法

`getUserAccess([userIds], [finalAccess=false])`

## 详情

指定 *userId* 时：

* 若 *finalAccess* = false，则返回指定用户所单独被赋予的权限，不包括用户所属组的权限。
* 若 *finalAccess* = true，则返回指定用户及其所属组的权限组合后的最终生效权限。

当没有指定 *userId* 时，返回当前登录用户的权限。

注：

该函数只能由管理员在控制节点、数据节点和计算节点运行。

## 参数

**userId** 是表示一个或多个用户的字符串标量或向量。

**finalAccess** 为布尔值，表示是否获取用户及其所属组权限叠加的结果。默认值为 false。

## 返回值

返回一个表，以下分别介绍返回表的各参数的详情：

| 参数 | 详情 |
| --- | --- |
| userId | 用户名 |
| groups | 组名 |
| isAdmin | 是否是管理员。 |
| MAX\_JOB\_PRIORITY | 该用户对应的作业最高优先级，范围是0-8，可以通过 `setMaxJobPriority` 指定。 |
| MAX\_PARALLELISM | 该用户提交的作业最多可以有多少个子任务同时并行执行，可以通过 `setMaxJobParallelism` 指定。 |
| QUERY\_RESULT\_MEM\_LIMIT | 该用户单次查询结果的占用内存上限，浮点类型，单位为 GB。可以通过 `grant` 指定，`revoke` 撤销。 |
| TASK\_GROUP\_MEM\_LIMIT | 该用户发送的批量子查询占用的内存上限，浮点类型，单位为 GB。可以通过 `grant` 指定，`revoke` 撤销。 |
| MAX\_PARTITION\_NUM\_PER\_QUERY | 该用户单次查询的最大分区数。整型标量，-1 表示没有设置该权限。可以通过 `grant` 指定，`revoke` 撤销。 |

以下字段对应权限，其值为 “allow" / "none" / "deny" ：

| 权限 |
| --- |
| ACCESS\_READ |
| ACCESS\_INSERT |
| ACCESS\_UPDATE |
| ACCESS\_DELETE |
| VIEW\_EXEC |
| SCRIPT\_EXEC |
| TEST\_EXEC |
| DBOBJ\_CREATE |
| DBOBJ\_DELETE |
| DB\_MANAGE |
| DB\_OWNER |
| VIEW\_OWNER |
| COMPUTE\_GROUP\_EXEC |
| TABLE\_SENSITIVE\_VIEW |
| DB\_SENSITIVE\_VIEW |
| CREATE\_SHARED\_VARS |
| MCP\_MANAGE |
| MCP\_DEVELOP |
| MCP\_EXEC |
| ORCA\_MANAGE |
| ORCA\_GRAPH\_CONTROL |
| ORCA\_GRAPH\_CREATE |
| ORCA\_GRAPH\_DROP |
| ORCA\_TABLE\_READ |
| ORCA\_TABLE\_WRITE |
| ORCA\_TABLE\_CREATE |
| ORCA\_TABLE\_DROP |
| ORCA\_ENGINE\_MANAGE |

**注意**：

* 自 3.00.5 版本起，支持获取 Orca 流图、流表权限。
* 自 3.00.2 版本起，支持获取访问计算节点组的权限。
* 自 3.00.0.0 版本起，支持获取访问 catalog 的相关权限。
* 自 2.00.9 版本开始，新增了表和数据库的插入更新和删除权限（即对写权限进行拓展），因此旧版本的 TABLE\_WRITE 字段由
  TABLE\_INSERT，TABLE\_UPDATE，TALBE\_DELETE 字段替代。
* 因为具有 DB\_READ / DB\_INSERT / DB\_UPDATE / DB\_DELETE
  权限的用户，可以在该数据库范围内对其下的所有表执行相应的操作，所以在 getUserAccess 函数中，用户对数据库和表的权限会被统一为
  ACCESS\_READ / ACCESS\_INSERT / ACCESS\_UPDATE /
  ACCESS\_DELETE。可以通过下表来区分上述权限的具体应用对象。

以下几个字段表示权限应用的具体对象：

| 对象 |
| --- |
| TABLE\_READ\_allowed |
| TABLE\_READ\_denied |
| TABLE\_INSERT\_allowed |
| TABLE\_INSERT\_denied |
| TABLE\_UPDATE\_allowed |
| TABLE\_UPDATE\_denied |
| TABLE\_DELETE\_allowed |
| TABLE\_DELETE\_denied |
| DB\_READ\_allowed |
| DB\_READ\_denied |
| DB\_INSERT\_allowed |
| DB\_INSERT\_denied |
| DB\_UPDATE\_allowed |
| DB\_UPDATE\_denied |
| DB\_DELETE\_allowed |
| DB\_DELETE\_denied |
| VIEW\_EXEC\_allowed |
| VIEW\_EXEC\_denied |
| DBOBJ\_CREATE\_allowed |
| DBOBJ\_CREATE\_denied |
| DBOBJ\_DELETE\_allowed |
| DBOBJ\_DELETE\_denied |
| DB\_OWNER\_allowed |
| DB\_MANAGE\_allowed |
| DB\_MANAGE\_denied |
| CATALOG\_READ\_allowed |
| CATALOG\_READ\_denied |
| CATALOG\_INSERT\_allowed |
| CATALOG\_INSERT\_denied |
| CATALOG\_UPDATE\_allowed |
| CATALOG\_UPDATE\_denied |
| CATALOG\_DELETE\_allowed |
| CATALOG\_DELETE\_denied |
| COMPUTE\_GROUP\_EXEC\_allowed |
| COMPUTE\_GROUP\_EXEC\_denied |
| TABLE\_SENSITIVE\_VIEW\_allowed |
| TABLE\_SENSITIVE\_VIEW\_denied |
| DB\_SENSITIVE\_VIEW\_allowed |
| DB\_SENSITIVE\_VIEW\_denied |
| MCP\_EXEC\_allowed |
| MCP\_EXEC\_denied |
| ORCA\_MANAGE\_allowed |
| ORCA\_MANAGE\_denied |
| ORCA\_CATALOG\_GRAPH\_CONTROL\_allowed |
| ORCA\_CATALOG\_GRAPH\_CONTROL\_denied |
| ORCA\_GRAPH\_CONTROL\_allowed |
| ORCA\_GRAPH\_CONTROL\_denied |
| ORCA\_CATALOG\_GRAPH\_CREATE\_allowed |
| ORCA\_CATALOG\_GRAPH\_CREATE\_denied |
| ORCA\_CATALOG\_GRAPH\_DROP\_allowed |
| ORCA\_CATALOG\_GRAPH\_DROP\_denied |
| ORCA\_CATALOG\_TABLE\_READ\_allowed |
| ORCA\_CATALOG\_TABLE\_READ\_denied |
| ORCA\_TABLE\_READ\_allowed |
| ORCA\_TABLE\_READ\_denied |
| ORCA\_CATALOG\_TABLE\_WRITE\_allowed |
| ORCA\_CATALOG\_TABLE\_WRITE\_denied |
| ORCA\_TABLE\_WRITE\_allowed |
| ORCA\_TABLE\_WRITE\_denied |
| ORCA\_CATALOG\_TABLE\_CREATE\_allowed |
| ORCA\_CATALOG\_TABLE\_CREATE\_denied |
| ORCA\_CATALOG\_TABLE\_DROP\_allowed |
| ORCA\_CATALOG\_TABLE\_DROP\_denied |
| ORCA\_CATALOG\_ENGINE\_MANAGE\_allowed |
| ORCA\_CATALOG\_ENGINE\_MANAGE\_denied |
| ORCA\_ENGINE\_MANAGE\_allowed |
| ORCA\_ENGINE\_MANAGE\_denied |
