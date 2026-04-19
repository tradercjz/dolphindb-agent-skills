# eqProxyVolatilitySurfaceBuilder

首发版本：3.00.5

## 语法

`eqProxyVolatilitySurfaceBuilder(referenceDate, proxyExpiries, proxyStrikes,
proxyCallPrices, proxyPutPrices, proxySpot, spot, discountCurve, dividendCurve,
[model=”SVI”], [surfaceName])`

## 详情

构造权益类代理波动率曲面。

## 参数

**referenceDate** DATE 类型标量，表示参考日期。

**proxyExpiries** DATE 类型向量，表示代理期权合约的到期日。

**proxyStrikes** DOUBLE 类型矩阵，表示代理期权合约的执行价，列数与 *proxyExpiries* 一致。

**proxyCallPrices** DOUBLE 类型矩阵，表示代理期权合约的看涨报价，列数与 *proxyExpiries* 一致，行数与
*proxyStrikes* 一致。

**proxyPutPrices** DOUBLE 类型矩阵，表示代理期权合约的看跌报价，列数与 *proxyExpiries* 一致，行数与
*proxyStrikes* 一致。

**proxySpot** DOUBLE 类型标量，表示代理期权的现货报价。

**spot** DOUBLE 类型标量，表示期权的现货报价。

**discountCurve** MKTDATA 标量或向量，表示折现曲线（IrYieldCurve）。

**dividendCurve** MKTDATA 标量或向量，表示股息曲线（DividendCurve）。该曲线通过
`eqDividendCurveBuilder` 构建。

**model** 可选参数，STRING 类型标量，表示构建波动率微笑的模型。默认值为 “SVI”， 可选值为“SABR”，
“Linear”，“CubicSpline”， “SVI”。

**surfaceName** 可选参数，STRING 类型标量，表示曲面名称。

## 返回值

一个 VolatilitySurface 对象。

## 例子

```
referenceDate = 2025.11.12

// parse For discount curve: CNY_FR_007

discountCurveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "curveName": "CNY_FR_007",
    "referenceDate": referenceDate,
    "currency": "CNY",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": [
        2025.11.13, 2025.11.19, 2025.11.26, 2025.12.03, 2025.12.12,
        2026.01.12, 2026.02.12, 2026.05.12, 2026.08.12, 2026.11.12,
        2027.05.12, 2027.11.12, 2028.11.12
    ],
    "values":[
        0.015219, 0.015311, 0.015668, 0.015948, 0.016003,
        0.015557, 0.015474, 0.015278, 0.01517, 0.01515,
        0.015306, 0.015462, 0.015716
    ]
}
discountCurve = parseMktData(discountCurveDict)

// build eq dividend curve

spot = 7.285

term_dates = [2026.01.28, 2026.03.25, 2026.06.23, 2026.12.23]

call_prices = matrix(
    [1.2850, 1.0350, 0.7850, 0.5350, 0.3078, 0.1618, 0.0730, 0.0318, 0.0141, 0.0073],
    [1.2850, 1.0350, 0.7850, 0.5350, 0.3421, 0.2235, 0.1388, 0.0898, 0.0544, 0.0362],
    [1.2850, 1.0350, 0.7850, 0.5350, 0.3901, 0.2851, 0.2087, 0.1495, 0.1083, 0.0788],
    [1.2850, 1.0350, 0.7850, 0.5350, 0.2850, 0.0945, 0.0168, 0.0031, 0.0016, 0.0012]
)

put_prices = matrix(
    [0.0040, 0.0086, 0.0189, 0.0408, 0.0938, 0.1934, 0.3500, 0.5638, 0.7947, 1.0380],
    [0.0279, 0.0493, 0.0847, 0.1428, 0.2354, 0.3668, 0.5289, 0.7182, 0.9429, 1.1685],
    [0.1000, 0.1525, 0.2224, 0.3175, 0.4276, 0.5790, 0.7471, 0.9336, 1.1392, 1.3555],
    [0.0012, 0.0013, 0.0021, 0.0048, 0.0139, 0.0710, 0.2414, 0.4752, 0.7342, 0.9793]
)

strikes = matrix(
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25],
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25],
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25],
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25]
)

dividendCurve = eqDividendCurveBuilder(referenceDate, term_dates, "CallPutParity", ,
    call_prices, put_prices, strikes, spot, discountCurve, "Actual365");

// build eq proxy volatility surface

expiries = [2026.01.28, 2026.03.25, 2026.06.23, 2026.12.23]

call_prices = matrix(
    [1.2850, 1.0350, 0.7850, 0.5350, 0.3078, 0.1618, 0.0730, 0.0318, 0.0141, 0.0073],
    [1.2850, 1.0350, 0.7850, 0.5350, 0.3421, 0.2235, 0.1388, 0.0898, 0.0544, 0.0362],
    [1.2850, 1.0350, 0.7850, 0.5350, 0.3901, 0.2851, 0.2087, 0.1495, 0.1083, 0.0788],
    [1.2850, 1.0350, 0.7850, 0.5350, 0.2850, 0.0945, 0.0168, 0.0031, 0.0016, 0.0012]
)

put_prices = matrix(
    [0.0040, 0.0086, 0.0189, 0.0408, 0.0938, 0.1934, 0.3500, 0.5638, 0.7947, 1.0380],
    [0.0279, 0.0493, 0.0847, 0.1428, 0.2354, 0.3668, 0.5289, 0.7182, 0.9429, 1.1685],
    [0.1000, 0.1525, 0.2224, 0.3175, 0.4276, 0.5790, 0.7471, 0.9336, 1.1392, 1.3555],
    [0.0012, 0.0013, 0.0021, 0.0048, 0.0139, 0.0710, 0.2414, 0.4752, 0.7342, 0.9793]
)

strikes = matrix(
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25],
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25],
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25],
    [6.00, 6.25, 6.50, 6.75, 7.00, 7.25, 7.50, 7.75, 8.00, 8.25]
)

proxy_spot = 7.285
spot = 7169.79

surface = eqProxyVolatilitySurfaceBuilder(referenceDate, expiries, strikes,
    call_prices, put_prices, proxy_spot, spot, discountCurve, dividendCurve , "SVI")
print(surface)
```

**相关函数：**parseMktData、eqDividendCurveBuilder
