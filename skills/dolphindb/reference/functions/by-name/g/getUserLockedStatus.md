# getUserLockedStatus

首发版本：3.00.3

## 语法

`getUserLockedStatus()`

## 详情

查看系统中用户的锁定状态。该函数仅限管理员用户调用，调用时须开启配置项 *enhancedSecurityVerification*。

## 返回值

返回一张表，包含以下字段：

* user：处于锁定状态的用户名。
* IP：用户被锁定的 IP。若该用户由管理员通过 `lockUser` 函数锁定，则该列为 ”\*“。
* lockTime：锁定的起始时间。
* unlockTime：预期解锁时间，若该用户由管理员通过 `lockUser` 函数锁定，则该列为空。

## 例子

```
getUserLockedStatus()
```

| user | IP | lockTime | unlockTime |
| --- | --- | --- | --- |
| user2 | \* | 2025.03.27 11:27:36.597 |  |
| user1 | 192.168.0.140 | 2025.03.27 11:27:23.916 | 2025.03.27 11:32:23.916 |
