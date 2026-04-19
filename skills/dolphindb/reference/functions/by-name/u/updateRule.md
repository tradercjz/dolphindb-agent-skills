# updateRule

## 语法

`updateRule(engineName, key, rules, [add=false])`

## 详情

更新规则引擎的规则集：

* 如果该规则引擎中不存在这个规则 *key*，则向其增加此规则 *key* 及其 *rules*。
* 如果该规则引擎中已存在指定的规则 *key*，

  + 若 *add* 为 false，则修改其 value 为输入参数 *rules*。
  + 若 *add* 为 true，则向其 value 中追加 *rules*。

## 参数

**engineName** 是一个字符串，表示引擎名。

**key** 是 STRING 或 INT 类型的标量，表示要更新的规则对应的 key 。

**rules** 是一个元代码元组，表示要更新的规则对应的 value。

**add** 是一个布尔标量，表示新规则是追加到已有规则中，还是覆盖已有规则。默认值为 false，表示覆盖。

## 返回值

如果执行成功，返回 true，否则返回 false。

## 例子

```
// 设置规则集，并创建规则引擎
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

// 修改规则前
test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quantity))
test.append!(table(3 as sym, 6 as value, 1 as price, 3 as quantity))

// 将 sym=1 对应的规则修改为 value >=0
updateRule("ruleEngineTest", 1, [ <value >= 0>])
test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quantity))

// 增加 sym=3 对应的规则为 value > 5
updateRule("ruleEngineTest",3,[<value>5>])
test.append!(table(3 as sym, 6 as value, 1 as price, 3 as quantity))
```

此时的输出表 outputTable 内容如下

表 1. outputTable

| sym | value | price | rule |
| --- | --- | --- | --- |
| 1 | 0 | 2 | [false] |
| 3 | 6 | 1 | [false] |
| 1 | 0 | 2 | [true] |
| 3 | 6 | 1 | [true] |

```
// 创建规则引擎
x = [1, 2, NULL]
y = [ [ < value>1 > ], [ < price<2 >, < price>6 > ], [ < value*price>10 > ] ]
ruleSets = dict(x, y)
names = `sym`value`price`quatity
types = [INT, DOUBLE, DOUBLE, DOUBLE]
dummy = table(10:0, names, types)
outputNames = `sym`value`price`rule
outputTypes = [INT, DOUBLE, DOUBLE, BOOL[]]
outputTable = table(10:0, outputNames, outputTypes)
test = createRuleEngine("ruleEngineTest",ruleSets,dummy ,`sym`value`price, outputTable,  "all",`sym)

test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quatity))
test.append!(table(3 as sym, 6 as value, 1 as price, 3 as quatity))
/* outputTable:
1	0	2	[false]
3	6	1	[false]
*/

// 把 sym=1 的规则修改为 value>=0
updateRule("ruleEngineTest", 1, [ <value >= 0>])
test.append!(table(1 as sym, 0 as value, 2 as price, 3 as quatity))
/* outputTable:
1	0	2	[true]
*/

// 增加 sym=3 对应的规则为 value > 5
updateRule("ruleEngineTest",3,[<value>5>])
test.append!(table(3 as sym, 6 as value, 1 as price, 3 as quatity))
/* outputTable:
3	6	1	[true]
*/

// 向 sym=1 对应的规则集中追加 value < 5
updateRule(engineName="ruleEngineTest", key=1, rules=[<value<5>], add=true)
test.append!(table(1 as sym, 12 as value, 1 as price, 3 as quatity))
/* outputTable:
1   12    1     [1,0]
*/
```

**相关信息**

* [createRuleEngine](../c/createRuleEngine.html "createRuleEngine")
* [deleteRule](../d/deleteRule.html "deleteRule")
