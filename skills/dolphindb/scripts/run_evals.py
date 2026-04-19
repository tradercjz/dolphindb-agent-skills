#!/usr/bin/env python3
"""Eval harness for the DolphinDB skill.

Measures skill effectiveness via three modes:

  1. list            dump every task's prompt (for piping into your agent)
  2. grade   FILE    score one response against one task
  3. battery DIR     score a directory of responses (one file per task)
                     and emit a battery-level report (battery_score,
                     per-task scores, anti-pattern rate).

The grader is **text-based**, not an LLM judge. It scans each agent
response for:

  - required keywords / regex patterns derived from the task's rubric
  - anti-pattern keywords that should NOT appear
  - presence of the expected artifact's core construct

Per-task score = (rubric_hits / rubric_total) with a -0.3 cap-penalty
if any anti-pattern is emitted. Output is a single JSON object for easy
piping.

Usage
-----
    # 1. dump all prompts (one file per task)
    python scripts/run_evals.py list --out evals/prompts

    # 2. run your agent against each prompt, save responses to evals/runs/<tag>/
    #    e.g. claude -p "$(cat evals/prompts/01-context-vs-group-by.txt)" \
    #              > evals/runs/sonnet-skill-on/01-context-vs-group-by.txt

    # 3. grade the whole battery
    python scripts/run_evals.py battery evals/runs/sonnet-skill-on \
        --baseline evals/runs/sonnet-skill-off

Exit codes: 0 ok, 1 battery below baseline, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = SKILL_ROOT / "evals" / "tasks"


# --------------------------------------------------------------------- parsing
_SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_BULLET_RE = re.compile(r"^-\s*\[\s\]\s+(.+?)$", re.MULTILINE)
_ANTI_BULLET_RE = re.compile(r"^-\s+(.+?)$", re.MULTILINE)


@dataclass
class Task:
    id: str
    path: Path
    prompt: str
    rubric: list[str] = field(default_factory=list)
    anti: list[str] = field(default_factory=list)
    expected: str = ""

    @classmethod
    def load(cls, path: Path) -> "Task":
        text = path.read_text(encoding="utf-8")
        # Split into sections by ##
        sections: dict[str, str] = {}
        matches = list(_SECTION_RE.finditer(text))
        for i, m in enumerate(matches):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sections[m.group(1).strip().lower()] = text[start:end].strip()

        rubric_items = _BULLET_RE.findall(sections.get("rubric", ""))
        anti_items = _ANTI_BULLET_RE.findall(sections.get("anti-patterns", ""))

        return cls(
            id=path.stem,
            path=path,
            prompt=sections.get("prompt", "").strip(),
            rubric=[r.strip() for r in rubric_items],
            anti=[a.strip() for a in anti_items],
            expected=sections.get("expected artifact (minimum)", "").strip(),
        )


def load_tasks() -> list[Task]:
    return [Task.load(p) for p in sorted(TASKS_DIR.glob("*.md"))]


# --------------------------------------------------------------------- grading
# Simple rubric → keyword-pattern extractor. Looks for backticked tokens
# (strong signal) and falls back to a loose phrase match.
_BACKTICK_RE = re.compile(r"`([^`]+)`")


def _rubric_keywords(item: str) -> list[str]:
    """Extract the identifiers we expect to find in a passing response."""
    ticks = _BACKTICK_RE.findall(item)
    # Filter out noisy generic tokens
    keep = [t for t in ticks if len(t) >= 2 and not t.startswith("as ")]
    return keep


def _matches(response: str, needles: list[str]) -> bool:
    """True if ANY needle is present in response (case-insensitive)."""
    if not needles:
        return False
    r = response.lower()
    return any(n.lower() in r for n in needles)


def _rubric_score(item: str, response: str) -> float:
    """Score a single rubric bullet: 1.0 full, 0.5 partial, 0.0 miss."""
    kws = _rubric_keywords(item)
    if kws:
        hits = sum(1 for k in kws if k.lower() in response.lower())
        if hits == len(kws):
            return 1.0
        if hits > 0:
            return 0.5
        return 0.0
    # No strong anchors — fall back to a loose phrase search
    phrase = re.sub(r"[^\w\s]", " ", item).lower().strip()
    tokens = [t for t in phrase.split() if len(t) > 4][:3]
    if tokens and all(t in response.lower() for t in tokens):
        return 0.5  # lexical-only match, cap at partial
    return 0.0


def _anti_hits(task: Task, response: str) -> list[str]:
    """Detect anti-patterns. We only match the FIRST backticked token in each
    bullet — that is conventionally the wrong construct itself (e.g.
    ``order by sym, ts``), while later backticks often reference correct
    constructs for contrast (e.g. ``in place of `csort```) which would
    otherwise trigger false positives."""
    triggered: list[str] = []
    resp_low = response.lower()
    for a in task.anti:
        kws = _rubric_keywords(a)
        if not kws:
            continue
        primary = kws[0]
        if primary.lower() in resp_low:
            triggered.append(a)
    return triggered


@dataclass
class TaskResult:
    id: str
    rubric_total: int
    rubric_hits: float
    anti_triggered: list[str]
    score: float  # in [0, 1]

    @classmethod
    def grade(cls, task: Task, response: str) -> "TaskResult":
        per = [_rubric_score(item, response) for item in task.rubric]
        total = len(task.rubric) or 1
        hits = sum(per)
        base = hits / total
        anti = _anti_hits(task, response)
        score = max(0.0, base - 0.3 * (1 if anti else 0))
        return cls(
            id=task.id,
            rubric_total=total,
            rubric_hits=round(hits, 2),
            anti_triggered=anti,
            score=round(score, 3),
        )


# ---------------------------------------------------------------------- modes
def cmd_list(out_dir: Path | None) -> int:
    tasks = load_tasks()
    if out_dir is None:
        for t in tasks:
            print(f"\n===== {t.id} =====\n")
            print(t.prompt)
        return 0
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in tasks:
        (out_dir / f"{t.id}.txt").write_text(t.prompt + "\n", encoding="utf-8")
    print(f"wrote {len(tasks)} prompts to {out_dir}", file=sys.stderr)
    return 0


def cmd_grade(response_path: Path, task_id: str | None) -> int:
    tasks = {t.id: t for t in load_tasks()}
    # Infer task id from filename if not given
    tid = task_id or response_path.stem
    if tid not in tasks:
        print(f"error: task '{tid}' not found. known: {sorted(tasks)}", file=sys.stderr)
        return 2
    response = response_path.read_text(encoding="utf-8")
    result = TaskResult.grade(tasks[tid], response)
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    return 0


def cmd_battery(run_dir: Path, baseline_dir: Path | None) -> int:
    tasks = load_tasks()
    results: list[TaskResult] = []
    missing: list[str] = []
    for t in tasks:
        rp = run_dir / f"{t.id}.txt"
        if not rp.exists():
            missing.append(t.id)
            continue
        response = rp.read_text(encoding="utf-8")
        results.append(TaskResult.grade(t, response))

    battery = sum(r.score for r in results) / len(results) if results else 0.0
    anti_rate = (
        sum(1 for r in results if r.anti_triggered) / len(results) if results else 0.0
    )

    report: dict = {
        "run_dir": str(run_dir),
        "tasks_graded": len(results),
        "tasks_missing": missing,
        "battery_score": round(battery, 3),
        "anti_pattern_rate": round(anti_rate, 3),
        "per_task": [asdict(r) for r in results],
    }

    if baseline_dir is not None:
        base_results: list[TaskResult] = []
        for t in tasks:
            rp = baseline_dir / f"{t.id}.txt"
            if rp.exists():
                base_results.append(
                    TaskResult.grade(t, rp.read_text(encoding="utf-8"))
                )
        if base_results:
            base_battery = sum(r.score for r in base_results) / len(base_results)
            report["baseline_dir"] = str(baseline_dir)
            report["baseline_battery_score"] = round(base_battery, 3)
            report["uplift"] = round(battery - base_battery, 3)
            # Per-task uplift
            by_id = {r.id: r.score for r in base_results}
            report["per_task_uplift"] = {
                r.id: round(r.score - by_id.get(r.id, 0.0), 3) for r in results
            }

    print(json.dumps(report, indent=2, ensure_ascii=False))
    # Fail if uplift is negative (> -0.05) when baseline is given
    if "uplift" in report and report["uplift"] < -0.05:
        return 1
    return 0


# ----------------------------------------------------------------------- main
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="run_evals",
        description="DolphinDB skill eval harness (measure hit-rate & skill uplift).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="dump prompts (optionally to files)")
    pl.add_argument("--out", type=Path, default=None, help="write one file per task here")

    pg = sub.add_parser("grade", help="grade a single response file against its task")
    pg.add_argument("response", type=Path)
    pg.add_argument("--task", default=None, help="override task id (default: infer from filename)")

    pb = sub.add_parser("battery", help="grade a whole run directory")
    pb.add_argument("run_dir", type=Path)
    pb.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="directory of skill-off responses for uplift comparison",
    )

    args = parser.parse_args()
    if args.cmd == "list":
        return cmd_list(args.out)
    if args.cmd == "grade":
        return cmd_grade(args.response, args.task)
    if args.cmd == "battery":
        return cmd_battery(args.run_dir, args.baseline)
    return 2


if __name__ == "__main__":
    sys.exit(main())
