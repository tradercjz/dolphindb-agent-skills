# getCurrentSessionAndUser

## 语法

`getCurrentSessionAndUser()`

## 详情

获取当前 session 的 session ID、用户名、远程 IP 地址和远程端口号。

## 参数

无

## 返回值

返回一个元组，第一个元素为 sessionId，第二个元素为 userId（若未登录，则返回"guest")，第三个元素为 remoteIP，第四个元素为
remotePort。

## 例子

```
getCurrentSessionAndUser()

//Output (2333906441, "admin", "127.0.0.1", 60302)
```
