<!-- Auto-mirrored from upstream `documentation-main/stream/cep_monitoring.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 实时监控 CEP 引擎状态及数据

CEP 引擎内部计算为事件触发，随着事件不断地注入引擎，引擎内部会产生许多不断更新的中间变量（监控值）。用户通常希望监控到这些变量的最新值及其变化趋势。因此，DolphinDB
提供了 DataView 引擎，允许 CEP 引擎在运行过程中将监控值写入 DataView 引擎。DataView
引擎负责维护每个监控值的最新快照，并将数据输出到目标表（通常为流表），供其它程序订阅。DataView 引擎中维护的数据称为 DataView。在 CEP 系统中，可以创建多个
DataView
引擎，并在创建时指定需要维护的监控值名称。请注意，数据视图页面仅展示监控值的最新快照，不支持查看历史快照。若需要查看监控值的历史快照和趋势变化图，请使用数据面板（Dashboard）。

## 创建 DataView 引擎

通过以下接口创建一个 DataView 引擎，返回一个键值表。该表记录了每个键值对应的最新记录。

**语法**

`createDataViewEngine(name, outputTable, keyColumns, timeColumn,
[useSystemTime=true], [throttle])`

**参数**

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

## 获取最新数据

通过以下两种方式，可以获取 DataView 引擎中的数据：

* 在 CEP 引擎内部创建的 DataView，通过 `getDataViewEngine` 获取指定 DataView
  引擎的数据。
* 在 CEP 引擎外部创建的 DataView，通过 `getStreamEngine` 获取指定 DataView
  引擎的数据。

**语法**

`getDataViewEngine([CEPEngine], dataViewEngineName)`

**参数**

**CEPEngine** CEP 引擎的句柄。

**dataViewEngineName** DataView 引擎的名称。

下例未指定 CEP 引擎，则在当前 CEP 引擎中获取名为 dv1 的 DataView 引擎中的数据。

```
dvEngine= getDataViewEngine(,"dv1"")
select * from dvEngine
```

**注意：**自 3.00.3 版本起，若需要获取当前 CEP 引擎的 DataView
引擎中的数据，可仅传入其名称，无需指定第一个参数。因此，上述代码可简写为：`dvEngine=
getDataViewEngine("dv1"")`。

下例中获取 cep1 中名为 dv1 的 DataView 引擎中的数据。

```
dvEngine= getDataViewEngine(`cep1,`dv1)
select * from dvEngine
```

通过 `getStreamEngine` 获取在 CEP 引擎外部定义的 DataView 引擎中的数据。

```
select * from getStreamEngine(dataViewEngineName)
```

## 向 DataView 引擎写入数据

`createDataViewEngine` 函数返回一个表，因此支持通过 `append!`,
`tableInsert`, `insert into` 等方法向 DataView
引擎写入数据。在向 DataView 引擎写入数据前，需要先通过
`getDataViewEngine(,dataViewEngineName)` 获取 DataView 引擎的句柄。

## 更新数据视图指定键值的数据

通过以下接口更新 DataView 引擎中指定键值对应的指定字段的值。若 *keys* 指定的键值列（key）不存在，则更新时会报错 。

`updateDataViewItems(engine, keys, valueNames, newValues)`

**参数**

**engine** DataView 引擎句柄或引擎名。

**keys** 标量、向量或 tuple，表示需要更新的键值， 如果是复合键值，则需要传入一个 tuple，其中每个元素表示组成键值的列，且顺序需与引擎中
*keyedColumns* 的指定顺序保持一致。

**valueNames** 字符串标量或向量，需要更新的字段的名称，需要与 DataView 引擎中 *outputTable*
指定的列名匹配。

**newValues** 标量、向量或 tuple，表示需要更新的字段对应的值。指定方式同 *keys*。

该函数可在 CEP 引擎内部或外部调用。如果在 CEP 引擎内部调用此函数，系统将优先在 CEP 引擎中查找句柄为 *engine* 的 DataView
引擎；若未找到，则会在 CEP 引擎外部进行查找。如果在 CEP 引擎外部调用此函数，系统只会在 CEP 引擎外部进行查找。

## 删除数据视图指定键值的数据

通过以下接口删除 DataView 引擎中指定键值的数据。若 *keys* 指定的键值列（key）不存在，则删除时会报错 。

`deleteDataViewItems(engine, keys)`

**参数说明：**

**engine** DataView 引擎句柄或引擎名。

**keys** 需要更新的键值， 如果是复合键值，则需要传入一个 tuple，其中每个元素表示组成键值的列，且顺序需与引擎中
*keyedColumns* 的指定顺序保持一致。

该函数可在 CEP 引擎内部或外部调用。如果在 CEP 引擎内部调用此函数，系统将优先在 CEP 引擎中查找句柄为 *engine* 的 DataView
引擎；若未找到，则会在 CEP 引擎外部进行查找。如果在 CEP 引擎外部调用此函数，系统只会在 CEP 引擎外部进行查找。

## 删除 DataView 引擎

通过以下接口删除当前 CEP 引擎中指定的 DataView 引擎。

**语法**

`dropDataViewEngine(name)`

**参数**

**name** 字符串，表示 DataView 引擎的名称。

**示例**

```
class MainMonitor:CEPMonitor {
    def MainMonitor(){
    }
    // 删除引擎时自动调用，删除共享流表
    def onunload(){
      undef('orderDV', SHARED)
      dropDataViewEngine('orderDV')
    }
	def checkOrders(newOrder)
    // 创建 DataViewEngine, 指定主键为 code 列，统计每个股票的最新的委托信息
    def onload(){
        addEventListener(checkOrders,'Orders',,'all')
        orderDV = streamTable(array(STRING, 0) as market, array(STRING, 0) as code, array(DOUBLE, 0) as price, array(INT, 0) as qty, array(TIMESTAMP, 0) as updateTime)
        share(orderDV,'orderDV')
        createDataViewEngine('orderDV', objByName('orderDV'), `code, `updateTime)
    }
    // 更新每个股票的最新的委托信息
    def checkOrders(newOrder){
		getDataViewEngine('orderDV').append!(table(newOrder.market as market, newOrder.code as code, newOrder.price as price, newOrder.qty as qty))
    }
}
```

## 示例

```
class MainMonitor:CEPMonitor {
    def MainMonitor(){
    }
    // 删除引擎时自动调用，删除共享流表
    def onunload(){
      undef('orderDV', SHARED)
      dropDataViewEngine('orderDV')
    }
	def checkOrders(newOrder)
    // 创建 DataViewEngine, 指定主键为 code 列，统计每个股票的最新的委托信息
    def onload(){
        addEventListener(checkOrders,'Orders',,'all')
        orderDV = streamTable(array(STRING, 0) as market, array(STRING, 0) as code, array(DOUBLE, 0) as price, array(INT, 0) as qty, array(TIMESTAMP, 0) as updateTime)
        share(orderDV,'orderDV')
        createDataViewEngine('orderDV', objByName('orderDV'), `code, `updateTime)
    }
    // 更新每个股票的最新的委托信息
    def checkOrders(newOrder){
		getDataViewEngine('orderDV').append!(table(newOrder.market as market, newOrder.code as code, newOrder.price as price, newOrder.qty as qty))
    }
}
```
