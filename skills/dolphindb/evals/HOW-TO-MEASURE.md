# 如何衡量 skill 效果（命中率 / uplift）

本目录提供 **10 个真实任务 + 自动打分器**，用来回答两个问题：

1. **Skill 单独能打多少分？** — `battery_score ∈ [0, 1]`
2. **相比不用 skill，提升多少？** — `uplift = battery_score(on) - battery_score(off)`

---

## 衡量的 4 个层级

| 层级 | 信号 | 自动化 | 本 harness 支持 |
|------|------|--------|----------------|
| L1 检索命中 (retrieval hit) | agent 打开了正确的 reference doc 吗 | 扫 trace | 未内置（取决于你的 agent runtime） |
| **L2 Lexical rubric** | 回答里出现必需的关键术语（`context by`, `@state`, `isValid`…） | 纯文本 regex | ✅ `run_evals.py grade` |
| **L3 Artifact 正确性** | 生成的代码用了正确构造 + 未触发 anti-pattern | 纯文本 regex | ✅ `run_evals.py grade` |
| L4 可执行验证 (gold) | 把生成代码在真实 DolphinDB 跑，结果匹配 ground truth | 需 DDB server | 未内置（高价值任务手动抽查） |

L2 + L3 能覆盖 80% 信号，自动可跑；L4 建议只做 3–5 个高价值任务的人工抽查。

---

## 三步流程

### 步骤 1：导出 10 个任务 prompt

```bash
python skills/dolphindb/scripts/run_evals.py list --out evals/prompts
# → 10 files: evals/prompts/01-context-vs-group-by.txt ... 10-jit-when-to-use.txt
```

每个文件是要发给 agent 的原始 prompt（不含 rubric）。

### 步骤 2：让 agent 回答每个任务（两遍）

**一遍 skill-on，一遍 skill-off**，保存到两个目录。文件名必须和 task id 一致。

#### 用 Claude CLI (Anthropic Skills)

```bash
# skill-on
mkdir -p evals/runs/sonnet-skill-on
for f in evals/prompts/*.txt; do
    name=$(basename "$f" .txt)
    claude --skill skills/dolphindb -p "$(cat $f)" \
        > "evals/runs/sonnet-skill-on/$name.txt"
done

# skill-off (same model, no --skill flag)
mkdir -p evals/runs/sonnet-skill-off
for f in evals/prompts/*.txt; do
    name=$(basename "$f" .txt)
    claude -p "$(cat $f)" \
        > "evals/runs/sonnet-skill-off/$name.txt"
done
```

#### 用 Python SDK (Anthropic)

```python
import anthropic, pathlib, os
client = anthropic.Anthropic()
prompts = sorted(pathlib.Path("evals/prompts").glob("*.txt"))

def run(out_dir, use_skill: bool):
    os.makedirs(out_dir, exist_ok=True)
    for p in prompts:
        kwargs = {"model": "claude-sonnet-4-5", "max_tokens": 4096,
                  "messages": [{"role": "user", "content": p.read_text()}]}
        if use_skill:
            # Skill attached via your deployment's skill registry
            kwargs["extra_headers"] = {"anthropic-skill": "dolphindb"}
        msg = client.messages.create(**kwargs)
        (pathlib.Path(out_dir) / p.name).write_text(msg.content[0].text)

run("evals/runs/sonnet-skill-on",  True)
run("evals/runs/sonnet-skill-off", False)
```

#### 用 OpenAI / 其它模型（想测模型端差异）

skill-off = 直接给 prompt；skill-on = prompt 前面 inline 拼 `SKILL.md` + `docs/cheatsheet.md` 的内容（最简单有效的 baseline）。这衡量的是「skill 文档本身的知识价值」，不依赖 skill runtime。

```python
skill_preamble = (pathlib.Path("skills/dolphindb/SKILL.md").read_text() +
                  "\n\n" +
                  pathlib.Path("skills/dolphindb/docs/cheatsheet.md").read_text())

# skill-on
content = skill_preamble + "\n\n---\n\n" + prompt
```

### 步骤 3：打分

