<!-- Auto-mirrored from upstream `documentation-main/stream/rule_engine.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 规则引擎

规则引擎是 DolphinDB 提供的一个强大的流数据处理工具，其核心思想是
“根据数据自身的特征，动态地选择并应用相应的业务规则进行逻辑判断”。数据流进入引擎后，引擎会依据数据中的某个关键字段（如用户
ID、产品类型、交易渠道等），从预先设定好的规则集中挑选出匹配的规则来检查这条数据。检查结果（是否通过规则）会输出到结果表中，并且可以触发自定义的回调函数进行即时处理。

DolphinDB 规则引擎：

* 毫秒级实时响应速度
* 精准处理大规模时序数据
* 在线动态规则调整

因此适用于需要高灵活性、实时性和业务可配置性的场景，如：

* 物联网：对设备进行监测，例如监测设备温度、湿度；电力监控，例如电压，用电量等。
* 金融：风控场景，例如根据指定规则过滤订单，监控股票成交量，设置超量预警信号等。

规则引擎由函数 `createRuleEngine` 创建。

语法如下：

`createRuleEngine(name, ruleSets, dummyTable, outputColumns, outputTable,
[policy], [ruleSetColumn], [callback], [snapshotDir],
[snapshotIntervalInMsgCount])`

具体可参考：createRuleEngine。

规则引擎可由函数 `updateRule` 和函数 `deleteRule` 动态调整规则，由函数
`getRules` 获取创建的规则信息。

语法如下：

`updateRule(engineName, key, rules, [add=false])`

`deleteRule(engineName, key)`

`getRules([engineName])`

具体可参考：updateRule，deleteRule，getRules。

## 计算规则

规则引擎的计算规则是：首先会通过 `ruleSets` 参数，设定一组规则，字典格式，key 表示规则的键值，为 NULL
时，此条规则为默认规则。`ruleSetColumn` 设置输入数据中命中规则的字段名，当字段值等于
`ruleSet` 中的 key 值时表示命中此规则，然后根据 `policy`
的设置输出引擎的计算结果，此时如果制定了 `callback`
则同时会触发回调处理逻辑。`ruleSetColumn` 若没指定或者没有命中规则，那么使用默认规则处理。

## 应用示例

采样电力设备的电流、电压、和温度，设置规则集进行告警监控。

采集的数据存放到流数据表中，规则引擎通过订阅流数据表来获取实时数据，并进行规则检查，将检查结果输出到另外一个表中。

实现步骤如下：

(1) 定义流表存放采集的数据

```
share streamTable(1000:0,`time`pointId`voltage`current`temprature,[TIMESTAMP,STRING,DOUBLE,DOUBLE,DOUBLE]) as inputTable
```

(2) 定义规则引擎的输出流表以及规则引擎回调函数处理后的流表

```
// 创建流表 保存规则引擎的输出数据
share streamTable(1000:0,`time`pointId`voltage`current`temprature`inputTime`rule,[TIMESTAMP,STRING,DOUBLE,DOUBLE,DOUBLE,NANOTIMESTAMP,BOOL[]]) as outputTable
// 创建流表 保存规则引擎回调函数处理后数据
share streamTable(1000:0,`time`pointId`voltage`current`temprature`inputTime`outputTime`comment,[TIMESTAMP,STRING,DOUBLE,DOUBLE,DOUBLE,NANOTIMESTAMP,NANOTIMESTAMP,STRING]) as resultTable
```

(3) 定义规则集

```
// 定义规则集
n = 10
pointId=`ID + string(1..n)
voltageHigh=round(double(rand(220..230,n))-rand(0.6,n),2)
voltageLow=round(double(rand(45..50,n)) +rand(0.5,n),2)
currentHigh=round(double(rand(40..45,n))-rand(0.6,n),2)
currentLow=round(double(rand(7..9,n))+rand(0.5,n),2)
tempratureHigh=round(double(rand(40..45,n))-rand(0.6,n),2)
tempratureLow=round(double(rand(7..9,n))+rand(0.5,n),2)
pt = table(pointId,voltageHigh,voltageLow,currentHigh,currentLow,tempratureHigh,tempratureLow)

ids = exec pointId from pt
ruleSet = dict(STRING,ANY)
for(i in 0:pt.size()){
    tmp = pt[i]
    keys = tmp.keys()[1:]
    value = tmp.values()[1:]
    a = array(STRING)
    for(j in 0:keys.size()){
        if(keys[j] like "%High"){
            s=strpos(keys[j],"High");
            a.append!(keys[j][0:s]+ ">" + value[j] )
        }else{
            s=strpos(keys[j],"Low");
            a.append!(keys[j][0:s] + "<" + value[j])
        }
    }
    ruleSet[ids[i]] = parseExpr(a)
}
ruleSet[string(NULL)] = [ <voltage > 100000>]
```

