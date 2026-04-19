# Factor computation & factor-based backtesting

## Contents
- The golden rule: point-in-time + `@state`
- Three execution modes (batch / streaming / backtest) — same factor
- Lookahead bias — audit rules
- PIT (point-in-time) fundamental data
- Factor evaluation workflow (compute → neutralize → lag → IC → buckets → backtest)
- Offline vectorized SQL factor backtest
- Built-in factor libraries (`wq101alpha`, `gtja191Alpha`, `ta`, `mytt`)
- Streaming HF factors, performance, common mistakes


Factors (alphas) are the heart of most DolphinDB quant workloads. The same
factor definition can run in three places — **batch** (over DFS history),
**streaming** (online, via reactive state engine), and **inside a
backtest** — and the engine requires the definition to be **point-in-time
correct** in every case.

## The golden rule: point-in-time + `@state`

A factor function in DolphinDB is a **vectorized function** operating on
per-symbol time series. To be reusable across batch / streaming /
backtest, tag it with `@state` and use only **past-and-current** values:

```dolphindb
@state
def momentum20(close) {
    return close / prev(close, 20) - 1
}

@state
def volRatio(volume, price) {
    return mavg(volume, 20) / mavg(abs(prev(price, 1) - price) / price, 20)
}
```

- `@state` marks the function as a **reactive-state metric**. The engine
  will maintain per-key state and emit one output per input tick.
- Only use past values (`prev`, `mavg`, `cumsum`, `msum`, `mcorr`, …) on
  the input vectors — never the current row alone unless the strategy
  executes at the same instant (e.g. end-of-bar close).
- Functions **without** `@state` are OK for pure vector compute but may
  not be usable in streaming/reactive engines.

See `../10-language/functions.md` for `@state` details and
`../40-streaming/engines.md#reactive-state-engine` for the runtime.

## Three execution modes — same factor definition

### A. Batch over DFS (research)

```dolphindb
t = loadTable("dfs://tick", `snap)
    where date = 2024.01.02 and sym in universe

select sym, ts, close,
       momentum20(close)    as mom20,
       volRatio(vol, close) as volR
from t
context by sym csort ts
```

`context by sym csort ts` is the only incantation you need. Don't use
`group by` — that collapses rows.

### B. Streaming (online)

```dolphindb
share streamTable(...) as ticks

engine = createReactiveStateEngine(
    name       = "factorEngine",
    metrics    = <[momentum20(close) as mom20,
                   volRatio(vol, close) as volR]>,
    dummyTable = ticks,
    outputTable = factorStream,
    keyColumn  = `sym
)

subscribeTable(tableName=`ticks, actionName=`toEngine,
               handler=append!{engine}, msgAsTable=true)
```

Each new tick fires the engine, output goes into `factorStream`.

### C. Inside backtest

Use `Backtest::subscribeIndicator` which internally spins up a reactive
engine with the same metrics:

```dolphindb
def initialize(mutable context) {
    Backtest::subscribeIndicator(
        engine     = context.engine,
        metrics    = <[momentum20(close) as mom20, volRatio(vol, close) as volR]>,
        keyColumn  = `sym,
        dummyTable = snapshotSchema
    )
}

def onSnapshot(mutable context, msg, indicator) {
    for (sym in msg.keys()) {
        mom = indicator[sym].mom20
        if (isValid(mom) && mom > 0.02) {
            Backtest::submitOrder(context.engine,
                (sym, context.tradeTime, 5, msg[sym].lastPx, 100, 1), "mom_entry")
        }
    }
}
```

Three modes, one factor function. This is a core DolphinDB value-add.

## Lookahead bias — the most common error

The factor is fed the **current bar** including the current close. That's
only "live" information if you also execute at bar-close. Two rules:

| Execution time | Valid factor inputs |
|----------------|---------------------|
| **At bar close** (end-of-bar strategy) | current bar values **are** known → `mavg(close, 5)` is fine |
| **At next-bar open** | shift by one: `prev(mavg(close, 5), 1)` or compute factor on previous bar and lag by 1 |

Common leak patterns to audit for:

- Using `high` / `low` / `close` of the **current bar** to decide a trade
  that fills **during** the bar → impossible in reality.
- Using T-day close to compute T-day open decision.
- Joining a future fundamental (e.g. earnings release) on the release
  date before it was public — use `asof join` on the release timestamp.
- Returns computed as `(close[t+1] - close[t]) / close[t]` but used as a
  feature at time `t`. Shift returns by one bar.

## PIT (point-in-time) fundamental data

Fundamental data (earnings, ratings, reports) must be joined **at the
timestamp it was first publicly available**, not at the as-of date. Use:

```dolphindb
// fundamentals has (sym, report_date, release_ts, eps, ...)
select t.*, f.eps
from aj(ticks, select sym, release_ts as ts, eps from fundamentals, `sym`ts)
```

Never `lj ... on report_date = date(ts)` — that leaks the release early.

## Factor evaluation workflow

1. **Compute** — run factor against DFS history (mode A).
2. **Neutralize** — de-mean by sector / market-cap, `rowRank`, winsorize
   with `winsorize` / `rowWinsorize`.
3. **Lag** — add a 1-bar lag to avoid lookahead (`prev(factor, 1)`).
4. **IC / rank-IC** — correlate with forward returns:
   ```dolphindb
   ic = select mcorr(factor, fwd_ret, 252) as ic from t context by date
   ```
5. **Portfolio formation** — bucket by factor quantile (`bucket` or
   `cutPoints`), compute bucket returns.
6. **Backtest** — long top bucket, short bottom, hold N days. Use Backtest
   plugin or the offline approach below.

Upstream tutorial (must-read): `../tutorials/best_practice_for_factor_calculation.md`
and `../tutorials/best_practices_for_multi_factor.md`.

## Offline quick-and-dirty factor backtest

For factor research you often don't need the full event-driven engine —
a vectorized SQL backtest is 100× faster and good enough:

```dolphindb
// signal: top-quintile long, bottom-quintile short, hold 1 day
signal = select sym, date, factor,
              iif(rowRank(factor) >= 0.8, 1, iif(rowRank(factor) <= 0.2, -1, 0)) as w
         from ranked
         context by date                 // rank across symbols per day

