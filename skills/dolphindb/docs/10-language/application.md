<!-- Auto-mirrored from upstream `documentation-main/progr/application.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 应用场景

OOP 在特定场景中提供了独特的优势，特别是以下几个场景：

* **开发响应式状态引擎算子**：OOP 范式能够简化算子的开发流程，降低成本。传统方法中，开发者需使用
  `genericIterateState` 等复杂的高阶函数，或 C++ 插件来编写算子。而 OOP
  的引入，将使算子代码更加直观易懂。具体可查看[示例 1](#topic_tvn_tz2_ccc)。
* **在复杂事件处理（CEP）中使用 OOP 表示事件：**采用 OOP
  来构建事件类型，可以替代复杂字典（dict）结构的构造方式。这种方法不仅使得事件的定义和处理逻辑更加直观，而且与 Apama 的 EPL
  语言相似，进一步提高了开发者编写 CEP 应用程序的效率。具体可查看[示例 2](#topic_pdj_zz2_ccc)。

## 示例1：响应式状态引擎算子

响应式状态引擎能实现流批一体的带有状态的高频因子计算。该引擎采用历史数据批处理中定义的表达式或函数作为输入，执行流式计算，并保证其结果与批处理结果的完全一致。本例介绍如何通过
OOP 实现高频算子。

**用法**

`class(...).append(...)` ，其中第一个 `...` 传入 class
的构造参数，第二个 `...` 传入 `append` 函数的参数。

用户需要在 class 中实现 `append` 函数，且 `append` 需要有返回值。

`append`
的返回值类型可以为：`CHAR`、`BOOL`、`SHORT`、`INT`、`LONG`、`FLOAT`、`DOUBLE`、`DECIMAL32`、`DECIMAL64`、`DECIMAL128`.

```
class MyCumSum {
  sum :: DOUBLE

  def MyCumSum() {
    sum = 0.0
  }

  def append(value) {
    sum = sum + value
    return sum
  }
}

metrics = [<MyCumSum().append(val)>]

inputTable = table(1:0, `sym`val, [SYMBOL, DOUBLE])
result = table(1000:0, `sym`res, [SYMBOL, DOUBLE])
rse = createReactiveStateEngine(
          name="reactiveDemo",
          metrics =metrics,
          dummyTable=inputTable,
          outputTable=result,
          keyColumn="sym")
rse.append!(table(rand(`A`B`C, 100) as sym, rand(100.0, 100) as val))
select TOP 10 * from result
```

返回：

| sym | res |
| --- | --- |
| B | 23.136844485998154 |
| C | 97.25657706148922 |
| C | 119.75046650040895 |
| B | 28.15541410818696 |
| C | 208.6210786132142 |
| A | 17.531023011542857 |
| B | 127.66627178061754 |
| C | 286.6357475752011 |
| A | 45.87050362024456 |
| C | 343.2471259729937 |

class 的构造函数可以有参数，需要在 metrics
中给出，且只能为常数，如下：

```
//首先清理环境，删除已注册的引擎
dropStreamEngine("reactiveDemo")

class MyCumSum {
  sum :: DOUBLE
  def MyCumSum(initialValue) {
    sum = initialValue
  }
  def append(value) {
    sum = sum + value
    return sum
  }
}
metrics= [<MyCumSum(0.0).append(val)>]
inputTable = table(1:0, `sym`val, [SYMBOL, DOUBLE])
result = table(1000:0, `sym`res, [SYMBOL, DOUBLE])
rse = createReactiveStateEngine(
          name="reactiveDemo",
          metrics =metrics,
          dummyTable=inputTable,
          outputTable=result,
          keyColumn="sym")
rse.append!(table(rand(`A`B`C, 100) as sym, rand(100.0, 100) as val))
select TOP 10 * from result
```

返回：

| sym | res |
| --- | --- |
| C | 79.73966575227678 |
| A | 50.2432547044009 |
| C | 108.56282587628812 |
| A | 137.95565224718302 |
| C | 179.22195203136653 |
| B | 41.10089084133506 |
| C | 253.5685545997694 |
| A | 173.4938955400139 |
| C | 262.32025355566293 |
| B | 105.45554195996374 |

`append` 的参数可以为常量、数值，或者是 lambda
表达式：

```
class MyCumSum {
  sum :: DOUBLE
  def MyCumSum() {
    g = def (): 0
    sum = g()
  }
  def append(value, f) {
    sum = f(sum, value)
    return sum
  }
}
metrics = [<MyCumSum().append(val, def (a, b): a + b)>]
inputTable = table(1:0, `sym`val, [SYMBOL, DOUBLE])
result = table(1000:0, `sym`res, [SYMBOL, DOUBLE])
result2 = table(1000:0, `sym`res, [SYMBOL, DOUBLE])
try {
    dropStreamEngine("reactiveDemo")
    dropStreamEngine("reactiveDemo2")
} catch (exp) {
}
rse = createReactiveStateEngine(
          name="reactiveDemo",
          metrics =metrics,
          dummyTable=inputTable,
          outputTable=result,
          keyColumn="sym")
