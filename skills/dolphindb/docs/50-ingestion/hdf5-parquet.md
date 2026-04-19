# HDF5 / Parquet / Arrow / ORC / Feather

These require loading the matching plugin. All plugins follow the same shape:
`<plugin>::loadXxx(path)` returns an in-memory table; `<plugin>::saveXxx(t, path)` writes.

## Parquet

```dolphindb
loadPlugin("parquet")

// read
t = parquet::loadParquet("/data/ticks.parquet")

// write
parquet::saveParquet(t, "/out/ticks.parquet")
```

Parquet is the recommended interchange format for data coming from
Spark/Presto/DuckDB/Pandas.

## HDF5

```dolphindb
loadPlugin("hdf5")

t = hdf5::loadHDF5("/data/ticks.h5", "/tables/trades")
hdf5::saveHDF5(t, "/out/trades.h5", "/tables/trades")
```

## Arrow

```dolphindb
loadPlugin("Arrow")
t = arrow::loadFromArrowStream("/data/stream.arrow")
```

Also exposed directly over the **Arrow protocol** in the Python API
(`ddb.session(protocol=ddb.PROTOCOL_ARROW)`) for zero-copy transfer without
using the plugin.

## ORC

```dolphindb
loadPlugin("orc")
t = orc::loadORC("/data/ticks.orc")
```

## Feather

```dolphindb
loadPlugin("feather")
t = feather::load("/data/ticks.feather")
```

## Typical pipeline — Parquet → DFS

```dolphindb
loadPlugin("parquet")
t = parquet::loadParquet("/data/ticks.parquet")
loadTable("dfs://demo", `trades).append!(t)
```

For very large Parquet files, loop per row group:

```dolphindb
meta = parquet::getSchema("/data/big.parquet")
for (rg in 0..(meta.rowGroups - 1)) {
    t = parquet::loadParquet("/data/big.parquet", , rg)
    loadTable("dfs://demo", `trades).append!(t)
}
```

## Traps

- **Plugin not installed.** `installPlugin("parquet")` once on every data
  node before use.
- **Decimal columns** may need type mapping — inspect `parquet::getSchema`.
- **Very wide Parquet** (>1000 cols): load only needed columns by passing
  a column list.

## See also

- `reference/plugins-catalog.md` — all file-format plugins.
- `loadText-ploadText.md` for CSV.
