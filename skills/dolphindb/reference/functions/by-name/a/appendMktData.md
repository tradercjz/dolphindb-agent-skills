# appendMktData

## 语法

`appendMktData(engine, data, [eventTime])`

## 详情

向市场数据构建引擎或者定价引擎中写入市场数据。

* 对于市场数据构建引擎，写入数据表示更新缓存的历史数据集。
* 对于定价引擎，写入数据表示使用该市场数据更新定价计算。

## 参数

**engine** 市场数据构建引擎句柄或定价引擎句柄。

**data** MKTDATA 类型标量/向量，或一个字典。表示市场数据。

**eventTime** 可选参数，NANOTIMESTAMP 类型标量，表示事件发生时间。仅在启用
`engineConfig.outputTime=true` 时使用。

## 返回值

LONG 类型标量。

## 例子

例1. 向市场数据引擎中写入一个或多个市场数据。

创建市场数据构建引擎。

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.07.01
config1 = {"name": "USDCNY", "type": "FxSpotRate"}
config2 = {"name": "EURUSD", "type": "FxSpotRate"}
config3 = {"name": "EURCNY", "type": "FxSpotRate"}
engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config1, config2, config3])
```

写入一个 MKTDATA 数据（标量）

```
fxSpot1 = {
    "mktDataType": "Price",
    "referenceDate": referenceDate,
    "spotDate": 2025.07.03,
    "priceType": "FxSpotRate",
    "value": 7.12,
    "unit": "USDCNY"
}
mktData1 = parseMktData(fxSpot1)

appendMktData(engine, mktData1)
```

写入多个 MKTDATA 数据（向量）。

```
fxSpot2 = {
    "mktDataType": "Price",
    "referenceDate": referenceDate,
    "priceType": "FxSpotRate",
    "value": 7.88,
    "unit": "EURCNY"
}
fxSpot3 = {
    "mktDataType": "Price",
    "referenceDate": referenceDate,
    "priceType": "FxSpotRate",
    "value": 1.10,
    "unit": "EURUSD"
}
mktData2 = parseMktData(fxSpot2)
mktData3 = parseMktData(fxSpot3)
appendMktData(engine, [mktData1, mktData2, mktData3])
```

查看生成的市场数据。

```
re = getMktData(engine, "Price", referenceDate, "EURUSD")
print(re)

// output: {"mktDataType": "Price","priceType": "FxSpotRate","spotDate": "2025.07.03","referenceDate": "2025.07.01","value": 1.1,"unit": "EURUSD","version": 2,"underlying": "EURUSD"}
```

例2. 当引擎配置为`outputTime=true` 时，使用 `appendMktData`
插入数据时需要指定 *eventTime* 参数。

```
// 清理环境（如果引擎已存在）
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}

// 设置参考日期和配置
referenceDate = 2025.07.01
config1 = {"name": "USDCNY", "type": "FxSpotRate"}
config2 = {"name": "EURUSD", "type": "FxSpotRate"}
config3 = {"name": "EURCNY", "type": "FxSpotRate"}

// 创建引擎配置，启用 outputTime
engineConfig = {
    "outputTime": true
}

// 创建市场数据构建引擎
engine = createMktDataEngine(
    name="MKTDATA_ENGINE",
    referenceDate=referenceDate,
    mktDataConfig=[config1, config2, config3],
    engineConfig=engineConfig
)

// 创建 MKTDATA 类型数据
fxSpot1 = {
    "mktDataType": "Price",
    "referenceDate": referenceDate,
    "spotDate": 2025.07.03,
    "priceType": "FxSpotRate",
    "value": 7.12,
    "unit": "USDCNY"
}
mktData1 = parseMktData(fxSpot1)

// 使用 appendMktData 并指定 eventTime 参数
eventTime = now()
appendMktData(engine, mktData1, eventTime)

re = getMktData(engine, "Price", referenceDate, "USDCNY")
print(re)

// output: {"mktDataType": "Price","priceType": "FxSpotRate","spotDate": "2025.01.03","referenceDate": "2025.01.01","value": 7.12,"unit": "USDCNY","version": 2,"underlying": "USDCNY"}
```

**相关函数**：createMktDataEngine, createPricingEngine,
parseMktData, getMktData
