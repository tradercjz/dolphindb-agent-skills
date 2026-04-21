---
name: dolphindb
description: "The ONE skill for anything DolphinDB — covers BOTH running queries against the user's live DolphinDB server AND offline reference / syntax lookup. Use this whenever the user mentions DolphinDB, ddb, .dos, DFS, or anything database-related for DolphinDB. Runtime side: the connection info (host/port/user/password) embedded below was written by the `dolphindb-agent-skills` installer and is the user's REAL server — use it verbatim, do NOT fall back to localhost:8848 or any other default. Runtime capabilities: one-shot queries via Python API (`import dolphindb`), executing .dos files, uploading pandas DataFrames, parameterized queries, listing DFS databases/tables (`getClusterDFSDatabases`, `getTables(database(…))`), checking table disk usage (`getTableDiskUsage`), bulk-inserting into DFS tables (`tableInsert`), robust long-lived connections (`keepAliveTime`, `reconnect`), error-safe execution. Reference side: DolphinDB SQL dialect (context by / pivot by / asof join / window join), DFS partitioned tables on TSDB / OLAP / PKEY / IMOLTP engines, stream computing (streamTable, subscribeTable, reactiveStateEngine, timeSeriesEngine, CEP, replay), strategy backtesting (Backtest plugin, MatchingEngineSimulator, simulatedExchangeEngine, OME) for stock / future / option / bond / crypto, factor computation with @state + @jit, client APIs (Python, Java, C++, JDBC, ODBC, Go, Rust), ingestion (loadText, HDF5, Parquet, Arrow, Kafka, MQTT), 70+ plugins, performance tuning, cluster ops, and lookup of any RefId Sxxxxx error code or built-in function. Keywords: DolphinDB, ddb, .dos, DFS, 回测, 策略, 因子, 我的数据库, 有哪些库, 有哪些表, 列出数据库, 列出表, list databases, list tables, show tables, run dolphindb script, connect to dolphindb, query dfs."
license: Apache-2.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# DolphinDB Skill

One skill, two modes:

- **Runtime** — run bash/Python snippets against the user's live DolphinDB
  server (patched connection info below).
- **Reference** — offline knowledge base for syntax, engines, plugins,
  error codes, and best practices (Routing Table below).

All content targets **DolphinDB Server 3.00+** and its official client APIs.

---

## ⚠️ Authoritative connection info — USE THESE VALUES VERBATIM

**Do not invent defaults like `localhost:8848` or `127.0.0.1:8848`.**
The values in the table below were written into this file by the
`dolphindb-agent-skills` installer and are the **user's real DolphinDB
server**. Every `s.connect(...)` call in the Runtime Patterns section
is already hard-coded with these same 4 values — copy a snippet as-is,
do not rewrite it.

| Field    | Value              |
|----------|--------------------|
| Host     | `{{DDB_HOST}}`     |
| Port     | `{{DDB_PORT}}`     |
| User     | `{{DDB_USER}}`     |
| Password | `{{DDB_PASSWD}}`   |

> If the table above still shows literal `{{DDB_HOST}}` / `{{DDB_PORT}}` /
> `{{DDB_USER}}` / `{{DDB_PASSWD}}` placeholders, the user never ran the
> `dolphindb-agent-skills` installer (or ran it non-interactively). Tell
> them to re-run it in a real terminal and enter their real server info.

---

## Decision tree — runtime vs reference

1. User wants to **run / query / execute** against their DolphinDB
   (e.g. "what databases do I have", "show me 10 rows", "跑一下这个脚本",
   "我的 dolphindb 里有哪些库") → use the **Runtime Patterns** section
   below.
2. User shows a `.dos` file or inline DolphinDB script and asks
   "does this work?" / "what does this return?" → run it via Runtime
   **Pattern 2** or **Pattern 3** and report the real result.
3. User asks "what databases/tables exist?" / "how big is this table?" →
   Runtime **Pattern 6** (`getClusterDFSDatabases`, `getTables(database(…))`,
   `getTableDiskUsage`).
4. User has a local CSV / pandas DataFrame to push into DolphinDB →
   Runtime **Pattern 4** (upload + query) or **Pattern 7** (bulk insert).
5. Long batch job / many calls → start from Runtime **Pattern 8**
   (robust connect) or **Pattern 10** (reusable `DDBClient`), wrap each
   call with Runtime **Pattern 9**'s `run_safely` helper.
