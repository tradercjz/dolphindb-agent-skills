# Data types

DolphinDB has a compact set of primitive types, all strongly-typed and
vectorizable.

## Numeric

| Type | Size | Literal | Range |
|------|------|---------|-------|
| `BOOL`   | 1 | `true` / `false` | |
| `CHAR`   | 1 | `'a'`, `12c`     | -128..127 |
| `SHORT`  | 2 | `42h`            | -32768..32767 |
| `INT`    | 4 | `42`, `42i`      | ~±2.1×10^9 |
| `LONG`   | 8 | `42l`            | ~±9.2×10^18 |
| `FLOAT`  | 4 | `3.14f`          | IEEE-754 |
| `DOUBLE` | 8 | `3.14`           | default float |
| `DECIMAL32(s)`  | 4  | `decimal32(3.14, 2)`  | fixed-point, scale s |
| `DECIMAL64(s)`  | 8  | `decimal64(...)`      | |
| `DECIMAL128(s)` | 16 | `decimal128(...)`     | |

Integer-literal suffixes: `c` (CHAR), `h` (SHORT), `i` (INT), `l` (LONG).
Float-literal suffix: `f` (FLOAT).

## Time

| Type | Format | Example |
|------|--------|---------|
| `DATE` | `YYYY.MM.DD` | `2024.01.01` |
| `MONTH` | `YYYY.MMM` | `2024.01M` |
| `TIME`  | `HH:mm:ss.SSS` | `09:30:00.000` |
| `MINUTE` | `HH:mm` | `09:30m` |
| `SECOND` | `HH:mm:ss` | `09:30:00` |
| `DATETIME` | `YYYY.MM.DDTHH:mm:ss` | `2024.01.01T09:30:00` |
| `TIMESTAMP` | `...SSS` (ms) | `2024.01.01T09:30:00.000` |
| `NANOTIMESTAMP` | `...SSSSSSSSS` (ns) | `2024.01.01T09:30:00.000000000` |
| `NANOTIME` | `HH:mm:ss.NNNNNNNNN` | `09:30:00.123456789` |
| `DATEHOUR` | `YYYY.MM.DDTHH` | `2024.01.01T09` |

**Literals are unquoted.** `"2024-01-01"` is a string; use `date("2024-01-01")`
to convert.

## Text

| Type | Notes |
|------|-------|
| `STRING` | Variable-length, UTF-8. |
| `SYMBOL` | Dictionary-encoded string (fast for columns with repeated values). Literal: `` `AAPL ``. |
| `BLOB`   | Binary bytes. |
| `UUID` / `INT128` | 128-bit binary ids. |

**Symbol vs string**: `` `AAPL `` is SYMBOL; `"AAPL"` is STRING. Use SYMBOL
for columns with limited cardinality — it stores as int under the hood and
speeds up joins and filters.

## Composite (see `data-forms.md`)

- `ARRAY VECTOR` — variable-length nested array per row (e.g. an array of
  depth levels per tick).
- `TENSOR` — n-dimensional arrays for ML.
- `COMPLEX` — 2 doubles.
- `POINT`, `IPADDR`.

## Nullability

- Every type has a **null sentinel**. `NULL` is polymorphic in script:
  `00i` / `00l` are int/long nulls (also written `int()`, `long()`).
- Do **not** compare with `= NULL`; use `isNull(x)` / `isValid(x)`.
- Numeric nulls are represented by the minimum value of the type. Arithmetic
  with null → null.

## Casting

```dolphindb
int("42")            // -> 42
double(42l)          // -> 42.0
date("2024-01-01")   // -> 2024.01.01
symbol("AAPL")       // -> `AAPL
string(2024.01.01)   // -> "2024.01.01"
cast(x, DOUBLE)      // generic cast
```

## Type introspection

```dolphindb
type(x)        // -> int code (see ``form`` / ``type`` )
typestr(x)     // -> "INT", "DOUBLE", ...
form(x)        // scalar / vector / matrix / table / dict / ...
schema(t)      // for tables
```

## Traps

- **Integer overflow** is silent — 32-bit INT wraps. Use LONG for counters.
- **DECIMAL scale** is part of the type — adding DECIMAL32(2) and
  DECIMAL32(3) requires explicit `cast`.
- **`cast(x, SYMBOL)` on a high-cardinality column** can blow the symbol
  dictionary (`S00003`).
- **Python `None`** uploaded from API becomes DolphinDB null; Python
  `numpy.nan` in a non-float column will fail to upload.

## See also

- `data_types.md`, `data_types_forms/*.md`.
- `../60-api/type-mapping.md` for cross-language type conversion.
