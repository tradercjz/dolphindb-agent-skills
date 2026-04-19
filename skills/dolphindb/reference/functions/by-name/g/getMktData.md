# getMktData

## 语法

`getMktData(dataSet, type, date, name)`

## 详情

在指定估值日期下，根据市场数据类型和名称，从数据集中获取相应的市场数据。

## 参数

**dataSet** 市场数据集合，支持以下类型：

* 市场数据构建引擎（由 `createMktDataEngine` 创建）
* 自定义市场数据集合，可以是向量或字典，其数据结构需符合 `instrumentPricer`
  所规定的市场数据输入规范。

**type** 字符串标量，表示市场数据类型，支持以下三种类型：

* "Price"：价格数据(期权标的价格)
* "Curve"：收益率曲线数据
* "Surface"：波动率曲面数据

**date** DATE 类型标量，参考日期。

**name** 字符串标量，表示市场数据名称（如曲线名称、曲面名称等）。

## 返回值

MKTDATA 类型标量。

## 例子

本例通过 `createMktDataEngine`
实时构建三种类型的市场数据：美元兑人民币（USDCNY）、欧元兑美元（EURUSD）和欧元兑人民币（EURCNY），然后通过
`getMktData` 查看引擎构造的即期价格数据。

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.07.01

config1 = {
    "name": "USDCNY",
    "type": "FxSpotRate"
}
config2 = {
    "name": "EURUSD",
    "type": "FxSpotRate"
}
config3 = {
    "name": "EURCNY",
    "type": "FxSpotRate"
}

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config1, config2, config3])

typeCol = ["FxSpot", "FxSpot", "FxSpot"]
nameCol = ["USDCNY", "EURCNY", "EURUSD"]
priceCol = [7.12, 7.88, 1.10]

data = table(typeCol as type, nameCol as name, priceCol as price)

engine.append!(data)
sleep(100)

re = getMktData(engine, "Price", referenceDate, "USDCNY")
print(re)
```

相关函数：createMktDataEngine, instrumentPricer
