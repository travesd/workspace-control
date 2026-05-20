---
name: task-closeoff
description: Close completed workspace tasks safely by preserving summaries, harvesting data products, updating indexes, regenerating sessions, and handling worktrees conservatively.
---

# Task Close-Off

Use this skill when a task is done, a PR merged, a review concluded, or the user asks to close/archive task work.

## Workflow

1. Read `/workspace/detection-platform-metal-work/ACTIVE.md`.
2. Verify PR/branch/worktree state before moving anything.
3. Check task directory size and data-shaped outputs.
4. Write or update `SUMMARY.md`.
5. Move reusable data products to `/workspace/datasets/` and leave pointers in task notes.
6. Move the task to the correct `done/`, `later/`, or `archived/` destination.
7. Update `DAY.md`, `done/INDEX.md`, and any dataset/backup index affected.
8. Regenerate session index with `/workspace/tools/agents/sessionctl index`.
9. Remove worktrees only when status is clean and the task rules allow it.

## Gates

- Warn for task dirs over 100 MB.
- Require an explicit harvest/keep decision for task dirs over 1 GB.
- Keep critical in-flight tasks unless the user explicitly says otherwise.

## Guardrails

- Never delete task context; move it.
- Never push, merge, or remove a worktree without explicit authorization when required by workspace rules.
