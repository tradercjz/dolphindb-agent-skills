# Window functions (`over`) vs `context by`

DolphinDB supports ANSI-style window functions via `over (partition by ... order by ... [rows between ...])`, but most real-world code uses **`context by`** or the **`m*` / `tm*` / `cum*` function families** because they are more concise and faster on time-series data.

## `over` syntax

```dolphindb
select sym, ts, price,
       avg(price)   over (partition by sym order by ts rows between 4 preceding and current row) as ma5,
       row_number() over (partition by sym order by ts)                                         as rn
from t
```

- `partition by` → same as `context by` keys.
- `order by` → ordering inside the partition.
- `rows between <N> preceding and current row` → fixed-size window.
- `range between <interval> preceding and current row` → time-range window.

## Equivalent with `context by`

```dolphindb
select sym, ts, price,
       mavg(price, 5)       as ma5,
       cumcount(price)      as rn
from t
context by sym csort ts
```

More concise and usually faster. Use this form for anything time-series.

## Row-wise rolling function families

| Prefix | Meaning | Example |
|--------|---------|---------|
| `m*`   | Row-count window | `mavg(x, 5)` — 5-row moving avg |
| `tm*`  | Time-based window | `tmavg(ts, x, 5s)` — 5-second moving avg |
| `cum*` | Cumulative window | `cumsum(x)` |
| `row*` | Row-wise (cross-column) | `rowSum(a, b, c)` |
| `mTopN*` / `tmTopN*` | Top-N inside window | `mpercentileTopN` |
| TA-lib (`ema`, `sma`, `wma`, `kama`, `t3`, `trima`, `tema`, `dema`, `ma`) | Technical analysis | `ema(x, 20)` |

Full catalog: `../../reference/functions/by-theme/数据操作.md`.

## Common mistakes

- **Forgetting `csort`** inside `context by`. The `m*` functions assume the
  input vector is already time-ordered.
- **Using `over` where `context by` is simpler** — increases code verbosity
  and sometimes costs performance because the planner has fewer optimizations.
- **Mixing `order by` (outer) with `order by` in `over(...)`** — the inner
  one affects the window; the outer affects result ordering.

## See also

- `analyticFunction.md` — full `over(...)` reference.
- `context-by.md` — core idiom.
