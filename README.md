# DolphinDB Agent Skills

简体中文 | [English](README_CN.md)

> Offline DolphinDB knowledge skills for AI coding agents (Claude Code, Cursor, Trae, and more).

---

## 🧩 Overview

This project bundles **DolphinDB documentation as Agent Skills** so your AI coding assistant can answer DolphinDB questions and write correct code — no internet required, no runtime dependencies.

Covers:
- DolphinDB scripting language syntax and built-in functions
- SQL queries, time-series analytics, stream computing
- Distributed table (DFS) design and best practices
- Python / Java / C++ API reference
- Data ingestion, performance tuning, and administration

---

## 📦 Included Skills

| Skill | Description |
|-------|-------------|
| `dolphindb` | Full offline DolphinDB knowledge base with high-frequency code snippets and API quick-reference |

---

## 🚀 Quick Start

### Option 1 — Install from PyPI (recommended)

```bash
pip install dolphindb-agent-skills
dolphindb-agent-skills
```

If your shell says `dolphindb-agent-skills: command not found` (PATH issue after `pip install --user`), run it as a module instead:

```bash
python -m dolphindb_skill_installer
```

The interactive installer will ask you to:
1. Select your AI coding tool (Claude Code / Cursor / Trae / …)
2. Confirm the install directory (project-level or global)
3. Pick skills and install with one confirmation

### Option 2 — Manual install

```bash
git clone https://github.com/dolphindb/dolphindb-agent-skills.git

# Example: install into Claude Code
cp -r dolphindb-agent-skills/skills/dolphindb .claude/skills/
```

---

## 🛠️ Supported Tools

| Tool | Skills directory | Scope |
|------|-----------------|-------|
| Claude Code | `.claude/skills/` | project |
| Cursor | `.cursor/skills/` | project |
| Trae | `.trae/skills/` | project |
| OpenCode | `.opencode/skills/` | project |
| GitHub Copilot | `.github/skills/` | project |
| Codex | `.agents/skills/` | project |
| OpenClaw | `~/.openclaw/workspace/skills/` | global |
| Qoder | `.qoder/skills/` | project |
| Antigravity (workspace) | `.agent/skills/` | project |
| Antigravity (global) | `~/.agent/skills/` | global |

---

## 📂 Project Structure

```
dolphindb-agent-skills/
├── plugin.json                          # Claude Code marketplace metadata
├── pyproject.toml                       # Python package config
├── upload_to_pypi.py                    # Build & publish helper
├── skills/
│   └── dolphindb/
│       ├── SKILL.md                     # ★ Skill entry (trigger + doc index)
│       └── docs/                        # Offline documentation library
│           ├── 00.overview.md
│           ├── 01.quick-start.md
│           ├── 02.data-types.md
│           ├── ...
│           └── 14.admin.md
└── src/
    └── dolphindb_skill_installer/
        ├── __init__.py
        └── main.py                      # Interactive installer CLI
```

---

## 🔧 Contributing

### Update documentation

Edit or add Markdown files in `skills/dolphindb/docs/`. Update the index table in `SKILL.md` accordingly.

### Build and publish

```bash
# Requires uv (https://docs.astral.sh/uv/)
uv run upload_to_pypi.py           # build only
uv run upload_to_pypi.py --upload  # build + upload to PyPI
```

---

## 📄 License

Apache License 2.0

---

## 🔗 Links

- [DolphinDB Documentation](https://docs.dolphindb.cn/)
- [DolphinDB GitHub](https://github.com/dolphindb)
