<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/format_temp_obj.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 日期和时间的调整及格式

temporalParse
函数能够把字符串转换成 DolphinDB 中的时序类型数据，temporalFormat 函数能够把 DolphinDB 中的时序对象转换成指定格式的字符串。

下表是 DolphinDB 时序对象的格式：

| 格式 | 含义 | 范围 |
| --- | --- | --- |
| yyyy | 年份（4个数字） | 1000-9999 |
| yy | 年份（2个数字 | 00-99. (00-39: 2000-2039; 40-99: 1940-1999) |
| MM | 月份 | 1-12 |
| MMM | 月份 | JAN, FEB, ... DEC （不区分大小写） |
| dd | 日期 | 1-31 |
| HH | 时（24小时制） | 0-23 |
| hh | 时（12小时制） | 0-11 |
| mm | 分钟 | 0-59 |
| ss | 秒 | 0-59 |
| aa | 上午/下午 | AM, PM. （不区分大小写） |
| SSS | 毫秒 | 0-999 |
| nnnnnn | 微秒 | 0-999999 |
| nnnnnnnnn | 纳秒 | 0-999999999 |

*temporalParse* 和 *temporalFormat* 中的 *format* 参数有以下两种表示方式：

## 使用分隔符

对于 *format* 参数，除了 y, M, d, H, h, m, s, a, S,
n以外的符号的字符都可以作为分隔符。format参数中的分隔符需要与输入字符串中的分隔符一致。

```
temporalParse("14-02-2018","dd-MM-yyyy");
// output
2018.02.14

temporalParse("14-02-2018","dd/MM/yyyy");
// output
00d

temporalParse("14//02//2018","dd//MM//yyyy");
// output
2018.02.14

temporalParse("14//02//2018","dd/MM/yyyy");
// output
00d

temporalParse("14//02//2018","dd..MM..yyyy");
// output
00d
```

我们可以使用单个字母来简化格式。例如，使用"y/M/d"代替"yyyy/MM/dd"。因为"y"可以表示"yyyy"和"yy"，系统会根据数字的个数采用"yyyy"或"yy"。

```
temporalParse("14-02-18","d-M-y");
// output
2018.02.14

temporalParse("2018/2/6 02:33:01 PM","y/M/d h:m:s a");
// output
2018.02.06T14:33:01
```

"MMM","SSS", "nnnnnn" , "nnnnnnnnn"不能使用单个字母。

```
temporalParse("02-FEB-2018","d-MMM-y");
// output
2018.02.02

temporalParse("02-FEB-2018","d-M-y");
// output
00d

temporalParse("13:30:10.001","H:m:s.SSS");
// output
13:30:10.001

temporalParse("13:30:10.001","H:m:s.S");
// output
Invalid temporal format: 'H:m:s.S'. Millisecond (S) must have three digits.

temporalParse("13:30:10.008001","H:m:s.nnnnnn");
// output
13:30:10.008001000

temporalParse("13:30:10.008001","H:m:s.n");
// output
Invalid temporal format: 'H:m:s.n'. Nanosecond (n) must have six or nine digits.
```

temporalParse 函数解释输入字符串中数字个数的方式是非常灵活的。

```
temporalParse("2-4-18","d-M-y");
// output
2018.04.02

temporalParse("2-19-6","H-m-s");
// output
02:19:06

temporalParse("002-019-006","H-m-s");
// output
02:19:06
```

对于毫秒，微秒和纳秒，对应的数字位个数必须是3, 6, 9.

```
temporalParse("2018/2/6 13:30:10.001","y/M/d H:m:s.SSS");
// output
2018.02.06T13:30:10.001

temporalParse("2018/2/6 13:30:10.01","y/M/d H:m:s.SSS");
// output
00T

temporalParse("2018/2/6 13:30:10.000001","y/M/d H:m:s.nnnnnn");
// output
2018.02.06T13:30:10.000001000

temporalParse("2018/2/6 13:30:10.0000010","y/M/d H:m:s.nnnnnn");
// output
00N
```

## 不使用分隔符

对于这种表示方式，*format* 参数必须与上述表格中的格式对应，不能使用单个字母来表示格式。

```
temporalParse("20180214","yyyyMMdd");
// output
2018.02.14

temporalParse("122506","MMddyy");
// output
2006.12.25

temporalParse("155950","HHmmss");
// output
15:59:50

temporalParse("035901PM","hhmmssaa");
// output
15:59:01

temporalParse("02062018155956001000001","MMddyyyyHHmmssnnnnnnnnn");
// output
2018.02.06T15:59:56.001000001
```

实际场景下，除了调用 temporalParse 函数外，还可以通过手动编写脚本实现。

例：若时分秒的时间戳被存储为仅包含数字的整型格式，如: 09:30:21 存储为 93021。现在需要将该数据格式化为
DolphinDB 的 SECOND 类型，其格式为 HH:MM:ss。

```
// 模拟生成一批待转换的数据
n = 100000
time = rand(0..23, n) * 10000+ rand(0..60, n) * 100 + rand(0..60, n)

// 方法1：转换为秒后，利用强制类型转换函数 :doc:`/funcs/s/second` 进行转换。
timer second(time / 10000 * 3600 + (time % 10000 / 100) * 60 + (time % 100))
// output
Time elapsed: 1.994 ms

// 方法2：将其转换为字符串后，利用 temporalParse 进行转换。
timer temporalParse(time.format("000000"), "HHmmss")
// output
Time elapsed: 9.974 ms

// 方法3：直接按照现有格式填充成字符串后，利用强制类型转换函数 second 进行转换。
timer second(each(time -> time[:2] + ":" + time[2:4] + ":" + time[4:], lpad(string(time), 6, "0")))
// output
Time elapsed: 1646.833 ms
```

调用 temporalParse 函数解析时间类型数据，在解析性能和脚本复杂度之间进行了折中。
