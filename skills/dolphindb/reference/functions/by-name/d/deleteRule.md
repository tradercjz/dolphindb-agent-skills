# deleteRule

## 语法

`deleteRule(engineName, key)`

## 详情

如果该引擎规则中存在指定的规则 *key* 则删除，删除成功返回 true；否则，返回 false。

注：

默认规则不可删除。

## 参数

**engineName** 是一个字符串，表示引擎名。

**key** 是 STRING 或 INT 类型的标量，表示要删除的规则对应的 key 。

## 返回值

布尔值。

## 例子

```
x = [1, 2, NULL]
y = [ [ < value>1 > ], [ < price<2 >, < price>6 > ], [ < value*price>10 > ] ]
ruleSets = dict(x, y)
names = `sym`value`price`quantity
types = [INT, DOUBLE, DOUBLE, DOUBLE]
dummy = table(10:0, names, types)
outputNames = `sym`value`price`rule
outputTypes = [INT, DOUBLE, DOUBLE, BOOL[]]
outputTable = table(10:0, outputNames, outputTypes)
test = createRuleEngine(name="ruleEngineTest", ruleSets=ruleSets, dummyTable=dummy, outputColumns=["sym","value","price"], outputTable=outputTable, policy="all", ruleSetColumn="sym")

// 删除规则前
test.append!(table(1 as sym, 6 as value, 1 as price, 8 as quantity))

// 删除 sym=1 的规则，sym=1会使用默认规则
deleteRule("ruleEngineTest",1)
test.append!(table(1 as sym, 6 as value, 1 as price, 8 as quantity))
```

此时的输出表 outputTable 内容如下

| sym | value | price | rule |
| --- | --- | --- | --- |
| 1 | 6 | 1 | [true] |
| 1 | 6 | 1 | [false] |

**相关信息**

* [updateRule](../u/updateRule.html "updateRule")
* [createRuleEngine](../c/createRuleEngine.html "createRuleEngine")
