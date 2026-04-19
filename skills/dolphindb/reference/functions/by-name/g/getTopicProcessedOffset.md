# getTopicProcessedOffset

## 语法

`getTopicProcessedOffset(topic)`

## 详情

如果 `subscribeTable` 函数的 *persistOffset* 参数为
true，那么该函数返回最新一条已经处理的订阅数据的偏移量；如果 `subscribeTable` 函数的
*persistOffset* 参数为 false，那么该函数返回-1。

## 参数

**topic** 是 subscribeTable 函数返回的订阅主题。

## 返回值

整型标量。

## 例子

```
share streamTable(1000:0, `time`sym`qty, [TIMESTAMP, SYMBOL, INT]) as trades
trades_1 = streamTable(1000:0, `time`sym`qty, [TIMESTAMP, SYMBOL, INT])
topic=subscribeTable(tableName="trades", actionName="trades_1", offset=0, handler=append!{trades_1}, msgAsTable=true, persistOffset=true)
def writeData(n){
   timev = 2018.10.08T01:01:01.001 + timestamp(1..n)
   symv =take(`A`B, n)
   qtyv = take(1, n)
   insert into trades values(timev, symv, qtyv)
}
writeData(6);
select * from trades_1;
```

| time | sym | qty |
| --- | --- | --- |
| 2018.10.08T01:01:01.002 | A | 1 |
| 2018.10.08T01:01:01.003 | B | 1 |
| 2018.10.08T01:01:01.004 | A | 1 |
| 2018.10.08T01:01:01.005 | B | 1 |
| 2018.10.08T01:01:01.006 | A | 1 |
| 2018.10.08T01:01:01.007 | B | 1 |

```
getTopicProcessedOffset(topic);

// output: 5
```
