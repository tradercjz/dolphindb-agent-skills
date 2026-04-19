# temporalSeq

## 语法

`temporalSeq(start, end, rule, [closed], [label],
[origin='start_day'])`

## 详情

根据 *rule* 指定的频率，对由 *start* 开始，*end*
结尾的时间序列进行重采样，并返回新生成的时间序列。

## 参数

**start** 时间类型标量。

**end** 时间类型标量。必须和 *start* 的类型相同，且值必须大于 *start*。

**rule** 字符串，可取以下值：

| rule 参数取值 | 对应 DolphinDB 函数 |
| --- | --- |
| "B" | businessDay |
| "W" | weekEnd |
| "WOM" | weekOfMonth |
| "LWOM" | lastWeekOfMonth |
| "M" | monthEnd |
| "MS" | monthBegin |
| "BM" | businessMonthEnd |
| "BMS" | businessMonthBegin |
| "SM" | semiMonthEnd |
| "SMS" | semiMonthBegin |
| "Q" | quarterEnd |
| "QS" | quarterBegin |
| "BQ" | businessQuarterEnd |
| "BQS" | businessQuarterBegin |
| "REQ" | fy5253Quarter |
| "A" | yearEnd |
| "AS" | yearBegin |
| "BA" | businessYearEnd |
| "BAS" | businessYearBegin |
| "RE" | fy5253 |
| "D" | date |
| "H" | hourOfDay |
| "U" | microsecond |
| "L" | millisecond |
| "min" | minuteOfHour |
| "N" | nanosecond |
| "S" | secondOfMinute |
| "SA" | semiannualEnd |
| "SAS" | semiannualBegin |

上述字符串亦可配合使用数字，例如 "2M" 表示频率为每两个月月末。此外，*rule*
也可以是交易日历标识，例如：国外交易所的 ISO Code、国内交易所简称或自定义交易日历名称。

**closed** 字符串，表示重采样时间窗口的闭合边界。可取值为 "left", "right"。

* *rule* 为 'M', 'A', 'Q', 'BM', 'BA', 'BQ' 和 'W' 时，*closed* 的默认取值为
  'right' ，否则，*closed* 的默认取值为 'left'。
* *origin* 取 'end' 或者 'end\_day' 时，*closed* 的默认值为
  'right'。

**label** 字符串，表示重采样时间窗口的标签位置。可取值为 "left", "right"。

* *rule* 为 'M', 'A', 'Q', 'BM', 'BA', 'BQ' 和 'W'
  时，label 的默认取值为 'right' ，否则，*label* 的默认取值为 'left'。
* *origin* 取 'end' 或者 'end\_day' 时，*label* 的默认值为 'right'。

**origin** 字符串或与 *start/end* 具有相同时间类型的标量，表示重采样的基准时间点，即重采样的起始点。*origin*
的取值为 'epoch', start', 'start\_day', 'end', 'end\_day' 或自定义的时间对象，默认值为 'start\_day'。
字符串，表示重采样时间窗口的标签位置。可取值为 "left", "right"。

* 'epoch'：分组起始点为1970-01-01。
* 'start'：分组起始点为 *start* 参数指定的值。
* 'start\_day'：分组起始点是 *start* 参数指定值对应日期的午夜零点。
* 'end'：分组起始点是 *end* 参数指定的值。
* 'end\_day'：分组起始点是 *end* 参数指定值对应日期的午夜24点（即下一日的零点）。

## 返回值

Temporal 类型向量。

## 例子

例1.
从00:01:00开始，到00:08:00，按3分钟间隔取样，默认左闭右开区间（*closed*='left'），默认取时间窗口的左边界（*label*='left'）。

```
temporalSeq(start=2022.01.01 00:01:00,end=2022.01.01 00:08:00,rule="3min")
```

输出返回：`[2022.01.01T00:00:00,2022.01.01T00:03:00,2022.01.01T00:06:00]`

例2. 基于例1，设置 *closed*=`right，为左开右闭。由于此时 *label* 的取值默认为 'left'，结果与例1相同。

```
temporalSeq(start=2022.01.01 00:01:00, end=2022.01.01 00:08:00, rule="3min", closed=`right)
```

输出返回：`[2022.01.01T00:00:00,2022.01.01T00:03:00,2022.01.01T00:06:00]`

例3. 基于例2，设置 *label*=`right，即输出每个窗口的右边界，因此生成3分、6分、9分三个时间点。

```
temporalSeq(start=2022.01.01 00:01:00, end=2022.01.01 00:08:00, rule="3min", closed=`right, label=`right)
```

输出返回：`[2022.01.01T00:03:00,2022.01.01T00:06:00,2022.01.01T00:09:00]`

例4. 基于例2，设置 *origin*='end'，以结束时间00:08:00为基准向前取样，此时默认为左开右闭，因此生成2分、5分、8分三个时间点。

```
temporalSeq(start=2022.01.01 00:01:00, end=2022.01.01 00:08:00, rule="3min", closed=`right, origin=`end)
```

输出返回：`[2022.01.01T00:02:00,2022.01.01T00:05:00,2022.01.01T00:08:00]`

例5. 与例4不同的是，本例设置 *origin*=2022.10.01
00:00:10，以自定义的10秒为基准点，生成了00:00:10、00:03:10、00:06:10三个时间点。

```
temporalSeq(start=2022.01.01 00:01:00, end=2022.01.01 00:08:00, rule="3min", closed=`right, origin=2022.10.01 00:00:10)
```

输出返回：`[2022.01.01T00:00:10,2022.01.01T00:03:10,2022.01.01T00:06:10]`
