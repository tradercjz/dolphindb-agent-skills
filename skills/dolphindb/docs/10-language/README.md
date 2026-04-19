# 10-language — DolphinDB script language

## Hand-authored

- `data-types.md`       — scalar types, literals, nullability.
- `data-forms.md`       — scalar, pair, vector, matrix, table, set, dict, tuple, tensor.
- `dict.md`             ★ dict cheat-sheet: creation, `ANY` values, `syncDict`, common mistakes.
- `time-types.md`       ★ 10 time types — DATE/TIMESTAMP/NANOTIMESTAMP/…, conversions, partition-key choices, timezone, join-empty trap.
- `null-handling.md`    ★ typed sentinels, `isValid`, `nullFill`/`ffill`, rolling-window propagation, CSV load pitfalls.
- `error-handling.md`   — `try/catch`, RefIds, `submitJob` errors, streaming poison-pill, client-side parity.
- `operators.md`        ★ `=` vs `==`, in-place `!`, `<-`, partial `{}`.
- `control-flow.md`     — `if`, `for`, `do..while`, `try..catch`, `break/continue`.
- `functions.md`        — named / anonymous / lambda / higher-order / partial.
- `metaprogramming.md`  — metacode, `sqlCol`, `makeCall`, `sql()`.
- `modules.md`          — `module`, `use`, file layout.

## Full upstream reference pages

Under `` (from `progr/`, except `progr/sql/` which lives in `20-sql/`).

Key files:

| Topic | File |
|-------|------|
| Overview | `progr_intro.md`, `lang_intro.md` |
| Types | `data_types.md`, `data_types_forms/*.md` |
| Forms | `data_forms.md`, `tensor.md` |
| Operators | `operators/*.md` |
| Statements | `statements/*.md` |
| Functions | `named_func.md`, `anonym_func.md`, `lambda.md`, `partial_app.md`, `func_progr.md` |
| OOP | `oop.md`, `class_objects.md`, `inheritance.md`, `member_function.md`, `constructor.md` |
| Metaprogramming | `metaProgr_func.md`, `macrovariations.md` |
| Data manipulation | `data_mani/*.md` |
| File I/O | `file_io/*.md` |
| Utility | `utility.md`, `application.md`, `attributes.md`, `closure.md`, `rfc.md` |
| Objects | `objs/*.md` |