(4) 定义回调函数

```
// 定义规则引擎的回调函数
def writeBack(result){
    outputTime = now(true)
    if(result.rule[0]==true){
        s="电压过高"
        insert into resultTable values (result.time,result.pointId,result.voltage,result.current,result.temprature,result.inputTime,outputTime,s)
    }
    if(result.rule[1]==true){
        s="电压过低"
        insert into resultTable values (result.time,result.pointId,result.voltage,result.current,result.temprature,result.inputTime,outputTime,s)
    }
    if(result.rule[2]==true){
        s="电流过高"
        insert into resultTable values (result.time,result.pointId,result.voltage,result.current,result.temprature,result.inputTime,outputTime,s)
    }
    if(result.rule[3]==true){
        s="电流过低"
        insert into resultTable values (result.time,result.pointId,result.voltage,result.current,result.temprature,result.inputTime,outputTime,s)
    }
    if(result.rule[4]==true){
        s="温度过高"
        insert into resultTable values (result.time,result.pointId,result.voltage,result.current,result.temprature,result.inputTime,outputTime,s)
    }
    if(result.rule[5]==true){
        s="温度过低"
        insert into resultTable values (result.time,result.pointId,result.voltage,result.current,result.temprature,result.inputTime,outputTime,s)
    }
}
```

(5) 创建规则引擎

```
// 创建规则引擎
colNames = inputTable.schema().colDefs.name join `inputTime
colTypes = inputTable.schema().colDefs.typeString join `NANOTIMESTAMP
schemaTable = table(1:0,colNames,colTypes)
ruleEngine=createRuleEngine(
    name="ruleEngine",
    ruleSets=ruleSet,
    dummyTable=schemaTable,
    outputColumns=["time","pointId","voltage","current","temprature","inputTime"],
    outputTable=outputTable,
    policy="all",
    ruleSetColumn="pointId",
    callback=writeBack
)
```

(6) 订阅流表写入 10 条模拟数据

```
def handle(msg){
    tmp = select *,now(true) as inputTime from msg
    getStreamEngine("ruleEngine").append!(tmp)
}
// 订阅数据数据流表
subscribeTable(
    tableName="inputTable",
    actionName="RuleEngine",
    handler=handle,
    msgAsTable=true,
    offset=0
)
// 生成10条模拟数据
n =10
t=table(n:n,`time`pointId`voltage`current`temprature,[TIMESTAMP,STRING,DOUBLE,DOUBLE,DOUBLE])
t["time"] = now() +( 1..10) *1000
t["pointId"]=`ID + string(1..n)
t["voltage"]=round(double(rand(45..225,n))+rand(0.5,n) ,2)
t["current"]=round(double(rand(7..43,n))+rand(0.5,n),2)
t["temprature"]=round(double(rand(7..43,n))+rand(0.5,n),2)
// 向流表写入模拟数据
inputTable.append!(t)
```

查看输入数据表

| time | pointId | voltage | current | temprature |
| --- | --- | --- | --- | --- |
| 2025.11.09 21:09:24.883 | ID1 | 100.15 | 37.19 | 22.33 |
| 2025.11.09 21:09:25.883 | ID2 | 196.06 | 11.12 | 18.32 |
| 2025.11.09 21:09:26.883 | ID3 | 81.21 | 35.07 | 30.04 |
| 2025.11.09 21:09:27.883 | ID4 | 181.4 | 40.18 | 40.01 |
| 2025.11.09 21:09:28.883 | ID5 | 217.13 | 42.31 | 27.18 |
| 2025.11.09 21:09:29.883 | ID6 | 182.47 | 24.18 | 43.36 |
| 2025.11.09 21:09:30.883 | ID7 | 124.44 | 12.27 | 43.25 |
| 2025.11.09 21:09:31.883 | ID8 | 198.33 | 39.03 | 8.33 |
| 2025.11.09 21:09:32.883 | ID9 | 78.04 | 16.04 | 31.31 |
| 2025.11.09 21:09:33.883 | ID10 | 194.28 | 18.45 | 35.37 |

查看规则引擎的输出数据表

