# StreamGraph::updateRule

首发版本：3.00.4

## 语法

`StreamGraph::updateRule(engineName, key, rules)`

## 详情

更新流图中规则引擎的规则集：

* 如果此规则引擎中存在指定的规则 *key*，则修改其 value 为输入参数 *rules*。
* 如果此规则引擎中不存在这个规则 *key*，则向其增加此规则 *key* 及其 *rules*。

与接口 `updateRule` 的核心区别在于：

* 通过 `StreamGraph::updateRule`
  执行的规则变更会被系统自动持久化，确保服务重启后所有已提交的规则修改能被加载并继续生效。
* 通过 `updateRule` 对规则的变更仅限于内存，修改将在服务重启后失效。

## 参数

**engineName** STRING 类型标量，引擎的全限定名（如 "catalog\_name.orca\_engine.engine\_name"）。

**key** 是 STRING 或 INT 类型的标量，表示要更新的规则对应的 key 。

**rules** 是一个元代码元组，表示要更新的规则对应的 value。

## 例子

```
createCatalog("demo")
go
use catalog demo

// 设置规则集
x = [1, 2, NULL]
y = [ [ < value > 1 > ], [ < price < 2 >, < price > 6 > ], [ < value*price > 10 > ] ]
ruleSets = dict(x, y)

// 创建并提交流图
g = createStreamGraph("updateRuleDemo")
g.source("trades", `sym`value`price`quantity, [INT, DOUBLE, DOUBLE, DOUBLE])
    .ruleEngine(ruleSets=ruleSets, outputColumns=["sym","value","price"], policy="all", ruleSetColumn="sym")
    .setEngineName("myRuleEngine")
    .sink("output")
g.submit()

// 修改规则
g.updateRule("demo.orca_engine.myRuleEngine", 1, [<value>=0>])
```

相关函数：StreamGraph::deleteRule, updateRule
