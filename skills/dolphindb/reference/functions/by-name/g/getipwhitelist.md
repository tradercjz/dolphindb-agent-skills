# getIPWhiteList

首发版本：3.00.3

## 语法

`getIPWhiteList()`

## 详情

查看当前集群的 IP 白名单。

## 参数

无

## 返回值

字符串向量。

## 例子

```
addIPWhiteList(["1.1.1.1", "2.2.2.2", "3.3.3.3"])
removeIPWhiteList("2.2.2.2")
getIPWhiteList()
// output: ["1.1.1.1", "3.3.3.3"]
```

相关函数：addIPWhiteList、removeIPWhiteList
