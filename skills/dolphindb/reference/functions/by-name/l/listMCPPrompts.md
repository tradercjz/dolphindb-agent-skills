# listMCPPrompts

首发版本：3.00.4

## 语法

`listMCPPrompts()`

## 详情

查看当前用户具有 MCP\_EXEC 权限的 MCP prompt 模板。

## 返回值

一张表，包含以下字段：

* name：STRING 类型，prompt 模板的名称。
* message：STRING 类型，prompt 模板的内容。
* description：STRING 类型，prompt 模板的描述。
* title：STRING 类型，prompt 模板的 title。
* lastModifyTime：TIMESTAMP 类型，最后一次修改时间。
* publishTime：TIMESTAMP 类型，发布时间。

## 例子

```
listMCPPrompts()
```

返回结果

| name | message | description | title | lastModifyTime | publishTime |
| --- | --- | --- | --- | --- | --- |
| stock\_summary | 请总结 ${stock} 在 ${startDate} 至 ${endDate} 的表现。 | 更新后的 Prompt 描述 | 股票走势总结 | 2025.08.24 17:17:29.091 |  |
