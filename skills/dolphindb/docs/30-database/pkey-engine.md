# PKEY engine — primary-key storage with upsert

**PKEY** is the DolphinDB engine that supports **point update** and
**upsert** by primary key. Internally it is an LSM with a primary-key
index. Use when you need mutation semantics that TSDB/OLAP cannot provide.

## When to choose PKEY

- You need **`upsert!`** — insert-if-absent / update-if-present by key.
- You need **`delete` by key** with low latency.
- You have a **stateful table** such as latest quote, position book,
  order book snapshot, or configuration data.

Do **not** use PKEY for pure append-only tick data — TSDB is faster and
cheaper.

## Create

```dolphindb
db = database("dfs://positions", VALUE, 2024.01.01..2030.12.31, engine="PKEY")

schema = table(1:0, `sym`ts`qty`px, [SYMBOL, TIMESTAMP, INT, DOUBLE])

pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `positions,
    partitionColumns = `ts,
    primaryKey       = `sym,                // ★ required for PKEY
    indexes          = {"ts": "sortIndex"}  // optional secondary indexes
)
```

## Upsert

```dolphindb
newRows = table(
    `AAPL`MSFT as sym,
    [now(), now()] as ts,
    100 200 as qty,
    150.0 260.0 as px
)

pt.upsert!(newRows, keyColNames=`sym, ignoreNull=false, sortColumns=`ts)
```

- `keyColNames` must be a prefix of the declared `primaryKey`.
- `ignoreNull=true` skips null fields on update (partial update).

## Delete by key

```dolphindb
delete from pt where sym = `AAPL
```

## Indexes

- **sortIndex** on a time column speeds up range scans.
- **hashIndex** on a high-cardinality non-PK column speeds up equality lookup.

Create at table creation via `indexes={"col": "sortIndex"}`, or later via
`addColumn` + ALTER commands.

## Traps

- **`upsert!` requires PKEY** — calling it on TSDB/OLAP errors out.
- **Primary key must not be NULL**.
- **Large primary keys** (e.g. full order UUID) increase index size; prefer
  compact types (LONG, SYMBOL).
- **Compaction** runs in background; excessive update rate may cause
  write amplification. Monitor via `getClusterPerf()`.

## See also

- `pkey_engine.md` — definitive upstream reference (20 KB).
- `../20-sql/update-insert-delete.md`.
