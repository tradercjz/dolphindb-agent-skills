<!-- Auto-mirrored from upstream `documentation-main/stream/cep_monitor_defining.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 定义 Monitor

在 CEP 引擎中可以定义多个 Monitor，每个 Monitor 执行特定任务。Monitor 之间通过发送和接收事件进行通信。Monitor 实例中可以通过 spwan
方式从已有的监视器中生成新的监视器。通常情况下，生成的 Monitor 实例都监听相同的事件，但每个监视器实例都可以监听具有不同属性值的事件。自 3.00.3
版本起，monitor 类需显式继承 CEPMonitor 类。

## 简单的 Monitor 实例

一个简单的 Monitor 定义如下：

* 首先，定义事件，它是监视器需要监视的事件。例如上文中的 orders 事件。
* 其次，定义一个全局的成员属性，用于保存 orders 的事件。该监视器中的所有操作都可以访问该成员。
* 定义事件监听器，监听所有 orders 事件。在监听器中匹配模式和回调函数。
* 定义 `onload` 方法。它是必须的，在引擎创建时会执行该方法，启动 Monitor 的监听动作。

本节创建一个简单的 Monitor 实例，对上文中 orders 事件进行监视：

```
class mainMonitor:CEPMonitor{
    ordersTable :: ANY  // 定义成员变量 ordersTable，不限制数据类型和形式
    isBusy :: BOOL
    def mainMonitor(busyFlag){
        ordersTable = array(ANY, 0)  // 这里确定 ordersTable 为一个元组
        isBusy = busyFlag
    }

    //声明更新事件的方法
    def updateOrders(event) {
        ordersTable.append!([event.trader, event.market, event.code, event.price, event.qty])
    }

    //在 CEP 引擎创建时，会执行 Monitor 的 onload 操作。这里通过 onload 方法增加事件监听器，一旦匹配到 orders 事件，便
    执行 updateOrders 操作。
    def onload(){
        addEventListener(updateOrders, 'orders',,'all')
    }
}
```

### 启动 Monitor

通过 `createCEPEngine` 将 Monitor 注入 CEP 引擎。引擎创建时会执行 Monitor 中声明的
`onload` 方法，启动 Monitor 的监听动作。

### 生成 Monitor 实例

**语法**

`spawnMonitor(name, handler, arguments...)`

**参数**

**name** 生成 monitor
实例的名称。不可与已存在的实例重名。

**handler** 生成的 Monitor 实例的方法。在生成新的实例后，将调用这个方法。

**arguments**
*handler* 的参数。

通常需要启用单个 Monitor 来同时监听多种相同的事件。例如，使用一个 Monitor
监听并处理具有不同股票名称的股票价格变动。可以通过生成 Monitor 实例来实现这一目的。

在 Monitor 中，通过
`spawnMonitor` 接口深拷贝构造一个
subMonitor。`spawnMonitor` 的功能如下:

1. 构造一个深拷贝的 Monitor 新实例。
2. 深拷贝原 Monitor 中所有支持深拷贝的属性和方法。
3. 在生成的 Monitor 实例中可以通过参数，指定需要执行的操作。

### 获取 CEP 引擎 monitor 实例

**获取一级 monitor
实例**

**语法**

```
getCEPEngineMonitor(engine, subEngineName, [monitorName])
```

**详情**

获取指定
CEP 引擎中指定或所有一级（非 spawn）monitor 实例，进一步查看其成员变量。

**返回值：** monitor
实例，或一个字典（键为 monitor 名称， 值为 monitor 实例）。

**参数**

**engine** CEP
引擎句柄或名称。

**subEngineName** 字符串标量，表示 CEP 子引擎名称。

**monitorName**
字符串标量，可选参数，表示 monitor 名称。若不指定，返回所有一级 monitor
实例。

**示例**

```
monitors = getCEPEngineMonitor('cep1', 'cep1', 'mainMonitor')
```

**获取
subMonitor
实例**

**语法**

```
getCEPEngineSubMonitor(engine, subEngineName, monitorName)
```

**详情**

返回指定
monitor 在指定 CEP 引擎中生成的 subMonitor。如果指定的是一级（非 spawn）monitor，则该函数返回它生成的所有
subMonitor，包括所有嵌套级别。如果指定的是一个
subMonitor，则该函数仅返回它直接生成的监视器（即下一层）。

**返回值：**一个字典，键为 monitor 名称， 值为
monitor 实例。

**参数**

**engine** CEP
引擎句柄或名称。

**subEngineName** 字符串标量，表示 CEP
子引擎名称。

**monitorName** 字符串标量，可选参数，表示 monitor
名称。

**示例**

```
monitors = getCEPEngineSubMonitor('cep1', 'cep1', 'mainMonitor')
```

### 终止 Monitor 实例

**语法**

`destroyMonitor()`

终止 Monitor 实例。传入 CEP 引擎的 Monitor 实例将持续存在，直至引擎被删除。内部生成的 Monitor 可以通过
`destroyMonitor` 接口进行删除。

如果在 Monitor 中已声明
`onDestroy` 方法，则在终止 Monitor 实例之前会执行此方法。终止 Monitor
实例后，其内部声明的事件监听器将不会被触发，但它不会被立即移除，而是在下一次进行事件匹配时才会被移除。
