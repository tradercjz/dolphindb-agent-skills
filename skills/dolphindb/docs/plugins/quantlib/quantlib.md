<!-- Auto-mirrored from upstream `documentation-main/plugins/quantlib/quantlib.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# QuantLib

[QuantLib](https://www.quantlib.org)是一个开源的金融计算库，用于执行复杂的定量金融分析和衍生品定价。其由
C++编写，为用户提供了广泛的金融工具和功能。为方便使用，现基于该库为用户提供 DolphinDB 的 QuantLib 插件。用户可在 DolphinDB
中调用该库的大多函数接口。

## 安装插件

### 版本要求

DolphinDB Server 2.00.14 及更高版本，支持 Linux x64、Windows x64。

### 安装步骤

1. 在 DolphinDB 客户端中使用 `listRemotePlugins` 命令查看插件仓库中的插件信息。

   注意：仅展示当前操作系统和 server 版本支持的插件。若无预期插件，可自行编译或在 [DolphinDB 用户社区](https://ask.dolphindb.net/)进行反馈。

   ```
   login("admin", "123456")
   listRemotePlugins()
   ```
2. 使用 `installPlugin` 命令完成插件安装。

   ```
   installPlugin("QuantLib")
   ```
3. 用 `loadPlugin`
   命令加载插件。

   ```
   loadPlugin("QuantLib")
   ```

## 函数接口

### Basic

#### Linear

**语法：**

`Linear()`

**描述：**

线性插值方法。

**示例：**

```
linear = QuantLib::Linear()
```

#### Period

**语法：**

`Period(n|Frequency,
[units])`

**参数：**

**frequency** String 标量，对应
QuantLib 的 Frequency 元素的字符串，如 "NoFrequency"，"Once"，"Annual"
等。

或

**n** Int 标量，表示数量。

**units** String 标量，对应
QuantLib 的 TimeUnit 类型，如 "Days"，"Weeks"，"Months"
等。

**描述：**

用于表示时间间隔。

**示例：**

```
p1 = QuantLib::Period("Annual");
p2 = QuantLib::Period(1, "Years");
```

#### Schedule

**语法：**

`Schedule(effectiveDate,
terminationDate, tenor, calendar, convention, terminationDateConvention,
rule, endOfMonth)`

**参数：**

**effectiveDate** Date 标量或
Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**terminationDate**
Date 标量或 Int 标量。

**tenor** Period 类型句柄。

**calendar**
Calendar 类型句柄。

**convention** String 标量，对应 QuantLib 的
BusinessDayConvention 类型，如 "Following"，"ModifiedFollowing"
等。

**terminationDateConvention** String 标量，对应 QuantLib 的
BusinessDayConvention 类型，如 "Following"，"ModifiedFollowing"
等。

**rule** String 标量，对应 DateGeneration 的 Rule 类型，如
"Backward"，"Forward" 等。

**endOfMonth**
布尔标量，用于控制生产日期序列时，是否保持月末对齐（End-of-Month rule）。

**描述：**

返回一个
Schedule
类型对象。Schedule（时间表）是一个常用的数据类型或数据结构，用于表示一系列日期或时间点。这些日期或时间点通常用于描述金融合约、支付日期、重置日期等与时间相关的事件。

**示例：**

```
use QuantLib

issue_date = 2015.01.15
maturity_date = 2016.01.15
tenor = Period("Semiannual")
calendar = UnitedStates("NYSE")
month_end = false
schedule = Schedule(issue_date, maturity_date, tenor, calendar,
              "Unadjusted", "Unadjusted", "Backward", month_end)
```

### Setting

#### getSettingsInstance

**语法：**

`getSettingsInstance()`

**描述：**

返回
SettingsInstance 类型对象，用于管理 QuantLib 的一些全局设置，与 QuantLib-Python 中的
ql.Settings.instance()
作用相同。

**示例：**

```
s = QuantLib::getSettingsInstance()
```

#### SettingsInstance::getStringOfEvaluationDate

**语法：**

`getStringOfEvaluationDate()`

**描述：**

getStringOfEvaluationDate
是 SettingsInstance 的成员函数，等价于 QuantLib-Python 的
ql.Settings.instance().evaluationDate().ISO()。

**示例：**

```
use QuantLib
s = getSettingsInstance().getStringOfEvaluationDate()
```

#### SettingsInstance::setEvaluationDate

**语法：**

`setEvaluationDate(date)`

**参数：**

**date**
Date 类型或 Int 类型标量。如果是 Int 标量则会用这个值构造 QuantLib 的 Date
类型。

**描述：**

setEvaluationDate 是 SettingsInstance 的成员函数，等价于
QuantLib-Python 的 ql.Settings.instance().evaluationDate =
date

**示例：**

```
use QuantLib
getSettingsInstance().setEvaluationDate(2014.03.07);
```

### Quote

#### SimpleQuote

**语法：**

`SimpleQuote(value)`

**参数：**

**value**
Double 标量。

**描述：**

返回一个 SimpleQuote
类型对象。

**示例：**

```
s = QuantLib::SimpleQuote(0.20);
```

#### QuoteHandle

**语法：**

`QuoteHandle(simpleQuote)`

**参数：**

**simpleQuote** Quote 类型句柄。

**描述：**

返回一个 QuoteHandle 类型对象。

**示例：**

```
use QuantLib

s = SimpleQuote(100.0);
q = QuoteHandle(s);
```

### Currency

#### CNYCurrency

**语法：**

`CNYCurrency()`

**描述：**

返回一个
CNYCurrency
类型对象。

**示例：**

```
c = QuantLib::CNYCurrency();
```

### Index

#### IborIndex

**语法：**

`IborIndex(familyName,
tenor, settlementDays, currency, fixingCalendar, convention, endOfMonth,
dayCounter, h)`

**参数：**

**familyName** String
标量。

**tenor** Period 类型句柄。

**settlementDays** Int
类型标量。

**currency** Currency 类型句柄。

**fixingCalendar**
Calendar 类型句柄。

**convention** String 标量，对应 QuantLib 的
BusinessDayConvention 类型，如 "Following"，"ModifiedFollowing"
等。

**endOfMonth** Bool 标量。

**dayCounter**
DayCounter 类型句柄。

**h** YieldTermStructureHandle
类型句柄。

**描述：**

返回一个 IborIndex
类型对象。

**示例：**

```
use QuantLib

today = 2023.07.18
getSettingsInstance().setEvaluationDate(today)

// Schedule Setting
settlementDays = 0
faceAmount = 100.0

effectiveDate = 2020.06.09
terminationDate = 2025.06.09
tenor = Period("Quarterly")

calendar = China("IB")
convention = "Unadjusted"
terminationDateConvention = convention
rule = "Backward"
endOfMonth = false

schedule = Schedule(
    effectiveDate,
    terminationDate,
    tenor,
    calendar,
    convention,
    terminationDateConvention,
    rule,
    endOfMonth)

nextLpr = 3.55 / 100.0
nextLprQuote = SimpleQuote(nextLpr)
nextLprHandle = QuoteHandle(nextLprQuote)
fixedLpr = 3.85 / 100.0

compounding = "Compounded"
frequency = "Quarterly"
accrualDayCounter = ActualActual("Bond", schedule)
cfDayCounter = ActualActual("Bond")
paymentConvention = "Unadjusted"

cfLprTermStructure = YieldTermStructureHandle(
      FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        cfDayCounter,
        compounding,
        frequency))

lpr3m = IborIndex(
    'LPR1Y',
    Period(3, "Months"),
    settlementDays,
    CNYCurrency(),
    calendar,
    convention,
    endOfMonth,
    cfDayCounter,
    cfLprTermStructure)
```

**IborIndex::addFixing**

```
use QuantLib

// lpr3m 和其他缺少的变量的构建见 IborIndex 函数的示例

fixedLpr = 3.85 / 100.0
lpr3m.addFixing(2020.06.08, fixedLpr)
```

**IborIndex::clearFixings**

```
use QuantLib

