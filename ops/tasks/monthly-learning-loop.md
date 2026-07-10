---
title: Monthly learning loop (consolidation pass)
status: todo
priority: normal
runner: any
recurring: monthly
created: 2026-07-10
---

Run the learning loop per CLAUDE.md:

1. Read any new files in `ops/reports/` since the last run (imported performance CSVs/markdown). If none exist, note that in the activity log body of this task and finish.
2. For each report: compare with the previous import of the same source; write findings to `kb/learned/` as entries with `status: unverified` and a `metrics` object including sample sizes, citing the report filename.
3. Consolidation pass: compare `kb/learned/` entries against each other and against `kb/tactics/` — merge duplicates (supersede, don't delete), flag contradictions with `contradicts`, and list promotion candidates (learned entries with consistent metrics across ≥2 reports) at the top of the newest learned entry for owner review.
4. Update `kb/INDEX.md` for any added entries and run the validators.
