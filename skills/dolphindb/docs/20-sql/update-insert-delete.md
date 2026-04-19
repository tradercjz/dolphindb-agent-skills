# `update` / `insert into` / `delete` / `append!`

DolphinDB offers both SQL-style mutation (`update`, `insert into`, `delete`)
and script-style mutation (`append!`, `update!`, `erase!`, `upsert!`).

## Append rows — `append!`

The fast path for bulk write. Works on in-memory tables, stream tables, and
DFS tables.

```dolphindb
pt = loadTable("dfs://demo", `trades)
pt.append!(t)            // t is a table with matching schema
```

- `append!` **appends** — it never updates existing rows.
- Columns must match **exactly** in count, order, and (convertible) type.
  Misalignment silently reorders or fails with `S01015`. Always verify with
  `schema(pt).colDefs` first.
- On DFS tables, `append!` is an atomic transaction per partition.

## `insert into`

SQL form of append, mostly for in-memory / stream tables. Not used for DFS
bulk load — prefer `append!`.

```dolphindb
insert into t values(2024.01.01, `AAPL, 100.0)
insert into t (sym, price) values(`MSFT, 260.0)
```

## `update`

```dolphindb
update t set price = price * 1.1 where sym = `AAPL
```

- Standard SQL form; works on in-memory, stream, OLAP, TSDB, PKEY tables.
- On **TSDB/OLAP** DFS tables, `update` rewrites entire partitions — slow
  and should be avoided at scale. Use PKEY engine + `upsert!` for
  fine-grained updates.
- Inside a script, `update!` is the mutating form on an in-memory handle:

  ```dolphindb
  update t set price = price * 1.1 where sym = `AAPL
  t.update!(`price, <price * 1.1>, <sym = `AAPL>)    // meta-code form
  ```

## `delete`

```dolphindb
delete from t where sym = `AAPL and ts < 2024.01.01
```

- For DFS tables, delete is done per-partition and may drop entire
  partitions if the predicate matches all rows.
- For PKEY tables, `delete` + `where primaryKey = ...` is point-delete.

## `upsert!` — PKEY engine only

```dolphindb
pt.upsert!(newRows, keyColNames=`sym, ignoreNull=false)
```

- Updates existing rows keyed by `keyColNames`, inserts new ones.
- Requires the table to be on the **PKEY** engine. TSDB/OLAP do not
  support upsert.

## Delete columns / rows in script

- `erase!(t, keyVals)` — row delete by keyed value (for keyed tables).
- `dropColumns!(t, `col`othercol)` — drop columns from an in-memory table.

## Traps

- **`append!` changes the source table in place** (that's what the `!`
  means). Its return value is the appended count, not the table.
- **Column order matters** when passing a plain table to `append!`.
  If source and target disagree on order, use `select col1, col2, ... from t`
  to realign first.
- **`update` on DFS TSDB/OLAP is expensive** — whole-partition rewrite.
  Consider keeping a small PKEY override table and joining.
- **`insert into` on a stream table publishes** — every inserted row is
  broadcast to subscribers.

## See also

- `update.md`, `delete.md`, `insertInto.md`,
  `alter.md`.
- `docs/30-database/pkey-engine.md` — upsert semantics.
- `../../reference/functions/by-theme/数据操作.md` — `append!`, `upsert!`,
  `erase!`, `pop!`, `dropColumns!`.
