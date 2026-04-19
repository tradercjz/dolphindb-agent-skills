# DStream::ruleEngine

首发版本：3.00.3

## 语法

`DStream::ruleEngine(ruleSets, outputColumns, [policy], [ruleSetColumn],
[callback])`

## 详情

创建流计算规则引擎。参考：createRuleEngine。

## 参数

**ruleSets** 是一个字典，表示规则集。字典的 key 是 STRING 或 INT 类型，value
是一个包含元代码的元组。如果 key 为NULL，表示此条为默认规则。如果未指定
*ruleSetColumn*，或数据未命中任何规则，将采用默认规则检查数据。一个规则集必须包含默认规则。

**outputColumns** 一个 STRING 类型向量，表示输入表中需要保留到输出表的列。

**policy** 是一个字符串标量，表示规则检查策略。可取以下值：

* "shortcut" 是默认值，代表短路逻辑。当检查到任一规则不符合（计算结果为 false）时，规则引擎立即停止检查并返回该规则的
  index（从 0 开始）；如果所有规则都符合，则返回 NULL。比如数据匹配到如下规则，当 age 字段的值小于 18 时，计算结果为
  false，规则引擎停止检查并返回 0 （规则的 index）到输出表中。

  ```
  (< age > 18 >,< income > 5000 >,< debtRatio < 0.5 >)
  ```
* "all" 代表检查全部规则，返回规则集的检查结果，布尔类型。比如数据匹配到如下规则，当
  `voltage=220`、`current=37.11`、`temperature=39`，检查结果为
  `[false, false, false]`。

  ```
  (< voltage > 221.86 >,< current > 39.96 >,< temperature > 44.43 >)
  ```

**ruleSetColumn** 是一个 STRING
类型标量，为输入表的某一列名，如果没有定义或者输入数据中的该列数据没有命中任何一个规则集，则使用默认规则，即规则集中 key 为 NULL 时所指示的规则。

**callback**
是一个函数，其参数为一个元组，是引擎输出的一行。若设置此参数，引擎每处理一行，在将引擎处理结果输出到输出表的同时，会将该结果作为入参调用此函数。

## 返回值

返回一个 DStream 对象。

## 例子

```
if (!existsCatalog("orca")) {
	createCatalog("orca")
}
go
use catalog orca

// 如已存在流图，则先销毁该流图
// dropStreamGraph('engine')
g = createStreamGraph('engine')

// 设置规则集
x = [1, 2, NULL]
y = [ [ < value > 1 > ], [ < price < 2 >, < price > 6 > ], [ < value*price > 10 > ] ]
ruleSets = dict(x, y)

// 创建分布式表，用于回调函数写入数据
if(existsDatabase("dfs://temp")){
    dropDatabase("dfs://temp")
}
db = database("dfs://temp", VALUE, 1..3)
t1 = table(1:0, `sym`value`price, [INT,DOUBLE,DOUBLE])
pt = db.createPartitionedTable(t1,`pt,`sym)

// 创建回调函数，根据检测结果，将数据写入分布式表
def writeBack(result){
    if(result.rule[0]==false){
        temp = select sym,value,price from result
        loadTable("dfs://temp",`pt).append!(temp)
    }
}

g.source("trades", `sym`value`price`quantity, [INT, DOUBLE, DOUBLE, DOUBLE])
.ruleEngine(ruleSets=ruleSets, outputColumns=["sym","value","price"], policy="all", ruleSetColumn="sym", callback=writeBack)
.sink("output")
g.submit()
go

tmp=table(1 1 as sym, 0 2 as value, 2 2 as price, 3 3 as quantity)
appendOrcaStreamTable("trades", tmp)

select * from orca_table.output
```

| sym | value | price | rule |
| --- | --- | --- | --- |
| 1 | 0 | 2 | [false] |
| 1 | 2 | 2 | [true] |
