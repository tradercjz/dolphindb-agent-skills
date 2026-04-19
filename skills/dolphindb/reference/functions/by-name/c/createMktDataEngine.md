# createMktDataEngine

首发版本：3.00.5

## 语法

`createMktDataEngine(name, referenceDate, mktDataConfig,
[handler], [historicalData], [engineConfig])`

## 详情

创建市场数据（曲线/曲面等）实时构建引擎。

该引擎能够根据配置自动构建曲线和曲面等市场数据，支持历史数据回填和实时数据更新。

## 参数

**name** 字符串标量，表示引擎名称。该参数是引擎在一个数据节点上的唯一标识，可包含字母，数字和下划线，但必须以字母开头。

**referenceDate** DATE 类型标量，表示市场数据的参考日期。

**mktDataConfig** 字典或由字典组成的元组，表示市场数据构建配置。关于配置格式，请参考[下文](#%E4%BE%8B%E5%AD%90)。

**handler** 可选参数，用于处理市场数据构建结果，可为自定义函数、共享内存表或定价引擎。其参数形式或表结构由
`engineConfig.outputTime` 决定：

* `engineConfig.outputTime=false`：自定义函数的参数为 (kind, date, name,
  data)；共享内存表包含 kind(STRING)、date(DATE)、name(STRING)、data(MKTDATA) 四列。
* `engineConfig.outputTime=true`：自定义函数的参数为 (eventTime, kind,
  date, name, data)；共享内存表包含
  eventTime(NANOTIMESTAMP)、kind(STRING)、date(DATE)、name(STRING)、data(MKTDATA)
  五列。

**historicalData** 可选参数，历史市场数据，当构建过程中无法从引擎缓存或实时流中获取所需市场数据时，将从该历史数据中获取。可以是：

* 字典或向量：数据格式参考 instrumentPricer
  函数中的 *marketData* 参数。
* 自定义函数：参数是 (kind，date，name)。

**engineConfig** 可选参数，一个字典，用于设置引擎运行配置。字典包含如下键值对：

* numThreads：可选，整型标量，表示工作线程数，默认 8。
* maxQueueDepth：可选，整型标量，表示最大队列深度，默认 10,000,000。
* useSystemTime：可选，布尔标量，表示是否使用系统时间作为事件时间。默认为 true，使用系统时间作为事件时间。
* timeColumn：可选，字符串标量，指定时间列（NANOTIMESTAMP）作为事件时间。指定该列后，输入数据中需要包含该列。
* outputTime：可选，布尔标量，表示是否输出事件时间。默认为 false。

## 返回值

返回一个市场数据引擎句柄。

## mktDataConfig 配置及数据写入示例

### 外汇即期汇率

生成外汇即期汇率曲线需要配置的 *mktDataConfig* 字段包括：

* **name**：必填，字符串标量，汇率表示的货币对。可选值为"EURUSD", "USDCNY", "EURCNY", "GBPCNY",
  "JPYCNY", "HKDCNY"。货币对的表示也可由 `.` 或 `/`
  分隔，例如 "EURUSD" 也可写为 "EUR.USD" 或 "EUR/USD"。
* **type**：必填，字符串标量，必须填 "FxSpotRate"。

**配置示例：**

```
config = {
    "name": "USDCNY",
    "type": "FxSpotRate"
}
```

**说明：**

在相关曲线或曲面构建过程中自动包含外汇即期汇率曲线，例如跨币种利率互换收益率曲线或外汇波动率曲面，因此无需要单独配置。仅当需要单独输出外汇即期汇率曲线时，才需要显式配置该类市场数据。

**插入数据格式：**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| type | STRING | 固定为 "FxSpotRate" |
| name | STRING | 货币对，例如 “USDCNY”（货币对的表示可由 `.` 或 `/` 分隔）。 |
| price | DOUBLE | 当前报价 |

注：插入数据时，列名和类型必须符合以上表格定义，列顺序不作要求。

**插入数据示例：**

```
typeCol = ["FxSpot", "FxSpot", "FxSpot"]
nameCol = ["USDCNY", "EURCNY", "EURUSD"]
priceCol = [7.12, 7.88, 1.10]

data = table(typeCol as type, nameCol as name, priceCol as price)
```

**完整示例：**

```
referenceDate = 2025.01.01

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
```

* 本例中创建了三个构建目标，分别用于表示美元兑人民币（USDCNY）、欧元兑美元（EURUSD）和欧元兑人民币（EURCNY）这三种汇率报价。
* 写入的数据中仅覆盖两个构建目标，共包含三条数据：其中 USDCNY 两条，EURUSD 一条。
* 数据写入采用异步模式，因此需要预留一定的等待时间，以确保所有数据均被完整处理。

可以使用 `getMktData` 接口获取已构建好的市场数据。

```
re = getMktData(engine, "Price", referenceDate, "USDCNY")
print(re)

re = getMktData(engine, "Price", referenceDate, "EURUSD")
print(re)

re = getMktData(engine, "Price", referenceDate, "EURCNY")
print(re)
```

结果将显示 USDCNY 和 EURUSD 的最新市场数据；由于未写入 EURCNY 数据，调用 `getMktData`
将报错。

### 债券收益率曲线

生成债券收益率曲线需要配置的 *mktDataConfig* 字段包括：

* **name**：必填，曲线名称
* **type**：必填，必须是 "BondYieldCurve"
* **bonds**：必填，构建使用的基准债券
* **currency**：必填，货币单位
* **dayCountConvention**：必填，日期计数惯例
* **compounding**：选填，复利类型
* **frequency**：选填，计息频率
* **interpMethod**：选填，内插方法
* **extrapMethod**：选填，外插方法
* **method**：选填，曲线构建方法

上述字段要求与 bondYieldCurveBuilder 的参数保持一致。

**配置示例：**

```
bonds = array(ANY, 5)
for (i in 0..4) {
    bond_template = {
        "productType": "Cash",
        "assetType": "Bond",
        "bondType": "FixedRateBond",
        "instrumentId": "88" + lpad(string(i), 4, "0") + ".IB",
        "start": 2024.06.01,
        "maturity": 2024.06.01 + (i + 1) * 365,
        "issuePrice": 100,
        "coupon": 0.02,
        "dayCountConvention": "Actual365",
        "frequency": "Annual"
    };
    bonds[i] = parseInstrument(bond_template);
}

config = {
    "name": "CNY_TREASURY_BOND",
    "type": "BondYieldCurve",
    "bonds": bonds,
    "currency": "CNY",
    "dayCountConvention": "Actual365"
}
```

**说明：**

构建名称为 “CNY\_TREASURY\_BOND” 的债券收益率曲线。参考债券为五支随机生成的债券（Instrument 数据）。其他参数的使用方式可参考
`bondYieldCurveBuilder` 函数。构建过程中，引擎将基于参考债券的信息，和引擎参数中的
*referenceDate*，计算出每支债券的剩余到期时间，并按到期顺序重新排列。

**插入数据格式：**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| type | STRING | 固定为 "Bond" |
| name | STRING | 债券名称 |
| price | DOUBLE | 报价 |

**插入数据示例：**

```
typeCol = ["Bond", "Bond", "Bond", "Bond", "Bond"]
nameCol = ["880000.IB", "880001.IB", "880002.IB", "880003.IB", "880004.IB"]
priceCol = [0.015, 0.016, 0.017, 0.018, 0.019]  // YTM

data = table(typeCol as type, nameCol as name, priceCol as price)
```

**完整示例：**

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.01.01
bonds = array(ANY, 5)
for (i in 0..4) {
    bond_template = {
        "productType": "Cash",
        "assetType": "Bond",
        "bondType": "FixedRateBond",
        "instrumentId": "88" + lpad(string(i), 4, "0") + ".IB",
        "start": 2024.06.01,
        "maturity": 2024.06.01 + (i + 1) * 365,
        "issuePrice": 100,
        "coupon": 0.02,
        "dayCountConvention": "Actual365",
        "frequency": "Annual"
    };
    bonds[i] = parseInstrument(bond_template);
}

config = {
    "name": "CNY_TREASURY_BOND",
    "type": "BondYieldCurve",
    "bonds": bonds,
    "currency": "CNY",
    "dayCountConvention": "Actual365"
}

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config])

