# Time types — 10 variants, pick exactly one

## Contents
- The ladder (10 types, precision, literal, range)
- Construction & conversion between levels
- The join-empty trap (type mismatch)
- Partition-key choices
- Timezones
- Comparison rules & NULL literals
- Performance (pruning)


DolphinDB has **10 temporal types**. Mismatches between them are the #1
source of empty-result bugs when joining or filtering. Know the ladder.

## The ladder (low → high precision)

| Type | Precision | Literal example | Range | Typical use |
|------|-----------|-----------------|-------|-------------|
| `DATE`          | 1 day       | `2024.03.15`          | 0000.01.01 – 9999.12.31 | daily bars, partitions |
| `MONTH`         | 1 month     | `2024.03M`            | 0000.01M – 9999.12M     | monthly tables, partitions |
| `TIME`          | 1 ms        | `09:30:00.123`        | 00:00:00.000 – 23:59:59.999 | intra-day offset |
| `MINUTE`        | 1 min       | `09:30m`              | 00:00m – 23:59m         | minute bars |
| `SECOND`        | 1 sec       | `09:30:00`            | 00:00:00 – 23:59:59     | second bars |
| `DATETIME`      | 1 sec       | `2024.03.15 09:30:00` | 1970 – 2038 (int32)     | **avoid** in new tables — Y2038 limit |
| `TIMESTAMP`     | 1 ms        | `2024.03.15 09:30:00.123` | 1970 – 2262         | **default for tick/trade data** |
| `NANOTIME`      | 1 ns        | `09:30:00.123456789`  | intra-day only          | FPGA / exchange nano offsets |
| `NANOTIMESTAMP` | 1 ns        | `2024.03.15T09:30:00.123456789` | 1677 – 2262  | HFT, L2 ticks |
| `DATEHOUR`      | 1 hour      | `datehour(2024.03.15 09)` | 0000.01.01 00H – ... | hourly partitions |

## Construction

```dolphindb
2024.03.15                                       // DATE literal
2024.03.15 09:30:00.123                          // TIMESTAMP literal
2024.03.15T09:30:00.123456789                    // NANOTIMESTAMP literal
date(2024.03.15 09:30:00)                        // cast → DATE
timestamp(2024.03.15)                            // cast → TIMESTAMP (00:00:00.000)
concatDateTime(2024.03.15, 09:30:00.123)         // DATE + TIME → TIMESTAMP
temporalAdd(2024.03.15, 1, "M")                  // 2024.04.15
temporalAdd(ts, 500, "ms")                       // shift timestamp
now()                                            // current TIMESTAMP
gmtime(now())                                    // → UTC
localtime(ts)                                    // TIMESTAMP (UTC) → local
```

## Conversions between levels

```dolphindb
// from a TIMESTAMP column
t.ts.date()         // DATE
t.ts.month()        // MONTH
t.ts.hour()         // INT 0-23
t.ts.minute()       // MINUTE
t.ts.second()       // SECOND
t.ts.time()         // TIME (ms of day)
t.ts.datehour()     // DATEHOUR (partition key)

// aggregate to bars
select first(price) as open, max(price) as high, min(price) as low,
       last(price) as close, sum(vol) as vol
from tick
group by sym, bar(ts, 60_000) as minute_bar                 // 1-minute bar
```

`bar(ts, 60_000)` takes **milliseconds**. For other sizes: `60*1000`,
`5*60*1000`, `24*60*60*1000`. Or use the `minute` / `date` casts above.

## The join-empty trap

This silently returns nothing:

```dolphindb
// trades.ts is TIMESTAMP, quotes.ts is NANOTIMESTAMP
select * from aj(trades, quotes, `sym`ts)                   // 0 rows !
```

Fix by matching types:

```dolphindb
quotes2 = select sym, timestamp(ts) as ts, bid, ask from quotes
select * from aj(trades, quotes2, `sym`ts)
```

Rule: **partition keys, join keys, and filter values must be the exact
same temporal type**, not just the same underlying instant.

## Partition-key choices

| Partition type | Key type | Granularity |
|----------------|----------|-------------|
| `VALUE`        | `DATE`   | one partition per day |
| `VALUE`        | `MONTH`  | one per month |
| `VALUE`        | `DATEHOUR` | one per hour (careful: many partitions) |
| `RANGE`        | `DATE`   | quarters, years, custom |

Never partition by `TIMESTAMP` directly — every row becomes its own
partition. Always aggregate to `DATE` / `MONTH` / `DATEHOUR`.

## Timezones

- All literal and system times are **UTC internally** unless explicitly
  tagged.
- `now()` returns UTC; `gmtime()` is idempotent UTC; `localtime()`
  converts to configured server timezone (`TZ` env or
  `localTimezoneOffset` config).
- **Exchange data convention:** store in UTC, convert on display.
  Chinese exchange data is GMT+8; store `2024.03.15T01:30:00` for a
  09:30 Shanghai tick — or accept the +8 offset and document it.
- Cross-cluster: ensure every node has the same timezone, else
  `datetime` columns shift silently on replication.

See `../tutorials/timezone.md`, `../tutorials/ddb_comparison_rules_of_time_types.md`.

## Comparison rules

- Compare across different types: DolphinDB promotes to higher
  precision, **but only within the same "family"**.
  - `DATE == TIMESTAMP` — compare day, truncating ts.
  - `DATE == NANOTIMESTAMP` — OK, truncated.
  - `TIME == TIMESTAMP` — **error / wrong result** (TIME is within a day).
- Use explicit `date(ts) == d` instead of relying on implicit casts.

## NULL time literal

```dolphindb
00d        // null DATE
00t        // null TIME (ms)
00:00m     // this is 00:00, NOT null!   → use 00M for null MINUTE
00p        // null TIMESTAMP
00n        // null NANOTIMESTAMP
```

Guard with `isValid(ts)` — see `../10-language/null-handling.md`.

## Performance

- **Equality on partition key** → single-partition scan.
  - `where date = 2024.03.15` → prunes.
  - `where year(date) = 2024` → **full scan** (function wraps key).
- **Range** on partition key also prunes:
  `where date between 2024.03.01 : 2024.03.31`.
- **TSDB sort columns**: put `ts` last in `sortColumns=`sym\`ts` so each
  symbol's time-series is contiguous.

## See also

- `data-types.md`, `null-handling.md`, `operators.md`.
- `../20-sql/context-by.md` for per-sym time-ordered compute.
- `../30-database/partitioning.md` for partition-key selection.
- `../tutorials/timezone.md`, `../tutorials/ddb_comparison_rules_of_time_types.md`.
