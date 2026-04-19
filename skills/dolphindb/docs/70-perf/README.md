# 70-perf — performance & tuning

## Hand-authored

- `query-optimization.md`   — how to read EXPLAIN, common rewrites.
- `partition-pruning.md`    ★ the single most impactful query rule.
- `memory-threading.md`     — parallelism config, memory limits, monitoring.
- `slow-query-diagnosis.md` ★ 10-step checklist from `explain` → sort cols → `getPerfMon` → skew → client.
- `jit-guide.md`            — `@jit` compilation: when it helps, supported types/ops, silent-fallback traps, `@state`+`@jit` combo.

## Related

- `docs/30-database/partitioning.md`, `docs/30-database/tsdb-engine.md`.
- `hint.md`, `hint_explain.md` (under `20-sql/`).
