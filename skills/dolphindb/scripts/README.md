# scripts/

Two scripts: one for maintainers, one for the agent/user at runtime.

## `lookup.py` — runtime lookup CLI (used by the agent)

Fast, bounded-output lookup into the reference tree. Prefer this over
grepping the large INDEX files.

```bash
# Look up a runtime error by RefId
python skills/dolphindb/scripts/lookup.py error S00012

# Read a built-in function reference
python skills/dolphindb/scripts/lookup.py fn mavg

# List all functions with a prefix
python skills/dolphindb/scripts/lookup.py fn --list-prefix mav

# Read the curated starter pages for a topic keyword
python skills/dolphindb/scripts/lookup.py topic backtest
python skills/dolphindb/scripts/lookup.py topic "stream python"
```

Exit codes: 0 success, 1 no match, 2 usage error. No external deps —
pure stdlib.

## `build_from_docs.py` — maintainer regeneration

Regenerates the auto-mirrored portion of `docs/` and the whole
`reference/` tree from `documentation-main/`. Preserves hand-authored
files via a marker comment.

### Obtaining `documentation-main/`

Not committed to this repo (`.gitignore`d). Maintainers fetch it fresh
from the upstream DolphinDB documentation repository before rebuilding:

```powershell
# From repo root
git clone --depth=1 https://github.com/dolphindb/documentation.git documentation-main
# (or download the upstream archive and extract to `documentation-main/`)
```

The mirrored content under `skills/dolphindb/docs/` and
`skills/dolphindb/reference/` is self-contained at runtime — agents and
`lookup.py` never read `documentation-main/`, only maintainers running
this script do.

```powershell
# From repo root
python skills/dolphindb/scripts/build_from_docs.py

# Regenerate only docs/ (skip reference/ rebuild)
python skills/dolphindb/scripts/build_from_docs.py --only docs
```

Re-run whenever `documentation-main/` is updated upstream.
