# Pattern — real-time stream → DFS persistence

## Problem

Receive a continuous stream of rows (ticks, IoT metrics, log events) from
Kafka / MQTT / a socket / a broker API. Land every row durably into a
partitioned DFS table while keeping a recent window queryable in memory.

## When to use

| Use | Don't use |
|-----|-----------|
| Rate > 10k rows/s per source and growth unbounded | Small, bounded loads → just `loadText` the file. |
| Need both live dashboards/queries AND historical analytics | Need only live queries → a persistent stream table is enough. |
| Multiple subscribers / pipelines downstream | One-shot ETL → a scheduled `loadText` + `append!` is fine. |

## Architecture

```
[external feed] ─► plugin connector ──► share streamTable (ticks)
                                           │
                                           ├── subscribeTable → DFS append
                                           ├── subscribeTable → reactiveStateEngine → factorStream
                                           └── subscribeTable → other consumers
```

The central **shared persistent stream table** is the hub; every consumer
attaches via `subscribeTable` with its own `actionName`.

## Solution

### 1. Create the durable stream table

```dolphindb
enableTableShareAndPersistence(
    table     = streamTable(1_000_000:0, `ts`sym`px`vol,
                            [TIMESTAMP, SYMBOL, DOUBLE, INT]),
    tableName = `ticks,
    asynWrite = true,
    compress  = true,
    cacheSize = 1_000_000,           // rows held in memory
    retentionMinutes = 1440          // 1 day retention on disk
)
```

### 2. Create the DFS target once

```dolphindb
if (not existsDatabase("dfs://tick")) {
    dbDate = database("", VALUE, 2024.01.01..2030.12.31)
    dbSym  = database("", HASH,  [SYMBOL, 20])
    db     = database("dfs://tick", COMPO, [dbDate, dbSym], engine="TSDB")
    db.createPartitionedTable(
        table            = table(1:0, `ts`sym`px`vol,
                                 [TIMESTAMP, SYMBOL, DOUBLE, INT]),
        tableName        = `trade,
        partitionColumns = `ts`sym,
        sortColumns      = `sym`ts
    )
}
```

### 3. Subscribe the stream to DFS append

```dolphindb
def persistToDfs(msg) {
    loadTable("dfs://tick", `trade).append!(msg)
}

subscribeTable(
    tableName    = `ticks,
    actionName   = `toDfs,
    handler      = persistToDfs,
    msgAsTable   = true,
    batchSize    = 10000,
    throttle     = 1,                // 1-second ceiling
    persistOffset = true,            // survive restart
    reconnect    = true
)
```

`batchSize=10000, throttle=1` is a good default: write every 10k rows or
every 1 s, whichever first. Adjust per throughput.

### 4. Feed the stream from the source

Examples (pick one):

```dolphindb
// From Kafka plugin
loadPlugin("kafka")
conf = dict(STRING, STRING)
conf["metadata.broker.list"] = "kafka:9092"
conf["group.id"] = "ddb-tick"
consumer = kafka::consumer(conf)
kafka::subscribe(consumer, ["ticks"])

def kafkaLoop(mutable consumer, mutable sink) {
    while (true) {
        msgs = kafka::pollBatch(consumer, 5000, 100)
        if (size(msgs) > 0) {
            t = select timestamp(value.ts) as ts,
                       symbol(value.sym)    as sym,
                       double(value.px)     as px,
                       int(value.vol)       as vol
                from msgs
            sink.append!(t)
        }
    }
}

submitJob("kafkaPoller", "ingest from kafka",
          kafkaLoop, consumer, ticks)
```

```dolphindb
// From MQTT
loadPlugin("mqtt")
def onMqttMsg(msg) {
    ticks.append!(parseJsonMsg(msg))       // user-defined parse
}
mqtt::subscribe(mqtt::connect("tcp://broker:1883","dev1"), "ticks/#", 1, onMqttMsg)
```

```dolphindb
// From a REST poll (httpClient)
loadPlugin("httpClient")
def pollLoop(mutable sink) {
    while (true) {
        resp = httpClient::httpGet("https://api.x.com/latest")
        t = parseResp(resp)                // user-defined
        sink.append!(t)
        sleep(100)
    }
}
submitJob("restPoller", "poll REST", pollLoop, ticks)
```

## Back-pressure & reliability

- **Persistence required** for `persistOffset=true`. Without disk
  persistence, a restart loses un-acked rows.
- **Cap memory** with `cacheSize` and `retentionMinutes`. Unbounded stream
  tables crash the node on OOM.
- **Multiple DFS appenders** lock the same partition → serialize. Route
  each consumer to a disjoint partition (by date or hash) if you truly
  need write parallelism.
- **Dead-letter**: wrap the handler in `try{} catch(ex){ errors.append!(...) }`
  to ring-buffer failures into another stream table.

## Monitoring

```dolphindb
getStreamingStat().pubTables       // publishers
getStreamingStat().subWorkers      // consumer workers
getStreamingStat().persistenceMeta // disk status
getPersistenceStat()
```

If a subscription falls behind, `msgAsTable` batches grow; consider
adding a parallel subscriber with `hash = <different>`.

## See also

- `../docs/40-streaming/stream-table.md`, `../docs/40-streaming/subscribe.md`.
- `../docs/50-ingestion/kafka-mqtt.md`.
- `../docs/30-database/partitioning.md` for picking the right DFS layout.
- `../docs/70-perf/memory-threading.md` for `cacheSize` tuning.
- `../docs/tutorials/README.md` → Streaming section for worked cases.
