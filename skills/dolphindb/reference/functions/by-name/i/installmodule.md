# installModule

首发版本：3.00.5，3.00.4.3

## 语法

`installModule(moduleName, [serverAddr])`

## 详情

下载并解压指定模块到节点的模块目录下。可通过 listRemoteModules 函数查询可供下载的模块。

## 参数

**moduleName** STRING 类型标量，用于指定模块名称。

**serverAddr** 可选参数，STRING 类型标量，用于指定模块仓库的 HTTP 地址。默认为 "http://dolphindb.cn" 。

## 返回值

无。

## 例子

从市场下载名为 ops 的模块：

```
installModule("ops")
```

**相关函数**

listRemoteModules

loadModule
