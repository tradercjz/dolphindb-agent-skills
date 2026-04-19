<!-- Auto-mirrored from upstream `documentation-main/progr/data_mani/null_in_tb.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 表中的空值

```
timestamp = [14:23:35,14:15:03,13:33:30,10:07:59,10:21:34,09:53:41,13:34:52,11:03:24,10:52:13,12:39:42];
qty = 1300 1900 6800 2200 8300 4600 1400 8800 5800 700;
price = 50.76 29.46 174.97 49.6 51.2 50.1 29.1 172.93 173.5 175.1;
sym = `C`MS`IBM`C`C`C`MS`IBM`IBM`IBM$SYMBOL;
qty[qty>4000]=NULL;
price[price<30||price>175]=NULL;
t1 = table(timestamp, sym, qty, price);
t1;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 14:23:35 | C | 1300 | 50.76 |
| 14:15:03 | MS | 1900 |  |
| 13:33:30 | IBM |  | 174.97 |
| 10:07:59 | C | 2200 | 49.6 |
| 10:21:34 | C |  | 51.2 |
| 09:53:41 | C |  | 50.1 |
| 13:34:52 | MS | 1400 |  |
| 11:03:24 | IBM |  | 172.93 |
| 10:52:13 | IBM |  | 173.5 |
| 12:39:42 | IBM | 700 |  |

```
select timestamp, qty, price from t1 where sym=`IBM order by price;
```

| timestamp | qty | price |
| --- | --- | --- |
| 12:39:42 | 700 |  |
| 11:03:24 |  | 172.93 |
| 10:52:13 |  | 173.5 |
| 13:33:30 |  | 174.97 |

```
// select records with prices less than the average price for all trades.
select * from t1 where price<avg(price) order by price;
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 14:15:03 | MS | 1900 |  |
| 13:34:52 | MS | 1400 |  |
| 12:39:42 | IBM | 700 |  |
| 10:07:59 | C | 2200 | 49.6 |
| 09:53:41 | C |  | 50.1 |
| 14:23:35 | C | 1300 | 50.76 |
| 10:21:34 | C |  | 51.2 |

```
// 选出price大于组平均值的记录
select * from t1 where price>contextby(avg, price, sym);
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 14:23:35 | C | 1300 | 50.76 |
| 13:33:30 | IBM |  | 174.97 |
| 10:21:34 | C |  | 51.2 |

```
// 选出price小于组平均值的记录
select * from t1 where price<contextby(avg, price, sym);
```

| timestamp | sym | qty | price |
| --- | --- | --- | --- |
| 10:07:59 | C | 2200 | 49.6 |
| 09:53:41 | C |  | 50.1 |
| 11:03:24 | IBM |  | 172.93 |
| 10:52:13 | IBM |  | 173.5 |
| 12:39:42 | IBM | 700 |  |
