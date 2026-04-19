# 05 — Sizing orders from a signal in Backtest plugin

**Tags:** backtest
**Difficulty:** medium
**Reference doc:** `patterns/backtest-signal-to-order.md`,
`docs/backtest/backtest-plugin-guide.md`

## Prompt

Inside a Backtest plugin `onBar`, I have a per-symbol signal in
`[-1, 0, 1]` from an indicator. I want to rebalance each symbol to
`signal * 10%` of equity each bar. How do I turn that into orders?

## Rubric

- [ ] Reads current equity via `Backtest::getCashInfo` (and `totalAsset`).
- [ ] Reads current net position via `Backtest::getPosition` for each
      symbol.
- [ ] Computes `target_qty` as `int(signal * equity * 0.10 / price / 100) * 100`
      (100-lot round-down for CN stocks, or equivalent).
- [ ] Computes `delta = target_qty - current` and only submits an order
      if `delta != 0`.
- [ ] Passes `direction = iif(delta > 0, 1, 2)` (buy / sell) with
      `abs(delta)` as quantity.
- [ ] Skips the bar when `signal == 0` AND current position is already 0
      (to avoid no-op orders).

## Expected artifact (minimum)

```dolphindb
def onBar(mutable context, msg, indicator) {
    cash = Backtest::getCashInfo(context.engine)
    equity = cash.totalAsset
    for (sym in msg.keys()) {
        signal = indicator[sym].signal
        if (not isValid(signal)) continue
        price = msg[sym].close
        target = int(signal * equity * 0.10 / price / 100) * 100
        cur = Backtest::getPosition(context.engine, sym).longPosition
            - Backtest::getPosition(context.engine, sym).shortPosition
        delta = target - cur
        if (delta == 0) continue
        Backtest::submitOrder(context.engine,
            (sym, context.tradeTime, 5,
             price + iif(delta > 0, 0.02, -0.02),
             abs(delta), iif(delta > 0, 1, 2)),
            "rebal")
    }
}
```

## Anti-patterns

- Submitting an order per bar even when the signal hasn't changed (ignoring current position).
- Using signed quantities instead of `direction + abs(qty)`.
- Sizing by `equity * signal` without dividing by `price`.
- No null-check on indicator warm-up.