```bash
# 单任务
python skills/dolphindb/scripts/run_evals.py grade \
    evals/runs/sonnet-skill-on/01-context-vs-group-by.txt

# 全量电池 + uplift 对比
python skills/dolphindb/scripts/run_evals.py battery \
    evals/runs/sonnet-skill-on \
    --baseline evals/runs/sonnet-skill-off
```

输出示例：

```json
{
  "run_dir": "evals/runs/sonnet-skill-on",
  "tasks_graded": 10,
  "battery_score": 0.82,
  "anti_pattern_rate": 0.1,
  "baseline_battery_score": 0.43,
  "uplift": 0.39,
  "per_task_uplift": {
    "01-context-vs-group-by": 0.4,
    "02-partition-pruning":   0.3,
    ...
  }
}
```

---

## 怎么读结果

| 指标 | 健康范围 | 说明 |
|------|---------|------|
| `battery_score` (skill-on) | > 0.75 | skill-on 的绝对正确率 |
| `uplift` | > +0.2 | skill 真的帮到 agent 了；<+0.1 说明没被用上 |
| `anti_pattern_rate` | < 0.15 | 10 题里最多 1–2 题带反模式 |
| `per_task_uplift` 里的 ≤0 项 | 少于 2 | 个别任务 skill-on 反而变差 = 路由有问题或文档误导 |

---

## 打分器的边界

`run_evals.py` 是 **lexical grader**，不跑代码。它会：

- ✅ 捕获「没用 `context by`」「没用 `@state`」「没提类型不匹配」这种硬错
- ✅ 扣 anti-pattern（回答里出现 `year(date)` 这种反模式 → 扣 0.3）
- ❌ 无法判断代码是否语法正确（会编译过但语义错的它看不出来）
- ❌ 无法判断「创造性好答案但没命中 rubric 关键词」（会低估）

对 5% 边缘情况做 **人工抽查**（看 `per_task` 里 `rubric_hits` < rubric_total 的项）。

---

## 建议的基线记录格式

```yaml
# evals/baselines/sonnet-4-5.yml
model: claude-sonnet-4-5
date:  2026-04-19
runs:
  skill_off:
    battery_score: 0.43
    anti_pattern_rate: 0.30
  skill_on:
    battery_score: 0.82
    anti_pattern_rate: 0.10
    uplift: +0.39
```

PR 改动 `skills/dolphindb/` 时，CI 跑一次并比对上次 baseline。`uplift` 若跌落 > 0.05 则挡回。

---

## 扩展：加自定义任务

在 `tasks/` 下加一个新 `NN-short-name.md`，遵循既有格式：

```markdown
# NN — short title

**Tags:** <area>, <sub-area>
**Difficulty:** easy | medium | hard
**Reference doc:** `docs/.../...md`

## Prompt
<自然语言问题，可能附代码>

## Rubric
- [ ] 必需提到的关键术语 —— 在反引号里
- [ ] 另一项
- [ ] ...

## Expected artifact (minimum)
```dolphindb
<最少可接受的代码>
```

## Anti-patterns
- `wrong_keyword` ...   <!-- 第一个反引号 token = 主要标识，打分器只扫它 -->
```

`run_evals.py` 自动发现 `tasks/*.md`，无需注册。

---

## 局限与下一步

- **当前 10 题** 覆盖 SQL / 流 / 回测 / 类型 / perf / api 等核心区，但只在 evals 目录里**没**覆盖 plugin、tutorial、web 管理的问答 —— 可按需扩展。
- **L1 检索命中**需要你的 agent runtime 暴露 "opened files" trace（Claude Skills 会返回 `file_reads`，可单独解析写入 retrieval 指标）。
- **L4 可执行验证**：建议起一个本地 DolphinDB standalone（docker），对 task 01 / 03 / 04 / 06 / 08 这五个产代码的任务，用 `ddb.session` run 之后对比输出。

---

## 文件清单

- `tasks/*.md` — 10 个评测任务
- `scoring.md` — 打分规则（人读）
- `run.md` — 原始 bash 循环说明（老版）
- `HOW-TO-MEASURE.md` — **本文件**（完整方法论）
- `../scripts/run_evals.py` — 自动打分器（Python 3.9+，纯 stdlib）
