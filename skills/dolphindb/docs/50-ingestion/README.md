# 50-ingestion — data import

## Hand-authored

- `loadText-ploadText.md` — CSV ingest, schema inference, parallel load.
- `hdf5-parquet.md`       — columnar file formats (HDF5, Parquet, Arrow, ORC, Feather).
- `kafka-mqtt.md`         — real-time ingest from message buses.

## Full reference pages

From `db_distr_comp/db_oper/*.md` upstream, in this directory:

| Topic | File |
|-------|------|
| Data import overview | `data_import_method.md` |
| Text / CSV | `text_files_import.md` |
| HDF5 | `hdf5_import.md` |
| Parquet | `parquet_import.md` |
| From databases | `database_import.md` |
| From message queue | `mq_import.md` |

Plus:
- Per-source plugin docs in `reference/plugins-catalog.md` and upstream
  `documentation-main/plugins/*`.
- `docs/40-streaming/` for streaming ingest details.

## Quick patterns

### CSV → DFS

```dolphindb
db = database("dfs://demo", VALUE, 2024.01.01..2024.12.31, engine="TSDB")
schema = extractTextSchema("/data/ticks.csv")

// parallel load
ploadText(
    filename   = "/data/ticks.csv",
    schema     = schema,
    dbHandle   = db,
    tableName  = `trades,
    partitionColumns = `ts,
    sortColumns = `sym`ts,
    delimiter  = ","
)
```

### Parquet → DFS (with plugin)

```dolphindb
loadPlugin("parquet")
t = parquet::loadParquet("/data/ticks.parquet")
loadTable("dfs://demo", `trades).append!(t)
```

### MySQL → DolphinDB

```dolphindb
loadPlugin("mysql")
conn = mysql::connect("host", 3306, "user", "pass", "db")
t = mysql::load(conn, "select * from mytable")
loadTable("dfs://demo", `trades).append!(t)
```
