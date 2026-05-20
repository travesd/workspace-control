---
name: workspace-status
description: Produce a short live orientation report for the workspace, active task context, sessions, worktrees, and next setup steps.
---

# Workspace Status

Use this skill at the start of a non-trivial session, when resuming work, or when asked for current workspace state.

## Workflow

1. Run `tools/workspace-status` from this repo when available, or inspect the live workspace manually.
2. Include only high-signal state:
   - active critical tasks,
   - session summary,
   - current cwd mapping to task/worktree,
   - open PR/branch context when relevant,
   - missing resume/session warnings,
   - intake checklist if no task context is detected.
3. Keep the report concise. Link to detailed indexes rather than dumping them.

## Guardrails

- Generate from live state. Do not rely on a stale saved `STATUS.md`.
- Do not print secrets or env values.
- Do not mutate task dirs.
