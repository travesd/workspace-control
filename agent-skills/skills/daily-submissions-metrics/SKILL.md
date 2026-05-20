---
name: daily-submissions-metrics
description: Investigate Daily Submissions UI and reporting counts by reading the metric implementation, applying exact DB predicates, and explaining differences from broader incident exports.
---

# Daily Submissions Metrics

Use this skill when a task asks why a Daily Submissions UI/reporting count differs from a DB query or incident export.

## Workflow

1. Read the service code that computes the metric before querying. Current reference:

```text
/workspace/detection-platform-metal/services/detection-core/src/submissions/submissions.service.go
```

2. Record the exact predicates and time window in the task notes or dataset README.
3. Query through `/workspace/tools/db/dbctl`; keep the operation read-only.
4. Produce a small breakdown by source, outcome, and judgement before creating any durable export.
5. If the investigation produces a reusable incident set, use `$detection-dataset-export` and preserve the run ID.

## Current Predicate Notes

Daily Submissions "new takedowns" is not "all submitted". It is counted from `gatekeeper_submissions` rows where:

```sql
outcome = 'pushed_new'
AND lower(judgement) = 'bad'
```

Apply date and source filters separately. If a query says "autohunt submitted today", distinguish:

- all autohunt submissions for the day
- autohunt submissions with `outcome = 'pushed_new'`
- all-source Daily Submissions new takedowns

When matching UI numbers, report both the UI-equivalent count and the broader count if they differ.
