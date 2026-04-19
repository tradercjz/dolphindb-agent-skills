# fxEuropeanOptionPricer

首发版本：3.00.4

## 语法

`fxEuropeanOptionPricer(instrument, pricingDate, spot,
domesticCurve, foreignCurve, volSurf, [setting])`

## 详情

使用 BlackScholes Model 和 Analytic Method，对外汇欧式期权进行定价，返回期权的净现值（NPV）。

## 参数

注意：所有输入向量必须等长，输入标量将自动扩展以匹配其它向量的长度。

**instrument** INSTRUMENT 类型标量或向量，表示待定价的外汇欧式期权。外汇欧式期权所需的关键字段详见[产品字段要求](#topic_sp5_5xj_ngc)。

**pricingDate** DATE 类型标量或向量，表示定价日期。

**spot** 数值类型标量或向量，表示标的汇率的即期价格。

**domesticCurve** MKTDATA 类型标量或向量（IrYieldCurve），表示本币的折现曲线。曲线所需包含的关键字段见[曲线字段要求](#topic_ldg_vxj_ngc)。

**foreignCurve** MKTDATA 类型标量或向量（IrYieldCurve），表示外币的折现曲线。曲线所需包含的关键字段见[曲线字段要求](#topic_ldg_vxj_ngc)。

**volSurf** MKTDATA 类型标量或向量（FxVolatilitySurface），表示外汇期权波动率曲面。曲线所需包含的关键字段见[曲线字段要求](#topic_ldg_vxj_ngc)。

**setting** 可选参数，一个字典，用于设置定价输出。包含以下 key：

* **calcDelta**：value 为布尔值，指定是否计算 delta。
* **calcGamma**：value 为布尔值，指定是否计算 gamma。
* **calcVega**：value 为布尔值，指定是否计算 vega。
* **calcTheta**：value 为布尔值，指定是否计算 theta。
* **calcRhoDomestic**：value 为布尔值，指定是否计算 domestic rho。
* **calcRhoForeign**：value 为布尔值，指定是否计算 foreign rho。

## 返回值

DOUBLE 类型标量或向量。

## 例子

```
pricingDate = 2025.08.18
ccyPair = "USDCNY"

option = {
    "productType": "Option",
    "optionType": "EuropeanOption",
    "assetType": "FxEuropeanOption",
    "notionalCurrency": "USD",
    "notionalAmount": 1E6,
    "strike": 7.2,
    "maturity": 2025.10.28,
    "payoffType": "Call",
    "dayCountConvention": "Actual365",
    "underlying": ccyPair
}

quoteTerms = ['1d', '1w', '2w', '3w', '1M', '2M', '3M', '6M', '9M', '1y', '18M', '2y', '3y']
quoteNames = ["ATM", "D25_RR", "D25_BF", "D10_RR", "D10_BF"]
quotes = [0.030000, -0.007500, 0.003500, -0.010000, 0.005500,
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
          0.044750,  0.006250, 0.003400,  0.009000, 0.008550]
quotes = reshape(quotes, size(quoteNames):size(quoteTerms)).transpose()

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

spot = 7.1627
instrument = parseInstrument(option)
domesticCurve = parseMktData(domesticCurveInfo)
foreignCurve = parseMktData(foreignCurveInfo)
surf = fxVolatilitySurfaceBuilder(pricingDate, ccyPair, quoteNames, quoteTerms, quotes, spot, domesticCurve, foreignCurve)

fxEuropeanOptionPricer(instrument, pricingDate, spot, domesticCurve, foreignCurve, surf)   // output: 1693.9919
fxEuropeanOptionPricer([instrument, instrument], pricingDate, spot, domesticCurve, foreignCurve, surf)
fxEuropeanOptionPricer(instrument, [pricingDate, pricingDate], spot, domesticCurve, foreignCurve, surf)
fxEuropeanOptionPricer(instrument, pricingDate, [spot, spot], domesticCurve, foreignCurve, surf)
fxEuropeanOptionPricer(instrument, pricingDate, spot, [domesticCurve, domesticCurve], foreignCurve, surf)
fxEuropeanOptionPricer(instrument, pricingDate, spot, domesticCurve, [foreignCurve, foreignCurve], surf)
fxEuropeanOptionPricer(instrument, pricingDate, spot, domesticCurve, foreignCurve, [surf, surf])
```

**相关函数：**parseInstrument, parseMktData

## 产品字段说明

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "UserDefined" | 是 |

## 曲线字段要求

**IrYieldCurve**

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| mktDataType | STRING | 固定填 "Curve" | 是 |
| referenceDate | DATE | 参考日期 | 是 |
| curveType | STRING | 固定填 "IrYieldCurve" | 是 |
| dayCountConvention | STRING | 曲线的日期计数惯例，可选值为：   * "Actual360"：实际天数除以360 * "Actual365"：实际天数除以365（不区分闰年） * "ActualActualISMA"：实际天数/实际天数（ISMA规则） * "ActualActualISDA"：实际天数/实际天数（ISDA规则） | 是 |
| interpMethod | STRING | 内插方法，可选值为：   * "Linear"：线性插值 * "CubicSpline"：三次样条插值 * "CubicHermiteSpline"：三次埃尔米特样条插值 | 是 |
| extrapMethod | STRING | 外插方法，可选值为：   * "Flat"：平插 * "Linear"：线性插值 | 是 |
| dates | DATE 向量 | 数据点的日期 | 是 |
| values | DOUBLE 向量 | 数据点的值，与 *dates* 中的元素一一对应 | 是 |
| curveName | STRING | 曲线名称 | 否 |
| currency | STRING | 货币，可选值为"CNY", "USD", "EUR", "GBP", "JPY", "HKD" | 是 |
| compounding | STRING | 复利类型，可选值为：   * "Simple"：单利 * "Compounded"：离散复利 * "Continuous"：连续复利 | 是 |
| settlement | DATE | 结算日，如果指定了结算日，则后续期限间隔的计算都将从 *settlement* 开始，而不是 *referenceDate* | 否 |
| frequency | INTEGRAL或 STRING | 计息频率，可选值为：   * -1 或 "NoFrequency"：无效计息频率 * 0 或 "Once"：到期一次还本付息 * 1 或 "Annual"：每年付息一次 * 2 或 "Semiannual"：每半年付息一次 * 3 或 "EveryFourthMonth"：每四个月付息一次 * 4 或 "Quarterly"：每季度付息一次 * 6 或 "BiMonthly"：每两月付息一次 * 12 或 "Monthly"：每月付息一次 * 13 或 "EveryFourthWeek"：每四周付息一次 * 26 或 "BiWeekly"：每两周付息一次 * 52 或 "Weekly"：每周付息一次 * 365 或 "Daily"：每日付息一次 * 999 或 "Other"：其他计息频率 | 否 |
| curveModel | STRING | 曲线构建模型，目前仅支持 "Bootstrap"。 | 否 |
| curveParams | DICT | 模型的参数。 | 否 |

**FxVolatilitySurface**

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| mktDataType | STRING | 固定填 "Surface" | 是 |
| referenceDate | DATE | 参考日期 | 是 |
| surfaceType | STRING | 固定填 "FxVolatilitySurface" | 是 |
| smileMethod | STRING | 波动率微笑方法，可选值为：   * "Linear"：线性微笑 * "CubicSpline"：三次样条微笑 * "SVI"：SVI 模型微笑 * "SABR"：SABR 模型微笑 | 是 |
| volSmiles | DICT(STRING, ANY) 向量 | 波动率微笑向量，向量中每个元素为一条波动率微笑。  包含以下成员：   * **strikes**: DOUBLE 类型向量，表示不同的行权价 * **vols**: DOUBLE 类型向量，表示行权价对应的波动率，与   *strikes*等长 * **curveParams**：字典DICT(STRING,   DOUBLE)类型，表示波动率微笑方法的模型参数，只在 *smileMethod* 取值   "SVI" 或 "SABR" 时生效：    + smileMethod = 'SVI': 应包含键 'a', 'b', 'rho', 'm',     'sigma'   + smileMethod = 'SABR': 应包含键 'alpha', 'beta',     'rho', 'nu' * **fwd**：可选，DOUBLE 类型标量，当 *smileMethod*取值   "SVI" 或 "SABR" 时必填，表示远期值 | 是 |
| termDates | DATE 向量 | *volSmiles*中每条波动率微笑对应的期限日期 | 是 |
| surfaceName | STRING | 曲面名称 | 否 |
| currencyPair | STRING | 外汇的货币对，可选值为"EURUSD", "USDCNY", "EURCNY", "GBPCNY", "JPYCNY", "HKDCNY"。  货币对的表示也可由 `.` 或 `/` 分隔，例如 "EURUSD" 也可写为 "EUR.USD" 或 "EUR/USD"。 | 是 |
