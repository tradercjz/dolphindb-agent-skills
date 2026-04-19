# Stream-engine selection — decision tree

## Contents
- The 8 engines (table)
- Decision tree
- Quick examples: reactive state, time-series, cross-sectional, asof join
- Cascading engines / `streamEngineParser`
- Sizing & tuning knobs
- Traps, monitoring, see-also


DolphinDB ships **8 stream engines**. Picking the wrong one is a common
cause of "my factor doesn't update" or "my latency is 10x what it should
be". This page is a decision tree.

## The 8 engines

| Engine | Constructor | Purpose |
|--------|-------------|---------|
| **Reactive state** | `createReactiveStateEngine` | Per-key stateful metrics on every new row. **The default for tick/factor pipelines.** |
| **Time-series** | `createTimeSeriesEngine` | Fixed-duration time window aggregation (1-min bars, 5-min OHLC). |
| **Daily time-series** | `createDailyTimeSeriesEngine` | Same as above but window auto-aligned to trading day. |
| **Session window** | `createSessionWindowEngine` | Gap-closed sessions (user session, trading halt). |
| **Cross-section** | `createCrossSectionalEngine` | Per-timestamp snapshot across all keys (e.g. sector average at each tick). |
| **Asof join** | `createAsofJoinEngine` | Streaming `aj` — merge two streams by key + time. |
| **Equi join / Left-semi / Lookup join** | `create{Equi,LeftSemi,Lookup}JoinEngine` | Streaming joins; pick by semantics. |
| **Anomaly detection** | `createAnomalyDetectionEngine` | Declarative rule → alert stream. |
| **CEP** | `createCEPEngine` | Monitor-style event pattern matching with state machines. See `cep-overview.md`. |

## Decision tree

```
Do you need pattern matching / state machines / alerts?
│
├── YES → CEP (createCEPEngine)  or  Anomaly Detection (simple rules)
│
└── NO → What's the computation shape?
         │
         ├── "Per key (e.g. per symbol), update on every new row"
         │   │
         │   └── Reactive State Engine  ★ most common
         │
         ├── "Aggregate a time window (1 min, 5 min, ...)"
         │   │
         │   ├── Window aligned to trading hours?
         │   │   └── YES → Daily Time-Series Engine
         │   │   └── NO  → Time-Series Engine
         │   │
         │   └── Window defined by activity gap?
         │       └── Session Window Engine
         │
         ├── "At each instant, aggregate across all keys (sector rotation, market breadth)"
         │   │
         │   └── Cross-Sectional Engine
         │
         └── "Join two streams"
             │
             ├── On key + time (asof)        → Asof Join Engine
             ├── On exact key equality        → Equi Join Engine
             ├── Left + optional right        → Left-Semi Join Engine
             └── Lookup static dim            → Lookup Join Engine
```

## Quick examples

### Reactive state — per-symbol rolling factor

```dolphindb
share streamTable(1:0, `sym`ts`price`vol, [SYMBOL, TIMESTAMP, DOUBLE, LONG]) as ticks

engine = createReactiveStateEngine(
    name        = "momentum",
    metrics     = <[ts, mavg(price, 20) as ma20,
                    price / prev(price, 60) - 1 as mom60]>,
    dummyTable  = ticks,
    outputTable = factorStream,
    keyColumn   = `sym)

subscribeTable(tableName=`ticks, actionName=`toEng,
               handler=append!{engine}, msgAsTable=true)
```

### Time-series — 1-minute OHLC

```dolphindb
engine = createTimeSeriesEngine(
    name          = "bars1m",
    windowSize    = 60000,                   // 60 s in ms
    step          = 60000,                   // non-overlapping
    metrics       = <[first(price) as open, max(price) as high,
                      min(price) as low, last(price) as close,
                      sum(vol) as vol]>,
    dummyTable    = ticks,
    outputTable   = bars1m,
    keyColumn     = `sym,
    useSystemTime = false,                   // use row's ts, not wall clock
    timeColumn    = `ts,
    fill          = none)                    // none / null / previous / linear
