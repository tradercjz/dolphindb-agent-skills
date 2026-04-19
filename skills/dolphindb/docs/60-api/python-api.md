# Python API (`dolphindb`)

## Contents
- Install & connect (`session`, pool)
- Running scripts (`run`, `runArrow`, `upload`)
- Writing data (`tableAppender`, `PartitionedTableAppender`)
- Streaming subscription from Python
- Type mapping (→ `type-mapping.md`)
- Common errors & performance

The official Python client. Install:

```bash
pip install dolphindb
```

Package name is `dolphindb`; idiomatic import alias is `ddb`.

## Connect

```python
import dolphindb as ddb

s = ddb.session()
s.connect(host="localhost", port=8848, userid="admin", password="123456")

# always close when done
s.close()

# or context-manager pattern
with ddb.session() as s:
    s.connect("localhost", 8848, "admin", "123456")
    print(s.run("version()"))
```

### Session options

```python
s = ddb.session(
    enableSSL        = False,
    enableASYNC      = False,   # async writes, non-blocking
    enableChunkGranularityConfig = False,
    keepAliveTime    = 30,
    enablePickle     = True,    # fastest serialization for DataFrames
    protocol         = ddb.PROTOCOL_DDB,    # or PROTOCOL_ARROW for Arrow
    show_output      = True,
    compress         = False,
)
```

For production, prefer **`DBConnectionPool`** (thread-safe, reusable):

```python
pool = ddb.DBConnectionPool("localhost", 8848, 8, "admin", "123456")
```

## Run a script

```python
df = s.run("select top 10 * from loadTable('dfs://demo', `trades)")
# df is a pandas DataFrame
```

`run` also accepts **parameterized templates**:

```python
df = s.run(
    "select * from loadTable('dfs://trades',`trade) where sym = sym and date = d",
    {"sym": "AAPL", "d": pd.Timestamp("2024-01-02").date()}
)
```

But the **safer, recommended** parameter-passing is `upload` + reference by
name (see below).

## Upload Python data to DolphinDB

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "sym": ["AAPL", "MSFT"],
    "px":  [100.0, 260.0],
    "ts":  pd.to_datetime(["2024-01-02 09:30", "2024-01-02 09:31"]),
})

s.upload({"pydf": df})
s.run("select * from pydf")   # pydf now lives in the server's session scope
```

Types are auto-mapped (see `type-mapping.md`). To control the target
DolphinDB type, construct a typed table first:

```python
s.run("pyt = table(pydf.sym as sym, pydf.px as px, nanotimestamp(pydf.ts) as ts)")
```

## Append to a DFS table

Fastest path: upload a DataFrame, then `append!` in-server.

```python
s.upload({"chunk": df})
s.run("loadTable('dfs://trades', `trade).append!(chunk)")
```

Or use the high-level writers:

```python
writer = ddb.PartitionedTableAppender(
    dbPath="dfs://trades", tableName="trade",
    partitionColName="date", dbConnectionPool=pool
)
writer.append(df)
```

For high-throughput ingest see `ddb.MultithreadedTableWriter`:

```python
mtw = ddb.MultithreadedTableWriter(
    host="localhost", port=8848, userId="admin", password="123456",
    dbPath="dfs://trades", tableName="trade",
    batchSize=10000, throttle=1,
    partitionCol="date", threads=4, compressMethods=["LZ4", "LZ4", "DELTA", "LZ4"]
)
for row in rows:
    mtw.insert(*row)
mtw.waitForThreadCompletion()
```

## Subscribe to a stream from Python

```python
def on_msg(msg):
    # msg is a list of lists (default) or a DataFrame (msgAsTable=True)
    print(msg)

s.enableStreaming(localPort=0)      # choose a free local port
s.subscribe(
    host="localhost", port=8848,
    handler=on_msg,
    tableName="ticks",
    actionName="pyDemo",
    offset=-1,
    msgAsTable=True,
    batchSize=1000, throttle=0.1
)
# later
s.unsubscribe(host="localhost", port=8848, tableName="ticks", actionName="pyDemo")
```

See `../40-streaming/subscribe.md` and upstream `str_api_python.md`
+ `py_sub.md`.

## Transactions

```python
s.run("beginTransaction()")
try:
    s.run("loadTable('dfs://demo',`a).append!(t1)")
    s.run("loadTable('dfs://demo',`b).append!(t2)")
    s.run("commitTransaction()")
except Exception:
    s.run("rollbackTransaction()")
    raise
```

## Result types

| DolphinDB output | Python type |
|------------------|-------------|
| scalar | python scalar (int / float / str / datetime / ...) |
| vector | `numpy.ndarray` |
| matrix | `numpy.ndarray` (2-D) |
| table | `pandas.DataFrame` |
| dict | `dict` |
| set | `set` |
| tuple | `list` |

## Traps

- **Connection per thread.** `session` is NOT thread-safe; use
  `DBConnectionPool` for concurrent use.
- **`enablePickle=True` pickles DataFrames**, very fast; set to False if the
  server's Python version differs (older servers).
- **Python `datetime.datetime` without tz** becomes `DATETIME` (s) or
  `TIMESTAMP` (ms/ns) depending on precision; beware of silent truncation.
- **`numpy.nan` in int columns** fails upload — cast to float or use
  pandas nullable `Int64`.
- **Per-call `s.run(script)`** creates/destroys session state for the
  server; keep frequently-used objects via `upload`.
- **Empty result** of `s.run(...)` returns `None`, not an empty DataFrame.

## See also

- `type-mapping.md`, `java-api.md`, `cpp-api.md`.
- `python/` subdirectory for detailed guides.
- Full external manual: <https://docs.dolphindb.cn/zh/pydoc/py.html>.
