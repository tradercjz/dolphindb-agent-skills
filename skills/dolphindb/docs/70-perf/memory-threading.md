# Memory & threading

## Threads

DolphinDB uses a pool of worker threads:

| Pool | Config key | Purpose |
|------|-----------|---------|
| Worker | `workerNum` | General tasks (queries, appends). |
| Local executor | `localExecutors` | Per-partition task executor. |
| Remote executor | `remoteExecutors` | Cross-node task dispatch. |
| Web worker | `webWorkerNum` | Web UI requests. |
| Subscribe executor | `subExecutors` | Streaming subscription handlers. |

Rule of thumb: `workerNum` ≈ number of physical cores. `localExecutors`
can equal `workerNum`.

## Memory

| Config key | Meaning |
|------------|---------|
| `maxMemSize` | Hard cap per node (GB). Beyond this, OOM errors. |
| `memoryReleaseRate` | How aggressively to return memory to the OS. |
| `chunkCacheEngineMemSize` | TSDB/OLAP cache size. |
| `OLAPCacheEngineSize`, `TSDBCacheEngineSize` | Per-engine caches. |

**Inspect**: `getMemUsage()`, `getPerf()`, `pnodeRun(getMemUsage)`.

## Reducing memory use

- Query only needed columns (`select col1, col2` not `*`).
- Use SYMBOL for repeated strings.
- Filter by partition first; never scan all partitions.
- For big result sets from the API, prefer `session.runBlock(script)` to
  stream rows instead of materializing.
- Clear session variables: `undef(all=true)` or `undef(`varName)`.

## Out-of-memory

If you hit OOM:
1. Check `getMemUsage()` per node.
2. Identify top consumers: `getCompletedQueries()`.
3. Kill runaway queries: `cancelConsoleJob`, `cancelJob`.
4. Tune `maxMemSize` and/or `chunkCacheEngineMemSize`.
5. For repeated offenders, see `../omc/omc_server_hang_guidelines.md`.

## Subscription memory

Stream tables are memory-resident by default. Persistence + `retentionMinutes`
+ `cacheSize` cap memory. Cache size is in **rows**, not bytes — size it
based on row width.

## Parallelism pitfalls

- **Writing to the same partition from many threads** serializes on the
  partition lock. Split by partition key to parallelize writes.
- **`peach`** parallelism is limited by `workerNum`. Extra parallelism
  beyond worker pool queues.
- **UDFs calling `run`** in a loop serialize at the server — batch queries.

## See also

- `../90-admin/` — cluster / monitoring / backup pages from `sys_man/`.
- `query-optimization.md`.
