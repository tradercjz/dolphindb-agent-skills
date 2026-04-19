# `loadText` / `ploadText` — CSV ingest

## Overview

| Function | Parallel? | Returns | Use for |
|----------|-----------|---------|---------|
| `loadText`         | No  | In-memory table | Small files. |
| `ploadText`        | Yes | In-memory table | Larger single files — parallel parse. |
| `loadTextEx`       | Yes | Loads directly into a DFS table | **Bulk ingest → DFS**; preferred. |

## Schema inference + override

```dolphindb
// inspect inferred schema
sch = extractTextSchema("/data/ticks.csv")
sch
// name  type
// sym   SYMBOL
// ts    DATETIME
// px    DOUBLE

// override column types
update sch set type = "TIMESTAMP" where name = "ts"

t = loadText(filename="/data/ticks.csv", schema=sch, delimiter=",")
```

## Parallel load → DFS (`loadTextEx`)

Fastest way to ingest a big CSV into a partitioned DFS table:

```dolphindb
db = database("dfs://demo", VALUE, 2024.01.01..2024.12.31, engine="TSDB")

loadTextEx(
    dbHandle         = db,
    tableName        = `trades,
    partitionColumns = `ts,
    filename         = "/data/ticks.csv",
    schema           = sch,
    sortColumns      = `sym`ts
)
```

- Parallelism is auto-derived from cluster size; override with
  `ploadText(..., arrayDelimiter=...)` parameters.

## Options you will adjust

| Param | Default | Notes |
|-------|---------|-------|
| `delimiter`       | `,` | e.g. `|` for pipe-delimited |
| `skipRows`        | 0   | Skip headers / comments. |
| `containHeader`   | true | Set false for no header row. |
| `arrayDelimiter`  | "" | If a column holds repeated values, e.g. `"a,b,c"`. |
| `transform`       | a function `table -> table` applied before load. Use for dtype cleanup. |

## Traps

- **Date / time parsing** requires a consistent format. Mixed formats fail;
  fix at the source or apply a `transform` lambda.
- **Symbol cardinality**: naively loading a column with millions of
  distinct strings as SYMBOL can blow the symbol dictionary (`S00003`).
  Load as STRING first, then `cast` on server if cardinality permits.
- **Encoding**: DolphinDB assumes UTF-8. For GBK files, set `charset`
  explicitly via `iconv` preprocessing or the `convertEncode` function.
- **Empty columns** at the end of CSV rows silently produce nulls.

## See also

- `text_files_import.md`, `data_import_method.md`.
- `hdf5-parquet.md` for non-text formats.
