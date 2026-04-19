# createPricingEngine

首发版本：3.00.5

## 语法

`createPricingEngine(name, instrument, [handler], [engineConfig])`

## 详情

创建实时估值定价引擎。该引擎支持调用 DolphinDB 内置估值定价函数，也支持用户传入自定义函数。

## 参数

**name** 字符串标量，表示引擎名称。该参数是引擎在一个数据节点上的唯一标识，可包含字母，数字和下划线，但必须以字母开头。

**instrument** INSTRUMENT 类型标量或向量，表示待定价的金融工具。定价过程中，市场数据匹配规则遵循 instrumentPricer 的规范。

**handler** 可选参数，一个自定义函数，用于处理定价完成后的结果输出。

* 若 *engineConfig* 中设置 `outputTime = true`，函数签名为
  `def(eventTime, name, date, npv)`；
* 若 *engineConfig* 中设置 `outputTime = false`（默认值），函数签名为
  `def(name, date, npv)`。

参数说明如下：

* eventTime：NANOTIMESTAMP，触发事件的时间。
* name：STRING，定价对象的 instrumentId。
* date：DATE，定价日期。
* npv：DOUBLE，定价结果的净值。

**engineConfig** 可选参数，一个字典，用于设置引擎运行配置。字典包含如下键值对：

* numThreads：可选，整型标量，表示工作线程数，默认 8。设为 0 表示同步执行。
* maxQueueDepth：可选，整型标量，表示最大队列深度，默认 10,000,000。
* useSystemTime：可选，布尔标量，表示是否使用系统时间作为事件时间。默认为 true，使用系统时间作为事件时间。
* timeColumn：可选，字符串标量，指定时间列作为事件时间。若指定该参数，必须将 useSystemTime 设置为 false。
* outputTime：可选，布尔标量，表示是否输出事件时间列。默认值为 false。

## 返回值

返回一个定价引擎句柄。

## 例子

本例中定义待定价金融工具 240025.IB，根据 `instrumentPricer` 的默认规则，该工具将使用名为
CNY\_TREASURY\_BOND 的市场数据。通过调用 `appendMktData` 接口将相关市场数据写入定价引擎。

```
try{dropStreamEngine("PRICING_ENGINE")}catch(ex){}

bondDict  = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "240025.IB",
    "start": 2024.12.25,
    "maturity": 2031.12.25,
    "issuePrice": 100.0,
    "coupon": 0.0149,
    "frequency": "Annual",
    "dayCountConvention": "ActualActualISDA"
}
instrument = parseInstrument(bondDict)

pricingDate = 2025.08.18

curveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": pricingDate,
    "currency": "CNY",
    "curveName": "CNY_TREASURY_BOND",
    "dayCountConvention": "ActualActualISDA",
    "compounding": "Compounded",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": [
        2025.09.18, 2025.11.18, 2026.02.18, 2026.08.18, 2027.08.18,
        2028.08.18, 2030.08.18, 2032.08.18, 2035.08.18, 2040.08.18,
        2045.08.18, 2055.08.18, 2065.08.18, 2075.08.18
    ],
    "values": [
        1.3000, 1.3700, 1.3898, 1.3865, 1.4299,
        1.4471, 1.6401, 1.7654, 1.7966, 1.9930,
        2.1834, 2.1397, 2.1987, 2.2225
    ] \ 100.0
}

discountCurve = parseMktData(curveDict)

share streamTable(1:0, `name`date`price, [STRING, DATE, DOUBLE]) as st

def myHandler(name, date, price) {
    tableInsert(st, name, date, price)
}

engine = createPricingEngine("PRICING_ENGINE", [instrument], myHandler)

appendMktData(engine, discountCurve)

select * from st
```

| name | date | price |
| --- | --- | --- |
| 240025.IB | 2025.08.18 | 99.60 |

**相关函数**：appendMktData
