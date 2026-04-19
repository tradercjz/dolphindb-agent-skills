# `group by`

Standard SQL-style aggregation.

```dolphindb
select sym, avg(price) as avgPx, sum(volume) as totVol
from t
group by sym
```

## Rules

- Every non-aggregated column in the `select` list must appear in
  `group by` (standard SQL).
- Any column in `group by` is automatically available in `having`.
- The group-by keys may be **expressions**: `group by bar(ts, 60s)`,
  `group by date(ts), hour(ts)`.

## Time bucketing — `bar`, `interval`

```dolphindb
// 1-minute bars per symbol
select sym, first(price) as open, max(price) as high, min(price) as low,
       last(price)  as close, sum(volume) as vol
from t
group by sym, bar(ts, 60s)
```

Use `bar(ts, 60s)` to floor to the bucket; use `interval(ts, 60s, "prev")`
to also fill empty buckets with a previous value (see `interval.md`).

## `having`

Runs after the aggregation. Can reference aggregate expressions:

```dolphindb
select sym, avg(price) as avgPx
from t
group by sym
having avg(price) > 100 and count(*) >= 10
```

## When NOT to use `group by`

If you want to **keep all rows** and add a rolling/cumulative column, use
`context by` instead. See `context-by.md`.

## See also

- `groupby.md`, `cgroupby.md`, `having.md`,
  `interval.md`.
- `../../reference/functions/by-theme/数据操作.md` — all aggregators.
