# getRawScriptLog

首发版本：3.00.4，3.00.3.1

## 语法

`getRawScriptLog([userId],[startTime],[endTime])`

## 详情

查询用户原始代码日志。该函数仅支持管理员调用。

## 参数

**userId** 字符串标量或向量，指定查询哪些用户的原始代码日志。默认为空，表示查询所有用户。

**startTime** 整型或时间类型标量，指定查询的起始时间。默认为 0，表示查询从 1970.01.01 开始的记录。

**endTime** 整型或时间类型标量，指定查询的结束时间。默认为空，表示查询到目前为止的记录。*startTime* 必须小于等于
*endTime*。

## 返回值

一张表，包含以下字段：

* node：字符串，执行脚本的节点名。
* username：字符串，执行脚本的用户名。
* sessionID：LONG 标量，当前会话 ID。
* rootJobID：字符串，当前 rootJob 的ID。
* remoteIP：IPADDR 标量，用户 IP。
* remotePort：INT 标量，用户端口。
* startTime：NANOTIMESTAMP 标量，脚本执行开始时间。
* endTime: NANOTIMESTAMP 标量，脚本执行结束时间。
* script：字符串，完整脚本代码。
* errorMsg：字符串，如果脚本执行过程报错，记录错误信息，否则为空。

## 例子

查询用户 user1 的原始代码日志：

```
getRawScriptLog(`user1)
```
