# 计算累计和并根据阈值打标签
t1 = select *, cumsum(volume) as sumVolume from t context by sym, orderNo
t2 = lj(t, t1,`sym`time`orderNo)
t3 = select sym, time, orderNo, volume, sumVolume, tag_func(sumVolume) as groupId from t2
```

对于历史数据，可以使用 SQL 语句计算不同组的累计记录数：

```
t4 = select sym, time, orderNo, prev(groupId) as prevGroupId from t3 context by sym,orderNo
t5 = lj(t3, t4,`sym`time`orderNo)
re = select sym, time, orderNo, dynamicGroupCumcount(groupId, prevGroupId, 3) as `groupId0`groupId1`groupId2 from t5 context by sym
re
```

| sym | time | orderNo | groupId0 | groupId1 | groupId2 |
| --- | --- | --- | --- | --- | --- |
| st0 | 2022.01.01T09:00:00.001 | 10001 | 1 | 0 | 0 |
| st0 | 2022.01.01T09:00:00.002 | 10002 | 2 | 0 | 0 |
| st0 | 2022.01.01T09:00:00.003 | 10001 | 1 | 1 | 0 |
| st1 | 2022.01.01T09:00:00.001 | 10002 | 1 | 0 | 0 |
| st1 | 2022.01.01T09:00:00.002 | 10003 | 2 | 0 | 0 |
| st1 | 2022.01.01T09:00:00.003 | 10002 | 1 | 0 | 1 |

对于实时数据，可以使用流数据引擎计算不同组的累计记录数：

```
result = table(1000:0, `sym`time`orderNo`groupId0`groupId1`groupId2, [SYMBOL, TIME, SYMBOL,INT,INT,INT])
factor0 = [<time>,  <prev(groupId) as prevGroupId>, <groupId>, <volume>]
factor1 = [<time>, <orderNo>, <dynamicGroupCumcount(groupId, prevGroupId, 3)>]
dm1 = table(1000:0, `sym`time`orderNo`volume`sumVolume`groupId, [SYMBOL, TIME, SYMBOL,INT, INT,INT])
dm2 = table(1000:0, `sym`orderNo`time`prevGroupId`groupId`volume, [SYMBOL, SYMBOL, TIME, INT,INT,INT])
res1 = createReactiveStateEngine(name="reactive_ccnt", metrics =factor1, dummyTable=dm2, outputTable=result, keyColumn=`sym, keepOrder=true)
res0 = createReactiveStateEngine(name="reactive_prev", metrics =factor0, dummyTable=dm1, outputTable=res1, keyColumn=`sym`orderNo, keepOrder=true)
res0.append!(t3)

select * from result
```

| sym | time | orderNo | groupId0 | groupId1 | groupId2 |
| --- | --- | --- | --- | --- | --- |
| st0 | 2022.01.01T09:00:00.001 | 10001 | 1 | 0 | 0 |
| st0 | 2022.01.01T09:00:00.002 | 10002 | 2 | 0 | 0 |
| st0 | 2022.01.01T09:00:00.003 | 10001 | 1 | 1 | 0 |
| st1 | 2022.01.01T09:00:00.001 | 10002 | 1 | 0 | 0 |
| st1 | 2022.01.01T09:00:00.002 | 10003 | 2 | 0 | 0 |
| st1 | 2022.01.01T09:00:00.003 | 10002 | 1 | 0 | 1 |

```
dropStreamEngine("reactive_ccnt")
dropStreamEngine("reactive_prev")
```

相关函数：dynamicGroupCumsum
