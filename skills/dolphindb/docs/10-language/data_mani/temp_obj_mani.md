<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/temp_obj_mani.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 时序对象的操作

## 获取时间变量的部分信息

获取时间变量的部分信息的用法如下：

```
year(2016.02.14);
// output
2016

monthOfYear(2016.02.14);
// output
2

dayOfMonth(2016.02.14);
// output
14

x=01:02:03.456;
hour(x);
// output
1

minuteOfHour(x);
// output
2

secondOfMinute(x);
// output
3

x mod 1000;
// output
456
```

## 用运算符调整时间变量值

使用运算符"+"或"-"来调整时间变量的值。

```
2016.02M-13;
// output
2015.01M

2018.02.17+100;
// output
2018.05.28

01:20:15+200;
// output
01:23:35
```

对于minute, second,
time和nanotime类型的时间序列对象，表示这些对象的内部整数的最小值为0，最大值分别为1440-1, 86400-1,
86400000-1和86400000000000-1。如果进行运算调整之后，其中一个表示这些对象的内部整数小于0或大于相应的最大值，最终结果是内部整数除以相应的最大值的余数。

```
23:59m+10;
// output
00:09m

00:00:01-2;
// output
23:59:59

23:59:59.900+200;
// output
00:00:00.100
```

## 用时间单位调整时间变量值

temporalAdd
函数以不同的时间单位调整时间变量的值。

```
temporalAdd(2017.01.16,1,"w");
// output
2017.01.23

temporalAdd(2016.12M,2,"M");
// output
2017.02M

temporalAdd(13:30m,-15,"m");
// output
13:15m
```

## 合并日期与时间

concatDateTime 函数可以合并日期和时间。

```
concatDateTime(2019.06.15,13:25:10);
// output
2019.06.15T13:25:10

concatDateTime(2019.06.15 2019.06.16 2019.06.17,[13:25:10, 13:25:12, 13:25:13]);
// output
[2019.06.15T13:25:10,2019.06.16T13:25:12,2019.06.17T13:25:13]
```

## 与 DateOffset 相关的函数

* yearBegin
  ：获取当年的第一天
* yearEnd
  ：获取当年的最后一天
* businessYearBegin ：获取当年的第一个工作日
* businessYearEnd ：获取当年的最后一个工作日
* isYearStart ：判断当天是否为年初第一天
* isYearEnd
  ：判断当天是否为年末最后一天
* isLeapYear ：判断当年是否为闰年

```
yearBegin(2011.06.02);
// output
2011.01.01

yearEnd(2011.06.02);
// output
2011.12.31

businessYearBegin(2011.06.02);
// output
2011.01.03

businessYearEnd(2011.06.12);
// output
2011.12.30

isYearBegin(2011.01.01);
// output
true

isYearEnd(2011.12.31);
// output
true

isLeapYear(2012.06.25);
// output
true
```

* monthBegin ：获取当月的第一天
* monthEnd
  ：获取当月的最后一天
* businessMonthBegin ：获取当月的第一个工作日
* businessMonthEnd ：获取当月的最后一个工作日
* semiMonthBegin ：获取当月开始的第15（或其他）天
* semiMonthEnd ：获取当月结束的第15（或其他）天
* isMonthStart ：判断当天是否为月初的第一天
* isMonthEnd ：判断当天是否为月末的最后一天
* daysInMonth ：获取当月的天数

```
monthBegin(2016.12.06);
// output
2016.12.01

monthEnd(2016.12.06);
// output
2016.12.31

businessMonthBegin(2016.10.06);
// output
2016.10.03

businessMonthEnd(2016.07.06);
// output
2016.07.29

semiMonthBegin(2016.12.26);
// output
2016.12.15

semiMonthEnd(2016.12.06,15);
// output
2016.11.30

isMonthStart(2011.01.01);
// output
true

isMonthEnd(2011.12.31);
// output
true

daysInMonth(2012.12.02);
// output
31
```

* quarterBegin ：获取当前季度的第一天
* quarterEnd ：获取当前季度的最后一天
* businessQuarterBegin ：获取当前季度的第一个工作日
* businessQuarterEnd ：获取当前季度的最后一个工作日
* isQuarterStart ：判断当天是否为季度的第一天
* isQuarterEnd ：判断当天是否为季度的最后一天

```
quarterBegin(2012.06.12);
// output
2012.04.01

quarterEnd(2012.06.12);
// output
2012.06.30

businessQuarterBegin(2012.06.12);
// output
2012.04.02

businessQuarterEnd(2012.06.12);
// output
2012.06.29

isQuarterStart(2011.01.01);
// output
true

isQuarterEnd(2011.12.31);
// output
true
```

* weekEnd
  ：获取当前星期或下一个星期的星期几（默认为星期一）
* weekBegin
  ：获取当前星期或上一个星期的星期几（默认为星期一）
* lastWeekOfMonth ：获取当月或上一个月最后一周的星期几（默认为星期一）
* weekOfMonth ：获取当月或上一个月第几周的星期几（默认为第一周的星期一）

```
week(2019.11.24);
// output
2019.11.25

weekBegin(2019.11.24);
// output
2019.11.18

lastWeekOfMonth(2019.11.01);
// output
2019.10.28

weekOfMonth(2019.11.01);
// output
2019.10.07
```

* fy5253
  ：获取当前财年开始的第一天
* fy5253Quarter ：获取当前财季开始的第一天

```
fy5253(2016.11.01);
// output
2016.02.01

fy5253Quarter(2016.11.01);
// output
2016.10.31
```

* duration：设置一个时间区间。时间单位可以是常规时间单位或交易日历标识符。

```
duration("5M")
// output: 5M

duration("3XNYS")
// output: 3XNYS
```
