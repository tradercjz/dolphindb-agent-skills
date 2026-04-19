# useOrcaStreamTable

首发版本：3.00.3

## 语法

`useOrcaStreamTable(name, func, args...)`

## 详情

该函数通过 orca 流表名称定位其所在节点，并在该节点获取流表对象。随后将该流表作为首个参数传递给用户指定的函数 *func* 并执行。

该机制允许用户在本地代码中远程调用与操作流表相关的函数（如
`replay`、`getStreamTableFilterColumn`
等），无需手动管理节点和流表对象的绑定。

## 参数

**name** 表示流表的名称。字符串标量，可以传入完整的流表全限定名（如
"trading.orca\_table.trades"）；也可以仅提供流表名（如 "trades"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**func** 在流表所在节点上执行的函数，可以是内置函数或自定义函数。该函数必须至少包含一个参数，系统会将流表对象自动作为第一个参数传入。

**args…** 传递给 *func* 的其他参数，使用方式类似于远程过程调用函数 rpc 的 *args…* 参数。

## 返回值

返回值是用户指定的函数 *func* 的执行结果。

## 例子

通过 `getStreamTableFilterColumn` 函数查看
`demo.orca_table.transaction` 流表的过滤列：

```
useOrcaStreamTable("demo.orca_table.transaction", getStreamTableFilterColumn)
```
