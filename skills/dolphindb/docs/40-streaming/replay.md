# Historical replay

`replay` streams a **historical table** through a stream table at a
controlled rate, so you can test/back-test stream pipelines against past
data.

## One-to-one replay

```dolphindb
// source: DFS tick table; sink: shared stream table
src  = loadTable("dfs://tick", `tick)
sink = ticks     // share streamTable(...) as ticks

replay(
    inputTables   = src,
    outputTables  = sink,
    dateColumn    = `ts,
    timeColumn    = `ts,
    replayRate    = 100000,        // rows per second; -1 = as fast as possible
    absoluteRate  = true
)
```

## Many-to-one and many-to-many

`replay` supports replaying multiple source tables into multiple stream
tables with a shared time axis — useful for joint tick+quote replay:

```dolphindb
replay(
    inputTables   = [tradesHist, quotesHist],
    outputTables  = [trades, quotes],
    dateColumn    = `ts,
    timeColumn    = `ts,
    replayRate    = -1
)
```

See `str_replay_n21.md` and `str_replay_n2n.md`.

## Stopping

```dolphindb
cancelJob(jobId)
// or
stopReplay(replayHandle)
```

## Traps

- **Replay writes into the **stream table**, not into a DFS table.** All
  data goes through the pub/sub path — subscribers receive it as if live.
- **Time jump**: if the first source row is much later than `now()`,
  subscribers may backlog. Use `replayRate` carefully.
- **Multiple replays into same stream table** will interleave rows; use
  separate stream tables if you need isolation.

## See also

- `str_replay.md`, `str_replay_1.md`, `str_replay_n21.md`,
  `str_replay_n2n.md`.
