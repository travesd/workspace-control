# Multi-Repo Task Organization

Status: draft in workspace-control; not activated live

Date: 2026-05-27

## Purpose

The workspace now has three first-class repos:

- `detection-platform-metal`
- `detection-agentic-workflows`
- `workspace-control`

Each repo needs local ownership of its branches, worktrees, validation rules,
and task artifacts. At the same time, agents need one place to discover current
work across the whole workspace.

The model is:

```text
distributed task ownership + central generated discovery
```

Do not move all task artifacts into one central physical task root.

## Repo Roots

Every first-class repo follows the same pattern:

```text
/workspace/<repo-name>
/workspace/<repo-name>.worktrees/
/workspace/<repo-name>-work/
```

Current and planned roots:

| Repo | Checkout | Worktrees | Task Root |
|---|---|---|---|
| `detection-platform-metal` | `/workspace/detection-platform-metal` | `/workspace/detection-platform-metal.worktrees/` | `/workspace/detection-platform-metal-work/` |
| `detection-agentic-workflows` | `/workspace/detection-agentic-workflows` | `/workspace/detection-agentic-workflows.worktrees/` | `/workspace/detection-agentic-workflows-work/` |
| `workspace-control` | `/workspace/workspace-control` | `/workspace/workspace-control.worktrees/` | `/workspace/workspace-control-work/` |

`workspace-control-work/` is the intended home for future workspace-control
operating-model tasks after live activation. Until activation, existing
workspace-control task records may remain where they were created, but new
repo-first work should move toward this root.

## Lifecycle Shape

Each task root uses the standard lifecycle directories:

```text
ACTIVE.md
SESSIONS.md
planned/
busy/
parked/
later/
done/
archived/
investigations/
.sessions/
```

The lifecycle definitions stay in `task-lifecycle.md`. This spec defines how
the same lifecycle applies across repos.

## Central Discovery

Create a generated workspace-level task index instead of centralizing task
artifacts:

```text
/workspace/TASKS.md
/workspace/.task-index/index.json
```

The central index is derived from:

- each `<repo-name>-work/ACTIVE.md`;
- each `<repo-name>-work/SESSIONS.md`;
- lightweight `planned/*.md` backlog notes;
- task-local `workflow.json`;
- task-local `resume.md`;
- task-local `SUMMARY.md` for closed work.

It is not authoritative for ownership. The authoritative task state remains in
the owning repo's task root.

Repo helper:

```bash
/workspace/workspace-control/tools/task-index render --out /tmp/task-index-preview
```

Live generation to `/workspace/TASKS.md` and
`/workspace/.task-index/index.json` should happen only after activation
approval.

## Task Ownership

Choose the task root by the repo that owns the outcome:

| Work Type | Coordinator Task Root |
|---|---|
| Product implementation, production-facing review, classifier/data investigation | `detection-platform-metal-work/` |
| Agentic workflow implementation, Pi/JSON-envelope tooling, workflow adapters | `detection-agentic-workflows-work/` |
| Workspace operating model, shared instructions, shared skills, live activation, task tooling | `workspace-control-work/` |

If the outcome is genuinely cross-repo, create a coordinator task plus
repo-specific child tasks.

## Cross-Repo Tasks

A cross-repo initiative should have one coordinator task and zero or more child
tasks.

Example:

```text
/workspace/workspace-control-work/busy/workflow-automation-rollout/
/workspace/detection-agentic-workflows-work/busy/workflowctl-adapter/
/workspace/detection-platform-metal-work/busy/brand-worker-integration/
```

The coordinator task owns:

- overall implementation brief or PRD;
- context pack;
- swarm routing decision;
- cross-repo validation ledger;
- approval stops;
- final closeoff summary.

Each child task owns:

- repo branch and worktree;
- repo-local implementation notes;
- repo-local validation;
- repo-local closeoff or handoff.

Record the relationship in `LINEAGE.md` and `workflow.json.related_tasks`.

## Worktrees

Keep worktrees repo-local. Do not create one shared worktree area.

For non-trivial workspace-control code or docs work, prefer:

```bash
git -C /workspace/workspace-control worktree add \
  /workspace/workspace-control.worktrees/<branch-name> -b <branch-name>
```

Direct edits in `/workspace/workspace-control` remain acceptable for tiny
docs-only or activation metadata changes when the repo is clean and the user
has approved the operation.

## Closeoff

Close tasks in the owning task root. A cross-repo coordinator task should not
close until each required child task is closed, parked, or explicitly deferred.

Closeoff must preserve:

- summary;
- validation evidence;
- branch/worktree/PR state;
- rollback notes for workspace-control live activations;
- durable learning route;
- child/coordinator lineage.

## Migration Notes

This model is additive.

Do not move existing task directories as part of activation unless a separate
movement table is reviewed and approved. Add the new `workspace-control-work/`
root first, then let future tasks use it.