6. User only wants **explanation / syntax / design / error-code lookup**
   → jump to the [Routing Table](#routing-table) and pull the right
   `docs/` or `reference/` file.

### Safety rules (for runtime execution)

- **Read-only by default.** Do not run `drop*`, `dropPartition`,
  `delete from`, `truncate`, `rename*`, or DDL that mutates the cluster
  unless the user explicitly asked for it.
- **Start small.** Probe with `select top 10 …` / `select count(*) …`
  before running heavy aggregations.
- **Echo the script you ran** in your reply so the user can audit.
- **Partition column in `where`.** Always filter on the partition
  column (usually a date/time) to avoid full-cluster scans.

---

# Runtime Patterns

## Pattern 1 — One-liner sanity check

```bash
python3 -c "import dolphindb as ddb; s=ddb.session(); s.connect('127.0.0.1', 8848, 'admin', '123456'); print(s.run('version()'))"
```

If this prints a version string, the connection is healthy.

---

## Pattern 2 — Run a .dos script file

```bash
python3 << 'PYEOF'
import dolphindb as ddb
s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456")
script = open("/path/to/your/script.dos").read()
result = s.run(script)
print(result)
PYEOF
```

Replace `/path/to/your/script.dos` with the actual file path (use
`Glob` to find it if the user didn't say).

---

## Pattern 3 — Run an inline DolphinDB script

```bash
python3 << 'PYEOF'
import dolphindb as ddb
s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456")

script = """
symVec = `AAPL`MSFT`GOOG
n=50; ts = 2024.01.02T09:30:00.000 + (0..(n-1))*60000
syms=array(SYMBOL,0); times=array(TIMESTAMP,0)
opens=array(DOUBLE,0); highs=array(DOUBLE,0); lows=array(DOUBLE,0)
closes=array(DOUBLE,0); vols=array(LONG,0)
for(sym in symVec){
    bp=100.0+rand(100.0,1)[0]; bv=5000.0+rand(3000.0,1)[0]
    for(t in ts){
        o=bp+rand(2.0,1)[0]; h=o+rand(1.5,1)[0]; l=o-rand(1.5,1)[0]
        c=l+rand(h-l,1)[0]; v=round(bv+rand(2000.0,1)[0],0)
        syms.append!(sym); times.append!(t)
        opens.append!(o); highs.append!(h); lows.append!(l)
        closes.append!(c); vols.append!(v)
    }
}
bars=table(syms as symbol, times as tradetime, opens as open,
           highs as high, lows as low, closes as close, vols as volume)
bars=select * from bars order by symbol, tradetime

f=select symbol, tradetime, close,
       mavg(volume,5)/mavg(volume,20) as volRatio,
       close/mavg(close,20)-1 as priceMom,
       (mavg(volume,5)/mavg(volume,20))*(close/mavg(close,20)-1) as pvpFactor
from bars context by symbol csort tradetime

print(select top 5 symbol,tradetime,close,volRatio,priceMom,pvpFactor from f)
print(select symbol,count(*) as n, avg(pvpFactor) as meanPvp from f group by symbol)
"""
r = s.run(script)
print(r)
PYEOF
```

---

## Pattern 4 — Upload a pandas DataFrame, then query it

```bash
python3 << 'PYEOF'
import dolphindb as ddb
import pandas as pd

s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456")

df = pd.DataFrame({
    "symbol": ["AAPL"] * 5,
    "close":  [100.0, 101.0, 102.0, 101.5, 103.0],
    "volume": [1000, 1100, 1050, 1150, 1200],
})

s.upload({"myDF": df})
result = s.run("""
    select * from myDF
    context by symbol csort rowNo
""")
print(result)
PYEOF
```

---

## Pattern 5 — Parameterized query (safe against SQL injection)

```bash
python3 << 'PYEOF'
import dolphindb as ddb
import pandas as pd

s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456")

# Upload filter values as a table, then reference by name.
local_df = pd.DataFrame({"sym": ["AAPL", "MSFT"], "d": ["2024.01.02", "2024.01.02"]})
s.upload({"filter": local_df})

result = s.run("""
    select count(*) as cnt from loadTable('dfs://demo',`trades)
    where sym in filter.sym and date in filter.d
""")
print(result)
PYEOF
```

Prefer this over f-string interpolation of user input.

---

## Pattern 6 — DFS catalog & disk usage (canonical ops)

These 4 operations cover most "what's in this DolphinDB?" questions.
Prefer these exact calls over `show databases` / `show tables` (the
latter are OLAP-era aliases and don't always work on newer clusters).

```bash
python3 << 'PYEOF'
import dolphindb as ddb
s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456",
          keepAliveTime=3600, reconnect=True)

# (1) List all DFS databases on the cluster
print(s.run("getClusterDFSDatabases()"))

# (2) List tables in a specific DFS database
print(s.run('getTables(database("dfs://trades"))'))

# (3) Disk usage for one DFS table (requires the 'ops' module)
print(s.run('use ops; getTableDiskUsage("dfs://trades", "trade", byNode=false)'))

# (4) Run an arbitrary script — the universal escape hatch
print(s.run("select top 10 * from loadTable('dfs://trades', `trade)"))
PYEOF
```

**Tip:** `getTableDiskUsage` returns a per-chunk breakdown by default.
Pass `byNode=true` if you want it rolled up per datanode, or wrap the
call to aggregate yourself (`select sum(diskSize) from …`).

---

## Pattern 7 — Bulk-append rows to a DFS table

```bash
python3 << 'PYEOF'
import dolphindb as ddb
import pandas as pd

s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456")

df = pd.DataFrame({
    "sym":    ["AAPL", "MSFT"],
    "date":   pd.to_datetime(["2024-01-02", "2024-01-02"]).date,
    "price":  [189.5, 370.1],
    "volume": [1000, 2000],
})
s.upload({"chunk": df})

# `tableInsert` returns the number of rows inserted.
print(s.run("""
    tableInsert(loadTable('dfs://trades', `trade), chunk)
"""))
PYEOF
```

For high-throughput ingestion use `MultithreadedTableWriter` — see
`docs/60-api/python-api.md` via the Routing Table below.

---

## Pattern 8 — Robust connect (long-running scripts / notebooks)

For anything longer than a one-shot query, pass `keepAliveTime` and
`reconnect=True` so a dropped TCP connection is auto-recovered.

```bash
python3 << 'PYEOF'
import dolphindb as ddb

s = ddb.session()
s.connect(
    "127.0.0.1", 8848, "admin", "123456",
    keepAliveTime=3600,   # seconds; suppresses idle-disconnect
    reconnect=True,       # auto-reconnect on transient network errors
)

# ... many calls over hours ...
print(s.run("now()"))
s.close()
PYEOF
```

Other useful kwargs on `session()` / `connect()`:

- `enableSSL=True` — if the server listens with TLS.
- `highAvailability=True, highAvailabilitySites=["ip1:port", "ip2:port"]`
  — cluster mode with failover across controllers.
- `compress=True` — compress result payloads for large frames.

---

## Pattern 9 — Capture errors (don't crash the whole run)

Wrap every `s.run(...)` in try/except so a bad script does not kill
the whole workflow.

```bash
python3 << 'PYEOF'
import dolphindb as ddb

def run_safely(s, script: str):
    try:
        return True, s.run(script)
    except Exception as e:
        return False, str(e)

s = ddb.session()
s.connect("127.0.0.1", 8848, "admin", "123456",
          keepAliveTime=3600, reconnect=True)

scripts = [
    "version()",
    "getClusterDFSDatabases()",
    "select top 5 * from loadTable('dfs://no_such_db', `x)",  # will fail
]
for sc in scripts:
    ok, result = run_safely(s, sc)
    status = "OK " if ok else "ERR"
    print(f"[{status}] {sc}\n  -> {result}\n")
s.close()
PYEOF
```

If you see `RefId: Sxxxxx` in the error string, look it up via the
Routing Table below (`reference/error-codes/Sxxxxx.md`).

---

## Pattern 10 — Reusable session context manager

Copy this class into a standalone script when you need to run many
snippets against the same server — it guarantees `close()` runs even
on exceptions.

```python
# dolphindb_client.py
import dolphindb as ddb

class DDBClient:
    def __init__(self, host="127.0.0.1", port=8848,
                 user="admin", passwd="123456",
                 keep_alive_time=3600, reconnect=True):
        self.host, self.port, self.user, self.passwd = host, port, user, passwd
        self.keep_alive_time, self.reconnect = keep_alive_time, reconnect
        self.session = ddb.session()

    def __enter__(self):
        self.session.connect(
            self.host, int(self.port), self.user, self.passwd,
            keepAliveTime=self.keep_alive_time, reconnect=self.reconnect,
        )
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.close()

    def run(self, script: str):
        try:
            return True, self.session.run(script)
        except Exception as e:
            return False, str(e)


if __name__ == "__main__":
    with DDBClient() as c:   # defaults match this skill's patched values
        print(c.run("version()"))
        print(c.run("getClusterDFSDatabases()"))
```

Then:

```bash
python3 dolphindb_client.py
```

---

## Connection troubleshooting

### `ConnectionRefusedError` / "Connection refused"

```bash
nc -zv 127.0.0.1 8848
```

If that fails: DolphinDB is not running on that host:port, or a
firewall is blocking it.

### `ModuleNotFoundError: No module named 'dolphindb'`

```bash
pip install dolphindb
# or, in an externally-managed env (macOS Homebrew / PEP 668):
uv pip install dolphindb
# or to run without installing globally:
uvx --with dolphindb python3 -c "import dolphindb; print(dolphindb.__version__)"
```

### "Server response: Authentication failed"

Credentials are wrong. Re-run the `dolphindb-agent-skills` installer and
enter the correct user/password, or edit this file.

### Script runs but `s.run(...)` returns `None`

Many DolphinDB scripts print nothing when they have no tail expression.
Either add an explicit `print(...)` inside the script, or end the script
with an expression (e.g. a variable name) whose value should be returned.

---

# Reference Library

## How to use this skill (reference mode)

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
