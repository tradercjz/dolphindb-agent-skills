# Joins in DolphinDB

DolphinDB supports standard SQL joins plus three time-series-specific joins
that are central to quant / IoT workloads. Each has a **two-letter alias**
usable in `from` clauses.

| Kind                         | Keyword (in `from`) | Function form | Typical use |
|------------------------------|---------------------|---------------|-------------|
| Inner equi join              | `inner join`, `ej`  | `ej`          | Standard join on equal keys. |
| Left outer join              | `left join`, `lj`   | `lj`          | Keep all left rows. |
| Right outer join             | `right join`        | —             | |
| Full outer join              | `full join`, `fj`   | `fj`          | |
| Cross join                   | `cross join`, `cj`  | `cj`          | Cartesian product. |
| **Asof join**                | `asof join`, `aj`   | `aj`          | ★ Each left row joined to the **latest** right row at-or-before its time. |
| **Window join**              | `window join`, `wj` | `wj`          | ★ Each left row joined to right rows in a **±window**, aggregated. |
| Prefix window join           | `pwj`               | `pwj`         | Window join keyed by a prefix; for pre-sorted data. |
| Left semi equi join          | `sej`               | `sej`         | Left row joined to a **single** matching right row (not cross-expanded). |

## Asof join (`aj`)

Given a left tick/trade and a right quote, pick the most recent quote at or
before each trade time — per symbol.

```dolphindb
trades = table(
    2024.01.01T09:30:00.5 2024.01.01T09:30:01.2 as ts,
    `AAPL`AAPL                                as sym,
    100.1 100.2                                as px
)

quotes = table(
    2024.01.01T09:30:00.0 2024.01.01T09:30:01.0 2024.01.01T09:30:01.5 as ts,
    `AAPL`AAPL`AAPL                            as sym,
    100.0 100.15 100.25                         as bid
)

// SQL form
select * from aj(trades, quotes, `sym`ts)

// function form
aj(trades, quotes, `sym`ts)
```

- Matching columns: all but the **last** are **equal-match** (typically
  `sym`); the **last** is a **≤** match (typically the time column).
- The right table must be **sorted** by the matching columns.

## Window join (`wj`)

Aggregate right-table rows that fall in a time window relative to each left
row.

```dolphindb
// For each trade, compute avg bid over [-1s, 0] window in quotes
select * from wj(
    trades, quotes,
    -1000:0,                     // window in ms (left-inclusive, right-inclusive)
    <[avg(bid) as avg_bid]>,     // aggregate expressions wrapped with <[ ]>
    `sym`ts
)
```

- Window can be **time-based** (`-1000:0` ms) or **row-based**
  (`<-5:0>`) depending on the key type.
- The aggregates must be wrapped in `<[ ... ]>` (a metacode list).
- For **pre-sorted** inputs, prefer `pwj` — it's faster because it avoids
  re-sorting.

## Semi-equi join (`sej`) vs equi join (`ej`)

- `ej` behaves like SQL inner join — one left row × N matching right rows
  expands into N rows.
- `sej` returns at most **one** right row per left row (the first match,
  or all aggregated depending on the variant). Useful when the right side
  is a dimension table and you just want to enrich columns.

## Writing joins in `from`

```dolphindb
// Equi
select a.sym, a.px, b.bid from trades a inner join quotes b on a.sym = b.sym

// Asof
select a.sym, a.ts, a.px, b.bid from aj(trades, quotes, `sym`ts)
```

Many DolphinDB codebases prefer **function form** (`aj(...)`) over SQL
`from ... join` because it composes better with `update!` / `append!`.

## Traps

- **Right side must be sorted** for `aj` / `wj`. If unsorted, wrap it:
  `aj(trades, select * from quotes order by sym, ts, `sym`ts)`.
- **Equal-match columns must share exact types.** `SYMBOL` vs `STRING`
  silently matches zero rows. Cast with `symbol()` / `string()` if needed.
- **Timezone** — DolphinDB stores naive times. Mixing timezones on left
  and right is your responsibility.
- **Null in match columns** never matches anything in `aj`. Clean with
  `dropna` or `where isValid(ts)` first.

## See also

- `asofjoin.md`, `windowjoin.md`, `equijoin.md`,
  `leftjoin.md`, `fulljoin.md`, `crossjoin.md`,
  `innerjoin.md`, `prefixjoin.md`, `rightjoin.md`,
  `tb_joiner_intro.md` — full keyword manuals.
- `patterns/asof-join-quotes-trades.md` — complete worked example.