typeCol = ["Bond", "Bond", "Bond", "Bond", "Bond"]
nameCol = ["880000.IB", "880001.IB", "880002.IB", "880003.IB", "880004.IB"]
priceCol = [0.015, 0.016, 0.017, 0.018, 0.019]  // YTM

data = table(typeCol as type, nameCol as name, priceCol as price)
engine.append!(data)
sleep(100)

re = getMktData(engine, "Curve", referenceDate, "CNY_TREASURY_BOND")
print(re)
```

### 单货币利率互换曲线

生成单货币利率互换曲线需要配置的 *mktDataConfig* 字段包括：

* **name**：必填，曲线名称
* **type**：必填，必须是 "IrSingleCurrencyCurve"
* **insts** ：必填，一个 Any Vector，每个元素是一个包含三个元素的元组：[instName, instType,
  term]。其中，

  + instName, instType 是 STRING 标量
  + term 是 STRING 或者 DURATION 标量
* **currency**：必填，货币单位
* **dayCountConvention**：必填，日期计数惯例
* **discountCurve**：选填，贴现曲线
* **compounding**：选填，复利类型
* **frequency**：选填，计息频率

除 insts 外，其它字段要求与 irSingleCurrencyCurveBuilder 参数保持一致。

**配置示例：**

```
config = {
    "name": "CNY_FR_007",
    "type": "IrSingleCurrencyCurve",
    "insts": [
        ["FR_007", "Deposit", 7d],
        ["CNY_FR_007", "IrVanillaSwap", 1M],
        ["CNY_FR_007", "IrVanillaSwap", 3M],
        ["CNY_FR_007", "IrVanillaSwap", 6M],
        ["CNY_FR_007", "IrVanillaSwap", 9M],
        ["CNY_FR_007", "IrVanillaSwap", 1y],
        ["CNY_FR_007", "IrVanillaSwap", 2y],
        ["CNY_FR_007", "IrVanillaSwap", 3y],
        ["CNY_FR_007", "IrVanillaSwap", 4y],
        ["CNY_FR_007", "IrVanillaSwap", 5y],
        ["CNY_FR_007", "IrVanillaSwap", 7y],
        ["CNY_FR_007", "IrVanillaSwap", 10y]
    ],
    "currency": "CNY",
    "dayCountConvention": "Actual365"
}
```

**说明：**

本例中，构建目标是名称为 CNY\_FR\_007 的 IrSingleCurrencyCurve，报价信息参考 irSingleCurrencyCurveBuilder 例2。

**插入数据格式：**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| type | STRING | 构建目标类型，目前仅支持 Deposit 或 IrVanillaSwap |
| name | STRING | 金融工具名称 |
| term | STRING/DURATION | 合约剩余期限，例如 "1M"。 |
| price | DOUBLE | 报价数据 |

**插入数据示例：**

```
typeCol = [
    "Deposit", "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap",
    "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap",
    "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap"
]

