# 40-streaming — stream tables, subscriptions, engines, CEP

## Hand-authored

- `stream-table.md`  — stream table lifecycle (`share`, persistence, filter).
- `subscribe.md`     ★ `subscribeTable` handler / batching / persistence.
- `engines.md`          — reference on every engine's constructor args.
- `engine-selection.md` ★ **decision tree** for picking among the 8 stream engines + CEP.
- `cep-overview.md`  — complex event processing engine intro (hand-authored guide; upstream `cep.md` is the full reference).
- `replay.md`        — historical replay for backfill / testing.

## Full upstream reference pages

| Topic | File |
|-------|------|
| Intro | `str_intro.md`, `str_funcs.md` |
| Stream tables | `str_table.md` |
| Pub/sub | `sub_pub.md`, `local_sub.md`, `cluster_sub.md` |
| HA streaming | `str_ha.md` |
| Monitoring | `str_monitor.md` |
| Reactive state | `reactive_state_engine.md`, `reactive_stateless_engine.md`, `narrow_reactive_state_engine.md`, `dual_ownership_engine.md` |
| Time series | `time_series_engine.md`, `time_bucket_engine.md` |
| Cross sectional | `cross_sectional_engine.md` |
| Asof join | `asof_join_engine.md`, `nearest_join_engine.md` |
| Equi / lookup / lsj / snapshot / window join | `equi_join_engine.md`, `lookup_join_engine.md`, `leftsemi_join_engine.md`, `snapshot_join_engine.md`, `window_join_engine.md` |
| Session window | `session_window_engine.md` |
| Anomaly | `anomaly_detection_engine.md` |
| Rule engine | `rule_engine.md` |
| Parser | `str_eng_parser.md` |
| CEP reference | `cep.md`, `cep_engine.md`, `cep_basic_concept.md`, `cep_events_defining.md`, `cep_monitor_defining.md`, `cep_monitoring.md`, `cep_viewing.md`, `cep_application.md` |
| Replay | `str_replay.md`, `str_replay_1.md`, `str_replay_n21.md`, `str_replay_n2n.md` |
| Python streaming | `str_api_python.md`, `py_sub.md` |
| Streaming SQL | `streaming_sql.md` |
| Orca real-time platform | `orca.md` |
