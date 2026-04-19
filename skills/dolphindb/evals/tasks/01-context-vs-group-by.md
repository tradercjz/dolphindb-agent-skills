# 01 — `context by` vs `group by`

**Tags:** sql, traps
**Difficulty:** easy
**Reference doc:** `docs/20-sql/context-by.md`

## Prompt

I have a tick table `t` with columns `(sym, ts, price, vol)`. I want to
add, for every row, a 5-tick moving average of `price` within the same
symbol, ordered by `ts`. My attempt returns one row per symbol — wrong:

```dolphindb
select sym, mavg(price, 5) as ma5
from t
group by sym
```

Fix it.

## Rubric

- [ ] Uses `context by sym` (not `group by sym`).
- [ ] Adds `csort ts` (since rows may not be pre-sorted).
- [ ] `select` includes the original row columns (at least `sym`, `ts`,
      `price`) so the result has one row per input row.
- [ ] Names the new column (`as ma5`).
- [ ] Explains **why** `group by` collapses rows while `context by`
      preserves them.

## Expected artifact (minimum)

```dolphindb
select sym, ts, price, mavg(price, 5) as ma5
from t
context by sym csort ts
```

## Anti-patterns

- `order by sym, ts` in place of `csort`.
- Using a `pivot by` (wrong construct for this problem).
- Computing the MA in a loop / per-symbol subquery.