nameCol = [
    "FR_007", "CNY_FR_007", "CNY_FR_007", "CNY_FR_007",
    "CNY_FR_007", "CNY_FR_007", "CNY_FR_007", "CNY_FR_007",
    "CNY_FR_007", "CNY_FR_007", "CNY_FR_007", "CNY_FR_007"
]

termCol = [
    7d, 1M, 3M, 6M,
    9M, 1y, 2y, 3y,
    4y, 5y, 7y, 10y
]

priceCol = [
    2.3500, 2.3396, 2.3125, 2.3613,
    2.4075, 2.4513, 2.5750, 2.6763,
    2.7650, 2.8463, 2.9841, 3.1350
] \ 100

data = table(typeCol as type, nameCol as name, termCol as term, priceCol as price)
```

**完整示例：**

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2021.05.26

config = {
    "name": "CNY_FR_007",
    "type": "IrSingleCurrencyCurve",
    "insts": [
        ["FR_007", "Deposit", 7d],
        ["CNY_FR_007", "IrVanillaSwap", 1M],
        ["CNY_FR_007", "IrVanillaSwap", 3M],
        ["CNY_FR_007", "IrVanillaSwap", 6M],
        ["CNY_FR_007", "IrVanillaSwap", 9M],
        ["CNY_FR_007", "IrVanillaSwap", 1y],
        ["CNY_FR_007", "IrVanillaSwap", 2y],
        ["CNY_FR_007", "IrVanillaSwap", 3y],
        ["CNY_FR_007", "IrVanillaSwap", 4y],
        ["CNY_FR_007", "IrVanillaSwap", 5y],
        ["CNY_FR_007", "IrVanillaSwap", 7y],
        ["CNY_FR_007", "IrVanillaSwap", 10y]
    ],
    "currency": "CNY",
    "dayCountConvention": "Actual365"
}

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config])

typeCol = [
    "Deposit", "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap",
    "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap",
    "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap", "IrVanillaSwap"
]

nameCol = [
    "FR_007", "CNY_FR_007", "CNY_FR_007", "CNY_FR_007",
    "CNY_FR_007", "CNY_FR_007", "CNY_FR_007", "CNY_FR_007",
    "CNY_FR_007", "CNY_FR_007", "CNY_FR_007", "CNY_FR_007"
]

termCol = [
    7d, 1M, 3M, 6M,
    9M, 1y, 2y, 3y,
    4y, 5y, 7y, 10y
]

priceCol = [
    2.3500, 2.3396, 2.3125, 2.3613,
    2.4075, 2.4513, 2.5750, 2.6763,
    2.7650, 2.8463, 2.9841, 3.1350
] \ 100

data = table(typeCol as type, nameCol as name, termCol as term, priceCol as price)

engine.append!(data)
sleep(100)

re = getMktData(engine, "Curve", referenceDate, "CNY_FR_007")
print(re)
```

