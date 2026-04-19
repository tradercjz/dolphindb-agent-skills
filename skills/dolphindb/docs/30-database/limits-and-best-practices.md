# Limits & best practices

Hard limits and operational guidelines for DolphinDB DFS databases.

## Hard / soft limits

| Item | Limit | Notes |
|------|-------|-------|
| Partitions per database | ~millions | Controller slows down beyond ~1M. |
| Rows per partition | Practical 100M, hard much higher | Aim 1M–100M. |
| Partition size on disk | 100 MB – 10 GB | <100 MB → overhead; >10 GB → slow recovery. |
| Columns per table | 4096 | |
| SYMBOL dict size per column (TSDB) | 2^21 = 2,097,152 | `S00003`. Use STRING for higher cardinality. |
| Levels in LSM (TSDB) | Configurable | Defaults are fine. |
| Concurrent transactions | Depends on `maxConcurrentTransactions` | Default 1000. |

See `limits.md` for the full list.

## Sizing guidelines

- **Tick data** (~1M rows/day/symbol): date VALUE × sym HASH, ~50 HASH
  buckets. One partition ≈ 1 day × 1 hash-bucket = ~1–5 GB on TSDB.
- **Bar data** (daily bars, ~5k symbols): date VALUE only. Each day is a
  single partition.
- **IoT** (many devices, high rate): date VALUE × device-id HASH(128 or
  512). Use TSDB with `sortColumns=\`device\`ts`.

## Write best practices

- Prefer **bulk `append!`** in 10k–1M row batches over single-row inserts.
- For parallel write: multiple sessions, each writing **disjoint partitions**
  (different dates or different hash buckets). Writing the same partition
  from multiple sessions serializes on the partition lock.
- Turn on `enableTSDBAsyncSorting()` for sustained write workloads.
- Use **`loadText`/`ploadText`** for CSV ingest; `ploadText` is parallel.

## Query best practices

- Always filter by the **partition column** first.
- Put low-cardinality columns first in `where` for TSDB index use.
- Use `select * from ... limit 10` on exploration; never on big tables.
- For sessions that return large DataFrames via Python API, prefer the
  **streaming path** (`session.runBlock`) or server-side aggregation.

## Operational

- **Backup**: `backup` / `backupDB` / `backupTable`. See
  `docs/90-admin/backup-restore.md`.
- **Recovery** kicks in automatically; monitor `getRecoveryTaskStatus()`.
- **Rebalance**: `rebalanceChunksAmongDataNodes()`.

## See also

- `limits.md`, `rebalance.md`, `recovery.md`,
  `transaction.md`.
- `docs/70-perf/` for query-side tuning.