// lpr3m 和其他缺少的变量的构建见 IborIndex 函数的示例

lpr3m.clearFixings()
```

**IborIndex::fixing**

```
use QuantLib
// lpr3m 和其他缺少的变量的构建见 IborIndex 函数的示例
lpr3m.fixing(2023.06.08)
```

### InterestRate

#### InterestRate

**语法：**

`InterestRate(rate,
dayCounter, compounding, frequency)`

**参数：**

**rate**
Double 标量。

**dayCounter** DayCounter 句柄，如 Actual360，Actual365Fixed
等。

**compounding** String 标量，对应 QuantLib 的 Compounding，如 "Simple",
"Compounded" 等。

**frequency** String 标量，对应 QuantLib 的 Frequency，如
"NoFrequency", "Once"
等。

**描述：**

这个类封装了利率复利代数。它管理日计数约定、复利约定、不同约定之间的转换、贴现/复利因子计算以及隐含/等效利率计算。

**示例：**

```
use QuantLib
rate = InterestRate(0.05, Actual360(), "Compounded", "Annual");
```

#### InterestRate::discountFactor

**语法：**

`discountFactor(t)`

或

`discountFactor(d1,
d2)`

**参数：**

**t** Double 标量。

或

**d1**
date 标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**d2** date
标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**描述：**

在时刻
t 处计算 discountFactor，或者在 d1 和 d2 两个日期计算
discountFactor。

**示例：**

```
use QuantLib
InterestRate(0.05, Actual360(), "Compounded", "Annual").discountFactor(367,109574);
```

#### InterestRate::compoundFactor

**语法：**

`compoundFactor(t)`

或

`compoundFactor(d1,
d2)`

**参数：**

**t** Double 标量。

或

**d1**
date 标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**d2** date
标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**描述：**

在时刻
t 处计算 compoundFactor，或者在 d1 和 d2 两个日期计算
compoundFactor。

**示例：**

```
use QuantLib
InterestRate(0.05, Actual360(), "Compounded", "Annual").compoundFactor(367,109574);
```

#### InterestRate::rate

**语法：**

`rate()`

**描述：**

返回
InterestRate 对象的
rate。

**示例：**

```
use QuantLib
InterestRate(0.05, Actual360(), "Compounded", "Annual").rate();
```

#### InterestRate::dayCounter

**语法：**

`dayCounter()`

**描述：**

返回
InterestRate 对象的
dayCounter。

**示例：**

```
use QuantLib
InterestRate(0.05, Actual360(), "Compounded", "Annual").dayCounter();
```

#### InterestRate::compounding

**语法：**

`compounding()`

**描述：**

返回
InterestRate 对象的
compounding。

**示例：**

```
use QuantLib
InterestRate(0.05, Actual360(), "Compounded", "Annual").compounding();
```

#### InterestRate::frequency

**语法：**

`frequency()`

**描述：**

返回
InterestRate 对象的
frequency。

**示例：**

```
use QuantLib
InterestRate(0.05, Actual360(), "Compounded", "Annual").frequency();
```

### CashFlow

#### SimpleCashFlow

**语法：**

`SimpleCashFlow(amount,
date)`

**参数：**

**amount** Double 标量。

**date**
Date 标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date
类型。

**描述：**

预定现金流，这种现金流在特定日期支付预先确定的金额。

**示例：**

```
s = QuantLib::SimpleCashFlow(105.0, 2020.06.15);
```

#### Redemption

**语法：**

`Redemption(amount,
date)`

**参数：**

**amount** Double
标量。

**date** Date 标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date
类型。

**描述：**

债券赎回，这个类专门处理简单现金流，以便访问者可以执行更详细的现金流分析。

**示例：**

```
r = QuantLib::Redemption(105.0, 2020.06.15);
```

#### AmortizingPayment

**语法：**

`AmortizingPayment(amount,
date)`

**参数：**

**amount** Double 标量。

**date**
Date 标量或 Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date
类型。

**描述：**

摊还付款，这个类专门处理简单现金流，以便访问者可以执行更详细的现金流分析。

**示例：**

```
a = QuantLib::AmortizingPayment(105.0, 2020.06.15);
```

### Coupon

#### FixedRateCoupon

**语法：**

`FixedRateCoupon(paymentDate,
nominal, rate, dayCounter, accrualStartDate,
accrualEndDate)`

**参数：**

**paymentDate** Date 标量或
Int 标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**nominal** Double
标量。

**rate** Double 标量。

**dayCounter** DayCounter 句柄，如
Actual360，Actual365Fixed 等。

**accrualStartDate** Date 标量或 Int
标量。

**accrualEndDate** Date 标量或 Int
标量。

**描述：**

固定利率的票息支付。

**示例：**

```
use QuantLib

amount = 105.0;
nominal = 100.0;
paymentDate = 2020.06.15;
startDate = 2019.12.15;
rate = 0.05;
dayCounter = Actual360();
coupon = FixedRateCoupon(paymentDate, nominal, rate, dayCounter, startDate, paymentDate);
```

#### IborCoupon

**语法：**

`IborCoupon(paymentDate, nominal,
startDate, endDate, fixingDays,
index)`

**参数：**

**paymentDate** Date 标量或 Int
标量，如果是 Int 标量则会用这个值构造 QuantLib 的 Date 类型。

**nominal** Double
标量。

**startDate** Date 标量或 Int 标量。

**endDate** Date 标量或
Int 标量。

**fixingDays** Int 标量。

**index** String 标量，对应
QuantLib 的 IborIndex 类型，如 "EuriborSW()"，"Euribor2W()"
等。

**描述：**

Libor
类型指数的票息支付。

**示例：**

```
use QuantLib

nominal = 100.0;
startDate = 2020.12.15
endDate = 2021.06.15
rate = 0.05;
dayCounter = Actual360();
index = "Euribor6M()";
coupon = IborCoupon(endDate, nominal, startDate, endDate, 2, index);
```

### Calendar

#### TARGET

**语法：**

`TARGET()`

**描述：**

TARGET
Calendar
类型。

**示例：**

```
t = QuantLib::TARGET()
```

#### UnitedStates

**语法：**

`UnitedStates(market)`

**参数：**

**market**
String 标量，对应 UnitedStates 的 Market 类型，如 "Settlement"，"NYSE"
等。

**描述：**

UnitedStates Calendar
类型。

**示例：**

```
c = QuantLib::UnitedStates("NYSE");
```

#### China

**语法：**

`China(market)`

**参数：**

**market**
String 标量，对应 China 的 Market 类型，如 "SSE"，"IB"
等。

**描述：**

China Calendar
类型。

**示例：**

```
c = QuantLib::China("IB");
```

**DayCounter**

#### Actual360

**语法：**

`Actual360([includeLastDay
= false])`

**参数：**

**includeLastDay** Bool
标量。

**描述：**

返回 Actual360
类型对象。

**示例：**

```
dayCounter = QuantLib::Actual360();
```

#### Actual365Fixed

**语法：**

`Actual365Fixed([convention
= "Standard"])`

**参数：**

**convention** String
标量，对应 Actual365Fixed 的 Convention 类型，如 "Standard"，"Canadian"
等。

**描述：**

返回 Actual365
类型对象。

**示例：**

```
dayCounter = QuantLib::Actual365Fixed("Standard");
```

#### Actual366

**语法：**

`Actual366([includeLastDay =
false])`

**参数：**

**includeLastDay** Bool
标量。

**描述：**

返回 Actual366
类型对象。

**示例：**

```
dayCounter = QuantLib::Actual366();
```

#### ActualActual

**语法：**

`ActualActual(convention,
[schedule])`

**参数：**

**convention** String 标量，对应
ActualActual 的 Convention 类型，如 "ISMA"，"Bond" 等。

**schedule**
Schedule 类型句柄，可选参数。

**描述：**

返回 ActualActual
类型对象。

**示例：**

```
dayCounter = QuantLib::ActualActual("ISMA");
```

#### OneDayCounter

**语法：**

`OneDayCounter()`

**描述：**

返回
OneDayCounter
类型对象。

**示例：**

```
dayCounter = QuantLib::OneDayCounter();
```

#### SimpleDayCounter

**语法：**

`SimpleDayCounter()`

**描述：**

返回
SimpleDayCounter
类型对象。

**示例：**

```
dayCounter = QuantLib::SimpleDayCounter();
```

#### Thirty365

**语法：**

`Thirty365()`

**描述：**

返回
Thirty365
类型对象。

**示例：**

```
dayCounter = QuantLib::Thirty365();
```

#### Thirty360

**语法：**

`Thirty360(convention,
[terminationDate])`

**参数：**

**convention** String
标量，对应 Thirty360 的 Convention 类型，如 "USA"，"BondBasis"
等。

**terminationDate** Date 标量或 Int 标量，如果是 Int 标量则会用这个值构造
QuantLib 的 Date 类型，是可选参数。

**描述：**

返回 Thirty360
类型对象。

**示例：**

```
dayCounter = QuantLib::Thirty360("USA");
```

### PayOff

#### PlainVanillaPayoff

**语法：**

`PlainVanillaPayoff(type,strike)`

**参数：**

**type**
String 标量，对应 QuantLib Option 的 Type 类型 ，如 "Put"，"Call"
等。

**strike** Double 类型标量。

**描述：**

返回
PlainVanillaPayoff
类型对象。

**示例：**

```
use QuantLib

