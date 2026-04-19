# pandas中 DateOffset 传入参数 months，计算结果一致
pd1 = pd.Timestamp("2020.08.31")
print(pd1 -pd.offsets.DateOffset(months=2))
// output
2020-06-30 00:00:00

temporalAdd(datetime(2020.02.29), -1y)
// output
2019.02.28T00:00:00
temporalAdd(datetime(2020.02.29), -4y)
// output
2016.02.29T00:00:00

// pandas 中 offset 设为1年
pd1 = pd.Timestamp("2020.02.29")
print(pd1 - pd.offsets.DateOffset(years=1))
// output
2019-02-28 00:00:00
// pandas 中 offset 设为4年
pd2 = pd.Timestamp("2020.02.29")
print(pd2 - pd.offsets.DateOffset(years=4))
// output
2016-02-29 00:00:00
```
