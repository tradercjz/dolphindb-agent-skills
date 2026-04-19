# DStream::udfEngine

首发版本：3.00.4

## 语法

`DStream::udfEngine(func)`

## 详情

`DStream::udfEngine` 是 Orca
流图中用于执行用户自定义处理逻辑的扩展引擎。当内置流计算引擎无法满足特定业务需求时，用户可通过 `DStream::udfEngine`
设置自定义函数，对每条流消息进行映射处理。

为支持有状态计算，自定义函数可访问由
`DStream::sharedTable`、`DStream::sharedDict` 或
`DStream::sharedKeyedTable` 声明的共享变量。这些变量可在同一流图内的多个 udfEngine 实例和
task 之间共享，其状态由 Orca 通过 Checkpoint 机制自动持久化，并在故障恢复时重建。

**注意：**自定义函数中禁止访问任何外部变量。仅允许使用局部变量，或通过 `orcaObj("name")`
引用已声明的共享变量。

**共享变量使用约束**：

* 共享变量必须先通过
  `DStream::sharedTable`、`DStream::sharedDict`
  或 `DStream::sharedKeyedTable` 声明；在 `udfEngine`
  的 自定义函数中，通过 `orcaObj("name")` 引用。注意：`orcaObj`
  仅在自定义函数执行上下文中有效。
* 每个共享变量仅支持单写多读：只能有一个 udfEngine 实例写入，但允许多个实例并发读取。
* 访问同一共享变量的所有任务会被 Orca 调度到同一个物理节点，以保证本地访问和一致性。

## 参数

**func** 用户定义函数，只有一个参数，为流数据表。该参数不可被原地修改或作为可变对象操作。函数内部可读写由
`DStream::sharedTable`、`DStream::sharedDict` 或
`DStream::sharedKeyedTable` 定义的共享变量，实现状态更新。若函数有返回值，类型必须为字典或表。

## 返回值

返回一个 DStream 对象。

## 例子

下面通过 `DStream::sharedKeyedTable` 与 `DStream::udfEngine`
的结合，实现计算历史差值的功能。

在本示例中，使用 `DStream::sharedKeyedTable` 存储已处理数据的历史记录，对每个 id
仅保留最新的一条记录。当新数据到达时，若该 id 已存在于表中，则输出新值与历史值之间的差值；否则，仅将新数据存入表中，不产生输出。

下面通过 `DStream::sharedKeyedTable` 与 `DStream::udfEngine`
的结合，实现计算历史差值的功能。

在本示例中，使用 `DStream::sharedKeyedTable` 存储已处理数据的历史记录，对每个 id
仅保留最新的一条记录。当新数据到达时，若该 id 已存在于表中，则输出新值与历史值之间的差值；否则，仅将新数据存入表中，不输出。

```
if(existsCatalog("orcaCatalog")) dropCatalog("orcaCatalog")
createCatalog("orcaCatalog")
go
use catalog orcaCatalog
// 创建流图
g = createStreamGraph("compare")
g.sharedKeyedTable("history", "id", 1:0, `id`value, [INT, DOUBLE])
g.source("data", `id`value`time, [INT, DOUBLE, TIMESTAMP])
  .udfEngine(def(msg) {
    history = orcaObj("history")
    diffTable = table(100:0, `id`diff, [INT, DOUBLE])
    for(i in 0:msg.size()) {
        idVal = msg.id[i]
        valueVal = msg.value[i]
        // 读取历史值
        old = select value from history where id = idVal
        // 写入新值
        newRow = table(idVal as id, valueVal as value)
        history.append!(newRow)
        // 计算差值
        if(old.size() > 0) {
            diffTable.append!(table(idVal as id, (valueVal - old.value[0]) as diff))
        }
    }
    return diffTable
  })
  .sink("comparison")
g.submit()
// 生成模拟数据
mockData = table(1..5 as id, rand(100.0, 5) as value, now() + 1..5 as time)
// 插入数据
appendOrcaStreamTable("orcaCatalog.orca_table.data", mockData)
// 生成id重复的数据
mockData = table(1..5 as id, rand(100.0, 5) as value, now() + 1..5 as time)
// 插入数据
appendOrcaStreamTable("orcaCatalog.orca_table.data", mockData)
// 等待处理并查看结果
sleep(1000)
select * from orcaCatalog.orca_table.comparison
```

| id | diff |
| --- | --- |
| 1 | 35.55946895749296 |
| 2 | -3.4362593906550387 |
| 3 | 36.283468999034596 |
| 4 | 68.97968558337999 |
| 5 | -91.64246928217878 |

**相关函数：**DStream::map, getUdfEngineVariable
