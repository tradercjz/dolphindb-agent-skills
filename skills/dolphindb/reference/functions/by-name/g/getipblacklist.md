# getIPBlackList

首发版本：3.00.3

## 语法

`getIPBlackList()`

## 详情

查看当前集群的 IP 黑名单。

## 参数

无

## 返回值

字符串向量。

## 例子

```
addIPBlackList(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
removeIPBlackList("2.2.2.2")
getIPBlackList()
// output: ["1.1.1.1", "3.3.3.3"]
```

相关函数：addIPBlackList、removeIPBlackList
