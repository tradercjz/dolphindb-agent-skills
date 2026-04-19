# `pivot by` — native pivot in SQL

DolphinDB's `pivot by` turns two grouping columns into (rows × columns) in
a single SQL clause. No cross join, no `case when` pyramid.

## Syntax

```dolphindb
select <aggregate(column)>
from <table>
pivot by <row_key>, <col_key>
```

- `<row_key>` values become distinct rows.
- `<col_key>` values become **distinct columns** in the output. Any value
  that shows up in `col_key` will produce one output column.
- The aggregate fills each cell.

## Example — minute OHLC matrix per symbol

```dolphindb
// t has columns: sym, minute, price
select avg(price) from t pivot by minute, sym
//                  AAPL    MSFT    GOOG
// 09:30:00         100.1   260.2   140.5
// 09:31:00         100.3   260.5   140.7
```

One row per `minute`, one column per `sym`. The result is a *regular table*
(not a matrix) — columns are typed the same as the aggregate's output.

## Tips

- **Use `exec ... pivot by` to return a matrix** when you want row + column
  indices as vectors (useful for matrix math, `rowSum` etc.):

  ```dolphindb
  m = exec avg(price) from t pivot by minute, sym
  typestr(m)   // MATRIX
  ```

- **Column names** are taken from the distinct values of `<col_key>` — they
  must be valid DolphinDB identifiers or get quoted. Numeric keys produce
  columns named `col_<value>`.

- **Order of rows/columns** is the sort order of the key columns. Use
  `order by` on the outer query if you need custom ordering.

- **Multiple aggregates** are allowed:

  ```dolphindb
  select avg(price) as px, sum(volume) as vol
  from t pivot by minute, sym
  ```

  Output columns become `px_AAPL, vol_AAPL, px_MSFT, vol_MSFT, ...`.

## Un-pivot

The inverse is the `unpivot` SQL function (wide → long). See
`../../reference/functions/by-name/u/unpivot.md`.

## When to reach for `pivot by` vs `context by`

- Need a **wide table** with one column per symbol? → `pivot by`.
- Need to keep the long format and add a rolling/rank column? → `context by`.

## See also

- `pivotBy.md` — full reference with all aggregate variants.
