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
5. Run durable-learning capture: record candidate reusable learnings or write "none" in `SUMMARY.md`.
6. Move reusable data products to `/workspace/datasets/` and leave pointers in task notes.
7. Move the task to the correct lifecycle destination:
   - `done/` for completed work,
   - `parked/` for valuable paused work with restart or extraction conditions,
   - `later/` for lightweight backlog items with no preserved active state,
   - `archived/` for reference-only closed or superseded task context.
8. Update `DAY.md`, `done/INDEX.md`, and any dataset/backup index affected.
9. Regenerate session index with `/workspace/tools/agents/sessionctl index`.
10. Remove worktrees only when status is clean and the task rules allow it.

## Gates

- Warn for task dirs over 100 MB.
- Require an explicit harvest/keep decision for task dirs over 1 GB.
- Keep critical in-flight tasks unless the user explicitly says otherwise.
- Score resumability with `/workspace/workspace-control/docs/specs/task-resumability.md` before parking, archiving, or closing tasks that may be mined later.
- Parked tasks need a `resume.md` lifecycle block, in clear Markdown labels or YAML frontmatter, with state, substate, parked reason, restart condition, branch/worktree/PR context, artifact policy, and extraction requirements.
- Use `/workspace/workspace-control/docs/templates/task-lifecycle-block.md` when available.

## Guardrails

- Never delete task context; move it.
- Never push, merge, or remove a worktree without explicit authorization when required by workspace rules.
- Use `detection-platform-metal-work/archived/` for future metal task archives after useful material is summarized or extracted. Treat top-level `/workspace/archive/` as historical migration provenance.
