# useOrcaStreamEngine

首发版本：3.00.3

## 语法

`useOrcaStreamEngine(name, func, args...)`

## 详情

该函数通过 orca 流引擎名称定位其所在节点，并在该节点获取流引擎对象。随后将该引擎作为首个参数传递给用户指定的函数 *func* 并执行。

该机制允许用户在本地代码中远程调用各种流引擎相关函数，无需手动管理节点和流表对象的绑定。

## 参数

**name** 表示引擎名称。字符串标量，可以传入完整的全限定名（如
"catalog\_name.orca\_engine.engine\_name"）；或引擎名（如 "engine\_name"），系统会根据当前的 catalog
设置自动补全为对应的全限定名。

**func** 在流表所在节点上执行的函数。该函数必须至少包含一个参数，系统会将流引擎对象自动作为第一个参数传入。

**args…** 传递给 *func* 的其他参数，使用方式类似于远程过程调用函数 rpc 的 *args…* 参数。

## 返回值

返回值为用户指定的函数 *func* 的执行结果。

## 例子

通过 `getStreamEngineStateTable`函数查看 orca 响应式状态引擎 test.orca\_engine.rse
的状态：

```
if (!existsCatalog("test")) {
	createCatalog("test")
}
go;
use catalog test

t = table(1..100 as id, 1..100 as value, take(09:29:00.000..13:00:00.000, 100) as timestamp)
g = createStreamGraph("factor")
baseStream = g.source("snapshot",  schema(t).colDefs.name, schema(t).colDefs.typeString)
  .reactiveStateEngine([<ema(value, 100)>, <timestamp>])
  .setEngineName("rse")
  .buffer("end")

g.submit()
useOrcaStreamEngine("test.orca_engine.rse", getStreamEngineStateTable)

 /*
 value ema(value, 100) timestamp
----- --------------- ---------
*/
```

**相关函数：**getOrcaStreamEngineMeta
