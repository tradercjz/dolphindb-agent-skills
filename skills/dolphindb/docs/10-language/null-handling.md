# NULL handling — typed nulls, `isValid`, and the `0` trap

## Contents
- Sentinels (per-type null literals)
- Testing with `isValid`
- Filling / replacing (`nullFill`, `ffill`, `coalesce`, `interpolate`)
- The `0` trap on integer nulls
- `count(*)` vs `count(col)`
- Null in joins / `context by` windows / type conversions / CSV load
- Checklist


DolphinDB NULLs are **per-type** and represented by **sentinel values**,
not a separate `NULL` state like in SQL databases. This causes four
characteristic bugs.

## Sentinels

| Type | NULL literal | Sentinel value |
|------|-------------|---------------|
| `BOOL`    | `00b`   | — |
| `CHAR`    | `00c`   | `-128` |
| `SHORT`   | `00h`   | `-32768` |
| `INT`     | `00i`   | `-2147483648` |
| `LONG`    | `00l`   | `-9223372036854775808` |
| `FLOAT`   | `00f`   | `-3.4028235e+38` (sort of — uses NaN pattern) |
| `DOUBLE`  | `00F`   | IEEE NaN |
| `STRING`  | `""` or `string(NULL)` | empty string |
| `SYMBOL`  | `""`    | empty symbol |
| `DATE` / `TIMESTAMP` / ... | `00d`, `00p`, ... | same int sentinel as underlying |

`NULL` alone (untyped) defaults to `VOID`. Avoid untyped `NULL` in
expressions — annotate with `int(NULL)` etc.

## Test with `isValid`

```dolphindb
isValid(x)        // true when x is NOT null
isNull(x)         // alias of !isValid(x)
```

**Never** write `x == NULL` — that compares two sentinels and may return
true or false based on accident. Always `isValid(x)`.

## Filling / replacing

```dolphindb
nullFill(x, 0)                    // replace NULL with 0
nullFill!(t, 0)                   // in-place, whole table
ffill(x)                          // forward-fill NULL from previous valid
bfill(x)                          // backward-fill
interpolate(x)                    // linear interpolate

coalesce(a, b, c)                 // first non-null of a, b, c
iif(isValid(x), x, defaultValue)  // explicit form
```

For rolling / reactive / factor compute, **always `nullFill` or `ffill`
your input** before windowing; `mavg(5)` etc. propagate nulls.

## The `0` trap

Because `INT` null is a sentinel, this SILENTLY counts nulls:

```dolphindb
sum(x)            // includes null sentinels? No — engine treats isValid()==false as skip
                  // BUT:
sum(x + 1)        // null + 1 = null, so OK
sum(iif(x > 0, 1, 0))     // x == 00i is NOT > 0, so 0. OK.
sum(iif(x, 1, 0))         // BAD: treats non-zero as true, but 00i is nonzero → counts nulls as true
```

Rule: aggregations (`sum`, `avg`, `max`, `min`, `count`) all treat nulls
correctly. Hand-rolled boolean tests on integers are where it breaks —
always go through `isValid`.

## `count(*)` vs `count(col)`

| Expression | What it counts |
|------------|---------------|
| `count(*)`   | rows in the group |
| `count(col)` | rows where `col` is not null |

Useful for coverage: `count(price) / count(*)` is the non-null ratio.

## Null in joins

```dolphindb
// inner join on sym=sym
select * from ej(left, right, `sym)
```

If `left.sym` or `right.sym` is null, **those rows never match** — even
to each other. SQL-standard behavior, but easy to forget. For outer
joins (`lj`, `fj`, `sj`), null keys in the driving table produce null
rights.

For `asof join` (`aj`): if the left timestamp is null, the result right
columns are null.

## Null in `context by` windows

```dolphindb
select sym, ts, mavg(price, 5) as ma5
from t
context by sym csort ts
```

If `price` has a null in the window, the whole window returns null (the
default `mavg` drops all nulls — check `help(mavg)` for each function).
To be explicit:

```dolphindb
select sym, ts, mavg(nullFill(price, 0.0), 5) as ma5    // or ffill
from t context by sym csort ts
```

## Null in type conversions

```dolphindb
int("abc")         // 00i (null int) — silent, not an error
double("abc")      // 00F
temporalParse("bad", "yyyy.MM.dd")   // 00d
```

Always `count(isValid(...))` after a bulk cast from strings.

## Saving / loading CSV

```dolphindb
loadText("/tmp/a.csv", schema=schema, skipRows=0)
// Empty fields → null of the column type. Good default.
// But "NULL", "NA", "-" strings are NOT recognized → become 0 or "NULL" string.
```

Cleanup after load:

```dolphindb
update t set price = NULL where price_str == "NA"
update t set price = double(price_str) where isValid(double(price_str))
```

## Checklist

- [ ] Use `isValid(x)`, never `x == NULL`.
- [ ] `nullFill` / `ffill` input before rolling windows.
- [ ] After string→numeric casts, verify `count(isValid(x))`.
- [ ] Join keys: confirm no null sym/ts if result looks short.
- [ ] `count(col)` != `count(*)` when null-bearing.

## See also

- `data-types.md`, `data-forms.md`, `time-types.md`.
- `reference/functions/INDEX.md` — lookup `isValid`, `nullFill`, `ffill`,
  `coalesce`, `interpolate`.
