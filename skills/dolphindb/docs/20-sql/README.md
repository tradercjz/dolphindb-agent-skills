# 20-sql — DolphinDB SQL

DolphinDB's SQL dialect is close to ANSI but **not** identical. The files
in this directory focus on the constructs agents get wrong most often.

## Hand-authored trap docs

- `select-where.md`         — filter precedence, partition-column
                              requirement, symbol-literal rules.
- `group-by.md`             — aggregation, `having`, ordering.
- `context-by.md`           ★ per-group vectorized calc — **read this before
                              writing any rolling query**.
- `pivot-by.md`             ★ DolphinDB's pivot is built in; no cross-join needed.
- `window-functions.md`     — `over ... order by`, `rows between`, difference
                              from `context by`.
- `joins-overview.md`       — equi / left / full / cross / **asof** / **window**
                              / prefix / left-semi. The asof and window joins
                              are core to quant use-cases.
- `asof-join.md`            ★ dedicated page for `aj` / `wj` — quote-trade
                              alignment, PIT fundamentals, sort requirement,
                              type-mismatch trap.
- `update-insert-delete.md` — mutations, `append!`, `upsert!` (PKEY only),
                              `sqlUpdate` / `sqlDelete`.

## Full keyword reference

Every SQL keyword has its own file in this directory (sourced from
`progr/sql/*.md` upstream). Read a trap file first, then consult
`<keyword>.md` for the exhaustive definition.

Key files:

| Topic | File |
|-------|------|
| `select` | `Select.md` |
| `where` | `where.md` |
| `group by` | `groupby.md` |
| `cgroup by` | `cgroupby.md` |
| `context by` | `contextBy.md` |
| `pivot by` | `pivotBy.md` |
| Analytic (`over`) | `analyticFunction.md` |
| `asof join` / `aj` | `asofjoin.md` |
| `window join` / `wj` / `pwj` | `windowjoin.md` |
| `equi join` / `ej` / `sej` | `equijoin.md` |
| `left join` / `lj` / `lsj` | `leftjoin.md` |
| `update` | `update.md` |
| `delete` | `delete.md` |
| `insert into` | `insertInto.md` |
| `alter` | `alter.md` |
| Execution order | `exe_order.md` |
| Hints / EXPLAIN | `hint.md`, `hint_explain.md` |
