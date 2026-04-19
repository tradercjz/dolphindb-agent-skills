# createDataViewEngine

## 语法

`createDataViewEngine(name, outputTable, keyColumns, timeColumn,
[useSystemTime=true], [throttle],[includeOperationType=false])`

## 详情

该函数用于在 CEP 中创建一个 DataView 引擎。该引擎负责维护指定监控值的最新快照，并将其输出到目标表（通常为流表），供其他程序订阅。通过该函数，用户可以在
CEP 引擎运行过程中实时监控关键变量的变化趋势。

## 参数

**name** 字符串，表示 DataView 引擎的名称，可包含字母，数字和下划线，但必须以字母开头。

**outputTable** 一个表，可以是内存表或分布式表，用于存储 DataView 引擎中的数据。如果需要前端展示实时数据，或绘制数据变化趋势图，则
*outputTable* 必须指定为一个流表。

**keyColumns** 字符串标量或向量，为 *outputTable*
中的列名。引擎将使用指定列中数据的唯一（组合）值作为引擎的键值，对于每个键值，引擎都只保留 1 条数据。

**timeColumn** 一个字符串，表示指定 *outputTable* 中时间列的名称。

**useSystemTime** 布尔值，表示是否使用数据注入引擎时的系统时间作为输出的时间列。

* 若 *useSystemTime*=true，输出表中的时间列为系统时间，此时数据中不能包含时间列。
* 若 *useSystemTime*=false，输出表中的时间列为数据中的时间，此时需要写入的数据中包含时间。

**throttle** DURATION 类型，用于设置 DataView 引擎输出数据到 *outputTable* 的时间间隔。

**includeOperationType** 可选参数，布尔值，设置是否在输出结果中包含每条数据记录的变更类型。默认值为
false。当设置为 true 时，输出表第一列必须为 CHAR 类型，用于标识对应记录的操作类型：

* 'A'：新增记录
* 'U'：更新记录
* 'D'：删除记录

注：

默认情况下，数据被删除后，引擎不会输出对应记录；开启 *includeOperationType* 后，引擎会额外输出被删除的记录（操作类型为
'D'）。因此，开启或关闭 *includeOperationType* 时，输出的记录行数可能不同。

## 返回值

一个键值表。该表记录了每个键值对应的最新记录。

## 例子

下例演示如何使用 CEP（复杂事件处理）引擎来实时维护股票委托订单的最新状态，包含订单的新增和删除操作。

```
class Orders{
    market :: STRING
    code :: STRING
    price :: DOUBLE
    qty :: INT
    def Orders(m,c,p,q){
        market = m
        code = c
        price = p
        qty = q
    }
}
class DeleteOrder{

    code :: STRING

    def DeleteOrder(c){
        code = c
    }
}
// 定义监视器
class MainMonitor:CEPMonitor {
    def MainMonitor(){
    }
    // 删除引擎时自动调用：删除共享流表
    def onunload(){ undef('orderDV', SHARED) }
    def checkOrders(newOrder)
    def deleteOrder(order)
    // 创建 Data View Engine, 指定主键为 code 列，统计每个股票的最新的委托信息
    def onload(){
        addEventListener(checkOrders,'Orders',,'all')
        orderDV = streamTable(array(CHAR, 0) as type, array(STRING, 0) as market, array(STRING, 0) as code, array(DOUBLE, 0) as price, array(INT, 0) as qty, array(TIMESTAMP, 0) as updateTime)
        share(orderDV,'orderDV')
        createDataViewEngine('orderDV', objByName('orderDV'), `code, `updateTime, true, ,true)
        addEventListener(deleteOrder,'DeleteOrder',,'all')
    }
    // 更新每个股票的最新的委托信息
    def checkOrders(newOrder){
        getDataViewEngine('orderDV').append!(table(newOrder.market as market, newOrder.code as code, newOrder.price as price, newOrder.qty as qty))
    }
    def deleteOrder(order){
        deleteDataViewItems('orderDV',order.code )
    }
}
// 创建 CEP 引擎
dummy = table(array(STRING, 0) as eventType, array(BLOB, 0) as blobs)
try{dropStreamEngine('cep1')}catch(ex){print(ex)}
engine = createCEPEngine(name='cep1', monitors=<MainMonitor()>, dummyTable=dummy, eventSchema=[Orders,DeleteOrder])
engine.appendEvent(Orders("m1", "c1", 10.0, 100))
engine.appendEvent(Orders("m1", "c2", 10.0, 100))
engine.appendEvent(Orders("m1", "c2", 9.5, 100))
engine.appendEvent(DeleteOrder("c2"))

// 查看 orderDV 中的订单数据
select * from orderDV
```

| type | market | code | price | qty | updateTime |
| --- | --- | --- | --- | --- | --- |
| A | m1 | c1 | 10 | 100 | 2026.02.01 14:53:12.928 |
| A | m1 | c2 | 10 | 100 | 2026.02.01 14:53:12.928 |
| U | m1 | c2 | 9.5 | 100 | 2026.02.01 14:53:12.928 |
| D | m1 | c2 | 9.5 | 100 | 2026.02.01 14:53:12.928 |

**相关函数**：createCEPEngine, deleteDataViewItems, dropDataViewEngine, getDataViewEngine
