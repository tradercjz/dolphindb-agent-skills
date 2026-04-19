# Dictionaries

## Contents
- Creating dicts (typed, from pairs, from `dict` constructor)
- Access, membership, delete
- `ANY` value dicts (heterogeneous)
- `syncDict` for concurrent access
- Common mistakes & quick-reference table

A DolphinDB dictionary is a **typed hash map**: keys share one type, values
share one type. It looks Python-like but has several DolphinDB-specific
rules that agents frequently get wrong.

## Creating

There are three shapes. **Use exactly one** — no `{}` literal exists.

```dolphindb
// 1. Empty dict, types declared up-front
d = dict(STRING, INT)                // key type, value type

// 2. From two parallel vectors
d = dict(`AAPL`MSFT`GOOG, 100 200 300)

// 3. Ordered dict (insertion-order iteration)
d = dict(`AAPL`MSFT`GOOG, 100 200 300, true)   // ordered=true
// or
d = dict(STRING, INT, true)
```

**There is no `{"a": 1, "b": 2}` literal.** Agents frequently write Python-
style dict literals; they are syntax errors in DolphinDB.

### Supported key types

`Literal` (SYMBOL / STRING), `Integral` (CHAR / SHORT / INT / LONG), `Floating`
(FLOAT / DOUBLE), `Temporal` (DATE / TIMESTAMP / ...). No BLOB, COMPRESS.

### Heterogeneous values — `ANY`

For Python-dict-like polymorphic values (the pattern used by stream-engine
configs), declare `ANY`:

```dolphindb
cfg = dict(STRING, ANY)
cfg["outputName"] = `stock_A:`amount
cfg["formula"]    = <price * volume>
cfg["price"]      = `stock_A:`price
```

`ANY` is only legal as the **value** type.

## Reading / writing

```dolphindb
d["AAPL"]                  // read a single key
d[`AAPL`MSFT]              // ★ vectorized read → returns a vector

d["AAPL"] = 150            // set
d[`AAPL`MSFT] = 150 260    // ★ vectorized set — one assignment for many keys

d.keys()                   // vector of keys
d.values()                 // vector of values
d.size()                   // number of entries
```

Vectorized read/write is a DolphinDB strength; prefer it over a `for`-loop
of scalar accesses.

## Missing-key behavior

Accessing a key that does not exist **returns the null of the value type**.
It does **not** throw (unlike Python `KeyError`).

```dolphindb
d = dict(STRING, INT)
d["AAPL"] = 100
d["missing"]               // -> INT null (00i), not an error

// safe existence check
d.contains("missing")      // false
"missing" in d.keys()      // also works, but slower — avoid in loops
```

Distinguish a real null value from "key absent" with `contains`:

```dolphindb
if(d.contains(k)) { ... use d[k] ... }
```

## Deleting

```dolphindb
erase!(d, "AAPL")          // remove one key
erase!(d, `AAPL`MSFT)      // vectorized remove

// reset to empty, keeping the declared types
d = dict(STRING, INT)
```

There is no `del d[k]`; use `erase!`.

## Iteration

```dolphindb
// pairs (Python dict.items() equivalent)
for (k in d.keys()) {
    v = d[k]
    ...
}

// apply a function to every value
each(f, d.values())

// build a new dict from transformation
d2 = dict(d.keys(), each(f, d.values()))
```

Iteration order is **arbitrary** unless the dict was created with
`ordered=true`.

## Merge / update

```dolphindb
d1.append!(d2)             // copy keys from d2 into d1

// apply a function to update specific keys
dictUpdate!(d, add, `AAPL`MSFT, 10 5)     // d[AAPL] += 10; d[MSFT] += 5

// with ANY-valued dict and missing keys, supply an init function
d.dictUpdate!(append!, newKeys, newVals, initFunc=x -> array(x.type(), 0, 512).append!(x))
```

## Dict ↔ table

```dolphindb
// dict whose values are same-length vectors → table
d = dict(`sym`px, [`AAPL`MSFT, 100 200])
t = table(d)                                // column per key

// table row → dict (row as a dict of scalars)
row = t[0]                                  // type = dict
row.sym                                     // `AAPL
```

This is how row iteration of tables yields a dict per row.

## Concurrency — use `syncDict`

Plain `dict` is **not thread-safe**. Concurrent writes from multiple
`submitJob` tasks or stream handlers can **crash the node** (see the
warning in the upstream `syncDict` docs). Always use `syncDict` when a
dict is shared across tasks/threads:

```dolphindb
d = syncDict(STRING, INT)            // same API as dict, but thread-safe

// shared across sessions:
syncDict(SYMBOL, INT, `myMap)        // becomes a global shared object named myMap
```

## Common mistakes

- **Python-style literal** `{"a": 1}` — syntax error. Build with `dict()`.
- **`dict()` with no args** — illegal. You must pass types or parallel vectors.
- **Treating missing-key read as an error** — it silently returns null.
  Guard with `.contains(k)` when the distinction matters.
- **SYMBOL vs STRING keys** — a dict created with SYMBOL keys requires
  SYMBOL lookup: `d[\`AAPL]`. Looking up with `d["AAPL"]` causes implicit
  cast and may miss. Pick one type at creation and stick with it.
- **`d + d2`** does **not** merge dicts — it tries element-wise add and
  typically errors. Use `d.append!(d2)` or `dictUpdate!`.
- **Using plain `dict` across `submitJob` / stream handlers** → may crash
  the node. Use `syncDict`.
- **Ordered iteration on an unordered dict** — iteration order is
  unspecified; pass `ordered=true` at creation time.
- **Polymorphic values** — forgetting to declare `ANY` for mixed value
  types. `dict(STRING, INT)` rejects non-INT values on assignment.
- **Key deletion with `del`** — no such operator; use `erase!`.

## Quick cheat-sheet

| Task | DolphinDB |
|------|-----------|
| Empty dict | `dict(KEY_TYPE, VAL_TYPE)` |
| Literal | `dict(keys, values)` — no `{ ... }` form |
| Heterogeneous values | `dict(STRING, ANY)` |
| Get | `d[k]` or vectorized `d[ks]` |
| Set | `d[k] = v` or vectorized `d[ks] = vs` |
| Contains | `d.contains(k)` |
| Delete | `erase!(d, k)` |
| Size | `d.size()` |
| Keys / values | `d.keys()`, `d.values()` |
| Update with function | `dictUpdate!(d, f, keys, params)` |
| Merge | `d.append!(d2)` |
| Thread-safe | `syncDict(...)` |
| Ordered | `dict(keys, values, true)` |
| → table | `table(d)` (values must be same-length vectors) |

## See also

- `../../reference/functions/by-name/d/dict.md` — full upstream reference.
- `../../reference/functions/by-name/d/dictUpdate_.md` — `dictUpdate!`.
- `../../reference/functions/by-name/s/syncDict.md` — thread-safe variant.
- `data-forms.md` — other data forms (vector, matrix, table, tuple).
- `operators.md` — in-place `!` operators.
