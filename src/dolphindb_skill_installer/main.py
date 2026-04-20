#!/usr/bin/env python3
"""Interactive installer for DolphinDB Agent Skills.

Installs DolphinDB knowledge skills into the skills directory of your
AI coding agent (Claude Code, Cursor, Trae, OpenCode, etc.).

Usage:
    dolphindb-agent-skills
"""

import sys
import shutil
from pathlib import Path
from typing import Dict, List

try:
    import questionary
    from questionary import Style
except ImportError:
    print("Error: questionary is not installed. Please run: pip install questionary")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────
# Style: no background highlight so terminals look consistent
# ──────────────────────────────────────────────────────────────
_STYLE = Style([
    ("selected", "noreverse"),
    ("highlighted", "noreverse"),
])


# ──────────────────────────────────────────────────────────────
# Supported tools and their skills directory paths.
# Paths starting with "~" are treated as global (user-home) paths.
# All others are relative to the project root (cwd at install time).
# ──────────────────────────────────────────────────────────────
TOOL_CONFIGS: Dict[str, str] = {
    "Claude Code":          ".claude/skills",
    "Cursor":               ".cursor/skills",
    "Trae":                 ".trae/skills",
    "OpenCode":             ".opencode/skills",
    "GitHub Copilot":       ".github/skills",
    "Codex":                ".agents/skills",
    "OpenClaw":             "~/.openclaw/workspace/skills",
    "Qoder":                ".qoder/skills",
    "Antigravity (workspace)": ".agent/skills",
    "Antigravity (global)":    "~/.agent/skills",
}

# ──────────────────────────────────────────────────────────────
# Available skill packages under skills/
# ──────────────────────────────────────────────────────────────
AVAILABLE_SKILLS: List[str] = [
    "dolphindb",
    "dolphindb-runtime",
]

# One-line descriptions shown next to each skill in the checkbox.
SKILL_DESCRIPTIONS: Dict[str, str] = {
    "dolphindb":         "offline knowledge base (SQL dialect, DFS, streaming, backtest, …) — no server needed",
    "dolphindb-runtime": "bash snippets to connect & run scripts via the Python API — will ask for your server info",
}

# Default placeholders inside the shipped dolphindb-runtime SKILL.md.
# The installer rewrites these to the values the user enters in Step 5.
_DDB_RUNTIME_SKILL = "dolphindb-runtime"
_DEFAULT_HOST   = "127.0.0.1"
_DEFAULT_PORT   = "8848"
_DEFAULT_USER   = "admin"
_DEFAULT_PASSWD = "123456"


# ──────────────────────────────────────────────────────────────
# Path helpers
# ──────────────────────────────────────────────────────────────

def get_package_skills_dir() -> Path:
    """Return the skills/ directory bundled with this package."""
    package_dir = Path(__file__).parent

    # Installed wheel: skills/ lives next to main.py
    bundled = package_dir / "skills"
    if bundled.exists():
        return bundled

    # Development checkout: skills/ is at the repo root
    # (package lives under src/dolphindb_skill_installer/)
    repo_root_skills = package_dir.parent.parent / "skills"
    if repo_root_skills.exists():
        return repo_root_skills

    raise FileNotFoundError(
        "Could not locate the skills/ directory. "
        "Re-install the package or run from the repository root."
    )


def is_global_path(tool_name: str) -> bool:
    """Return True if the tool's skills directory is a global (home-relative) path."""
    return TOOL_CONFIGS.get(tool_name, "").startswith("~")


def resolve_tool_skills_path(tool_name: str, project_root: Path) -> Path:
    """Return the absolute path to the skills directory for the given tool."""
    raw = TOOL_CONFIGS[tool_name]
    if raw.startswith("~"):
        return Path(raw).expanduser()
    return project_root / raw


# ──────────────────────────────────────────────────────────────
# Installation logic
# ──────────────────────────────────────────────────────────────

