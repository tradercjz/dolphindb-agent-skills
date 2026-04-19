# eqAmericanOptionPricer

首发版本：3.00.5

## 语法

`eqAmericanOptionPricer(instrument, pricingDate, spot, discountCurve,
dividendCurve, volSurf, [setting], [model='BlackScholes'],
[method='Analytic'])`

## 详情

对权益类美式期权进行定价。

## 参数

**instrument**
EqAmerican 类型的 Instrument 标量或向量，表示需要定价的权益类美式期权。权益类美式期权所需的关键字段详见产品字段要求。

**pricingDate**
DATE 类型标量或向量，表示定价日期。

**spot**
数值类型标量或向量，表示现货价格。

**discountCurve** IrYieldCurve 类型的 MktData 标量或向量，表示折现曲线。

**dividendCurve** DividendCurve 类型的 MktData 标量或向量，表示股息曲线。

**volSurf**
MKTDATA 类型（VolatilitySurface）的标量或向量，表示波动率曲面。

**setting**
可选参数，一个字典，用于设置定价输出。包含以下 key：

* calcDelta：value 是布尔值，指定是否计算 delta
* calcGamma：value 是布尔值，指定是否计算 gamma
* calcVega：value 是布尔值，指定是否计算 vega
* calcTheta：value 是布尔值，指定是否计算 theta
* calcRhoIr：value 是布尔值，指定是否计算 rhoir
* calcRhoDividend：value 是布尔值，指定是否计算 rhodividend

**model**
可选参数，STRING 类型标量，表示使用的模型。可选值为：

* “BlackScholes”（默认值）：Black–Scholes model
* “BAW”：Barone-Adesi-Whaley 公式
* “AmericanBinomialTree”：美式二叉树定价模型

**method**
可选参数，STRING 类型标量，表示使用的方法。可选值为：

* “Analytic”（默认值）：解析法，支持
  *model*
  为 BlackScholes 或 BAW。
* “Tree”：树方法，支持 *model* 为 AmericanBinomialTree。

## 返回值

* 当未指定
  *setting*
  时：返回 DOUBLE 类型标量，表示期权的净现值（NPV）。
* 当指定
  *setting*
  时：返回一个字典，包含 NPV 及按
  *setting*
  指定的 Greeks 结果。

## 例子

