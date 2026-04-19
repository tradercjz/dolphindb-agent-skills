# fxSwapPricer

首发版本：3.00.4

## 语法

`fxSwapPricer(instrument, pricingDate, spot, domesticCurve,
foreignCurve)`

## 详情

计算外汇掉期的净现值。

## 参数

注意：所有输入向量必须等长，输入标量将自动扩展以匹配其它向量的长度。

**instrument**INSTRUMENT 类型标量或向量，一个 FxSwap 对象，表示需要定价的外汇掉期。

**pricingDate** DATE 类型标量或向量，表示定价日期。

**spot** 数值类型标量或向量，表示汇率即期价格。

**domesticCurve** MKTDATA 类型标量或向量，一个 IrYieldCurve 对象，表示本币折现曲线。

**foreignCurve** MKTDATA 类型标量或向量，一个 IrYieldCurve 对象，表示外币折现曲线。

## 返回值

DOUBLE 类型标量或向量。

## 例子

```
pricingDate = 2025.08.18

fxSwap = {
    "productType": "Swap",
    "swapType": "FxSwap",
    "currencyPair": "USDCNY",
    "direction": "Buy",
    "notionalCurrency": "USD",
    "notionalAmount": 1E6,
    "nearStrike": 7.15,
    "nearExpiry": pricingDate + 60,
    "nearDelivery": pricingDate + 62,
    "farStrike": 7.18,
    "farExpiry": pricingDate + 180,
    "farDelivery": pricingDate + 182
}

curveDates = [2025.08.21,
              2025.08.27,
              2025.09.03,
              2025.09.10,
              2025.09.22,
              2025.10.20,
              2025.11.20,
              2026.02.24,
              2026.05.20,
              2026.08.20,
              2027.02.22,
              2027.08.20,
              2028.08.21]
domesticCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": pricingDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": curveDates,
    "values":[1.5113,
              1.5402,
              1.5660,
              1.5574,
              1.5556,
              1.5655,
              1.5703,
              1.5934,
              1.6040,
              1.6020,
              1.5928,
              1.5842,
              1.6068]/100
}
foreignCurveInfo = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "referenceDate": pricingDate,
    "currency": "USD",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "frequency": "Annual",
    "dates": curveDates,
    "values":[4.3345,
              4.3801,
              4.3119,
              4.3065,
              4.2922,
              4.2196,
              4.1599,
              4.0443,
              4.0244,
              3.9698,
              3.7740,
              3.6289,
              3.5003]/100
}

instrument = parseInstrument(fxSwap)
domesticCurve = parseMktData(domesticCurveInfo)
foreignCurve = parseMktData(foreignCurveInfo)
spot = 7.1627

fxSwapPricer(instrument, pricingDate, spot, domesticCurve, foreignCurve)   // output:84379.328782705269986
fxSwapPricer(instrument, pricingDate, [spot, spot], domesticCurve, foreignCurve)
fxSwapPricer(instrument, [pricingDate, pricingDate], spot, domesticCurve, foreignCurve)
fxSwapPricer([instrument, instrument], pricingDate, spot, domesticCurve, foreignCurve)
fxSwapPricer(instrument, pricingDate, spot, [domesticCurve, domesticCurve], foreignCurve)
fxSwapPricer(instrument, pricingDate, spot, domesticCurve, [foreignCurve, foreignCurve])
```

**相关函数：**parseInstrument，parseMktData
