---
name: dolphindb
description: "OFFLINE DolphinDB reference library — use this for LOOKUP and EXPLANATION ONLY. Do NOT use this skill if the user wants to actually connect to / query / run something against a live DolphinDB server; use the `dolphindb-runtime` skill for that instead. This skill provides DolphinDB expertise for writing .dos scripts and client code. Covers the DolphinDB SQL dialect (context by / pivot by / asof join / window join), DFS partitioned tables on TSDB / OLAP / PKEY / IMOLTP engines, stream computing (streamTable, subscribeTable, reactiveStateEngine, timeSeriesEngine, CEP, replay), strategy backtesting (Backtest plugin, MatchingEngineSimulator, simulatedExchangeEngine, OME) for stock / future / option / bond / crypto, factor computation with @state + @jit, client APIs (Python, Java, C++, JDBC, ODBC, Go, Rust), ingestion (loadText, HDF5, Parquet, Arrow, Kafka, MQTT), 70+ plugins, performance tuning, cluster ops, and lookup of any RefId Sxxxxx error code or built-in function. Use when the user mentions DolphinDB, ddb, .dos scripts, DFS tables, stream engines, 回测/策略/因子, or any listed keyword — AND the user is NOT asking to actually run/query their own server."
license: Apache-2.0
---

# DolphinDB Knowledge Base

DolphinDB is a high-performance distributed time-series database with a built-in vectorized programming language. This skill provides offline reference so an AI agent can answer DolphinDB questions and write correct scripts without internet access.

All content is authored for **DolphinDB Server 3.00+** and its official client APIs.

---

## How to use this skill

