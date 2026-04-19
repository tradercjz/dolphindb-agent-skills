# getUdfEngineVariable

首发版本：3.00.4

## 语法

`getUdfEngineVariable(engine, name)`

## 详情

查询指定 DStream::udfEngine 中指定外部变量的当前值。

## 参数

**engine** 字符串标量，流图中由 DStream::udfEngine 创建的自定义引擎名称。

**name** 字符串标量，外部变量名称，需为创建 DStream::udfEngine 时 *variableNames* 中定义的变量之一。

## 返回值

返回指定变量当前的值，类型和形式取决于变量本身。

## 例子

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

**相关函数：**DStream::udfEngine
