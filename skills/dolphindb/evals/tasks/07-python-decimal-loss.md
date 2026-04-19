# 07 — Python roundtrip loses DECIMAL precision

**Tags:** api, python
**Difficulty:** medium
**Reference doc:** `patterns/python-roundtrip-type-safety.md`,
`docs/60-api/type-mapping.md`

## Prompt

I store prices as `DECIMAL32(4)` in DolphinDB. In Python I pull them,
multiply by volume, and write back. But occasional rows come back with
values like `15.4399999...` instead of `15.4400`. What's going on, how
to fix?

## Rubric

- [ ] Identifies that the default Python path
      (`session.run(...)`) materializes DECIMAL as `float64`, which cannot
      represent most decimal fractions exactly.
- [ ] Switches to the **Arrow path** (`session.runArrow`) to preserve
      DECIMAL as `decimal128`, or explicitly casts server-side with
      `decimal32(col, 4)` before append.
- [ ] Mentions `ArrowDtype` (`types_mapper=pd.ArrowDtype`) for pandas
      to keep decimal/integer/null fidelity.
- [ ] (Bonus) Notes that `tableAppender` works but still requires a
      DataFrame whose column types match the DolphinDB schema.

## Expected artifact (minimum)

```python
df = s.runArrow("select * from loadTable('dfs://tick', `trade) "
                "where date = 2024.03.15")
pdf = df.to_pandas(types_mapper=pd.ArrowDtype)
# pdf["px"].dtype == decimal128[pyarrow](9, 4)

# compute, then push back with explicit cast
s.upload({"payload": pdf})
s.run("""
    loadTable('dfs://tick', `trade).append!(
        select nanotimestamp(ts) as ts, symbol(sym) as sym,
               decimal32(px, 4) as px, long(vol) as vol
        from payload)
""")
```

## Anti-patterns

- "Just round to 4 decimals in Python" — masks the symptom, still lossy.
- Casting the Python column to `Decimal` manually, then uploading —
  works but slow; Arrow path is better.
- Keeping `float64` and accepting the drift.
