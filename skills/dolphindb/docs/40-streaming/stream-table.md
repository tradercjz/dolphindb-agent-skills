# Stream tables

A **stream table** is an append-only in-memory table that publishes every
insert to its subscribers. It is the core building block of DolphinDB
streaming.

## Create

```dolphindb
share streamTable(capacity:0, colNames, colTypes) as <name>
```

- `capacity` = initial row capacity (hint; table grows dynamically).
- `share` makes the table accessible across sessions. **Required** before
  other sessions can subscribe.
- `<name>` is a global symbol.

```dolphindb
share streamTable(1000000:0, `ts`sym`px, [TIMESTAMP, SYMBOL, DOUBLE]) as ticks
```

## Persist to disk (durable stream)

```dolphindb
enableTableShareAndPersistence(
    table     = streamTable(1000000:0, `ts`sym`px, [TIMESTAMP, SYMBOL, DOUBLE]),
    tableName = `ticks,
    asynWrite = true,
    compress  = true,
    cacheSize = 1_000_000,            // rows kept in memory
    retentionMinutes = 1440           // 1 day
)
```

Persistence allows:
- Subscribers to resume from a saved offset after restart.
- Replaying recent history.
- Automatic pruning via `retentionMinutes`.

## Publish

```dolphindb
insert into ticks values(now(), `AAPL, 100.5)
// or bulk
ticks.append!(t)
```

Every insert triggers the subscription handler (see `subscribe.md`).

## Types of stream tables

| Constructor | Purpose |
|-------------|---------|
| `streamTable(...)`            | Standard append-only stream table. |
| `keyedStreamTable(keys, ...)` | Dedup by key — same key replaces prior row. |
| `haStreamTable(...)`          | Raft-replicated, high-availability. Requires cluster config. |

## Filter column — topic partitioning

Subscribers can receive only rows matching a filter column:

```dolphindb
setStreamTableFilterColumn(ticks, `sym)

subscribeTable(
    tableName=`ticks, actionName=`onlyAAPL,
    handler=onAAPL, filter=`AAPL`AAPL2
)
```

## Inspect

```dolphindb
getStreamTables()
getStreamingStat().pubTables
```

## Lifecycle

```dolphindb
// remove
unsubscribeTable(tableName=`ticks, actionName=`demo)
dropStreamTable(`ticks)

// clear persistence
clearTablePersistence(ticks)
```

## Traps

- **Not `share`d → cannot subscribe.** `subscribeTable` errors out.
- **Dropping a stream table with active subscribers** leaves zombie
  subscriptions. Always `unsubscribeTable` first.
- **Persistence directory needs free disk.** Monitor `getPersistenceStat()`.
- **`insert into` on a stream table is synchronous by default** — batch
  via `append!` for throughput.

## See also

- `subscribe.md`
- `str_table.md`, `sub_pub.md`, `str_ha.md`.
