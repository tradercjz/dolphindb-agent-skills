# Backtest plugin — practical handbook

## Contents
- Install & load
- Strategy skeleton (`initialize` / `onBar` / `onSnapshot` / …)
- Engine configuration (`createBacktester`)
- Submitting orders (`submitOrder` codes, cancel, modify)
- Subscribing indicators (`subscribeIndicator`)
- Feeding data (bars / snapshots / trades)
- Reading results (trades, daily PnL, positions, cash)
- Performance optimization

Event-driven strategy backtest engine packaged as a DolphinDB plugin. All
functions live under the `Backtest::` namespace.

Requires **DolphinDB Server ≥ 2.00.14 or ≥ 3.00.2**. Internally depends on
the **MatchingEngineSimulator** plugin — load it first.

## 1. Install & load

```dolphindb
login("admin", "123456")
listRemotePlugins()                       // confirm plugin is available

installPlugin("MatchingEngineSimulator")
installPlugin("Backtest")

loadPlugin("MatchingEngineSimulator")     // must be loaded FIRST
loadPlugin("Backtest")
```

Load order matters: Backtest references symbols from MES at load time.

## 2. Lifecycle

```
config + callbacks
       │
       ▼
createBacktester(name, config, callbacks, jit?)   ──► engine handle
       │
       ▼
appendQuotationMsg(engine, data)   ──► replays data through callbacks
       │                                (onSnapshot/onBar/onTick depending on dataType)
       ▼
getTradeDetails / getOrderDetails / getPosition / getReturnSummary
       │
       ▼
dropBacktestEngine(name)                          ──► tears down
```

Always `try { dropBacktestEngine(name) } catch(e){}` at the top of a script
— re-running with the same name errors out.

## 3. Callbacks you can implement

All are optional except the one matching your `dataType`. Signatures:

| Callback | When it fires | Signature |
|----------|---------------|-----------|
| `initialize`      | once at engine creation | `(mutable context)` |
| `beforeTrading`   | start of each trading day | `(mutable context, date)` |
| `onSnapshot`      | each L1/L2 snapshot | `(mutable context, msg, indicator)` |
| `onTick`          | each trade / order-level tick | `(mutable context, msg, indicator)` |
| `onBar`           | each bar (minute / day) | `(mutable context, msg, indicator)` |
| `onOrder`         | order state changes (acked / partial / filled / cancelled / rejected) | `(mutable context, order)` |
| `onTrade`         | each fill | `(mutable context, trade)` |
| `afterTrading`    | end of each trading day | `(mutable context, date)` |
| `finalize`        | once at end | `(mutable context)` |

Register in `callbacks` dict:

```dolphindb
callbacks = {
    initialize:   initFn,
    onSnapshot:   onSnap,
    onOrder:      onOrder,
    onTrade:      onTrade,
    afterTrading: onDayEnd
}
```

`msg` is a **dict keyed by symbol** (whose value is a row/dict of market
data for that symbol at this event time). Iterate with `for (sym in msg.keys())`.

`context` is the user-defined state carrier — whatever you put there in
`initialize` is available in all subsequent callbacks. `context.engine`,
`context.tradeTime`, `context.tradeDate` are injected by the engine.

## 4. Key `config` keys

