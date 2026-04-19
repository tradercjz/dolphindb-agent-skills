# Built-in modules

Modules bundled with DolphinDB. Install (once) and use from script with:

```dolphindb
installModule("<name>")      // from module marketplace
use <name>                    // per session, enables unqualified calls
// or
use <name> as m; m::someFunc(...)
```

## Catalog

| Module | File | Purpose |
|--------|------|---------|
| `ta`         | `ta/ta.md`                   | TA-Lib–style technical indicators (MACD, RSI, KDJ, Bollinger, …). |
| `wq101alpha` | `wq101alpha/wq101alpha.md`   | WorldQuant 101 alpha factors, ported to DolphinDB. |
| `gtja191Alpha` | `gtja191Alpha/191alpha.md` | 国泰君安 191 alpha factor library. |
| `mytt`       | `mytt/mytt.md`               | MyTT-style indicators (minimalist technical-analysis set). |
| `ops`        | `ops/ops.md`                 | Operational helpers / cluster automation. |
| `MarketHoliday` | `MarketHoliday/mkt_calendar.md`, `MarketHoliday/release.md` | Exchange trading calendars & holidays. |
| `easyNSQ`    | `easyNSQ/easynsq.md`, `easyNSQ/easynsq_2.md` | Convenience wrapper for NSQ L2 feed. |
| `easyTLDataImport` | `easyTLDataImport/easytl_data_import.md` | TongLian (通联) tick data loader. |

## Typical usage

```dolphindb
// Technical indicators
use ta
close = 100.0 + cumsum(rand(1.0, 100) - 0.5)
rsi14 = ta::rsi(close, 14)

// WorldQuant 101 factors
use wq101alpha
// compute alpha#1 on a DFS tick table
f1 = wq101alpha::alpha1(close, returns)

// Market calendar
use MarketHoliday
MarketHoliday::getTradingDays(2024.01.01, 2024.12.31, "CN")
```

## See also

- Tutorial index: `../tutorials/README.md` → "Factor calculation" section
  for WQ101 / GTJA alpha workflows.
- Language reference: `../10-language/modules.md`.
- Plugin catalog (different thing — plugins are compiled shared libs;
  modules are pure DolphinDB script).
