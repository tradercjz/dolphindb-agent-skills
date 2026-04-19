# cmFutEuropeanOptionPricer

首发版本：3.00.5

## 语法

`cmFutEuropeanOptionPricer(instrument, pricingDate, futPrice, discountCurve,
futPriceCurve, volSurf, [setting], [model], [method])`

## 详情

对商品期货欧式期权进行定价。

## 参数

**instrument** INSTRUMENT 类型标量或向量，表示需要定价的商品期货欧式期权。

**pricingDate** DATE 类型标量或向量，表示定价日期。

**futPrice** DOUBLE 类型标量或向量, 表示标的期货的现价。

**discountCurve** MKTDATA 标量或向量，表示折现曲线（IrYieldCurve）。

**futPriceCurve** MKTDATA 标量或向量，表示期货价格曲线（AssetPriceCurve）。

**volSurf** MKTDATA 标量或向量，表示波动率曲面（VolatilitySurface），该曲面由
`cmFutVolatilitySurfaceBuilder` 构建。

**setting** 可选参数，字典（Dictionary<STRING,
BOOL>），用于指定是否计算希腊字母（Greeks）所代表的期权价格敏感性指标。可选值：

| 键 | 值 | 描述 |
| --- | --- | --- |
| calcDelta | 布尔值，默认为 false | 是否计算 Delta，即期权价格相对于标的资产价格的敏感性。 |
| calcGamma | 布尔值，默认为 false | 是否计算 Gamma，即期权 Delta 相对于标的资产价格的敏感性。 |
| calcVega | 布尔值，默认为 false | 是否计算 Vega，即期权价格相对于标的资产波动率的敏感性。 |
| calcTheta | 布尔值，默认为 false | 是否计算 Theta，即期权价格相对于时间变化的敏感性。 |
| calcRho | 布尔值，默认为 false | 是否计算 Rho，即期权价格相对于无风险利率的敏感性。 |

**model** 可选参数，STRING 类型标量。默认且唯一支持的值为“Black76”，表示采用 Black76 模型进行定价。

**method** 可选参数，STRING 类型标量。默认且唯一支持的值为“ Analytic”，表示采用解析法。

## 返回值

* 若不指定 *setting* 参数，返回 DOUBLE 类型标量，表示期权的净现值，即期权的理论价格。
* 若指定 *setting* 参数，返回字典（Dictionary<STRING,
  DOUBLE>），包含期权的净现值以及希腊字母（Greeks）所代表的期权价格敏感性指标。有关敏感性指标的说明请参考 *settings*
  参数说明。

## 例子

```
pricingDate = 2019.07.08
spot = 2800.0
strike = spot * 1.2
nominal = 1.0

// Discount curve (CNY FR007) — zero rates
discountCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": pricingDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": [pricingDate+2, pricingDate+8, pricingDate+93, pricingDate+185, pricingDate+276, pricingDate+367,
              pricingDate+732, pricingDate+1099, pricingDate+1463, pricingDate+1828, pricingDate+2558, pricingDate+3654],
    "values": [0.0145993931630537, 0.0229075517972275, 0.0253020667393029, 0.0257564866303201,
               0.0259751440992468, 0.0260355181479988, 0.0265336263144786, 0.0272721454114050,
               0.0282024453631075, 0.0290231222075799, 0.0304665029488732, 0.0319855013976250]
}
discountCurve = parseMktData(discountCurveInfo)

// Futures price curve (Soymeal)
futPriceCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "AssetPriceCurve",
    "referenceDate": pricingDate,
    "currency": "CNY",
    "asset": "SOY_MEAL",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": [2019.09.16, 2019.11.14, 2019.12.13, 2020.01.15, 2020.03.13],
    "values": [2784, 2821, 2772, 2847, 2775]
}
futPriceCurve = parseMktData(futPriceCurveInfo)

// Option expiries, futures maturities, strikes, market prices, payoff types
optionExpiries = [2019.08.07, 2019.10.11, 2019.11.07, 2019.12.06, 2020.02.07]
futMaturities = [2019.09.16, 2019.11.14, 2019.12.13, 2020.01.15, 2020.03.13]
strikes = [
    [2600,2650,2700,2750,2800,2850,2900,2950,3000,3050],
    [2600,2650,2700,2750,2800,2850,2900,2950,3000,3050],
    [2650,2700,2750,2800,2850,2900,2950,3000],
    [2650,2700,2750,2800,2850,2900,2950,3000],
    [2600,2650,2700,2750,2800,2850,2900]
]
optionPrices = [
    [9,17,30,48.5,57,37.5,23,13.5,7.5,4],
    [29,41.5,56.5,75.5,98,95.5,75,58.5,44.5,33.5],
    [50,68.5,90.5,89,69,52.5,39,29],
    [56,72,91,113,134.5,112.5,93,76.5],
    [58.5,75.5,95,118,119.5,98.5,80.5]
]
payoffTypes = [
    ["Put","Put","Put","Put","Call","Call","Call","Call","Call","Call"],
    ["Put","Put","Put","Put","Put","Call","Call","Call","Call","Call"],
    ["Put","Put","Put","Call","Call","Call","Call","Call"],
    ["Put","Put","Put","Put","Call","Call","Call","Call"],
    ["Put","Put","Put","Put","Call","Call","Call"]
]

// Build vol surface from quotes
volSurf = cmFutVolatilitySurfaceBuilder(pricingDate, futMaturities, optionExpiries, strikes, optionPrices, payoffTypes, discountCurve, futPriceCurve)
print(volSurf)
// Instrument
cmFutEuropeanOption = {
    "productType": "Option",
    "optionType": "EuropeanOption",
    "assetType": "CmFutEuropeanOption",
    "instrumentId": "SOYMEAL_CALL",
    "notionalAmount": nominal,
    "notionalCurrency": "CNY",
    "strike": strike,
    "maturity": pricingDate + 180,
    "payoffType": "Call",
    "dayCountConvention": "Actual365",
    "underlying": "SOY_MEAL",
    "domesticCurve": "CNY_FR_007"
}
instrument = parseInstrument(cmFutEuropeanOption)

// Price
result = cmFutEuropeanOptionPricer(instrument, pricingDate, spot, discountCurve, volSurf)
```

**相关函数：**parseMktData、parseInstrument、cmFutVolatilitySurfaceBuilder
