# Pattern — Python ↔ DolphinDB roundtrip without type loss

## Problem

You pull a DolphinDB table into Python, process it with pandas / numpy,
and write it back. Along the way `SYMBOL` becomes `object`, `TIMESTAMP`
becomes `datetime64[ns]` (which loses ms/us distinction in edge cases),
`DECIMAL` becomes `float64` (silently lossy), and nulls get muddled
between `NaN`, `NaT`, `None`, and DolphinDB sentinels.

This pattern locks the types down.

## When to use

| Use | Don't use |
|-----|-----------|
| Any production pandas ↔ DolphinDB pipeline | One-off exploratory script — just accept the defaults. |
| You have `DECIMAL`, `SYMBOL[]`, nano-second timestamps, or `BLOB` | All your columns are `INT` / `DOUBLE` / `DATE` — defaults are fine. |

## Solution

### 1. Pin the DolphinDB schema explicitly

Never rely on `loadText` schema inference for production tables.

```dolphindb
def makeTickSchema() {
    return table(1:0,
        `ts`sym`px`vol`side,
        [NANOTIMESTAMP, SYMBOL, DECIMAL32(4), LONG, CHAR])
}
```

Decide on the **narrowest correct type**: `CHAR` instead of `INT` for
side, `DECIMAL32(4)` instead of `DOUBLE` for prices that need exact
arithmetic.

### 2. Pull into pandas with matching dtypes

```python
import dolphindb as ddb
import pandas as pd
import numpy as np

s = ddb.session()
s.connect("localhost", 8848, "admin", "123456")

# Prefer the Arrow path — preserves SYMBOL, DECIMAL, nano timestamps.
df = s.runArrow("select * from loadTable('dfs://tick', `trade) "
                "where date = 2024.03.15")
# df is a pyarrow.Table; convert with explicit types
pdf = df.to_pandas(
    types_mapper=pd.ArrowDtype,          # keep pyarrow dtypes end-to-end
    timestamp_as_object=False,
)

# Falls back to pickle path if runArrow not available.
# pdf = s.run("select * from ...")       # returns pd.DataFrame; SYMBOL → object
```

**Key:** `runArrow` + `ArrowDtype` keeps `SYMBOL` as `string[pyarrow]`
(no conversion cost, no `.astype(str)` surprises) and `DECIMAL` as
`decimal128` (exact arithmetic with `decimal.Decimal`).

### 3. Null mapping

| DolphinDB | pandas (Arrow) | pandas (numpy) |
|-----------|---------------|----------------|
| `00i` (null INT) | `pd.NA` | `NaN` (silently cast to float!) |
| `00F` (null DOUBLE) | `pd.NA` / NaN | `NaN` |
| `00p` (null TIMESTAMP) | `NaT` | `NaT` |
| `""` (null SYMBOL / STRING) | `pd.NA` | `None` or `""` (ambiguous!) |

Use **ArrowDtype everywhere** to get `pd.NA` uniformly and keep INT
columns as integer (not float-with-NaN).

### 4. Compute in pandas without breaking types

```python
# BAD: casts INT with nulls to float64
pdf["vol_x2"] = pdf["vol"] * 2

# GOOD: with ArrowDtype, INT stays INT
pdf["vol_x2"] = pdf["vol"] * 2            # dtype: int64[pyarrow], null preserved

# BAD: .fillna(0) on a nanotimestamp column — converts to object
pdf["ts"] = pdf["ts"].fillna(pd.NaT)      # OK

# DECIMAL math: only use decimal or pyarrow compute; numpy will coerce
import pyarrow.compute as pc
pdf["notional"] = pc.multiply(pdf["px"].array, pdf["vol"].array).to_pandas()
```

### 5. Push back with explicit column types

```python
# Build a DolphinDB schema-matched DataFrame
payload = pdf[["ts", "sym", "px", "vol", "side"]].reset_index(drop=True)

# Option A: tableAppender (fast, validates schema)
appender = ddb.tableAppender(
    dbPath="dfs://tick", tableName="trade", ddbSession=s)
n = appender.append(payload)              # returns rows appended