### 跨币种利率互换收益率曲线

生成跨币种利率互换收益率曲线需要配置的 *mktDataConfig* 字段包括：

* **name**：必填，曲线名称
* **type**：必填，必须是 "IrCrossCurrencyCurve"
* **insts** ：必填，一个 Any Vector，每个元素是一个包含三个元素的元组：[instName, instType,
  term]。其中，

  + instName, instType 是 STRING 标量
  + term 是 STRING 或者 DURATION 标量
* **currency**：必填，货币单位
* **currencyPair**：必填，货币对
* **dayCountConvention**：必填，日期计数惯例
* **discountCurve**：必填，贴现曲线
* **compounding**：选填，复利类型
* **frequency**：选填，计息频率

除 insts 外，其它字段要求与 irCrossCurrencyCurveBuilder 参数保持一致。

**配置示例：**

```
config = {
    "name": "USD_USDCNY_FX",
    "type": "IrCrossCurrencyCurve",
    "insts": [
        ("USDCNY", "FxSwap", "1d"),
        ("USDCNY", "FxSwap", "1w"),
        ("USDCNY", "FxSwap", "2w"),
        ("USDCNY", "FxSwap", "3w"),
        ("USDCNY", "FxSwap", "1M"),
        ("USDCNY", "FxSwap", "2M"),
        ("USDCNY", "FxSwap", "3M"),
        ("USDCNY", "FxSwap", "6M"),
        ("USDCNY", "FxSwap", "9M"),
        ("USDCNY", "FxSwap", "1y"),
        ("USDCNY", "FxSwap", "18M"),
        ("USDCNY", "FxSwap", "2y"),
        ("USDCNY", "FxSwap", "3y")
    ],
    "currency": "USD",
    "currencyPair": "USDCNY",
    "dayCountConvention": "Actual365",
    "discountCurve": "CNY_SHIBOR_3M"
}
```

**说明：**

本例中构建目标为名称是 “USD\_USDCNY\_FX” 的跨币种利率互换收益率曲线。使用外汇掉期作为定价所使用的金融工具，指定构建时使用的贴现曲线为
“CNY\_SHIBOR\_3M”。因为跨币种利率互换收益率曲线中已经包含货币对信息，因此不需要再额外定义 FxSpot
作为构建目标。具体参数要求请参考：irCrossCurrencyCurveBuilder

**插入数据格式：**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| type | STRING | 目前仅支持 “FxSwap” |
| name | STRING | FxSwap: 对应的货币对 |
| term | STRING / DURATION | 期限 |
| price | DOUBLE | 报价数据 |

**插入数据示例：**

