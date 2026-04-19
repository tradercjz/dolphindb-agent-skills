<!-- Auto-mirrored from upstream `documentation-main/stream/stateful_operators.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 有状态算子

有状态算子是指在处理流数据时，需要维护状态的算子。这种算子的输出不仅依赖于当前输入，还依赖于先前的状态或历史记录。在处理完当前输入后，有状态算子会更新其内部状态，并将其用于后续的计算。因此，相同的输入在不同的状态下可能会产生不同的输出。

![](images/stateful_operators_1.png)

## 有状态算子

在 DolphinDB 的部分流计算引擎中，例如状态引擎、时序聚合引擎、window join
引擎，可以使用内置有状态算子。内置的有状态算子经过系统优化，实现了增量计算，可以提高计算性能。在状态引擎中，还可以使用自定义状态算子，以满足用户复杂的流计算需求。

**内置有状态算子**

以下内置函数可以作为响应式状态引擎的有状态算子：

* 累计窗口函数：cumavg, cumsum, cumprod, cumcount, cummin, cummax, cumvar, cumvarp, cumstd, cumstdp, cumcorr, cumcovar, cumbeta, cumwsum, cumwavg, cumfirstNot,
  cumlastNot, cummed, cumpercentile, cumnunique,
  cumPositiveStreak, cummdd, cumcovarp
* 滑动窗口函数：ema, mavg, msum, mcount, mprod, mvar, mvarp, mstd, mstdp, mskew, mkurtosis, mmin, mmax, mimin, mimax, mimaxLast, miminLast, mmed, mpercentile, mrank, mcorr, mcovar, mbeta, mwsum, mwavg, mmad, mfirst, mlast, mslr, tmove, tmfirst, tmlast, tmsum, tmsum2, tmavg, tmcount, tmvar, tmvarp, tmstd, tmstdp, tmprod, tmskew, tmkurtosis, tmmin, tmmax, tmmed, tmpercentile, tmrank, tmcovar, tmbeta, tmcorr, tmwavg, tmwsum, tmoving, moving, sma, wma, dema, tema,
  trima, linearTimeTrend, talib, t3, ma, gema, wilder, mmaxPositiveStreak, movingWindowData, tmovingWindowData, mcovarp, tmcovarp
* 序列相关函数：deltas, ratios, ffill, move, prev, iterate, ewmMean, ewmVar, ewmStd, ewmCov, ewmCorr, prevState, percentChange
* topN 相关函数：msumTopN, mavgTopN, mstdpTopN, mstdTopN, mvarpTopN, mvarTopN, mcorrTopN, mbetaTopN, mcovarTopN, mwsumTopN, cumsumTopN, cumwsumTopN, cumvarTopN, cumvarpTopN, cumstdTopN, cumstdpTopN, cumcorrTopN, cumbetaTopN, cumavgTopN, cumskewTopN, cumkurtosisTopN, mskewTopN,
  mkurtosisTopN,tmsumTopN, tmavgTopN, tmstdTopN, tmstdpTopN, tmvarTopN, tmvarpTopN, tmskewTopN, tmkurtosisTopN, tmbetaTopN, tmcorrTopN, tmcovarTopN, tmwsumTopN, mcovarpTopN, tmcovarpTopN, cumcovarpTopN
* 高阶函数：segmentby (参数 *func* 暂支持 cumsum, cummax, cummin, cumcount,
  cumavg, cumstd, cumvar, cumstdp, cumvarp), moving, byColumn, accumulate, window
* 其他函数：talibNull, dynamicGroupCumsum, dynamicGroupCumcount, topRange, lowRange, trueRange, sumbars
* 特殊函数（仅支持在引擎内使用）：stateIterate, conditionalIterate, genericStateIterate, genericTStateIterate

以下内置函数可以作为时序聚合引擎的有状态算子：

corr, covar, first, last, max, med, min, percentile, quantile, std, var, sum, sum2,
sum3, sum4, wavg, wsum, count, firstNot, ifirstNot, lastNot, ilastNot, imax, imin,
nunique, prod, sem, mode, searchK, beta, avg。

以下内置函数可以作为 window join 引擎的有状态算子：

sum, sum2, avg, std, var, corr, covar, wavg, wsum, beta, max, min, last, first, med,
percentile。

**自定义有状态算子**

用户还可以通过 @state 声明自定义函数，将其封装一个自定义的状态算子。在使用自定义状态函数时，需要注意以下事项：

1. 需在定义前添加声明 "@state"。状态函数只能包含赋值语句和 return 语句。

   自 2.00.9 版本起，支持使用 if-else
   条件语句，且条件只能是标量。

   自2.00.11 版本起，支持使用 for 循环（包含 break, continue
   语句），请注意不支持嵌套 for 循环，且循环次数须小于 100 次。
2. 状态引擎中可以使用无状态函数或者状态函数。但不允许在无状态函数中嵌套使用状态函数。
3. 若赋值语句的右值是一个多返回值的函数（内置函数或自定义函数），则需要将多个返回值同时赋予多个变量。例如：两个返回值的函数 linearTimeTrend
   应用于自定义状态函数中，正确写法为：

   ```
   @state
   def forcast2(S, N){
         linearregIntercept, linearregSlope = linearTimeTrend(S, N)
         return (N - 1) * linearregSlope + linearregIntercept
   }
   ```
4. 在响应式状态引擎中，自定义状态函数不允许包含自赋值语句，如 `a=a+b`。以下示例中，当条件为 false
   时，`iif` 表达式会返回 out，从而导致自赋值（`out =
   out`）并报错。

   ```
   out = iif((p1 > 0) and (p2 == 0), p1, out)
   // An assignment statement in state function 'xxx' can't use self reference
   ```

自定义状态算子在使用上存在一些局限性，例如其运行效率低于内置状态算子，并且仅支持部分语句。为更方便用户开发自定义状态算子，DolphinDB
还提供了更灵活且易于维护的解决方案：

* 使用 DolphinDB Class 开发状态算子。更多信息，请参考使用 DolphinDB Class 来开发流计算状态算子 。

## 有状态算子应用示例

本节我们以涨幅为例介绍如何使用响应式状态引擎进行有状态计算。在股票市场中涨幅指最新成交价格与之前某一刻的历史成交价格的价差的比。本例中将涨幅定义为当前一条行情快照的最新价与上一条行情快照的最新价格的比。

**step1：创建发布流数据表**

```
share(table=streamTable(1:0, `securityID`datetime`lastPrice`openPrice, [SYMBOL,TIMESTAMP,DOUBLE,DOUBLE]), sharedName=`tick)
```

**step2：创建存储处理后数据的共享流数据表**

```
share(table=streamTable(10000:0, `securityID`datetime`factor, [SYMBOL, TIMESTAMP, DOUBLE]), sharedName=`resultTable)
```

