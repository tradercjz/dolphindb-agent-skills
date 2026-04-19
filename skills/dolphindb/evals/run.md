# Running the battery

## Manual

```bash
# In each task file, the "Prompt" section is what you paste into the agent.
# Capture the response, grade against the task's Rubric.
```

## Semi-automated (bash)

```bash
#!/usr/bin/env bash
# Run every task, write one response file per task.

OUT=evals/runs/$(date +%Y-%m-%d_%H-%M)
mkdir -p "$OUT"

for f in evals/tasks/*.md; do
    name=$(basename "$f" .md)
    prompt=$(sed -n '/^## Prompt/,/^## Rubric/p' "$f" | sed '1d;$d')
    # replace this with your actual agent CLI
    your-agent --skill skills/dolphindb \
        --input "$prompt" > "$OUT/$name.txt"
done

echo "Runs in $OUT. Grade with evals/scoring.md."
```

## CI harness (suggested)

- Trigger: any PR touching `skills/dolphindb/`.
- Steps:
  1. Lint: ensure every `tasks/*.md` has `## Prompt`, `## Rubric`,
     `## Expected artifact` sections.
  2. Run: loop through tasks with skill on, collect responses.
  3. Grade: automated rubric items (keyword match) + human review flag
     for open-ended items.
  4. Report: battery score vs main branch baseline; fail CI if delta <
     -0.05 on any task.

## Comparing skill-on vs skill-off

Run the battery twice:

```bash
bash run-battery.sh --skill-dir skills/dolphindb   > off-run.log
bash run-battery.sh --skill-dir skills/dolphindb   > on-run.log
diff <(cut ...) <(cut ...)
```

Expected uplift for a well-organised skill: +0.3 to +0.5 on the battery.

## Task authoring checklist

Before merging a new task:

- [ ] Prompt is realistic (based on an actual user bug or doc gap).
- [ ] Rubric has 4–8 items, each independently testable.
- [ ] Reference doc exists and contains the answer.
- [ ] At least one **anti-pattern** listed (what correct-looking but
      wrong answers to watch for).
- [ ] Difficulty rating agrees with task 01–10 peers.
