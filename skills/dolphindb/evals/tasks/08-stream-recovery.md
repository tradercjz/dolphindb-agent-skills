# 08 — Stream pipeline duplicates data after restart

**Tags:** streaming, ops
**Difficulty:** hard
**Reference doc:** `patterns/stream-recovery-after-restart.md`,
`docs/40-streaming/stream-table.md`, `subscribe.md`

## Prompt

My streaming pipeline reads a shared stream table `ticks` and appends
each batch to `dfs://tick.trade`. On server restart, the subscriber
replays every row from the start of the stream — I end up with duplicate
rows in DFS. How do I fix?

## Rubric

- [ ] Enables persistent stream table via
      `enableTableShareAndPersistence(...)` on `ticks` with a reasonable
      `cacheSize` / `retentionMinutes`.
- [ ] Sets `persistOffset = true` on `subscribeTable` so the subscriber
      resumes from its last consumed offset on restart.
- [ ] Adds `reconnect = true` for remote subscriber resiliency.
- [ ] Makes the DFS target **idempotent**: TSDB with
      `sortColumns = \`sym\`ts` + `keepDuplicates = LAST`, OR delete-then-
      append per batch.
- [ ] Wraps handler in try/catch → dead-letter table to avoid poison-pill.
- [ ] Mentions testing with a kill -9 to verify no duplicates.

## Expected artifact (minimum)

```dolphindb
enableTableShareAndPersistence(
    table = streamTable(1_000_000:0, `ts`sym`px`vol,
                        [TIMESTAMP, SYMBOL, DOUBLE, INT]),
    tableName = `ticks,
    asynWrite = true, compress = true,
    cacheSize = 1_000_000, retentionMinutes = 1440)

// TSDB target with keepDuplicates=LAST -> idempotent append
// ... (create table with sortColumns=`sym`ts, keepDuplicates=LAST)

def safeAppend(msg) {
    try { loadTable("dfs://tick", `trade).append!(msg) }
    catch (ex) { deadLetter.append!(select msg.*, now() as errTs, ex as errMsg) }
}
subscribeTable(
    tableName=`ticks, actionName=`toDfs, handler=safeAppend,
    msgAsTable=true, batchSize=10000, throttle=1,
    persistOffset=true, reconnect=true)
```

## Anti-patterns

- "Just run `delete from trade where date = today()` before restart" —
  loses legit data.
- Enabling `persistOffset` without making the publisher stream
  persistent (offsets make no sense then).
- Using PKEY engine for raw ticks (write-amp; TSDB + `keepDuplicates=LAST`
  is the right tool).
- Ignoring dead-letter → one bad row halts the pipeline.
