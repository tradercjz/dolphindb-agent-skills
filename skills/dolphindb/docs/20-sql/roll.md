<!-- Auto-mirrored from upstream `documentation-main/progr/sql/roll.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# roll

首发版本：3.00.4

## 语法

`roll(X, step, [stepType='time'], [fill='none'],
[closed='left'], [origin='start_day'], [exclude], [label])`

## 详情

`roll` 是一个哑函数，用于在 SQL 查询中定义自定义滑动窗口。标准 CONTEXT BY 子句，或 GROUP BY
搭配分析函数时，窗口滑动步长固定为 1 行。GROUP BY 配合哑函数 `interval`
可以指定任意时间步长，但要求所有窗口长度相同。使用 roll 可以突破这些限制，自由定义窗口步长和长度。

`roll` 必须作为 SELECT 子句中第一个表达式，并且与 CONTEXT BY 搭配使用。

**返回值：**一个向量，其长度与窗口数量相同。通常，向量的每个元素表示对应窗口中 *X* 列的最后一个值。

但当 *stepType* = 'window' 时，每个元素表示对应窗口的标签（*label*），而非最后一个值。

**窗口确定规则**

在使用 `roll` 配合 SELECT 时，窗口的滑动步长和窗口长度由不同机制决定：

* 当 *stepType*='window' 时，窗口长度由自定义窗口（*window* 参数）确定。
* *stepType* ≠ 'window'：`roll` 只定义步长，不确定窗口长度。窗口长度则由 SELECT
  子句中的函数类型确定：

  + 聚合函数（内置或自定义）：窗口长度 = 步长。
  + 内置 m 系列滑动函数：

    - 当  *stepType* = 'time' 时，若 *window* 是 DURATION
      类型时，窗口长度 = *window*；若 *window* 是整数时，窗口长度是步长的
      *window* 倍。
    - 当 *stepType* = 'row' 时，*window* 必须是整数，窗口长度等于
      *window*。
    - 当 *stepType* = 'volume' / 'cumvol' 时，*window*
      必须是整数，窗口长度是步长的 *window* 倍。
  + 内置 tm 系列滑动函数（仅支持 *stepType* = 'time'）：窗口长度 = 函数中 *window*
    参数。
  + 表中列：窗口长度 = 步长，结果等价于对该列应用 `last` 函数。

## 参数

**X** 时间列或交易量的列。

* 若 *stepType* 为 'time'，*X* 必须为
  DATETIME/TIMESTAMP/NANOTIME/NANOTIMESTAMP 类型，并按升序排列。
* 若 *stepType* 为 'volume'，*X* 必须为数值类型，表示交易量。
* 若 *stepType* 为 'cumvol'，*X* 必须为数值类型，且按升序排列，表示累计交易量。

**step** 窗口滑动步长，可以为：

* DURATION 类型标量，表示时间间隔，支持如下时间单位：M, w, d, H, m, s, ms, us, ns。
* 当 *stepType* = ‘window’ 时，*step* 是长度为 2
  的元组，用于指定自定义窗口。第一个元素为起始时间，第二个元素为结束时间（需大于起始时间），两个元素的数据类型需与 *X*
  相同，且升序排列。默认左闭右开，可通过 *closed* 参数调整。

**stepType** 可选参数，STRING 类型标量，指定步长类型，可选值：

* 'time'：按时间列滑动，默认值。
* 'row'：按行数滑动。
* 'volume'：按交易量滑动。
* 'cumvol'：按累计交易量滑动。
* 'window'：按自定义窗口滑动。

**fill** 可选参数，STRING 类型标量，指定窗口内无数据时的处理方式，可选值：

* 'none'：不输出，默认值。
* 'null'：输出空值。
* 'prev'：填充前一个非空值。

**closed** 可选参数，STRING 类型标量，指定自定义窗口的闭合方式。可选值：

* 'left'：左闭右开，默认值。
* 'right'：左开右闭。

**origin** 可选参数，STRING 类型标量，指定时间滑动的起点，仅在 *stepType*='time' 时生效。可选值：

* 'start\_day'：起始点是时间序列的第一个值对应日期的午夜零点，默认值。
* 'start'：起始点为时间序列的第一个值。
* 'epoch'：起始点为 1970-01-01。

**exclude** 可选参数，元组，指定需要排除的时间段，仅在 *stepType*='time' 时生效。每个元素为
TIME、NANOTIME、MINUTE 和 SECOND 类型的数据对，例如 A 股午休时间
(11:30:00:13:00:00)。如果指定的时间段内存在数据，则必须通过 WHERE 子句过滤这段时间的数据。

**label** 可选参数，STRING 类型向量，自定义窗口名称，长度与自定义窗口数量一致。仅在 *stepType*='window'
时指定。

## 例子

例1. 按 symbol 分组，使用时间为步长 60 秒的滑动窗口，计算过去 180 秒，300 秒的平均价格。

```
timestamp = 2025.08.10T00:00:00 + 30 * 0..19
symbol = take(`A`B`C, 20)
price = [20.81,20.34,20.42,20.99,20.01,20.60,20.45,20.70,20.05,20.25,20.52,20.32,20.15,20.67,20.28,20.70,20.98,20.48,20.01,20.42]
vol = [1002,1091,1035,1041,1016,1038,1007,1007,1062,1030,1064,1012,1007,1007,1035,1038,1015,1041,1029,1048]
t = table(timestamp as timestamp, symbol as symbol, vol as vol, price as price)

select * from t order by symbol
// 使用 roll + mavg 计算 180 秒和 300 秒滑动平均
select
    roll(X=timestamp, step=60s, stepType='time') as period,
    mavg(price, 180s) as avg_60s,
    mavg(price, 300s) as avg_300s,
    symbol,
    price,
    vol
from t
context by symbol
```

部分结果展示：

| period | avg\_60s | avg\_300s | symbol | price | vol |
| --- | --- | --- | --- | --- | --- |
| 2025.08.10 00:01:00 | 20.81 | 20.81 | A | 20.81 | 1,002 |
| 2025.08.10 00:02:00 | 20.9 | 20.9 | A | 20.99 | 1,041 |
| 2025.08.10 00:04:00 | 20.72 | 20.75 | A | 20.45 | 1,007 |
| 2025.08.10 00:05:00 | 20.35 | 20.625 | A | 20.25 | 1,030 |
| 2025.08.10 00:07:00 | 20.2 | 20.28333333333333 | A | 20.15 | 1,007 |
| 2025.08.10 00:08:00 | 20.424999999999997 | 20.3875 | A | 20.7 | 1,038 |
| 2025.08.10 00:10:00 | 20.355 | 20.286666666666665 | A | 20.01 | 1,029 |

例2. 按 symbol 分组，滑动步长为 2 行，分别计算过去 2 行的交易量均值，以及过去 3 行交易量总和。

```
select roll(X=vol, step=2, stepType='row') as window, avg(vol), msum(vol, 3), symbol, price, vol from t context by symbol
```

| window | avg\_vol | msum\_vol | symbol | price | vol |
| --- | --- | --- | --- | --- | --- |
| 1,041 | 1,021.5 | 2,043 | A | 20.99 | 1,041 |
| 1,030 | 1,018.5 | 3,078 | A | 20.25 | 1,030 |
| 1,038 | 1,022.5 | 3,075 | A | 20.7 | 1,038 |
| 1,016 | 1,053.5 | 2,107 | B | 20.01 | 1,016 |
| 1,064 | 1,035.5 | 3,087 | B | 20.52 | 1,064 |
| 1,015 | 1,011 | 3,086 | B | 20.98 | 1,015 |
| 1,038 | 1,036.5 | 2,073 | C | 20.6 | 1,038 |
| 1,012 | 1,037 | 3,112 | C | 20.32 | 1,012 |
| 1,041 | 1,038 | 3,088 | C | 20.48 | 1,041 |

例3. 本例通过参数 *exclude* 排除1:30–13:00 的午休时段。在该时间区间内，系统不进行窗口划分。

```
select
    roll(X=timestamp, step=60s, stepType='time', exclude=(11:30:00 : 13:00:00)) as period,
    mavg(price, 180s) as avg_60s,
    mavg(price, 300s) as avg_300s,
    symbol,
    price,
    vol
from t
context by symbol
```

| period | avg\_60s | avg\_300s | symbol | price | vol |
| --- | --- | --- | --- | --- | --- |
| 2025.08.10 00:01:00 | 20.81 | 20.81 | A | 20.81 | 1,002 |
| 2025.08.10 00:02:00 | 20.9 | 20.9 | A | 20.99 | 1,041 |
| 2025.08.10 00:04:00 | 20.72 | 20.75 | A | 20.45 | 1,007 |
| 2025.08.10 00:05:00 | 20.35 | 20.625 | A | 20.25 | 1,030 |
| 2025.08.10 00:07:00 | 20.2 | 20.28333333333333 | A | 20.15 | 1,007 |
| 2025.08.10 00:08:00 | 20.424999999999997 | 20.3875 | A | 20.7 | 1,038 |
| 2025.08.10 00:10:00 | 20.355 | 20.286666666666665 | A | 20.01 | 1,029 |
| 2025.08.10 00:01:00 | 20.34 | 20.34 | B | 20.34 | 1,091 |
| 2025.08.10 00:03:00 | 20.175 | 20.175 | B | 20.01 | 1,016 |
| 2025.08.10 00:04:00 | 20.355 | 20.35 | B | 20.7 | 1,007 |

例4. 通过*stepType*='window' 自定义 3 个时间窗口，计算每个股票过去 1 天，3 天和 7
天内的成交量和加权平均价格。`roll` 函数采用增量计算，可以大幅提升计算效率。

```
date = stretch(2025.08.01+ 0..8, 24)
time = take([09:30:00, 10:00:00, 10:30:00],24)
symbol = take(`A`B, 24)
price = [22.40, 24.00, 23.50, 29.30, 24.10, 27.60, 20.10, 21.00, 23.60, 22.40,
               24.60, 23.30, 21.20, 20.60, 27.30, 29.30, 26.90, 25.20, 20.20, 20.10,
               28.30, 22.50, 28.20, 23.50]

vol = [1088, 1074, 1081, 1018, 1045, 1007, 1023, 1009, 1018, 1019,
           1013, 1017, 1039, 1057, 1045, 1062, 1046, 1033, 1022, 1007,
           1087, 1012, 1091, 1074]
timestamp=concatDateTime(date,time)
t = table(timestamp as timestamp, symbol as symbol, price as price, vol as vol)
t = select * from t order by symbol, timestamp

startDates = [datetime(2025.08.01), datetime(2025.08.01), datetime(2025.08.01)]
endDates = [datetime(2025.08.02), datetime(2025.08.04), datetime(2025.08.07)]
labels = ["1d", "3d", "7d"]

// 计算窗口指标
select
    roll(X=datetime(timestamp), step=(startDates, endDates), stepType='window', label=labels, fill='none') as period,
    timestamp,
    symbol,
    vol,
    price,
    sum(vol) as vol_sum,
    wavg(price, vol) as vwap
from t context by symbol
```

| period | timestamp | symbol | vol | price | vol\_sum | vwap |
| --- | --- | --- | --- | --- | --- | --- |
| 1d | 2025.08.01 10:30:00 | A | 1,081 | 23.5000 | 2,169 | 22.9482 |
| 3d | 2025.08.03 10:30:00 | A | 1,018 | 23.6000 | 5,255 | 22.7491 |
| 7d | 2025.08.06 10:00:00 | A | 1,046 | 26.9000 | 9,398 | 23.7454 |
| 1d | 2025.08.01 10:00:00 | B | 1,074 | 24.0000 | 1,074 | 24.0000 |
| 3d | 2025.08.03 10:00:00 | B | 1,009 | 21.0000 | 4,108 | 25.4590 |
| 7d | 2025.08.06 10:30:00 | B | 1,033 | 25.2000 | 9,296 | 24.7450 |
