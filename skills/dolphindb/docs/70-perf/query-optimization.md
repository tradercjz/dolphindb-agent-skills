# Query optimization

Beyond partition pruning, a handful of rewrites cover most real-world
speed-ups.

## Inspect the plan

```dolphindb
select HINT_EXPLAIN * from ... where ...
```

Output shows chosen partitions, join order, and filter push-down.

## Hints

`/* +hint */` comments in `select` can force the planner:

```dolphindb
select /* +HASH_JOIN */ * from a inner join b on a.k = b.k
```

Common hints live in `hint.md` (under `20-sql/`). Use
sparingly — planner defaults are usually right.

## Rewrites

### Push `where` before `group by`

Filter as early as possible. The planner usually does this, but be explicit:

```dolphindb
// ✅
select sym, avg(price) from t where date >= 2024.01.01 group by sym

// ❌ Filter after aggregation (still correct but can't skip rows)
select sym, avg from (
    select sym, avg(price) as avg from t group by sym
) where avg > 100
```

### Prefer `context by` to `over(...)` for time-series windows

`context by` is often faster and always more concise.

### Project only what you need

```dolphindb
// ✅
select sym, price from t where date = 2024.01.02

// ❌ select *  (pulls every column off disk)
```

### Use `symbol` over `string` for repeated values

SYMBOL columns compress and filter 5–50× faster than STRING.

### Avoid per-row UDFs in `where`

```dolphindb
// ❌ per-row function call
where myClassify(sym) = "tech"

// ✅ pre-compute + equality filter
where sym in techSyms
```

### Asof/window joins on sorted inputs

`aj` and `wj` require the right side to be sorted on the matching cols.
If sorting is the bottleneck, use `pwj` on already-sorted inputs.

### Vector ops over loops

```dolphindb
// ❌
for (i in 0..size(v)-1) { v[i] = v[i] * 2 }

// ✅
v = v * 2
```

## Parallelism

The planner automatically parallelizes partition scans across `workerNum`
threads. Tune with:

- `workerNum`, `localExecutors` (cluster config).
- `parallel` SQL hint (rare).
- `peach(f, xs)` for user-level parallelism in scripts.

## Profile

```dolphindb
getQueryStatus()        // in-flight queries
getCompletedQueries(10) // recent history
getPerf()               // per-node perf counters
pnodeRun(getPerf)       // all nodes
```

## See also

- `partition-pruning.md`, `memory-threading.md`.
- `hint.md`, `hint_explain.md`, `exe_order.md`.
