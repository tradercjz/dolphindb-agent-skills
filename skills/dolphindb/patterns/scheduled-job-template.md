# Pattern — scheduled jobs that survive restart & errors

## Problem

You need to run a DolphinDB script on a schedule — nightly ETL, intra-day
snapshot, weekly archive. It must survive server restarts, not re-run on
failure without logging, and be idempotent when manually re-triggered.

## When to use

| Use | Don't use |
|-----|-----------|
| Pure DolphinDB-side schedule | You need cross-system orchestration → use Airflow / DolphinScheduler (see `docs/tutorials/ddb_airflow.md`, `dolphinscheduler_integration.md`). |
| Daily / weekly / monthly batch over DFS | Sub-minute schedules → use a streaming subscription + timer. |

## Solution

### 1. Make the job function idempotent

The #1 rule: running today's job twice must equal running it once.

```dolphindb
def nightlyIngest(runDate) {
    // Delete today's rows first, then insert. Safe on re-run.
    tgt = loadTable("dfs://tick", `trade)
    delete from tgt where date = runDate
    src = loadText("/data/raw/" + temporalFormat(runDate, "yyyyMMdd") + ".csv")
    tgt.append!(src)
    return size(src)
}
```

Alternative idempotent patterns:
- **PKEY table** — `upsert!` the same keys, no delete needed.
- **Staging partition** — write to a new partition, swap atomically.
- **Checksum & skip** — read a `job_runs` tracking table, skip if row exists.

### 2. Wrap in try/catch with audit table

```dolphindb
if (not existsTable("dfs://ops", `jobRuns)) {
    db = database("dfs://ops", VALUE, 2024.01.01..2030.12.31)
    db.createPartitionedTable(
        table(1:0, `date`jobName`startTs`endTs`status`rowsOrErr,
              [DATE, SYMBOL, TIMESTAMP, TIMESTAMP, SYMBOL, STRING]),
        `jobRuns, `date)
}

def runWithAudit(jobName, runDate, fn) {
    start = now()
    audit = loadTable("dfs://ops", `jobRuns)
    try {
        rows = fn(runDate)
        audit.append!(table(
            [runDate] as date, [jobName] as jobName,
            [start] as startTs, [now()] as endTs,
            [`ok] as status, [string(rows)] as rowsOrErr))
        return rows
    } catch (ex) {
        audit.append!(table(
            [runDate] as date, [jobName] as jobName,
            [start] as startTs, [now()] as endTs,
            [`failed] as status, [ex] as rowsOrErr))
        throw "[" + jobName + "] " + ex                    // re-raise for scheduleJob
    }
}
```

### 3. Register the schedule

```dolphindb
scheduleJob(
    jobId       = "nightlyIngest",
    jobDesc     = "Load yesterday's CSV into dfs://tick",
    jobFunc     = runWithAudit{`nightlyIngest, _, nightlyIngest},
    startTime   = 02:00:00,                             // run at 02:00
    endTime     = 05:00:00,                             // cutoff
    frequency   = 'D',                                  // daily
    days        = weekdays,                             // ['Mon','Tue',...'Fri']
    onComplete  = onJobDone                             // optional callback
)
```

Notes:
- `jobFunc` is called as `jobFunc(date())` — the scheduler passes today's date.
- The **partial application** `runWithAudit{`nightlyIngest, _, nightlyIngest}`
  binds the job name and function, leaving `runDate` for the scheduler.
- `scheduleJob` persists the schedule to `<home>/sysmgmt/jobEditlog.meta`.
  Survives restarts automatically.

### 4. Manage schedules

```dolphindb
getScheduledJobs()              // list all
deleteScheduledJob(`nightlyIngest)
getRecentJobs(20)               // last runs
getJobMessage(jobId)            // error text of a failed run
```

### 5. Manual re-run with the same code path

```dolphindb
// Back-fill 2024-03-14:
runWithAudit(`nightlyIngest, 2024.03.14, nightlyIngest)
```

Because the function is idempotent, this is safe even if the original run
also succeeded.

## Variants

### Hourly / intra-day

```dolphindb
scheduleJob("hourlyAgg", "...",
    def() { aggregateLastHour(now()) },
    minutesOfHour(0),               // top of each hour
    00:00:00, 23:59:59, 'H')
```

`minutesOfHour(0)` means every hour at :00. Alternative forms:
`minutes(0 15 30 45)` for every 15 min.

### Weekly close-of-business

```dolphindb
scheduleJob("weeklyArchive", "...",
    archiveFn,
    17:30:00, 23:59:59, 'W',
    days=[`Fri])
```

### Chained jobs

If job B depends on job A:

```dolphindb
def chainAfterA(date) {
    // busy-wait for A's success row; simple but OK for daily jobs
    audit = loadTable("dfs://ops", `jobRuns)
    for (i in 0..60) {
        ok = exec count(*) from audit
             where date = date and jobName = `A and status = `ok
        if (ok > 0) { return runWithAudit(`B, date, jobB) }
        sleep(60000)
    }
    throw "[B] timeout waiting for A"
}
scheduleJob("B", "...", chainAfterA, 03:00:00, 07:00:00, 'D')
```

For real DAGs, prefer DolphinScheduler / Airflow (`ddb_airflow.md`).

## Traps

- **Non-idempotent jobs + manual re-run = double data.** Always
  `delete then insert` or `upsert!`.
- **`scheduleJob` is per-node.** In a HA cluster, register on the
  controller or one specific data node; don't replicate or it runs N times.
- **`startTime` / `endTime`** are **both required and bound the window**.
  If the job overruns `endTime`, it's killed at the deadline.
- **Job definitions are captured by value at registration.** If you
  redefine `nightlyIngest` later, re-run `scheduleJob` to pick it up, or
  use a loader that reads from a module file.
- **The `catch` must re-throw** (as shown) so `scheduleJob` records
  failure. Silent catch hides errors from `getJobMessage`.
- **Memory**: long-running scheduled jobs accumulate session memory.
  Either exit often (preferred — the scheduler creates a new session
  per run) or call `undef(all)` / `clearCachedDatabase()` at end.

## Monitoring

```dolphindb
// daily: list yesterday's failures across all jobs
select * from loadTable("dfs://ops", `jobRuns)
where date = today() - 1 and status = `failed
```

Wire into Prometheus via `prometheusExporter` or email via `httpClient`.

## See also

- `../docs/tutorials/scheduledJob.md`, `scheduledJob_2.md`.
- `../docs/tutorials/ddb_airflow.md`, `dolphinscheduler_integration.md`
  for cross-system DAGs.
- `../docs/10-language/error-handling.md` for audit patterns.
- `stream-ingestion-to-dfs.md` for the streaming counterpart.
