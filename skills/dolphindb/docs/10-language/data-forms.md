# Data forms

DolphinDB distinguishes **type** (int, double, timestamp, …) from **form**
(scalar, vector, matrix, table, …). A column can be `INT:vector`, `INT:scalar`,
or even `INT:arrayVector`.

## The forms

| Form | Constructor / syntax | Notes |
|------|----------------------|-------|
| **Scalar** | `42` | Single value. |
| **Pair** | `1 : 10`, `pair(a, b)` | Exactly two values; used for ranges. |
| **Vector** | `[1,2,3]`, `1 2 3`, `array(INT, 10)` | 1-D of a single type. |
| **Matrix** | `matrix([...])`, `1..100$10:10` | 2-D; rectangular; single type. |
| **Set** | `set([1,2,3])` | Unordered unique values. |
| **Dictionary** | `dict(KEY_TYPE, VAL_TYPE)`, `dict(`a`b, 1 2)` | Typed hash map. **No `{}` literal.** See `dict.md` for the full cheat-sheet (creation, access, `ANY` values, `syncDict` for concurrency). |
| **Table** | `table(col1, col2, ...)` | Named typed columns. |
| **Tuple** | `(a, b, c)` | Heterogeneous list. |
| **Array vector** | `arrayVector(rowOffset, data)` | Variable-length arrays per row (e.g. depth vector per tick). |
| **Tensor** | `tensor(...)` | n-D arrays for ML. |

## Vectors

```dolphindb
v = 1 2 3 4 5              // literal
v = 1..100                 // range
v = take(`AAPL`MSFT, 10)   // repeat to length 10
v = rand(100.0, 5)         // random
v[0]                       // first element
v[0:3]                     // slice, like Python 0..2
size(v)                    // length
```

## Pair and range

`1:10` creates a pair; inside `select` it means "half-open range" (like Python
`1..10`). Used in `between`, `limit`, slicing.

## Tables

```dolphindb
t = table(
    `AAPL`MSFT as sym,
    100.0 200.0 as px
)

// empty-with-capacity
t = table(1000000:0, `sym`px, [SYMBOL, DOUBLE])

// from dict of vectors
t = table(d)          // d is dict
```

Table is a dict of vectors under the hood; `t[`px]` and `t.px` both return
the column vector.

## Keyed / indexed tables

| Constructor | Semantics |
|-------------|-----------|
| `keyedTable(`sym, t)` | Dedup by key; `append!` with existing key replaces. |
| `indexedTable(`sym, t)` | Dedup + hash index for O(1) key lookup. |
| `streamTable(...)` | Append-only stream (see `docs/40-streaming/`). |
| `keyedStreamTable(...)` | Stream + key dedup. |

## Array vector — nested arrays per row

Useful for storing e.g. 10-level order book depth as one value per row:

```dolphindb
bidsAll = arrayVector(0 3 6, 100.0 99.9 99.8 101.0 100.9 100.8)
// row 0: [100.0, 99.9, 99.8]
// row 1: [101.0, 100.9, 100.8]
```

Access with `bidsAll[0]`. Most aggregate functions accept array vectors
and operate per row.

## Matrix

```dolphindb
m = 1..12$3:4            // 3×4 matrix filled by column
rowSum(m)                // per-row sum
m[0, ]                   // first row
m[, 0]                   // first column
```

## Converting between forms

| From | To | |
|------|----|---|
| vector | matrix | `reshape(v, r:c)` or `v$r:c` |
| matrix | table | `table(m)` |
| table | matrix | `matrix(t)` (all columns must be same type) |
| table | dict | `dict(t.keyCol, t.valCol)` |

## Tips

- Use **dictionaries** for state you'd build a Python dict for.
- Use **tables** for anything that'll eventually be persisted or queried
  with SQL.
- Prefer **typed construction** with `table(capacity:0, cols, types)` over
  mass row-at-a-time appends.

## See also

- `data_forms.md`, `tensor.md`, `objs/*.md`.
