# One-page cheatsheet — the top traps & idioms

A compressed reference for agents under token pressure. Each item links
to a full doc for depth.

## Contents
- SQL top-5 traps
- Time & null top-3 traps
- Streaming & backtest top-3 traps
- Performance quick rules
- Canonical snippets (copy-paste)

---

## SQL top-5 traps

| # | Wrong | Right | Why |
|---|-------|-------|-----|
| 1 | `select ... group by sym` for per-sym rolling | `context by sym csort ts` | `group by` collapses rows; `context by` keeps them. → `20-sql/context-by.md` |
| 2 | `where year(date) = 2024` | `where date between 2024.01.01 : 2024.12.31` | Function on partition key blocks pruning. → `70-perf/partition-pruning.md` |
| 3 | `aj(trades, quotes, \`sym\`ts)` with `TIMESTAMP` vs `NANOTIMESTAMP` | cast both sides to same type, sort both | Silent 0-row join. → `20-sql/asof-join.md` |
| 4 | `join ... on f(a) = b` | precompute key column, then plain `ej`/`lj` | Function in join key defeats indexes. → `20-sql/joins-overview.md` |
| 5 | `x == NULL` | `isValid(x)` | NULLs are typed sentinels, not a state. → `10-language/null-handling.md` |

## Time & null top-3 traps

| # | Symptom | Fix |
|---|---------|-----|
| 1 | `aj` returns 0 rows | **match temporal types exactly** on both sides (TIMESTAMP ≠ NANOTIMESTAMP). → `10-language/time-types.md` |
| 2 | Rolling `mavg(x, 20)` yields all-null for 20+ rows | `mavg(ffill(x), 20)` inside same `context by` block. → `10-language/null-handling.md` |
| 3 | `iif(x, 1, 0)` silently counts null ints as true | always route boolean tests on integers through `isValid(x) and x > 0`. |

## Streaming & backtest top-3 traps

| # | Symptom | Fix |
|---|---------|-----|
| 1 | Factor in reactive engine emits garbage per key | **missing `@state` decorator** on the factor function. → `backtest/factors.md` |
| 2 | Subscribers replay everything after restart | `enableTableShareAndPersistence` + `subscribeTable(persistOffset=true)` + DFS `keepDuplicates=LAST`. → `patterns/stream-recovery-after-restart.md` |
| 3 | Look-ahead bias in backtest fills | execute on **next-bar open**, not current-bar close; shift factors by `prev(..., 1)`. → `backtest/traps.md` |

## Performance quick rules

- **Pruning first** — if partition column isn't in WHERE without a function wrapper, nothing else matters.
- **TSDB sort columns** — `sortColumns=\`sym\`ts` (key filter column first, ts last).
- **Select narrow** — `select sym, ts, price` not `select *`.
- **`context by` > per-sym subqueries.** Always.
- **Don't `@jit` table code** — SQL engine is already vectorized; `@jit` is for scalar loops.
- **`tableAppender` / `PartitionedTableAppender`** for Python writes, not per-row `append!`.

## Canonical snippets

### Create a TSDB DFS tick table

```dolphindb
dbDate = database("", VALUE, 2024.01.01..2030.12.31)
dbSym  = database("", HASH,  [SYMBOL, 20])
db     = database("dfs://tick", COMPO, [dbDate, dbSym], engine="TSDB")
db.createPartitionedTable(
    table(1:0, `ts`sym`price`vol, [TIMESTAMP, SYMBOL, DOUBLE, LONG]),
    `trade, `ts`sym,
    sortColumns    = `sym`ts,
    keepDuplicates = ALL)
```

### 1-minute OHLC from ticks

```dolphindb
select sym, bar(ts, 60_000) as minute,
       first(price) as open, max(price) as high,
       min(price)   as low,  last(price) as close,
       sum(vol)     as vol
from ticks
group by sym, bar(ts, 60_000)
```

### Attach prevailing quote to trades

```dolphindb
sortBy!(trades, `sym`ts); sortBy!(quotes, `sym`ts)
r = aj(trades, quotes, `sym`ts)
```

### Reactive state factor

```dolphindb
@state
def mom20(close) { return close / prev(close, 20) - 1 }

engine = createReactiveStateEngine(
    name="mom", metrics=<[mom20(close) as mom]>,
    dummyTable=ticks, outputTable=factorStream, keyColumn=`sym)

subscribeTable(tableName=`ticks, actionName=`toEng,
               handler=append!{engine}, msgAsTable=true)
```

### Persistent stream + DFS subscriber (recoverable)

```dolphindb
enableTableShareAndPersistence(
    table=streamTable(1_000_000:0, `ts`sym`px`vol,
                      [TIMESTAMP, SYMBOL, DOUBLE, INT]),
    tableName=`ticks, asynWrite=true, cacheSize=1_000_000,
    retentionMinutes=1440)

subscribeTable(tableName=`ticks, actionName=`toDfs,
    handler=def(m){loadTable("dfs://tick",`trade).append!(m)},
    msgAsTable=true, batchSize=10000, throttle=1,
    persistOffset=true, reconnect=true)
```

### Python connect + Arrow read

```python
import dolphindb as ddb, pandas as pd
s = ddb.session(); s.connect("localhost", 8848, "admin", "123456")
pdf = s.runArrow(
    "select * from loadTable('dfs://tick',`trade) where date=2024.03.15"
).to_pandas(types_mapper=pd.ArrowDtype)
```

### Look up an error by code

```bash
python skills/dolphindb/scripts/lookup.py error S00012
python skills/dolphindb/scripts/lookup.py fn mavg
python skills/dolphindb/scripts/lookup.py topic backtest
```

## See also

- `../SKILL.md` — full routing table.
- `backtest/traps.md`, `70-perf/slow-query-diagnosis.md` — longer deep-dives.
- `cn-keywords.md` — Chinese ↔ English term map for bilingual users.