option_type = "Call";
strike = 100.0;
payoff = PlainVanillaPayoff(option_type, strike);
```

### Exercise

#### EuropeanExercise

**语法：**

`EuropeanExercise(date)`

**参数：**

**date**
Date 标量或 Int 标量。

**描述：**

返回 EuropeanExercise
类型对象，欧式期权只能在一个（到期）日期行使。

**示例：**

```
use QuantLib
date = 2016.01.15;
exercise = EuropeanExercise(date);
```

### Bond

#### FixedRateBond

**语法：**

`FixedRateBond(settlementDays,
faceAmount, schedule, coupons,
accrualDayCounter)`

**参数：**

**settlementDays** Int
标量。

**faceAmount** Double 标量。

**schedule** Schedule
类型句柄。

**coupons** Double 向量。

**accrualDayCounter**
DayCounter 类型句柄。

**描述：**

返回一个 FixedRateBond
类型对象，表示固定利率债券。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
```

#### FixedRateBond::setPricingEngine

**语法：**

`setPricingEngine(pricingEngine)`

**参数：**

**pricingEngine**
DiscountingBondEngine
类型句柄。

**描述：**

设置定价引擎。

**示例：**

```
use QuantLib
spot_dates = [2015.01.15, 2015.07.15, 2016.01.15]
spot_rates = [0.0, 0.005, 0.007]
day_count = Thirty360("BondBasis")
calendar = UnitedStates("NYSE")
interpolation = Linear()
compounding = "Compounded"
compounding_frequency = "Annual"
spot_curve = ZeroCurve(spot_dates, spot_rates, day_count, calendar,
                    interpolation, compounding, compounding_frequency)
spot_curve_handle = YieldTermStructureHandle(spot_curve)

issue_date = 2015.01.15
maturity_date = 2016.01.15
tenor = Period("Semiannual")
calendar = UnitedStates("NYSE")
month_end = false
schedule = Schedule(issue_date, maturity_date, tenor, calendar,
              "Unadjusted", "Unadjusted", "Backward", month_end)

coupon_rate = 0.06
coupons = [coupon_rate]
settlement_days = 0
face_value = 100.0
fixed_rate_bond = FixedRateBond(settlement_days, face_value, schedule, coupons, day_count)

bond_engine = DiscountingBondEngine(spot_curve_handle)
fixed_rate_bond.setPricingEngine(bond_engine)
```

#### FixedRateBond::NPV

**语法：**

`NPV()`

**描述：**

计算
NPV。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的示例
fixed_rate_bond.setPricingEngine(bond_engine)

getSettingsInstance().setEvaluationDate(2015.01.15)
fixed_rate_bond.NPV()
```

#### FixedRateBond::settlementDate

**语法：**

`settlementDate()`

**描述：**

计算
settlementDate。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的示例
fixed_rate_bond.setPricingEngine(bond_engine)

getSettingsInstance().setEvaluationDate(2015.01.15)
fixed_rate_bond.settlementDate()
```

#### FixedRateBond::maturityDate

**语法：**

`maturityDate()`

**描述：**

计算
maturityDate。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的示例
fixed_rate_bond.setPricingEngine(bond_engine)

getSettingsInstance().setEvaluationDate(2015.01.15)
fixed_rate_bond.maturityDate()
```

#### FixedRateBond::cleanPrice

**语法：**

`cleanPrice()`

**描述：**

计算
cleanPrice。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的示例
fixed_rate_bond.setPricingEngine(bond_engine)

getSettingsInstance().setEvaluationDate(2015.01.15)
fixed_rate_bond.cleanPrice()
```

#### FixedRateBond::dirtyPrice

**语法：**

`dirtyPrice()`

**描述：**

计算
dirtyPrice。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的示例
fixed_rate_bond.setPricingEngine(bond_engine)

getSettingsInstance().setEvaluationDate(2015.01.15)
fixed_rate_bond.dirtyPrice()
```

#### FixedRateBond::accruedAmount

**语法：**

`accruedAmount()`

**描述：**

计算
accruedAmount。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的示例
fixed_rate_bond.setPricingEngine(bond_engine)

getSettingsInstance().setEvaluationDate(2015.01.15)
fixed_rate_bond.accruedAmount()
```

#### FixedRateBond::getBondYield

**语法：**

`getBondYield(dayCounter, compounding, frequency)`

**参数：**

**dayCounter** DayCounter 类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如 "Simple",
"Compounded" 等。

**frequency** String 标量，对应 QuantLib 的 Frequency，如 "NoFrequency", "Once"
等。

**描述：**

计算 bondYield。

**示例：**

```
use QuantLib
// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的Examples
fixed_rate_bond.setPricingEngine(bond_engine)
getSettingsInstance().setEvaluationDate(2015.01.15)
bondYield = fixed_rate_bond.getBondYield(day_count, compounding, compounding_frequency)
```

#### FixedRateBond::cashflows

**语法：**

`cashflows()`

**描述：**

返回内含多个
cashflows 的 Resource 类型对象，支持 getDate 和 amount
方法，以向量形式返回结果。

**示例：**

```
use QuantLib
// fixed_rate_bond 和其他缺少的变量的构建见 FixedRateBond::setPricingEngine 的Examples
fixed_rate_bond.setPricingEngine(bond_engine)
getSettingsInstance().setEvaluationDate(2015.01.15)
cfs = fixed_rate_bond.cashflows()
print(cfs.getDate())
print(cfs.amount())
```

#### FloatingRateBond

**语法：**

`FloatingRateBond(settlementDays,
faceAmount, schedule, iborIndex, accrualDayCounter, paymentConvention,
fixingDays, gearings,
spreads)`

**参数：**

**settlementDays** Int
标量。

**faceAmount Double** 标量。

**schedule Schedule**
类型句柄。

**iborIndex** IborIndex 类型句柄。

**accrualDayCounter**
DayCounter 类型句柄。

**paymentConvention** String 标量，对应 QuantLib 的
BusinessDayConvention 类型，如 "Following"，"ModifiedFollowing"
等。

**fixingDays** Int 标量。

**gearings** Double
向量。

**spreads** Double 向量。

**描述：**

返回
FloatingRateBond
类型对象。

**示例：**