```
typeCol = [
    "FxSwap", "FxSwap", "FxSwap", "FxSwap",
    "FxSwap", "FxSwap", "FxSwap", "FxSwap",
    "FxSwap", "FxSwap", "FxSwap", "FxSwap",
    "FxSwap"
]
nameCol = [
    "USDCNY", "USDCNY", "USDCNY", "USDCNY",
    "USDCNY", "USDCNY", "USDCNY", "USDCNY",
    "USDCNY", "USDCNY", "USDCNY", "USDCNY",
    "USDCNY"
]
termCol = [
    "1d", "1w", "2w", "3w",
    "1M", "2M", "3M", "6M",
    "9M", "1y", "18M", "2y",
    "3y"
]
priceCol = [
    -5.54, -39.00, -75.40, -113.20,
    -177.00, -317.00, -466.00, -898.50,
    -1284.99, -1676.00, -2320.00, -2870.00,
    -3962.50
] \ 10000

data = table(typeCol as type, nameCol as name, termCol as term, priceCol as price)
insert into data values("FxSpot", "USDCNY", "0d", 7.1627)
```

**完整示例：**

利用市场数据引擎从 USDCNY 外汇掉期报价和人民币 CNY\_FR\_007 曲线，自动构建出美元的隐含收益率曲线（USD\_USDCNY\_FX）。

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.08.18

config = {
    "name": "USD_USDCNY_FX",
    "type": "IrCrossCurrencyCurve",
    "insts": [
        ("USDCNY", "FxSwap", "1d"),
        ("USDCNY", "FxSwap", "1w"),
        ("USDCNY", "FxSwap", "2w"),
        ("USDCNY", "FxSwap", "3w"),
        ("USDCNY", "FxSwap", "1M"),
        ("USDCNY", "FxSwap", "2M"),
        ("USDCNY", "FxSwap", "3M"),
        ("USDCNY", "FxSwap", "6M"),
        ("USDCNY", "FxSwap", "9M"),
        ("USDCNY", "FxSwap", "1y"),
        ("USDCNY", "FxSwap", "18M"),
        ("USDCNY", "FxSwap", "2y"),
        ("USDCNY", "FxSwap", "3y")
    ],
    "currency": "USD",
    "currencyPair": "USDCNY",
    "dayCountConvention": "Actual365",
    "discountCurve": "CNY_SHIBOR_3M"
}

typeCol = [
    "FxSwap", "FxSwap", "FxSwap", "FxSwap",
    "FxSwap", "FxSwap", "FxSwap", "FxSwap",
    "FxSwap", "FxSwap", "FxSwap", "FxSwap",
    "FxSwap"
]
nameCol = [
    "USDCNY", "USDCNY", "USDCNY", "USDCNY",
    "USDCNY", "USDCNY", "USDCNY", "USDCNY",
    "USDCNY", "USDCNY", "USDCNY", "USDCNY",
    "USDCNY"
]
termCol = [
    "1d", "1w", "2w", "3w",
    "1M", "2M", "3M", "6M",
    "9M", "1y", "18M", "2y",
    "3y"
]
priceCol = [
    -5.54, -39.00, -75.40, -113.20,
    -177.00, -317.00, -466.00, -898.50,
    -1284.99, -1676.00, -2320.00, -2870.00,
    -3962.50
] \ 10000

data = table(typeCol as type, nameCol as name, termCol as term, priceCol as price)
insert into data values("FxSpot", "USDCNY", "0d", 7.1627)

cnyShibor3mDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "curveName": "CNY_SHIBOR_3M",
    "referenceDate": referenceDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": [
        2025.08.21, 2025.08.27, 2025.09.03, 2025.09.10,
        2025.09.22, 2025.10.20, 2025.11.20, 2026.02.20,
        2026.05.20, 2026.08.20, 2027.02.22, 2027.08.20,
        2028.08.21
    ],
    "values": [
        1.5113, 1.5402, 1.5660, 1.5574,
        1.5556, 1.5655, 1.5703, 1.5934,
        1.6040, 1.6020, 1.5928, 1.5842,
        1.6068
    ] \ 100
}

cnyShibor3m = parseMktData(cnyShibor3mDict)

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config], historicalData=[cnyShibor3m])

engine.append!(data)
sleep(100)

