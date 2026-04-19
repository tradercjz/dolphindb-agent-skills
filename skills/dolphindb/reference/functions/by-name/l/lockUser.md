# lockUser

首发版本：3.00.3

## 语法

`lockUser(userId)`

## 详情

锁定用户 *userId*。该函数仅限管理员用户调用，调用时须开启配置项 *enhancedSecurityVerification*。

## 参数

**userId** 是表示用户名的字符串。

## 返回值

无。

## 例子

```
lockUser("user1")
```

相关函数：unlockUser
