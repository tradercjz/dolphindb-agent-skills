# 10 — When to reach for `@jit`

**Tags:** perf, jit
**Difficulty:** hard
**Reference doc:** `docs/70-perf/jit-guide.md`, `docs/backtest/factors.md`

## Prompt

I have three candidate functions to speed up. Which should I decorate
with `@jit`, which with `@state`, and which should I leave alone
(rewrite in vectorized SQL instead)?

```dolphindb
// (A) Per-element Black-Scholes called in a scalar loop across strikes
def bsCall(spot, strike, r, t, sigma) { ... }

// (B) Per-symbol rolling factor used inside createReactiveStateEngine
def momentum20(close) { return close / prev(close, 20) - 1 }

// (C) Aggregation over a table: select sum(price * vol) from trades group by sym, date
def sumNotional(price, vol) { return sum(price * vol) }
```

## Rubric

- [ ] **(A)** should be `@jit` — scalar math loop, big speedup.
- [ ] **(B)** should be `@state` (mandatory for reactive engine) AND
      `@jit` is a further speedup for HF frequencies; order of decorators
      doesn't matter.
- [ ] **(C)** should NOT be `@jit` — the SQL engine's vectorized
      aggregation is already near-optimal; JIT adds compile overhead with
      no gain, and table-shaped inputs aren't supported inside JIT
      anyway. Rewrite inline as SQL.
- [ ] Mentions that `@jit` silently falls back to interpreter if the
      body uses unsupported types (STRING, tables, dicts).
- [ ] Mentions verifying with `getFunctionView("bsCall").jit == true`.

## Expected artifact (minimum)

```dolphindb
@jit
def bsCall(spot, strike, r, t, sigma) { ... }      // A

@state
@jit
def momentum20(close) { return close / prev(close, 20) - 1 }   // B

// C: don't wrap in a UDF at all
select sym, date, sum(price * vol) as notional
from trades group by sym, date
```

## Anti-patterns

- Annotating (C) with `@jit` and claiming speedup.
- Omitting `@state` on (B) (silent wrong outputs in reactive engine).
- Using `@jit` on a function that contains `throw` / `try` (unsupported).
- Blindly applying `@jit` everywhere "because it's faster".
