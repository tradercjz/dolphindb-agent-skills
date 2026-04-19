# getMachineFingerprint

## 语法

`getMachineFingerprint(outputPath)`

别名：`generateMachineFingerprint`

## 参数

**outputPath** 是字符串，表示存放机器指纹的目录。

## 详情

生成机器指纹，用于 license 验证。该命令必须要用户登录后才能执行。Windows 操作系统下执行该函数需要管理员权限。

## 例子

```
generateMachineFingerprint("/home/DolphinDB")
```
