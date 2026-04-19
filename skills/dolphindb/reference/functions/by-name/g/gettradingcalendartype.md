# getTradingCalendarType

## 语法

`getTradingCalendarType(marketName)`

## 详情

获取指定交易所对应的交易日历的类型。返回值是字符串标量，为 "holidayDate" 或 "tradingDate"。

## 参数

**marketName** 字符串标量，表示交易日历标识，例如：国外交易所的 ISO Code、国内交易所简称或自定义交易日历名称。

## 返回值

字符串标量，为 "holidayDate" 或 "tradingDate"。

## 例子

运行以下命令获取交易日历类型：

```
getTradingCalendarType("SZSE")
```

返回：holidayDate

**相关信息**

* [updateMarketHoliday](../u/updateMarketHoliday.html "updateMarketHoliday")
* [getMarketCalendar](getMarketCalendar.html "getMarketCalendar")
* [addMarketHoliday](../a/addMarketHoliday.html "addMarketHoliday")
