# eqVolatilitySurfaceBuilder

首发版本：3.00.5

## 语法

`eqVolatilitySurfaceBuilder(referenceDate, optionExpiries, strikes, optionPrices,
payoffTypes, spot, discountCurve, dividendCurve, [model='SVI'], [surfaceName])`

## 详情

构建权益类期权波动率曲面。

## 参数

**referenceDate** DATE 类型标量，表示曲面的参考日期。

**optionExpiries** DATE 类型向量，表示期权合约的到期日。

**strikes** DOUBLE 类型矩阵，列数与 optionExpries 一致，表示期权合约的执行价。

**optionPrices** DOUBLE 类型矩阵，列数与 optionExpries 一致，表示期权合约的价格。

**payoffTypes** STRING 类型矩阵，列数与 optionExpries 一致，表示期权类型。可选 “Call” 和 “Put”。

注意： *strikes* ， *optionPrices* ， *payoffTypes*  形状要求一致。

**spot** DOUBLE 类型标量，表示即期价格。

**discountCurve** IrYieldCurve 对象，表示折现曲线。

**dividendCurve** DividendCurve 对象，表示标的分红曲线。

**model** 可选参数，STRING 类型标量，表示构建波动率微笑的模型。默认值为 “SVI”，可选值为 “SABR”，“Linear”，“CubicSpline”。

**surfaceName** 可选参数，STRING 类型标量，表示曲面名称。

## 返回值

一个 VolatilitySurface 对象。

## 例子

下面展示标的为科创 50ETF(588080.SH) 期权的波动率曲面构建过程。

```
referenceDate = 2026.02.11
spot = 1.5007

// 1. Term Structure
termDates = [2026.02.25, 2026.03.25, 2026.06.24, 2026.09.23]

// 2. Raw Data Matrices (Aligned)
callPrices = matrix(
    [0.2402, 0.1908, 0.1415, 0.0927, 0.0496, 0.0199, 0.0075, 0.0032, 0.0014, 0.0010, 0.0007, 0.0002],
    [0.2398, 0.1956, 0.1516, 0.1095, 0.0780, 0.0530, 0.0347, 0.0232, 0.0152, 0.0101, 0.0069, 0.0043],
    [0.2537, 0.2137, 0.1803, 0.1494, 0.1252, 0.1051, 0.0871, 0.0717, 0.0597, 0.0500, 0.0421, 0.0361],
    [0.2730, 0.2442, 0.2086, 0.1816, 0.1676, 0.1439, 0.1301, 0.1099, 0.0961, 0.0848, 0.0748, 0.0663]
)
putPrices = matrix(
    [0.0003, 0.0003, 0.0004, 0.0018, 0.0085, 0.0297, 0.0671, 0.1130, 0.1601, 0.2084, 0.2609, 0.3124],
    [0.0033, 0.0062, 0.0114, 0.0215, 0.0383, 0.0621, 0.0947, 0.1331, 0.1767, 0.2114, 0.2565, 0.3032],
    [0.0234, 0.0349, 0.0505, 0.0713, 0.0936, 0.1237, 0.1562, 0.1919, 0.2218, 0.2610, 0.3010, 0.3437],
    [0.0445, 0.0640, 0.0808, 0.1062, 0.1312, 0.1615, 0.1882, 0.2187, 0.2567, 0.2937, 0.3323, 0.3777]
)
strikes = matrix(
    [1.2500, 1.3000, 1.3500, 1.4000, 1.4500, 1.5000, 1.5500, 1.6000, 1.6500, 1.7000, 1.7500, 1.8000],
    [1.2500, 1.3000, 1.3500, 1.4000, 1.4500, 1.5000, 1.5500, 1.6000, 1.6500, 1.7000, 1.7500, 1.8000],
    [1.2500, 1.3000, 1.3500, 1.4000, 1.4500, 1.5000, 1.5500, 1.6000, 1.6500, 1.7000, 1.7500, 1.8000],
    [1.2500, 1.3000, 1.3500, 1.4000, 1.4500, 1.5000, 1.5500, 1.6000, 1.6500, 1.7000, 1.7500, 1.8000]
)

// 3. Discount Curve
discountCurveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "curveName": "CNY_RF",
    "referenceDate": referenceDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": [referenceDate + 1, referenceDate + 3650],
    "values":[0.02, 0.02]
}
discountCurve = parseMktData(discountCurveDict)

// 4. Implied Dividend Curve
// Using Call-Put Parity on the full matrices
dividendCurve = eqDividendCurveBuilder(
    referenceDate, termDates, "CallPutParity", ,
    callPrices, putPrices, strikes, spot, discountCurve, "Actual365"
)

// 5. Volatility Surface Construction Data
// Selecting OTM options: Puts for Low Strikes, Calls for High Strikes
optionExpiries = termDates
optionPrices = matrix(
    [0.0003, 0.0003, 0.0004, 0.0018, 0.0085, 0.0297, 0.0075, 0.0032, 0.0014, 0.0010, 0.0007, 0.0002],
    [0.0033, 0.0062, 0.0114, 0.0215, 0.0383, 0.0621, 0.0347, 0.0232, 0.0152, 0.0101, 0.0069, 0.0043],
    [0.0234, 0.0349, 0.0505, 0.0713, 0.0936, 0.1237, 0.0871, 0.0717, 0.0597, 0.0500, 0.0421, 0.0361],
    [0.0445, 0.0640, 0.0808, 0.1062, 0.1312, 0.1615, 0.1301, 0.1099, 0.0961, 0.0848, 0.0748, 0.0663]
)
payoffTypes = matrix(
    ["Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call"]
)

// 6. Build Surface.
surf = eqVolatilitySurfaceBuilder(
        referenceDate,
        optionExpiries,
        strikes,        // Matrix
        optionPrices,   // Matrix (OTM)
        payoffTypes,    // Matrix ("Call"/"Put")
        spot,
        discountCurve,
        dividendCurve,
        "SABR",         // Model
        "588080.SH"     // Name
)
print(surf)

// 波动率曲面可视化

dts = (0..20)*0.05
ks = (0..40)*((max(strikes[0])-min(strikes[0]))\40)+min(strikes[0])
m = optionVolPredict(surf, dts, ks).rename!(dts, ks)

plot(
    m,
    title=["Vol Surface", "K", "T", "vol"],
    chartType=SURFACE)
```

**相关函数：**
parseMktData、eqDividendCurveBuilder
