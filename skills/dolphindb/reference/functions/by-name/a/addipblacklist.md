# addIPBlackList

首发版本：3.00.3

## 语法

`addIPBlackList(ips)`

## 详情

新增 IP 到黑名单中。添加第一个 IP 即为启用黑名单，IP 黑名单与白名单只能同时启用一种。启用黑名单后，服务器会拒绝来自黑名单中 IP 的连接请求。

此函数仅可由管理员执行，对整个集群生效。

## 参数

**ips** 是 STRING 或 IPADDR 类型的标量或向量，表示一个或多个 IP 地址。最多支持设置 65535 个 IP。

## 例子

```
addIPBlackList(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
```

相关函数：removeIPBlackList、getIPBlackList
