# Pattern — tick → OHLC bars

## Problem

Aggregate raw ticks into fixed-interval OHLC (open / high / low / close /
volume) bars, either in batch over DFS history or live via streaming.

## Batch form (DFS history)

```dolphindb
t = loadTable("dfs://tick", `tick)

bars = select
    first(px)  as open,
    max(px)    as high,
    min(px)    as low,
    last(px)   as close,
    sum(vol)   as volume,
    count(*)   as tradeCount
from t
where date between 2024.01.02 : 2024.01.02
group by sym, bar(ts, 60s) as minute
order by sym, minute
```

- `bar(ts, 60s)` floors to the 1-minute bucket.
- For daily bars: `bar(ts, 1d)` or `group by sym, date(ts)`.

### Missing-bar fill

Ticks can have gaps; if you need one row per minute regardless:

```dolphindb
// pre-build the calendar of expected minutes, then left-join
cal = cj(symList, 2024.01.02T09:30 + 0..389 * 60s)
select sym, minute, ... from lj(cal, bars, `sym`minute) csort sym, minute
```

## Streaming form (live)

```dolphindb
share streamTable(1000000:0, `sym`ts`px`vol, [SYMBOL, TIMESTAMP, DOUBLE, INT]) as ticks
share streamTable(1000000:0, `sym`minute`open`high`low`close`volume,
                  [SYMBOL, TIMESTAMP, DOUBLE, DOUBLE, DOUBLE, DOUBLE, LONG]) as bars

// TimeSeries engine: 60-s tumbling window, keyed by sym
engine = createTimeSeriesEngine(
    name         = "ohlc",
    windowSize   = 60000,            // 60 s in ms
    step         = 60000,
    metrics      = <[first(px) as open, max(px) as high, min(px) as low,
                     last(px) as close, sum(vol) as volume]>,
    dummyTable   = ticks,
    outputTable  = bars,
    timeColumn   = `ts,
    useSystemTime = false,
    keyColumn    = `sym
)

subscribeTable(tableName=`ticks, actionName=`ohlc,
               handler=append!{engine}, msgAsTable=true, batchSize=5000, throttle=0.1)
```

Drop-in variants:

- **Sliding window** (e.g. 1-min bar every 10 s): set `step = 10000`.
- **Per-session daily bar**: `createDailyTimeSeriesEngine` with
  `sessionBegins / sessionEnds`.
- **Variable-length buckets** (e.g. by event): `createTimeBucketEngine`.

## Persist bars to DFS

```dolphindb
// bars is a stream table; subscribe to append into DFS
def dfsAppend(msg) {
    loadTable("dfs://bar", `minBar).append!(msg)
}

subscribeTable(tableName=`bars, actionName=`toDfs,
               handler=dfsAppend, msgAsTable=true, batchSize=1000, throttle=1)
```

## Gotchas

- **Out-of-order ticks**: `createTimeSeriesEngine` with
  `useSystemTime=false` drops late ticks. Use `useSystemTime=true` for
  wall-clock windows (trades closing on time regardless of data) or
  `createDailyTimeSeriesEngine` with tolerance.
- **Memory per key** — one state per `keyColumn` value. Bound with
  `keyPurgeFreqInSec`.
- **Nanosecond vs millisecond** — `windowSize` must match the timestamp
  precision (ms for TIMESTAMP, ns for NANOTIMESTAMP).

## See also

- `docs/40-streaming/engines.md`, `docs/40-streaming/subscribe.md`.
- `time_series_engine.md`, `time_bucket_engine.md`.