re = getMktData(engine, "Curve", referenceDate, "USD_USDCNY_FX")
print(re)
```

1. 因为构建目标中自动包含了外汇即期汇率，因此写入数据中也需要包含相应的报价数据，否则无法构建成功。
2. 本例中将 CNY\_SHIBOR\_3M 作为历史数据传入引擎，而非实时构建，因此需要提前准备一条对应曲线。

### 外汇波动率曲面

生成外汇波动率曲面需要配置的 *mktDataConfig* 字段包括：

* **name**：必填，曲面名称
* **type**：必填，必须是 "FxVolatilitySurface"
* **names**：必填，为 ["ATM", "D25\_RR", "D25\_BF", "D10\_RR", "D10\_BF"]
  的一组排列，表示报价名称
* **terms**：必填，市场报价的对应期限
* **currencyPair**：必填，货币对
* **domesticCurve**：必填，本币折现曲线
* **foreignCurve**：必填，外币折现曲线
* **model**：选填。构建波动率曲面所用模型

上述字段要求与 fxVolatilitySurfaceBuilder 参数保持一致。

**配置示例：**

```
config = {
    "name": "USDCNY",
    "type": "FxVolatilitySurface",
    "names": ["ATM", "D25_RR", "D25_BF", "D10_RR", "D10_BF"],
    "terms": ["1d", "1w", "2w", "3w", "1M", "2M", "3M", "6M", "9M", "1y", "18M", "2y", "3y"],
    "currencyPair": "USDCNY",
    "domesticCurve": "CNY_FR_007",
    "foreignCurve": "USD_USDCNY_FX",
    "model": "SVI"
}
```

**说明：**

本例中构建目标是名为 USDCNY 的外汇波动率曲面。使用 CNY\_FR\_007 作为本币的折现曲线，USD\_USDCNY\_FX 作为外币的折现曲线，并且使用模型
SVI 进行曲面构建。

**插入数据格式：**

| 列名 | 类型 | 说明 |
| --- | --- | --- |
| type | STRING | 固定为 FxOption |
| name | STRING | 货币对 |
| subType | STRING | “ATM” / “D25\_RR” / “D25\_BF” / “D10\_RR” / “D10\_BF” |
| term | STRING / DURATION | 期限 |
| price | DOUBLE | 报价数据 |

**插入数据示例：**

```
typeCol = take("FxOption", 65)
nameCol = take("USDCNY", 65)
subTypeCol = take(["ATM"], 13)
    .append!(take(["D25_RR"], 13))
    .append!(take(["D25_BF"], 13))
    .append!(take(["D10_RR"], 13))
    .append!(take(["D10_BF"], 13))
termCol = take([
    "1d", "1w", "2w", "3w", "1M", "2M", "3M", "6M", "9M", "1y", "18M", "2y", "3y"
], 65)
priceCol = [
    0.030000, -0.007500, 0.003500, -0.010000, 0.005500,
    0.020833, -0.004500, 0.002000, -0.006000, 0.003800,
    0.022000, -0.003500, 0.002000, -0.004500, 0.004100,
    0.022350, -0.003500, 0.002000, -0.004500, 0.004150,
    0.024178, -0.003000, 0.002200, -0.004750, 0.005500,
    0.027484, -0.002650, 0.002220, -0.004000, 0.005650,
    0.030479, -0.002500, 0.002400, -0.003500, 0.005750,
    0.035752, -0.000500, 0.002750,  0.000000, 0.006950,
    0.038108,  0.001000, 0.002800,  0.003000, 0.007550,
    0.039492,  0.002250, 0.002950,  0.005000, 0.007550,
    0.040500,  0.004000, 0.003100,  0.007000, 0.007850,
    0.041750,  0.005250, 0.003350,  0.008000, 0.008400,
    0.044750,  0.006250, 0.003400,  0.009000, 0.008550
].reshape(5:13).transpose().flatten()

