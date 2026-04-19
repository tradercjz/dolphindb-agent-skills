# listRemoteModules

首发版本：3.00.5，3.00.4.3

## 语法

`listRemoteModules([serverAddr])`

## 详情

查询已在市场发布的模块。

## 参数

**serverAddr** 可选参数，STRING 类型标量，用于指定模块仓库的 HTTP 地址。默认为"http://dolphindb.cn"。

## 返回值

一张表，包含以下字段：

* moduleName：模块名称。
* moduleVersion：模块版本。

## 例子

列出市场上所有可供下载的模块：

```
listRemoteModules()
```

返回一张模块信息表，如下所示：

| moduleName | moduleVersion |
| --- | --- |
| DolphinDBModules | 1.0.0 |
| LogSearcher | 1.0.0 |
| alphalens | 1.0.0 |
| gtja191Alpha | 1.0.0 |
| marketHoliday | 1.0.0 |
| mytt | 1.0.0 |
| ops | 1.0.0 |

**相关函数**

installModule

loadModule