```
use QuantLib

settlementDays = 0
faceAmount = 100.0

effectiveDate = 2020.06.09
terminationDate = 2025.06.09
tenor = Period("Quarterly")

calendar = China("IB")
convention = "Unadjusted"
terminationDateConvention = convention
rule = "Backward"
endOfMonth = false

schedule = Schedule(
    effectiveDate,
    terminationDate,
    tenor,
    calendar,
    convention,
    terminationDateConvention,
    rule,
    endOfMonth)

nextLpr = 3.55 / 100.0
nextLprQuote = SimpleQuote(nextLpr)
nextLprHandle = QuoteHandle(nextLprQuote)
fixedLpr = 3.85 / 100.0

compounding = "Compounded"
frequency = "Quarterly"
accrualDayCounter = ActualActual("Bond", schedule)
cfDayCounter = ActualActual("Bond")
paymentConvention = "Unadjusted"

cfLprTermStructure = YieldTermStructureHandle(
      FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        cfDayCounter,
        compounding,
        frequency))

lpr3m = IborIndex(
    'LPR1Y',
    Period(3, "Months"),
    settlementDays,
    CNYCurrency(),
    calendar,
    convention,
    endOfMonth,
    cfDayCounter,
    cfLprTermStructure)

lpr3m.addFixing(2020.06.08, fixedLpr)
lpr3m.addFixing(2020.09.08, fixedLpr)
lpr3m.addFixing(2020.12.08, fixedLpr)

lpr3m.addFixing(2021.03.08, fixedLpr)
lpr3m.addFixing(2021.06.08, fixedLpr)
lpr3m.addFixing(2021.09.08, fixedLpr)
lpr3m.addFixing(2021.12.08, fixedLpr)

lpr3m.addFixing(2022.03.08, 3.7/100)
lpr3m.addFixing(2022.06.08, 3.7/100)
lpr3m.addFixing(2022.09.08, 3.65/100)
lpr3m.addFixing(2022.12.08, 3.65/100)

lpr3m.addFixing(2023.03.08, 3.65/100)
lpr3m.addFixing(2023.06.08, 3.65/100)

fixingDays = 1
gearings = [1.0]
benchmarkSpread = [ -0.75 / 100.0]
bond = FloatingRateBond(settlementDays, faceAmount, schedule, lpr3m, accrualDayCounter, convention, fixingDays, gearings, benchmarkSpread)
```

#### FloatingRateBond::setPricingEngine

**语法：**

`setPricingEngine(pricingEngine)`

**参数：**

**pricingEngine**
PricingEngine 类型句柄。

**描述：**

FloatingRateBond
类型的成员函数，用于设置定价引擎。

**示例：**

```
use QuantLib

// bond 和其他缺少的变量的构建见 FloatingRateBond 的示例

getSettingsInstance().setEvaluationDate(2023.07.18)

lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)

zeroSpreadedTermStructure = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
zeroSpreadedTermStructure.enableExtrapolation()

zeroSpreadedTermStructureHandle = YieldTermStructureHandle(zeroSpreadedTermStructure)
engine = DiscountingBondEngine(zeroSpreadedTermStructureHandle)

bond.setPricingEngine(engine)
```

#### FloatingRateBond::NPV

**语法：**

`NPV()`

**描述：**

计算
NPV。

**示例：**

```
use QuantLib

// bond 和其他缺少的变量的构建见 FloatingRateBond 的示例

getSettingsInstance().setEvaluationDate(2023.07.18)

lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)

zeroSpreadedTermStructure = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
zeroSpreadedTermStructure.enableExtrapolation()

zeroSpreadedTermStructureHandle = YieldTermStructureHandle(zeroSpreadedTermStructure)
engine = DiscountingBondEngine(zeroSpreadedTermStructureHandle)

bond.setPricingEngine(engine)
bond.NPV()
```

#### FloatingRateBond::cleanPrice

**语法：**

`cleanPrice()`

**描述：**

计算
cleanPrice。

**示例：**

```
use QuantLib

// bond 和其他缺少的变量的构建见 FloatingRateBond 的示例

getSettingsInstance().setEvaluationDate(2023.07.18)

lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)

zeroSpreadedTermStructure = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
zeroSpreadedTermStructure.enableExtrapolation()

zeroSpreadedTermStructureHandle = YieldTermStructureHandle(zeroSpreadedTermStructure)
engine = DiscountingBondEngine(zeroSpreadedTermStructureHandle)

bond.setPricingEngine(engine)
bond.cleanPrice()
```

#### FloatingRateBond::dirtyPrice

**语法：**

```
dirtyPrice()

lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)

zeroSpreadedTermStructure = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
zeroSpreadedTermStructure.enableExtrapolation()

zeroSpreadedTermStructureHandle = YieldTermStructureHandle(zeroSpreadedTermStructure)
engine = DiscountingBondEngine(zeroSpreadedTermStructureHandle)

bond.setPricingEngine(engine)
bond.dirtyPrice()
```

**描述：**

计算 dirtyPrice。

**示例：**

```
use QuantLib

// bond 和其他缺少的变量的构建见 FloatingRateBond 的示例

getSettingsInstance().setEvaluationDate(2023.07.18)
```

#### FloatingRateBond::accruedAmount

**语法：**

`accruedAmount([date])`

**参数：**

**date**
Int 或 Date 标量，是可选参数。

**描述：**

计算
accruedAmount。

**示例：**

```
use QuantLib

// bond 和其他缺少的变量的构建见 FloatingRateBond 的示例

getSettingsInstance().setEvaluationDate(2023.07.18)

lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)

zeroSpreadedTermStructure = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
zeroSpreadedTermStructure.enableExtrapolation()

zeroSpreadedTermStructureHandle = YieldTermStructureHandle(zeroSpreadedTermStructure)
engine = DiscountingBondEngine(zeroSpreadedTermStructureHandle)

bond.setPricingEngine(engine)
bond.accruedAmount()
```

#### FloatingRateBond::cashflows

**语法：**

`cashflows()`

**描述：**

返回内含多个
cashflows 的 Resource 类型对象，支持 getDate 和 amount
方法，以向量形式返回结果。

**示例：**

```
use QuantLib
// bond 和其他缺少的变量的构建见 FloatingRateBond 的Examples
getSettingsInstance().setEvaluationDate(2023.07.18)
lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))
bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)
zeroSpreadedTermStructure = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
zeroSpreadedTermStructure.enableExtrapolation()
zeroSpreadedTermStructureHandle = YieldTermStructureHandle(zeroSpreadedTermStructure)
engine = DiscountingBondEngine(zeroSpreadedTermStructureHandle)
bond.setPricingEngine(engine)
cfs = bond.cashflows()
print(cfs.getDate())
print(cfs.amount())
```

#### getBondFunctions

**语法：**

`getBondFunctions()`

**描述：**

返回
BondFunctions 类型对象，用于调用 QuantLib 的 BondFunctions，与 QuantLib-Python 中的
ql.BondFunctions
作用相同。

**示例：**

```
bondFunctions = QuantLib::getBondFunctions()
```

#### BondFunctions::getDuration

**语法：**

`getDuration(bond,
yield)`

或

`getDuration(bond, yield, dayCounter,
compounding, frequency, [type])`

**参数：**

**bond** Bond
类型句柄。

**yield** InterestRate 类型句柄。

或

**bond** Bond
类型句柄。

**yield** Double 标量。

**dayCounter** DayCounter
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等。

**frequency** String 标量，对应 QuantLib 的
Frequency，如 "NoFrequency", "Once" 等。

**type** String 标量，对应 Duration
的 Type，如 "Simple"，"Macaulay" 等，是可选参数。

**描述：**

计算
duration。

**示例：**

```
use QuantLib

day_count = Thirty360("BondBasis")
calendar = UnitedStates("NYSE")
compounding = "Compounded"
compounding_frequency = "Annual"
spot_curve = ZeroCurve([2015.01.15, 2015.07.15, 2016.01.15], [0.0, 0.005, 0.007], day_count, calendar,
                    Linear(), compounding, compounding_frequency)
spot_curve_handle = YieldTermStructureHandle(spot_curve)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), calendar,
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], day_count)

fixed_rate_bond.setPricingEngine(DiscountingBondEngine(spot_curve_handle))
bondYield = fixed_rate_bond.getBondYield(day_count, compounding, compounding_frequency)
getSettingsInstance().setEvaluationDate(2015.01.15)

getBondFunctions().getDuration(fixed_rate_bond, bondYield, day_count, compounding, compounding_frequency)
```

