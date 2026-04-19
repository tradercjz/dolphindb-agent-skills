# getAuthenticatedUserTicket

首发版本：3.00.3

## 语法

`getAuthenticatedUserTicket([expire])`

## 详情

生成当前已登录用户的动态登录口令，并可设置口令过期时间。用户可使用该口令，通过`authenticateByTicket(ticket)`进行免密登录。

## 参数

**expire** 是一个 DATETIME 标量，表示登录口令的过期时间。

## 返回值

字符串标量。

## 例子

```
login("user1", "123456")
getAuthenticatedUserTicket(2030.12.31T12:00:00)
/ output:
VQEpuZYCbwhPDj6qvuyW+zDwdnQI3HiUhfJOpyUW/J5X5XZmponkmE6n5COI1xUP
xCVr29VHsNYOV00tGZrFkGKPOJhjWJtSt85ok5s8EVYXwZCgdrYjdharJLBk/e04
u1oBC0/6nD4WdDM68pCbsZgUqDe94+czqG0M21Sy8PA=
/
```
