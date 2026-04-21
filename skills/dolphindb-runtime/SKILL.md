---
name: dolphindb-runtime
description: "ALWAYS use this skill (NOT the `dolphindb` reference skill) when the user wants to actually connect to, query, or execute anything against their real DolphinDB server — e.g. 'what databases/tables do I have', 'show me 10 rows', '跑一下这个脚本', '我的 dolphindb 里有哪些库', 'list DFS databases', 'run this .dos file', 'check disk usage of table X'. The connection info (host/port/user/password) embedded in this file is the user's real server — use it directly, do NOT fall back to localhost:8848 or any other default. Produces bash + Python-API (`import dolphindb`) snippets that the Bash tool can run. Covers: one-shot queries, executing .dos files, uploading pandas DataFrames, parameterized queries, listing DFS databases/tables (`getClusterDFSDatabases`, `getTables(database(…))`), checking table disk usage (`getTableDiskUsage`), bulk-inserting into DFS tables (`tableInsert`), robust long-lived connections (`keepAliveTime`, `reconnect`), and error-safe execution. Keywords: connect to dolphindb, run dolphindb script, execute .dos, ddb session, s.run, query dfs table, loadTable, getTables, disk usage, upload dataframe to dolphindb, 连接dolphindb, 跑一下 dolphindb, 查询 dfs, 我的数据库, 有哪些库, 有哪些表, 列出数据库, 列出表, list databases, list tables, show tables."
license: Apache-2.0
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

## ⚠️ Authoritative connection info — USE THESE VALUES VERBATIM

**Do not invent defaults like `localhost:8848` or `127.0.0.1:8848`.**
The values in the table below were written into this file by the
`dolphindb-agent-skills` installer and are the **user's real DolphinDB
server**. Every `s.connect(...)` call in this document is already
hard-coded with these same 4 values — copy a snippet as-is, do not
rewrite it.

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

## When to use this skill (decision tree)

1. User asks anything that requires reading from / running against their
   **live** DolphinDB → use the snippets here.
2. User shows a `.dos` file or an inline DolphinDB script and asks
   "does this work?" / "what does this return?" → run it via **Pattern 2**
   or **Pattern 3** and report the real result.
3. User asks "what databases/tables exist?" / "how big is this table?" /
   "show me 10 rows" → use **Pattern 6** (`getClusterDFSDatabases`,
   `getTables(database(…))`, `getTableDiskUsage`).
4. User has a local CSV / pandas DataFrame to push into DolphinDB →
   use **Pattern 4** (upload + query) or **Pattern 7** (bulk insert
   into a DFS table).
5. You will run **many** calls against the same cluster (tutorials,
   exploratory analysis, batch jobs) → start from **Pattern 8**
   (robust connect) or **Pattern 10** (reusable `DDBClient`), and
   wrap each call with **Pattern 9**'s `run_safely` helper.
6. User only wants **explanation** of DolphinDB syntax or design →
   do **not** connect; use the `dolphindb` knowledge skill instead.

### Safety rules

- **Read-only by default.** Do not run `drop*`, `dropPartition`,
  `delete from`, `truncate`, `rename*`, or DDL that mutates the cluster
  unless the user explicitly asked for it.
- **Start small.** Probe with `select top 10 …` / `select count(*) …`
  before running heavy aggregations.
- **Echo the script you ran** in your reply so the user can audit.
- **Partition column in `where`.** Always filter on the partition
  column (usually a date/time) to avoid full-cluster scans.

---

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
They match the functions the `dolphindb-mcp-server` project exposes
as MCP tools, so prefer these exact calls over `show databases` /
`show tables` (the latter are OLAP-era aliases and don't always work
on newer clusters).

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

For high-throughput ingestion use `MultithreadedTableWriter` — see the
`dolphindb` knowledge skill's `docs/60-api/python-api.md`.

---

## Pattern 8 — Robust connect (long-running scripts / notebooks)

For anything longer than a one-shot query, pass `keepAliveTime` and
`reconnect=True` so a dropped TCP connection is auto-recovered. This
mirrors what `dolphindb-mcp-server` uses internally.

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
the whole workflow. This matches `DatabaseSession.execute()` in the
MCP server.

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

If you see `RefId: Sxxxxx` in the error string, hand that code to the
`dolphindb` knowledge skill (`reference/error-codes/Sxxxxx.md`) for a
Chinese/English explanation and the canonical fix.

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

## Tips (common pitfalls — also covered in the `dolphindb` skill)

- **Symbol literals use backtick**: `` `AAPL `` is SYMBOL, `"AAPL"` is STRING.
- **Date literals have no quotes**: `2024.01.01`, not `"2024-01-01"`.
  Use `date("2024-01-01")` to convert from a string.
- **`append!` mutates in place**; the `!` matters.
- **Loop syntax** uses braces: `for(sym in symVec){ ... }`.
- **`=` inside `where`** is equality, not assignment.
- **Session is not thread-safe** — one `ddb.session()` per thread, or use
  `ddb.DBConnectionPool` for pools.
- **`s.run(...)` returns a pandas DataFrame** for table-shaped results;
  `SYMBOL`/`STRING` columns come back as `object`, `TIMESTAMP` as
  `datetime64[ns]`.
- For any unknown function / error code, consult the sibling `dolphindb`
  skill (offline reference for the full language).
