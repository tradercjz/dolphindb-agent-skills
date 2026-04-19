# createReactiveStatelessEngine

## 语法

`createReactiveStatelessEngine(name, metrics, outputTable, [snapshotDir],
[snapshotIntervalInMsgCount], [filter], [dummyTable], [keyColumn],
[timeColumn])`

## 详情

创建一个响应式无状态引擎，基于当前最新值与其他指标结果进行组合计算，支持对不同数据设置独立的触发规则和计算逻辑。

注：

不支持乱序处理机制，用户需要自行保证输入的数据有序。

## 计算规则

引擎每有一批数据注入，会根据参数 metrics
中定义的依赖关系，将任何直接依赖或间接依赖这批数据的数据输出，每次输出的条数等于直接或间接依赖这批数据的变量个数。即使这个变量的值没有改变，也会输出。

## 参数

**name** 字符串标量，表示引擎的名称，作为其在一个数据节点/计算节点上的唯一标识。可包含字母，数字和下划线，但必须以字母开头。

**metrics** 可以是表或字典数组，表示规则集合。

* 当 *metrics* 为表时：必须以下四列：

  + formula：STRING 类型，表示计算逻辑。其中的变量采用 *keyColumn*
    指定的列中的值标识，*keyColumn* 如不止一列，则使用 `:`
    连接各值。
  + outputMetricKey：STRING 类型，为该计算指定指标名。
  + triggerOn：STRING 类型，表示触发该计算的数据标识，即 *keyColumn*
    指定的列为该值时触发计算，*keyColumn* 如不止一列，则使用 `:`
    连接各值 。
  + filter：一个数据对，表示计算结果的限定范围，属于该范围的结果才会被输出。
* 当 *metrics* 为字典数组时：每个字典表示一条规则，包含键值 *outputName*，formula 以及可选键值
  triggerOn，filter。

**outputTable** 输出表，包含以下列：

* 若干特定数据标识列，与 *keyColumn* 指定的列名和顺序一致。
* 若干时间列，与 *timeColumn* 指定的列名和顺序一致。
* DOUBLE 类型列的计算结果列 outputValue。

**snapshotDir** 可选参数，字符串，表示保存引擎快照的文件目录。

* 指定的目录必须存在，否则系统会提示异常。
* 创建流数据引擎时，如果指定了 *snapshotDir*，会检查该目录下是否存在快照。如果存在，会加载该快照，恢复引擎的状态。
* 多个引擎可以指定同一个目录存储快照，用引擎的名称来区分快照文件。
* 一个引擎的快照可能会使用三个文件名：

  + 临时存储快照信息：文件名为 <engineName>.tmp；
  + 快照生成并刷到磁盘：文件保存为 <engineName>.snapshot；
  + 存在同名快照：旧快照自动重命名为 <engineName>.old。

**snapshotIntervalInMsgCount** 可选参数，为整数类型，表示每隔多少条数据保存一次流数据引擎快照。

**filter** 可选参数，一个数据对，表示引擎级整体输出过滤范围。仅当 *metrics*
中没有设置为空时才使用该整体过滤。

**dummyTable** 可选参数，是一个表，表示用于初始化引擎的样例表，其 schema 必须与订阅的流数据表一致。当指定 *keyColumn*
或 *timeColumn* 时，*dummyTable* 为必填参数。

**keyColumn** 可选参数，字符串标量或向量，表示输入表中用于标识数据的列名。

**timeColumn**
可选参数，字符串标量或向量，表示输入表的时间戳列名。配置后输出表包含对应时间列，其值为触发本次计算的数据时间；若多个计算触发同时触发，取最大时间。

## 返回值

返回一个流数据引擎对象句柄，向该句柄写入数据，即为将数据注入引擎。

## 例子

例1. 现有一个窄表，表中信息如下

| productName | metricName | value |
| --- | --- | --- |
| product\_A | factor1 | 1 |
| product\_A | factor2 | 2 |
| product\_B | factor1 | 1 |
| product\_B | value | 4 |
| product\_C | factor1 | 2 |
| product\_C | value | 8 |

上表中，product\_A:factor1, product\_A:factor2, product\_B:factor1, product\_C:factor1
完全由外部输入决定；一些数据依赖其他数据的值
product\_B:value=product\_A:factor1+product\_A:factor2+product\_B:factor1，product\_C:value=product\_B:value\*product\_C:factor1

根据以上信息，通过以下脚本创建引擎

```
// 创建输出表
names = `product`metric`value
types = [STRING, STRING, DOUBLE]
outputTable = table(1:0, names, types)

// 创建 metrics 描述数据间的依赖关系
metrics = array(ANY, 0, 0)
metric1 = dict(STRING,ANY)
// 依赖关系 product_B:value=product_A:factor1+product_A:factor2+product_B:factor1
metric1["outputName"] = `product_B:`value
metric1["formula"] = <A+B+C>
metric1["A"] = `product_A:`factor1
metric1["B"] = `product_A:`factor2
metric1["C"] = `product_B:`factor1
metrics.append!(metric1)
// 依赖关系 product_C:value=product_B:value*product_C:factor1
metric2 = dict(STRING, ANY)
metric2["outputName"] =`product_C:`value
metric2["formula"] = <A*B>
metric2["A"] = `product_B:`value
metric2["B"] = `product_C:`factor1
metrics.append!(metric2)

