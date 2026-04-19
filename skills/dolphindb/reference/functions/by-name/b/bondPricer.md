# bondPricer

首发版本：3.00.4

## 语法

`bondPricer(instrument, pricingDate, discountCurve,
[spreadCurve], [setting])`

## 详情

对债券进行定价，输出净现值（NPV），同时可计算多种风险指标，包括一阶敏感度（Delta）、二阶敏感度（Gamma）以及关键利率久期（Key Rate
Duration）。

## 参数

注意：所有输入向量必须等长，输入标量将自动扩展以匹配其它向量的长度。

**instrument** INSTRUMENT 类型标量或向量，表示需要定价的债券产品。不同类型的债券产品所需的关键字段各不相同，详见债券[产品字段要求](#topic_nsv_2k2_ngc)。

**pricingDate** DATE 类型标量或向量，表示定价日期。

**discountCurve** MKTDATA 类型标量或向量（IrYieldCurve），表示贴现曲线。贴现曲线所需包含的关键字段见[曲线字段要求](#topic_o4f_fk2_ngc)。

**spreadCurve** 可选参数，MKTDATA 类型标量或向量（IrYieldCurve），表示信用利差曲线。若未提供，则默认使用 0%
利率的平坦曲线。利差曲线所需包含的关键字段见[曲线字段要求](#topic_o4f_fk2_ngc)。

**setting** 可选参数，字典（Dictionary<STRING, ANY>），用于定价设置，包括以下键值对：

| 键 | 值类型 | 描述 |
| --- | --- | --- |
| "calcDiscountCurveDelta" | BOOL | 是否计算债券对贴现曲线的一阶敏感度 |
| "calcDiscountCurveGamma" | BOOL | 是否计算债券对贴现曲线的二阶敏感度 |
| "calcDiscountCurveKeyRateDuration" | BOOL | 是否计算债券的关键利率久期 |
| "discountCurveShift" | DOUBLE 标量 | 贴现曲线的平行扰动，比如一个 bp(0.0001) |
| "discountCurveKeyTerms" | DOUBLE 标量或向量 | 关键期限年数，比如 [1.0, 3.0, 5.0] |
| "discountCurveKeyShifts" | DOUBLE 标量或向量 | 关键期限的扰动幅度, 与 discountCurveKeyTerms 等长，比如 [0.0001, 0.0002, 0.0015] |

## 返回值

若输入为标量：

* 若未指定 *setting*，返回 NPV（DOUBLE 类型标量）。
* 若指定 *setting*，返回 Dictionary<STRING, ANY>，键为指标名称，值为相应结果：

  + "npv"：DOUBLE 标量
  + "discountCurveDelta"：DOUBLE 标量
  + "discountCurveGamma"：DOUBLE 标量
  + "discountCurveKeyRateDuration"：DOUBLE 向量

若输入为向量，返回 DOUBLE 类型向量（若未指定 *setting*）或字典组成的元组（若指定 *setting*）。

## 例子

```
bond = {
  "productType": "Cash",
  "assetType": "Bond",
  "bondType": "FixedRateBond",
  "version": 0,
  "instrumentId": "240025.IB",
  "start": 2024.12.25,
  "maturity": 2031.12.25,
  "issuePrice": 100.0,
  "coupon": 0.0149,
  "frequency": "Annual",
  "dayCountConvention": "ActualActualISDA"
}

pricingDate = 2025.08.18

curve = {
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
  "dates":[2025.09.18, 2025.11.18, 2026.02.18, 2026.08.18, 2027.08.18, 2028.08.18, 2030.08.18,
      2032.08.18, 2035.08.18, 2040.08.18, 2045.08.18, 2055.08.18,2065.08.18, 2075.08.18],
  "values":[1.3000, 1.3700, 1.3898, 1.3865, 1.4299, 1.4471, 1.6401,
       1.7654, 1.7966, 1.9930, 2.1834, 2.1397, 2.1987, 2.2225] / 100.0
}

instrument = parseInstrument(bond)
discountCurve = parseMktData(curve)

setting = dict(STRING, ANY)
setting["calcDiscountCurveDelta"] = true
setting["calcDiscountCurveGamma"] = true
setting["calcDiscountCurveKeyRateDuration"] = true
setting["discountCurveShift"] = 0.0001
setting["discountCurveKeyTerms"] = [1.0, 3.0, 5.0]
setting["discountCurveKeyShifts"] = [0.0002, 0.0003, 0.0001]

bondPricer(instrument, pricingDate, discountCurve, setting=setting)

bondPricer([instrument, instrument], pricingDate, discountCurve, setting=setting)
bondPricer(instrument, pricingDate, [discountCurve, discountCurve], setting=setting)
bondPricer(instrument, [pricingDate], discountCurve, setting=setting)
bondPricer(instrument, [pricingDate, pricingDate], discountCurve, setting=setting)
```

**相关函数：**parseInstrument, parseMktData

## 债券产品字段要求

贴现债

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "DiscountBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 否 |
| instrumentId | STRING | 债券代码，如 "259926.IB" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| issuePrice | DOUBLE | 发行价格 | 是 |
| currency | STRING | 货币，默认为 "CNY" | 否 |
| cashFlow | TABLE | 债券现金流表 | 否 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，如 "CNY\_TRASURY\_BOND" | 否 |
| spreadCurve | STRING | 定价时参考的利差曲线名称 | 否 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+" | 否 |

**零息债**

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "ZeroCouponBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 否 |
| instrumentId | STRING | 债券代码，如 "250401.IB" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| coupon | DOUBLE | 票面利率，如 0.03 表示 3% | 是 |
| frequency | STRING | 付息频率 | 否 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| currency | STRING | 货币，默认为 "CNY" | 否 |
| cashFlow | TABLE | 债券现金流表 | 否 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，如 "CNY\_TRASURY\_BOND" | 否 |
| spreadCurve | STRING | 定价时参考的利差曲线名称 | 否 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+" | 否 |

**固定利率债**

| 字段名 | 类型 | 描述 | 是否必填 |
| --- | --- | --- | --- |
| productType | STRING | 固定填 "Cash" | 是 |
| assetType | STRING | 固定填 "Bond" | 是 |
| bondType | STRING | 固定填 "FixedRateBond" | 是 |
| nominal | DOUBLE | 名义金额，默认值 100 | 否 |
| instrumentId | STRING | 债券代码，如 "250401.IB" | 否 |
| start | DATE | 起息日 | 是 |
| maturity | DATE | 到期日 | 是 |
| coupon | DOUBLE | 票面利率，如0.03表示3% | 是 |
| frequency | STRING | 付息频率 | 是 |
| dayCountConvention | STRING | 日期计数惯例，可选 "ActualActualISDA", "ActualActualISMA", "Actual365", "Actual360" | 是 |
| currency | STRING | 货币，默认为 "CNY" | 否 |
| cashFlow | TABLE | 债券现金流表 | 否 |
| discountCurve | STRING | 定价时参考的贴现曲线名称，如 "CNY\_TRASURY\_BOND" | 否 |
| spreadCurve | STRING | 定价时参考的利差曲线名称 | 否 |
| subType | STRING | 债券子类型，中国债券可选值为：   * "TREASURY\_BOND"：国债 * "CENTRAL\_BANK\_BILL"：央行票据 * "CDB\_BOND"：政策性金融债（国开） * "EIBC\_BOND"：政策性金融债（进出口行） * "ADBC\_BOND"：政策性金融债（农发行）。 * "MTN"：中期票据 * "CORP\_BOND"：企业债。 * "UNSECURED\_CORP\_BOND"：无担保企业债 * "SHORT\_FIN\_BOND"：短期融资券 * "NCD"：同业存单 * "LOC\_GOV\_BOND"：地方政府债 * "COMM\_BANK\_FIN\_BOND"：商业银行普通金融债 * "BANK\_SUB\_CAP\_BOND"：商业银行二级资本债 * "ABS"：资产支持证券 * "PPN"：非公开发行债 | 否 |
| creditRating | STRING | 信用等级类型，可选值为："B", "BB", "BBB", "BBB+", "A-", "A", "A+", "AA-", "AA", "AA+", "AAA-", "AAA", "AAA+" | 否 |

## 曲线字段要求

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
| curveModel | STRING | 曲线构建模型，可选值为 "Bootstrap"（默认），"NS"，"NSS"。  当取值 "NSS" 或 "NS"，无需传 *interpMethod*、*extrapMethod*、*dates*、*values*字段。 | 否 |
| curveParams | DICT | 模型的参数，当 *curveModel*取值 "NSS" 或 "NS" 时必填：   * curveModel = "NS"：应包含键 'beta0', 'beta1', 'beta2',   'lambda' * curveModel = "NSS"：应包含键'beta0', ‘beta1', 'beta2',   'beta3', 'lambda0', 'lambda1' | 否 |
