# getUserPasswordStatus

首发版本：3.00.3

## 语法

`getUserPasswordStatus([user])`

## 详情

获取用户 *user* 的密码状态，省略参数 *user* 时获取集群中除 admin 以外所有用户的密码状态。

## 参数

**user** 可选参数，STRING 类型标量，表示用户名。

## 返回值

返回一个表，包含以下字段：

* user：用户名
* setTime：当前密码的设置时间
* expireTime：密码的过期时间
* authMode：密码验证方式，可能的取值包括 "SHA256" 和 "SCRAM”"

## 例子

```
getUserPasswordStatus(`user1)
```

| user | setTime | expireTime | authMode |
| --- | --- | --- | --- |
| user1 | 2025.03.27 11:51:09.154259866 | 2025.04.26 11:51:09.154259866 | SHA256 |
