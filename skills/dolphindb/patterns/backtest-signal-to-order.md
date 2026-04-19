# Pattern — signal vector → orders inside a Backtest callback

## Problem

You have a **per-symbol factor/signal** computed each bar. You want the
Backtest plugin to translate every signal change into orders, sized by a
cash budget, and respect min-order quantities and position caps.

## When to use

| Use | Don't use |
|-----|-----------|
| Any rule-based strategy: long top quantile, cross moving averages, mean-reversion entry, event trigger. | Pure research where you only need IC/rank-IC metrics — stick with the offline SQL backtest (see `docs/backtest/factors.md`). |
| Signal already available as a column in `msg` or `indicator`. | Signal requires future lookahead — fix the signal first. |

## Solution

### 1. Tag the factor with `@state` and subscribe it

```dolphindb
@state
def myFactor(close, volume) {
    return (close - prev(close, 20)) / prev(close, 20)    // 20-bar return
}

def initialize(mutable context) {
    context.entered  = dict(SYMBOL, BOOL)
    context.targetLong  = 0.10                             // 10% per name
    Backtest::subscribeIndicator(
        engine     = context.engine,
        metrics    = <[myFactor(close, volume) as fac]>,
        keyColumn  = `symbol,
        dummyTable = barSchema
    )
}
```

### 2. Convert signal → target position → order

Classic flow: compute target weight from signal, diff against current
position, place orders for the delta.

```dolphindb
def onBar(mutable context, msg, indicator) {
    cash = Backtest::getCashInfo(context.engine)
    equity = cash.totalAsset                               // mark-to-market

    for (sym in msg.keys()) {
        fac = indicator[sym].fac
        if (not isValid(fac)) continue                     // warmup period

        // 3-state signal: +1 long, 0 flat, -1 short
        signal = iif(fac > 0.02, 1, iif(fac < -0.02, -1, 0))

        pos = Backtest::getPosition(context.engine, sym)
        cur = pos.longPosition - pos.shortPosition
        price = msg[sym].close

        target_notional = signal * equity * context.targetLong
        target_qty = int(target_notional / price / 100) * 100    // lot of 100

        delta = target_qty - cur
        if (delta == 0) continue

        direction = iif(delta > 0, 1, 2)                   // 1=buy, 2=sell
        qty = abs(delta)
        slipped_px = price + iif(delta > 0, 0.02, -0.02)   // aggressive limit

        Backtest::submitOrder(
            context.engine,
            (sym, context.tradeTime, 5, slipped_px, qty, direction),
            "signal"
        )
    }
}
```

### 3. Safety rails

```dolphindb
// per-sym position cap (shares)
MAX_QTY = 100000
if (abs(target_qty) > MAX_QTY) target_qty = MAX_QTY * sign(target_qty)

// per-bar order count cap
if (context.orderCountThisBar >= 50) continue

// minimum notional
if (abs(target_notional) < 5000) continue
```

## Variants

### Long-only, top-quintile portfolio

```dolphindb
def onBar(mutable context, msg, indicator) {
    // collect all signals this bar, rank, pick top N
    syms = array(SYMBOL, 0)
    facs = array(DOUBLE, 0)
    for (sym in msg.keys()) {
        f = indicator[sym].fac
        if (isValid(f)) {
            syms.append!(sym)
            facs.append!(f)
        }
    }

    if (size(facs) < 20) return                   // need enough universe
    rankvec = rank(facs, false) / size(facs)      // 1 = best
    topMask = rankvec >= 0.8

    equity = Backtest::getCashInfo(context.engine).totalAsset
    perName = equity * 0.9 / sum(topMask)         // keep 10% cash buffer

    for (i in 0..(size(syms) - 1)) {
        sym = syms[i]
        price = msg[sym].close
        pos = Backtest::getPosition(context.engine, sym).longPosition

        target = iif(topMask[i], int(perName / price / 100) * 100, 0)
        delta = target - pos
        if (delta == 0) continue

        Backtest::submitOrder(
            context.engine,
            (sym, context.tradeTime, 5,
             price + iif(delta > 0, 0.02, -0.02),
             abs(delta), iif(delta > 0, 1, 2)),
            "rebalance"
        )
    }
}
```

### Event-triggered (cross-over)

```dolphindb
@state
def sma5(x)  { return mavg(x, 5) }

@state
def sma20(x) { return mavg(x, 20) }

// in initialize: subscribe <sma5(close) as s5, sma20(close) as s20>

def onBar(mutable context, msg, indicator) {
    for (sym in msg.keys()) {
        s5  = indicator[sym].s5
        s20 = indicator[sym].s20
        if (not (isValid(s5) and isValid(s20))) continue

        pos = Backtest::getPosition(context.engine, sym).longPosition
        price = msg[sym].close

        // golden cross → enter
        if (s5 > s20 and pos == 0) {
            Backtest::submitOrder(context.engine,
                (sym, context.tradeTime, 5, price + 0.02, 100, 1), "gc_enter")
        }
        // death cross → exit
        if (s5 < s20 and pos > 0) {
            Backtest::submitOrder(context.engine,
                (sym, context.tradeTime, 5, price - 0.02, pos, 2), "dc_exit")
        }
    }
}
```

## Gotchas

- **`subscribeIndicator` must be called in `initialize`** (or at engine
  creation), not inside `onBar`. The reactive engine needs the metric
  definitions before the first tick arrives.
- **`indicator[sym]` is null until warm-up finishes.** Guard with
  `if (not isValid(fac)) continue`.
- **Order type code 5 is delayed limit** (recommended default for L1/bar
  execution). Type 1 is plain limit; check asset-specific docs for more.
- **Lot size** is your responsibility. `int(qty / 100) * 100` for CN stocks;
  futures use 1 contract = 1 "share".
- **Cash lockups**: sending overlapping orders without checking
  `getPendingOrders` can double-commit cash. Track `context.pending` or
  read from `getPendingOrders`.
- **Same-bar signal → order → fill is optimistic.** See `../docs/backtest/traps.md`.

## See also

- `../docs/backtest/backtest-plugin-guide.md`.
- `../docs/backtest/factors.md` for `@state` factor design.
- `../docs/backtest/traps.md` for lookahead and slippage.
- `../docs/tutorials/cta_strategy_implementation_and_backtesting.md` — full 56 KB case study.
- `../examples/backtest-quickstart.dos`.
