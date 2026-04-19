# DStream::sharedDict

## 语法

`DStream::sharedDict(name, keyObj, valueObj, [ordered=false])`

或

`DStream::sharedDict(name, keyType, valueType, [ordered=false])`

## 详情

在 Orca 中创建一个共享字典，仅支持在 `DStream::udfEngine` 中使用。关于字典的说明参见 dict。

## 参数

**name** 字符串标量，表示共享字典的名称。

对于第一种情形，**keyObj** 是表示键的向量，**valueObj** 是表示值的向量。

对于第二种情形，**keyType** 是字典键的数据类型，**valueType**
是字典值的数据类型。系统支持以下键的数据类型：Literal、Integral（COMPRESS 除外）、Floating 和 Temporal。字典中的值不支持
COMPLEX，POINT 和 Decimal 类别。

**ordered** 一个布尔值，默认为 false，表示创建一个无序字典。当 *ordered* = true
时，创建一个有序字典。无序字典在输出或进行遍历时，其键值对不保留输入时的顺序；有序字典在输出或进行遍历时，键值对的顺序与输入顺序保持一致。

## 返回值

一个字典。

## 例子

本例结合 `DStream::sharedDict` 与
`DStream::udfEngine`，实现计数并触发条件告警的功能。具体实现为，使用
`DStream::sharedDict`
统计每个键（key）的出现次数。当某个键的累计计数超过预设阈值时，自定义函数将向下游输出一条告警消息。

```
if(existsCatalog("orcaCatalog")) dropCatalog("orcaCatalog")
createCatalog("orcaCatalog")
go
use catalog orcaCatalog
// 创建流图
g = createStreamGraph("counter")
g.sharedDict("counts", STRING, LONG)
g.source("items", ["key"], [STRING])
  .udfEngine(def(msg) {
    counts = orcaObj("counts")
    triggered = table(100:0, `key`count, [STRING, LONG])
    for(i in 0:msg.size()) {
        keyVal = msg.key[i]
        // 读取当前计数
        current = 0
        if (keyVal in counts) {
            current = counts[keyVal]
        }
        newCount = current + 1
        // 更新计数
        counts[keyVal] = newCount
        // 判断条件
        if(newCount >= 3) {
            triggered.append!(table(keyVal as key, newCount as count))
        }
    }
    return triggered
  })
  .sink("alerts")
g.submit()
go
// 生成模拟数据
keys = ["A", "B", "A", "C", "B", "A", "B", "B", "C", "C"]
mockData1 = table(take(keys[0:3], 3) as key)
mockData2 = table(take(keys[3:6], 3) as key)
mockData3 = table(take(keys[6:10], 4) as key)
// 插入数据
appendOrcaStreamTable("orcaCatalog.orca_table.items", mockData1)
appendOrcaStreamTable("orcaCatalog.orca_table.items", mockData2)
appendOrcaStreamTable("orcaCatalog.orca_table.items", mockData3)
// 等待处理并查看结果
sleep(1000)
select * from orcaCatalog.orca_table.alerts;
```

| key | count |
| --- | --- |
| A | 3 |
| B | 3 |
| B | 4 |
| C | 3 |
