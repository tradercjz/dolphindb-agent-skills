"""Build the generated portion of the DolphinDB skill from the upstream docs mirror.

Inputs:  documentation-main/documentation-main/
Outputs: skills/dolphindb/reference/

Regenerates:
    reference/functions/INDEX.md
    reference/functions/by-theme/*.md
    reference/functions/by-name/<letter>/<name>.md
    reference/error-codes/INDEX.md
    reference/error-codes/<Code>.md
    reference/plugins-catalog.md
    docs/<area>/_source/<name>.md   (upstream mirrors; hand-authored siblings untouched)

Usage:
    python skills/dolphindb/scripts/build_from_docs.py
    python skills/dolphindb/scripts/build_from_docs.py \
        --docs-root documentation-main/documentation-main \
        --skill-root skills/dolphindb
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

COPYRIGHT_RE = re.compile(
    r"\n*Copyright\s*\n+\*\*©\d{4}.*?\*\*\s*$",
    re.DOTALL,
)


def strip_footer(text: str) -> str:
    """Remove the standard ``Copyright / ©YYYY ...`` footer."""
    return COPYRIGHT_RE.sub("", text).rstrip() + "\n"


def rewrite_html_links(text: str, link_rewriter) -> str:
    """Rewrite markdown links of the form ``[label](path.html[#anchor])``.

    ``link_rewriter(path, anchor)`` returns the new href, or ``None`` to strip
    the link and keep only the label text.
    """
    link_re = re.compile(r"\[([^\]]+)\]\(([^)\s]+?\.html)(#[^)\s]*)?\)")

    def repl(m: re.Match) -> str:
        label, path, anchor = m.group(1), m.group(2), m.group(3) or ""
        new = link_rewriter(path, anchor)
        if new is None:
            return label
        return f"[{label}]({new}{anchor})"

    return link_re.sub(repl, text)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Error codes
# ---------------------------------------------------------------------------

ERR_CATEGORY = {
    "00": "系统 (System)",
    "01": "存储 (Storage / DFS / TSDB / OLAP)",
    "02": "SQL",
    "03": "流数据 (Streaming)",
    "04": "管理 (Admin / Permission / Cluster)",
    "05": "通用 (General)",
    "06": "解释器 (Interpreter / Parser)",
    "07": "其他 (Other - 07)",
    "09": "其他 (Other - 09)",
    "10": "其他 (Other - 10)",
    "12": "其他 (Other - 12)",
}


@dataclass
class ErrorDoc:
    code: str           # e.g. "S00001"
    category: str       # e.g. "00"
    title_line: str     # first non-heading message bullet, best-effort
    src_path: Path


FIRST_MSG_RE = re.compile(r"## 报错信息\s*\n+(.*?)(?:\n## |\Z)", re.DOTALL)


def extract_error_title(md: str) -> str:
    m = FIRST_MSG_RE.search(md)
    if not m:
        return ""
    body = m.group(1).strip()
    # take first line of the first bullet
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("*", "-")):
            line = line.lstrip("*-").strip()
        return line.rstrip(",，.")
    return ""


def build_error_codes(docs_root: Path, out_dir: Path) -> None:
    src_dir = docs_root / "error_codes"
    if not src_dir.is_dir():
        print(f"[error-codes] source not found: {src_dir}", file=sys.stderr)
        return

    # Wipe generated content to stay idempotent.
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def link_rewriter(path: str, _anchor: str) -> str | None:
        # Most cross-links point to sibling skill docs that don't exist yet.
        # Keep the label but drop the dead link.
        _ = path
        return None

    docs: list[ErrorDoc] = []

    for src in sorted(src_dir.glob("*.md")):
        name = src.stem  # e.g. "S00001" or "err_codes" or "troubleshooting"
        text = src.read_text(encoding="utf-8", errors="replace")
        text = strip_footer(text)
        text = rewrite_html_links(text, link_rewriter)

        # Normalize stem to uppercase code form where applicable.
        if re.fullmatch(r"[sS]\d{5}(_\d+)?", name):
            code_upper = name.upper().split("_")[0]
            category = code_upper[1:3]
            title_line = extract_error_title(text)
            docs.append(ErrorDoc(code_upper, category, title_line, src))
            # Normalize filename (lower-case → upper-case).
            out_path = out_dir / f"{code_upper}.md"
        else:
            out_path = out_dir / src.name

        write(out_path, text)

    # Build INDEX.md
    docs_by_cat: dict[str, list[ErrorDoc]] = defaultdict(list)
    for d in docs:
        docs_by_cat[d.category].append(d)
    for cat in docs_by_cat:
        docs_by_cat[cat].sort(key=lambda d: d.code)

    lines: list[str] = []
    lines.append("# DolphinDB error-code index")
    lines.append("")
    lines.append(
        "When a DolphinDB runtime error shows `RefId: Sxxxxx`, look up the code "
        "below and open the matching file for full 报错信息 / 错误原因 / 解决办法."
    )
    lines.append("")
    lines.append(
        "Error code format: `S + <category (2 digits)> + <sub-code (3 digits)>`. "
        "See `err_codes.md` in this directory for the category legend."
    )
    lines.append("")

    for cat in sorted(docs_by_cat):
        label = ERR_CATEGORY.get(cat, f"Category {cat}")
        lines.append(f"## {cat} — {label}")
        lines.append("")
        lines.append("| Code | Message |")
        lines.append("|------|---------|")
        for d in docs_by_cat[cat]:
            msg = d.title_line.replace("|", "\\|")
            lines.append(f"| [{d.code}]({d.code}.md) | {msg} |")
        lines.append("")

    write(out_dir / "INDEX.md", "\n".join(lines))
    print(f"[error-codes] wrote {len(docs)} codes + INDEX.md to {out_dir}")


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

TOPIC_FILE = "funcs_by_topics.md"

# Matches a markdown link to a function page relative to funcs/, e.g.
#   [abs](a/abs.html)     or     [eachAt(@)](../progr/operators/eachAt.html)
FUNC_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+?\.html)\)")


@dataclass
class FuncRef:
    display: str         # label as shown in the topics file (may include suffix like "(@)")
    name: str            # normalized function name (used as filename basename)
    src_rel: str         # path relative to docs/funcs/, e.g. "a/abs.md" or "../progr/operators/eachAt.md"
    one_liner: str = ""  # first paragraph of `## 详情` from the source file
    in_funcs_dir: bool = True


@dataclass
class Subtopic:
    title: str
    funcs: list[FuncRef] = field(default_factory=list)


@dataclass
class Section:
    title: str
    slug: str
    intro: str = ""
    subtopics: list[Subtopic] = field(default_factory=list)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[\s/]+", "-", text)
    text = re.sub(r"[^a-z0-9\-_一-龥]", "", text)
    return text or "section"


def normalize_func_name(display: str, src_rel: str) -> str:
    """Derive a safe filename from the display label and source path."""
    # Prefer the basename of the source path (handles things like
    # ``append%21`` → ``append!`` after URL-decoding we ignore, and
    # preserves ``eachAt`` from ``operators/eachAt.md``).
    base = Path(src_rel).stem
    # Percent-decode a couple of common encodings.
    base = base.replace("%21", "!").replace("%2A", "*")
    return base or display.strip()


def parse_topics(topics_md: Path) -> list[Section]:
    text = topics_md.read_text(encoding="utf-8", errors="replace")
    text = strip_footer(text)

    sections: list[Section] = []
    current: Section | None = None
    current_sub: Subtopic | None = None

    # Drop the H1 (``# 函数分类``) but keep everything below.
    lines = text.splitlines()

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## "):
            current = Section(title=line[3:].strip(), slug="")
            current.slug = slugify(current.title)
            current_sub = None
            sections.append(current)
            continue

        if current is None:
            continue

        # Bullet lines look like: ``* **子主题：**[fn](path.html), [fn2](path2.html), ...``
        m = re.match(r"^\*\s+\*\*([^*]+?)[：:]\*\*\s*(.*)$", line)
        if m:
            sub_title = m.group(1).strip()
            remainder = m.group(2)
            current_sub = Subtopic(title=sub_title)
            current.subtopics.append(current_sub)
            _absorb_links(current_sub, remainder)
            continue

        # Continuation of a previous bullet (indented with spaces).
        if current_sub is not None and line.startswith(" "):
            _absorb_links(current_sub, line)
            continue

        # Plain-text paragraph before any bullets → intro.
        if current_sub is None and line.strip():
            current.intro = (current.intro + " " + line.strip()).strip()

    return sections


def _absorb_links(sub: Subtopic, text: str) -> None:
    for m in FUNC_LINK_RE.finditer(text):
        display = m.group(1).strip()
        href = m.group(2).strip()
        # ``href`` is always relative to ``funcs/``.
        if href.startswith("../"):
            src_rel = href[3:].replace(".html", ".md")
            in_funcs_dir = False
        else:
            src_rel = href.replace(".html", ".md")
            in_funcs_dir = True
        name = normalize_func_name(display, src_rel)
        sub.funcs.append(FuncRef(
            display=display,
            name=name,
            src_rel=src_rel,
            in_funcs_dir=in_funcs_dir,
        ))


DETAIL_RE = re.compile(r"## 详情\s*\n+(.*?)(?:\n##\s|\Z)", re.DOTALL)
SYNTAX_RE = re.compile(r"## 语法\s*\n+(.*?)(?:\n##\s|\Z)", re.DOTALL)


def extract_one_liner(md: str) -> str:
    m = DETAIL_RE.search(md)
    if not m:
        return ""
    body = m.group(1).strip()
    # first non-empty paragraph
    para = body.split("\n\n", 1)[0].strip()
    # collapse newlines + whitespace
    para = re.sub(r"\s+", " ", para)
    # take up to ~200 chars or first sentence end
    if len(para) > 220:
        cut = para[:220]
        # back off to last sentence boundary if possible
        for sep in ("。", ". ", "；", "，"):
            idx = cut.rfind(sep)
            if idx > 80:
                cut = cut[: idx + 1]
                break
        para = cut.rstrip() + "…"
    return para


def build_functions(docs_root: Path, out_dir: Path) -> None:
    funcs_root = docs_root / "funcs"
    topics_md = funcs_root / TOPIC_FILE
    if not topics_md.is_file():
        print(f"[functions] source not found: {topics_md}", file=sys.stderr)
        return

    by_name_dir = out_dir / "by-name"
    by_theme_dir = out_dir / "by-theme"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    by_name_dir.mkdir(parents=True, exist_ok=True)
    by_theme_dir.mkdir(parents=True, exist_ok=True)

    def funcs_link_rewriter(path: str, _anchor: str) -> str | None:
        # Strip links inside function pages — they mostly point to sibling
        # html pages we cannot follow from inside the skill.
        _ = path
        return None

    sections = parse_topics(topics_md)

    # Copy all function pages under funcs/ (letter dirs + ho_funcs/ + themes/)
    # into by-name/, preserving the sub-directory structure.
    copied: dict[str, Path] = {}  # src_rel -> out_path (relative to by_name_dir)
    for src in funcs_root.rglob("*.md"):
        if src.name in {TOPIC_FILE, "funcs_intro.md", "appendix.md"}:
            continue
        rel = src.relative_to(funcs_root)
        # skip images etc. — already filtered by *.md
        text = src.read_text(encoding="utf-8", errors="replace")
        text = strip_footer(text)
        text = rewrite_html_links(text, funcs_link_rewriter)
        out = by_name_dir / rel
        write(out, text)
        copied[str(rel).replace("\\", "/")] = out

    # Fill in one-liners for each FuncRef.
    for section in sections:
        for sub in section.subtopics:
            for fr in sub.funcs:
                if not fr.in_funcs_dir:
                    # e.g. operators living under ../progr/. We skip copying
                    # those here (they belong to docs/ narrative).
                    continue
                src_path = funcs_root / fr.src_rel
                if not src_path.is_file():
                    continue
                text = src_path.read_text(encoding="utf-8", errors="replace")
                fr.one_liner = extract_one_liner(text)

    # Write by-theme files (one per H2 section).
    theme_files: list[tuple[str, str, str]] = []  # (title, slug, intro)
    for section in sections:
        path = by_theme_dir / f"{section.slug}.md"
        lines: list[str] = []
        lines.append(f"# {section.title}")
        lines.append("")
        if section.intro:
            lines.append(section.intro)
            lines.append("")
        for sub in section.subtopics:
            lines.append(f"## {sub.title}")
            lines.append("")
            for fr in sub.funcs:
                if fr.in_funcs_dir:
                    name_link = f"[`{fr.display}`](../by-name/{fr.src_rel})"
                else:
                    name_link = f"`{fr.display}`"
                desc = f" — {fr.one_liner}" if fr.one_liner else ""
                lines.append(f"- {name_link}{desc}")
            lines.append("")
        write(path, "\n".join(lines))
        theme_files.append((section.title, section.slug, section.intro))

    # Write INDEX.md
    idx: list[str] = []
    idx.append("# DolphinDB function catalog")
    idx.append("")
    idx.append(
        "Functions are grouped by topic below. Open a theme file to see every "
        "function in that group together with a one-line description; follow "
        "the link from there into `by-name/<letter>/<name>.md` for full "
        "signature, parameters and examples."
    )
    idx.append("")
    idx.append("## Themes")
    idx.append("")
    for title, slug, _intro in theme_files:
        idx.append(f"- [{title}](by-theme/{slug}.md)")
    idx.append("")
    idx.append("## Lookup by name")
    idx.append("")
    idx.append(
        "Every built-in function has a dedicated page at "
        "`by-name/<letter>/<name>.md` (e.g. `by-name/a/abs.md` for `abs`). "
        "If you know the exact function name, open that file directly."
    )
    idx.append("")
    write(out_dir / "INDEX.md", "\n".join(idx))

    total_funcs = sum(len(sub.funcs) for s in sections for sub in s.subtopics)
    print(
        f"[functions] wrote {len(theme_files)} themes, "
        f"{len(copied)} function pages, {total_funcs} theme-entries to {out_dir}"
    )


# ---------------------------------------------------------------------------
# Docs mirrors
# ---------------------------------------------------------------------------

# Marker embedded as the first line of every auto-mirrored file. On rebuild we
# scan ``docs/`` for this marker and delete only those files; any hand-authored
# sibling (no marker) survives untouched.
MIRROR_MARKER = "<!-- Auto-mirrored from upstream"


# Directory → directory mappings. Files under *src_sub* are written flat into
# *dst_sub* (subdirectory structure preserved), alongside any hand-authored
# files already in that directory.
# (src_sub, dst_sub, exclude_first_level_subdirs)
DOCS_MIRRORS: list[tuple[str, str, tuple[str, ...]]] = [
    # language / SQL / storage / streaming
    ("progr/sql",                "20-sql",       ()),
    ("db_distr_comp/db",         "30-database",  ()),
    ("db_distr_comp/db_oper",    "50-ingestion", ()),
    ("db_distr_comp/cfg",        "90-admin/cfg", ()),
    ("stream",                   "40-streaming", ("scripts",)),
    ("progr",                    "10-language",  ("sql", "py_parser")),

    # APIs / clients / tools
    ("api",                      "60-api",       ()),
    ("tools",                    "60-api/tools", ()),

    # Admin / ops / monitoring
    ("sys_man",                  "90-admin",     ()),
    ("omc",                      "90-admin/omc", ()),
    ("db_distr_comp/db_man/web", "90-admin/web", ()),

    # Entry-level
    ("getstarted",               "getstarted",   ()),
    ("about",                    "about",        ()),

    # Cross-cutting areas (new)
    ("tutorials",                "tutorials",    ("images",)),
    ("plugins",                  "plugins",      ("images", "data", "script", "scripts")),
    ("modules",                  "modules",      ("images",)),
    ("deploy",                   "deploy",       ()),
    ("mcp",                      "mcp",          ()),
    ("backtest",                 "backtest",     ()),
    ("rn",                       "release-notes",()),
]


# Individual files that do not fit any directory mapping above. Used for the
# handful of ``db_distr_comp/*.md`` pages that belong to different thematic
# areas of the skill.
# (src_file_rel_docs_root, dst_file_rel_docs_base)
DOCS_FILE_MIRRORS: list[tuple[str, str]] = [
    # Client-style pages → 60-api/
    ("db_distr_comp/clients.md",                "60-api/clients.md"),
    ("db_distr_comp/gui.md",                    "60-api/gui.md"),
    ("db_distr_comp/jupyter.md",                "60-api/jupyter.md"),
    ("db_distr_comp/terminal.md",               "60-api/terminal.md"),
    ("db_distr_comp/vscode.md",                 "60-api/vscode.md"),
    # Database operation pages → 30-database/
    ("db_distr_comp/db_distr_comp.md",          "30-database/db_distr_comp.md"),
    ("db_distr_comp/drop_database_table.md",    "30-database/drop_database_table.md"),
    ("db_distr_comp/mod_data.md",               "30-database/mod_data.md"),
    ("db_distr_comp/modify_table_structure.md", "30-database/modify_table_structure.md"),
    # Top-level index pages
    ("index.md",                                "upstream-index.md"),
    ("third_party.md",                          "third_party.md"),
]


# Global filename substring blacklist. Any upstream .md whose filename
# contains one of these substrings is skipped by all directory mirrors.
# Used to prune content tied to features we deliberately do not surface
# in the skill (e.g. the Python parser, which is unstable and rarely
# used — see also the ``py_parser`` entry in the ``progr`` excludes).
FILE_SKIP_SUBSTRINGS: tuple[str, ...] = (
    "py_parser",
)


# Files mirrored into reference/ rather than docs/.
# (src_file_rel_docs_root, dst_file_rel_skill_root)
REF_FILE_MIRRORS: list[tuple[str, str]] = [
    ("funcs/funcs_intro.md",     "reference/functions/funcs_intro.md"),
    ("funcs/appendix.md",        "reference/functions/appendix.md"),
    ("funcs/funcs_by_topics.md", "reference/functions/funcs_by_topics.md"),
]


def _clean_auto_mirrored(root: Path) -> int:
    """Delete every ``*.md`` file under *root* whose first non-blank line
    starts with ``MIRROR_MARKER``. Hand-authored siblings are untouched.
    Returns the number of files removed.
    """
    if not root.is_dir():
        return 0
    removed = 0
    for md in root.rglob("*.md"):
        try:
            with md.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(MIRROR_MARKER):
                        md.unlink()
                        removed += 1
                    break
        except OSError:
            continue
    # Remove now-empty directories, bottom-up.
    for d in sorted([p for p in root.rglob("*") if p.is_dir()],
                    key=lambda p: len(p.parts), reverse=True):
        try:
            d.rmdir()
        except OSError:
            pass
    return removed


def build_docs_mirrors(docs_root: Path, skill_root: Path) -> None:
    """Flat-merge upstream narrative docs into ``docs/<area>/`` (no
    ``_source``/``_upstream`` layer). Hand-authored files are preserved.
    """

    def link_rewriter(path: str, _anchor: str) -> str | None:
        # Cannot reliably translate cross-document links; keep label, drop link.
        _ = path
        return None

    docs_base = skill_root / "docs"
    docs_base.mkdir(parents=True, exist_ok=True)

    # 1. Clean previously-generated files so the build is idempotent.
    removed = _clean_auto_mirrored(docs_base)
    if removed:
        print(f"[docs] cleaned {removed} stale auto-mirrored files")

    # Also wipe any leftover _source / _upstream dirs from older builds.
    for legacy in list(docs_base.rglob("_source")) + list(docs_base.rglob("_upstream")):
        if legacy.is_dir():
            shutil.rmtree(legacy, ignore_errors=True)

    total_files = 0

    # 2. Directory mappings.
    for src_sub, dst_sub, excludes in DOCS_MIRRORS:
        src_dir = docs_root / src_sub
        if not src_dir.is_dir():
            continue
        dst_dir = docs_base / dst_sub
        dst_dir.mkdir(parents=True, exist_ok=True)

        files_here = 0
        for src in src_dir.rglob("*.md"):
            if src.name in {"funcs_by_topics.md"}:
                continue
            # Globally skip any file whose name matches a FILE_SKIP pattern.
            # Used to drop upstream content we do not want to expose (e.g.
            # py_parser tutorials, since py_parser itself is excluded).
            if any(pat in src.name for pat in FILE_SKIP_SUBSTRINGS):
                continue
            rel = src.relative_to(src_dir)
            if excludes and rel.parts and rel.parts[0] in excludes:
                continue
            text = src.read_text(encoding="utf-8", errors="replace")
            text = strip_footer(text)
            text = rewrite_html_links(text, link_rewriter)
            upstream_rel = src.relative_to(docs_root).as_posix()
            header = (
                f"{MIRROR_MARKER} `documentation-main/{upstream_rel}`. "
                f"Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->\n\n"
            )
            write(dst_dir / rel, header + text)
            files_here += 1

        total_files += files_here
        print(f"[docs] mirrored {files_here:>4} files: {src_sub} -> docs/{dst_sub}")

    # 3. Per-file mappings.
    per_file = 0
    for src_rel, dst_rel in DOCS_FILE_MIRRORS:
        src = docs_root / src_rel
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        text = strip_footer(text)
        text = rewrite_html_links(text, link_rewriter)
        upstream_rel = src.relative_to(docs_root).as_posix()
        header = (
            f"{MIRROR_MARKER} `documentation-main/{upstream_rel}`. "
            f"Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->\n\n"
        )
        write(docs_base / dst_rel, header + text)
        per_file += 1

    if per_file:
        print(f"[docs] mirrored {per_file:>4} individual files (db_distr_comp tops)")
        total_files += per_file

    # 4. Per-file mappings into reference/ (e.g. funcs_intro, appendix, funcs_by_topics).
    ref_file = 0
    for src_rel, dst_rel in REF_FILE_MIRRORS:
        src = docs_root / src_rel
        if not src.is_file():
            continue
        text = src.read_text(encoding="utf-8", errors="replace")
        text = strip_footer(text)
        text = rewrite_html_links(text, link_rewriter)
        upstream_rel = src.relative_to(docs_root).as_posix()
        header = (
            f"{MIRROR_MARKER} `documentation-main/{upstream_rel}`. "
            f"Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->\n\n"
        )
        write(skill_root / dst_rel, header + text)
        ref_file += 1

    if ref_file:
        print(f"[docs] mirrored {ref_file:>4} individual files into reference/")
        total_files += ref_file

    print(f"[docs] total mirrored: {total_files}")


# ---------------------------------------------------------------------------
# Plugins catalog
# ---------------------------------------------------------------------------

# Short blurbs for plugins that are hard to auto-extract. Anything missing here
# falls back to a generic "see upstream" stub.
PLUGIN_BLURBS: dict[str, str] = {
    "amdquote":           "AMD low-latency quote feed connector (Level-1/Level-2).",
    "amdhistory":         "AMD historical tick archive loader.",
    "Arrow":              "Read/write Apache Arrow IPC streams and files.",
    "ASTTrader":          "AST counter trading API connector.",
    "aws":                "AWS S3 object storage read/write.",
    "backtest":           "Event-driven backtest engine with order-matching.",
    "CSM":                "CSM counter trading API.",
    "ctp":                "CTP futures trading/market-data connector (SimNow / live).",
    "ctp_2":              "CTP futures trading/market-data connector (v2 API).",
    "DataFeed":           "Generic market-data feed adapter framework.",
    "EFH":                "Exegy EFH market-data connector.",
    "EncoderDecoder":     "Binary encode/decode helpers (FIX, protobuf, custom).",
    "Excel Add-In":       "Query DolphinDB from Excel cells.",
    "Feather":            "Feather v2 file reader/writer.",
    "GP":                 "Symbolic regression / genetic programming.",
    "gurobi":             "Gurobi optimizer bindings.",
    "HBase":              "HBase table read/write.",
    "HDF5":               "HDF5 file read/write (datasets + attributes).",
    "HDFS":               "HDFS file system client.",
    "HttpClient":         "HTTP(S) client for REST calls and webhooks.",
    "input":              "Interactive prompt / stdin capture inside scripts.",
    "INSIGHT":            "华鑫 INSIGHT 行情 connector.",
    "Kafka":              "Apache Kafka producer/consumer.",
    "Kdb+":               "Read kdb+ splayed/partitioned tables.",
    "LDAP":               "LDAP authentication backend.",
    "lgbm":               "LightGBM training / prediction bindings.",
    "LibTorch":           "Run TorchScript models inside DolphinDB (CPU/GPU).",
    "mat":                "MATLAB .mat file reader.",
    "MatchingEngine":     "Internal order matching / backtesting engine.",
    "MDL":                "Market Data Layer — unified high-frequency feed.",
    "MongoDB":            "MongoDB read/write connector.",
    "mqtt":               "MQTT pub/sub client.",
    "mseed":              "MiniSEED seismic file reader.",
    "MySQL":              "MySQL read/write connector.",
    "NSQ":                "中信 NSQ Level-2 quote connector.",
    "ODBC":               "ODBC read/write via Driver Manager.",
    "OPCUA":              "OPC UA client (industrial IoT).",
    "OPC":                "OPC DA/HDA client.",
    "ORC":                "Apache ORC file reader/writer.",
    "Parquet":            "Apache Parquet file reader/writer.",
    "pulsar":             "Apache Pulsar pub/sub.",
    "Py":                 "Embed CPython; call Python functions from DolphinDB.",
    "QuantLib":           "QuantLib pricing / curve / option bindings.",
    "QuickFix":           "FIX protocol client via QuickFIX.",
    "RabbitMQ":           "RabbitMQ producer/consumer.",
    "Redis":              "Redis client.",
    "RocketMQ":           "Apache RocketMQ producer/consumer.",
    "SchemalessWriter":   "Schemaless write path for line-protocol-style feeds.",
    "SevenZip":           "7z archive extract.",
    "signal":             "DSP primitives (FFT, filter, complex math).",
    "SimulatedExchangeEngine": "Simulated exchange for strategy validation.",
    "SipUI2":             "SipUI2 trading UI bridge.",
    "SSEQuotationFile":   "SSE 交易所行情文件解析器.",
    "SVM":                "libsvm train/predict bindings.",
    "TCPSocket":          "Raw TCP client.",
    "UniqueID":           "Generate cluster-unique IDs (snowflake-style).",
    "WebSocket":          "WebSocket client.",
    "WindTDF":            "Wind TDF market-data file parser.",
    "xgboost":            "XGBoost train/predict bindings.",
    "XTP":                "XTP 交易柜台 connector.",
    "zip":                "ZIP archive read/write.",
    "Zlib":               "zlib compress/decompress.",
    "zmq":                "ZeroMQ pub/sub/req/rep.",
    "order_management_engine":   "Order-management engine for live/simulated trading.",
    "matchingEngineSimulator":   "Exchange matching engine simulator.",
    "performance_comparison":    "Plugin performance comparison reference.",
    "datafeed":           "Generic data-feed adapter (file/socket).",
    "simulatedexchangeengine":   "Simulated exchange engine (same as SimulatedExchangeEngine).",
}


def build_plugins_catalog(docs_root: Path, out_path: Path) -> None:
    plg_dir = docs_root / "plugins"
    if not plg_dir.is_dir():
        print(f"[plugins] source not found: {plg_dir}", file=sys.stderr)
        return

    # Discover plugin entries: either a subdirectory (folder-style plugin)
    # or a top-level ``<name>.md`` file (single-file plugin).
    seen: set[str] = set()
    plugins: list[tuple[str, str]] = []   # (display name, upstream path)

    for child in sorted(plg_dir.iterdir(), key=lambda p: p.name.lower()):
        if child.name in {"images", "data", "script", "scripts"}:
            continue
        if child.is_dir():
            name = child.name
            rel = f"plugins/{name}/"
            plugins.append((name, rel))
            seen.add(name.lower())
        elif child.suffix == ".md":
            stem = child.stem
            lower = stem.lower()
            # Skip meta pages
            if lower.startswith("plg_") or lower in {"performance_comparison"}:
                continue
            # Skip if a folder with the same (case-insensitive) stem exists.
            if lower in seen:
                continue
            plugins.append((stem, f"plugins/{stem}.md"))
            seen.add(lower)

    lines: list[str] = []
    lines.append("# DolphinDB plugin catalog")
    lines.append("")
    lines.append(
        "One-line summary of every bundled plugin. Load any plugin from the "
        "marketplace with `installPlugin(\"<name>\"); loadPlugin(\"<name>\")`, "
        "then call its functions under the `<name>::` namespace."
    )
    lines.append("")
    lines.append("Full manuals for every plugin are mirrored into "
                 "`docs/plugins/`. This catalog is meant for quick discovery "
                 "only — follow the link column to read the details.")
    lines.append("")
    lines.append("| Plugin | One-line summary | In-skill path |")
    lines.append("|--------|------------------|---------------|")
    for name, rel in plugins:
        blurb = PLUGIN_BLURBS.get(name) or PLUGIN_BLURBS.get(name.lower()) or ""
        in_skill = rel.replace("plugins/", "docs/plugins/")
        lines.append(f"| `{name}` | {blurb} | `{in_skill}` |")
    lines.append("")
    lines.append("## Common usage")
    lines.append("")
    lines.append("```dolphindb")
    lines.append("// one-time install (download from the plugin marketplace)")
    lines.append("listRemotePlugins()")
    lines.append("installPlugin(\"parquet\")")
    lines.append("")
    lines.append("// per-session load")
    lines.append("loadPlugin(\"parquet\")")
    lines.append("")
    lines.append("// call a plugin function under its namespace")
    lines.append("t = parquet::loadParquet(\"/data/foo.parquet\")")
    lines.append("```")
    lines.append("")
    write(out_path, "\n".join(lines))
    print(f"[plugins] wrote catalog with {len(plugins)} plugins -> {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[3]
    default_docs = repo_root / "documentation-main" / "documentation-main"
    default_skill = repo_root / "skills" / "dolphindb"

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--docs-root", type=Path, default=default_docs)
    ap.add_argument("--skill-root", type=Path, default=default_skill)
    ap.add_argument(
        "--only",
        choices=["errors", "functions", "docs", "plugins", "all"],
        default="all",
        help="only regenerate one subtree",
    )
    args = ap.parse_args(argv)

    docs_root = args.docs_root.resolve()
    skill_root = args.skill_root.resolve()

    if not docs_root.is_dir():
        print(f"docs-root not found: {docs_root}", file=sys.stderr)
        return 2

    if args.only in {"errors", "all"}:
        build_error_codes(docs_root, skill_root / "reference" / "error-codes")

    if args.only in {"functions", "all"}:
        build_functions(docs_root, skill_root / "reference" / "functions")

    if args.only in {"docs", "all"}:
        build_docs_mirrors(docs_root, skill_root)

    if args.only in {"plugins", "all"}:
        build_plugins_catalog(docs_root, skill_root / "reference" / "plugins-catalog.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
