# Partition pruning — the #1 performance rule

Every query against a DFS partitioned table should reference the
**partition column(s)** in its `where` clause so the planner can prune to
the relevant partitions. Missing this turns a millisecond query into a
full-table scan.

## The rule

For VALUE/RANGE/LIST partitioning, the `where` predicate on the partition
column must be a **direct comparison or range** using the same type as the
column:

```dolphindb
// ✅ Good — date is the partition column
where date = 2024.01.02
where date between 2024.01.02 : 2024.01.05
where date in [2024.01.02, 2024.01.05]
where date >= 2024.01.02 and date < 2024.02.01
```

The following **disable pruning**:

```dolphindb
// ❌ Function wraps the partition column
where year(date) = 2024
where string(date) like "2024-01%"
where bar(date, 7d) = 2024.01.08

// ❌ Cast implicit or explicit
where date = "2024-01-02"        // string vs date

// ❌ Arithmetic on the partition column
where date + 1 = 2024.01.03
```

Rewrite by moving the transformation to the **literal side**:

```dolphindb
// instead of where year(date) = 2024
where date between 2024.01.01 : 2024.12.31

// instead of where string(date) like "2024-01%"
where date between 2024.01.01 : 2024.01.31
```

## HASH partitioning

For HASH, the `where` predicate on the hash-key must be **equality** (or
`in`):

```dolphindb
// ✅
where sym = `AAPL
where sym in `AAPL`MSFT

// ❌ range predicate can't be pruned on HASH
where sym between `A : `M
```

## Composite (COMPO)

Prune at each level independently. Typical:

```dolphindb
where date between 2024.01.02 : 2024.01.05    // prunes date level
  and sym = `AAPL                              // prunes sym hash level
```

## Verifying

Use `EXPLAIN` / `HINT_EXPLAIN` to see chosen partitions:

```dolphindb
select HINT_EXPLAIN * from loadTable("dfs://trades", `trade)
where date = 2024.01.02 and sym = `AAPL
```

The output includes `partitions` — should be a small number, not "all".

## Index + TSDB sortColumns

Pruning selects partitions; the **TSDB level index** (`sortColumns`) then
skips level files within a partition. Both matter:

- Partition pruning → decides which partition dirs to touch.
- Level index → within each chosen partition, which column segments to read.

For best results, lead `sortColumns` with low-cardinality prefix keys
(e.g. `sym`) and the time column last.

## Common rewrites

| Bad | Good |
|-----|------|
| `where year(ts) = 2024 and month(ts) = 1` | `where ts between 2024.01.01 : 2024.02.01` |
| `where sym like "AA%"` | Pre-compute a prefix column; or don't partition by sym. |
| `where temporalParse(tsStr, "yyyy-MM-dd") = 2024.01.02` | `where ts = 2024.01.02` |
| `where substr(sym,0,1) = "A"` | Materialize first-letter column; or avoid filter. |

## Traps

- **Dimension tables** are replicated, not partitioned. No pruning needed
  but also no parallelism — keep them small.
- **Joining a large fact table to another large table** without a partition
  predicate on both sides is a cluster-wide shuffle. Use `aj` or pre-filter.
- **`select *` + `limit 100`** still requires partition pruning to be fast;
  `limit` does not imply pruning.

## See also

- `hint.md`, `hint_explain.md`.
- `../30-database/partitioning.md`, `../30-database/tsdb-engine.md`.