```
//腾讯股票期权定价
referenceDate = 2026.02.13
// 1. Discount Curve (HKD Proxy - Simplified)
// 注意：实际生产中应使用HIBOR或OIS曲线
discountCurveDict = {
    "mktDataType": "Curve",
    "curveType": "IrYieldCurve",
    "curveName": "HKD_RF",
    "referenceDate": referenceDate,
    "currency": "HKD",
    "dayCountConvention": "Actual365",
    "compounding": "Continuous",
    "interpMethod": "Linear",
    "extrapMethod": "Flat",
    "dates": [
        referenceDate + 1, referenceDate + 30, referenceDate + 90,
        referenceDate + 180, referenceDate + 365
    ],
    "values":[0.04, 0.04, 0.04, 0.04, 0.04]
}
discountCurve = parseMktData(discountCurveDict)
// 2. Data Preparation
spot = 532.0
termDates = [2026.02.20, 2026.02.26, 2026.03.30, 2026.04.29, 2026.05.28, 2026.06.29, 2026.09.29, 2026.12.30]
// Matrices are ensured to be dense (no zeros) by Python preprocessing
callPrices = matrix(
    [102.240, 92.250, 82.270, 72.300, 62.360, 52.480, 42.710, 33.180, 24.170, 15.940, 9.000, 4.600, 2.130, 0.960, 0.370, 0.130, 0.050, 0.020, 0.010, 0.010],
    [102.480, 92.530, 82.620, 72.750, 62.980, 53.350, 43.970, 35.430, 26.800, 19.250, 12.390, 8.200, 5.010, 3.030, 1.710, 0.940, 0.490, 0.250, 0.130, 0.070],
    [105.350, 94.410, 84.930, 75.670, 66.690, 59.800, 50.880, 41.900, 34.080, 29.030, 23.600, 18.700, 14.700, 11.470, 8.880, 7.000, 5.320, 4.000, 2.990, 2.220],
    [107.770, 96.450, 87.340, 78.510, 70.000, 61.880, 55.250, 46.990, 41.510, 34.530, 29.120, 24.370, 20.000, 16.900, 13.980, 11.410, 9.320, 7.760, 6.500, 5.320],
    [109.270, 97.890, 89.050, 80.500, 72.290, 64.460, 57.080, 50.140, 45.000, 38.800, 33.130, 28.330, 24.220, 20.630, 17.580, 14.840, 12.540, 10.560, 8.850, 7.440],
    [110.210, 98.620, 90.010, 81.730, 73.930, 66.430, 59.420, 52.930, 47.380, 42.070, 36.780, 32.290, 28.310, 24.260, 21.250, 18.380, 15.900, 13.610, 11.710, 10.000],
    [115.610, 107.450, 96.760, 89.450, 82.610, 75.990, 69.870, 63.990, 58.540, 54.680, 49.600, 45.520, 40.960, 36.480, 33.520, 30.130, 27.110, 24.080, 21.680, 19.310],
    [124.400, 116.880, 109.390, 99.560, 92.910, 89.300, 82.750, 77.110, 69.700, 66.470, 61.260, 56.670, 52.370, 48.220, 44.480, 40.740, 37.360, 34.350, 31.340, 28.570]
)
putPrices = matrix(
    [0.010, 0.010, 0.030, 0.050, 0.110, 0.210, 0.460, 0.880, 1.750, 3.450, 6.570, 12.100, 19.820, 28.260, 38.190, 48.020, 58.000, 68.000, 78.000, 88.000],
    [0.050, 0.090, 0.160, 0.290, 0.510, 0.900, 1.480, 2.390, 3.930, 6.260, 10.000, 15.350, 21.820, 30.000, 39.150, 48.500, 58.190, 68.000, 80.340, 88.000],
    [0.560, 0.900, 1.410, 2.140, 3.160, 4.540, 6.360, 8.640, 11.390, 14.720, 18.710, 24.150, 30.180, 37.360, 44.600, 53.900, 61.660, 70.100, 80.340, 88.940],
    [1.310, 1.960, 2.840, 4.000, 5.470, 7.000, 9.210, 11.950, 15.110, 18.850, 23.340, 28.440, 34.710, 41.520, 48.300, 57.590, 64.690, 73.180, 81.860, 90.830],
    [2.860, 3.870, 5.230, 6.730, 8.460, 10.740, 13.480, 16.630, 20.240, 24.470, 29.080, 34.410, 40.600, 47.430, 54.580, 62.650, 70.440, 78.580, 86.920, 95.580],
    [3.790, 5.140, 6.750, 8.680, 10.870, 13.690, 16.300, 19.650, 23.400, 27.920, 32.950, 38.280, 44.180, 50.760, 57.030, 65.510, 73.230, 78.580, 86.920, 97.520],
    [8.130, 10.140, 12.540, 15.140, 17.750, 20.910, 24.310, 28.300, 32.340, 37.020, 42.040, 47.690, 53.480, 60.030, 66.160, 73.900, 80.970, 88.120, 95.810, 101.990],
    [14.020, 15.890, 18.190, 21.170, 24.270, 27.800, 31.600, 35.490, 40.040, 44.910, 49.510, 54.850, 60.560, 67.000, 72.830, 78.360, 84.930, 94.000, 102.120, 109.690]
)
strikes = matrix(
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00],
    [430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00, 510.00, 520.00, 530.00, 540.00, 550.00, 560.00, 570.00, 580.00, 590.00, 600.00, 610.00, 620.00]
)
optionPrices = matrix(
    [0.010, 0.010, 0.030, 0.050, 0.110, 0.210, 0.460, 0.880, 1.750, 3.450, 6.570, 4.600, 2.130, 0.960, 0.370, 0.130, 0.050, 0.020, 0.010, 0.010],
    [0.050, 0.090, 0.160, 0.290, 0.510, 0.900, 1.480, 2.390, 3.930, 6.260, 10.000, 8.200, 5.010, 3.030, 1.710, 0.940, 0.490, 0.250, 0.130, 0.070],
    [0.560, 0.900, 1.410, 2.140, 3.160, 4.540, 6.360, 8.640, 11.390, 14.720, 18.710, 18.700, 14.700, 11.470, 8.880, 7.000, 5.320, 4.000, 2.990, 2.220],
    [1.310, 1.960, 2.840, 4.000, 5.470, 7.000, 9.210, 11.950, 15.110, 18.850, 23.340, 24.370, 20.000, 16.900, 13.980, 11.410, 9.320, 7.760, 6.500, 5.320],
    [2.860, 3.870, 5.230, 6.730, 8.460, 10.740, 13.480, 16.630, 20.240, 24.470, 29.080, 28.330, 24.220, 20.630, 17.580, 14.840, 12.540, 10.560, 8.850, 7.440],
    [3.790, 5.140, 6.750, 8.680, 10.870, 13.690, 16.300, 19.650, 23.400, 27.920, 32.950, 32.290, 28.310, 24.260, 21.250, 18.380, 15.900, 13.610, 11.710, 10.000],
    [8.130, 10.140, 12.540, 15.140, 17.750, 20.910, 24.310, 28.300, 32.340, 37.020, 42.040, 45.520, 40.960, 36.480, 33.520, 30.130, 27.110, 24.080, 21.680, 19.310],
    [14.020, 15.890, 18.190, 21.170, 24.270, 27.800, 31.600, 35.490, 40.040, 44.910, 49.510, 56.670, 52.370, 48.220, 44.480, 40.740, 37.360, 34.350, 31.340, 28.570]
)
payoffTypes = matrix(
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"],
    ["Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Put", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call", "Call"]
)
// 3. Build Dividend Curve (CallPutParity)
// 使用 Call-Put Parity 从期权价格中隐含出分红（股息）曲线
dividendCurve = eqDividendCurveBuilder(
    referenceDate, termDates, "CallPutParity", ,
    callPrices, putPrices, strikes, spot, discountCurve, "Actual365"
)
// 4. Build Volatility Surface (SVI Model)
// 构建波动率曲面
surface = eqVolatilitySurfaceBuilder(
        referenceDate,
        termDates,
        strikes,
        optionPrices,
        payoffTypes,
        spot,
        discountCurve,
        dividendCurve,
        "SVI"
)
// 5. Pricing Test: eqAmericanOptionPricer
optionDict = {
    "productType": "Option",
    "optionType": "AmericanOption",
    "assetType": "EqAmericanOption",
    "notionalCurrency": "HKD",    // price currency
    "notionalAmount": 1,          // 份数
    "strike": 530.0,
    "maturity": 2026.02.24,
    "payoffType": "Call",
    "dayCountConvention": "Actual365",
    "underlying": "00700.HK"
}
instrument = parseInstrument(optionDict)
res = eqAmericanOptionPricer(
        instrument,
        referenceDate,
        spot,
        discountCurve,
        dividendCurve,
        surface,
        setting={"calcDelta": true, "calcGamma": true, "calcVega": true, "calcTheta": true, "calcRho": true, "calcRhoIr": true, "calcRhoDividend": true}
)
print(res)
```

