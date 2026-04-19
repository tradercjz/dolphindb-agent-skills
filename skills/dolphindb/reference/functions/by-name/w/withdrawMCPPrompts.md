# withdrawMCPPrompts

首发版本：3.00.4

## 语法

`withdrawMCPPrompts([names])`

## 详情

撤销已发布的 MCP prompt 模板。

## 参数

**names** 可选参数，STRING 类型标量或向量，表示 prompt 模板的名称。

## 返回值

一个 STRING 类型向量，表示撤销成功的 prompt 模板。

## 例子

```
withdrawMCPPrompts("stock_summary")
// output:["stock_summary"]
```
