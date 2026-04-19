# Cross-language type mapping

Reference for converting values between DolphinDB, Python, Java, C++, JDBC.

## Scalars

| DolphinDB | Python | Java | C++ | JDBC (SQL type) |
|-----------|--------|------|-----|-----------------|
| `BOOL`    | `bool`    | `boolean` / `Boolean` | `char`  | `BIT` |
| `CHAR`    | `int`     | `byte`    | `char`    | `TINYINT` |
| `SHORT`   | `int`     | `short`   | `short`   | `SMALLINT` |
| `INT`     | `int`     | `int`     | `int`     | `INTEGER` |
| `LONG`    | `int`     | `long`    | `long long` | `BIGINT` |
| `FLOAT`   | `float`   | `float`   | `float`   | `REAL` |
| `DOUBLE`  | `float`   | `double`  | `double`  | `DOUBLE` |
| `DECIMAL32/64/128` | `decimal.Decimal` | `BigDecimal` | `Decimal32/64/128` | `DECIMAL` |
| `STRING`  | `str`     | `String`  | `std::string` | `VARCHAR` |
| `SYMBOL`  | `str` (categorical-ish) | `String` | `std::string` | `VARCHAR` |
| `UUID` / `INT128` | `str` (hex) | `String` | `Guid`/`Int128` | `VARCHAR` |
| `BLOB`    | `bytes`   | `byte[]`  | `std::string` | `BINARY` |
| `DATE`    | `datetime.date` | `LocalDate` | `int` (days) | `DATE` |
| `MONTH`   | `int` (YYYYMM) | `YearMonth` | `int` | `INTEGER` |
| `TIME`    | `datetime.time` | `LocalTime` | `int` (ms) | `TIME` |
| `MINUTE`  | `datetime.time` | `LocalTime` | `int` | `TIME` |
| `SECOND`  | `datetime.time` | `LocalTime` | `int` | `TIME` |
| `DATETIME`| `datetime.datetime` (s) | `LocalDateTime` | `int` (s) | `TIMESTAMP` |
| `TIMESTAMP`| `datetime.datetime` (ms) / `pandas.Timestamp` | `LocalDateTime` | `long long` (ms) | `TIMESTAMP` |
| `NANOTIMESTAMP` | `pandas.Timestamp` (ns) | `LocalDateTime` | `long long` (ns) | `TIMESTAMP` |
| `NANOTIME`| `datetime.time` (ns) | `LocalTime` | `long long` | `TIME` |
| `DATEHOUR`| `datetime.datetime` (hour) | `LocalDateTime` | `int` | `TIMESTAMP` |
| `POINT`   | `tuple(float,float)` | `double[2]` | `struct` | — |
| `IPADDR`  | `str` | `String` | `string` | `VARCHAR` |
| `COMPLEX` | `complex` | `double[2]` | `complex<double>` | — |

## Vectors → columns

| DolphinDB vector | Python |
|------------------|--------|
| INT / LONG vector | `numpy.ndarray` dtype `int32` / `int64` |
| DOUBLE vector     | `numpy.ndarray` `float64` |
| BOOL vector       | `numpy.ndarray` `bool` or `int8` |
| SYMBOL/STRING vector | `numpy.ndarray` `object` (Python str) |
| TIMESTAMP vector  | `numpy.ndarray` `datetime64[ns]` |
| NANOTIMESTAMP vector | `numpy.ndarray` `datetime64[ns]` |
| DATE vector       | `numpy.ndarray` `datetime64[D]` |

## Tables

Always a `pandas.DataFrame` in Python; `BasicTable` in Java; `TableSP` in C++.
Column dtypes follow the vector table above.

## Null handling

| DolphinDB null | Python | Pitfall |
|----------------|--------|---------|
| INT null | the smallest int (-2^31) | `numpy.nan` is FLOAT; casting int column to float replaces null sentinel with NaN silently. Use pandas nullable `Int64` to preserve. |
| DOUBLE null | `numpy.nan` | |
| STRING null | `""` (empty string) by default, or `None` with session option `convertNullToNone=True` | |
| DATE / TIMESTAMP null | `pandas.NaT` | |
| BOOL null | cast to int8; 0/1/null → -128 sentinel | |

## Uploading pandas DataFrame

Auto-mapping rules (uploading `df` with `s.upload({"t": df})`):

- Numeric → DolphinDB numeric of same width.
- `object` column with strings → `STRING` (not `SYMBOL`). Convert to
  SYMBOL on the server: `t = select sym, symbol(sym) as sym, ... from t`.
- `datetime64[ns]` → `NANOTIMESTAMP` (unless precision can be reduced).
- pandas `Int64` (nullable) → DolphinDB `LONG` with proper null handling.

## Traps

- **SYMBOL vs STRING round-trip.** Uploading a DataFrame creates STRING
  columns; to join fast on the server, cast to SYMBOL explicitly.
- **Timezone.** DolphinDB stores naive times. Python `datetime.datetime`
  with `tzinfo` is converted to **UTC** before upload. Strip tz with
  `df["ts"] = df["ts"].dt.tz_localize(None)` if you want wall-clock.
- **Decimal precision.** Python `Decimal` → DECIMAL32/64/128 depends on
  value magnitude; force with `s.run("decimal64(py_dec, 6)")`.
- **Arrow protocol** (`PROTOCOL_ARROW`) skips most conversions and is
  fastest for wide DataFrames, but requires `pyarrow` on both ends.

## See also

- `python-api.md`, `java-api.md`, `cpp-api.md`.
- `connapi_intro.md` — upstream API overview.
