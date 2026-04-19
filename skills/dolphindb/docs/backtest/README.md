# Backtest & simulated matching

DolphinDB's backtest toolkit spans **four separate engines**. They compose
but each does one thing well — picking the right one is the biggest win.

## Which engine do I want?

| Goal | Engine | File |
|------|--------|------|
| Event-driven strategy backtest on historical bars / snapshots / ticks, with P&L, positions, commission, slippage. Supports stocks / futures / options / bonds / crypto / multi-asset / margin trading. | **Backtest plugin** (`Backtest::`) | `backtest-plugin-guide.md` |
| Realistic L2 tick-by-tick matching (honor order book, partial fills, queue position). Usually fed by the Backtest plugin, but can be used standalone. | **Matching Engine Simulator** (`MatchingEngineSimulator::`) | `matching-engine-guide.md` |
| Full virtual exchange (orders, partial fills, cancels, FIX-style semantics) for end-to-end strategy + execution testing. | **Simulated Exchange Engine** (`simulatedexchangeengine::`) | `../plugins/simulatedexchangeengine.md` |
| Live / paper order lifecycle management (place / cancel / amend, position book, per-account risk). Not a backtester per se, pairs with live feeds or with the engines above. | **Order Management Engine (OME)** | `../plugins/order_management_engine.md` |

Default for strategy research: **Backtest plugin**. It internally uses the
Matching Engine Simulator and gives you the fewest moving parts.

Use Matching Engine Simulator **standalone** when you are already driving
a custom event loop (e.g. your own CEP pipeline) and only need realistic
fills.

## What lives in this directory

- `README.md`                    — this file.
- `backtest-plugin-guide.md`     ★ Backtest plugin: install, strategy shape, config, callbacks, data, running, results.
- `matching-engine-guide.md`     — Matching Engine Simulator: how it models the book and fills.
- `assets.md`                    — 6 asset types (stock / future / option / bond / crypto / multi-asset / margin-trading) and their config differences.
- `traps.md`                     ★ the lookahead / slippage / commission / ordering pitfalls you will hit.
- `factors.md`                   ★ factor / alpha computation: `@state`, PIT, lookahead, 3 execution modes (batch/stream/backtest), WQ101 / GTJA191 modules.
- `tutorials-index.md`           — curated index of full worked case studies under `docs/tutorials/`.
- `backtest_intro.md`            — upstream intro page (short).

## Where the details live

- `../plugins/backtest.md`           — 44 KB main plugin manual (interface list).
- `../plugins/backtest/quick_start.md` (20 KB), `stock.md` (49 KB), `futures.md` (21 KB), `option.md` (18 KB), `digital_currency.md`, `interbank_bonds.md`, `multi_asset.md` — per-asset manuals.
- `../plugins/backtest/interface_description.md` (67 KB) — every plugin function signature.
- `../plugins/matchingEngineSimulator/*` — MES internals.
- `../tutorials/*backtest*.md`, `../tutorials/cta_*`, `../tutorials/*factor*backtest*` — complete worked examples.

## Minimum example (copy-paste-run)

```dolphindb
loadPlugin("MatchingEngineSimulator")    // required before Backtest
loadPlugin("Backtest")

// 1. Strategy body: on each bar, open a long if flat.
def onBar(mutable context, msg, indicator) {
    for (sym in msg.keys()) {
        pos   = Backtest::getPosition(context.engine, sym)
        price = msg[sym].close
        if (pos.longPosition < 1) {
            Backtest::submitOrder(
                context.engine,
                (sym, context.tradeTime, 5, price + 0.02, 100, 1),
                "buyOpen"
            )
        }
    }
}

// 2. Config + callbacks
config = {
    startDate:     2023.07.11,
    endDate:       2023.07.11,
    strategyGroup: `stock,
    cash:          1000000.0,
    commission:    0.00015,
    tax:           0.001,
    dataType:      3                     // 3 = minute bar
}
callbacks = { onBar: onBar }

// 3. Create + run
try { Backtest::dropBacktestEngine("t01") } catch(ex) { /* ignore */ }
engine = Backtest::createBacktester("t01", config, callbacks, false)

bars = loadText("./barData.csv")
Backtest::appendQuotationMsg(engine, bars)

// 4. Results
trades = Backtest::getTradeDetails(engine)
summary = Backtest::getReturnSummary(engine)
```

Read `backtest-plugin-guide.md` next.