1. Identify the user's intent and **consult the Routing Table** below to pick the right file.
2. For an unknown DolphinDB function, look it up in `reference/functions/INDEX.md` → then read the theme file it points to.
3. For a runtime error message containing `RefId: Sxxxxx`, look it up in `reference/error-codes/INDEX.md` → then read `reference/error-codes/Sxxxxx.md`.
4. For "how do I do X" tasks, check `patterns/` first; for runnable end-to-end scripts check `examples/`.
5. Only fall back to the [Quick snippets](#quick-snippets) section below for the most common one-liners.

---

## Routing Table

| If the user is asking about... | Go to |
|---|---|
| What DolphinDB is / architecture / node types | `docs/00-overview.md` |
| Install, connect, first script | `docs/01-quickstart.md` |
| Data types (INT, LONG, DECIMAL, SYMBOL, TIMESTAMP, …) | `docs/10-language/data-types.md` |
| Data forms (vector, matrix, table, dict, tuple, set, pair, tensor) | `docs/10-language/data-forms.md` |
| **Dict** (creation, `ANY` values, `syncDict`, missing-key, merge) ★ | `docs/10-language/dict.md` |
| Operators, assignment `=` / `<-`, in-place `!` | `docs/10-language/operators.md` |
| Control flow (`if`, `for`, `do..while`, `try..catch`) | `docs/10-language/control-flow.md` |
| Named / anonymous / lambda / partial application / higher-order | `docs/10-language/functions.md` |
| Metaprogramming, `sqlCol`, `makeCall`, `sql()` | `docs/10-language/metaprogramming.md` |
| Modules (`use`, `module`) | `docs/10-language/modules.md` |
| `SELECT ... WHERE` basics | `docs/20-sql/select-where.md` |
| `group by` aggregation | `docs/20-sql/group-by.md` |
| **`context by`** (per-group vectorized calc) ★ | `docs/20-sql/context-by.md` |
| **Time types** (DATE/TIMESTAMP/NANOTIMESTAMP/… — 10 variants, join-empty trap) ★ | `docs/10-language/time-types.md` |
| **NULL handling** (typed nulls, `isValid`, `nullFill`, window propagation) ★ | `docs/10-language/null-handling.md` |
| **Error handling** (`try/catch`, RefIds, job errors, streaming poison-pill) | `docs/10-language/error-handling.md` |
| **`pivot by`** ★ | `docs/20-sql/pivot-by.md` |
| Window functions / analytic functions | `docs/20-sql/window-functions.md` |
| Joins: equi / left / full / cross / asof / window / prefix | `docs/20-sql/joins-overview.md` |
| **`asof join` (`aj`) / `wj` — time-series alignment** ★ | `docs/20-sql/asof-join.md` |
| `update` / `insert into` / `delete` / `alter` | `docs/20-sql/update-insert-delete.md` |
| Create DFS database, `database(...)`, `createPartitionedTable` | `docs/30-database/dfs-database.md` |
| Partitioning schemes (VALUE / RANGE / HASH / LIST / COMPO) | `docs/30-database/partitioning.md` |
| TSDB engine specifics (sortColumns, keepDuplicates) | `docs/30-database/tsdb-engine.md` |
| OLAP engine specifics | `docs/30-database/olap-engine.md` |
| Primary-key engine (PKEY) — upsert semantics | `docs/30-database/pkey-engine.md` |
| DFS limits & best practices | `docs/30-database/limits-and-best-practices.md` |
| `streamTable`, `share`, persist | `docs/40-streaming/stream-table.md` |
| `subscribeTable`, handler, `msgAsTable` | `docs/40-streaming/subscribe.md` |
| Stream engines (reactiveState / timeSeries / cross / asof / session / anomaly) | `docs/40-streaming/engines.md` |
| **Stream engine selection — decision tree** ★ | `docs/40-streaming/engine-selection.md` |
| CEP | `docs/40-streaming/cep-overview.md` |
| Historical replay | `docs/40-streaming/replay.md` |
| `loadText`, `ploadText`, schema inference | `docs/50-ingestion/loadText-ploadText.md` |
| HDF5 / Parquet / Arrow | `docs/50-ingestion/hdf5-parquet.md` |
| Kafka / MQTT ingestion | `docs/50-ingestion/kafka-mqtt.md` |
| Python API (`dolphindb`, `ddb.session`, `.run`, `.upload`) | `docs/60-api/python-api.md` |
| Java API | `docs/60-api/java-api.md` |
| C++ API | `docs/60-api/cpp-api.md` |
| Cross-language type mapping | `docs/60-api/type-mapping.md` |
| Query optimization, EXPLAIN, hints | `docs/70-perf/query-optimization.md` |
| Partition pruning | `docs/70-perf/partition-pruning.md` |
| Memory & threading tuning | `docs/70-perf/memory-threading.md` |
| **Slow-query diagnosis checklist** ★ | `docs/70-perf/slow-query-diagnosis.md` |
| **JIT (`@jit`) compilation guide** | `docs/70-perf/jit-guide.md` |
| Cluster ops | `docs/90-admin/cluster.md` |
| Backup / restore | `docs/90-admin/backup-restore.md` |
| Users / ACL | `docs/90-admin/security.md` |
| **Look up any built-in function by name** | `python scripts/lookup.py fn <name>` (or `reference/functions/INDEX.md`) |
| **Look up any runtime error `RefId: Sxxxxx`** | `python scripts/lookup.py error S00012` (or `reference/error-codes/INDEX.md`) |
| **Jump to curated reads for a topic** | `python scripts/lookup.py topic <backtest|stream|factor|python|…>` |
| **One-page top-traps cheatsheet** ★ | `docs/cheatsheet.md` |
| **Chinese ↔ English keyword map (中文提问)** | `docs/cn-keywords.md` |
| Plugin quick catalog (one-line per plugin) | `reference/plugins-catalog.md` |
| **Any specific plugin manual** (amdQuote / Arrow / Kafka / ODBC / Parquet / CTP / INSIGHT / …) | `docs/plugins/README.md` (hub) + `docs/plugins/<name>/` or `docs/plugins/<name>.md` |
| Worked tutorials (OHLC, backtest, IoT anomaly, scheduledJob, …) | `docs/tutorials/README.md` (curated index of 281 tutorials) |
| Built-in modules (`ta`, `wq101alpha`, `gtja191Alpha`, `mytt`, `MarketHoliday`, …) | `docs/modules/README.md` |
| Deployment guides / license fingerprint | `docs/deploy/` |
| DolphinDB MCP | `docs/mcp/` |
| O&M troubleshooting (connection lost / server hang / slow I/O) | `docs/90-admin/omc/` |
| **Web console admin UI** (user mgmt, config, stream graph, querybuilder, Shell) | `docs/90-admin/web/README.md` (18 pages) |
| Client IDE & editor integrations (VSCode, Jupyter, DBeaver, Grafana, PowerBI, Superset) | `docs/60-api/{vscode,jupyter,gui,terminal,clients}.md` + `docs/60-api/tools/` |
| Configuration parameter reference | `docs/90-admin/cfg/` |
| Version release notes | `docs/release-notes/` |
| Upstream top-level index & 3rd-party integrations list | `docs/upstream-index.md`, `docs/third_party.md` |
| **Functions by topic** (categorical index of all 1721 built-ins) | `reference/functions/funcs_by_topics.md` (55 KB) + `funcs_intro.md` + `appendix.md` |
| **Backtest / simulated matching** (Backtest plugin, MatchingEngineSimulator, OME, SimulatedExchangeEngine) ★ | `docs/backtest/README.md` (hub) + `docs/backtest/{backtest-plugin-guide,matching-engine-guide,assets,traps,factors,tutorials-index}.md` |
| **Factor / alpha computation** (`@state`, reactive state engine, lookahead, WQ101, GTJA191) ★ | `docs/backtest/factors.md` |
| Runnable end-to-end scripts | `examples/` (backtest-quickstart/-future/-option, parquet-roundtrip, stream-reactive-engine, tick-to-ohlc, python-api-quickstart) |
| "How do I do X" recipes | `patterns/` (signal-to-order, stream-ingestion-to-dfs, stream-recovery-after-restart, scheduled-job-template, python-roundtrip-type-safety, asof-join, partition-design, tick-to-ohlc, upsert-via-pkey) |
| **Eval battery — 10 representative tasks** | `evals/README.md` |
| **How to measure hit-rate / uplift** | `evals/HOW-TO-MEASURE.md` + `scripts/run_evals.py` |

---

## Common traps (read before writing DolphinDB code)

These are the most frequent mistakes agents make. Follow the linked page for details.

- **`context by` ≠ `group by`.** `group by` collapses rows; `context by` keeps all rows and computes per-group vectors. Use `context by` for rolling/cumulative per-symbol calculations. → `docs/20-sql/context-by.md`
- **Partition column must appear in `where`**, otherwise the query scans all partitions. Always filter on the partition column first (typically a date/time). → `docs/70-perf/partition-pruning.md`
- **`share` before subscribe.** A stream table must be `share`d (or persisted) before `subscribeTable` can attach. → `docs/40-streaming/stream-table.md`
- **`=` vs `==`.** In DolphinDB, `=` is assignment _and_ equality comparison inside `where` clauses. Use `==` for equality in script expressions; use `=` inside SQL predicates. → `docs/10-language/operators.md`
- **`<-` is assignment in function definitions** and also appears in some stream APIs; it is NOT a comparison operator.
- **Symbol literals use backticks.** `` `AAPL `` is a SYMBOL literal; `"AAPL"` is STRING. Mixing them changes partition routing and join behavior.
- **Date literals have no quotes.** Write `2024.01.01`, not `"2024-01-01"`. Use `date("2024-01-01")` to convert from string.
- **`append!` mutates; `append` does not exist for tables.** The `!` suffix means in-place mutation.
- **`loadTable(...)` is lazy.** Operations are lazily planned; only fully materialized when the query is executed or the result is touched.
- **Python API returns numpy-backed DataFrames.** `SYMBOL`/`STRING` become `object`, `TIMESTAMP` becomes `datetime64[ns]`. Check `docs/60-api/type-mapping.md` before comparing values.
- **Dict is NOT Python-style.** No `{"a": 1}` literal — use `dict(STRING, INT)` (empty) or `dict(keys, vals)`. Missing-key read returns null (not an error); use `d.contains(k)`. Concurrent writes need `syncDict`, otherwise the node can crash. → `docs/10-language/dict.md`
- **Backtest lookahead bias.** `mavg(close, 5)` and any same-bar factor include the current bar, which is only valid if you execute at bar close. For next-bar execution, lag signals by one bar. `matchingRatio=1`, zero `slippage`, and unmodeled queue position all flatter results. → `docs/backtest/traps.md`
- **`show engines`, `getStreamingStat()` and `getPerformance()`** are your first debugging tools — check them before assuming a bug.

---

## Quick snippets

Kept intentionally minimal. For more, read `examples/`.

### Connect from Python

```python
import dolphindb as ddb

s = ddb.session()
s.connect("localhost", 8848, "admin", "123456")

df = s.run("select top 100 * from loadTable('dfs://trades', `trade)")
```

### Create a partitioned DFS table (TSDB engine)

```dolphindb
db = database("dfs://trades", VALUE, 2024.01.01..2024.12.31, engine="TSDB")

schema = table(
    1:0,
    `sym`date`price`volume,
    [SYMBOL, DATE, DOUBLE, INT]
)

db.createPartitionedTable(
    table       = schema,
    tableName   = `trade,
    partitionColumns = `date,
    sortColumns = `sym`date
)
```

### Append rows

```dolphindb
t = table(
    take(`AAPL`MSFT, 10) as sym,
    take(2024.01.01..2024.01.10, 10) as date,
    rand(100.0, 10) as price,
    rand(1000, 10)   as volume
)
loadTable("dfs://trades", `trade).append!(t)
```

### `context by` vs `group by`

```dolphindb
// group by: 1 row per sym
select sym, avg(price) as avgPx from t group by sym

// context by: keep all rows, add per-sym 5-row moving avg
select sym, date, price, mavg(price, 5) as ma5
from t context by sym
```

### Stream table + subscription

```dolphindb
share streamTable(1000:0, `time`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as trades

def myHandler(msg) { /* msg is a table when msgAsTable=true */ }

subscribeTable(
    tableName = `trades,
    actionName = `printAction,
    handler    = myHandler,
    msgAsTable = true
)
```

### Diagnosing an error from a script

If the user shows a log line like `... RefId: S02006`, read `reference/error-codes/S02006.md` — every error code ships with **报错信息 / 错误原因 / 解决办法**.

---

## Maintenance

Every file in this skill is either **hand-authored** or **auto-mirrored**
from the upstream DolphinDB documentation. They coexist flatly — there is
no separate `_source/` layer.

**Auto-mirrored files** begin with the HTML comment
`<!-- Auto-mirrored from upstream ... -->`. Do not edit them by hand; rerun
the build script and they will be overwritten. Hand-authored files have no
such marker and are never touched by the build.

Auto-mirrored tree (regenerated by `scripts/build_from_docs.py`):

- `reference/functions/` — INDEX, by-theme, by-name (1718 function pages).
- `reference/error-codes/` — every `RefId: Sxxxxx` page in full.
- `reference/plugins-catalog.md` — one-line summary per plugin.
- `docs/**/*.md` except the hand-authored files listed below.

Hand-authored (never auto-touched):

- `docs/00-overview.md`, `docs/01-quickstart.md`.
- `docs/<area>/README.md` in every numbered area.
- `docs/10-language/{data-types,data-forms,dict,time-types,null-handling,error-handling,operators,control-flow,functions,metaprogramming,modules}.md`.
- `docs/20-sql/{select-where,group-by,context-by,pivot-by,window-functions,joins-overview,asof-join,update-insert-delete}.md`.
- `docs/30-database/{dfs-database,partitioning,tsdb-engine,olap-engine,pkey-engine,limits-and-best-practices}.md`.
- `docs/40-streaming/{stream-table,subscribe,engines,engine-selection,cep-overview,replay}.md`.
- `docs/50-ingestion/{loadText-ploadText,hdf5-parquet,kafka-mqtt}.md`.
- `docs/60-api/{python-api,java-api,cpp-api,type-mapping}.md`.
- `docs/70-perf/{partition-pruning,query-optimization,memory-threading,slow-query-diagnosis,jit-guide}.md`.
- `docs/90-admin/{cluster,backup-restore,security}.md`.
- `docs/backtest/{README,backtest-plugin-guide,matching-engine-guide,assets,traps,factors,tutorials-index}.md`.
- `docs/tutorials/README.md`, `docs/plugins/README.md`, `docs/modules/README.md` — curated navigation indexes.
- `patterns/*.md` — "how do I do X" recipes.
- `examples/*.dos`, `examples/*.py` — runnable end-to-end scripts.
- `evals/{README,scoring,run}.md` + `evals/tasks/*.md` — regression battery.
- `docs/cheatsheet.md` — compressed top-traps.
- `docs/cn-keywords.md` — CN↔EN keyword map.
- `scripts/lookup.py` — agent-invokable CLI for error codes / functions / topics.
- `SKILL.md` — this file.

Rebuild after upstream changes:

```powershell
python skills/dolphindb/scripts/build_from_docs.py
```

Only files carrying the auto-mirror marker are deleted/rewritten; anything
you wrote manually is preserved across rebuilds.
