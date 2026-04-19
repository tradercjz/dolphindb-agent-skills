# Backtest traps

The mistakes that make a backtest look good but fail live.

## Lookahead bias

The #1 source of too-good-to-be-true returns.

- **Rolling window with current bar included.** `mavg(close, 5)` includes
  the current bar's close — that's a *point-in-time* snapshot at bar close
  and is fine if you also enter at bar close. If you enter at the *next*
  bar's open, signal must be computed as of the previous close. Use `prev`
  or lag the signal by one bar.
- **Using same-bar high/low as a trigger for a limit order filled in the
  same bar.** The engine may fill the order at an impossible price. Gate
  triggers on prior-bar data only.
- **Reactive state indicator with `@state`** is computed **before** the
  strategy callback sees the bar. That's what you want — but make sure
  the indicator uses only past values (see `../10-language/functions.md`
  for `@state` semantics).

## Slippage & commission

- **Zero slippage = free alpha.** Model a realistic spread: stocks
  typically 1–2 bps, illiquid small caps 10+, futures 1 tick.
- **Commission is a *rate*, not absolute.** `commission=0.0001` is
  1 bp of notional. For options / futures per-contract fees, use
  `openFeeRate` / `closeFeeRate` as absolute cash amounts per contract.
- **Tax only on sell side** for CN stocks (`tax=0.001` = 10 bps stamp on
  sell). The engine applies it automatically when `strategyGroup = `stock`.
- **Market impact not modeled** by default. For large orders, reduce
  `matchingRatio` below 1 or split orders manually.

## Fill assumptions

- **`matchingRatio = 1.0`** assumes unlimited liquidity — orders fill at
  the touching price with no queue contention. Fine for illustrative
  tests, wrong for serious execution backtests.
- **Passive orders can sit forever.** With queue modeling enabled, your
  order only fills after sufficient volume trades through at your price.
  If the market never touches your price, you never fill (as expected).
- **Orders submitted in `onBar` fill "at next bar"** by default because
  `orderDelay` is 0 but matching happens on the next tick. Check the
  reported `tradeTime` of each fill.

## Callback ordering

Per event, callbacks fire in this order:

```
data event  →  onSnapshot / onTick / onBar
            →  matching engine processes pending orders
            →  onOrder  (state change)
            →  onTrade  (fills)
```

Inside `onOrder` / `onTrade` you can place **new** orders; they enter the
queue for the *next* tick, not the current one.

## Data cleanliness

- **Timestamps must be monotonic per symbol.** Out-of-order ticks within a
  symbol produce undefined behaviour. Sort before loading.
- **`SYMBOL` vs `STRING`.** The engine uses SYMBOL keys; feed data with
  `sym` column already typed SYMBOL. STRING works via implicit cast but is
  slower and can mismatch on joins.
- **Missing prev-close / settlement price** breaks daily-P&L attribution.
  Fill via a pre-step.

## Engine lifecycle

- **Recreating with the same name fails.** Always
  `try { Backtest::dropBacktestEngine(name) } catch(ex) {}` first.
- **`engine` handle survives session** until the node restarts or you
  drop it. Long-running research sessions leak engines — enumerate with
  `getBacktestEngineList()`.
- **JIT compile time** can exceed short-backtest runtime. Pass `false` as
  the 4th arg to `createBacktester` for one-day smoke tests.

## Position & cash accounting

- **`getPosition(engine, sym)`** returns a struct with `longPosition`,
  `shortPosition`, `availablePosition` (T+1 locks matter for CN A-shares).
  Do not assume `longPosition` is immediately sellable.
- **Cash vs asset value.** `getCashInfo(engine).cash` is idle cash;
  `.totalAsset` includes positions at mark-to-market. Use the right one.
- **Futures margin** is released only on *close*; failing to close before
  day's end ties up margin overnight.
- **Option margin for short positions** is position-dependent; the engine
  recomputes each tick.

## Multi-asset gotchas

- **Symbol-to-asset mapping**: the engine needs a lookup. Register it in
  `initialize` via `setAssetType(sym, `stock)` etc. Missing mapping →
  orders routed incorrectly.
- **Cash is shared across assets.** Positions in futures contracts lock
  margin out of the shared cash pool; plan sizing accordingly.

## Performance

- **`for (sym in msg.keys())`** is the idiomatic inner loop. Vectorizing
  across symbols with `each(...)` or using `<[...]>` metrics is faster
  when possible.
- **Huge `indicator` tables** (thousands of symbols × many metrics) copy
  on every tick. Keep the metric set tight.
- **`appendQuotationMsg` per-row** is slow; load a day of data and append
  once per day.

## Validation checklist

Before trusting a backtest run:

1. Reproduce with a known strategy (e.g. buy-and-hold) and check
   `getReturnSummary` matches hand computation.
2. Log `getPosition` at each day's end; confirm no phantom longs/shorts.
3. Compare `sum(trades.tradeAmt) * commission + sum(sells) * tax` vs the
   engine's `totalFee`.
4. Turn off your signal (force flat) and verify zero P&L, zero fees.
5. Set `slippage = 0.01 * avg_price` and confirm returns degrade
   proportionally — if they don't, your P&L is not respecting slippage.

## See also

- `backtest-plugin-guide.md`, `matching-engine-guide.md`, `assets.md`.
- `../tutorials/best_practice_for_factor_calculation.md` — factor-specific
  lookahead discussion.
