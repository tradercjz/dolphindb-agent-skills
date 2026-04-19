# floatingRateBondDirtyPrice

## 语法

`floatingRateBondDirtyPrice(settlement, issue, maturity, redemption, spread,
riskFree, calendar, frequency, [basis=1], [convention="Following"])`

## 详情

计算每 100 面值的浮动利率债券（Floating Rate Bond）的含息价格（Dirty Price）。

浮息债的年息票利率（Coupon Rate）不固定，它根据某个基准利率（如 LIBOR、SHIBOR
等）定期调整。浮息债的实际利率通常是基准利率加上一个固定的利差（Spread），该利差在债券发行时确定，并在债券存续期内保持不变。

## 参数

**注意：**如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。所有向量的长度必须一致。

**settlement** DATE 类型标量或向量，表示债券的结算日。

**issue** DATE 类型标量或向量，表示债券的发行日。

**maturity** DATE 类型标量或向量，表示债券的到期日。

**redemption** 数值型标量或向量，表示债券的赎回价格。

**spread** 数值型标量或向量，表示债券的息差。

**riskFree**数值型标量或向量，表示无风险利率。

**calendar** 字符串类型标量或向量，表示使用的市场日历类型，请参阅[交易日历](../../modules/MarketHoliday/mkt_calendar.md#11-%E6%9F%A5%E8%AF%A2%E4%BA%A4%E6%98%93%E6%97%A5%E5%8E%86-getmarketcalendar)。

**frequency** 支持以下两种输入类型：

* INT 标量或向量：表示每年的付息次数，如 1 表示每年付息 1 次；
* DURATION 标量或向量：表示间隔多长时间进行一次付息，如 3M，表示每 3 个月付息一次。

| **可选值** | **含义** |
| --- | --- |
| 1 / 1y | 表示每年付息1次 |
| 2 / 6M | 表示每年付息2次 / 每6个月付息1次 |
| 3 / 4M | 表示每年付息3次 / 每4个月付息1次 |
| 4 / 3M | 表示每年付息4次 / 每3个月付息1次 |
| 6 / 2M | 表示每年付息6次 / 每2个月付息1次 |
| 12 / 1M | 表示每年付息12次 / 每月付息1次 |
| 13 / 4w | 表示每年付息13次 / 每4周付息1次 |
| 26 / 2w | 表示每年付息26次 / 每2周付息1次 |
| 52 / 1w | 表示每年付息52次 / 每周付息1次 |
| 365 / 1d | 表示每年付息365次 / 每天付息1次 |

**basis** 可选参数，整型或 STRING 类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| Basis | 日计数基准 |
| --- | --- |
| 0 / "Thirty360US" | US (NASD) 30/360 |
| 1 / "ActualActual" (默认值) | 实际/实际 |
| 2 / "Actual360" | 实际/360 |
| 3 / "Actual365" | 实际/365 |
| 4 / "Thirty360EU" | 欧洲 30/360 |

**convention** 可选参数，字符串标量或向量，用于指定如何调整落在非工作日的现金流支付日期。可选值为：

* 'Following'：表示选择给定假日后的第一个工作日，默认值；
* 'ModifiedFollowing'：表示选择给定假日后的第一个工作日，除非该工作日属于不同的月份，此时应选择假日前的第一个工作日；
* 'Preceding'：表示选择给定假日前的第一个工作日；
* 'ModifiedPreceding'：表示选择给定假日前的第一个工作日，除非该工作日属于不同的月份，此时应选择假日后的第一个工作日；
* 'Unadjusted'：表示不作调整；
* 'HalfMonthModifiedFollowing'：表示选择给定假日后的第一个工作日，除非该工作日跨越了月中（15日）或月末，此时应选择假日前的第一个工作日；
* 'Nearest'：表示选择离给定假日最近的工作日。如果前一个和后一个工作日距离给定假日同样远，则默认选择后一个工作日。

## 返回值

DOUBLE 类型标量或向量。

## 例子

假设有一张五年期浮息债，发行日为2020年6月9日，到期日为2025年6月9日，交易日为2020年9月15日。其赎回价格为100。市场无风险利率为0.0385，债券息差为-0.0075。付息频率为每季度一次。日计数基准为Actual/Actual。交易日历使用上海证交所（XSHG），不调整非工作日。

```
floatingRateBondDirtyPrice(settlement=2020.09.15, issue=2020.06.09, maturity=2025.06.09, redemption=100.0, spread=-0.0075, riskFree=0.0385, calendar=`XSHG, frequency=3M,convention=`Unadjusted)
// output: 96.8209
```
