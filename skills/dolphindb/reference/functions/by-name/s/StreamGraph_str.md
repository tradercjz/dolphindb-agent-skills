# StreamGraph::str

首发版本：3.00.3

## 语法

`StreamGraph::str()`

## 详情

以字符串格式输出流图拓扑结构。

## 返回值

STRING 类型标量。

## 例子

```
// g 是流图
g.str()

/*
当 g 尚未提交
{name=engine_3, id=3, subgraphId=-1, taskId=-1, type=REACTIVE_STATE_ENGINE, parallelism=1} ---> {name=mycl.orca_table.one_min_indicators, id=4, subgraphId=-1, taskId=-1, type=TABLE, parallelism=1}
    properties(from)={type=REACTIVE_STATE_ENGINE, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], arguments= [engine_3,(< time >,< high >,< low >,< close >,< volume >,< EMA(close, 20) as ema20 >,< EMA(close, 60) as ema60 >,< MACD(close) as `dif`dea`macd >,< KDJ(close, high, low) as `k`d`j >),[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE],symbol,,,,,,,,,,]}
    properties(to)={type=TABLE, id_=76ed5cea-16b3-22a9-3446-3a2eaf2d7083, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], filterColumn_=}
    edge={id=3, partition=FORWARD, handler=[]}
{name=mycl.orca_table.one_min_bar, id=2, subgraphId=-1, taskId=-1, type=TABLE, parallelism=1} ---> {name=engine_3, id=3, subgraphId=-1, taskId=-1, type=REACTIVE_STATE_ENGINE, parallelism=1}
    properties(from)={type=TABLE, id_=39008be5-47a0-b09f-6045-58e2abe24d72, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], filterColumn_=}
    properties(to)={type=REACTIVE_STATE_ENGINE, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], arguments= [engine_3,(< time >,< high >,< low >,< close >,< volume >,< EMA(close, 20) as ema20 >,< EMA(close, 60) as ema60 >,< MACD(close) as `dif`dea`macd >,< KDJ(close, high, low) as `k`d`j >),[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE],symbol,,,,,,,,,,]}
    edge={id=2, partition=FORWARD, handler=[]}
{name=mycl.orca_table.trade, id=0, subgraphId=-1, taskId=-1, type=TABLE, parallelism=1} ---> {name=engine_1, id=1, subgraphId=-1, taskId=-1, type=TIME_SERIES_ENGINE, parallelism=1}
    properties(from)={type=TABLE, id_=1d690e44-22aa-049c-ad47-83aa48f75add, schema=[DATETIME,SYMBOL,DOUBLE,LONG], filterColumn_=}
    properties(to)={type=TIME_SERIES_ENGINE, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], arguments= [engine_1,60,60,(< first(price) as open >,< max(price) as high >,< min(price) as low >,< last(price) as close >,< sum(volume) as volume >),[DATETIME,SYMBOL,DOUBLE,LONG],[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],time,,symbol,,,,,,,,,,,,,,,]}
    edge={id=0, partition=FORWARD, handler=[]}
{name=engine_1, id=1, subgraphId=-1, taskId=-1, type=TIME_SERIES_ENGINE, parallelism=1} ---> {name=mycl.orca_table.one_min_bar, id=2, subgraphId=-1, taskId=-1, type=TABLE, parallelism=1}
    properties(from)={type=TIME_SERIES_ENGINE, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], arguments= [engine_1,60,60,(< first(price) as open >,< max(price) as high >,< min(price) as low >,< last(price) as close >,< sum(volume) as volume >),[DATETIME,SYMBOL,DOUBLE,LONG],[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],time,,symbol,,,,,,,,,,,,,,,]}
    properties(to)={type=TABLE, id_=39008be5-47a0-b09f-6045-58e2abe24d72, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], filterColumn_=}
    edge={id=1, partition=FORWARD, handler=[]}
*/

/*
当 g 已经提交
{name=channel_6, id=6, subgraphId=2, taskId=0, type=CHANNEL, parallelism=1} ---> {name=engine_3, id=3, subgraphId=2, taskId=0, type=REACTIVE_STATE_ENGINE, parallelism=1}
    properties(from)={type=CHANNEL, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], arguments= [channel_6,[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE],aebdc8bf-1fe8-c0a5-6149-3b1b250d66d3,[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE]]}
    properties(to)={type=REACTIVE_STATE_ENGINE, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], arguments= [engine_3,(< time >,< high >,< low >,< close >,< volume >,< EMA(close, 20) as ema20 >,< EMA(close, 60) as ema60 >,< MACD(close) as `dif`dea`macd >,< KDJ(close, high, low) as `k`d`j >),[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE],symbol,,,,,,,,,,]}
    edge={id=7, partition=FORWARD, handler=[]}
{name=engine_3, id=3, subgraphId=2, taskId=0, type=REACTIVE_STATE_ENGINE, parallelism=1} ---> {name=mycl.orca_table.one_min_indicators, id=4, subgraphId=2, taskId=0, type=TABLE, parallelism=1}
    properties(from)={type=REACTIVE_STATE_ENGINE, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], arguments= [engine_3,(< time >,< high >,< low >,< close >,< volume >,< EMA(close, 20) as ema20 >,< EMA(close, 60) as ema60 >,< MACD(close) as `dif`dea`macd >,< KDJ(close, high, low) as `k`d`j >),[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE],symbol,,,,,,,,,,]}
    properties(to)={type=TABLE, id_=76ed5cea-16b3-22a9-3446-3a2eaf2d7083, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], filterColumn_=}
    edge={id=3, partition=FORWARD, handler=[]}
{name=engine_1, id=1, subgraphId=1, taskId=2, type=TIME_SERIES_ENGINE, parallelism=1} ---> {name=mycl.orca_table.one_min_bar, id=2, subgraphId=1, taskId=2, type=TABLE, parallelism=1}
    properties(from)={type=TIME_SERIES_ENGINE, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], arguments= [engine_1,60,60,(< first(price) as open >,< max(price) as high >,< min(price) as low >,< last(price) as close >,< sum(volume) as volume >),[DATETIME,SYMBOL,DOUBLE,LONG],[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],time,,symbol,,,,,,,,,,,,,,,]}
    properties(to)={type=TABLE, id_=39008be5-47a0-b09f-6045-58e2abe24d72, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], filterColumn_=}
    edge={id=1, partition=FORWARD, handler=[]}
{name=mycl.orca_table.trade, id=0, subgraphId=0, taskId=1, type=TABLE, parallelism=1} ---> {name=channel_5, id=5, subgraphId=1, taskId=2, type=CHANNEL, parallelism=1}
    properties(from)={type=TABLE, id_=1d690e44-22aa-049c-ad47-83aa48f75add, schema=[DATETIME,SYMBOL,DOUBLE,LONG], filterColumn_=}
    properties(to)={type=CHANNEL, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], arguments= [channel_5,[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],e57e4a2d-663f-9eb6-004d-e777b4adda89,[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG]]}
    edge={id=4, partition=FORWARD, handler=[]}
{name=channel_5, id=5, subgraphId=1, taskId=2, type=CHANNEL, parallelism=1} ---> {name=engine_1, id=1, subgraphId=1, taskId=2, type=TIME_SERIES_ENGINE, parallelism=1}
    properties(from)={type=CHANNEL, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], arguments= [channel_5,[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],e57e4a2d-663f-9eb6-004d-e777b4adda89,[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG]]}
    properties(to)={type=TIME_SERIES_ENGINE, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], arguments= [engine_1,60,60,(< first(price) as open >,< max(price) as high >,< min(price) as low >,< last(price) as close >,< sum(volume) as volume >),[DATETIME,SYMBOL,DOUBLE,LONG],[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG],time,,symbol,,,,,,,,,,,,,,,]}
    edge={id=5, partition=FORWARD, handler=[]}
{name=mycl.orca_table.one_min_bar, id=2, subgraphId=1, taskId=2, type=TABLE, parallelism=1} ---> {name=channel_6, id=6, subgraphId=2, taskId=0, type=CHANNEL, parallelism=1}
    properties(from)={type=TABLE, id_=39008be5-47a0-b09f-6045-58e2abe24d72, schema=[DATETIME,SYMBOL,DOUBLE,DOUBLE,DOUBLE,DOUBLE,LONG], filterColumn_=}
    properties(to)={type=CHANNEL, schema=[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE], arguments= [channel_6,[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE],aebdc8bf-1fe8-c0a5-6149-3b1b250d66d3,[SYMBOL,DATETIME,DOUBLE,DOUBLE,DOUBLE,LONG,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE,DOUBLE]]}
    edge={id=6, partition=FORWARD, handler=[]}
*/
```
