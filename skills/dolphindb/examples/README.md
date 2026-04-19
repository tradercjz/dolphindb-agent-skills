# examples/ — runnable end-to-end scripts

Complete, copy-pastable scripts. Each file should run top-to-bottom against
a local DolphinDB server (unless noted). Keep comments terse — the agent
reads these as-is.

Naming: `<topic>-<specific-case>.dos` for DolphinDB scripts, `.py` / `.java`
/ `.cpp` for client-side.

## Current scripts

| File | Demonstrates |
|------|-------------|
| `backtest-quickstart.dos`   | Backtest plugin end-to-end (stock). |
| `backtest-future.dos`       | Futures CTA (double-MA cross, margin, settlement). |
| `backtest-option.dos`       | ETF-option vertical spread + JIT Black-Scholes IV/Greeks. |
| `create-dfs-and-load.dos`   | DFS database creation + CSV load. |
| `parquet-roundtrip.dos`     | Parquet → TSDB DFS → Parquet with DECIMAL/SYMBOL preservation. |
| `stream-reactive-engine.dos`| Per-symbol factor in `createReactiveStateEngine`. |
| `tick-to-ohlc.dos`          | 1-min OHLC aggregation from ticks. |
| `python-api-quickstart.py`  | Python client: connect, `runArrow`, `tableAppender`. |
