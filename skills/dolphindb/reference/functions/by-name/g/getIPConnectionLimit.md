# getIPConnectionLimit

首发版本：3.00.4

## 语法

`getIPConnectionLimit()`

## 详情

获取当前节点对不同 IP 的连接数限制。该限制适用于 API 连接和 `xdb` 连接，不会限制集群内部节点间的连接（如
`rpc` 等）。

仅支持管理员调用，仅支持 Linux 系统部署的 server。

## 参数

无。

## 返回值

返回一个表，包含两列：

* remoteIP：表示 IP 地址。
* limit：表示该 IP 地址允许的最大连接数。

## 例子

```
getIPConnectionLimit();
```

| remoteIP | limit |
| --- | --- |
| 192.168.1.56 | 10 |
| 192.168.1.57 | 20 |

相关函数：setIPConnectionLimit
