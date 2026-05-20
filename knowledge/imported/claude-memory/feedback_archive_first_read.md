---
name: Archive-first read when porting
description: When a task has an archived counterpart, read the archive's reference implementation BEFORE writing new code — not after the first bug
type: feedback
originSessionId: 3a6db8e5-07f8-4b01-83d9-1ee422701a50
---
When the metal repo gets a task that was already solved in the archived detection-platform repo (pattern: `migrate` tooling, `snapshot portability`, `client restore`, any cross-env data sync), the archived implementation in `/workspace/archive/detection-platform.worktrees/<branch>/tools/classifiers/` or the matching service dir is almost always the proven reference. Read it BEFORE writing the new code, not after the first dry-run fails.

**Why:** On the `migrate-sh-data-sync` task (PR metal#7, 2026-04-23), I wrote `migrate_snapshots` and `migrate_detection_data` by inferring semantics from metal's API shape and reading the schema. The archived `classifier_data_bundle_lib.py` already had all the non-obvious decisions nailed down: only remap `sourceType=="snapshot"` (not corpus/incident — those use `sourceRef` for non-snapshot tags like `"seed:2026-03-25"`), export only snapshots referenced by detection_data (not the whole snapshots table), group promote calls by `(clientId, sourceType, sourceRef, promotedBy)` to preserve provenance. Cost ~4 dry-run iterations + user annoyance ("you made some bullshit assumptions without reading the task or code again") before I went back and read the archive. Once I did, one surgical rewrite passed cleanly.

**How to apply:**
- When creating a new task that touches an area with archived history, the plan.md should cite the archived task's plan/notes/code by file path before the design section is written.
- When debugging a task with an archived counterpart, before iterating on the fix: re-read the archived implementation. The bug is often something the archive explicitly handled.
- `/workspace/archive/detection-platform-work/busy/<task>/` for plan/notes; `/workspace/archive/detection-platform.worktrees/<branch>/` for code. The `tooling-notes/` and `memory-gke/` subdirs hold the GKE-era memory files.
