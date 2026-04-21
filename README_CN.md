# DolphinDB Agent Skills

[English](README.md) | 简体中文

> 为 AI 编程助手（Claude Code、Cursor、Trae 等）提供 DolphinDB 数据库知识技能包。

---

## 🧩 项目概述

本项目为各大主流 AI Coding Agent 提供 **DolphinDB 离线知识技能（Agent Skills）**，涵盖：

- DolphinDB 脚本语言语法与内置函数
- SQL 查询、时序分析、流计算（Stream）
- 分布式表（DFS）设计与最佳实践
- Python / Java / C++ API 参考
- 数据导入、性能调优、权限管理

安装后，你的 AI 助手在处理 DolphinDB 相关问题时会自动读取这份离线文档，**无需联网、无需运行时依赖**。

---

## 📦 包含的技能

| 技能名称 | 说明 |
|---------|------|
| `dolphindb` | 完整的 DolphinDB 离线文档知识库，含高频代码片段与 API 速查 |

---

## 🚀 快速开始

### 方式一：PyPI 安装（推荐）

```bash
pip install dolphindb-agent-skills
dolphindb-agent-skills
```

> **Windows 或 PATH 问题？** 如果提示 `dolphindb-agent-skills: command
> not found`（Windows 上是 `'dolphindb-agent-skills' 不是内部或外部
> 命令`），说明 pip 把可执行文件装到了不在 PATH 里的 `Scripts` 目录。
> 直接用 Python 模块方式调用就行，**一定能跑**：
>
> ```bash
> python -m dolphindb_skill_installer
> ```
>
> 或者改用 **pipx** 安装，它会自动处理 PATH：
>
> ```bash
> pipx install dolphindb-agent-skills
> ```

交互式安装器会引导你：
1. 选择 AI 编程工具（Claude Code / Cursor / Trae 等）
2. 确认安装目录（项目级或全局）
3. 选择技能包并一键安装

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/dolphindb/dolphindb-agent-skills.git

# 以 Claude Code 为例，复制技能目录
cp -r dolphindb-agent-skills/skills/dolphindb .claude/skills/
```

---

## 🛠️ 支持的 AI 工具

| 工具 | 安装目录 | 类型 |
|------|----------|------|
| Claude Code | `.claude/skills/` | 项目级 |
| Cursor | `.cursor/skills/` | 项目级 |
| Trae | `.trae/skills/` | 项目级 |
| OpenCode | `.opencode/skills/` | 项目级 |
| GitHub Copilot | `.github/skills/` | 项目级 |
| Codex | `.agents/skills/` | 项目级 |
| OpenClaw | `~/.openclaw/workspace/skills/` | 全局 |
| Qoder | `.qoder/skills/` | 项目级 |
| Antigravity（工作区级） | `.agent/skills/` | 项目级 |
| Antigravity（全局） | `~/.agent/skills/` | 全局 |

---

## 📂 项目结构

```
dolphindb-agent-skills/
├── plugin.json                          # Claude Code marketplace 元信息
├── pyproject.toml                       # Python 包配置
├── upload_to_pypi.py                    # 构建与发布脚本
├── skills/
│   └── dolphindb/
│       ├── SKILL.md                     # ★ 技能入口（触发条件 + 文档导航）
│       └── docs/                        # 离线文档库
│           ├── 00.overview.md
│           ├── 01.quick-start.md
│           ├── 02.data-types.md
│           ├── 03.scripting.md
│           ├── 04.sql.md
│           ├── 05.distributed-tables.md
│           ├── 06.in-memory-tables.md
│           ├── 07.streaming.md
│           ├── 08.functions.md
│           ├── 09.python-api.md
│           ├── 10.java-api.md
│           ├── 11.cpp-api.md
│           ├── 12.data-import.md
│           ├── 13.performance.md
│           └── 14.admin.md
└── src/
    └── dolphindb_skill_installer/
        ├── __init__.py
        └── main.py                      # 交互式安装器 CLI
```

---

## 🔧 开发与贡献

### 添加或更新文档

直接在 `skills/dolphindb/docs/` 目录下编辑或新增 Markdown 文档，然后在 `SKILL.md` 的文档索引表中补充对应条目即可。

### 构建发布到 PyPI

```bash
# 需要先安装 uv
uv run upload_to_pypi.py           # 仅构建
uv run upload_to_pypi.py --upload  # 构建 + 上传
```

---

## 📄 许可证

Apache License 2.0

---

## 🔗 相关链接

- [DolphinDB 官方文档](https://docs.dolphindb.cn/)
- [DolphinDB GitHub](https://github.com/dolphindb)
