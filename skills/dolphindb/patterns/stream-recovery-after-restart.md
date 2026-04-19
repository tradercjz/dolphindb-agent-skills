# Pattern — streaming pipelines that recover after restart

## Problem

DolphinDB streaming pipelines can lose in-flight messages or replay
duplicates when a publisher/subscriber restarts. You want **exactly-once
end-to-end** or at least **at-least-once + idempotent**.

## When to use

| Use | Don't use |
|-----|-----------|
| Production stream → DFS pipelines | Prototype: in-memory stream tables are fine. |
| Subscriber must catch up after downtime | You can afford to replay from the source → re-ingest from CSV / Kafka. |
| Multiple subscribers per topic | One-shot batch. |

## Three failure modes

| Mode | What breaks | Mitigation |
|------|-------------|------------|
| **Publisher restart** | In-memory stream table loses rows since last persistence flush | Enable disk persistence + fsync |
| **Subscriber restart** | Subscriber forgets last-consumed offset → replays all | `persistOffset=true` + idempotent handler |
| **Network partition** | Subscription breaks, reconnects stale | `reconnect=true` + resume handle |

## Solution

### 1. Persistent publisher-side stream table

```dolphindb
// In the controller startup script or initial setup:
enableTableShareAndPersistence(
    table         = streamTable(1_000_000:0, `ts`sym`px`vol,
                                [TIMESTAMP, SYMBOL, DOUBLE, INT]),
    tableName     = `ticks,
    asynWrite     = true,                       // background persist
    compress      = true,
    cacheSize     = 1_000_000,                  // rows kept in memory
    retentionMinutes = 1440,                    // 1 day on disk
    flushMode     = 1,                          // 1 = fsync after every batch
    preCache      = 10000
)
```

Data path on disk: `<persistenceDir>/ticks/`. On restart, the table
reloads the last `retentionMinutes` of data from disk, and subscribers
can resume from their persisted offset.

`flushMode=1` trades some throughput for durability. Use `0` (default,
no fsync) if the upstream source can replay.

### 2. Idempotent + offset-checkpointed subscriber

```dolphindb
// Target DFS (TSDB, unique by (sym, ts) via sortColumns+keepDuplicates=LAST)
def ensureDfs() {
    if (existsTable("dfs://tick", `trade)) return
    db = database("dfs://tick", VALUE, 2024.01.01..2030.12.31,
                  engine="TSDB")
    db.createPartitionedTable(
        table(1:0, `ts`sym`px`vol, [TIMESTAMP, SYMBOL, DOUBLE, INT]),
        `trade, `ts,
        sortColumns    = `sym`ts,
        keepDuplicates = LAST                   // upsert-like on exact (sym, ts)
    )
}
ensureDfs()

def safeAppend(mutable deadLetter, msg) {
    try {
        loadTable("dfs://tick", `trade).append!(msg)
    } catch (ex) {
        deadLetter.append!(select msg.*, now() as errTs, ex as errMsg)
    }
}

// Separate stream table to collect failures
if (not defined(`deadLetter)) {
    enableTableShareAndPersistence(
        table = streamTable(10000:0, `ts`sym`px`vol`errTs`errMsg,
                            [TIMESTAMP, SYMBOL, DOUBLE, INT, TIMESTAMP, STRING]),
        tableName = `deadLetter)
}

subscribeTable(
    tableName     = `ticks,
    actionName    = `toDfs,
    handler       = safeAppend{deadLetter},
    msgAsTable    = true,
    batchSize     = 10000,
    throttle      = 1,
    persistOffset = true,                       // resume from disk on restart
    reconnect     = true,                       // auto-retry on disconnect
    handlerNeedMsgId = false
)
```

Key ingredients:
- **`persistOffset=true`** writes `<persistenceDir>/subOffset/<topic>_<action>`
  after each batch. On restart, `subscribeTable` resumes from there.
- **`reconnect=true`** makes the subscriber auto-reconnect to remote
  publishers (useful across nodes).
- **`keepDuplicates=LAST`** on the DFS target makes re-delivered rows
  idempotent (last write wins on exact `(sym, ts)` duplicates).
- **Dead-letter table** ensures one bad row doesn't poison-pill the
  stream.

### 3. Track subscription health

```dolphindb
def streamHealth() {
    s = getStreamingStat()
    return dict(`pub`sub`persist, [s.pubTables, s.subWorkers, s.persistenceMeta])
}
streamHealth()

// Inspect a specific subscription's lag
select * from getStreamingStat().subWorkers
where topic like "%ticks%"
```

Watch `msgAsTableCount` vs `msgAsTableConsumedCount` — gap means a
subscriber is falling behind.

### 4. Orderly shutdown

```dolphindb
def gracefulShutdown() {
    // stop subscribers first so publisher stops accumulating
    unsubscribeTable(tableName=`ticks, actionName=`toDfs)
    // let async persistence flush
    sleep(2000)
    // optionally drop in-memory share
    // undef(`ticks, SHARED)
}
```

Call this in a `shutdown` hook or via a controlled job so the offset
state is consistent on disk.

### 5. Recovery test checklist

Before relying on it in production, test:

- [ ] Kill `-9` the server mid-batch → restart → verify no duplicates
      in DFS (run `select count(*), count(distinct (sym, ts))` on today's
      partition; they should match).
- [ ] Disconnect subscriber network for 60s → verify `reconnect` catches
      up without data loss.
- [ ] Poison a message (bad schema) → verify it goes to dead-letter and
      doesn't block normal flow.
- [ ] Restart publisher → verify subscribers resume from their offsets
      (they should not replay everything from 0).

## Variants

### Exactly-once with a 2-phase commit table

For financial-grade guarantees:

```dolphindb
// A sequence table the publisher writes to atomically:
share streamTable(1:0, `seqNo`payload, [LONG, BLOB]) as seqStream

// Subscriber tracks last applied seqNo in a KV state table:
share dict(STRING, LONG) as lastSeq
lastSeq["tickPipeline"] = 0

def applyExactlyOnce(mutable state, msg) {
    for (i in 0..(size(msg)-1)) {
        if (msg.seqNo[i] <= state["tickPipeline"]) continue
        applyOne(decode(msg.payload[i]))
        state["tickPipeline"] = msg.seqNo[i]
    }
}
```

Trade-off: extra latency and storage for the seq column.

### At-most-once (sampling)

`persistOffset=false, reconnect=false` — on any failure you skip the
backlog entirely. Useful for live monitoring dashboards where fresh > complete.

## Traps

- **`persistOffset=true` requires the publisher stream to also be
  persistent.** Otherwise the offset is nonsensical after publisher
  restart.
- **`throttle` vs latency.** `throttle=1` waits up to 1 s; fine for DFS
  append, bad for alerting. For low-latency, use `throttle=0.01, batchSize=1`.
- **DFS append is not atomic across partitions.** A batch spanning two
  days can half-succeed. Split batches by date before `append!` for
  strict idempotency.
- **`unsubscribeTable` is async.** Don't assume the handler has stopped
  right after the call; sleep or poll `getStreamingStat`.
- **Reactive-state engine state is NOT persistent.** On restart, per-key
  state is lost; factors need warm-up data. Pre-replay recent history
  from DFS into the stream on startup.

## See also

- `../docs/40-streaming/stream-table.md`, `subscribe.md`,
  `engines.md`.
- `../docs/tutorials/haStreaming.md` for HA streaming with raft.
- `../docs/tutorials/streaming_auto_sub.md`, `streaming_auto_sub_2.md`.
- `stream-ingestion-to-dfs.md` for the basic pipeline.
