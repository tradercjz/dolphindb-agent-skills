# Partitioning — choosing a scheme

DolphinDB requires every DFS table to be partitioned. The partitioning
scheme is **the most important design decision** — it determines query
parallelism, data locality, and write throughput, and it cannot be changed
without rewriting the data.

## The five partition types

| Type   | Partition key values   | When to use |
|--------|------------------------|-------------|
| `VALUE` | `{v1, v2, …}` → one partition per value | Natural low-cardinality key, especially dates. Most common for time-series. |
| `RANGE` | `[a, b), [b, c), …` | Unbounded values with skewed distribution; you pre-define boundaries. |
| `HASH`  | `hash(key) mod N` | High-cardinality keys; balances data evenly (e.g. per-symbol in COMPO). |
| `LIST`  | Explicit `{[v1,v2], [v3,v4], …}` | Manual bucketing (e.g. by region). |
| `COMPO` | Two levels (e.g. date VALUE × symbol HASH) | Large tables with two natural dimensions. |

## Rules of thumb

- **Time-series**: `VALUE` on the date (or hour for very high-frequency),
  optionally `COMPO` with HASH on symbol.
- **Day-based VALUE partitioning** is the industry-standard default for
  tick data. One partition = one trading day per symbol bucket.
- **Partition size target**: 100 MB – 1 GB of on-disk data per partition
  after compression. Much smaller → metadata overhead; much larger →
  poor parallelism.
- **Avoid** 1M+ partitions per database. Controller will slow down.
- **Prefer HASH over LIST** for high-cardinality secondary dimensions —
  simpler and self-balancing.

## Examples

### Single-level VALUE by date

```dolphindb
db = database("dfs://trades", VALUE, 2024.01.01..2030.12.31, engine="TSDB")
```

Expand the scheme later with `addValuePartitions`:

```dolphindb
addValuePartitions(db, 2031.01.01..2031.12.31)
```

### COMPO: date × symbol hash

```dolphindb
dbDate = database("", VALUE, 2024.01.01..2030.12.31)
dbSym  = database("", HASH, [SYMBOL, 50])            // 50 hash buckets
db     = database("dfs://trades", COMPO, [dbDate, dbSym], engine="TSDB")

pt = db.createPartitionedTable(
    schema, `trades, `ts`sym,
    sortColumns=`sym`ts
)
```

This is the canonical layout for multi-symbol tick tables.

### RANGE for skewed numeric keys

```dolphindb
db = database("dfs://orders", RANGE,
    0 1_000_000 10_000_000 100_000_000 int(1e15)    // pre-sized
)
```

Use when distribution is predictable but non-uniform. Extend with
`addRangePartitions`.

## Partition pruning

Every query **must filter by the partition column** in `where` to get
parallelism and locality. See `docs/70-perf/partition-pruning.md`.

## Changing partitioning

You cannot alter the partitioning scheme of an existing table. To migrate:

1. Create a new database with the new scheme.
2. Create a new table.
3. Copy data via `select ... from oldTable`, then `append!` to new table
   (per partition, to avoid OOM).
4. Drop the old table.

## Traps

- **Partition column must never be NULL** for VALUE partitions (`S01001`).
- **Invisible characters in STRING/SYMBOL partition keys are rejected**
  (`S01018`). Strip whitespace before loading.
- **Too many HASH buckets** fragment small tables. 10–50 is usually enough
  for symbol HASH.
- **Using date+time in the same partition key** rarely helps. Partition by
  date; let `sortColumns` (TSDB) sort within a day.
- **Writing to non-existent partitions** (outside the declared range) is
  rejected by default (`S01016`). Extend the scheme first.

## See also

- `db_partitioning.md` — comprehensive upstream guide.
- `patterns/partition-design.md` — worked examples by data size.
