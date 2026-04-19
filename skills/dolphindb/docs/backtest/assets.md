# Asset types — what differs

## Contents
- Stock (cash equity + T+1 settlement)
- Margin-trading (融资融券)
- Future (multiplier, margin, daily settlement)
- Option (contract master, exercise)
- Bond (coupon, accrued interest)
- Digital currency
- Multi-asset (mixing the above)

The Backtest plugin supports 7 `strategyGroup` modes. Each changes the
expected schema of market data, the set of supported `direction` codes,
and a handful of config keys. Core strategy logic stays the same.

Set the asset mode with `config.strategyGroup`:

| Mode | `strategyGroup` value | Typical `dataType` |
|------|----------------------|--------------------|
| Stock (cash)                | `` `stock ``                | 1=snapshot, 2=tick, 3=minBar, 4=dayBar |
| Stock margin trading (融资融券) | `` `securityCreditAccount `` | same as stock |
| Future                      | `` `future ``               | 1=snapshot, 3=minBar, 4=dayBar |
| Option                      | `` `option ``               | 1=snapshot, 3=minBar |
| Interbank bond              | `` `bond ``                 | dataType varies; see bond page |
| Digital currency            | `` `digitalCurrency ``      | snapshot / tick |
| Multi-asset                 | `` `multiAsset ``           | per-asset dicts |

## Stock (cash)

```dolphindb
config = {
    strategyGroup: `stock,
    cash:          1000000.0,
    commission:    0.00015,     // rate on notional
    tax:           0.001,        // stamp duty (sell side in CN)
    dataType:      3,
    slippage:      0.0
}
```

- `direction`: 1 = buy, 2 = sell.
- Supports snapshot / tick / bar data.
- `dayBar` mode is the fastest; use for daily-frequency portfolio
  strategies.

Reference: `../plugins/backtest/stock.md` (49 KB).
Tutorials: `../tutorials/stock_backtest.md`,
`../tutorials/daily_stock_portfolio_backtest.md`.

## Stock margin trading (融资融券)

```dolphindb
config = {
    strategyGroup: `securityCreditAccount,
    cash:          1000000.0,
    commission:    0.00015,
    tax:           0.001,
    lineOfCredit:              2000000.0,
    marginTradingInterestRate: 0.0588,    // 融资年利率
    secuLendingInterestRate:   0.1005,    // 融券年利率
    longConcentration:         0.3,       // 单标的多头集中度
    shortConcentration:        0.2
}
```

- `direction` codes extend to include financing open/close and securities-
  lending open/close.
- Daily interest / fee accrual done by the engine.
- Risk controls honored: concentration limits, credit line.

Reference: `../tutorials/backtest_introduction_usage.md` (dedicated 融资融券
walkthrough, 41 KB).

## Future

```dolphindb
config = {
    strategyGroup: `future,
    cash:          1000000.0,
    marginRatio:   0.12,                  // 保证金比例
    openFeeRate:   0.00023,
    closeFeeRate:  0.00023,
    slippage:      0.2,                   // price slippage per contract
    contractMultiplier: 10,               // CU 5t/lot, IC 200/point, etc.
    dataType:      3
}
```

- `direction`: 1 buyOpen, 2 sellClose, 3 sellOpen, 4 buyClose. Distinct
  open/close is required to track long vs short position.
- Contract multiplier is mandatory for correct P&L.
- No stamp tax.

Reference: `../plugins/backtest/futures.md`.
Tutorials: `../tutorials/cta_strategy_implementation_and_backtesting.md`,
`../tutorials/futures_minute_frequency_cta_strategy_backtest_example.md`.

## Option

```dolphindb
config = {
    strategyGroup:     `option,
    cash:              1000000.0,
    marginRatio:       0.12,
    openFeeRate:       5.0,      // per contract (abs), not rate
    closeFeeRate:      5.0,
    contractMultiplier: 10000,
    dataType:          1
}
```

- Direction codes mirror futures.
- Option margin logic honored (for short positions, SSE/SZSE formulas).
- Greeks are NOT computed by the engine — compute them in your strategy
  and feed as indicators.

Reference: `../plugins/backtest/option.md`.
Tutorial: `../tutorials/backtest_volatility_timing_vertical_spread.md`.

## Interbank bond

```dolphindb
config = {
    strategyGroup: `bond,
    cash:          100000000.0,
    dataType:      ...           // see bond page
}
```

- Models yield / full-price conversions at trade time.
- Different commission / spread conventions than stocks.

Reference: `../plugins/backtest/interbank_bonds.md`.

## Digital currency (crypto)

```dolphindb
config = {
    strategyGroup: `digitalCurrency,
    cash:          100000.0,
    commission:    0.0008,
    dataType:      1                 // usually snapshot / L2
}
```

- Fractional lot sizes (no integer-shares constraint).
- Separate base / quote balances modeled.
- Funding rate and perpetual-swap semantics: confirm in manual.

Reference: `../plugins/backtest/digital_currency.md`.

## Multi-asset

When one strategy trades **multiple asset classes** in one engine:

```dolphindb
config = {
    strategyGroup: `multiAsset,
    cash:          1000000.0,
    assets: {                        // asset-specific sub-configs
        stock:   { commission: 0.00015, tax: 0.001 },
        future:  { marginRatio: 0.12, contractMultiplier: 10 },
        option:  { ... }
    },
    dataType:      1
}
```

- `msg` delivered to callbacks is a dict keyed by symbol; the engine
  infers asset type per symbol from a lookup table you register.
- Direction codes resolve per asset.

Reference: `../plugins/backtest/multi_asset.md`.
Tutorial: `../tutorials/multi_asset_backtest.md`.

## See also

- `backtest-plugin-guide.md` for the shared lifecycle.
- `traps.md` for cross-asset pitfalls.
