# Scoring

Each task has a checklist-style rubric. For each item: agent gets 1 if
fully satisfied, 0.5 if partially, 0 otherwise. Task score = mean of
items. Battery score = mean of task scores.

## What counts as a pass

- **Full score = 1.0** — every rubric item met, no anti-patterns emitted.
- **Acceptable = ≥ 0.8** — minor wording / ordering issues only.
- **Fail = < 0.8** — agent missed a trap or produced broken code.

## Grading tips

- **Run the code** whenever feasible. DolphinDB script can be dry-run
  against a local standalone server; see `run.md` for the harness.
- **Check for named concepts** — rubric items like "mentions
  `context by` (not `group by`)" are easy to grep for, but ensure the
  usage is correct, not just the word.
- **Anti-patterns are tie-breakers** — if the agent produces the right
  answer AND an anti-pattern (e.g. a `where year(date) = 2024` filter),
  cap the score at 0.7.

## Baseline comparison

Record the skill-off baseline once per model. Suggested format:

```
model: <name>
date:  2024-06-01
skill: off
battery_score: 0.42
task_scores:
  01: 0.5
  02: 0.0
  03: 0.3
  ...
```

Rerun with skill on; report the delta. A well-organised skill should
move the battery from ~0.4 to ~0.85+ for focused trap tasks.

## When to revise the skill

If task N's score drops below 0.8 on a model that's competent generally:

1. Open the reference doc named in the task.
2. Check: does the doc actually say the thing the rubric requires?
3. If not — **update the doc first**, then re-run.
4. If yes — the doc is there but the agent didn't find it. Check:
   - Does `SKILL.md` routing table point at it?
   - Does the doc have keywords that would surface in a grep?
   - Is the doc buried behind another file the agent reads first?

Improving discoverability (SKILL.md routing, section READMEs, keywords)
is usually higher leverage than writing more content.