def copy_skill(skills_source_dir: Path, target_skills_dir: Path, skill_name: str) -> bool:
    """Copy a single skill directory into target_skills_dir.

    Overwrites any previously installed version of the skill.
    Returns True on success, False on error.
    """
    src = skills_source_dir / skill_name
    dst = target_skills_dir / skill_name

    if not src.exists():
        print(f"  ⚠️  Skill '{skill_name}' not found in package, skipping.")
        return False

    try:
        if dst.exists():
            shutil.rmtree(dst)
        target_skills_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dst)
        return True
    except Exception as exc:
        print(f"  ❌ Error installing '{skill_name}': {exc}")
        return False


def install_skills(
    tool_name: str,
    skills: List[str],
    project_root: Path,
) -> None:
    """Install selected skills into the chosen tool's skills directory."""
    source_dir = get_package_skills_dir()
    target_dir = resolve_tool_skills_path(tool_name, project_root)

    print(f"\n📦 Skills source : {source_dir}")
    if not is_global_path(tool_name):
        print(f"📁 Project root  : {project_root}")
    print(f"📂 Target        : {target_dir}")
    print()

    print(f"🔧 Installing to {tool_name}...")
    for skill in skills:
        if copy_skill(source_dir, target_dir, skill):
            print(f"  ✅ Installed '{skill}'")

    print()


# ──────────────────────────────────────────────────────────────
# DolphinDB connection configuration (for dolphindb-runtime skill)
# ──────────────────────────────────────────────────────────────

def _patch_skill_connection(
    skill_file: Path,
    host: str, port: str, user: str, passwd: str,
) -> None:
    """Rewrite the 4 default connection values inside an installed SKILL.md.

    Uses literal replacement of the defaults that ship in the template.
    Only called after the skill has been copied into the target directory,
    so the package's own template is never modified.
    """
    text = skill_file.read_text(encoding="utf-8")
    # Two-phase replacement via sentinel tokens so that a user value that
    # happens to equal another default (e.g. passwd == "admin") cannot be
    # re-replaced in a later pass.
    H, P, U, W = "\x00DDB_H\x00", "\x00DDB_P\x00", "\x00DDB_U\x00", "\x00DDB_W\x00"
    text = (
        text.replace(_DEFAULT_HOST,   H)
            .replace(_DEFAULT_PORT,   P)
            .replace(_DEFAULT_USER,   U)
            .replace(_DEFAULT_PASSWD, W)
    )
    text = (
        text.replace(H, host)
            .replace(P, str(port))
            .replace(U, user)
            .replace(W, passwd)
    )
    skill_file.write_text(text, encoding="utf-8")


def configure_dolphindb_connection(
    tool_name: str,
    installed_skills: List[str],
    project_root: Path,
) -> None:
    """Interactively patch the dolphindb-runtime skill with real connection info.

    The shipped SKILL.md uses generic defaults (127.0.0.1:8848/admin/123456).
    After install, we offer to rewrite them to the user's actual DolphinDB so
    the AI agent has ready-to-run bash snippets.
    """
    if _DDB_RUNTIME_SKILL not in installed_skills:
        return

    target_dir = resolve_tool_skills_path(tool_name, project_root)
    skill_file = target_dir / _DDB_RUNTIME_SKILL / "SKILL.md"
    if not skill_file.exists():
        return

    print("\n🔗 DolphinDB Connection Info")
    print("-" * 50)
    print("The 'dolphindb-runtime' skill contains bash snippets that connect")
    print("to DolphinDB via the Python API. Please enter your server info so")
    print("the installed skill is ready to run. Press Enter to accept a default.")

    host: str = _ask(questionary.text, "DDB host:", default=_DEFAULT_HOST)
    port: str = _ask(
        questionary.text, "DDB port:", default=_DEFAULT_PORT,
        validate=lambda v: v.isdigit() or "port must be a number",
    )
    user: str = _ask(
        questionary.text, "DDB user:", default=_DEFAULT_USER,
        validate=lambda v: bool(v.strip()) or "user cannot be empty",
    )
    passwd: str = _ask(
        questionary.password, "DDB password:", default=_DEFAULT_PASSWD,
        validate=lambda v: bool(v) or "password cannot be empty",
    )

    try:
        _patch_skill_connection(skill_file, host, port, user, passwd)
    except OSError as exc:
        print(f"  ❌ Failed to patch {skill_file}: {exc}")
        return

    print(f"  ✅ Patched connection info into {skill_file}")
    print(f"     host={host}  port={port}  user={user}  password={'*' * len(passwd)}")