```dolphindb
config = {
    // === required ===
    startDate:      2023.07.11,            // inclusive
    endDate:        2023.07.11,            // inclusive
    strategyGroup:  `stock,                // stock / future / option / bond / digitalCurrency / multiAsset / securityCreditAccount
    cash:           1000000.0,             // initial cash
    dataType:       3,                     // 1=snapshot, 2=tick, 3=minBar, 4=dayBar (stock conventions; see per-asset pages)

    // === common ===
    commission:     0.00015,               // rate applied to notional
    tax:            0.001,                 // stamp tax etc. (stock)
    slippage:       0.0,                   // price slippage per unit
    orderDelay:     0,                     // artificial ack latency (ms)
    matchingRatio:  1.0,                   // fraction of touching liquidity that fills

    // === strategy-custom ===
    userConfig:     { myParam: 42 }        // copied into context at initialize
}
```

Per-asset extras: margin ratio, multiplier, margin-trading interest rates,
concentration limits, etc. — see `../plugins/backtest/<asset>.md`.

## 5. Placing orders

```dolphindb
Backtest::submitOrder(
    context.engine,
    (
        sym,                 // SYMBOL
        context.tradeTime,   // TIMESTAMP
        orderType,           // 1=limit, 5=limit with delay; per-asset pages
        price,               // DOUBLE
        qty,                 // LONG
        direction            // 1=buyOpen, 2=sellClose, 3=sellOpen, 4=buyClose, ...
    ),
    "buyOpen"                // user label, free-form string
)
```

`direction` codes differ by asset class — stocks use 1/2 only (buy/sell);
futures and options add open/close distinction (1 buyOpen, 2 sellClose,
3 sellOpen, 4 buyClose). Margin trading adds 5/6/7/8 for financing/lending
open/close. Confirm in `../plugins/backtest/<asset>.md` before use.

Cancel / amend: `Backtest::cancelOrder(engine, orderId)`,
`Backtest::modifyOrder(...)`.

## 6. Querying state inside callbacks

```dolphindb
pos = Backtest::getPosition(engine, sym)           // long/short/available
cash = Backtest::getCashInfo(engine)               // cash / asset / usedMargin
orders = Backtest::getPendingOrders(engine)        // active orders
history = Backtest::getFilledOrders(engine, sym)   // for this symbol
```

## 7. Indicators via reactive state engine

You can subscribe to computed indicators. In `initialize`:

```dolphindb
@state
def pctChg(lastPrice, prevClose) { return lastPrice / prevClose - 1 }

def initialize(mutable context) {
    context.mySignal = 0.0
    Backtest::subscribeIndicator(
        engine     = context.engine,
        metrics    = <[pctChg(lastPx, prevClosePx) as pctChg]>,
        keyColumn  = `symbol,
        dummyTable = snapshotSchema
    )
}
```

In `onSnapshot`, the computed values show up in `indicator`:

```dolphindb
def onSnapshot(mutable context, msg, indicator) {
    for (sym in msg.keys()) {
        if (indicator[sym].pctChg > 0.01) {
            Backtest::submitOrder(context.engine,
                (sym, context.tradeTime, 5, msg[sym].lastPx, 100, 1), "signal")
        }
    }
}
```

`@state` on the factor function makes it a stateful reactive-state metric
(reuses `docs/40-streaming/engines.md`).

## 8. Results

```dolphindb
Backtest::getTradeDetails(engine)    // every fill
Backtest::getOrderDetails(engine)    // every order event
Backtest::getPositionHistory(engine) // daily position snapshots
Backtest::getReturnSummary(engine)   // total return, maxDD, sharpe, winRate
Backtest::getDailyReturn(engine)     // daily P&L vector
```

For multi-metric reporting or attribution, export to DataFrame and
post-process in Python.

## 9. Performance

- **JIT** (pass `true` as 4th arg to `createBacktester`): accelerates tight
  inner loops at a 1-time compile cost. Use for strategies with thousands
  of instruments on L2 tick data.
- **Batch append**: `appendQuotationMsg` accepts a table; call once per
  day rather than per row.
- **`matchingRatio < 1`** reduces matching engine work when you just want
  signal behaviour, not precise fills.
- Full perf notes: `../plugins/backtest/performance_tuning.md`.

## 10. Common APIs at a glance

| Function | Purpose |
|----------|---------|
| `createBacktester` / `dropBacktestEngine` | Engine lifecycle. |
| `appendQuotationMsg` | Feed market data. |
| `submitOrder` / `cancelOrder` / `modifyOrder` | Order actions. |
| `getPosition` / `getCashInfo` / `getPendingOrders` | State lookup. |
| `getTradeDetails` / `getOrderDetails` / `getPositionHistory` / `getReturnSummary` / `getDailyReturn` | Result accessors. |
| `subscribeIndicator` | Register a reactive-state indicator. |
| `getBacktestEngineList` | List engines in current session. |

Complete signature reference: `../plugins/backtest/interface_description.md`.

## See also

- `traps.md` — lookahead bias, slippage, commission, order-delay gotchas.
- `assets.md` — what differs between stock / future / option / bond / crypto / multi-asset.
- `matching-engine-guide.md` — how fills are decided.
- `tutorials-index.md` — case studies.
- `../plugins/backtest.md` — upstream plugin manual.
- `../plugins/backtest/quick_start.md` — upstream walkthrough.