// 创建引擎
engine1 = createReactiveStatelessEngine("engine1", metrics, outputTable)
```

每次插入数据，无论插入的数据量有多大，都只会返回一次。

第一次插入2条数据，此时，两个依赖关系所需的数据尚不完整，无法计算得到需要的结果，所以输出表中对应值为空。

```
insert into engine1 values(["product_A","product_A"],["factor1","factor2"],[1,2])
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |

第二次插入1条数据，此时，第一个依赖关系所需数据已经完整，故得到结果，第二个依赖关系所需数据仍不完整，对应值为空。

```
insert into engine1 values("product_B","factor1",1)
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |

第三次插入1条数据，此时，第二个依赖关系所需数据完整，输出对应结果。

```
insert into engine1 values("product_C","factor1",2)
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
| product\_C | value | 8 |

第四次插入1条数据，此时，由于数据被修改，依赖此数据的相关数据均会受到影响，并将更新后的结果输出。

```
insert into engine1 values("product_C","factor1",3)
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
| product\_C | value | 8 |
| product\_C | value | 12 |

注意，数据更新后，即使依赖此数据的相关数据的值最终没有变化，也会将最新结果输出

```
insert into engine1 values(["product_A","product_A"],["factor1","factor2"],[2,1])
outputTable
```

| product | metric | value |
| --- | --- | --- |
| product\_B | value |  |
| product\_C | value |  |
| product\_B | value | 4 |
| product\_C | value |  |
| product\_C | value | 8 |
| product\_C | value | 12 |
| product\_B | value | 4 |
| product\_C | value | 12 |

如果只想获得变量的最新状态，可以创建键值表作为输出表

```
kt = keyedTable(`product`metric, 1:0, `product`metric`value, [STRING, STRING, DOUBLE])
```

例2. 一个表中实时记录有 factor1，factor2，factor3，factor4 的数据。要求每当 factor3 的数据来到时，计算
factor1+factor2+factor3 的结果 value1，以及 value1\*factor3 的结果 value2，且仅当 value2 属于
[10,40] 时才输出。

```
metricsTable = table(
    // 指标计算公式列表
    [
        '"factor1" + "factor2" + "factor3"',  // 对应 eventA 的计算逻辑
        '"value1"*"factor3"'                  // 模拟计算逻辑
    ] as formula,
    // 对应每个公式的输出指标名称
    ["value1", "value2"] as outputMetricKey,
    // 触发条件，仅当对应字段更新时计算公式
    ["factor3", ""] as triggerOn,
    // 输出过滤器，仅当结果值满足条件时输出
    [NULL,2.0:100.0] as filter  // 仅对 R134_A 生效，第二条为空
)

// 创建输入数据表和输出表
share streamTable(1000:0, `MetricKey`timestamp`value,[STRING, TIMESTAMP,DOUBLE]) as inputTable
share streamTable(1000:0, `MetricKey`timestamp`value,[STRING, TIMESTAMP,DOUBLE]) as outputTable

// 创建引擎
engine1 = createReactiveStatelessEngine("engine1", metricsTable, outputTable, dummyTable=inputTable, keyColumn=`MetricKey, timeColumn=`timestamp)
subscribeTable(tableName="inputTable", actionName="statelessEngine", handler=tableInsert{engine1})

// 插入数据
insert into inputTable values(["factor1","factor2"],[2025.10.11T09:00:00.000,2025.10.11T09:00:00.000], [1,2])
insert into inputTable values(["factor3"],[2025.10.11T09:00:01.000],[3])
insert into inputTable values(["factor4"],[2025.10.11T09:00:02.000],[3])
insert into inputTable values(["factor3"],2025.10.11T09:00:03.000,[4])
insert into inputTable values(["factor3"],2025.10.11T09:00:04.000,[6])

// 查看输出表
outputTable
```

| MetricKey | timestamp | value |
| --- | --- | --- |
| value1 | 2025.10.11 09:00:01.000 | 6 |
| value2 | 2025.10.11 09:00:01.000 | 18 |
| value1 | 2025.10.11 09:00:03.000 | 7 |
| value2 | 2025.10.11 09:00:03.000 | 28 |
| value1 | 2025.10.11 09:00:04.000 | 9 |

上述结果中可以看到， 09:00:01.000 时 factor3 的数据触发了 value1 和 value2 的计算。09:00:02.000 时 factor4
的数据并不会触发计算。09:00:03.000 和 09:00:04.000 时 factor3 的数据都触发了 value1 和 value2
的计算，但因09:00:04.000 时计算结果中 value2 大于 40，所以不会输出。
