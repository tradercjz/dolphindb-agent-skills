# 按照行标签重组
label = 1 2 1 2
regroup(X=m, label=label, func=firstNot, byRow=true)
```

| label | col1 | col2 | col3 | col4 | col5 |
| --- | --- | --- | --- | --- | --- |
| 1 | 11 | 6 | 6 | 10 | 4 |
| 2 | 6 | 7 | 5 | 2 | 16 |

例2：内置函数和用户自定函数的性能对比

```
m = rand(1000.0, 10000)$100:100
defg my_avg(v):avg(v)

timer(1000) regroup(m, take(1 2 3 4 5, 100), avg)
// output
Time elapsed: 176.175 ms

timer(1000) regroup(m, take(1 2 3 4 5, 100), my_avg)
// output
Time elapsed: 1062.553 ms
```

例3：对面板数据进行分钟聚合

```
n=1000
timestamp = 09:00:00 + rand(10000, n).sort!()
id = take(`st1`st2`st3, n)
vol = 100 + rand(10.0, n)
vt = table(timestamp, id, vol)
m = exec vol from vt pivot by timestamp, id
regroup(m, minute(m.rowNames()), avg)
```
