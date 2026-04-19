<!-- Auto-mirrored from upstream `documentation-main/stream/defining_event_listeners.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 定义事件监听器

## 定义事件监听器

在 CEP 引擎中，通过 `addEventListener` 指定事件匹配规则和回调函数，返回一个 EventListener
实例。事件监听器只能在 Monitor 内调用，其观察注入引擎的每个事件，当事件或事件模式与匹配规则相匹配时，会触发执行回调函数。

**语法**

```
addEventListener(handler, [eventType], [condition], [times="all"], [at], [wait], [within], [exceedTime], [name])
```

**参数**

* 事件匹配：

  **handler** 回调函数，如果指定了 *eventType*
  则为一元函数，参数为匹配的事件。如果指定为按时间触发，则没有参数。

  ```
  def actions1(stockVal){
      //将事件类型 stockVal 的属性写入一个共享表
      insert into objByName("sharedUSPrices") values([stockVal.price, stockVal.qty])
  }
  ```

  *handler* 中可以动态添加新的监听器：

  ```
  def actions1(stockVal){
      //将事件类型 stockVal 的属性写入一个共享表
      insert into objByName("sharedUSPrices") values([stockVal.price, stockVal.qty])
      //新增加一个事件侦听器
      addEventListener(handler=action2, eventType="Stock", condition=<self.prices > stockVal.price>)
  }
  ```

  **eventType**字符串标量，表示事件类型。若指定为 “any”，则表示任意事件。

  **condition** 元代码类型，指定匹配的事件条件，即事件匹配规则。元代码的返回结果必须是布尔值。例如 *eventType* 为
  Stock 时，指定 <Stock.price > 10 and Stock.qty < 10> 。

  **times** 可以是正整数或者 ”all”，表示在 *handler* 被触发指定次数后自动删除监听，默认为
  ”all”。例如，若设置为 5，表示 *handler* 被触发 5 次后，将删除该监听器；若设置为
  ”all”，则会持续监听事件，对每个匹配的事件都触发 *handler*，直至引擎被删除。
* 按时间触发（此时不会进行事件匹配，因此不可指定 *eventType*）：

  **at** 一个长度为 6 的元组，用于指定触发 *handler* 的时间频率。其形式为 (seconds，minutes,
  hours, days\_of\_the\_week，days\_of\_the\_month, month )
  ，其中各元素依次表示秒（必须指定）、分钟、小时、一周中的第几天、当月的第几天、月份。如果*times*="all”，则表示每月/日/周几/小时/分钟的第
  seconds 秒触发 *handler*。例如：(0, 5, , , )，表示在每小时的 05 分触发 *handler*。如果
  *times* 指定为具体数字，则 *handler* 只会被触发指定次数。

  **wait** DURATION 类型，表示等待多长时间后触发 *handler*。如果
  *times*=”all”，则表示每隔多久触发 *handler*。例如：*wait* = 60s, *times*=”all”，每隔 60秒触发一次 *handler*。如果 *times* 指定为具体数字，则
  *handler* 只会被触发指定次数。
* 同时限定时间和事件：

  **within** 仅在限定的时间内收到匹配的事件时才触发
  *handler*。例如：*eventType*="tickets", *within*=60s ，表示60秒内匹配到事件
  tickets，则触发 *handler*，否则删除这个监听器。

  **exceedTime** 仅在限定的时间内没有匹配的事件时才触发
  *handler*。例如：*eventType*="tickets",
  *exceedTime*=60s，表示若60秒内未匹配到事件 tickets，则触发
  *handler*，否则删除这个监听器。

下面举例说明事件监听器的几种触发方式：

|  |
| --- |
| **事件匹配：监听单一事件或者所有事件，并且限定事件条件** |
| 监听价格大于10.0 的股票。下例中 *eventType* 为事件，*condition* 为事件匹配条件，*handler* 为监听到符合条件的事件之后的回调函数。   * ```   addEventListener(handler=action, eventType=`Stock, condition=<Stock.price > 10.0>)   ```   监听所有的股票   * ```   addEventListener(handler=action, eventType=`Stock)   ```   监听任意事件   * ```   addEventListener(handler=action, eventType="any")   ``` |
| **按时间触发** |
| 在固定时间触发，比如：在每天的 8:30 触发。  `addEventListener(handler=action, at=(0,30,8,,,))`  等待固定时间之后触发，比如：   * 从监听器被添加开始，每隔60秒触发一次。  `addEventListener(handler=action,   wait=60s)` * 从监听器被添加开始，等待60秒触发一次。  `addEventListener(handler=action,   wait=60s,times=1)` |
| **同时限定时间和事件** |
| 在限定时间内匹配事件，比如在60秒内匹配到价格大于10.0的 Stock 事件，则执行回调函数。   * `` addEventListener(handler=action,   eventType=`Stock, condition=<Stock.price >   10.0>，within = 60s,times=1) ``   在限定时间内未匹配事件，如在60秒内没有匹配到价格大于10.0的 Stock 事件，则执行回调函数。   * `` addEventListener(handler=action,   eventType=`Stock, condition=<Stock.price >   10.0>，exceedTime= 60s,times=1) `` |

**name** 字符串标量，可选参数，表示监听器的名称，用于唯一标识该监听器。默认值根据 *condition* 得出：

* 若指定 *condition*，则名称为其表达式的字符串形式；
* 若 *condition* 为空且指定了 *eventType*，则名称为 *eventType*；
* 若 *condition* 和 *eventType* 均未指定，则默认名称为 "timer"；
* 若生成的名称与现有监听器重名，将自动在名称后追加编号以确保唯一性。

## 获取事件监听器实例

在 CEP 引擎中，`getEventListener` 是 monitor 的一个成员方法，可用于查询当前 monitor
中已注册的事件监听器实例。若指定 *listenerName*，则返回对应的事件监听器实例，否则返回所有事件监听器实例。

返回值为一个 EventListener 实例，或一个字典（键为事件监听器名称， 值为事件监听器实例）。

**语法**

```
getEventListener([listenerName])
```

**参数**

**listenerName** 字符串标量，表示事件监听器名称。

**示例**

```
listeners = getEventListener('Stock')
```

## EventListener 类说明

EventListener 类封装了 listener 的所有属性与方法。

**属性**

| 属性名 | 描述 |
| --- | --- |
| name | 监听器名称 |
| handler | 回调函数名称 |
| eventType | 匹配的事件类型 |
| condition | 事件匹配规则 |
| times | 最多触发次数 |
| at | 定时触发的时间设置 |
| wait | 触发前等待时间 |
| within | 限时内匹配事件触发 |
| exceedTime | 限时未匹配事件触发 |

**方法**

**terminate()**：终止该监听器。
