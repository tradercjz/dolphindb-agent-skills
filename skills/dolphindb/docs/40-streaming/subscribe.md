# `subscribeTable` — consuming a stream

## Contents
- Handler shape & `msgAsTable`
- Batching (`batchSize`, `throttle`)
- Persistence (`persistOffset`) & reconnect
- Multi-consumer routing (`hash`)
- Unsubscribe, diagnostics
- Common traps

`subscribeTable` attaches a handler to a stream table. Every insert triggers
the handler.

## Minimal

```dolphindb
def onTick(msg) {
    // msg is a table when msgAsTable=true
    print(size(msg))
}

subscribeTable(
    tableName   = `ticks,
    actionName  = `demo,
    handler     = onTick,
    msgAsTable  = true
)
```

`(tableName, actionName)` is the unique subscription ID — you can attach
multiple actions to one table by using different action names.

## Full parameter set

```dolphindb
subscribeTable(
    server          = NULL,          // leave NULL for local; set node alias for remote
    tableName       = `ticks,
    actionName      = `demo,
    offset          = -1,            // -1 = start from next; 0 = from beginning; N = from row N
    handler         = onTick,        // function OR a table (auto-append)
    msgAsTable      = true,          // batch as table (true) vs tuple-of-vectors (false)
    batchSize       = 1000,          // trigger every N rows
    throttle        = 0.1,           // OR every 0.1s (whichever first)
    hash            = -1,            // which handler thread (use different values to parallelize)
    filter          = NULL,          // values of the filter column to receive
    persistOffset   = true,          // survive restart
    timeTrigger     = false,         // fire by wall-clock throttle even if no data
    handlerNeedMsgId = false,
    reconnect       = true           // auto-reconnect to remote publisher
)
```

## Key patterns

### A. Log / aggregate to another table

```dolphindb
agg = table(1000000:0, `sym`minute`avgPx, [SYMBOL, TIMESTAMP, DOUBLE])

def onTick(msg, agg) {
    r = select sym, bar(ts, 60s) as minute, avg(px) as avgPx
        from msg
        group by sym, bar(ts, 60s)
    agg.append!(r)
}

subscribeTable(tableName=`ticks, actionName=`minAgg,
               handler=onTick{, agg},     // partial application
               msgAsTable=true, batchSize=5000, throttle=1)
```

`handler{, agg}` is **partial application** — binds the second argument to
`agg`, yielding a function of one argument (`msg`).

### B. Feed directly into a compute engine

```dolphindb
engine = createTimeSeriesEngine(
    name="ohlc", windowSize=60000, step=60000,
    metrics=<[first(px), max(px), min(px), last(px), sum(vol)]>,
    dummyTable=ticks, outputTable=bars,
    timeColumn=`ts, keyColumn=`sym, useSystemTime=false
)

subscribeTable(tableName=`ticks, actionName=`toEngine,
               handler=append!{engine}, msgAsTable=true)
```

### C. Parallel subscribers (hash)

Use the `hash` param to pin each subscription to a different handler thread:

```dolphindb
for (i in 0..3) {
    subscribeTable(tableName=`ticks, actionName="w" + string(i),
                   handler=onTick, msgAsTable=true, hash=i)
}
```

Four handlers run in parallel on independent event loops. Only useful if
handlers are CPU-bound.

### D. Remote subscription (cross-node)

```dolphindb
subscribeTable(
    server     = "publisherNode",
    tableName  = `ticks,
    actionName = `remoteDemo,
    handler    = onTick,
    msgAsTable = true,
    reconnect  = true
)
```

The server must publish via `publish=enabled` + `maxPubConnections>0`
(see error `S00001`).

## Traps

- **`subscribe` before `share`** → `S00001` / "table not shared".
- **Handler throws** → subscription auto-stops; check `getStreamingStat()`.
- **`msgAsTable=false`** means `msg` is a tuple of vectors, not a table.
  SQL-style `select ... from msg` won't work; use `msg[0]`, `msg[1]` etc.
  Prefer `msgAsTable=true` unless you need the raw form.
- **`batchSize` + `throttle`**: handler fires when *either* threshold is
  reached. Set both; don't rely on `batchSize` alone for low-rate streams.
- **`persistOffset=true` requires the publisher table to be persistent**.
- **Dropping the publisher without unsubscribing** leaks topic metadata.
  Always `unsubscribeTable`.

## Inspect & stop

```dolphindb
getStreamingStat().subWorkers
getStreamingStat().pubConns
unsubscribeTable(tableName=`ticks, actionName=`demo)
```

## See also

- `stream-table.md`, `engines.md`, `replay.md`.
- `sub_pub.md`, `local_sub.md`, `str_api_python.md`
  (Python-side subscription).
