# TSDB engine

**TSDB** is the recommended engine for time-series workloads (tick, bar,
IoT, telemetry). It is an LSM-style columnar store with:

- Per-partition **sorted storage** driven by `sortColumns`.
- Background compaction.
- Optional **dedup** via `keepDuplicates`.
- Fast point/range lookup on `(sortColumns prefix, time)`.

## Create

```dolphindb
db = database("dfs://tick", VALUE, 2024.01.01..2030.12.31, engine="TSDB")

pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `tick,
    partitionColumns = `ts,
    sortColumns      = `sym`ts,        // ★
    keepDuplicates   = ALL             // ALL (default) | FIRST | LAST
)
```

## `sortColumns` — the big knob

- The **last** element must be the time column (or any monotonically
  increasing integer).
- Preceding elements are **low-cardinality prefix keys** (typically
  `sym`, `exchange`, `tag`).
- Queries that filter by the prefix + time range get index-seek
  performance (tens of microseconds per range).
- **Wrong choice** (time first, or high-cardinality column first) makes
  TSDB effectively equivalent to OLAP.

Rule of thumb: `sortColumns=\`sym\`ts` covers 90% of quant use-cases.

## `keepDuplicates`

| Value | Semantics | When to use |
|-------|-----------|-------------|
| `ALL` | Keep every row. | Append-only, allow duplicates (default). |
| `FIRST` | Keep only the first row per `sortColumns` prefix. | Enable point-dedup. |
| `LAST` | Keep only the latest row per `sortColumns` prefix. | Snapshots / latest-state lookup. |

Note: `FIRST`/`LAST` **only dedup within the same partition**. Use a date
partition + sym prefix to dedup by (sym, day).

## Point lookup & range scan

TSDB builds a level index over each partition. Queries like:

```dolphindb
select * from pt where sym = `AAPL and ts between t1 : t2
```

use the level index to skip unrelated level files. If `sortColumns` is
`(sym, ts)`, scanning one symbol over a day is near-constant time.

## Async sorting / writes

Set `enableTSDBAsyncSorting` per-session to stream writes without waiting
for sort completion:

```dolphindb
enableTSDBAsyncSorting()   // call once per writing session
```

This improves ingest rate at the cost of slightly delayed visibility.

## Cache & flush

TSDB stages writes in a per-table **cache engine**. Force flush with
`flushTSDBCache()`. The controller auto-flushes based on memory thresholds.

## Traps

- **Changing `sortColumns` later is not possible** — drop and recreate.
- **`keepDuplicates=LAST` + out-of-order writes** → the "latest" is
  whatever sorts latest by `sortColumns`, not necessarily the most recent
  write. Keep a real timestamp column as the last sortColumn.
- **Small partitions** (<100 MB) incur disproportionate overhead because
  each partition keeps its own level metadata.
- **Wildcard SYMBOL cardinality**: TSDB stores a per-column symbol
  dictionary; cardinality >16M will hit limits (`S00003`).

## See also

- `tsdb.md` — definitive upstream reference (35 KB, read for tuning).
- `../70-perf/partition-pruning.md`.
- `dfs-database.md`, `partitioning.md`.
