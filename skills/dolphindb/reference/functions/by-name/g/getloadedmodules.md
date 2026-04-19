# getLoadedModules

首发版本：3.00.5，3.00.4.3

## 语法

`getLoadedModules()`

## 详情

查询当前会话中已经加载的模块。

注：

如果已通过 *preloadModules* 配置项加载指定模块，则每个会话都默认加载了该模块，所以会在返回结果中展示。

## 参数

无。

## 返回值

返回一张表，包含以下字段：

* moduleName：模块名称。
* moduleVersion：模块版本。
* isFree：是否为免费模块。

如果是自定义模块，moduleVersion 为空，isFree 为 true。

## 例子

假设已通过 use 语句加载 alphalens 和 ops 模块：

```
getLoadedModules()
```

返回一张模块信息表，如下所示：

| moduleName | moduleVersion | isFree |
| --- | --- | --- |
| alphalens | 1.0.0 | true |
| ops | 1.0.0 | true |

**相关函数**

loadModule
