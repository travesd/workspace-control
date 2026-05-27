# Task Lifecycle Spec

Status: active live reference for task-state definitions; physical task movement
remains intentional and user-approved

Date: 2026-05-21

This spec defines task states for the workspace task roots. The multi-repo
ownership model is defined in `docs/specs/multi-repo-task-organization.md`.

Task state and task resumability are related but separate. This spec defines
where task context belongs. The resume packet, notes ledger, and quality score
are defined in `docs/specs/task-resumability.md`.

## Principle

Task state should describe the next operational relationship to the work, not just where files happen to live.

Each task has one primary lifecycle state. Substates are metadata inside
`resume.md` or `SUMMARY.md`; they are not extra top-level directories.

The normal task lifecycle roots are:

```text
/workspace/detection-platform-metal-work/
/workspace/detection-agentic-workflows-work/
/workspace/workspace-control-work/
```

Future task archives use the owning task root:

```text
/workspace/<repo-name>-work/archived/YYYYMMDD-<reason>/<task>/
```

The top-level `/workspace/archive/` is the legacy migration/provenance
collection for old repos, GKE-era work, historical datasets, loose migration
files, and backward-compatibility symlink targets.

## Classification Order

When a task could fit more than one state, classify by the next action:

1. `done/` if the requested outcome is complete and close-off has happened.
2. `busy/` if someone must act on it in the current session, current work
   block, or near-term PR/review/CI cycle.
3. `parked/` if it is intentionally paused but has valuable state to preserve
   and a credible restart, extraction, or decision condition.
4. `planned/` if it is scoped enough to schedule but has not started.
5. `later/` if it is only a lightweight future idea with no important local
   working state.
6. `archived/` if it is closed, superseded, obsolete, or provenance-only after
   useful state has been extracted or summarized.
7. `investigations/` if it is standalone research not yet tied to a task
   lifecycle.

## States

### `planned/`

Use for accepted or plausible work that has not started but is concrete enough
to be scheduled.

Criteria:

- No active owner/session.
- No active worktree requirement yet.
- Scope may still be a sketch or proposal.
- Starting the work should create or move into `busy/<task>/`.
- The task has enough shape that an agent can tell what "started" means.

Typical contents:

- one Markdown spec or task brief,
- links to related context,
- rough acceptance criteria.

Not for:

- implemented prototypes,
- deferred PR branches,
- vague someday ideas with no trigger or owner,
- tasks with valuable local artifacts to preserve.

### `busy/`

Use for work that is active now or needs near-term attention.

Criteria:

- An agent or human is actively working it in the current session or work block, or
- a PR is awaiting review/CI/merge and needs near-term follow-up, or
- `ACTIVE.md` names it as critical active inventory, or
- a live worktree/container/session must be protected while work continues.

Required:

- `resume.md` for non-trivial work,
- resume packet for multi-step or handoff-prone work,
- lifecycle state line or block when the task is not obviously active,
- current branch/worktree/PR/session context when applicable,
- next action.

Examples:

- live agent-owned branch,
- PR waiting review,
- critical work intentionally kept in the active inventory,
- current prototype iteration being reviewed.

Exit destinations:

- `done/` when complete,
- `parked/` when intentionally paused but expected to resume or be mined,
- `archived/` when closed/superseded after useful context is preserved,
- `later/` only when it has been reduced to a lightweight backlog item with no preserved working state.

### `parked/`

Use for valuable paused work that is not active now, but has a concrete reason
to preserve and revisit.

Criteria:

- Not currently being worked.
- Contains useful implementation, prototype, research, branch, data, or review evidence.
- Has a clear resume, extraction, or decision condition.
- Should not be treated as ordinary active work.
- The next action is deliberately delayed, blocked, or dependent on a future
  decision.

Required lifecycle fields in `resume.md`, either as Markdown labels or YAML
frontmatter:

```yaml
state: parked
substate: prototype-baseline | deferred-pr | extraction-needed | blocked-external | paused-critical
parked_reason: "Why it is not active now"
restart_when: "Condition that brings this back to busy"
extract_before_archive: "What should be harvested before final archive"
branch_worktree_status: "Branch/worktree/PR state"
artifact_policy: "What must be preserved"
review_after: "Optional date or trigger"
chat_dependency: "optional | useful-for-history | required"
resumability_score: "0-10"
```

Markdown equivalent:

