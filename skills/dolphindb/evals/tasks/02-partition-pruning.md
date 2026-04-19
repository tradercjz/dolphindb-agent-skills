# 02 — Partition pruning

**Tags:** perf, partitioning
**Difficulty:** easy
**Reference doc:** `docs/70-perf/partition-pruning.md`, `docs/70-perf/slow-query-diagnosis.md`

## Prompt

My query over `dfs://tick.trade` (partitioned by `date` VALUE) takes 40 s
but only returns 10000 rows. Why, and how to fix?

```dolphindb
select sym, avg(price) as p
from loadTable("dfs://tick", `trade)
where year(date) = 2024 and month(date) = 3 and sym = `IBM
group by sym
```

## Rubric

- [ ] Identifies that `year(date) = ...` wraps the partition column in a
      function → **full partition scan**.
- [ ] Rewrites the filter as a range on `date`:
      `where date between 2024.03.01 : 2024.03.31`.
- [ ] Mentions verifying with `explain(<...>)` and checking
      `scannedPartition`.
- [ ] (Bonus) notes `sym` should also benefit from the TSDB sort-column
      index if it's sorted on.

## Expected artifact (minimum)

```dolphindb
select sym, avg(price) as p
from loadTable("dfs://tick", `trade)
where date between 2024.03.01 : 2024.03.31 and sym = `IBM
group by sym
```

## Anti-patterns

- Rewriting as `where date >= 2024.03.01 and date < 2024.04.01` is also
  fine — but `year() = ... and month() = ...` **is not**.
- Claiming the problem is compute-side without checking pruning first.
- Adding `hint(...)` before trying the filter rewrite.
