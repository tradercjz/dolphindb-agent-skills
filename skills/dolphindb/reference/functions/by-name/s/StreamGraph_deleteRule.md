# StreamGraph::deleteRule

首发版本：3.00.4

## 语法

`StreamGraph::deleteRule(engineName, key)`

## 详情

删除流图中规则引擎的指定规则。

与接口 `deleteRule` 的核心区别在于：

* 通过 `StreamGraph::deleteRule`
  执行的规则变更会被系统自动持久化，确保服务重启后所有已提交的规则修改能被加载并继续生效。
* 通过 `deleteRule` 对规则的变更仅限于内存，修改将在服务重启后失效。

## 参数

**engineName** STRING 类型标量，引擎的全限定名（如 "catalog\_name.orca\_engine.engine\_name"）。

**key** 是 STRING 或 INT 类型的标量，表示要删除的规则对应的 key 。

## 例子

```
createCatalog("demo")
go
use catalog demo

g = createStreamGraph("updateRuleDemo")

// 设置规则集
x = [1, 2, NULL]
y = [ [ < value > 1 > ], [ < price < 2 >, < price > 6 > ], [ < value*price > 10 > ] ]
ruleSets = dict(x, y)

g.source("trades", `sym`value`price`quantity, [INT, DOUBLE, DOUBLE, DOUBLE])
    .ruleEngine(ruleSets=ruleSets, outputColumns=["sym","value","price"], policy="all", ruleSetColumn="sym")
    .setEngineName("myRuleEngine")
    .sink("output")
g.submit()

// 删除规则
g.deleteRule("demo.orca_engine.myRuleEngine",1)
```

相关函数：StreamGraph::updateRule, updateRule