```markdown
## Lifecycle

- State: parked
- Substate: deferred-pr
- Parked reason: Closed because the broader design is not ready.
- Restart when: Structured sub-product support is needed again.
- Extract before archive: prompt contract notes and validated tests.
- Branch/worktree status: local branch preserved, remote PR closed.
- Artifact policy: preserve deferred patch and review notes.
- Review after: next classifier prompt redesign.
- Chat dependency: useful-for-history.
- Resumability score: 8/10.
```

Substates:

- `prototype-baseline`: a working prototype kept as a reference while another slice ships.
- `deferred-pr`: a branch/PR was closed or paused, but the patch or validation may be useful later.
- `extraction-needed`: research or prototype is complete enough that reusable parts should be harvested.
- `blocked-external`: continuation depends on credentials, review, product decision, upstream fix, or environment access.
- `paused-critical`: strategically important work is paused, but still needs explicit protection in `ACTIVE.md` or another owner-visible inventory.

Not for:

- vague ideas with no concrete artifact,
- completed work that only needs a summary,
- superseded work after useful pieces have already been extracted,
- work that a human or agent is expected to resume in the current work block.

Exit destinations:

- back to `busy/` when restarted,
- `done/` if completed through close-off without more implementation,
- `archived/` after extraction or decision that it will not resume,
- `later/` only if reduced to a lightweight idea with no state to preserve.

### `later/`

Use for lightweight backlog items that may be useful but do not preserve active
working state.

Criteria:

- No live owner/session.
- No active worktree/container requirement.
- No important local-only patch or artifact requiring careful preservation.
- Resume condition may be broad or opportunistic.
- The item can be understood from a short note without reconstructing a
  worktree/session history.

Typical contents:

- short plan or notes,
- links to parked/done/archived context if relevant.

Not for:

- deferred PRs with local patches,
- prototypes that should be inspected before deletion,
- large analysis artifacts,
- paused critical work,
- scoped work that is ready to schedule; use `planned/` for that.

### `done/`

Use for completed work.

Criteria:

- The requested outcome shipped, review was delivered, investigation concluded, or the user accepted the result.
- Reusable data products were harvested or deliberately left with pointers.
- Durable learnings were captured or explicitly marked none.
- Worktree cleanup decision is recorded.

Required:

- `SUMMARY.md`,
- preserved `plan.md` and `notes.md` when they exist,
- links to merged PRs, commits, datasets, or decisions when applicable,
- resumability or extraction decision for any task that may be mined later,
- day index update after live activation of this lifecycle.

### `archived/`

Use for inactive task context kept for provenance, not expected to resume.

Criteria:

- Superseded,
- closed-unmerged after useful pieces were extracted,
- abandoned/obsolete by explicit decision,
- historical task context kept for reference,
- no credible restart condition remains.

Destination:

```text
/workspace/<repo-name>-work/archived/YYYYMMDD-<reason>/<task>/
```

Required before archive:

- read `ACTIVE.md`,
- write or preserve summary/notes explaining why it is archived,
- record any extracted work, dataset pointers, or replacement path,
- verify branch/worktree/PR state before removing any worktree,
- keep task context by moving it, not deleting it.

Archived differs from parked:

- `parked/` has a credible restart or extraction condition.
- `archived/` is reference-only unless a future task deliberately mines it.

If useful material has not yet been extracted, prefer `parked/` with substate
`extraction-needed`.

### `investigations/`

Use for standalone investigations not tied to a branch or task lifecycle yet.

Criteria:

- Evidence-gathering, research, or design analysis.
- May later produce a `planned/`, `busy/`, `parked/`, `done/`, or `archived/` task.
- Does not itself own an active product branch unless promoted to `busy/`.

Close-off:

- Keep finished investigation under `investigations/` when it is primarily reference material.
- Promote reusable data products to `/workspace/datasets/`.
- Promote durable learnings to `knowledge/` or shared skills.

## Decision Table

| Question | Destination |
|---|---|
| Is someone actively working it or does it need near-term PR/CI/review action? | `busy/` |
| Is it valuable paused work with a concrete restart/extract condition? | `parked/` |
| Is it accepted/scoped but not started? | `planned/` |
| Is it only a lightweight future idea or reminder? | `later/` |
| Is it complete and summarized? | `done/` |
| Is it closed/superseded/reference-only after extraction or decision? | `archived/` |
| Is it research without a branch/task lifecycle yet? | `investigations/` |

## Positive Archive Rule

Use `detection-platform-metal-work/archived/` for future metal task lifecycle archives.

Treat `/workspace/archive/` as the historical migration/provenance collection described by its own `README.md`.
