# DolphinDB quickstart

End-to-end recipe to go from *nothing* to a running query in ~5 minutes.

## 1. Start a single-node server

Download the community edition from <https://dolphindb.cn/>. Extract, then:

```bash
cd server
./dolphindb -console 1 -home data -port 8848
```

- Default user: `admin` / `123456` (change it immediately in production).
- Web notebook: <http://localhost:8848>.
- License: free community edition for up to 2 cores / 8 GB.

Full deployment options: `docs/getstarted/chap1_getstarted.md`.

## 2. Connect from a client

### Python API

```bash
pip install dolphindb
```

```python
import dolphindb as ddb
s = ddb.session()
s.connect("localhost", 8848, "admin", "123456")

print(s.run("1 + 2"))       # -> 3
print(s.run("take(1..5, 5)"))
```

Options: `ddb.session(enableASYNC=True)` for fire-and-forget writes;
`ddb.session(enablePickle=False)` to disable pickle when sending pandas.

### DolphinDB script (inside the web notebook)

```dolphindb
x = 1..10
avg(x)
```

## 3. Create your first DFS table (TSDB engine)

```dolphindb
// 1. create the database (once per physical disk layout)
if(existsDatabase("dfs://demo")) { dropDatabase("dfs://demo") }
db = database("dfs://demo", VALUE, 2024.01.01..2024.12.31, engine="TSDB")

// 2. define the schema
schema = table(
    1:0,
    `sym`ts`price`volume,
    [SYMBOL, TIMESTAMP, DOUBLE, INT]
)

// 3. create a partitioned table
pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `trades,
    partitionColumns = `ts,
    sortColumns      = `sym`ts         // TSDB-only; speeds up (sym, time) range scans
)

// 4. write some rows
t = table(
    take(`AAPL`MSFT`GOOG, 30)          as sym,
    2024.01.01T09:30:00.000 + 0..29 * 1000 as ts,
    90.0 + rand(20.0, 30)              as price,
    rand(1000, 30)                     as volume
)
pt.append!(t)

// 5. query it
select sym, avg(price) as avgPx
from loadTable("dfs://demo", `trades)
where ts between 2024.01.01T09:30:00.000 : 2024.01.01T09:31:00.000
group by sym
```

## 4. Query from Python

```python
df = s.run("""
    select sym, avg(price) as avgPx
    from loadTable('dfs://demo', `trades)
    where ts between 2024.01.01T09:30:00.000 : 2024.01.01T09:31:00.000
    group by sym
""")
print(df)   # pandas DataFrame
```

## 5. Add a stream table + subscription

```dolphindb
share streamTable(1000:0, `ts`sym`price, [TIMESTAMP, SYMBOL, DOUBLE]) as ticks

def onTick(msg) {
    // msg is a table when msgAsTable=true
    print("got " + size(msg) + " rows")
}

subscribeTable(
    tableName=`ticks,
    actionName=`demo,
    handler=onTick,
    msgAsTable=true,
    batchSize=100,
    throttle=0.1
)

// publish
insert into ticks values(now(), `AAPL, 101.5)
```

## Where to go next

- `docs/20-sql/context-by.md` — the single most useful (and most misused)
  SQL construct in DolphinDB.
- `docs/30-database/partitioning.md` — choose the right partitioning scheme.
- `docs/60-api/python-api.md` — full Python API cheat-sheet.
- `patterns/` — "how do I do X" recipes.