**step3：自定义状态算子--涨幅因子**

```
@state
def priceChange(lastPrice){
    return lastPrice \ prev(lastPrice) - 1
}
```

**step4：**创建响应式状态引擎****

```
try{ dropStreamEngine("reactiveDemo") } catch(ex){ print(ex) }
createReactiveStateEngine(name="reactiveDemo",
metrics =<[datetime, priceChange(lastPrice)]>,
dummyTable=tick, outputTable=resultTable, keyColumn="securityID")
```

创建响应式状态引擎时指定
securityID 作为分组列，即计算每支股票各自的价格涨幅。 输入引擎的消息格式同表 tick，结果输出到内存表 resultTable
中。需要计算的指标定义在 *metrics*里。

**step5：订阅发布流数据表**

```
subscribeTable(tableName="tick", actionName="reactiveDemo",
handler=getStreamEngine(`reactiveDemo), msgAsTable=true, offset=-1)
```

**step6：模拟批量数据写入**

```
securityID = ["AA", "AA", "BB", "AA"]
dateTime = [2024.06.02 09:00:00.000, 2024.06.02 09:01:00.000, 2024.06.02 09:03:00.000, 2024.06.02 09:04:00.000]
lastPrice = [9.99, 1.58, 5.37, 9.82]
openPrice = [10.05, 1.50, 5.25, 9.70]
simulateData =  table(securityID, dateTime, lastPrice, openPrice)
tableInsert(tick, simulateData)
```

**step7：查询结果表数据**

```
res = select * from resultTable
```

返回结果
res：

![](images/stateful_operator_3.png)

**step8：取消订阅**

```
unsubscribeTable(tableName="tick", actionName="reactiveDemo")
```

**step9：删除响应式状态引擎**

```
dropStreamEngine(name="reactiveDemo")
```

**step10：删除发布流数据表和结果流数据表**

**注意**：删除发布流数据表前，必须先把其所有订阅取消掉。

```
dropStreamTable(tableName="tick")
dropStreamTable(tableName="resultTable")
```

**相关信息**

* [append!](../funcs/a/append%21.html "append!")
* [createReactiveStateEngine](../funcs/c/createReactiveStateEngine.html "createReactiveStateEngine")
* [dropStreamTable](../funcs/d/dropStreamTable.html "dropStreamTable")
* [subscribeTable](../funcs/s/subscribeTable.html "subscribeTable")
* [unsubscribeTable](../funcs/u/unsubscribeTable.html "unsubscribeTable")
