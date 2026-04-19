# callableFixedRateBondDirtyPrice

## 语法

`callableFixedRateBondDirtyPrice(settlement, issue, maturity, redemption,
coupon, riskFree, volatility, reversion, type, exerciseDates, exercisePrices,
calendar, frequency, [basis=1], [convention='Following'], [method='HullWhite'],
[kwargs])`

## 详情

计算含权固息债每 100 面值的含息价格。

含权债券（Bonds with Embedded
Options）是一种特殊类型的债券，在其基础债券合约中嵌入了期权（Option），允许债券的发行人或持有人在特定条件下行使某些权利。根据期权的不同，含权债券主要分为可赎回债券（Callable
Bonds）和可回售债券（Putable Bonds）：

* 可赎回债券：赋予债券发行人在债券到期前按特定价格（赎回价格）提前赎回债券的权利。
* 可回售债券：赋予债券持有人在债券到期前按特定价格（回售价格）将债券卖回给发行人的权利。

## 参数

注：

如果输入参数中，部分为标量，其余为向量时，则会将标量当作与向量长度相同，所有元素值等于该标量的向量。所有向量的长度必须一致。若输入参数为数组向量，则其行数必须与其他向量参数的长度相同。

**settlement** DATE 类型标量或向量，表示债券的结算日。

**issue** DATE 类型标量或向量，表示债券的发行日。

**maturity** DATE 类型标量或向量，表示债券的到期日。

**redemption** 数值型标量或向量，表示债券的赎回价格。

**coupon** 数值型标量或向量，表示债券的年息票利率。

**riskFree** 数值标量或向量，表示无风险利率。

**volatility** 数值标量或向量，表示波动率。

**reversion** 数值标量或向量，表示利率的均值回归率。

**type** 字符串类型标量或向量，表示含权债的类型。可选值为：

* 'call'：表示可赎回债券（Callable Bonds）。
* 'put'：表示可回售债券（Putable Bonds）。

**exerciseDates** DATE 类型向量或数组向量，表示约定的提前赎回或回售债券的日期。

**exercisePrices** 数值型向量或数组向量，表示约定的提前赎回或回售债券的价格。

注：

*exercisePrices* 必须与 *exerciseDates* 结构一致。

**calendar** 字符串类型标量或向量，表示使用的市场日历类型，请参阅[交易日历](../../modules/MarketHoliday/mkt_calendar.md)。

**frequency**INT 类型或 Duration 类型的标量或向量，表示年付息频率。可选值为：

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

**basis** 可选参数，整型或字符串类型的标量或向量，表示要使用的日计数基准类型。可选值为：

| **basis** | **日计数基准** |
| --- | --- |
| 0 / 'Thirty360US' | US (NASD) 30/360 |
| 1 / 'ActualActual' (默认值) | 实际/实际 |
| 2 / 'Actual360' | 实际/360 |
| 3 / 'Actual365' | 实际/365 |
| 4 / 'Thirty360EU' | 欧洲 30/360 |

**convention** 可选参数，字符串标量或向量，用于指定如何调整落在非工作日的现金流支付日期。可选值为：

* 'Following'（默认值）：选择给定假日后的第一个工作日；
* 'ModifiedFollowing'：选择给定假日后的第一个工作日。如果该工作日属于不同的月份，则选择假日前的第一个工作日；
* 'Preceding'：选择给定假日前的第一个工作日；
* 'ModifiedPreceding'：选择给定假日前的第一个工作日。如果该工作日属于不同的月份，则选择假日后的第一个工作日;
* 'Unadjusted'：不作调整；
* 'HalfMonthModifiedFollowing'：选择给定假日后的第一个工作日。如果该工作日跨越了月中（15日）或月末，则选择假日前的第一个工作日；
* 'Nearest'：选择离给定假日最近的工作日。如果前后工作日距离相同，则默认选择后一个工作日。

**method** 可选参数，字符串标量，表示使用的估值方法，目前只支持 'HullWhite'， 即使用 Hull–White 模型进行估值。

**kwargs** 可选参数，一个字典，表示估值的其他参数，不同的估值方法有不同的参数要求。具体参数要求如下

* *method* = 'HullWhite' 时，*kwargs* 应包含成员 'timeSteps'，其值是 INT
  类型标量或向量，表示对 Hull–White 模型进行离散化时使用的时间间隔数，默认值为 50。

## 返回值

DOUBLE 类型的标量或向量。

## 例子

现有八年期含权固息债券，发行日期为 2024 年 9 月 16 日，到期日期为 2032 年 9 月 15 日。当前的交易日为 2026 年 8 月 16
日，债券的赎回价格为 100，年息票利率为 2.5%，并且每三个月支付一次利息。合约约定自 2026 年 9 月 15 日起，债券发行人有权每隔三个月以 100
的价格赎回债券。市场无风险利率为 4.65%，波动率为 20%，利率的均值回归率为 6%。该债券采用 Actual/365 日计数基准，非工作日调整方法为
Following，且交易日历为上海证券交易所（XSHG）。计算该债券的含息价格。

```
issue = 2024.09.16
settlement = 2026.08.16
maturity = 2032.09.15

redemption = 100
riskFree = 0.0465
reversion = 0.06
volatility = 0.20

convention = `Following
calendar = `SSE
frequency = 3M
coupon = 0.025
basis = 3

type="call"
callDate = 2026.09.15
exerciseDates = array(DATE, 0);
for (i in 1..24) {
	exerciseDates.append!(callDate)
	callDate = temporalAdd(callDate, frequency, `Null)
}

exercisePrices = take([100.0], 24)

res = callableFixedRateBondDirtyPrice(settlement, issue, maturity, redemption, coupon, riskFree, volatility, reversion, type, exerciseDates, exercisePrices, calendar, frequency, basis, convention)
res
// output:53.603309242600587
```
