# Evals — measuring whether the skill actually helps

A small, curated set of **real tasks** that an AI agent using this skill
should be able to solve correctly. Use it to:

1. **Regression-test** skill edits: rerun after every SKILL.md / docs
   change to catch drift.
2. **A/B test** skill-on vs skill-off: show the actual uplift from
   exposing these docs to an agent.
3. **Feed prompt templates** when training / fine-tuning a DolphinDB-
   specialized agent.

## Layout

- `tasks/*.md` — one file per evaluation task. Each has:
  - **Prompt** (what the user asks)
  - **Rubric** (checklist of correct-solution properties)
  - **Tags** (topic area, difficulty)
  - **Reference** (pointer to the skill doc an oracle would consult)
  - **Minimal expected artifact** (code stub / pattern)
- `scoring.md` — how to grade responses.
- `run.md` — how to loop through tasks in a harness.

## Current set (10 tasks)

| # | Task | Tags | Difficulty |
|---|------|------|------------|
| 1 | `tasks/01-context-vs-group-by.md`   | sql, traps            | easy |
| 2 | `tasks/02-partition-pruning.md`     | perf, partitioning    | easy |
| 3 | `tasks/03-asof-join-empty.md`       | sql, time-types       | medium |
| 4 | `tasks/04-state-factor-streaming.md`| streaming, factor     | medium |
| 5 | `tasks/05-backtest-signal.md`       | backtest              | medium |
| 6 | `tasks/06-dfs-schema-choice.md`     | database, partitioning| medium |
| 7 | `tasks/07-python-decimal-loss.md`   | api, python           | medium |
| 8 | `tasks/08-stream-recovery.md`       | streaming, ops        | hard |
| 9 | `tasks/09-null-window-propagation.md`| language, null       | hard |
| 10 | `tasks/10-jit-when-to-use.md`      | perf, jit             | hard |

Each task is **self-contained** — it states the realistic scenario and
the verifier needs only the rubric to judge correctness. Tasks are
written in the agent's working language (English + DolphinDB code).

## Why 10?

Small enough to run by hand in 15 minutes, large enough to cover the
high-traffic traps. Expand over time as new trap patterns emerge from
real user interactions.

## Adding a new task

When a user hits a bug that wasn't caught by existing tasks:

1. Write it up as `tasks/NN-short-name.md` using the template below.
2. Make sure a hand-authored doc exists that would have prevented the
   bug — if not, **write that doc first**, then the task.
3. Update this README's table.

## Task template

```markdown
# NN — <title>

**Tags:** tag1, tag2
**Difficulty:** easy | medium | hard
**Reference doc:** docs/…/…md

## Prompt

<what the user asks. realistic. might include wrong code.>

## Rubric

The agent's answer is correct iff all of the following hold:

- [ ] …
- [ ] …

## Expected artifact (minimum)

\`\`\`dolphindb
…
\`\`\`

## Anti-patterns (agent should NOT do)

- …
```
