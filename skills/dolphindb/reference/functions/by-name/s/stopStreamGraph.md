# stopStreamGraph

首发版本：3.00.4

## 语法

`stopStreamGraph(name)`

### 详情

暂停指定流图。该函数成功执行后将是指定流图状态变为 stopped。

可通过 `getStreamGraphMeta` 查看流图状态。

**返回值：**无

### 参数

**name** 字符串标量，表示需要暂停的流图名称。可以传入完整的流图全限定名（如
catalog\_name.orca\_graph.graph\_name），也可以仅提供流图名（如 factors）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

### 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go

use catalog orca

def callTimes(mutable call, mutable tempTable, msg) {
    call += 1
    price = [call]
    volume = [call]
    t = table(price, volume)
    tempTable.append!(t)
    return t
}
name = "UDF"
g = createStreamGraph(name)
ckptConfig = {
    "enable":true,
    "interval": 10000,
    "timeout": 36000,
    "maxConcurrentCheckpoints": 1
};

g.source("trade", `price`volume, [INT,INT])
 .udfEngine(callTimes,["price", "volume"], [`cnt, `tmpTable], [433, table(128:0, ["price","volume"], [INT, INT])])
 .setEngineName("udf")
 .sink("output")
g.submit(ckptConfig)
go
getStreamGraphMeta()
stopStreamGraph("UDF") // 暂停流图，流图状态变为 stopped
startStreamGraph("UDF") // 开始流图，流图状态变为 running
```

**相关函数：**createStreamGraph, startStreamGraph