#### BondFunctions::convexity

**语法：**

`convexity(bond,
yield)`

或

`convexity(bond, yield, dayCounter,
compounding, frequency)`

**参数：**

**bond** Bond
类型句柄。

**yield** InterestRate 类型句柄。

或

**bond** Bond
类型句柄。

**yield** Double 标量。

**dayCounter** DayCounter
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等。

**frequency** String 标量，对应 QuantLib 的
Frequency，如 "NoFrequency", "Once" 等。

**描述：**

计算
convexity。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 BondFunctions::getDuration 的示例

fixed_rate_bond.setPricingEngine(DiscountingBondEngine(spot_curve_handle))
bondYield = fixed_rate_bond.getBondYield(day_count, compounding, compounding_frequency)
getSettingsInstance().setEvaluationDate(2015.01.15)

getBondFunctions().convexity(fixed_rate_bond, bondYield, day_count, compounding, compounding_frequency)
```

#### BondFunctions::basisPointValue

**语法：**

`basisPointValue(bond,
yield)`

或

`basisPointValue(bond, yield, dayCounter,
compounding, frequency)`

**参数：**

**bond** Bond
类型句柄。

**yield** InterestRate 类型句柄。

或

**bond** Bond
类型句柄。

**yield** Double 标量。

**dayCounter** DayCounter
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等。

**frequency** String 标量，对应 QuantLib 的
Frequency，如 "NoFrequency", "Once" 等。

**描述：**

计算
basisPointValue。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 BondFunctions::getDuration 的示例

fixed_rate_bond.setPricingEngine(DiscountingBondEngine(spot_curve_handle))
bondYield = fixed_rate_bond.getBondYield(day_count, compounding, compounding_frequency)
getSettingsInstance().setEvaluationDate(2015.01.15)

getBondFunctions().basisPointValue(fixed_rate_bond, bondYield, day_count, compounding, compounding_frequency)
```

#### BondFunctions::bps

**语法：**

`bps(bond,
yield)`

或

`bps(bond,
discountCurve)`

或

`bps(bond, yield, dayCounter,
compounding, frequency)`

**参数：**

**bond** Bond
类型句柄。

**yield** InterestRate 类型句柄。

或

**bond** Bond
类型句柄。

**discountCurve** YieldTermStructure
类型句柄。

或

**bond** Bond 类型句柄。

**yield** Double
标量。

**dayCounter** DayCounter 类型句柄。

**compounding** String
标量，对应 QuantLib 的 Compounding，如 "Simple", "Compounded"
等。

**frequency** String 标量，对应 QuantLib 的 Frequency，如
"NoFrequency", "Once" 等。

**描述：**

计算
bps。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 BondFunctions::getDuration 的示例

fixed_rate_bond.setPricingEngine(DiscountingBondEngine(spot_curve_handle))
bondYield = fixed_rate_bond.getBondYield(day_count, compounding, compounding_frequency)
getSettingsInstance().setEvaluationDate(2015.01.15)

getBondFunctions().bps(fixed_rate_bond, bondYield, day_count, compounding, compounding_frequency)
```

#### BondFunctions::yieldValueBasisPoint

**语法：**

`yieldValueBasisPoint(bond,
yield) 或 yieldValueBasisPoint(bond, yield, dayCounter, compounding,
frequency)`

**参数：**

**bond** Bond
类型句柄。

**yield** InterestRate 类型句柄。

或

**bond**
Bond 类型句柄。

**yield** Double 标量。

**dayCounter** DayCounter
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等。

**frequency** String 标量，对应 QuantLib 的
Frequency，如 "NoFrequency", "Once" 等。

**描述：**

计算
yieldValueBasisPoint。

**示例：**

```
use QuantLib

// fixed_rate_bond 和其他缺少的变量的构建见 BondFunctions::getDuration 的示例

fixed_rate_bond.setPricingEngine(DiscountingBondEngine(spot_curve_handle))
bondYield = fixed_rate_bond.getBondYield(day_count, compounding, compounding_frequency)
getSettingsInstance().setEvaluationDate(2015.01.15)

