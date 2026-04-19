# patterns/ — "how do I do X" recipes

One file per recurring task. Each file should follow the template:

1. **Problem** — 1 sentence.
2. **When to use / not use** — pick-list.
3. **Solution** — minimal code.
4. **Variants / gotchas**.
5. **See also** — links to `docs/` and `reference/`.

## Current recipes

| File | Topic |
|------|-------|
| `asof-join-quotes-trades.md`      | Attach prevailing quote to every trade. |
| `backtest-signal-to-order.md`     | Signal → target position → order delta, with variants (long-only top-quintile, cross-over). |
| `partition-design.md`             | Choose VALUE / RANGE / HASH / COMPO layout. |
| `python-roundtrip-type-safety.md` | DataFrame ↔ DolphinDB without losing DECIMAL / SYMBOL / nano-ts. |
| `scheduled-job-template.md`       | Idempotent nightly jobs, audit table, `scheduleJob`. |
| `stream-ingestion-to-dfs.md`      | Kafka/MQTT/REST → stream table → DFS pipeline. |
| `stream-recovery-after-restart.md`| Exactly-once-ish subscription: `persistOffset`, dead-letter, `keepDuplicates=LAST`. |
| `tick-to-ohlc.md`                 | 1-min OHLC from tick stream (vectorized + streaming). |
| `upsert-via-pkey.md`              | PKEY engine upsert semantics. |