data = table(typeCol as type, nameCol as name, subTypeCol as subType, termCol as term, priceCol as price)
insert into data values("FxSpot", "USDCNY", "", "0d", 7.1627)
```

**完整示例：**

本例说明如何使用 DolphinDB 的市场数据引擎（`createMktDataEngine`）来构建和管理 USDCNY
外汇波动率曲面。包含如下步骤：

1. 构造波动率报价数据、即期汇率、收益率曲线数据。
2. 使用 `parseMktData` 将字典格式的曲线数据解析为 MKTDATA 类型对象。
3. 创建名为 "MKTDATA\_ENGINE" 的市场数据引擎，配置 USDCNY 波动率曲面的构建参数（使用 SVI 模型）。然后将
   CNY\_FR\_007 和 USD\_USDCNY\_FX 作为历史数据传入引擎。
4. 通过 `getMktData` 从引擎中获取构建完成的 USDCNY
   外汇波动率曲面，该曲面可用于后续的外汇期权定价。

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.08.18

config = {
    "name": "USDCNY",
    "type": "FxVolatilitySurface",
    "names": ["ATM", "D25_RR", "D25_BF", "D10_RR", "D10_BF"],
    "terms": ["1d", "1w", "2w", "3w", "1M", "2M", "3M", "6M", "9M", "1y", "18M", "2y", "3y"],
    "currencyPair": "USDCNY",
    "domesticCurve": "CNY_FR_007",
    "foreignCurve": "USD_USDCNY_FX",
    "model": "SVI"
}

typeCol = take("FxOption", 65)
nameCol = take("USDCNY", 65)
subTypeCol = take(["ATM"], 13)
    .append!(take(["D25_RR"], 13))
    .append!(take(["D25_BF"], 13))
    .append!(take(["D10_RR"], 13))
    .append!(take(["D10_BF"], 13))
termCol = take([
    "1d", "1w", "2w", "3w", "1M", "2M", "3M", "6M", "9M", "1y", "18M", "2y", "3y"
], 65)
priceCol = [
    0.030000, -0.007500, 0.003500, -0.010000, 0.005500,
    0.020833, -0.004500, 0.002000, -0.006000, 0.003800,
    0.022000, -0.003500, 0.002000, -0.004500, 0.004100,
    0.022350, -0.003500, 0.002000, -0.004500, 0.004150,
    0.024178, -0.003000, 0.002200, -0.004750, 0.005500,
    0.027484, -0.002650, 0.002220, -0.004000, 0.005650,
    0.030479, -0.002500, 0.002400, -0.003500, 0.005750,
    0.035752, -0.000500, 0.002750,  0.000000, 0.006950,
    0.038108,  0.001000, 0.002800,  0.003000, 0.007550,
    0.039492,  0.002250, 0.002950,  0.005000, 0.007550,
    0.040500,  0.004000, 0.003100,  0.007000, 0.007850,
    0.041750,  0.005250, 0.003350,  0.008000, 0.008400,
    0.044750,  0.006250, 0.003400,  0.009000, 0.008550
].reshape(5:13).transpose().flatten()

data = table(typeCol as type, nameCol as name, subTypeCol as subType, termCol as term, priceCol as price)
insert into data values("FxSpot", "USDCNY", "", "0d", 7.1627)

domesticCurveDict = {
    "mktDataType": "Curve",
    "curveName": "CNY_FR_007",
    "curveType": "IrYieldCurve",
    "referenceDate": referenceDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": [
        2025.08.21, 2025.08.27, 2025.09.03, 2025.09.10, 2025.09.22,
        2025.10.20, 2025.11.20, 2026.02.24, 2026.05.20, 2026.08.20,
        2027.02.22, 2027.08.20, 2028.08.21
    ],
    "values": [
        1.5113, 1.5402, 1.5660, 1.5574, 1.5556,
        1.5655, 1.5703, 1.5934, 1.6040, 1.6020,
        1.5928, 1.5842, 1.6068
    ] \ 100
}
domesticCurve = parseMktData(domesticCurveDict)

foreignCurveDict = {
    "mktDataType": "Curve",
    "curveName": "USD_USDCNY_FX",
    "curveType": "IrYieldCurve",
    "referenceDate": referenceDate,
    "currency": "USD",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": [
        2025.08.21, 2025.08.27, 2025.09.03, 2025.09.10, 2025.09.22,
        2025.10.20, 2025.11.20, 2026.02.24, 2026.05.20, 2026.08.20,
        2027.02.22, 2027.08.20, 2028.08.21
    ],
    "values": [
        4.3345, 4.3801, 4.3119, 4.3065, 4.2922,
        4.2196, 4.1599, 4.0443, 4.0244, 3.9698,
        3.7740, 3.6289, 3.5003
    ] \ 100
}
foreignCurve = parseMktData(foreignCurveDict)

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config], historicalData=[domesticCurve, foreignCurve])

engine.append!(data)
sleep(100)

re = getMktData(engine, "Surface", referenceDate, "USDCNY")
print(re)
```

