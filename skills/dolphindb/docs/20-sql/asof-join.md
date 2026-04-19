# `asof join` (`aj`) — time-series alignment

`aj` is DolphinDB's killer join for tick-series work: **for each row in
`left`, find the last row in `right` with a matching key and timestamp ≤
`left.ts`**. Think "as-of".

## Canonical use cases

- **Attach the prevailing quote to each trade** (most common).
- **Point-in-time fundamentals**: align report data by release time, not
  report date.
- **Latest reference** from a slow-changing dim table.
- **Cross-frequency alignment** (1-min bars to tick).

## Signature

```dolphindb
aj(left, right, matchingCols)
```

- `matchingCols` — column name or vector of names. **Last column must be
  the timestamp** to asof on; earlier columns are equality keys.
- Both tables **must be sorted ascending** on the join cols. DolphinDB
  does NOT sort for you.

## Quote-trade example

```dolphindb
trades = table(`IBM`IBM`MS as sym,
               2024.03.15 09:30:01.100 2024.03.15 09:30:01.300 2024.03.15 09:30:01.500 as ts,
               150.0 150.1 220.0 as price)

quotes = table(`IBM`IBM`MS`MS as sym,
               2024.03.15 09:30:00.500 2024.03.15 09:30:01.200 2024.03.15 09:30:00.800 2024.03.15 09:30:01.400 as ts,
               149.9 150.05 219.8 219.95 as bid,
               150.0 150.10 220.0 220.05 as ask)

select * from aj(trades, quotes, `sym`ts)
```

Yields each trade with the most recent preceding quote for that symbol.

## PIT fundamentals

```dolphindb
// fundamentals: (sym, release_ts, eps, book_value)
// ticks:        (sym, ts, price)

aligned = aj(ticks,
             select sym, release_ts as ts, eps, book_value from fundamentals,
             `sym`ts)
// every tick now has the latest eps/bv that was already public.
```

The key trick: name the release timestamp `ts` in the right table, so
`aj` matches on `[sym, ts]` with the asof semantics.

## vs other joins

| Want | Use |
|------|-----|
| Exact equality on all cols | `ej` |
| Left-outer on equality | `lj` |
| Full outer on equality | `fj` |
| "Latest before" by timestamp | **`aj`** |
| "First after" by timestamp | reverse-sort both sides, use `aj` |
| "Within ±N ms" | `wj` (window join) |
| Per-row aggregation of right in ±N ms of left.ts | `wj` |

## Window join (`wj`) for ±N windows

```dolphindb
// For each trade, avg quote in the 1 second before and 1 second after
wj(trades, quotes, -1000:1000,
   <[avg(bid) as avg_bid, avg(ask) as avg_ask]>,
   `sym`ts)
```

`-1000:1000` is a ms offset range relative to left.ts. The second arg is
aggregation metrics, not columns.

## Traps

- **Right table not sorted** → wrong results silently. `aj` assumes
  sorted input. `sortBy!(quotes, \`sym\`ts)` first.
- **Non-unique right rows at the exact boundary** → `aj` picks **one of
  them** (implementation-defined). Ensure monotonicity or dedupe.
- **Mismatched timestamp types** (`TIMESTAMP` vs `NANOTIMESTAMP`) →
  zero matches, silent. Cast both sides to the same type. See
  `../10-language/time-types.md`.
- **Null `ts`** in left → result right-side null.
- **Large right** — `aj` is O((L+R) log R). For very large R, partition
  by `sym` and process per-group.
- **DFS vs in-memory**: DFS-to-DFS `aj` is fully pushed down across
  partitions if both tables share partition scheme; otherwise one side
  is pulled to the executor. Watch `explain()`.

## Chained asof joins (3+ tables)

```dolphindb
aj(aj(trades, quotes, `sym`ts), fundamentals_pit, `sym`ts)
```

Each `aj` is streaming-pipelineable; chain them instead of materializing
intermediate.

## See also

- `joins-overview.md`, `context-by.md`.
- `../patterns/asof-join-quotes-trades.md` — runnable pattern.
- `../10-language/time-types.md` — the type-match gotcha.
- `../30-database/partitioning.md` — colocation for pushdown.
