# 0004 — Multi-repo task roots + agentic-workflows in scope

Date: 2026-05-26

## Context

The workspace has historically been scoped to a single product repo,
`detection-platform-metal`, with `AGENTS.md` Scope section stating
"This workspace is for **detection-platform-metal** only". A second
in-scope repo, `detection-agentic-workflows`
(github.com/travesd/agentic-workflows), is now present at
`/workspace/detection-agentic-workflows/` and is the canonical home for
agent-facing operator surfaces (Pi CLI + deterministic JSON-envelope
tools).

A conversion task was created to port the categorisation-first
`evaluator-accuracy-audit` Python skill into the agentic-workflows repo
as the `daily-result-review` workflow. That task was initially scaffolded
in `detection-platform-metal-work/busy/…` (wrong repo's task root) and
moved to `detection-agentic-workflows-work/busy/…`.

This decision encodes the multi-repo convention so future tasks land
in the right place.

## Decision

Each in-scope repo follows the **parallel-suffix convention**:

| Element | Pattern | Example (metal) | Example (agentic-workflows) |
|---|---|---|---|
| Read-only checkout | `<repo-name>` | `detection-platform-metal` | `detection-agentic-workflows` |
| Branch worktrees | `<repo-name>.worktrees/<branch>/` | `detection-platform-metal.worktrees/feat-foo` | `detection-agentic-workflows.worktrees/feat-bar` |
| Task state | `<repo-name>-work/` | `detection-platform-metal-work/` | `detection-agentic-workflows-work/` |

Each `-work/` tree contains the standard lifecycle dirs (`busy/`,
`parked/`, `later/`, `done/`, `archived/`, `planned/`, `investigations/`)
and its own `ACTIVE.md` + `SESSIONS.md`.

**Cross-repo task lineage** (a task in one `-work/` tree continuing or
extending a task in another) is recorded in `LINEAGE.md` under the
successor task, with a forward-pointer paragraph appended to the origin
task's `resume.md`. The forward-pointer is human-readable durable text;
no symlinks.

## Why

- The `detection-agentic-workflows` repo is a different artifact with its
  own lifecycle, branches, PRs, and CI. Mixing its tasks into the metal
  `-work/` tree would conflate two repos' branch states and make agent
  orientation harder.
- `LINEAGE.md` is a small, durable, bidirectional record. Symlinks would
  break on archival; metadata-only linking would be invisible to a fresh
  agent reading the task dir.

## Activation

Live changes applied 2026-05-26:

1. `current-workspace/AGENTS.md` — Scope section, Primary Paths table,
   worktree-naming sentence, Tool Routing table (agentic-workflows runtime
   row), Task Lifecycle section all updated.
2. Activated by copy to `/workspace/AGENTS.md`. Source ↔ runtime
   verified in sync after the copy.
3. Created `/workspace/detection-agentic-workflows-work/{ACTIVE.md,SESSIONS.md}`
   and the first busy task under it.
4. Origin task `audit-pr64-before-after/resume.md` updated with a forward-
   pointer to the successor.

## Rollback

If this convention turns out wrong:

1. Revert this commit in workspace-control.
2. Restore the prior `current-workspace/AGENTS.md` and copy to runtime.
3. Move `detection-agentic-workflows-work/busy/<task>/` back into
   `detection-platform-metal-work/busy/`.
4. Remove the `LINEAGE.md`.
5. Remove the forward-pointer paragraph from the origin task's `resume.md`.

No external systems read these paths today, so rollback is local-only.

## Open follow-up

- `sessionctl index` does not yet know about per-task-root scoping.
  `detection-agentic-workflows-work/SESSIONS.md` is hand-maintained until
  `sessionctl` gains a `--root` flag or auto-detects multiple roots.
  Separate work item; not blocking this activation.
- `workspace-status --brief` may also need awareness of the new task root;
  verify on first agentic-workflows session.
