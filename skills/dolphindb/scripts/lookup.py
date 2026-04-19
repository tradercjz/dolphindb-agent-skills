#!/usr/bin/env python3
"""Lookup CLI for DolphinDB skill reference pages.

Usage:
    python scripts/lookup.py error S00012
    python scripts/lookup.py fn mavg
    python scripts/lookup.py fn --list-prefix mav
    python scripts/lookup.py topic backtest

Designed for AI agents and humans: returns the raw markdown of the
matching reference page, or a short candidate list when ambiguous.
Exit code 0 on success, 1 on no match, 2 on usage error.

Why this exists: the function and error-code indexes are large. Grepping
them repeatedly wastes tokens. This script gives a one-shot lookup with
bounded output.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REF_ROOT = SKILL_ROOT / "reference"
DOCS_ROOT = SKILL_ROOT / "docs"


def _die(msg: str, code: int = 1) -> "None":
    print(msg, file=sys.stderr)
    sys.exit(code)


def _print_file(path: Path, max_bytes: int | None = None) -> None:
    data = path.read_text(encoding="utf-8", errors="replace")
    if max_bytes and len(data) > max_bytes:
        data = data[:max_bytes] + f"\n\n... [truncated at {max_bytes} bytes; full file: {path.relative_to(SKILL_ROOT)}]"
    print(data)


# ---------------------------------------------------------------------- error
def lookup_error(ref_id: str) -> int:
    ref_id = ref_id.strip().upper()
    m = re.match(r"^(?:REFID[:\s]*)?(S\d{5})$", ref_id)
    if not m:
        _die(f"error: bad RefId '{ref_id}'. expected e.g. S00012", 2)
    code = m.group(1)
    p = REF_ROOT / "error-codes" / f"{code}.md"
    if not p.exists():
        _die(f"error: {code} not found in reference/error-codes/")
    _print_file(p)
    return 0


# -------------------------------------------------------------------- function
def _fn_path(name: str) -> Path | None:
    if not name or not name[0].isalpha():
        return None
    p = REF_ROOT / "functions" / "by-name" / name[0].lower() / f"{name}.md"
    return p if p.exists() else None


def _fn_candidates(prefix: str, limit: int = 40) -> list[str]:
    prefix = prefix.lower()
    if not prefix or not prefix[0].isalpha():
        return []
    bucket = REF_ROOT / "functions" / "by-name" / prefix[0]
    if not bucket.is_dir():
        return []
    out: list[str] = []
    for f in sorted(bucket.iterdir()):
        if f.suffix == ".md" and f.stem.lower().startswith(prefix):
            out.append(f.stem)
            if len(out) >= limit:
                break
    return out


def lookup_fn(arg: str, list_prefix: bool = False) -> int:
    arg = arg.strip()
    if list_prefix:
        cands = _fn_candidates(arg)
        if not cands:
            _die(f"no functions with prefix '{arg}'")
        print(f"{len(cands)} function(s) with prefix '{arg}':")
        print("\n".join(f"  {c}" for c in cands))
        return 0

    p = _fn_path(arg)
    if p:
        _print_file(p)
        return 0

    # exact miss: show prefix candidates
    cands = _fn_candidates(arg[:3] if len(arg) >= 3 else arg)
    if cands:
        close = [c for c in cands if arg.lower() in c.lower()][:20]
        if close:
            print(f"no exact match for '{arg}'. did you mean:", file=sys.stderr)
            for c in close:
                print(f"  {c}", file=sys.stderr)
            return 1
    _die(f"function '{arg}' not found under reference/functions/by-name/")


# ------------------------------------------------------------------------ topic
TOPIC_MAP = {
    # trigger -> list of (relpath from skills/dolphindb) in suggested read order
    "backtest":   ["docs/backtest/README.md", "docs/backtest/backtest-plugin-guide.md",
                   "docs/backtest/traps.md", "docs/backtest/factors.md"],
    "factor":     ["docs/backtest/factors.md", "docs/modules/README.md"],
    "stream":     ["docs/40-streaming/engine-selection.md",
                   "docs/40-streaming/subscribe.md", "docs/40-streaming/stream-table.md"],
    "partition":  ["docs/30-database/partitioning.md", "docs/70-perf/partition-pruning.md"],
    "slow":       ["docs/70-perf/slow-query-diagnosis.md"],
    "jit":        ["docs/70-perf/jit-guide.md"],
    "python":     ["docs/60-api/python-api.md", "patterns/python-roundtrip-type-safety.md",
                   "docs/60-api/type-mapping.md"],
    "asof":       ["docs/20-sql/asof-join.md", "patterns/asof-join-quotes-trades.md"],
    "null":       ["docs/10-language/null-handling.md"],
    "time":       ["docs/10-language/time-types.md"],
    "context-by": ["docs/20-sql/context-by.md"],
    "dict":       ["docs/10-language/dict.md"],
    "error":      ["docs/10-language/error-handling.md", "reference/error-codes/INDEX.md"],
    "plugin":     ["docs/plugins/README.md"],
    "tutorial":   ["docs/tutorials/README.md"],
    "module":     ["docs/modules/README.md"],
    "schedule":   ["patterns/scheduled-job-template.md"],
    "recovery":   ["patterns/stream-recovery-after-restart.md"],
    "web":        ["docs/90-admin/web/README.md"],
    "console":    ["docs/90-admin/web/README.md"],
    "ide":        ["docs/60-api/vscode.md", "docs/60-api/jupyter.md", "docs/60-api/gui.md"],
    "vscode":     ["docs/60-api/vscode.md"],
    "jupyter":    ["docs/60-api/jupyter.md"],
    "cluster":    ["docs/90-admin/cluster.md", "docs/90-admin/ha.md"],
    "acl":        ["docs/90-admin/security.md", "docs/90-admin/web/access_man.md"],
    "backup":     ["docs/90-admin/backup-restore.md"],
    "cheatsheet": ["docs/cheatsheet.md"],
    "funcs-by-topic": ["reference/functions/funcs_by_topics.md"],
}


def lookup_topic(q: str) -> int:
    q = q.strip().lower()
    matches = [k for k in TOPIC_MAP if k in q or q in k]
    if not matches:
        print("known topics:", file=sys.stderr)
        for k in sorted(TOPIC_MAP):
            print(f"  {k}", file=sys.stderr)
        return 1
    # Flatten unique paths preserving order
    seen: set[str] = set()
    paths: list[str] = []
    for k in matches:
        for p in TOPIC_MAP[k]:
            if p not in seen:
                seen.add(p)
                paths.append(p)
    for rel in paths:
        full = SKILL_ROOT / rel
        if not full.exists():
            continue
        print(f"\n===== {rel} =====\n")
        _print_file(full, max_bytes=20_000)
    return 0


# --------------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="lookup",
        description="DolphinDB skill lookup CLI. Emits raw markdown of the matching reference page.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("error", help="look up a runtime error by RefId, e.g. S00012")
    pe.add_argument("ref_id")

    pf = sub.add_parser("fn", help="look up a built-in function reference page")
    pf.add_argument("name")
    pf.add_argument("--list-prefix", action="store_true",
                    help="treat 'name' as a prefix and list matches instead of reading one page")

    pt = sub.add_parser("topic", help="read the curated starter pages for a topic keyword")
    pt.add_argument("query", help="e.g. backtest, stream, python, factor, null, time, ...")

    args = parser.parse_args()
    if args.cmd == "error":
        return lookup_error(args.ref_id)
    if args.cmd == "fn":
        return lookup_fn(args.name, list_prefix=args.list_prefix)
    if args.cmd == "topic":
        return lookup_topic(args.query)
    return 2


if __name__ == "__main__":
    sys.exit(main())
