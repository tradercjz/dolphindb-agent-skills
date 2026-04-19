# getSessionExpiredTime

首发版本：3.00.3

## 语法

`getSessionExpiredTime()`

## 详情

在启用严格安全策略（参见配置项*strictSecurityPolicy*）时，通过此函数查看会话的过期时间。

## 参数

无

## 返回值

空值或 DURATION 类型标量。

## 例子

```
getSessionExpiredTime() // output: 1H
```
