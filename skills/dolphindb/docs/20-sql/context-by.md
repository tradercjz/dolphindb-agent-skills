# `context by` — per-group vectorized calculation

## Contents
- `context by` vs `group by` (behavior comparison)
- `csort` requirement
- Rolling / cumulative per-group compute
- `having` filter semantics
- Common mistakes & performance notes

`context by` is the **most important DolphinDB-specific SQL keyword**.
It is NOT `group by`. Agents and human users frequently confuse the two;
getting this right is the single biggest correctness win.

## The core distinction

```
group by   → reduces each group to one row     (aggregation)
context by → keeps all rows, computes per-group vectors   (transform)
```

Both partition rows by the grouping columns. `group by` then applies a
**reducer** per group; `context by` applies a **vectorized function** per
group and broadcasts the result back to every row.

## Canonical example

```dolphindb
t = table(
    `A`A`A`B`B`B                 as sym,
    2024.01.01..2024.01.06       as date,
    10.0 11.0 12.0 20.0 22.0 21.0 as price
)

// group by — 1 row per sym
select sym, avg(price) as avgPx from t group by sym
// sym  avgPx
// A    11.0
// B    21.0

// context by — 6 rows, ma3 computed per sym
select sym, date, price, mavg(price, 3) as ma3 from t context by sym
// sym  date        price  ma3
// A    2024.01.01  10.0
// A    2024.01.02  11.0
// A    2024.01.03  12.0   11.0
// B    2024.01.04  20.0
// B    2024.01.05  22.0
// B    2024.01.06  21.0   21.0
```

## When to use `context by`

- **Rolling windows per symbol**: `mavg`, `mstd`, `mmax`, `mrank`, any
  `m*` / `tm*` / `cum*` function.
- **Per-group ranking / indexing**: `rank`, `cumcount`, `denseRank`.
- **Lag / lead per symbol**: `prev`, `next`, `move`.
- **Cross-sectional per timestamp**: `context by timestamp` with row-wise
  functions like `rank`.

## Execution semantics

1. Rows are partitioned by the `context by` columns (preserving row order
   within each partition).
2. Each column in the `select` list is evaluated **as a vector against the
   partition** — not as a scalar per row. So `mavg(price, 3)` receives the
   full price vector for one symbol and returns a same-length vector.
3. Results are stitched back together in original row order (unless you
   add `order by`).

This is why scalar-looking expressions "just work" with window functions:
they are really vectorized under the hood.

## Combine with other clauses

```dolphindb
// context by + where: filter first, then per-group calc
select sym, date, price, mavg(price, 5) as ma5
from t
where date >= 2024.01.01
context by sym

// context by + having: keep only groups whose latest ma5 > 100
select sym, date, price, mavg(price, 5) as ma5
from t
context by sym
having mavg(price, 5) > 100 and date = max(date)

// context by + csort (context-sort): sort inside each group
select sym, date, price, cumsum(volume)
from t
context by sym csort date
```

`csort` sorts rows **inside each context-by group** before the per-group
vector is evaluated. Essential when data arrives unsorted.

## Multiple columns

```dolphindb
select sym, exchange, date, price, mavg(price, 3) as ma3
from t
context by sym, exchange csort date
```

## `cgroup by` — cumulative group

`cgroup by` is `group by` with *prefix* windows: the aggregation runs over
rows 1..k for each k, producing one row per input row. Useful for YTD-style
calculations.

```dolphindb
select sym, date, cumsum(volume) from t cgroup by sym
```

## Common mistakes

- **Using `group by` where `context by` is intended.** If you meant "add a
  rolling column", you want `context by`. `group by` will error out
  ("column not in group by") or silently collapse rows.
- **Forgetting `csort`** when the source table is not time-ordered. Rolling
  functions assume the per-group vector is in chronological order.
- **Mixing aggregates and row-level expressions in `context by`.**
  `sum(price)` inside `context by` returns a scalar broadcast to every row
  in the group — that's fine, but be aware it is not an aggregation in the
  `group by` sense.
- **Expecting `limit`/`top` to be per-group** — by default they are global.
  Use `context by sym limit N` for per-group top-N.

## See also

- `contextBy.md` — full upstream reference.
- `cgroupby.md` — prefix cumulative grouping.
- `window-functions.md` — comparison with SQL `over(...)`.
- `../../reference/functions/by-theme/数据操作.md` — all `m*`/`cum*`/`row*`
  functions usable inside `context by`.