1. 因为构建目标中自动包含了外汇即期汇率曲线，因此写入数据中也需要包含相应的报价数据，否则无法构建成功。
2. 本例中将 CNY\_FR\_007 和 USD\_USDCNY\_FX 作为历史数据传入引擎，而非实时构建，因此需要提前准备对应曲线。

## *handler* 参数示例

**指定为自定义函数**

以构建外汇即期汇率曲线为例，定义一个自定义函数，打印构建出来的市场数据。

```
def myHandler(kind, date, name, data) {
    print(data)
}

try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.01.01

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

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config1, config2, config3], handler=myHandler)

typeCol = ["FxSpot", "FxSpot", "FxSpot"]
nameCol = ["USDCNY", "EURCNY", "EURUSD"]
priceCol = [7.12, 7.88, 1.10]

data = table(typeCol as type, nameCol as name, priceCol as price)

engine.append!(data)
sleep(100)
```

**指定为共享内存表**

定义一个结构如下的共享表（需保证列顺序一致）。

| 列名 | 类型 |
| --- | --- |
| kind | STRING |
| date | DATE |
| name | STRING |
| data | MKTDATA |

**完整示例**

```
share streamTable(1:0, `kind`date`name`data, [STRING, DATE, STRING, MKTDATA]) as st

try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
referenceDate = 2025.01.01

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

engine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config1, config2, config3], handler=st)

typeCol = ["FxSpot", "FxSpot", "FxSpot"]
nameCol = ["USDCNY", "EURCNY", "EURUSD"]
priceCol = [7.12, 7.88, 1.10]

data = table(typeCol as type, nameCol as name, priceCol as price)

engine.append!(data)
sleep(100)

print(select * from st)
```

**指定为定价引擎**

创建一个定价引擎，并传入 *handler* 参数。

**完整示例**

```
try{dropStreamEngine("MKTDATA_ENGINE")}catch(ex){}
try{dropStreamEngine("PRICING_ENGINE")}catch(ex){}
referenceDate = 2025.01.01

bonds = array(ANY, 5)
for (i in 0..4) {
    bond_template = {
        "productType": "Cash",
        "assetType": "Bond",
        "bondType": "FixedRateBond",
        "instrumentId": "88" + lpad(string(i), 4, "0") + ".IB",
        "start": 2024.06.01,
        "maturity": 2024.06.01 + (i + 1) * 365,
        "issuePrice": 100,
        "coupon": 0.02,
        "dayCountConvention": "Actual365",
        "frequency": "Annual"
    };
    bonds[i] = parseInstrument(bond_template);
}

config = {
    "name": "CNY_TREASURY_BOND",
    "type": "BondYieldCurve",
    "bonds": bonds,
    "currency": "CNY",
    "dayCountConvention": "Actual365"
}

bondDict = {
    "productType": "Cash",
    "assetType": "Bond",
    "bondType": "FixedRateBond",
    "instrumentId": "880010.IB",
    "start": 2028.05.01,
    "maturity": 2038.05.01,
    "issuePrice": 100,
    "coupon": 0.02,
    "dayCountConvention": "Actual365",
    "frequency": "Annual",
    "discountCurve": "CNY_TREASURY_BOND"
}
bond = parseInstrument(bondDict)

share streamTable(1:0, `name`date`price, [STRING, DATE, DOUBLE]) as priceSt

pricingEngine = createPricingEngine("PRICING_ENGINE", [bond], tableInsert{priceSt})

mktdataEngine = createMktDataEngine("MKTDATA_ENGINE", referenceDate, [config], handler=pricingEngine)

typeCol = ["Bond", "Bond", "Bond", "Bond", "Bond"]
nameCol = ["880000.IB", "880001.IB", "880002.IB", "880003.IB", "880004.IB"]
priceCol = [0.015, 0.016, 0.017, 0.018, 0.019]  // YTM

data = table(typeCol as type, nameCol as name, priceCol as price)

mktdataEngine.append!(data)
sleep(100)

re = getMktData(mktdataEngine, "Curve", referenceDate, "CNY_TREASURY_BOND")
print(re)

print(select * from priceSt)
```

本例中使用 880000.IB ~ 880004.IB作为基准债券构建曲线 CNY\_TREASURY\_BOND，并将该曲线作为定价引擎的输入曲线，对 880010.IB
定价。最后输出定价结果到 priceSt 表中。

**相关函数**：appendMktData,
append!, getMktData, createPricingEngine
