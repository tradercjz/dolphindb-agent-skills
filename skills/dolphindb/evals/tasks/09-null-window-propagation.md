# 09 — Rolling window returns null even though data is present

**Tags:** language, null
**Difficulty:** hard
**Reference doc:** `docs/10-language/null-handling.md`,
`docs/20-sql/context-by.md`

## Prompt

I have a 1-minute bar table with occasional missing bars (printed as
`NULL` in `close`). I compute a 20-minute MA:

```dolphindb
select sym, ts, mavg(close, 20) as ma20
from bars context by sym csort ts
```

Whenever there's any null in the window, `ma20` is null for 20 rows
after. How do I keep the MA rolling despite sporadic missing bars?

## Rubric

- [ ] Identifies that `mavg` (and related rolling functions) propagate
      nulls through the window. Or depending on the function variant,
      drops nulls — the student should name the specific behaviour of
      `mavg` and show awareness.
- [ ] Fills nulls before the rolling call, using `ffill` (preferred for
      prices) or `nullFill(close, <default>)`.
- [ ] Wraps the fill inside the same `context by sym csort ts` block so
      the fill is per-symbol, not cross-symbol.
- [ ] (Bonus) Notes that `isValid(ma20)` can be used downstream to skip
      warm-up rows.

## Expected artifact (minimum)

```dolphindb
select sym, ts, mavg(ffill(close), 20) as ma20
from bars context by sym csort ts
```

Or, with a richer cleanup:

```dolphindb
clean = select sym, ts, ffill(close) as close
        from bars context by sym csort ts
ma = select sym, ts, mavg(close, 20) as ma20
     from clean context by sym csort ts
```

## Anti-patterns

- `nullFill(close, 0)` for price series — introduces fake zeros that
  destroy the MA.
- Pre-computing `ffill` over the whole table without `context by sym`
  (fills across symbol boundaries).
- Dropping null rows with `where isValid(close)` — changes the window
  semantics silently (20-row window no longer spans 20 minutes).
