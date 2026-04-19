# 03 — `asof join` returns zero rows

**Tags:** sql, time-types
**Difficulty:** medium
**Reference doc:** `docs/20-sql/asof-join.md`, `docs/10-language/time-types.md`

## Prompt

I'm attaching the prevailing quote to each trade. Both tables have `sym`
and `ts`, same symbols, overlapping times. But the result is empty:

```dolphindb
// trades.ts is TIMESTAMP, quotes.ts is NANOTIMESTAMP
r = aj(trades, quotes, `sym`ts)
select count(*) from r           // 0 !?
```

What's wrong?

## Rubric

- [ ] Identifies the **type mismatch** between `TIMESTAMP` and
      `NANOTIMESTAMP` join keys.
- [ ] Fixes by casting one side to match the other
      (`nanotimestamp(...)` or `timestamp(...)`).
- [ ] Mentions that both tables must be **sorted** ascending on the
      matching columns for `aj` correctness.
- [ ] (Bonus) Notes the general rule: join keys + partition keys +
      filter literals must match temporal types exactly.

## Expected artifact (minimum)

```dolphindb
quotes2 = select sym, timestamp(ts) as ts, bid, ask from quotes
// or: trades2 = select sym, nanotimestamp(ts) as ts, price, size from trades
sortBy!(quotes2, `sym`ts)
sortBy!(trades,  `sym`ts)
r = aj(trades, quotes2, `sym`ts)
```

## Anti-patterns

- Switching to `lj` — loses the asof semantics.
- Using `wj` with a wide window to "make it match" — hides the root cause.
- Blaming the data (missing symbols) without checking types first.