rse2 = createReactiveStateEngine(
          name="reactiveDemo2",
          metrics =[<cumsum(val)>],
          dummyTable=inputTable,
          outputTable=result2,
          keyColumn="sym")
t = table(rand(`A`B`C, 100) as sym, rand(100.0, 100) as val)
rse.append!(t)
rse2.append!(t)
t1 = select TOP 10 * from result ORDER BY sym
t2 = select TOP 10 * from result2 ORDER BY sym
```

t1 表：

| sym | res |
| --- | --- |
| A | 73.74901322182268 |
| A | 151.10119895543903 |
| A | 234.97340406756848 |
| A | 249.01866489090025 |
| A | 263.8336496660486 |
| A | 277.98473422881216 |
| A | 321.98982320260257 |
| A | 394.077792391181 |
| A | 442.3658183310181 |
| A | 538.974173902534 |

t2 表：

| sym | res |
| --- | --- |
| A | 73.74901322182268 |
| A | 151.10119895543903 |
| A | 234.97340406756848 |
| A | 249.01866489090025 |
| A | 263.8336496660486 |
| A | 277.98473422881216 |
| A | 321.98982320260257 |
| A | 394.077792391181 |
| A | 442.3658183310181 |
| A | 538.974173902534 |

## 示例2：CEP 应用

```
class orders{
    trader :: STRING
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    eventTime :: TIMESTAMP
    def orders(t, m, c, p, q){
        trader = t
        market = m
        code = c
        price = p
        qty = q
        eventTime = now()
    }
}
class traderOnline{
    trader :: STRING
    eventTime :: TIMESTAMP
    def traderOnline(t){
        trader = t
        eventTime = now()
    }
}
class mainMonitor:CEPMonitor{
    ordersTable :: ANY
    isBusy :: BOOL
    def mainMonitor(busyFlag){
        ordersTable = array(ANY, 0)
        isBusy = busyFlag
    }
    def updateOrders(event)
    def unOnload(){
        undef('traderDV', SHARED)
    }
    def online(online){
        getDataViewEngine(,'traderDV').append!(table(online.trader as trader, 0 as orderCount, 0 as tradeCount, 0.0 as price, false as busy, date(online.eventTime) as orderDate))
    }
    def onload(){
        addEventListener(online,'traderOnline',,'all')
        addEventListener(updateOrders, 'orders',,'all')
        traderDV = streamTable(array(STRING, 0) as trader,  array(INT, 0) as orderCount, array(INT, 0) as tradeCount, array(DOUBLE, 0) as price, array(BOOL, 0) as busy, array(DATE, 0) as orderDate, array(TIMESTAMP, 0) as updateTime)
        share(traderDV, 'traderDV')
        createDataViewEngine('traderDV', objByName('traderDV'), `trader, `updateTime, true)
    }
    def updateOrders(event) {
        ordersTable.append!([event.trader, event.market, event.code, event.price, event.qty])
        updateDataViewItems('traderDV', event.trader, ['orderCount', 'busy'], [ordersTable.size(), false])
    }
}
dummy = table(array(TIMESTAMP, 0) as eventTime, array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
engineCep = createCEPEngine('cep1', <mainMonitor(true)>, dummy, [orders, traderOnline], 1, 'eventTime', 10000)
traderOnline = traderOnline('t1')
appendEvent(engineCep, traderOnline)
traderOnline = traderOnline('t2')
appendEvent(engineCep, traderOnline)
traderOnline = traderOnline('t3')
appendEvent(engineCep, traderOnline)
orders1 = orders('t1', 'sz', 's001', 11.0, 10)
appendEvent(engineCep, orders1)
objByName(`traderDV)
getCEPEngineStat(`cep1)

/* output:
streamEngineStat->{
}
subEngineStat->
subEngineName eventsOnInp...monitorNumber listeners timers eventsRouted eventsSent eventsReceived...
------------- ------------- ---------------- --------- ------ ------------ ---------- -------------
cep1          4             1             2         0      0            0          4             ...

engineStat->{
eventsOnOutputQueue->0
lastErrorTimestamp->
numOfSubEngine->1
lastErrorMessage->
eventsEmitted->0
eventsReceived->4
name->cep1
queueDepth->10000
user->guest
useSystemTime->true
status->OK
}
eventSchema->
eventType    eventField                fieldType                 fieldTypeId        fieldFormId
------------ ------------------------- ---------------------------- --------------------- -------------
orders       trader,market,code,pric...STRING,STRING,STRING,DO...[18,18,18,16,4,12] [0,0,0,0,0,0]
traderOnline trader,eventTime          STRING,TIMESTAMP          [18,12]            [0,0]

dataViewEngines->
name     user  status lastErrorMes...lastErrorTim...keyColumns outputTableNameuseSystemTime throttle ...
-------- ----- ------ -------------- ----------------- ------------- -------------- ------------- --------
traderDV guest OK                                   trader     traderDV       true                   ...

*/
```
