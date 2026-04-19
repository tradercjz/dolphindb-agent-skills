# enableTDEKey

首发版本：3.00.3

## 语法

`enableTDEKey(masterKeyPath)`

## 详情

启用数据静态加密并初始化 TDE 密钥。该函数必须由管理员在控制节点执行。仅 Linux 系统支持该功能。

完成主密钥设置后，用户可以调用函数 getCurrentTDEKeyVersion 查询当前主密钥版本，验证加密配置是否生效。

## 参数

**masterKeyPath** 字符串标量，指定 TDE 密钥文件的路径。

## 返回值

如果设置成功，函数返回 true。如函数报错，请检查密钥路径是否正确，以及文件是否符合密钥格式要求。

## 例子

```
enableTDEKey(path/to/key)
```
