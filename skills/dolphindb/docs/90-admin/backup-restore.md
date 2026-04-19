# Backup & restore

DolphinDB supports two backup granularities:

- **Chunk backup** (default) — raw binary; fastest; can only restore to a
  compatible DolphinDB version.
- **SQL backup** — portable; backs up via `select` queries; restorable
  across versions.

## Back up a database

```dolphindb
backup(
    backupDir     = "/data/backups/demo-2024-01",
    sqlObj        = <select * from loadTable("dfs://demo", `trades)>,   // SQL backup
    force         = false,
    parallel      = true,
    chunkGranularity = "CHUNK"     // or "DATABASE"
)

// chunk backup of a whole DB
backupDB(backupDir = "/data/backups/demo-2024-01", dbPath = "dfs://demo")
backupTable(backupDir = "/data/backups/demo-2024-01", dbPath = "dfs://demo", tableName=`trades)
```

## Restore

```dolphindb
restore(
    backupDir = "/data/backups/demo-2024-01",
    dbPath    = "dfs://demo",
    tableName = `trades,
    partition = "%",
    force     = false
)

// or from chunk backup
migrate(backupDir = "/data/backups/demo-2024-01", dbPath = "dfs://demo")
```

## Inspect

```dolphindb
getBackupList("/data/backups/demo-2024-01")
getBackupMeta("/data/backups/demo-2024-01")
getBackupStatus()
checkBackup("/data/backups/demo-2024-01")
```

## Practical tips

- **Schedule** with `scheduledJob` (see upstream `tutorials/scheduledJob_2.md`).
- **Back up to S3** via the `aws` plugin or via mount.
- **Test restore** in a staging cluster regularly; untested backups are not
  backups.
- **Retention**: chunk backups can be large; rotate manually.

## Traps

- **`chunkGranularity = "DATABASE"`** requires SQL backup (cannot mix with
  chunk) — see error `S01021`.
- **Restore requires the same partitioning scheme** as the source database
  (for chunk restore).
- **`force=true`** overwrites existing target data — use with care.

## See also

- `bak_resto.md` and other sibling admin pages in this directory.
- Upstream `tutorials/` for scheduling examples.
