# getStreamEngineList

## 语法

`getStreamEngineList()`

## 详情

获取当前节点上所有流计算引擎的信息。

## 参数

无

## 返回值

一个表，包含以下字段：

* engineType：引擎的类型。
* engineName：引擎的名称。
* user：创建引擎的用户名。

## 例子

假设在当前节点上，admin 用户已创建1个时序引擎和1个 window join 引擎，user1 用户已创建1个响应式状态引擎，则调用
`getStreamEngineList` 后返回可以所有已创建引擎的信息。

```
getStreamEngineList()
```

| engineType | engineName | user |
| --- | --- | --- |
| ReactiveStreamEngine | reactiveDemo | user1 |
| WindowJoinEngine | test1 | admin |
| TimeSeriesEngine | engine1 | admin |