getBondFunctions().yieldValueBasisPoint(fixed_rate_bond, bondYield, day_count, compounding, compounding_frequency)
```

#### BondFunctions::startDate

**语法：**

`startDate(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

获取
startDate。

**示例：**

```
use QuantLib
schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().startDate(fixed_rate_bond)
```

#### BondFunctions::maturityDate

**语法：**

`maturityDate(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

获取
maturityDate。

**示例：**

```
use QuantLib
schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().maturityDate(fixed_rate_bond)
```

#### BondFunctions::isTradable

**语法：**

`isTradable(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

获取
isTradable。

**示例：**

```
use QuantLib
schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().isTradable(fixed_rate_bond)
```

#### BondFunctions::previousCouponRate

**语法：**

`previousCouponRate(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
previousCouponRate。

**示例：**

```
use QuantLib
schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().previousCouponRate(fixed_rate_bond)
```

#### BondFunctions::nextCouponRate

**语法：**

`nextCouponRate(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
nextCouponRate。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().nextCouponRate(fixed_rate_bond)
```

#### BondFunctions::accrualStartDate

**语法：**

`accrualStartDate(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accrualStartDate。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accrualStartDate(fixed_rate_bond)
```

#### BondFunctions::accrualEndDate

**语法：**

`accrualEndDate(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accrualEndDate。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accrualEndDate(fixed_rate_bond)
```

#### BondFunctions::accrualPeriod

**语法：**

`accrualPeriod(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accrualPeriod。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accrualPeriod(fixed_rate_bond)
```

#### BondFunctions::accrualDays

**语法：**

`accrualDays(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accrualDays。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accrualDays(fixed_rate_bond)
```

#### BondFunctions::accruedPeriod

**语法：**

`accruedPeriod(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accruedPeriod。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accruedPeriod(fixed_rate_bond)
```

#### BondFunctions::accruedDays

**语法：**

`accruedDays(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accruedDays。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accruedDays(fixed_rate_bond)
```

#### BondFunctions::accruedAmount

**语法：**

`accruedAmount(bond)`

**参数：**

**bond**
Bond 类型句柄。

**描述：**

计算
accruedAmount。

**示例：**

```
use QuantLib
calc_date = 2015.01.15
getSettingsInstance().setEvaluationDate(calc_date)

schedule = Schedule(2015.01.15, 2016.01.15, Period("Semiannual"), UnitedStates("NYSE"),
              "Unadjusted", "Unadjusted", "Backward", false)
fixed_rate_bond = FixedRateBond(0, 100.0, schedule, [0.06], Thirty360("BondBasis"))
getBondFunctions().accruedAmount(fixed_rate_bond)
```

#### BondFunctions::previousCashFlowDate

**语法：**

`previousCashFlowDate(bond,
date)`

**参数：**

**bond** Bond 类型句柄。

**date**
Date 标量。

**描述：**

计算
previousCashFlowDate。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
print(getBondFunctions().previousCashFlowDate(bond, 2020.12.15))
```

#### BondFunctions::previousCashFlowAmount

**语法：**

`previousCashFlowAmount(bond,
date)`

**参数：**

**bond** Bond 类型句柄。

**date**
Date 标量。

**描述：**

计算
previousCashFlowAmount。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
print(getBondFunctions().previousCashFlowAmount(bond, 2020.12.15))
```

#### BondFunctions::nextCashFlowDate

**语法：**

`nextCashFlowDate(bond,
date)`

**参数：**

**bond** Bond 类型句柄。

**date**
Date 标量。

**描述：**

计算
nextCashFlowDate。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
print(getBondFunctions().nextCashFlowDate(bond, 2020.12.15))
```

#### BondFunctions::nextCashFlowAmount

**语法：**

`nextCashFlowAmount(bond,
date)`

**参数：**

**bond** Bond 类型句柄。

**date**
Date 标量。

**描述：**

计算
nextCashFlowAmount。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
print(getBondFunctions().nextCashFlowAmount(bond, 2020.12.15))
```

#### BondFunctions::cleanPrice

**语法：**

`cleanPrice(bond,
discountCurve) 或 cleanPrice(bond,
yield)`

**参数：**

**bond** Bond
类型句柄。

**discountCurve** YieldTermStructure
类型句柄。

或

**bond** Bond 类型句柄。

**yield**
InterestRate 类型句柄。

**描述：**

计算
cleanPrice。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
rate = InterestRate(0.05, Actual360(), "Compounded", "Annual")
print(getBondFunctions().cleanPrice(bond, rate))
```

#### BondFunctions::atmRate

**语法：**

`atmRate(bond,
discountCurve)`

**参数：**

**bond** Bond
类型句柄。

**discountCurve** YieldTermStructure
类型句柄。

**描述：**

计算
atmRate。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
crv = FlatForward(2, TARGET(), 0.04, Actual360())
print(getBondFunctions().atmRate(bond, crv))
```

#### BondFunctions::zSpread

**语法：**

`zSpread(bond,
cleanPrice, yieldTermStructure, dayCounter, compounding,
frequency)`

**参数：**

**bond** Bond
类型句柄。

**cleanPrice** Double 标量。

**yieldTermStructure**
YieldTermStructure 类型句柄。

**dayCounter** DayCounter
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等。

**frequency** String 标量，对应 QuantLib 的
Frequency，如 "NoFrequency", "Once" 等。

**描述：**

计算
zSpread。

**示例：**

```
use QuantLib
s = Schedule(2019.12.15, 2024.12.15, Period(1, "Years"), TARGET(), "Unadjusted", "Unadjusted", "Backward", false)
bond = FixedRateBond(2, 100.0, s, [0.05], ActualActual("Bond"))
crv = FlatForward(2, TARGET(), 0.04, Actual360())
print(getBondFunctions().zSpread(bond, 101.0, crv, Actual360(), "Compounded", "Annual"))
```

### Option

#### EuropeanOption

**语法：**

`EuropeanOption(payoff,
exercise)`

**参数：**

**payoff** StrikedTypePayoff
类型句柄。

**exercise** Exercise 类型句柄。

**描述：**

返回一个
EuropeanOption
类型对象。

**示例：**

```
use QuantLib
option = EuropeanOption(PlainVanillaPayoff("Call",100.0),EuropeanExercise(2014.06.07));
```

#### EuropeanOption::setPricingEngine

**语法：**

`setPricingEngine(pricingEngine)`

**参数：**

**pricingEngine**
PricingEngine 类型句柄。

**描述：**

EuropeanOption
类型的成员函数，用于设置定价引擎。

**示例：**

```
use QuantLib

today=2014.03.07;
getSettingsInstance().setEvaluationDate(today);

option = EuropeanOption(PlainVanillaPayoff("Call",100.0),EuropeanExercise(2014.06.07));

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
engine = AnalyticEuropeanEngine(process);

option.setPricingEngine(engine);
```

#### EuropeanOption::NPV

**语法：**

`NPV()`

**描述：**

EuropeanOption
类型的成员函数，用于计算 NPV（Net Present
Value）值。

**示例：**

```
use QuantLib

today=2014.03.07;
getSettingsInstance().setEvaluationDate(today);

option = EuropeanOption(PlainVanillaPayoff("Call",100.0),EuropeanExercise(2014.06.07));

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
engine = AnalyticEuropeanEngine(process);

option.setPricingEngine(engine);
option.NPV();
```

#### EuropeanOption::delta

**语法：**

`delta()`

**描述：**

EuropeanOption
类型的成员函数，用于计算 Delta
值。

**示例：**

```
use QuantLib

today=2014.03.07;
getSettingsInstance().setEvaluationDate(today);

option = EuropeanOption(PlainVanillaPayoff("Call",100.0),EuropeanExercise(2014.06.07));

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
engine = AnalyticEuropeanEngine(process);

option.setPricingEngine(engine);
option.delta();
```

#### EuropeanOption::gamma

**语法：**

`gamma()`

**描述：**

EuropeanOption
类型的成员函数，用于计算 gamma
值。

**示例：**

```
today=2014.03.07;
getSettingsInstance().setEvaluationDate(today);

option = EuropeanOption(PlainVanillaPayoff("Call",100.0),EuropeanExercise(2014.06.07));

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
engine = AnalyticEuropeanEngine(process);

option.setPricingEngine(engine);
option.gamma();
```

#### EuropeanOption::vega

**语法：**

`vega()`

**描述：**

EuropeanOption
类型的成员函数，用于计算 vega
值。

**示例：**

```
use QuantLib

today=2014.03.07;
getSettingsInstance().setEvaluationDate(today);

option = EuropeanOption(PlainVanillaPayoff("Call",100.0),EuropeanExercise(2014.06.07));

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
engine = AnalyticEuropeanEngine(process);

option.setPricingEngine(engine);
option.vega();
```

#### BarrierOption

**语法：**

`BarrierOption(barrierType,
barrier, rebate, payoff,
exercise)`

**参数：**

**barrierType** String 标量，对应
Barrier 的 Type，如 "DownIn"，"UpIn" 等。

**barrier** Double
标量。

**rebate** Double 标量。

**payoff** StrikedTypePayoff
类型句柄。

**exercise** Exercise
类型句柄。

**描述：**

障碍期权。

**示例：**

```
use QuantLib

option_type = "Put"
strike = 1.10
barrier_type = "DownOut"
barrier = 1.05
payoff_amt = 1000000.0
trade_dt = 2023.07.20
settle_dt = 2023.07.22
expiry_dt = 2023.07.24
delivery_dt = 2023.07.27

spot_quote = SimpleQuote(1.12)
vol_atm_quote = SimpleQuote(12.48 / 100)
eur_depo_quote = SimpleQuote(0.72 / 100)
usd_depo_quote = SimpleQuote(3.85 / 100)

domesticTS = FlatForward(0, UnitedStates("Settlement"), QuoteHandle(eur_depo_quote), Actual360())
foreignTS = FlatForward(0, UnitedStates("Settlement"),  QuoteHandle(usd_depo_quote), Actual360())
expanded_volTS = BlackConstantVol(0, UnitedStates("Settlement"), QuoteHandle(vol_atm_quote), Actual360())

payoff = PlainVanillaPayoff(option_type, strike)
exercise = EuropeanExercise(expiry_dt)
option = BarrierOption(barrier_type, barrier, 0.0, payoff, exercise)
```

#### BarrierOption::setPricingEngine

**语法：**

`setPricingEngine(pricingEngine)`

**参数：**

**pricingEngine**
DiscountingBondEngine
类型句柄。

**描述：**

设置定价引擎。

**示例：**

```
use QuantLib

// option 和其他缺少的变量的构建见 BarrierOption 函数的示例

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
analyticBarrierEngine = AnalyticBarrierEngine(process)
option.setPricingEngine(analyticBarrierEngine)
```

#### BarrierOption::NPV

**语法：**

`NPV()`

**描述：**

计算
NPV。

**示例：**

```
use QuantLib

// option 和其他缺少的变量的构建见 BarrierOption 函数的示例

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
analyticBarrierEngine = AnalyticBarrierEngine(process)
option.setPricingEngine(analyticBarrierEngine)

getSettingsInstance().setEvaluationDate(2023.07.20)
option.NPV()
```

#### BarrierOption::delta

**语法：**

`delta()`

**描述：**

计算
delta。

**示例：**

```
use QuantLib

// option 和其他缺少的变量的构建见 BarrierOption 函数的示例

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
fdBarrierEngine = FdBlackScholesBarrierEngine(process)
option.setPricingEngine(fdBarrierEngine)

getSettingsInstance().setEvaluationDate(2023.07.20)
option.delta()
```

#### BarrierOption::gamma

**语法：**

`gamma()`

**描述：**

计算
gamma。

**示例：**

```
use QuantLib

// option 和其他缺少的变量的构建见 BarrierOption 函数的示例

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
fdBarrierEngine = FdBlackScholesBarrierEngine(process)
option.setPricingEngine(fdBarrierEngine)

getSettingsInstance().setEvaluationDate(2023.07.20)
option.gamma()
```

### PricingEngine

#### AnalyticEuropeanEngine

**语法：**

`AnalyticEuropeanEngine(process)`

**参数：**

**process**
GeneralizedBlackScholesProcess
类型句柄。

**描述：**

欧式普通期权的定价引擎。

**示例：**

```
loadPlugin("path_to_plugin/PluginQuantLib.txt")
use QuantLib

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
engine = AnalyticEuropeanEngine(process);
```

#### BinomialBarrierEngine

**语法：**

`BinomialBarrierEngine(process,
type, timeSteps)`

**参数：**

**process**
GarmanKohlagenProcess 类型句柄。

**type** String 标量，目前只支持 "crr" 代表
CoxRossRubinstein 型。

**timeSteps** Int
标量。

**描述：**

BinomialBarrierEngine
类型定价引擎。

**示例：**

```
use QuantLib
spot_quote = SimpleQuote(1.12)
eur_depo_quote = SimpleQuote(0.72 / 100)
usd_depo_quote = SimpleQuote(3.85 / 100)
vol_atm_quote = SimpleQuote(12.48 / 100)

foreignTS = FlatForward(0, UnitedStates("Settlement"),  QuoteHandle(usd_depo_quote), Actual360())
domesticTS = FlatForward(0, UnitedStates("Settlement"), QuoteHandle(eur_depo_quote), Actual360())
expanded_volTS = BlackConstantVol(0, UnitedStates("Settlement"), QuoteHandle(vol_atm_quote), Actual360())

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
binomialEngine = BinomialBarrierEngine(process, "crr", 200)
```

#### FdBlackScholesBarrierEngine

**语法：**

`FdBlackScholesBarrierEngine(process)`

**参数：**

**process**
GarmanKohlagenProcess
类型句柄。

**描述：**

FdBlackScholesBarrierEngine
类型定价引擎。

**示例：**

```
use QuantLib
spot_quote = SimpleQuote(1.12)
eur_depo_quote = SimpleQuote(0.72 / 100)
usd_depo_quote = SimpleQuote(3.85 / 100)
vol_atm_quote = SimpleQuote(12.48 / 100)

foreignTS = FlatForward(0, UnitedStates("Settlement"),  QuoteHandle(usd_depo_quote), Actual360())
domesticTS = FlatForward(0, UnitedStates("Settlement"), QuoteHandle(eur_depo_quote), Actual360())
expanded_volTS = BlackConstantVol(0, UnitedStates("Settlement"), QuoteHandle(vol_atm_quote), Actual360())

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
fdBlackScholesBarrierEngine = FdBlackScholesBarrierEngine(process)
```

#### AnalyticBarrierEngine

**语法：**

`AnalyticBarrierEngine(process)`

**参数：**

**process**
GarmanKohlagenProcess 类型句柄。

**描述：**

AnalyticBarrierEngine
类型定价引擎。

**示例：**

```
use QuantLib
spot_quote = SimpleQuote(1.12)
eur_depo_quote = SimpleQuote(0.72 / 100)
usd_depo_quote = SimpleQuote(3.85 / 100)
vol_atm_quote = SimpleQuote(12.48 / 100)

foreignTS = FlatForward(0, UnitedStates("Settlement"),  QuoteHandle(usd_depo_quote), Actual360())
domesticTS = FlatForward(0, UnitedStates("Settlement"), QuoteHandle(eur_depo_quote), Actual360())
expanded_volTS = BlackConstantVol(0, UnitedStates("Settlement"), QuoteHandle(vol_atm_quote), Actual360())

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
analyticBarrierEngine = AnalyticBarrierEngine(process)
```

#### DiscountingBondEngine

**语法：**

`DiscountingBondEngine(discountCurve)`

**参数：**

**discountCurve**
YieldTermStructureHandle 类型句柄。

**描述：**

DiscountingBondEngine
类型定价引擎。

**示例：**

```
use QuantLib
spot_dates = [2015.01.15, 2015.07.15, 2016.01.15]
spot_rates = [0.0, 0.005, 0.007]
day_count = Thirty360("BondBasis")
calendar = UnitedStates("NYSE")
interpolation = Linear()
compounding = "Compounded"
compounding_frequency = "Annual"
spot_curve = ZeroCurve(spot_dates, spot_rates, day_count, calendar,
                    interpolation, compounding, compounding_frequency)
spot_curve_handle = YieldTermStructureHandle(spot_curve)

issue_date = 2015.01.15
maturity_date = 2016.01.15
tenor = Period("Semiannual")
calendar = UnitedStates("NYSE")
month_end = false
schedule = Schedule(issue_date, maturity_date, tenor, calendar,
              "Unadjusted", "Unadjusted", "Backward", month_end)

coupon_rate = 0.06
coupons = [coupon_rate]
settlement_days = 0
face_value = 100.0
fixed_rate_bond = FixedRateBond(settlement_days, face_value, schedule, coupons, day_count)

bond_engine = DiscountingBondEngine(spot_curve_handle)
```

### Process

#### BlackScholesProcess

**语法：**

`BlackScholesProcess(x0,
riskFreeTS, blackVolTS)`

**参数：**

**x0** QuoteHandle
类型句柄。

**riskFreeTS** YieldTermStructureHandle
类型句柄。

**blackVolTS** BlackVolTermStructureHandle
类型句柄。

**描述：**

返回一个 BlackScholesProcess
类型对象。

**示例：**

```
use QuantLib

u = SimpleQuote(100.0);
r = SimpleQuote(0.01);
sigma = SimpleQuote(0.20);

riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());

process = BlackScholesProcess(QuoteHandle(u),
                              YieldTermStructureHandle(riskFreeCurve),
                              BlackVolTermStructureHandle(volatility));
```

#### GarmanKohlagenProcess

**语法：**

`GarmanKohlagenProcess(x0,
foreignRiskFreeTS, domesticRiskFreeTS,
blackVolTermStructureHandle)`

**参数：**

**x0**
QuoteHandle 类型句柄。

**foreignRiskFreeTS** YieldTermStructure
类型句柄。

**domesticRiskFreeTS** YieldTermStructure
类型句柄。

**blackVolTermStructureHandle** BlackVolTermStructure
类型句柄。

**描述：**

返回一个 GarmanKohlagenProcess
类型对象。

**示例：**

```
use QuantLib
domesticTS = FlatForward(0, UnitedStates("Settlement"), QuoteHandle(eur_depo_quote), Actual360())
foreignTS = FlatForward(0, UnitedStates("Settlement"),  QuoteHandle(usd_depo_quote), Actual360())
expanded_volTS = BlackConstantVol(0, UnitedStates("Settlement"), QuoteHandle(vol_atm_quote), Actual360())

payoff = PlainVanillaPayoff(option_type, strike)
exercise = EuropeanExercise(expiry_dt)
option = BarrierOption(barrier_type, barrier, 0.0, payoff, exercise)

process = GarmanKohlagenProcess(QuoteHandle(spot_quote), YieldTermStructureHandle(foreignTS), YieldTermStructureHandle(domesticTS), BlackVolTermStructureHandle(expanded_volTS))
```

### Volatility

#### BlackConstantVol

**语法：**

`BlackConstantVol(referenceDate|settlementDays, calendar, volatility,
dayCounter)`

**参数：**

**referenceDate** Date 标量。

**settlementDays** Int 标量。

**calendar** Calendar 类型句柄。

**volatility** Double 标量或者 QuoteHandle 类型句柄。

**dayCounter** DayCounter 类型句柄。

**描述：**

返回一个 BlackConstantVol 类型对象。

**示例：**

```
use QuantLib

sigma = SimpleQuote(0.20);
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());
```

#### BlackVolTermStructureHandle

**语法：**

`BlackVolTermStructureHandle(blackVolTermStructure)`

**参数：**

**blackVolTermStructure**
BlackVolTermStructure 类型句柄。

**描述：**

返回一个
BlackVolTermStructureHandle
类型对象。

**示例：**

```
use QuantLib

sigma = SimpleQuote(0.20);
volatility = BlackConstantVol(0, TARGET(), QuoteHandle(sigma), Actual360());
BlackVolTermStructureHandle(volatility);
```

### YieldTerm

#### FlatForward

**语法：**

`FlatForward(settlementDays,
calendar, forward, dayCounter, [compounding = "Continuous"], [frequency =
"Annual"])`

**参数：**

**settlementDays** Int
类型标量。

**calendar** Calendar 类型句柄。

**forward**
QuoteHandle 类型句柄或 Double 类型标量。

**dayCounter** DayCounter
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等，可选参数。

**frequency** String 标量，对应 QuantLib
的 Frequency，如 "NoFrequency", "Once"
等，可选参数。

**描述：**

用于表示平坦利率曲线。

**示例：**

```
use QuantLib

r = SimpleQuote(0.01);
riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
```

#### DiscountCurve

**语法：**

`DiscountCurve(dates, dfs,
dayCounter)`

**参数：**

**dates** Date 或 Int
类型的向量。

**dfs** Double 类型向量。

**dayCounter** DayCounter
类型句柄。

**描述：**

返回一个 DiscountCurve
类型对象。

**示例：**

```
use QuantLib

dates = [2019.05.07,2020.05.07,2021.05.07];
dfs = [1.0,0.99,0.98];
dayCounter = Actual360();
curve = DiscountCurve(dates, dfs, dayCounter);
```

#### ZeroCurve

**语法：**

`ZeroCurve(dates, yields,
dayCounter, calendar, linear, [compounding="Continuous"],
[frequency="Annual"])`

**参数：**

**dates** Date 或 Int
类型的向量。

**yields** Double 类型向量。

**dayCounter** DayCounter
类型句柄。

**calendar** Calendar 类型句柄。

**linear** Linear
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded" 等，可选参数。

**frequency** String 标量，对应 QuantLib
的 Frequency，如 "NoFrequency", "Once" 等，可选参数。

**描述：**

返回一个
ZeroCurve
类型对象。

**示例：**

```
use QuantLib

dates = [5000,100000];
yields = [0.24,0.75];
dayCounter = Actual360();
calendar = UnitedStates("NYSE");
linear = Linear();
compounding = "Continuous";
frequency = "Annual";
curve = ZeroCurve(dates, yields, dayCounter, calendar, linear, compounding, frequency);
```

#### ZeroCurve::zeroRate

**语法：**

`zeroRate(date,
dayCounter, compounding, frequency,
[extrapolate])`

**参数：**

**date** Date 或 Int
标量。

**dayCounter** DayCounter 类型句柄。

**compounding** String
标量，对应 QuantLib 的 Compounding，如 "Simple",
"Compounded"。

**frequency** String 标量，对应 QuantLib 的 Frequency，如
"NoFrequency", "Once"。

**extrapolate** Bool
标量，可选参数。

**描述：**

ZeroCurve
类型的成员函数，用于计算零收益率。

**示例：**

```
use QuantLib

dates = [5000,100000];
yields = [0.24,0.75];
dayCounter = Actual360();
calendar = UnitedStates("NYSE");
linear = Linear();
compounding = "Continuous";
frequency = "Annual";

curve = ZeroCurve(dates, yields, dayCounter, calendar, linear, compounding, frequency);

date = 40000;
curve.zeroRate(date,dayCounter,compounding,frequency).rate();
```

#### ZeroSpreadedTermStructure

**语法：**

`ZeroSpreadedTermStructure(yieldTermStructure,
spread, compounding, frequency,
dayCounter)`

**参数：**

**yieldTermStructure**
YieldTermStructure 类型句柄。

**spread** QuoteHandle
类型句柄。

**compounding** String 标量，对应 QuantLib 的 Compounding，如
"Simple", "Compounded"。

**frequency** String 标量，对应 QuantLib 的
Frequency，如 "NoFrequency", "Once"。

**dayCounter** DayCounter
类型句柄。

**描述：**

返回一个 ZeroSpreadedTermStructure
类型的对象。

**示例：**

```
use QuantLib

settlementDays = 0
faceAmount = 100.0

effectiveDate = 2020.06.09
terminationDate = 2025.06.09
tenor = Period("Quarterly")

calendar = China("IB")
convention = "Unadjusted"
terminationDateConvention = convention
rule = "Backward"
endOfMonth = false

schedule = Schedule(
    effectiveDate,
    terminationDate,
    tenor,
    calendar,
    convention,
    terminationDateConvention,
    rule,
    endOfMonth)

nextLpr = 3.55 / 100.0
nextLprQuote = SimpleQuote(nextLpr)
nextLprHandle = QuoteHandle(nextLprQuote)
fixedLpr = 3.85 / 100.0

compounding = "Compounded"
frequency = "Quarterly"
accrualDayCounter = ActualActual("Bond", schedule)
cfDayCounter = ActualActual("Bond")
paymentConvention = "Unadjusted"

lprTermStructure = YieldTermStructureHandle(
    FlatForward(
        settlementDays,
        calendar,
        nextLprHandle,
        accrualDayCounter,
        compounding,
        frequency))

bondYield = 2.35 / 100.0
basisSpread = bondYield - nextLpr
basisSpreadQuote = SimpleQuote(basisSpread)
basisSpreadHandle = QuoteHandle(basisSpreadQuote)

z = ZeroSpreadedTermStructure(lprTermStructure, basisSpreadHandle, compounding, frequency, accrualDayCounter)
```

#### ZeroSpreadedTermStructure::enableExtrapolation

**语法：**

`enableExtrapolation()`

**描述：**

ZeroSpreadedTermStructure
类型的成员函数，用于开启曲线外推。

**示例：**

```
use QuantLib

// z 的构建见 ZeroSpreadedTermStructure 函数的示例

z.enableExtrapolation()
```

#### YieldTermStructureHandle

**语法：**

`YieldTermStructureHandle(yieldTermStructure)`

**参数：**

**yieldTermStructure**
YieldTermStructure 类型句柄。

**描述：**

返回一个
YieldTermStructureHandle
类型对象。

**示例：**

```
use QuantLib

r = SimpleQuote(0.01);
riskFreeCurve = FlatForward(0, TARGET(), QuoteHandle(r), Actual360());
YieldTermStructureHandle(riskFreeCurve)
```

## 附录

### 代码示例

1. Barrier Option 计算示例

   [DolphinDB 脚本](example/BarrierEngine.dos)

   [Python 脚本](example/BarrierEngine.py)
2. FixedRateBond 计算示例

   [DolphinDB 脚本](example/FixRateBondFunction.dos)

   [Python
   脚本](example/FixRateBondFunction.py)
3. FloatingRateBond 计算示例

   [DolphinDB 脚本](example/FloatingRateBond.dos)

   [Python
   脚本](example/FloatingRateBond.py)
4. 其他计算示例：
   * [EuropeanOption.dos](example/EuropeanOption.dos)
   * [EuropeanOption.py](example/EuropeanOption.py)
   * [InterestRate.dos](example/InterestRate.dos)
   * [InterestRate.py](example/InterestRate.py)
   * [zeroRate.dos](example/zeroRate.dos)
   * [zeroRate.py](example/zeroRate.py)

### 使用 CMake 编译

```
cd /path/to/QuantLib
mkdir build
cd build
cp /path/to/DolphinDB/libDolphinDB.so ../lib
cmake ..
make
```
