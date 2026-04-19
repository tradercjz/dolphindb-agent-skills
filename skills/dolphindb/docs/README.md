# docs/ — DolphinDB documentation

A merged tree of **hand-authored trap/overview guides** and **auto-mirrored
upstream reference pages**. They coexist flatly per directory; each
auto-mirrored file begins with an `<!-- Auto-mirrored from upstream ... -->`
marker comment.

## Directory naming convention

Two styles coexist on purpose:

- **Numeric-prefixed** (`10-language/`, `20-sql/`, …, `90-admin/`) —
  the **learning-path / core knowledge stack**. Digits force a
  progression-friendly order in the file tree (language → SQL →
  database → streaming → ingestion → API → perf → admin) instead of
  alphabetic. Gaps (80) are reserved for future insertion.
- **Name-only** (`backtest/`, `plugins/`, `tutorials/`, `modules/`,
  `mcp/`, `deploy/`, `release-notes/`, `about/`, `getstarted/`) —
  **vertical reference areas** that do not belong on the learning
  ladder. They are looked up by topic, not read in order.

Rule of thumb: **if a newcomer would read it as part of "how to learn
DolphinDB end-to-end", it gets a number. Otherwise it stays named.**

This split is agent-friendly: the numbered areas match the routing
table in `../SKILL.md`; the named areas are surfaced by the
"cross-cutting" and "any specific plugin / tutorial" rows.

## Entry points (read first)

- `00-overview.md`  — what DolphinDB is, node types, storage engines.
- `01-quickstart.md` — install → connect → first DFS table → first query.

## Numbered functional areas

- `10-language/` — DolphinDB script language. Key hand-authored: `data-types`, `data-forms`, **`dict`**, `operators`, `functions`, `metaprogramming`. ~140 md.
- `20-sql/`      — SQL dialect + keyword reference. Key: **`context-by`**, **`pivot-by`**, `joins-overview`, `select-where`. ~70 md.
- `30-database/` — DFS databases, partitioning, storage engines. Key: **`partitioning`**, `tsdb-engine`, `pkey-engine`. ~30 md.
- `40-streaming/` — stream tables, subscriptions, engines, CEP, replay. Key: **`subscribe`**, `engines`, `cep-overview`. ~70 md.
- `50-ingestion/` — CSV / Parquet / HDF5 / Kafka / MQTT ingest. ~20 md.
- `60-api/`      — Python / Java / C++ APIs, type mapping, client tools. Key: `python-api`, **`type-mapping`**. ~30 md.
- `70-perf/`     — performance & tuning. Key: **`partition-pruning`**, `memory-threading`. 4 md.
- `90-admin/`    — cluster ops, backup, security + `cfg/` (configuration parameters) + `omc/` (O&M troubleshooting). ~22 md.

## Cross-cutting areas

- `backtest/`      — **strategy backtest & simulated matching**. Hub at `backtest/README.md`; guides for plugin / matching engine / assets / factors / traps / tutorials index.
- `tutorials/`     — 281 runnable end-to-end case studies. Navigation at `tutorials/README.md`.
- `plugins/`       — 70+ plugin manuals. Navigation at `plugins/README.md`; one-line catalog at `../reference/plugins-catalog.md`.
- `modules/`       — 10 built-in script modules (`ta`, `wq101alpha`, `gtja191Alpha`, `mytt`, `MarketHoliday`, …). Navigation at `modules/README.md`.
- `deploy/`        — deployment / license.
- `mcp/`           — DolphinDB MCP (Model Context Protocol).
- `release-notes/` — Server / API / plugin version history.
- `about/`         — product overview page.
- `getstarted/`    — upstream getting-started chapter.
- `backtest/` entry file `backtest_intro.md` — upstream short intro.

## Identifying generated vs hand-authored

**Generated (safe to delete on rebuild):** first non-blank line starts with
`<!-- Auto-mirrored from upstream ...`.

**Hand-authored (never auto-touched):** no such marker. The whitelist is
documented in `../SKILL.md` → Maintenance section.

Rebuild the generated portion with:

```powershell
python ../scripts/build_from_docs.py
```
