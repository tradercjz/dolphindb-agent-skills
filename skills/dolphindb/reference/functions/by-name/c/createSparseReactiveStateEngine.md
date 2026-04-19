# createSparseReactiveStateEngine

首发版本：3.00.5

## 语法

`createSparseReactiveStateEngine(name, metrics, dummyTable, outputTable,
keyColumn, [extraColumn])`

## 详情

创建一个稀疏响应式状态引擎，用于对数据进行稀疏状态计算：仅当某些特定的数据到达时，才触发与之相关的状态计算。

该引擎适用于工业场景下“规则只对部分设备/传感器有意义”的稀疏计算需求。相比
`createReactiveStateEngine`，可避免无意义的全量指标更新。

## 参数

**name** 字符串标量，表示响应式状态引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics** 是一个表，表示稀疏状态计算规则集合。该表至少包含 3 列：

* 前若干列为特定数据的标识列，与 *keyColumn* 指定的列名和顺序一致。
* formula：可以是字符串或元代码，表示该特定数据到达时触发的计算表达式。
* outputMetricKey：字符串标量，为该计算指定指标名。

**dummyTable** 一个表对象，和输入的流数据表的 schema 一致，可以含有数据，亦可为空表。

**outputTable** 计算结果的输出表，可以是内存表或分布式表，引擎会将计算结果写入该表。包含以下列：

* 若干特定数据标识列，与 *keyColumn* 指定的列名和顺序一致。
* 若干保留的原始列，与 *extraColumn* 指定的列名和顺序一致。
* outputMetricKey 列，表示特定数据计算的指标名，其值由 *metrics* 的 outputMetricKey 列指定。
* 计算结果列，表示该指标的计算结果。

**keyColumn** 字符串标量或向量，表示输入表中标识特定数据的主键列名。

**extraColumn** 可选参数，字符串标量或向量，表示输入表中需要保留到输出表的列名。

## 返回值

返回一个流数据引擎对象句柄。通过向该句柄写入，将数据注入引擎进行计算。

## 例子

例1. 输入数据包含三个设备 ID A001，A002，A003。每当 A001 的数据到来，计算长度为 3 的滑动窗口内数据的平均值；每当 A002
的数据到来，计算长度为 3 的滑动窗口内的最大值与最小值的差，以及窗口内元素的和 ；当 A003
的数据到来不做任何处理。输入数据中的时间列不做处理，保留到输出表中。

```
// 创建输入数据表
share streamTable(1:0, `timestamp`deviceID`value,
    [TIMESTAMP, SYMBOL, DOUBLE]) as inputTable

// 创建输出表
share streamTable(1000:0, `deviceID`timestamp`outputMetricKey`outputValue,
    [SYMBOL, TIMESTAMP, STRING, DOUBLE]) as outputTable

// 定义规则
metrics = table(
    ["A001", "A002", "A002"] as deviceID,
    [
        "mavg(value,3) ",
        "mmax(value,3)-mmin(value,3)",
        "msum(value,3)"
    ] as formula,
    ["A001_1", "A002_1", "A002_2"] as outputMetricKey
)

// 创建稀疏状态引擎
stateEngine = createSparseReactiveStateEngine(
    name="demoengine",
    metrics=metrics,
    dummyTable=inputTable,
    outputTable=outputTable,
    keyColumn="deviceID",
    extraColumn="timestamp"
)
// 订阅输入流表
subscribeTable(tableName="inputTable", actionName="demo1", handler=tableInsert{stateEngine})
// 写入数据
data = table([2026.02.07T20:29:53.927,2026.02.07T20:29:53.928,2026.02.07T20:29:53.929,2026.02.07T20:29:53.930,2026.02.07T20:29:53.931,2026.02.07T20:29:53.932,2026.02.07T20:29:53.933,2026.02.07T20:29:53.934,2026.02.07T20:29:53.935,2026.02.07T20:29:53.936,2026.02.07T20:29:53.937,2026.02.07T20:29:53.938,2026.02.07T20:29:53.939,2026.02.07T20:29:53.940,2026.02.07T20:29:53.941,2026.02.07T20:29:53.942,2026.02.07T20:29:53.943,2026.02.07T20:29:53.944,2026.02.07T20:29:53.945,2026.02.07T20:29:53.946] as time,
    ["A003","A002","A003","A002","A003","A002","A002","A001","A003","A001","A002","A003","A001","A002","A003","A002","A003","A002","A003","A002"] as deviceID,
    [47,87,36,63,28,53,65,48,86,40,18,28,61,77,81,73,66,47,29,3] as value)

inputTable.append!(data)
// 查看结果
result = select * from outputTable
result
```

| deviceID | timestamp | outputMetricKey | outputValue |
| --- | --- | --- | --- |
| A002 | 2026.02.07 20:29:53.928 | A002\_1 |  |
| A002 | 2026.02.07 20:29:53.928 | A002\_2 |  |
| A002 | 2026.02.07 20:29:53.930 | A002\_1 |  |
| A002 | 2026.02.07 20:29:53.930 | A002\_2 |  |
| A002 | 2026.02.07 20:29:53.932 | A002\_1 | 34 |
| A002 | 2026.02.07 20:29:53.932 | A002\_2 | 203 |
| A002 | 2026.02.07 20:29:53.933 | A002\_1 | 12 |
| A002 | 2026.02.07 20:29:53.933 | A002\_2 | 181 |
| A001 | 2026.02.07 20:29:53.934 | A001\_1 |  |
| A001 | 2026.02.07 20:29:53.936 | A001\_1 |  |
| A002 | 2026.02.07 20:29:53.937 | A002\_1 | 47 |
| A002 | 2026.02.07 20:29:53.937 | A002\_2 | 136 |
| A001 | 2026.02.07 20:29:53.939 | A001\_1 | 49.666666666666664 |
| A002 | 2026.02.07 20:29:53.940 | A002\_1 | 59 |
| A002 | 2026.02.07 20:29:53.940 | A002\_2 | 160 |
| A002 | 2026.02.07 20:29:53.942 | A002\_1 | 59 |
| A002 | 2026.02.07 20:29:53.942 | A002\_2 | 168 |
| A002 | 2026.02.07 20:29:53.944 | A002\_1 | 30 |
| A002 | 2026.02.07 20:29:53.944 | A002\_2 | 197 |
| A002 | 2026.02.07 20:29:53.946 | A002\_1 | 70 |
| A002 | 2026.02.07 20:29:53.946 | A002\_2 | 123 |

**相关函数**：addSparseReactiveMetrics, getSparseReactiveMetrics, deleteSparseReactiveMetric
