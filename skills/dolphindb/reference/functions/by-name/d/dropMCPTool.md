# dropMCPTool

首发版本：3.00.4

## 语法

`dropMCPTool(name)`

## 详情

删除一个 MCP tool。如果该 tool 已被发布，需要先调用 `withdrawMCPTools` 撤销发布后才能删除。

## 参数

**name** STRING 类型标量，表示 tool 的名称。

## 返回值

一个字符串，表示删除 tool 的名称。

## 例子

```
dropMCPTool("myTool")
```
