<!-- Auto-mirrored from upstream `documentation-main/tutorials/financial_mock_data_generation_module.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 金融 Mock 数据生成模块

测试 DolphinDB 数据库性能时，往往需要快速写入一些测试数据。为方便用户快速完成简单的基准性能测试，金融 Mock 数据生成模块覆盖了常用的金融数据集，满足用户生成模拟数据的需求。基于本模块生成的模拟数据不具有实际意义，建议仅作读写性能测试和基础功能体验使用。

本模块基于 DolphinDB 2.00.13 开发，请使用 2.00.13 及以上版本进行测试。

## **1. 环境配置**

本教程的模块代码文件（ MockData.dos ）可在附录中获取，将 MockData.dos 文件移至节点的 [home]/modules 目录下即完成环境配置。其中 [home] 目录由系统配置参数 *home* 决定，可以通过 `getHomeDir()` 函数查看。

更多 DolphinDB 模块的说明，请参阅：DolphinDB 教程：模块。

## **2. 使用说明**

通过 use 关键字导入模块。导入模块后，可以通过以下两种方式来使用模块内的自定义函数：

(1) 直接调用模块中的函数，生成1天10个股票的 Level-2 快照数据，一共有48020行：

```
use MockData
t = stockSnapshot(tradeDate=2020.01.06, securityNumber=10)
```

(2) 通过模块中的函数的完整路径来调用：

```
use MockData
t = MockData::stockSnapshot(tradeDate=2020.01.06, securityNumber=10)
```

**若导入的不同模块中含有相同名称的函数，则必须通过第二种方式调用。**

## 3. 模拟数据生成函数说明

本模块仅生成交易日的数据，当输入日期为非交易日时，会返回空数据表。交易日通过 DolphinDB 内置交易日历获取。由于存在多个交易所的交易日历，本文使用上交所的交易日历作为金融 Mock 数据生成模块的交易日。更多 DolphinDB 内置交易日历的说明，请参阅：交易日历。

模拟数据生成函数参考真实市场的交易量。对于每只标的，生成的一天数据量都相同，且生成的数据在一天中的交易时间段内均匀分布。生成的相关数值指标由随机数和固定值组成，不具备实际意义。具体数据量和说明如下表所示：

| **函数名** | **单日单标的数据量（行）** | **说明** | **函数名** | **单日单标的数据量（行）** | **说明** |
| --- | --- | --- | --- | --- | --- |
| stockSnapshot | 4,802 | 每 3 秒生成一只标的数据 | XBondTrade | 120 | 按固定数据量在交易时间内均匀分布，约 2 分钟生成一只标的数据 |
| stockEntrust | 28,802 | 每 0.5 秒生成一只标的数据 | dailyFactor（单因子） | 1 | 每 1 天生成一只标的因子数据 |
| stockTrade | 28,802 | 每 0.5 秒生成一只标的数据 | halfHourFactor（单因子） | 8 | 每 30 分钟生成一只标的因子数据 |
| stockMinuteKLine | 242 | 每 1 分钟生成一只标的数据 | tenMinutesFactor（单因子） | 240 | 每 10 分钟生成一只标的因子数据 |
| stockDailyKLine | 1 | 每 1 天生成一只标的数据 | minuteFactor（单因子） | 240 | 每 1 分钟生成一只标的因子数据 |
| optionsSnapshot | 900 | 按固定数据量在交易时间内均匀分布，约 19 秒生成一只标的数据 | secondFactor（单因子） | 14,400 | 每 1 秒生成一只标的因子数据 |
| futuresSnapshot | 2,000 | 按固定数据量在交易时间内均匀分布，约 9 秒生成一只标的数据 | level2Factor（单因子） | 4,800 | 每 3 秒生成一只标的因子数据 |
| ESPDepth | 80 | 按固定数据量在交易时间内均匀分布，约 3 分钟生成一只标的数据 | tickFactor（单因子） | 28,800 | 每 0.5 秒生成一只标的因子数据 |
| ESPTrade | 10 | 按固定数据量在交易时间内均匀分布，约 30 分钟生成一只标的数据 | futuresFactor（单因子） | 66,600 | 每 0.5 秒生成一只标的因子数据 |
| XBondDepth | 1,000 | 按固定数据量在交易时间内均匀分布，约 17 秒生成一只标的数据 |  |  |  |

### 3.1 股票数据

股票数据主要有 Level-2 快照、逐笔委托以及逐笔成交等类型，可通过本模块中的函数生成这些数据。下面对数据生成模块的相关函数进行说明。

#### 3.1.1 stockSnapshot

`stockSnapshot(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示快照数据的日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。

**详情**

创建一天的 Level-2 快照模拟数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，股票标的数量通过 *securityNumber* 指定。

**例子**

```
snapshotData = stockSnapshot(tradeDate=2020.01.06, securityNumber=10)
```

#### 3.1.2 stockEntrust

`stockEntrust(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示逐笔委托数据的日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。

**详情**

创建一天的逐笔委托数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，股票标的数量通过 *securityNumber* 指定。

**例子**

```
entrustData = stockEntrust(tradeDate=2020.01.06, securityNumber=10)
```

#### 3.1.3 stockTrade

`stockTrade(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示逐笔成交数据的日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。

**详情**

创建一天的逐笔成交数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，股票标的数量通过 *securityNumber* 指定。

**例子**

```
tradeData = stockTrade(tradeDate=2020.01.06, securityNumber=10)
```

#### 3.1.4 stockMinuteKLine

`stockMinuteKLine(startDate, endDate, securityNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示分钟 K 数据的起始日期。
* *endDate*：DATE 类型的标量，表示分钟 K 数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。

**详情**

创建指定时间范围内分钟 K 线数据，并以表的数据形式返回。交易的起始日期通过 *startDate* 指定，交易的结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定。

**例子**

```
minuteKLineData = stockMinuteKLine(startDate=2020.09.05, endDate=2021.01.07, securityNumber=10)
```

#### 3.1.5 stockDailyKLine

`stockDailyKLine(startDate, endDate, securityNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示日 K 数据的起始日期。
* *endDate*：DATE 类型的标量，表示日 K 数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。

**详情**

创建指定时间范围内的日 K 线数据，并以表的数据形式返回。交易的起始日期通过 *startDate* 指定，交易的结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定。

**例子**

```
dailyKLineData = stockDailyKLine(startDate=2015.01.01, endDate=2021.01.30, securityNumber=1000)
```

### 3.2 期权数据

#### 3.2.1 optionsSnapshot

`optionsSnapshot(tradeDate, instrumentNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示期权数据的日期。
* *instrumentNumber*：INT 类型的标量，表示期权合约数量。

**详情**

创建一个单日的期权快照数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，期权标的数量通过 *instrumentNumber* 指定。

**例子**

```
optionsSnapshotData = optionsSnapshot(tradeDate=2020.01.06, instrumentNumber=14000)
```

### 3.3 期货数据

#### 3.3.1 futuresSnapshot

`futuresSnapshot(tradeDate, instrumentNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示期货数据的日期。
* *instrumentNumber*：INT 类型的标量，表示期货合约数量。

**详情**

创建一个单日的期货数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，期权标的数量通过 *instrumentNumber* 指定。

**例子**

```
FuturesData = futuresSnapshot(tradeDate=2020.06.01, instrumentNumber=2000)
```

### 3.4 银行间债券数据

银行间债券数据有 ESP 报价、ESP 成交、XBond 报价、XBond 成交类型，可通过本模块中的函数生成这些数据。下面对数据生成模块的相关函数进行说明。

#### 3.4.1 ESPDepth

`ESPDepth(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示银行间债券 ESP 报价数据的日期。
* *securityNumber*：INT 类型的标量，表示银行间债券 ESP 标的数量。

**详情**

创建一个单日的银行间债券 ESP 报价数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，银行间债券 ESP 标的数量通过 *securityNumber* 指定。

**例子**

```
ESPDepthData = ESPDepth(tradeDate=2020.06.01, securityNumber=4000)
```

#### 3.4.2 ESPTrade

`ESPTrade(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示银行间债券 ESP 成交数据的日期。
* *securityNumber*：INT 类型的标量，表示银行间债券 ESP 标的数量。

**详情**

创建一个单日的银行间债券 ESP 成交数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，银行间债券 ESP 标的数量通过 *securityNumber* 指定。

**例子**

```
ESPTradeData = ESPTrade(tradeDate=2020.06.01, securityNumber=3000)
```

#### 3.4.3 XBondDepth

`XBondDepth(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示银行间债券 XBond 报价数据的日期。
* *securityNumber*：INT 类型的标量，表示银行间债券 XBond 标的数量。

**详情**

创建一个单日的银行间债券 XBond 报价数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，银行间债券 XBond 标的数量通过 *securityNumber* 指定。

**例子**

```
XBondDepthData = XBondDepth(tradeDate=2020.06.01, securityNumber=200)
```

#### 3.4.4 XBondTrade

`XBondTrade(tradeDate, securityNumber)`

**参数**

* *tradeDate*：DATE 类型的标量，表示银行间债券 XBond 成交数据的日期。
* *securityNumber*：INT 类型的标量，表示银行间债券 XBond 标的数量。

**详情**

创建一个单日的银行间债券 XBond 成交数据，并以表的数据形式返回。交易日期通过 *tradeDate* 指定，银行间债券 XBond 标的数量通过 *securityNumber* 指定。

**例子**

```
XBondTradeData = XBondTrade(tradeDate=2020.06.01, securityNumber=200)
```

### 3.5 因子库数据

因子库数据有各种频率因子数据类型，可通过本模块中的函数生成这些数据。下面对数据生成模块的相关函数进行说明。

#### 3.5.1 dailyFactor

`dailyFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* securityNumber：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的日频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
dailyFactorData = dailyFactor(startDate=2016.01.01,endDate=2021.12.31,securityNumber=500,
    factorNumber=100)
```

上述代码会生成一个大小约为1.8GB，变量名为 dailyFactorData 的内存表。

#### 3.5.2 halfHourFactor

`halfHourFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的半小时频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
halfHourFactorData = halfHourFactor(startDate=2021.06.01,endDate=2021.12.31,securityNumber=500,
    factorNumber=100)
```

上述代码会生成一个大小约为1.7GB，变量名为 halfHourFactorData 的内存表。

#### 3.5.3 tenMinutesFactor

`tenMinutesFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的十分钟频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
tenMinutesFactorData = tenMinutesFactor(startDate=2021.09.01,endDate=2021.12.31,securityNumber=500,
    factorNumber=100)
```

上述代码会生成一个大小约为2.2GB，变量名为 tenMinutesFactorData 的内存表。

#### 3.5.4 minuteFactor

`minuteFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的分钟频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
minuteFactorData = minuteFactor(startDate=2021.12.01,endDate=2021.12.31,securityNumber=100,
    factorNumber=100)minuteFactor
```

上述代码会生成一个大小约为1.5GB，变量名为 minuteFactorData 的内存表。

#### 3.5.5 secondFactor

`secondFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的秒钟频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
secondFactorData = secondFactor(startDate=2021.12.15, endDate=2021.12.31, securityNumber=50,
    factorNumber=10)
```

上述代码会生成一个大小约为2.6GB，变量名为 secondFactorData 的内存表。

#### 3.5.6 level2Factor

`level2Factor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的 Level-2 快照频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
level2FactorData = level2Factor(startDate=2021.12.01,endDate=2021.12.31,securityNumber=50,
    factorNumber=10)
```

上述代码会生成一个大小约为1.5GB，变量名为 level2FactorData 的内存表。

#### 3.5.7 tickFactor

`tickFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的逐笔频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
tickFactorData = tickFactor(startDate=2021.12.01,endDate=2021.12.31,securityNumber=50, factorNumber=10)
```

上述代码会生成一个大小约为8.6GB，变量名为 tickFactorData 的内存表。

#### 3.5.8 futuresFactor

`futuresFactor(startDate, endDate, securityNumber, factorNumber)`

**参数**

* *startDate*：DATE 类型的标量，表示因子数据的起始日期。
* *endDate*：DATE 类型的标量，表示因子数据的结束日期。
* *securityNumber*：INT 类型的标量，表示股票标的数量。
* *factorNumber*：INT 类型的标量，表示因子数量。

**详情**

创建指定时间范围内的期货500ms频因子数据，并以表的数据形式返回。起始日期通过 *startDate* 指定，结束日期通过 *endDate* 指定，股票标的数量通过 *securityNumber* 指定，因子数量通过 *factorNumber* 指定。

**例子**

```
futuresFactorData = futuresFactor(startDate=2021.12.15,endDate=2021.12.31,securityNumber=50,
    factorNumber=10)
```

上述代码会生成一个大小约为10.6GB，变量名为 futuresFactorData 的内存表。

## 4. 库表生成函数说明

由于不同类型的金融数据具有不同的表结构，自行创建这些库表会非常繁琐。在该模块中，我们将提供针对不同数据类型的库表创建函数，以便用户更轻松地创建所需的库表。本模块的建库建表代码参考自存储金融数据的分区方案最佳实践。

### 4.1 股票数据

#### 4.1.1 stockSnapShotPT

`stockSnapShotPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储快照数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储快照数据的数据表名。

**详情**

创建存储快照数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = stockSnapShotPT("dfs://merge_TB", "merge_snapshotTB")
```

#### 4.1.2 stockEntrustPT

`stockEntrustPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储逐笔委托数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储逐笔委托数据的数据表名。

**详情**

创建存储逐笔委托数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = stockEntrustPT("dfs://merge_TB", "merge_entrustTB")
```

#### 4.1.3 stockTradePT

`stockTradePT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储逐笔成交数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储逐笔成交数据的数据表名。

**详情**

创建存储逐笔成交数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = stockTradePT("dfs://merge_TB", "merge_tradeTB")
```

#### 4.1.4 stockMinuteKLinePT

`stockMinuteKLinePT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储分钟 K 数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储分钟 K 数据的数据表名。

**详情**

创建存储分钟K数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = stockMinuteKLinePT("dfs://k_minute_level", "k_minute")
```

#### 4.1.5 stockDailyKLinePT

`stockDailyKLinePT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储日 K 数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储日 K 数据的数据表名。

**详情**

创建存储日 K 数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = stockDailyKLinePT("dfs://k_day_level", "k_day")
```

### 4.2 期货数据

#### 4.2.1 futuresPT

`futuresPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储期货数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储期货数据的数据表名。

**详情**

创建存储期货数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = futuresPT("dfs://ctp_futures", "futures")
```

### 4.3 期权数据

#### 4.3.1 optionsPT

`optionsPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储期权数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储期权数据的数据表名。

**详情**

创建存储期权数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = optionsPT("dfs://ctp_options", "options")
```

### 4.4 银行间债券

#### 4.4.1 ESPDepthPT

`ESPDepthPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储银行间债券 ES P报价数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储银行间债券 ESP 报价数据的数据表名。

**详情**

创建银行间债券ESP报价数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = ESPDepthPT("dfs://ESPDepth", "ESPDepthtable")
```

#### 4.4.2 ESPTradePT

`ESPTradePT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储银行间债券 ESP 成交数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储银行间债券 ESP 成交数据的数据表名。

**详情**

创建银行间债券ESP成交数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = ESPTradePT("dfs://ESPTrade", "ESPTradetable")
```

#### 4.4.3 XBondDepthPT

`XBondDepthPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储银行间债券 XBond 报价数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储银行间债券 XBond 报价数据的数据表名。

**详情**

创建银行间债券XBond报价数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = XBondDepthPT("dfs://XBondDepth", "XBondDepthtable")
```

#### 4.4.4 XBondTradePT

`XBondTradePT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储银行间债券 XBond 成交数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储银行间债券 XBond 成交数据的数据表名。

**详情**

创建银行间债券 XBond 成交数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = XBondTradePT("dfs://XBondTrade", "XBondTradetable")
```

### 4.5 因子库数据

#### 4.5.1 dailyFactorPT

`dailyFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储日频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储日频因子数据的数据表名。

**详情**

创建日频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = dailyFactorPT("dfs://dayFactorDB", "dayFactorTB")
```

#### 4.5.2 halfHourFactorPT

`halfHourFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储半小时频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储半小时频因子数据的数据表名。

**详情**

创建半小时频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = halfHourFactorPT("dfs://halfhourFactorDB", "halfhourFactorTB")
```

#### 4.5.3 tenMinutesFactorPT

`tenMinutesFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储十分钟频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储十分钟频因子数据的数据表名。

**详情**

创建十分钟频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = tenMinutesFactorPT("dfs://tenMinutesFactorDB", "tenMinutesFactorTB")
```

#### 4.5.4 minuteFactorPT

`minuteFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储分钟频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储分钟频因子数据的数据表名。

**详情**

创建分钟频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = minuteFactorPT("dfs://minuteFactorDB", "minuteFactorTB")
```

#### 4.5.5 secondFactorPT

`secondFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储秒钟频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储秒钟频因子数据的数据表名。

**详情**

创建秒钟频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = secondFactorPT("dfs://secondFactorDB", "secondFactorTB")
```

#### 4.5.6 level2FactorPT

`level2FactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储Level-2 快照频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储Level-2 快照频因子数据的数据表名。

**详情**

创建Level-2 快照频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = level2FactorPT("dfs://level2FactorDB", "level2FactorTB")
```

#### 4.5.7 tickFactorPT

`tickFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储逐笔频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储逐笔频因子数据的数据表名。

**详情**

创建逐笔频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = tickFactorPT("dfs://tickFactorDB", "tickFactorTB")
```

#### 4.5.8 futuresFactorPT

`futuresFactorPT(dbName, tbName)`

**参数**

* *dbName*：STRING 类型的标量，表示存储期货500ms频因子数据的数据库名。
* *tbName*：STRING 类型的标量，表示存储期货500ms频因子数据的数据表名。

**详情**

创建期货500ms频因子数据的数据库表，并返回数据表的句柄。数据库名通过 *dbName* 指定，数据表名通过 *tbName* 指定。

**例子**

```
t = futuresFactorPT("dfs://futuresFactorDB", "futuresFactorTB")
```

## 5. 应用示例

用户可以将第 3 节中生成的模拟数据，存入第 4 节所创建的数据库表，以 Level2 快照行情为例，代码如下：

```
use MockData

snapshotData = stockSnapshot(tradeDate=2020.01.06, securityNumber=10)
t = stockSnapShotPT("dfs://merge_TB", "merge_snapshotTB")
t.append!(snapshotData)
```

相应的金融数据可存入对应数据库表，Mock 数据生成函数与数据库表创建函数的对应关系如下：

| **数据生成函数** | **数据库表创建函数** |
| --- | --- |
| stockSnapshot | stockSnapShotPT |
| stockEntrust | stockEntrustPT |
| stockTrade | stockTradePT |
| stockMinuteKLine | stockMinuteKLinePT |
| stockDailyKLine | stockDailyKLinePT |
| optionsSnapshot | optionsPT |
| futuresSnapshot | futuresPT |
| ESPDepth | ESPDepthPT |
| ESPTrade | ESPTradePT |
| XBondDepth | XBondDepthPT |
| XBondTrade | XBondTradePT |
| dailyFactor | dailyFactorPT |
| halfHourFactor | halfHourFactorPT |
| tenMinutesFactor | tenMinutesFactorPT |
| minuteFactor | minuteFactorPT |
| secondFactor | secondFactorPT |
| level2Factor | level2FactorPT |
| tickFactor | tickFactorPT |
| futuresFactor | futuresFactorPT |

## 6. 常见问题

### 6.1 创建数据库表时报错：CacheEngineOOM

执行数据插入数据库表的代码后可能会出现 CacheEngineOOM 的问题，示例代码如下：

```
minuteKLineData = genStockMinuteKLine(startDate=2020.01.01, endDate=2020.06.30, securityNumber=2000)
t = createMinuteKLineTable("dfs://MinuteK", "MinuteK")
t.append!(minuteKLineData)
```

报出如下错误：

```
::append!(t, minuteKLineData) =>
	[appendDFSTablet] parallel execution of save table failed with error msg:
	ChunkCacheEngine is out of memory,
	possibly due to a transaction that tries to write data larger than the available memory.
```

**解决方法：**

* 方法一：减小一次写入的数据量。
* 方法二：增大 CacheEngine 的大小。可以调用 setOLAPCacheEngineSize 在线增大 OLAP Cache Engine 的容量，需要注意同时修改配置项 *OLAPCacheEngineSize*，否则重启后在线修改的容量会失效。

### 6.2 查询数据库时报错：The query is too large

执行查询数据库表的代码后可能会出现查询分区数量过多的问题，示例代码如下：

```
temp = select top 100 * from loadTable(db_path, tb_name)
```

报出如下错误：

```
The number of partitions [880900] relevant to the query is too large.
	Please add more specific filtering conditions on partition columns in WHERE clause,
	or consider changing the value of the configuration parameter maxPartitionNumPerQuery.
```

**解决方法：**

* 方法一：查询时通过 WHERE 语句减少查询涉及的分区数量。
* 方法二：增大单个查询语句可查找的最大分区数，系统默认值是 65536，可以通过参数 *maxPartitionNumPerQuery* 进行配置并在重启后生效。

### 6.3 模拟数据生成返回0行记录

成功执行模拟数据生成函数后，返回的结果表里仅有0行记录，示例代码如下：

```
snapshotData = stockSnapshot(tradeDate=2020.01.05, securityNumber=10)
select * from snapshotData
```

2020.01.05 为非交易日。本模块仅生成交易日的数据，当输入日期为非交易日时，会返回空数据表。交易日通过交易日历进行获取，且默认使用上交所交易日历。

**解决方法：**

* *tradeDate* 填入真实的交易日。

### 6.4 创建分布式数据库表时报错

执行创建数据库表的代码后可能会出现无法写入一个已经存在的数据库的问题，示例代码如下：

```
t = ESPDepthPT("dfs://merge_TB", "merge_TB")
```

报出如下错误：

```
MockData::ESPDepthPT: db = database(newdbName, VALUE, 2022.06.01 .. 2023.01.01, , "TSDB") =>
	It is not allowed to overwrite an existing database.
```

**解决方法：**

* 建议使用其他名字或者删掉该数据库再创建该数据库表。

  删除指定数据库的代码如下：

  ```
  dropDatabase("dfs://merge_TB")
  ```

  检查指定数据库是否存在的代码如下：

  ```
  existsDatabase("dfs://merge_TB")
  ```

## 附录

[MockData](script/financial_mock_data_generation_module/MockData.dos)
