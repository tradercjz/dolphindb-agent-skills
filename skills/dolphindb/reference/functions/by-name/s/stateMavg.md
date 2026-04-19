# stateMavg

## 语法

`stateMavg(X, window)`

该函数只能用作响应式状态引擎 *metrics* 中的函数。

## 详情

计算基于历史结果的移动平均。

计算逻辑为：若窗口中 *X* 的元素个数小于 *window*，则直接输出 *X*；否则取输出字段前
*window* - 1 个值与当前 *X* 值求平均。

## 参数

**X** 输入表的字段，仅支持数值类型。

**window** 正整数，表示窗口长度。

## 例子

定义一个响应式状态引擎，按照 sym 分组。

对于 A 组数据，窗口大小为 3，当 09:00:02 和 09:00:06 这两条数据到来时，窗口未满，因此直接输出 val 的值
2 和 6 到 total 列。下一条到来的 A 组数据的时间戳为 09:00:08，val=8，此时 A 组的第一个窗口触发计算，计算结果为
(2+6+8)\3=5.333333；接下来一条 A 组数据的时间戳为 09:00:10，val=10，计算结果为
(6+5.333333...+10)\3=7.11111，以此类推。

```
n=10
trade = table(09:00:00 + 1..n as time, rand(`A`B, n) as sym, 1..n as val)

outputTable = table(100:0, `sym`time`total, [STRING, SECOND, DOUBLE])

engine = createReactiveStateEngine(name="test", metrics=[<time>, <stateMavg(val, 3)>], dummyTable=trade, outputTable=outputTable, keyColumn=`sym, keepOrder=true)

engine.append!(trade)
select * from outputTable
```

| sym | time | total |
| --- | --- | --- |
| B | 09:00:01 | 1 |
| A | 09:00:02 | 2 |
| B | 09:00:03 | 3 |
| B | 09:00:04 | 2.6667 |
| B | 09:00:05 | 3.5556 |
| A | 09:00:06 | 6 |
| B | 09:00:07 | 4.4074 |
| A | 09:00:08 | 5.3333 |
| B | 09:00:09 | 5.6543 |
| A | 09:00:10 | 7.1111 |

相关函数：conditionalIterate, stateIterate
