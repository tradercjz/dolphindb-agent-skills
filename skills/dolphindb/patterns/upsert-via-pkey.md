# Pattern — upsert semantics on DFS

## Problem

Maintain a table where rows are **added or updated by primary key**
(e.g. latest position per account, latest quote per symbol, config values).
TSDB/OLAP do not support this; PKEY does.

## When to use / not use

| Use PKEY + `upsert!` | Don't |
|----------------------|-------|
| Natural PK exists and is small (SYMBOL / LONG) | Pure append-only tick data → TSDB. |
| Write rate is moderate (<100k/s per node) | Write rate >1M/s → consider keyed stream + periodic TSDB flush. |
| You need `delete where pk = ...` | You never delete. |

## Solution

```dolphindb
// 1. Create PKEY database + table
db = database("dfs://positions", VALUE, 2024.01.01..2030.12.31, engine="PKEY")

schema = table(1:0, `acct`sym`qty`avgPx`updatedAt,
               [SYMBOL, SYMBOL, LONG, DOUBLE, TIMESTAMP])

pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `positions,
    partitionColumns = `updatedAt,
    primaryKey       = `acct`sym,           // composite PK
    indexes          = {"sym": "hashIndex"}
)

// 2. Upsert a batch
updates = table(
    `A1`A1`A2                  as acct,
    `AAPL`MSFT`AAPL            as sym,
    100 50 -20                 as qty,
    150.0 260.0 148.5          as avgPx,
    [now(), now(), now()]      as updatedAt
)

pt.upsert!(
    newData      = updates,
    keyColNames  = `acct`sym,
    ignoreNull   = true,                    // partial updates
    sortColumns  = `updatedAt
)

// 3. Read the current state
select * from pt where acct = `A1
```

## Variants

### Incremental update (patch only changed columns)

With `ignoreNull=true`, nulls in the input are skipped — existing columns
retain their old value. Useful when upstream delivers deltas.

### Deletion

```dolphindb
delete from pt where acct = `A1 and sym = `AAPL
```

### Periodic flush to TSDB snapshot

Common pattern: keep **current state** in PKEY, and snapshot to TSDB once
per hour / day for history.

```dolphindb
scheduledJob("pkeySnapshot", "hourly snapshot", <
    hist = loadTable("dfs://positions_hist", `snapshot)
    hist.append!(select *, now() as snapshotTs from pt)
>, 02:00m, today(), today()+365, "D")
```

## Gotchas

- **TSDB does not support `upsert!`** — the call errors out. Always check
  the engine with `schema(db).engineType`.
- **Primary key must be non-null** and fit in a reasonable size. Wide
  composite keys slow index lookups.
- **Index column must exist in `primaryKey` or `indexes`** declared at
  table creation.
- **Update amplification** — each upsert rewrites the level file; monitor
  with `getLevelFileIndexCacheStatus()` under sustained load.

## See also

- `docs/30-database/pkey-engine.md`, `docs/20-sql/update-insert-delete.md`.
- `pkey_engine.md`.