## 产品字段说明

| **字段名** | **类型** | **描述** | **是否必填** |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Option" | 是 |
| optionType | STRING | 固定填 "AmericanOption" | 是 |
| assetType | STRING | 固定填 "EqAmericanOption" | 是 |
| notionalAmount | DOUBLE | 名义本金额 | 是 |
| notionalCurrency | STRING | 名义本金货币，默认为 CNY | 是 |
| instrumentId | STRING | 合约代码，如代码 `TCH250328C0040000`的解读如下：   * `TCH`: 标的为腾讯控股 * `250328`: 到期日为2025年3月28日。 * `C`: 期权类型为认购（Call） * `0040000`: 行权价为400.00港元。 | 否 |
| direction | SRTRING | 买卖方向 Buy Sell，默认为 Buy | 否 |
| maturity | DATE | 到期日 | 是 |
| strike | DOUBLE | 执行利率 | 是 |
| payoffType | STRING | 枚举，可选Call和Put | 是 |
| underlying | STRING | 标的期货合约代码，如 `TCH` | 是 |
| dayCountConvention | STRING | 日期计数惯例, 可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，人民币存款默认为 "CNY\_FR\_007" | 否 |
| dividendCurve | STRING | 定价时参考的股息曲线名称 | 否 |

**相关函数：**parseInstrument、parseMktData、eqDividendCurveBuilder、eqVolatilitySurfaceBuilder
