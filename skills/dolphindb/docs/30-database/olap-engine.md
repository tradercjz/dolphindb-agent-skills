# OLAP engine

**OLAP** is the legacy / simpler columnar engine. Still widely used for
append-only wide tables where you don't need per-row dedup or `upsert`.

## When to choose OLAP over TSDB

- Wide analytic tables with **no per-row point lookup** requirement.
- You want the simplest storage model (one file per column per partition).
- Your access pattern is **full scans + GROUP BY** rather than
  `(sym, time-range)` lookups.

For new projects prefer TSDB unless the above clearly applies.

## Create

```dolphindb
db = database("dfs://fact", VALUE, 2024.01.01..2030.12.31, engine="OLAP")

pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `fact,
    partitionColumns = `date
)
```

OLAP does **not** accept `sortColumns` or `keepDuplicates`.

## Behavior

- One column file per partition; full-partition column reads.
- No background compaction.
- Updates rewrite the **whole partition**.

## Cache

Query-result and data-cache are controlled by:

```dolphindb
flushOLAPCache()
```

## Traps

- **Update on OLAP** rewrites the entire partition. Batch updates or
  migrate to PKEY if you need row-level mutation.
- **Per-symbol latest lookup is slow** without sort metadata — prefer TSDB
  with `keepDuplicates=LAST` for that pattern.

## See also

- `olap.md`.
