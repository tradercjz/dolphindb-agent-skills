# 06 — DFS schema for tick data

**Tags:** database, partitioning
**Difficulty:** medium
**Reference doc:** `docs/30-database/partitioning.md`,
`docs/30-database/tsdb-engine.md`

## Prompt

I'm storing CN A-share L1 ticks: ~50 M rows/day, 5000 symbols, columns
`(ts, sym, price, vol, amount)`. Queries are almost always
`where date = X and sym in (...)`. Design the DFS database and table.

## Rubric

- [ ] Chooses **TSDB** engine (not OLAP, not PKEY).
- [ ] Partitioning: **COMPO** of VALUE (by date) + HASH (by sym, ~20–50
      buckets) — or an equivalent two-level scheme.
- [ ] `sortColumns = \`sym\`ts` (sym first so `where sym` uses the
      sort-key index; ts last for time-series locality).
- [ ] Mentions appropriate `keepDuplicates` (e.g. `ALL` for raw ticks, or
      `LAST` if dedup needed).
- [ ] Picks correct temporal type — `TIMESTAMP` or `NANOTIMESTAMP`
      (not `DATETIME`, which has Y2038 limit).
- [ ] Does **not** partition by `TIMESTAMP` directly (would explode).

## Expected artifact (minimum)

```dolphindb
dbDate = database("", VALUE, 2024.01.01..2030.12.31)
dbSym  = database("", HASH,  [SYMBOL, 20])
db     = database("dfs://tick", COMPO, [dbDate, dbSym], engine="TSDB")
db.createPartitionedTable(
    table(1:0, `ts`sym`price`vol`amount,
          [TIMESTAMP, SYMBOL, DOUBLE, LONG, DOUBLE]),
    `trade, `ts`sym,
    sortColumns    = `sym`ts,
    keepDuplicates = ALL)
```

## Anti-patterns

- Partitioning by `sym` alone (hot-symbol skew, no date pruning).
- Partitioning by `TIMESTAMP` directly (millions of tiny partitions).
- Using OLAP (doesn't support sort-column point lookup well).
- `sortColumns = \`ts\`sym` (ts first → sym filter can't use the index).
- Choosing `DATETIME` for `ts` (second precision only, Y2038).
