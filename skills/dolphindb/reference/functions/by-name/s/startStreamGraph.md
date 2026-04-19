# startStreamGraph

首发版本：3.00.4

## 语法

`startStreamGraph(name)`

## 详情

重启指定流图。该函数成功执行后将使指定流图状态变为 running。可通过 getStreamGraphMeta 查看流图状态。

在使用该功能时，建议通过 setConfigMap
明确设置数据源消费策略（subscription.sourceOffset**）**，以控制暂停期间的数据处理方式。

* sourceOffset =
  -1（推荐）：流图重启时从源表当前最新一条数据开始消费。暂停期间收到的数据将被忽略，适用于只关心实时数据、不需处理历史数据的场景。
* sourceOffset =
  -3（默认，谨慎使用）：流图重启时会从源表第一行开始回放所有历史数据，可能消耗大量资源并产生重复计算，适用于需保证绝对数据完整性且源表数据量可控的场景。

**返回值：**无

## 参数

**name** 字符串标量，表示需要重启的流图名称。可以传入完整的流图全限定名（如
catalog\_name.orca\_graph.graph\_name），也可以仅提供流图名（如 factors）；系统会根据当前的 catalog
设置自动补全为对应的全限定名。

## 例子

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

**相关函数：**createStreamGraph, stopStreamGraph
