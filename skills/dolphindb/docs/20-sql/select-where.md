# `select` / `where`

DolphinDB's `select` looks like ANSI SQL, but a few rules matter a lot for
correctness and performance.

## Clause order (execution)

```
from → where → group/context/pivot by → having → select → order by → limit/top
```

See `exe_order.md` for the exhaustive order used by the planner.

## `where` — the partition-pruning rule

When you query a DFS partitioned table, **the `where` clause must reference
the partition columns** for the planner to prune partitions. Missing this
scans the entire table.

```dolphindb
// Good — date is the partition column
select * from loadTable("dfs://trades", `trade)
where date between 2024.01.01 : 2024.01.03 and sym = `AAPL

// Bad — pruning disabled; full table scan
select * from loadTable("dfs://trades", `trade)
where string(date) like "2024-01%"

// Bad — function on partition column; planner cannot prune
select * from loadTable("dfs://trades", `trade)
where year(date) = 2024
```

Rules for partition-column predicates:
- Simple comparison (`=`, `<`, `<=`, `>`, `>=`, `between`, `in`) works.
- Wrapping the partition column in a function (e.g. `year(date)`, `string(date)`)
  **disables pruning**. Instead filter by raw value ranges.

See `docs/70-perf/partition-pruning.md`.

## `=` inside `where`

In DolphinDB SQL, `=` is the equality operator inside `where`. Outside of
SQL (in regular script), `=` is assignment and `==` is equality. The `where`
clause inherits DolphinDB's SQL rule, so `where x = 1` compares x to 1.

## Literals in predicates

- **Symbol/string**: `sym = \`AAPL` (SYMBOL) vs `sym = "AAPL"` (STRING).
  Do not mix — a SYMBOL column compared to a STRING literal will be cast,
  but can be slower and may lose index benefits.
- **Date**: `date = 2024.01.01`. String dates need `date("2024-01-01")`.
- **Timestamp**: `ts = 2024.01.01T09:30:00.000` (ms) or `...000.000` (ns).
- **Null check**: `where isNull(x)` / `where isValid(x)`, not `x = NULL`.

## `select` with computed columns

```dolphindb
select sym, price, price * volume as notional from t
```

- Column aliases use `as`.
- Computed columns are vectorized per row unless you add `context by` /
  `group by`.
- Use `select *` sparingly on DFS tables — pulls every column.

## `top` / `limit`

Both return at most N rows. They are **global by default**. For per-group
top-N, use `context by`:

```dolphindb
// Global top 10 latest ticks
select top 10 * from t order by ts desc

// Per-symbol top 3 latest
select top 3 * from t context by sym order by ts desc
```

## `distinct`

```dolphindb
select distinct sym from t
```

Fast on dictionary-encoded SYMBOL columns. For counting distinct values,
prefer `count(distinct sym)` or `nunique(sym)`.

## `union` / `union all`

Same as ANSI SQL: `union all` concatenates; `union` deduplicates.

## See also

- `Select.md`, `where.md`, `limit.md`,
  `top.md`, `distinct.md`, `exe_order.md`.
