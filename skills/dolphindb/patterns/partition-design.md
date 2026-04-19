# Pattern — designing a DFS partition scheme

## Problem

Given a new data source, pick a partitioning scheme that:
- Prunes well under typical `where` clauses.
- Keeps partition size in the **100 MB – 1 GB on-disk** sweet spot.
- Parallelizes reads and writes without lock contention.

## When to use / not use this recipe

| Use for | Skip if |
|---------|---------|
| Time-series tick / bar / snapshot / IoT data | Pure reference / dimension data → dimension table, no partitioning. |
| Tables that will grow unboundedly | Tables that fit comfortably in memory → use in-memory / stream tables. |

## Quick picks

| Data shape | Scheme |
|------------|--------|
| Daily bars, few thousand symbols | `VALUE` by date |
| Tick data, multi-symbol, high frequency | `COMPO(VALUE by date, HASH(SYMBOL, 20-50))` |
| Per-device IoT, many devices, high rate | `COMPO(VALUE by date, HASH(SYMBOL, 50-200))` |
| Append-only logs | `VALUE` by date or `VALUE` by date-hour |
| Skewed numeric key (e.g. order-id) | `RANGE` pre-sized |

## Solution — step by step

### 1. Estimate per-day volume

Compute expected rows × avg bytes/row × TSDB compression (typically 3–10×).
Target: **one partition ≈ 0.1–2 GB** post-compression.

```
rows/day × cols × avg-col-bytes / compression ≈ per-partition size
```

### 2. Pick date granularity

- Size < 100 MB/day? — Partition by **month** (VALUE by monthOf).
- Size 100 MB – 10 GB/day? — Partition by **date**.
- Size > 10 GB/day? — Add a second dim: COMPO(VALUE by date, HASH(SYMBOL, N)).

### 3. Pick HASH bucket count (N) if COMPO

- N chosen so that `(per-day data) / N` ≈ 100 MB – 1 GB.
- Prefer 2^k or small primes; exact value is not critical.
- Usually **20–50** for tick; **50–200** for IoT.

### 4. Define sortColumns (TSDB only)

- Lead with **low-cardinality prefix keys** that appear in `where` (usually
  `sym`).
- End with the **time column**.

### 5. Pre-declare the date range

VALUE-by-date requires the date scheme to cover the full expected range.
Declare a generous range; extend later with `addValuePartitions`.

## Worked example — 5M ticks/sec × 8h × 5000 symbols

Estimate: ~1.4×10^11 rows/day ≈ 1 TB raw, 100–200 GB on disk with TSDB
compression.

- 1 partition / day → too big.
- Split by HASH(SYMBOL, 64) → ~2 GB / partition. OK for TSDB.
- Partition columns: `[ts, sym]` with COMPO.

```dolphindb
dbDate = database("", VALUE, 2024.01.01..2030.12.31)
dbSym  = database("", HASH,  [SYMBOL, 64])
db     = database("dfs://hf", COMPO, [dbDate, dbSym], engine="TSDB")

schema = table(1:0, `sym`ts`bid`ask`bidSz`askSz,
    [SYMBOL, NANOTIMESTAMP, DOUBLE, DOUBLE, INT, INT])

pt = db.createPartitionedTable(
    table            = schema,
    tableName        = `quote,
    partitionColumns = `ts`sym,
    sortColumns      = `sym`ts,
    keepDuplicates   = ALL
)
```

## Variants / gotchas

- **Too many partitions** (1M+ per DB) — controller overhead dominates.
  Drop date granularity or reduce HASH N.
- **Too few partitions** — queries don't parallelize. Add HASH.
- **Uneven data distribution** — HASH(SYMBOL) balances naturally; LIST
  with manual buckets rarely does.
- **Extending the date scheme**: `addValuePartitions(db, 2031.01.01..2031.12.31)`.

## See also

- `docs/30-database/partitioning.md`, `docs/30-database/tsdb-engine.md`,
  `docs/70-perf/partition-pruning.md`.
