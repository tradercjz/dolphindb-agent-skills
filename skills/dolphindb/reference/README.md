# reference/ — structured lookups

Machine-friendly reference data. Most of this is **generated** by
`scripts/build_from_docs.py` from the upstream documentation mirror.
Do not edit generated files by hand; re-run the build script instead.

- `functions/INDEX.md`            — master function catalog (by theme)
- `functions/by-theme/*.md`       — functions grouped by topic, with signatures + short examples
- `functions/by-name/*.md`        — (optional) one page per function, lifted from `funcs/<letter>/<name>.md`
- `error-codes/INDEX.md`          — all DolphinDB RefId error codes, with a 1-line summary
- `error-codes/Sxxxxx.md`         — full page per error code (报错信息 / 错误原因 / 解决办法)
- `plugins-catalog.md`            — one-line summary per plugin
