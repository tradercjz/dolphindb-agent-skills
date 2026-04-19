# removeIPBlackList

首发版本：3.00.3

## 语法

`removeIPBlackList(ips)`

## 详情

从黑名单中移除 IP。当所有 IP 都从黑名单中移除后，即为关闭黑名单。

此函数仅可由管理员执行，对整个集群生效。

## 参数

**ips** 是 STRING 或 IPADDR 类型的标量或向量，表示一个或多个 IP 地址。

## 例子

```
addIPBlackList(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
removeIPBlackList("2.2.2.2")
getIPBlackList()
// output: ["1.1.1.1", "3.3.3.3"]
```

相关函数：addIPBlackList、getIPBlackList
