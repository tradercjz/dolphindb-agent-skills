# Error handling — `try/catch`, error types, and RefIds

## Syntax

```dolphindb
try {
    risky()
} catch (ex) {
    print("caught: " + ex)
    // ex is a STRING like "RefId: S00001. <message>"
}
```

- No `finally` clause. Use `try` inside a loop for per-item recovery.
- No typed exceptions. `ex` is a string; parse the `RefId` if you need
  to branch on error class.
- `throw "some message"` (string only) inside user code. The engine
  wraps it into a RefId-less error.

## Typical pattern: per-row isolation

```dolphindb
errors = table(1000:0, `idx`msg, [INT, STRING])
for (i in 0..(size(rows) - 1)) {
    try {
        processRow(rows[i])
    } catch (ex) {
        errors.append!(table([i] as idx, [ex] as msg))
    }
}
```

A `submitJob` that finishes with an exception is retrievable via
`getJobMessage("jobId")` — the return type is a string.

## Common error classes

| RefId | Class | Typical cause |
|-------|-------|--------------|
| `S00001` | Syntax | missing `;`, `{` / `}` mismatch |
| `S00002` | Type mismatch | `int + string`, bad cast |
| `S00003` | Dimension mismatch | vector vs scalar / matrix shape |
| `S00030` | Permission | missing ACL for table / DFS / function |
| `S00031` | Authentication | wrong login |
| `S01004` | Not found | unknown column / table / variable |
| `S02022` | Partition | invalid partition key value |
| `S03xxx` | DFS I/O | disk full, broken partition, sync failure |
| `S04xxx` | Streaming | subscription backlog, persistence |

Full list in `reference/error-codes/INDEX.md`. Query by RefId whenever
you see one in a log or client response.

## Log-only vs re-throw

```dolphindb
try {
    connect()
} catch (ex) {
    writeLog(ex)
    throw ex            // re-raise to caller — string; preserves message
}
```

## Background-job errors

`submitJob` / `submitJobEx` wrap the function body in an implicit
try/catch. Inspect with:

```dolphindb
jobId = submitJob("ingest", "nightly load", ingestFn, args)
getJobMessage(jobId)        // returns error string if failed, "" if OK
getJobStatus(jobId)         // "queuing" / "running" / "completed" / "failed"
getRecentJobs(10)           // recent
```

## Streaming subscription errors

Exception in a `subscribeTable` handler does NOT stop the subscription
by default — it logs and retries the same message, which **poison-pills
the topic**. Either:

- Wrap the body in `try/catch` and route bad messages to a dead-letter
  table.
- Set `handlerNeedMsgId=true` and checkpoint past the failing id.

```dolphindb
def safeHandler(mutable deadLetter, msg) {
    try {
        process(msg)
    } catch (ex) {
        deadLetter.append!(select msg.*, ex as error)
    }
}
subscribeTable(..., handler=safeHandler{deadLetter})
```

## Client-side (Python / Java / C++)

- **Python API:** raises `dolphindb.ErrorCodeInfo` with `errorCode`
  (the `RefId`) and `errorInfo`. Catch via `except Exception as e` and
  inspect `e.args[0]`.
- **Java:** `com.xxdb.data.exception.RuntimeException` with the same
  message text.
- **C++:** `IOException` / `RuntimeException` with `.what()`.

Log both the RefId and the message. The RefId is stable across versions.

## Common traps

- **String concatenation `+` with null**: produces a null string, not
  `"null"`. Guard with `isValid` or `string(x)`.
- **`try` inside a `for` loop** catches per-iteration, but variables set
  inside the `try` persist only if assigned before the throw. Initialize
  loop variables above the `try`.
- **No stack trace.** The message ends at the throw point. Add your
  own context: `throw "[stage=load] " + ex`.
- **`throw` must be a string.** `throw 42` fails syntax.
- **`catch (ex)` scope:** `ex` is only visible in the catch block.

## See also

- `reference/error-codes/INDEX.md` — full RefId catalog (3.9 MB).
- `../tutorials/guide_to_obtaining_stack_traces.md`,
  `../tutorials/faultAnalysis.md`.
- `../60-api/python-api.md` for client-side error types.