# ──────────────────────────────────────────────────────────────
# Interactive CLI
# ──────────────────────────────────────────────────────────────

def _ask(prompt_fn, *args, **kwargs):
    """Wrap questionary calls to handle Ctrl-C gracefully."""
    try:
        result = prompt_fn(*args, **kwargs).ask()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled.")
        sys.exit(0)
    if result is None:
        # User hit Ctrl-C through questionary's own handling
        print("\nInstallation cancelled.")
        sys.exit(0)
    return result


def main() -> None:
    print("🐬 DolphinDB Agent Skills Installer")
    print("=" * 50)

    # ── Step 1: Choose target tool ────────────────────────────
    print("\n📋 Select the AI coding agent to install into:")
    selected_tool: str = _ask(
        questionary.select,
        "Choose one tool  (↑↓ navigate · Enter confirm · Ctrl+C cancel):",
        choices=list(TOOL_CONFIGS.keys()),
        style=_STYLE,
    )

    # ── Step 2: Confirm install path ──────────────────────────
    project_root = Path.cwd()
    target_path = resolve_tool_skills_path(selected_tool, project_root)

    if is_global_path(selected_tool):
        print(f"\n📁 Skills will be installed to: {target_path}")
        confirmed: bool = _ask(questionary.confirm, "Continue?", default=True)
        if not confirmed:
            print("Installation cancelled.")
            sys.exit(0)
    else:
        print(f"\n📁 Project root  : {project_root}")
        print(f"   Skills dir    : {TOOL_CONFIGS[selected_tool]}")
        confirmed = _ask(
            questionary.confirm,
            "Install skills into this project directory?",
            default=True,
        )
        if not confirmed:
            print("Installation cancelled.")
            sys.exit(0)

    # ── Step 3: Choose skills ─────────────────────────────────
    print("\n📦 Available skills:")
    for s in AVAILABLE_SKILLS:
        print(f"   • {s:<18} {SKILL_DESCRIPTIONS.get(s, '')}")
    selected_skills: List[str] = _ask(
        questionary.checkbox,
        "Choose skills  (Space select · Enter confirm · Ctrl+C cancel):",
        choices=[
            questionary.Choice(
                title=f"{s}  —  {SKILL_DESCRIPTIONS.get(s, '')}",
                value=s,
                checked=True,
            )
            for s in AVAILABLE_SKILLS
        ],
        instruction="(Space to toggle, Enter to confirm)",
        style=_STYLE,
    )

    if not selected_skills:
        print("No skills selected. Nothing to install.")
        sys.exit(0)

    # ── Step 4: Summary + install ─────────────────────────────
    print("\n📝 Installation summary")
    print(f"   Tool   : {selected_tool}")
    print(f"   Skills : {', '.join(selected_skills)}")
    if not is_global_path(selected_tool):
        print(f"   Root   : {project_root}")

    install_skills(selected_tool, selected_skills, project_root)

    # ── Step 5: Optional DolphinDB connection patching ───────
    configure_dolphindb_connection(selected_tool, selected_skills, project_root)

    print("\n✨ Done! Please restart your AI agent to pick up the new skills.")
    print("💡 Tip: verify with /skills or by asking about DolphinDB in your agent.")


if __name__ == "__main__":
    main()
