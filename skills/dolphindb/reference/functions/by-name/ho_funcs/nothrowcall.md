# nothrowCall

首发版本：3.00.5

## 语法

`nothrowCall(func, args...)`

别名：nothrow

## 详情

用指定的参数调用一个函数。调用语法与 call 相同。

与 `call` 的区别在于，`nothrowCall`
在执行过程中即使发生错误也不会抛出异常。但如果提供的参数数量与*func*所需参数数量不匹配，`nothrowCall`
仍会抛出异常。

## 参数

**func** 是一个函数名。

**args** 是函数 *func* 的参数。

## 返回值

取决于 `func(args)` 的返回值。

## 例子

在准备 DolphinDB 系统环境时，通常需要先清理环境，比如删除已存在的流数据表。但有时无法确定某个流数据表是否已存在。若直接调用 dropStreamTable，当表不存在时会抛出异常。此时可直接使用 `nothrowCall` 忽略该异常。

以下示例中假设流数据表 orderData 并不存在：

```
dropStreamTable(`orderData)
//抛出异常：Can't find stream table orderData

nothrowCall(dropStreamTable, `orderData)
//正常执行，无异常抛出
```

**相关函数：**call