# Option B: upload + run (when you need transform server-side)
s.upload({"payload": payload})
s.run("""
    loadTable('dfs://tick', `trade).append!(
        select nanotimestamp(ts)  as ts,
               symbol(sym)        as sym,
               decimal32(px, 4)   as px,
               long(vol)          as vol,
               char(side)         as side
        from payload
    )
""")
```

**Option B with explicit casts is the safe form** for DECIMAL /
NANOTIMESTAMP / SYMBOL — it prevents silent truncation.

### 6. Verify roundtrip

```python
def roundtrip_check(df_before, dbPath, tableName, key_cols):
    df_after = s.runArrow(
        f"select * from loadTable('{dbPath}', `{tableName}')").to_pandas(
        types_mapper=pd.ArrowDtype)
    merged = df_before.merge(df_after, on=key_cols, suffixes=("_b","_a"))
    for col in df_before.columns:
        if col in key_cols: continue
        mism = ~(merged[f"{col}_b"].astype("string") == merged[f"{col}_a"].astype("string"))
        if mism.any():
            print(f"{col}: {mism.sum()} rows differ")
```

Add this to your CI. The `.astype("string")` normalises NA handling for
the comparison.

## Type quick-reference

| DolphinDB | pyarrow | pandas (ArrowDtype) | numpy fallback |
|-----------|---------|---------------------|----------------|
| `BOOL`    | bool    | `bool[pyarrow]`     | `bool`         |
| `CHAR`    | int8    | `int8[pyarrow]`     | `int8` / `float64` if null |
| `INT`     | int32   | `int32[pyarrow]`    | `int32` / `float64` if null |
| `LONG`    | int64   | `int64[pyarrow]`    | `int64` / `float64` if null |
| `FLOAT`   | float32 | `float32[pyarrow]`  | `float32` |
| `DOUBLE`  | float64 | `float64[pyarrow]`  | `float64` |
| `DECIMAL32(s)` | decimal128(9, s) | `decimal128[pyarrow]` | `object` (Decimal) |
| `DECIMAL64(s)` | decimal128(18, s) | `decimal128[pyarrow]` | `object` (Decimal) |
| `SYMBOL`  | string  | `string[pyarrow]`   | `object` |
| `STRING`  | string  | `string[pyarrow]`   | `object` |
| `BLOB`    | binary  | `binary[pyarrow]`   | `object` (bytes) |
| `DATE`    | date32  | `date32[pyarrow]`   | `datetime64[ns]` (widened) |
| `TIMESTAMP` | timestamp[ms] | `timestamp[ms][pyarrow]` | `datetime64[ns]` |
| `NANOTIMESTAMP` | timestamp[ns] | `timestamp[ns][pyarrow]` | `datetime64[ns]` |
| `UUID`    | extension | `object` | `object` (UUID) |

## Traps

- **`SYMBOL[]` (array vector of symbol)** — only Arrow path preserves
  this. Pickle path flattens to nested `object`.
- **`DECIMAL` through numpy = `float64`**, which silently truncates
  beyond 15 decimal digits. Always Arrow or upload-then-cast.
- **pandas `datetime64[ns]`** cannot represent dates < 1677 or > 2262.
  DolphinDB `NANOTIMESTAMP` can. If you have boundary data, stay in
  pyarrow.
- **`None` in a SYMBOL column uploaded via `session.upload`** becomes
  the string `"None"`. Replace with `""` or `pd.NA` before upload.
- **Timezone**: DolphinDB is timezone-naive (UTC-ish); pandas Arrow
  `timestamp[ns, tz=UTC]` requires `tz_convert(None)` before upload or
  explicit cast.
- **`tableAppender` with mismatched column order** silently fills
  columns in position order. Always call with a DataFrame whose columns
  match the DolphinDB schema exactly (use `reset_index(drop=True)` too).
- **Symbol table pollution:** appending many unique SYMBOL values
  (e.g. from user input strings) grows the per-partition symbol
  dictionary forever. Use `STRING` for high-cardinality columns.

## Performance

| Size | Method | Typical throughput |
|------|--------|-------------------|
| < 100k rows | `session.run` (pickle) | 50k rows/s |
| < 10M rows | `session.runArrow` | 500k – 2M rows/s |
| Write < 100k | `session.run` + upload | 100k rows/s |
| Write bulk | `tableAppender` | 500k – 1M rows/s |
| Write partitioned | `PartitionedTableAppender` | 1M – 5M rows/s (parallel) |

Rules:
- Arrow for reads, `tableAppender` / `PartitionedTableAppender` for writes.
- For > 10M rows, stage via Parquet — write Parquet from pandas, then
  `loadPlugin("parquet"); parquet::loadParquet(...)` in DolphinDB. 10×
  faster than uploading a DataFrame.

## See also

- `../docs/60-api/python-api.md`, `type-mapping.md`.
- `../docs/tutorials/function_mapping_py.md`,
  `hybrid_programming_paradigms.md`, `Python_HDF5_vs_DolphinDB.md`.
- `../examples/python-api-quickstart.py` — runnable starting point.
