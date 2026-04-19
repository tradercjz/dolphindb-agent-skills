# setSessionExpiredTime

首发版本：3.00.3

## 语法

`setSessionExpiredTime(expire)`

## 详情

在启用严格安全策略（参见配置项 *strictSecurityPolicy*）时，管理员可通过此函数设置会话过期时间。

## 参数

**expire** 是一个 DURATION 类型的标量，表示会话的有效期限。

## 例子

```
setSessionExpiredTime(3600s)  // 设置会话过期时间为1小时
getSessionExpiredTime() // output: 1H
```
