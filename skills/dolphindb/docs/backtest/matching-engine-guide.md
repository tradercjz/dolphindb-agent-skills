# Matching Engine Simulator (MES)

`MatchingEngineSimulator::` — a deterministic event-driven order-matching
engine. The Backtest plugin uses it under the hood; you can also drive it
directly for custom simulation pipelines.

## When to use MES directly

- You already have an event loop (CEP / reactive state / scheduledJob) and
  just need the **matching semantics**.
- You want queue-position-aware fills on your own L2 data feed.
- You are building a production-like paper-trading pipeline on live data.

If you just want to backtest a strategy end-to-end, use the **Backtest
plugin** instead — MES is wrapped inside it.

## Core concepts

- **Order book per symbol**: maintained from the L2 snapshot / tick feed
  you provide.
- **Latency model**: orders you submit are delayed by `orderDelay` (ms)
  before entering the book.
- **Fill rules**:
  - Marketable orders match against the current top-of-book, optionally
    limited by `matchingRatio`.
  - Passive orders **queue at their price level**. Fills happen when the
    opposite side trades through (respecting queue position estimated from
    L2 depth).
- **Partial fills** are produced when liquidity is insufficient.
- **Cancels / amends** honored according to exchange rules (time priority
  reset on amend).

## Minimal standalone flow

```dolphindb
loadPlugin("MatchingEngineSimulator")

engine = MatchingEngineSimulator::createMatchEngine(
    name       = "mes1",
    config     = {
        matchingRatio: 1.0,
        orderDelay:    0,
        commission:    0.00015,
        tax:           0.001
    },
    dummyQuote = snapshotSchema,       // schema of your market-data feed
    outputTrade  = tradeOutTable,      // receives fills
    outputOrder  = orderOutTable       // receives order events
)

// feed market data (in timestamp order)
MatchingEngineSimulator::appendQuote(engine, snapshotBatch)

// place orders
MatchingEngineSimulator::appendOrder(engine, (sym, ts, type, px, qty, dir, userId))

// inspect
MatchingEngineSimulator::getPosition(engine)
MatchingEngineSimulator::getOrderBook(engine, sym)

// tear down
MatchingEngineSimulator::dropMatchEngine("mes1")
```

## Typical pipeline integration

```
Live / replayed L2 feed  ──►  stream table (quotes)
                               │
                               ▼  subscribeTable → MES.appendQuote
                              MES
                               ▲  subscribeTable → MES.appendOrder
                               │
              strategy stream table (orders)
```

Two subscriptions: one feeds quotes, one feeds the strategy's orders.
Outputs (`tradeOutTable` / `orderOutTable`) can themselves be stream tables
that subscribers consume for P&L.

## Fill-model controls

| Param | Effect |
|-------|--------|
| `matchingRatio` | Fraction of opposing-side liquidity available per match step. `1.0` = all; `0.5` = you only fill half the touching volume. |
| `orderDelay`    | Latency added to each inbound order. Model broker/network latency. |
| `queuePosition` | If enabled, passive orders join the back of the queue at their price; you only fill after size ahead of you trades. |
| `slippage`      | Per-unit price impact on market orders. |
| `commission` / `tax` | Deducted from cash on each fill. |

## When MES fills are wrong / surprising

- **Your feed is out of order.** Quotes must arrive in non-decreasing
  timestamp order per symbol.
- **Passive fill never happens** even though the market traded at your
  price → you're waiting on queue position. Turn queue modeling off if
  you want optimistic fills.
- **Commission / tax not applied** → confirm in config; some asset wrappers
  (e.g. futures) use `feeRate` / `openFeeRate` / `closeFeeRate` instead.
- **Cancels look slow** → `orderDelay` applies to cancels too.

## See also

- `backtest-plugin-guide.md` — the high-level wrapper most users want.
- `../plugins/matchingEngineSimulator/matching_engine_simulator.md` — full
  upstream reference (61 KB).
- `../tutorials/backtesting_using_MatchingEngineSimulator.md` — worked case
  study.
- `../tutorials/matching_engine_simulator.md` — extended tutorial.
- `../plugins/simulatedexchangeengine.md` — a fuller exchange simulator
  (order types, matching rules beyond continuous auction).
