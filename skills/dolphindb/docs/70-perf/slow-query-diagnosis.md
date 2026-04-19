# Diagnosing slow queries — a checklist

## Contents
1. Partition pruning
2. Sort-column & column selection (TSDB)
3. `getPerfMon()` / `getSessionMemoryStat()`
4. `EXPLAIN` plan shape
5. SQL anti-patterns
6. Data skew / hot partitions
7. Engine-specific (OLAP / TSDB / PKEY)
8. Memory settings
9. Compute nodes & separation of storage
10. Client side + triage script template


When a query is slow, work down this list in order. Most production
slowness is **item 1 or 2**.

## 1. Partition pruning — did it happen?

```dolphindb
explain(<select * from loadTable("dfs://tick", `trade)
         where date = 2024.03.15 and sym = `IBM>)
```

Look at the output:
- `scannedPartition: 1` (or N for N days) → good, pruned.
- `scannedPartition: 4821` → **full scan**, fix the WHERE.

Common pruning killers:

| Broken | Fix |
|--------|-----|
| `where year(date) = 2024` | `where date between 2024.01.01 : 2024.12.31` |
| `where date + 1 = 2024.03.16` | `where date = 2024.03.15` |
| `where sym like "IB%"` | `where sym in (...)` |
| `where date = today()` inside subscribe handler | bind `today()` to a var at top of handler |
| Type mismatch: `where date = 2024.03.15 09:30:00` (TIMESTAMP vs DATE) | cast filter to partition type |

Detail: `partition-pruning.md`.

## 2. Sort-column and column selection (TSDB)

For TSDB tables, point lookups use the `sortColumns` BTree. `sym` first,
`ts` last is the standard for tick data:

```dolphindb
db.createPartitionedTable(...,
    sortColumns = `sym`ts,             // filter on sym hits the index
    keepDuplicates = ALL)
```

Verify:

```dolphindb
schema(loadTable("dfs://tick", `trade)).sortColumns
```

Also: **read only the columns you need.** `select *` reads every column
file; `select sym, ts, price` reads 3. For 50-column tables this is
10× saving.

## 3. `getPerfMon()` / `getSessionMemoryStat()`

On a running node:

```dolphindb
getPerfMon()                    // per-session recent job stats
getCompletedQueries(20)         // last 20 queries + runtime
getRunningQueries()             // currently executing
getSessionMemoryStat()          // which session holds what memory
```

Look for:
- `elapsedTime` spikes on specific shapes of query.
- `memoryUsed` > 80% of the box → GC thrashing, add RAM or split work.

## 4. `EXPLAIN` plan shape

```dolphindb
explain(<select sym, avg(price) from loadTable("dfs://tick",`trade)
         where date = 2024.03.15 group by sym>)
```

Key fields:
- `tasks` — parallel partition workers. Want ≥ `workerNum`.
- `taskTime` — per-partition work. Huge outliers ⇒ hot partition, rebalance.
- `transferTime` — network. Large ⇒ compute-storage separation
  overhead; consider compute nodes local-cache.
- `strategy` — `HASH`, `SEGMENT_BY_PARTITION`, etc. Avoid `BROADCAST`
  on large tables.

Details: `query-optimization.md`, `../tutorials/DolphinDB_Explain.md`.

## 5. SQL anti-patterns

| Anti-pattern | Fix |
|-------------|-----|
| `group by` used where you meant `context by` | use `context by` (keeps rows) |
| `context by` without `csort` when data isn't time-sorted | add `csort ts` |
| `order by` without `limit` | add `limit` or remove `order by` |
| `distinct` on a giant column | `group by col` then `select col` |
| JOIN with function on key: `on f(a) = b` | precompute key column |
| `left.col in right.col` via `in` on huge right | use `ej`/`lj` join |
| Repeated same-query calls inside a loop | hoist outside the loop, reuse result |

## 6. Data skew / hot partitions

```dolphindb
select count(*) from loadTable("dfs://tick", `trade)
where date = 2024.03.15
group by sym
order by count(*) desc
limit 10
```

If top sym has 100× the rows of median → hot partition. Remedies:
- HASH partition by sym on top of VALUE by date.
- Finer time partitioning (`DATEHOUR` instead of `DATE`).
- Colocate related partitions; avoid `BROADCAST`.

## 7. Engine-specific

- **OLAP**: poor for updates, great for bulk scan. Don't `update` it in
  a loop.
- **TSDB**: sort-column point lookups fast; full scan slow relative to
  OLAP.
- **PKEY**: upsert-fast; range scan slightly slower than OLAP.
- Pick with `../30-database/tsdb-engine.md`, `olap-engine.md`,
  `pkey-engine.md`.

## 8. Memory settings

If you see `The server ran out of memory`:

- `maxMemSize` per node (config) — raise; leave 20% for OS.
- `chunkCacheEngineMemSize` — TSDB write-ahead cache.
- `memoryReleaseRate` — how aggressively GC returns to OS.
- `warningMemSize` — threshold for auto-releasing caches.

## 9. Compute nodes & separation-of-storage

Slow DFS read on compute-only nodes? Check `enableLocalCache`, and
whether the query hits a few partitions (local-cache-friendly) or
thousands (not worth caching).

Tutorial: `../tutorials/best_practice_for_storage_compute_separation.md`.

## 10. Client side

Still slow after server says fast? Then:

- Python API: use `tableAppender` / `PartitionedTableAppender`, not
  row-by-row `append!`.
- Big result pulls: `session.runFile` + streaming fetch; or compress:
  `session.enableStreaming(0)` and `session.run("...", pickleTableToList=True)`.
- Network: run `run("getNodeAlias()")` latency test; < 1 ms means not
  network-bound.

## Script template for quick triage

```dolphindb
def triage(qstr) {
    q = parseExpr(qstr)
    plan = explain(q)
    start = now()
    result = eval(q)
    elapsed = now() - start
    return dict(`elapsed`rows`plan, [elapsed, size(result), plan])
}

triage("select sym, avg(price) from loadTable('dfs://tick',`trade) where date = 2024.03.15 group by sym")
```

## See also

- `query-optimization.md`, `partition-pruning.md`, `memory-threading.md`.
- `jit-guide.md` when CPU-bound scalar loops dominate.
- `../tutorials/DolphinDB_Explain.md`,
  `../tutorials/sql_performance_optimization_wap_di_rv.md`,
  `../tutorials/api_performance.md`,
  `../tutorials/perf_opti_glibc.md`.
