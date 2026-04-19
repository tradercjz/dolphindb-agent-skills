<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/temp_type_conv.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 时序类型和转换

DolphinDB 支持以下九种时序数据类型：

| Data Type | Example |
| --- | --- |
| date | 2013.06.13 |
| month | 2012.06M |
| time | 13:30:10.008 |
| minute | 13:30m |
| second | 13:30:10 |
| datetime | 2012.06.13 13:30:10 or 2012.06.13T13:30:10 |
| timestamp | 2012.06.13 13:30:10.008 or 2012.06.13T13:30:10.008 |
| nanotime | 09:00:01.000100001 |
| nanotimestamp | 2016.12.30T09:00:01.000100001 |

我们可以使用时序类型转换函数把时序数据转换成另一种时序类型的数据。

```
month(2016.02.14);
// output
2016.02M

date(2012.06.13 13:30:10);
// output
2012.06.13

second(2012.06.13 13:30:10);
// output
13:30:10

timestamp(2012.06.13 13:30:10);
// output
2012.06.13T13:30:10.000
```
