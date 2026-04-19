# Stream computing engines — decision guide

DolphinDB ships many purpose-built streaming engines. Pick the one whose
**semantics match your problem**; do not try to compose everything with raw
subscriptions.

## Decision table

| Problem | Engine | Key function |
|---------|--------|--------------|
| Rolling aggregates on fixed time buckets per key (OHLC / VWAP) | **Time-series engine** | `createTimeSeriesEngine` |
| Variable-length buckets (e.g. daily / session) | **Daily time-series / Time-bucket** | `createDailyTimeSeriesEngine`, `createTimeBucketEngine` |
| Stateful per-row transformations (factor calc with state) | **Reactive state** | `createReactiveStateEngine` |
| Stateless per-row transformations (Python-style map) | **Reactive stateless** | `createReactiveStateEngine` with stateless metrics, or `createStreamDispatchEngine` |
| Emit narrow (long-format) output | **Narrow reactive state** | `createNarrowReactiveStateEngine` |
| Two different partitionings in parallel (cascaded reactive) | **Dual ownership reactive state** | `createDualOwnershipReactiveStateEngine` |
| Only compute when certain data arrives | **Sparse reactive state** | `createSparseReactiveStateEngine` |
| Snapshot at fixed clock instants across all symbols | **Cross-sectional engine** | `createCrossSectionalEngine` |
| Join trade stream to latest quote stream (asof) | **Asof join engine** | `createAsofJoinEngine` |
| Join streams where keys must be ≤ some tolerance | **Nearest join engine** | `createNearestJoinEngine` |
| Equi join between two streams | **Equi join engine** / **Equal join engine** | `createEquiJoinEngine` |
| Left-semi stream join (enrich from slow-changing table) | **Left-semi / Lookup** | `createLeftSemiJoinEngine`, `createLookupJoinEngine` |
| Merge left + right on a windowed basis | **Window join** | `createWindowJoinEngine` |
| Join two persistent streams by timestamp | **Snapshot join** | `createSnapshotJoinEngine` |
| Group rows by session (gap-based) | **Session window** | `createSessionWindowEngine` |
| Detect anomalies by rule | **Anomaly detection** | `createAnomalyDetectionEngine` |
| Trigger actions on arbitrary predicates | **Rule engine** | `createRuleEngine` |
| Order-book snapshot from tick-by-tick updates | **Order-book snapshot** | `createOrderBookSnapshotEngine` |
| Crypto order-book (partial-update model) | **Crypto order-book** | `createCryptoOrderBookEngine` |
| Route / balance data across sinks | **Stream dispatch** | `createStreamDispatchEngine` |
| Nested factor (reactive + timeseries + cross) composed automatically | **Stream engine parser** | `streamEngineParser` |

## Typical cascade

```
ticks  → subscribeTable → timeSeriesEngine (OHLC 1min)
                       ↘
                        reactiveStateEngine (rolling factor)
                       ↘
                        crossSectionalEngine (cross-sectional z-score)
                       ↘ outputTable → DFS append
```

Use `streamEngineParser` to describe the whole cascade as a single formula
and let the parser build the pipeline.

## Engine is a table

Every engine returns a **table handle**. Appending rows to the handle is
equivalent to feeding the engine. So typical wiring is:

```dolphindb
engine = createTimeSeriesEngine(...)
subscribeTable(..., handler=append!{engine}, msgAsTable=true)
```

## Inspect & tear down

```dolphindb
getStreamEngineStat()       // status of every engine
getAggregatorStat()         // time-series engines
dropStreamEngine(`ohlc)
```

## Traps

- **Forgetting `dummyTable`** — the engine needs a schema template; pass
  the publishing table as `dummyTable=ticks`.
- **`useSystemTime=true` vs `useSystemTime=false`**: true triggers on wall
  clock (missing data still closes windows); false triggers on event time
  from the data.
- **Memory** — reactive state engines keep state per key. Cap with
  `keyPurgeFreqInSec` / `keyPurgeFreqInBatch`.
- **Ordering** — stream engines expect per-key time-ordered input. Use
  `asofJoinEngine` or `reactiveStateEngine` with care on late data.

## See also

- `*_engine.md`, `str_eng_parser.md`.
- `../../reference/functions/by-theme/流数据.md` — full function index.
