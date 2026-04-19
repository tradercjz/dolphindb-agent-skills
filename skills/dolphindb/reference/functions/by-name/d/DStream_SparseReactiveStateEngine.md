# DStream::sparseReactiveStateEngine

首发版本：3.00.5

## 语法

`DStream::sparseReactiveStateEngine(metrics, keyColumn,
[extraColumn])`

## 详情

创建流计算稀疏响应式状态引擎。参考：createSparseReactiveStateEngine。

## 参数

**metrics** 是一个表，表示稀疏状态计算规则集合。该表至少包含 3 列：

* 前若干列为特定数据的标识列，与 *keyColumn* 指定的列名和顺序一致。
* formula：可以是字符串或元代码，表示该特定数据到达时触发的计算表达式。
* outputMetricKey：字符串标量，为该计算指定指标名。

**注**：Orca 中包含自定义函数的 formula 仅支持 `<>` 格式的元代码。

**keyColumn** 字符串标量或向量，表示输入表中标识特定数据的主键列名。

**extraColumn** 可选参数，字符串标量或向量，表示输入表中需要保留到输出表的列名。

## 返回值

返回一个 DStream 对象。

## 例子

```
// 若 catalog 不存在则创建
if (!existsCatalog("orca")) {
    createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph("sparseGraph")
g = createStreamGraph("sparseGraph")

// 定义输入流表结构与输出表结构、稀疏响应式状态引擎

baseStream = g.source("trade", `timestamp`date`deviceId1`deviceId2`deviceId3`value1`value2`value3, [TIMESTAMP, DATE, STRING, STRING, STRING, DOUBLE, DOUBLE, DOUBLE])
formulas = [<cumsumTopN(value1, value2, 5)>, <cumavgTopN(value1, value2, 10)>, <cumstdTopN(value1, value2, 15)>, <cumstdpTopN(value1, value2, 20)>, <cumvarTopN(value1, value2, 5)>, <cumvarpTopN(value1, value2, 10)>, <cumskewTopN(value1, value2, 10)>, <cumkurtosisTopN(value1, value2, 10)>, <cumbetaTopN(value1, value2, value3, 10)>, <cumcorrTopN(value1, value2, value3, 10)>, <cumcovarTopN(value1, value2, value3, 10)>, <cumwsumTopN(value1, value2, value3, 10)>]
keys = "A"+string(1..size(formulas))
keys1 = keys.shuffle()
keys2 = keys.shuffle()
outKeys = "event"+string(1..size(formulas))
metrics = table(
    keys1 as deviceId1,
    keys2 as deviceId2,
    formulas as formula,
    outKeys as outputMetricKey
)
baseStream.sparseReactiveStateEngine(metrics, `deviceId1`deviceId2, `timestamp`date)
.setEngineName("srsEngine")
.sink("output")
g.submit()
go

// 写入数据到 Orca 流表
n = 10000
for(i in 1..5){
    data = table(rand(timestamp(1..1000), n) as timestamp, rand(date(1..1000), n) as date, rand(keys, n) as deviceId1, rand(keys, n) as deviceId2, take(keys, n) as deviceId3, rand(rand(-1000.0:1000.0, n) join take(double(), n/5), n) as value1, rand(rand(-1000.0:1000.0, n) join take(double(), n/5), n) as value2, rand(rand(-1000.0:1000.0, n) join take(double(), n/5), n) as value3)
    appendOrcaStreamTable("trade", data)
}
sleep(3000)
res = select * from orca_table.output
```

**相关函数**：createSparseReactiveStateEngine
