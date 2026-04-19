# Pattern — asof-join trades with quotes

## Problem

Enrich each **trade** with the **prevailing quote** (latest bid/ask at the
time of the trade) for the same symbol.

## When to use / not use

| Use | Don't use |
|-----|-----------|
| Time-series join where right-side timestamps differ | Both sides share timestamps exactly → `ej`. |
| Need the **latest** right-side row at-or-before left time | Need all matching right rows → `wj` or `ej`. |

## Solution

```dolphindb
// example source tables
trades = table(
    2024.01.02T09:30:00.500 2024.01.02T09:30:01.200 2024.01.02T09:30:02.100 as ts,
    `AAPL`AAPL`AAPL                                                           as sym,
    100.1 100.2 100.3                                                         as px,
    100 50 200                                                                as qty
)

quotes = table(
    2024.01.02T09:30:00.100 2024.01.02T09:30:00.800 2024.01.02T09:30:01.500
                                                                  2024.01.02T09:30:02.000 as ts,
    `AAPL`AAPL`AAPL`AAPL                                                                  as sym,
    99.9 100.05 100.15 100.25                                                              as bid,
    100.1 100.15 100.25 100.35                                                             as ask
)

// right-side must be sorted by (sym, ts)
quotes = select * from quotes order by sym, ts

// asof join
enriched = select *, bid, ask
from aj(trades, quotes, `sym`ts)
```

Result: every trade row gets the `bid` / `ask` from the latest quote at or
before its `ts`. The first trade may have nulls if no prior quote exists.

## Variants

### Windowed aggregate instead of point lookup

Average bid over the last second before each trade:

```dolphindb
select * from wj(
    trades, quotes,
    -1000:0,                       // window in ms
    <[avg(bid) as avg_bid]>,
    `sym`ts
)
```

### On DFS tables

Both sides can be DFS tables; asof join will stream partitions efficiently
as long as both have the same partition keys and the right side is
TSDB-sorted on `(sym, ts)`.

### Streaming (continuous)

Use `createAsofJoinEngine` for a live trade-quote join:

```dolphindb
share streamTable(1000:0, schema(trades).colDefs.name, schema(trades).colDefs.typeString) as tradeIn
share streamTable(1000:0, schema(quotes).colDefs.name, schema(quotes).colDefs.typeString) as quoteIn

engine = createAsofJoinEngine(
    name           = "tradeQuote",
    leftTable      = tradeIn,
    rightTable     = quoteIn,
    outputTable    = enrichedSink,
    metrics        = <[px, qty, bid, ask]>,
    matchingColumn = `sym,
    timeColumn     = `ts,
    useSystemTime  = false
)

subscribeTable(tableName=`tradeIn, actionName=`toEngine, handler=append!{engine.getLeftStream()}, msgAsTable=true)
subscribeTable(tableName=`quoteIn, actionName=`toEngine, handler=append!{engine.getRightStream()}, msgAsTable=true)
```

## Gotchas

- **Right side must be sorted** by `(sym, ts)`. Unsorted → silently wrong.
- **Type mismatch** between `sym` on left and right (SYMBOL vs STRING) →
  zero matches. Cast explicitly.
- **Null timestamps** never match; drop them first.
- **Late quotes** (quotes arriving after the trade's time) won't appear in
  the asof result. If you also care about the *next* quote, use
  `nearestJoinEngine` instead.

## See also

- `docs/20-sql/join.md`, `docs/40-streaming/engines.md`.
- `asofjoin.md`, `asof_join_engine.md`,
  `nearest_join_engine.md`.
