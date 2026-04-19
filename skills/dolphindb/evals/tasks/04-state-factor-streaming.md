# 04 — `@state` factor for reactive engine

**Tags:** streaming, factor
**Difficulty:** medium
**Reference doc:** `docs/backtest/factors.md`, `docs/40-streaming/engine-selection.md`

## Prompt

I want to compute a 20-tick momentum factor `(close / close[t-20]) - 1`
online, per symbol, on a stream of ticks. Here's my factor function:

```dolphindb
def momentum20(close) {
    return close / prev(close, 20) - 1
}
```

I plug it into a reactive state engine and the output is all null /
wrong per symbol. What's missing?

## Rubric

- [ ] Adds `@state` decorator to `momentum20`.
- [ ] Correctly uses `createReactiveStateEngine` with
      `metrics = <[momentum20(close) as mom]>`, `keyColumn = \`sym`.
- [ ] Explains that without `@state`, per-key state is not maintained
      across ticks → every call sees only the current row, so `prev(...)`
      returns null.
- [ ] (Bonus) Mentions that `@jit` can be added on top for HF feeds.

## Expected artifact (minimum)

```dolphindb
@state
def momentum20(close) {
    return close / prev(close, 20) - 1
}

engine = createReactiveStateEngine(
    name        = "mom",
    metrics     = <[momentum20(close) as mom]>,
    dummyTable  = ticks,
    outputTable = factorStream,
    keyColumn   = `sym)

subscribeTable(tableName=`ticks, actionName=`toEng,
               handler=append!{engine}, msgAsTable=true)
```

## Anti-patterns

- Computing the factor in SQL inside the handler (`select ... context by`) —
  works but doesn't scale per-tick.
- Using `createTimeSeriesEngine` — wrong shape; this is per-row, not
  per-window.
- Dropping `keyColumn` — factor gets mixed across symbols.