```

### Cross-sectional — sector average at each instant

```dolphindb
engine = createCrossSectionalEngine(
    name            = "sectorMean",
    metrics         = <[avg(ret) as sectorRet]>,
    dummyTable      = ticks,
    outputTable     = sectorAgg,
    keyColumn       = `sector,
    triggeringPattern = "perBatch")          // or "keyCount" / "interval"
```

### Asof join — attach prevailing quote to each trade

```dolphindb
engine = createAsofJoinEngine(
    name            = "tradeQuote",
    leftTable       = trades,
    rightTable      = quotes,
    outputTable     = tradesWithQuote,
    metrics         = <[trades.price, quotes.bid, quotes.ask]>,
    matchingColumn  = `sym,
    timeColumn      = `ts,
    useSystemTime   = false,
    delayedTime     = 100)                   // ms tolerance
```

## Cascading engines

Engines can feed each other — output one to input the next. Classic:

```
ticks → reactiveStateEngine (tick-freq factor) → timeSeriesEngine (1-min bar) → anomalyEngine (rule)
```

Use `streamEngineParser` to declare the chain and have it wired automatically:

```dolphindb
pipe = streamEngineParser(
    ...
    stages = [
        dict(STRING, ANY, ...reactive stage...),
        dict(STRING, ANY, ...timeseries stage...),
        dict(STRING, ANY, ...anomaly stage...)
    ])
```

Detail: `../tutorials/StreamEngineParser.md`.

## Sizing & tuning

| Knob | Effect |
|------|--------|
| `keyColumn`            | Must match your partition key for factor correctness. |
| `keyPurgeFreqInSec`    | Reactive state engine: drop per-key state after idle. Prevents unbounded memory for wide universes. |
| `outputTable` as DFS vs share | Write-heavy: DFS (batched). Subscriber-heavy: `share` a stream table. |
| `useSystemTime=false`  | Default in production. `true` only for demos (clock-driven). |
| `throttle` on `subscribeTable` | Trade latency for throughput. |
| `hash` on `subscribeTable`     | Route different keys to different worker threads. |

## Traps

- **`group by` inside engine metrics fails** — use reactive-state's
  per-key implicit grouping, or pre-group upstream.
- **`createTimeSeriesEngine` without `keyColumn`** aggregates globally.
  Set `keyColumn=`sym` for per-symbol bars.
- **`useSystemTime=true`** ignores the row's `ts` and uses wall clock.
  Wrong for backfill / replay.
- **Engine state is in memory only.** On restart, all per-key state is
  lost. Pre-replay recent rows from DFS on startup (see
  `../patterns/stream-recovery-after-restart.md`).
- **Output table not `share`d** → downstream subscribers can't find it.
- **Reactive-state factor references `high` / `low` of current row** —
  fine if input is a tick, wrong if input is a bar with a close-time
  lookahead. See `../backtest/factors.md`.
- **CEP vs Anomaly** — Anomaly engine handles per-key declarative rules
  (`rule` syntax); CEP handles multi-event state machines. Don't reach
  for CEP if one threshold rule suffices.

## Monitoring

```dolphindb
getStreamEngineStat()                       // all engines on this node
getStreamEngineStat().reactiveStateEngine   // reactive-state-specific
```

Per-engine row counts, cumulative output, memory usage.

## See also

- `engines.md` — full reference on every engine's constructor args.
- `stream-table.md`, `subscribe.md`.
- `cep-overview.md`.
- `../patterns/stream-ingestion-to-dfs.md`,
  `../patterns/stream-recovery-after-restart.md`.
- `../backtest/factors.md` — `@state` factor design (feeds reactive engine).
- `../tutorials/streaming_tutorial.md`, `reactive_state_engine.md`,
  `stream_aggregator.md`, `StreamEngineParser.md`,
  `Anomaly_Detection_Engine.md`, `getting_started_with_cep_engine.md`.