pnl = select date, sum(w * fwd_ret) / sum(abs(w)) as daily_ret
      from signal context by date

cumCurve = select date, cumprod(1 + daily_ret) - 1 as cum from pnl
```

Takes seconds to iterate. Use the Backtest plugin (`backtest-plugin-guide.md`)
only when you need:
- Realistic slippage / commission.
- Position / cash tracking across days.
- Per-asset risk rules.
- Execution micro-structure (queue position, matching).

## Built-in factor libraries

Two modules ship pre-built alpha factors — good starting points:

| Module | File | Coverage |
|--------|------|----------|
| `wq101alpha` | `../modules/wq101alpha/wq101alpha.md` | WorldQuant 101 alphas |
| `gtja191Alpha` | `../modules/gtja191Alpha/191alpha.md` | 国泰君安 191 alpha |
| `ta` | `../modules/ta/ta.md` | TA-Lib technical indicators |
| `mytt` | `../modules/mytt/mytt.md` | Minimalist TA set |

```dolphindb
use wq101alpha
a1 = wq101alpha::alpha1(close, returns)      // per-sym vector
```

## Streaming HF factors

For **tick / L2** frequency factors that need to run live:

- `reactiveStateEngine` with `@state` factors — see mode B above.
- Cascade with `timeSeriesEngine` for minute-bar aggregation:
  ticks → factors (tick freq) → 1-min bars → factor summary.
- For complex cascades, let `streamEngineParser` auto-compose the pipeline.
  See `../40-streaming/engines.md`.

Tutorials: `../tutorials/hf_factor_streaming.md`,
`../tutorials/l2_snapshot_factor_calc.md`,
`../tutorials/hf_to_lf_factor.md`.

## Performance

- **Per-key state** grows with the number of symbols. Cap with
  `keyPurgeFreqInSec` on reactive engines.
- **`@state` overhead** is small but non-zero; for pure batch, plain
  vectorized SQL (`context by`) is fastest.
- **JIT** (`createBacktester(..., jit=true)`) compiles your callback +
  factor chain; worth it for 1000+ symbol × L2 tick workloads.

## Common mistakes

- **Forgetting `@state`** for a factor used inside a streaming engine.
  Silent wrong outputs (per-key state not maintained).
- **Using `group by` when you meant `context by`** — collapses rows.
- **Missing `csort` inside `context by`** when source data is not time-
  ordered → rolling windows see garbage.
- **Joining fundamentals by report date** (not release timestamp) →
  look-ahead leak.
- **Same-bar execution of a factor computed from same-bar close** →
  look-ahead leak. Shift by one bar.
- **Mixing SYMBOL and STRING keys** between factor table and return
  table → empty joins silently.
- **Factor NaN / inf** → wrap with `nullFill` / `nanInfFill` before
  using in `context by` with `mavg` family; otherwise the window
  propagates.

## See also

- `backtest-plugin-guide.md`, `traps.md`.
- `../10-language/functions.md` — `@state`, vectorized functions.
- `../20-sql/context-by.md` — per-group vectorized compute.
- `../40-streaming/engines.md` — reactive state & time-series engines.
- `../tutorials/README.md` → Factor calculation section.
- `../modules/README.md` — built-in factor libraries.
