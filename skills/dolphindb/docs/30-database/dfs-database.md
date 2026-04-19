# DFS database basics

A **DFS (Distributed File System) database** is the durable, partitioned,
cluster-wide storage layer. All production tables live in a DFS database.

## Create

```dolphindb
db = database(
    directory        = "dfs://trades",
    partitionType    = VALUE,
    partitionScheme  = 2024.01.01..2025.12.31,
    engine           = "TSDB",       // or "OLAP", "PKEY", "IMOLTP", ...
    atomic           = "TRANS"       // transaction granularity: TRANS or CHUNK
)
```

- `directory` must start with `dfs://`. Standalone servers use the local
  store transparently.
- `partitionType` determines how rows are sharded: `VALUE`, `RANGE`,
  `HASH`, `LIST`, `COMPO` (composite). See `partitioning.md`.
- `engine` is **immutable** once created.
- `atomic="CHUNK"` allows concurrent writes to different chunks of the same
  partition at the cost of larger metadata; `TRANS` (default) is per-transaction.

## Composite partitioning

Stack two partition schemes for big workloads (most common: date × symbol).

```dolphindb
db1 = database("", VALUE, 2024.01.01..2024.12.31)
db2 = database("", HASH, [SYMBOL, 50])
db  = database("dfs://trades", COMPO, [db1, db2], engine="TSDB")
```

## Create a partitioned table

```dolphindb
schema = table(1:0, `sym`ts`price`vol, [SYMBOL, TIMESTAMP, DOUBLE, INT])

pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `trades,
    partitionColumns = `ts`sym,       // must match the COMPO scheme above
    sortColumns      = `sym`ts,       // TSDB-only; reduces disk I/O on point queries
    keepDuplicates   = ALL            // TSDB: ALL | FIRST | LAST
)
```

- `partitionColumns` **must appear in every query's `where` clause**
  (otherwise the full table is scanned).
- `sortColumns` (TSDB only): last column is typically the time column;
  others are **low-cardinality** prefix filters. Do not put a high-cardinality
  column first (e.g. don't lead with `ts`).
- `keepDuplicates`:
  - `ALL` (default) — keep every row; lets duplicates coexist.
  - `FIRST` / `LAST` — dedup on `sortColumns` keeping first/last; enables
    fast lookup by key.

## Dimension table

For small, frequently-joined reference data (e.g. security master), create a
**dimension table** — stored once, replicated to every node:

```dolphindb
dim = db.createDimensionTable(table(1:0, `sym`name, [SYMBOL, STRING]), `security)
```

## Open / load / drop

```dolphindb
pt = loadTable("dfs://trades", `trades)

existsDatabase("dfs://trades")       // → true/false
existsTable("dfs://trades", `trades)

dropTable(db, `trades)
dropDatabase("dfs://trades")
```

## Inspect

```dolphindb
schema(pt)                            // schema dict
getClusterDFSTables("dfs://trades")   // list tables
getDFSTablesByDatabase("dfs://trades")
getTabletsMeta("dfs://trades")        // partition metadata
```

## Traps

- **Choosing the wrong engine is hard to reverse.** You must drop and
  recreate. Default to **TSDB** unless you need PKEY upsert or IMOLTP.
- **Partition count matters.** Aim for 10k–100k rows per partition minimum;
  1M+ partitions per database will stress the controller.
- **Symbol dictionary is per-table (or per-column in TSDB).** A single
  SYMBOL column with 10M distinct values is a bad idea — use STRING.
- **`dfs://` path is the unique ID** — you cannot rename a database.

## See also

- `partitioning.md` — scheme selection guide.
- `tsdb-engine.md`, `olap-engine.md`, `pkey-engine.md`.
- `db_architecture.md`, `db_partitioning.md`.