| time | pointId | voltage | current | temprature | inputTime | rule |
| --- | --- | --- | --- | --- | --- | --- |
| 2025.11.09 21:09:24.883 | ID1 | 100.15 | 37.19 | 22.33 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, false] |
| 2025.11.09 21:09:25.883 | ID2 | 196.06 | 11.12 | 18.32 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, false] |
| 2025.11.09 21:09:26.883 | ID3 | 81.21 | 35.07 | 30.04 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, false] |
| 2025.11.09 21:09:27.883 | ID4 | 181.4 | 40.18 | 40.01 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, false] |
| 2025.11.09 21:09:28.883 | ID5 | 217.13 | 42.31 | 27.18 | 2025.11.09 21:09:23.886 | [false, false, true, false, false, false] |
| 2025.11.09 21:09:29.883 | ID6 | 182.47 | 24.18 | 43.36 | 2025.11.09 21:09:23.886 | [false, false, false, false, true, false] |
| 2025.11.09 21:09:30.883 | ID7 | 124.44 | 12.27 | 43.25 | 2025.11.09 21:09:23.886 | [false, false, false, false, true, false] |
| 2025.11.09 21:09:31.883 | ID8 | 198.33 | 39.03 | 8.33 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, true] |
| 2025.11.09 21:09:32.883 | ID9 | 78.04 | 16.04 | 31.31 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, false] |
| 2025.11.09 21:09:33.883 | ID10 | 194.28 | 18.45 | 35.37 | 2025.11.09 21:09:23.886 | [false, false, false, false, false, false] |

查看规则引擎回调函数处理后的输出表

| time | pointId | voltage | current | temprature | inputTime | outputTime | comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025.11.09 21:09:28.883 | ID5 | 217.13 | 42.31 | 27.18 | 2025.11.09 21:09:23.886 | 2025.11.09 21:09:23.886 | 电流过高 |
| 2025.11.09 21:09:29.883 | ID6 | 182.47 | 24.18 | 43.36 | 2025.11.09 21:09:23.886 | 2025.11.09 21:09:23.887 | 温度过高 |
| 2025.11.09 21:09:30.883 | ID7 | 124.44 | 12.27 | 43.25 | 2025.11.09 21:09:23.886 | 2025.11.09 21:09:23.887 | 温度过高 |
| 2025.11.09 21:09:31.883 | ID8 | 198.33 | 39.03 | 8.33 | 2025.11.09 21:09:23.886 | 2025.11.09 21:09:23.887 | 温度过低 |

结果解释：

设备 'ID5' 的规则集为：

```
(< voltage > 221.86 >,< voltage < 45.16 >,< current > 39.96 >,< current < 7.47 >,< temprature > 44.43 >,< temprature < 8.03 >)
```

输入数据命中规则集中的 current > 39.96，经回调函数处理，输出“电流过高”；

设备 'ID6' 的规则集为：

```
(< voltage > 221.89 >,< voltage < 49.05 >,< current > 43.42 >,< current < 7.06 >,< temprature > 41.98 >,< temprature < 7.418>)
```

输入数据命中规则集中的 temprature > 41.98 ，经回调函数处理，输出“温度过高”；

设备 'ID7' 的规则集为：

```
(< voltage > 226.61 >,< voltage < 48.40 >,< current > 40.77 >,< current < 9.19 >,< temprature > 41.95 >,< temprature < 8.14 >)
```

输入数据命中规则集中的 < temprature > 41.95，经回调函数处理，输出“温度过高”；

设备 'ID8' 的规则集为：

```
(< voltage > 228.97 >,< voltage < 46.137 >,< current > 42.607 >,< current < 7.29 >,< temprature > 44.40 >,< temprature < 9.27 >)
```

输入数据命中规则集中的 temprature < 9.27，经回调函数处理，输出“温度过高”；

(7) 动态调整规则示例

```
//修改规则
newRules = [ < voltage > 223.41 >,< voltage < 49.25 >,< current > 36.84 >,< current < 8.4 >,< temprature > 44.60 >,< temprature < 7.43 >]
updateRule("ruleEngine","ID1",newRules)
//插入一条模拟数据
insert into inputTable values (now(), 'ID1',100.15,37.19,22.33)
```

current= 37.19，之前的规则未触发报警，现在命中更新后的规则 current > 36.84，输出表新增记录：

| time | pointId | voltage | current | temprature | inputTime | outputTime | comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025.11.09 21:43:55.505 | ID1 | 100.15 | 37.19 | 22.33 | 2025.11.09 21:43:55.505 | 2025.11.09 21:43:55.506 | 电流过高 |
