# Backtest tutorials — curated index

Full, runnable case studies live under `../tutorials/`. These are
auto-mirrored from upstream and tend to be 30–150 KB each (complete with
data loading, signal code, result analysis). Below: which one to read for
which scenario.

## Getting started

| Topic | File |
|-------|------|
| End-to-end intro, margin-trading focus | `../tutorials/backtest_introduction_usage.md` |
| Quick start via the plugin | `../plugins/backtest/quick_start.md` |
| Using MatchingEngineSimulator standalone | `../tutorials/backtesting_using_MatchingEngineSimulator.md`, `../tutorials/matching_engine_simulator.md` |

## By asset class

| Asset | File |
|-------|------|
| Stock — single name, intraday | `../tutorials/stock_backtest.md` |
| Stock — daily portfolio | `../tutorials/daily_stock_portfolio_backtest.md` |
| Futures — minute-frequency CTA | `../tutorials/futures_minute_frequency_cta_strategy_backtest_example.md` |
| Futures — full CTA implementation | `../tutorials/cta_strategy_implementation_and_backtesting.md` |
| Options — volatility timing, vertical spread | `../tutorials/backtest_volatility_timing_vertical_spread.md` |
| Multi-asset portfolio | `../tutorials/multi_asset_backtest.md` |

## Factor-driven strategies

| Topic | File |
|-------|------|
| Factor calculation best practices | `../tutorials/best_practice_for_factor_calculation.md` |
| Multi-factor workflow | `../tutorials/best_practices_for_multi_factor.md` |
| Factor evaluation framework | `../tutorials/factor_evaluation_framework.md` |
| Factor attribution analysis | `../tutorials/factor_attribution_analysis.md` |
| Practical factor analysis modeling | `../tutorials/Practical_Factor_Analysis_Modeling.md` |
| Multi-factor risk model | `../tutorials/multi_factor_risk_model.md` |
| Fund factor (Python-compared) | `../tutorials/fund_factor_contrasted_by_py.md` |
| High-frequency → low-frequency factor | `../tutorials/hf_to_lf_factor.md` |
| Streaming high-frequency factors | `../tutorials/hf_factor_streaming.md`, `../tutorials/hf_factor_streaming_2.md` |
| L2 snapshot factor compute | `../tutorials/l2_snapshot_factor_calc.md` |

## Execution / order handling

| Topic | File |
|-------|------|
| Order splitting via CEP | `../tutorials/order_splitting_with_cep.md` |
| Order splitting advanced | `../tutorials/order_splitting_with_cep_advanced.md` |
| Order-book snapshot engine application | `../tutorials/insight_plugin_orderbook_engine_application.md` |
| Matching engine simulator deep dive | `../tutorials/matching_engine_simulator.md` |

## Quant finance misc

| Topic | File |
|-------|------|
| Quant finance examples overview | `../tutorials/quant_finance_examples.md` |
| Streaming capital flow order-by-order | `../tutorials/streaming_capital_flow_order_by_order.md` |

## Tips

- All upstream tutorials are in **Chinese**. If an English version is
  required, run the script through a translator before feeding the agent.
- Each tutorial assumes a specific DolphinDB version; check the header.
- Code blocks are directly runnable against the DolphinDB Web notebook
  after loading the referenced sample data.

## See also

- `backtest-plugin-guide.md`, `traps.md`, `assets.md`.
- `../patterns/` — short how-to recipes.
- `../examples/` — minimal runnable scripts maintained by this skill.
