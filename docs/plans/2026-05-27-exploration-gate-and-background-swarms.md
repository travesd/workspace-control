# Exploration Gate And Background Swarms Plan

Date: 2026-05-27

Status: proposed; workflowctl MVP implemented in workspace-control; not activated live

Related research:

- `docs/research/2026-05-27-exploration-to-implementation-swarms/README.md`

Related existing work:

- `docs/specs/implementation-automation-kernel.md`
- `docs/reviews/2026-05-26-workflowctl-five-task-pilot.md`
- `tools/workflowctl`

## Objective

Preserve exploratory code conversations while preventing accidental,
under-scoped implementation. Add a lightweight gate that turns exploration into
an implementation brief or PRD before edits begin, then route non-trivial
implementation through a provider-neutral background-agent contract.

In practice, this should feel like a short mode switch, not a ceremony wall:

```text
explore freely -> size scope -> write brief -> choose swarm lanes -> preflight
-> dispatch workers -> coordinator integrates -> fresh validation -> review
```

## Non-Goals

- Do not suppress exploratory code discussion.
- Do not activate new always-loaded instructions in `/workspace` in this slice.
- Do not add autonomous product-code execution.
- Do not push, open PRs, merge, live-activate, remove worktrees, or run
  destructive cleanup without explicit approval.
- Do not require a full PRD for one-file fixes.
- Do not make background agents share the same write scope without isolation.
- Do not copy provider-specific tmux automation or standing auto-merge behavior
  from reference skills into workspace-control.

## Core Rule

Exploration is conversational. Implementation is contractual.

When exploration turns into implementation, stop before edits and create an
implementation brief with:

- goal;
- context and source-read evidence;
- non-goals;
- assumptions and open questions;
- write scope;
- sealed surfaces;
- implementation packages;
- validation plan;
- approval stops;
- swarm routing decision.

Use the PRD addendum only for product-facing or cross-cutting features.

## Scope Buckets

Every promoted implementation gets one of three buckets:

| Bucket | Definition | Default Swarm Decision |
|---|---|---|
| `trivial` | one file, small diff, obvious existing pattern | `none` or `review-only` |
| `standard` | 2-5 files or one subsystem | `parallel-read` plus review/validation lane |
| `wide` | cross-subsystem, schema/API/UI, LLM/eval, workspace-control | `parallel-implement` only with disjoint write scopes or separate worktrees |

The bucket controls overhead. Trivial tasks should not need a full PRD. Wide
tasks should not proceed from chat directly into edits.

## Stage Artifacts

Use task-local artifacts instead of hidden provider-specific state:

```text
busy/<task>/
  implementation-brief.md
  workflow.json
  validation.jsonl
  artifacts/
    swarm/<lane-id>-brief.md
    swarm/<lane-id>-handoff.md
    review/<iteration>.md
```

The operator-facing brief stays concise. Worker lane briefs and context packs
carry detailed file paths, commands, and acceptance criteria.

## Workstream A: Contract And Templates

Files:

- `docs/templates/implementation-brief.md`
- `docs/specs/implementation-automation-kernel.md`
- `docs/templates/workflow.json`
- `docs/templates/resume-packet.md`

Changes:

- add `implementation_gate` to the workflow contract;
- add `swarm` to the workflow contract;
- add scope bucket and stage artifact fields;
- add an `Implementation Gate` block to the resume packet template;
- document when a brief is enough versus when a PRD addendum is required.

Acceptance:

- a fresh agent can identify whether it is still exploring or cleared to edit;
- the brief template supports small changes without full PRD overhead;
- the PRD addendum is available for larger product behavior changes.
- the human-facing plan is short enough to review, while worker artifacts carry
  detailed handoff instructions.

## Workstream B: workflowctl Gate MVP

Commands:

```text
workflowctl gate init --task-path <path>
workflowctl gate check --task-path <path>
workflowctl gate record --task-path <path> --decision <decision> --brief <path>
```

Behavior:

- `gate init` writes default `implementation_gate` fields under
  `workflow.json`;
- `gate check` blocks implementation when goal, source-read evidence, write
  scope, validation plan, or approval stops are missing;
- `gate check` warns when the scope bucket and requested swarm routing are
  inconsistent;
- `gate record` records the promotion decision and brief/PRD path.

Acceptance:

- docs-only exploration can remain exploration without forcing product worktree
  setup;
- implementation tasks cannot pass the gate with an empty write scope;
- gate check reports blockers without mutating product code.
- `trivial` tasks can pass with `swarm.router_decision=none`.

## Workstream C: Swarm Contract MVP

Commands:

```text
workflowctl swarm init --task-path <path> --decision <decision>
workflowctl swarm check --task-path <path>
workflowctl swarm assign --task-path <path> --lane <id> --role <role> --task <text>
workflowctl swarm record --task-path <path> --lane <id> --status <status> --handoff <path>
workflowctl export --task-path <path> --format swarm-runbook
```

Behavior:

- every non-trivial implementation records a swarm routing decision;
- `none` is valid for clear one-file changes;
- `review-only`, `parallel-read`, and `parallel-implement` require lane
  definitions;
- implementation lanes require mutable and sealed surfaces;
- parallel implementation requires disjoint write scopes or separate worktrees;
- implementation lanes require a worker preflight result before dispatch;
- review loops only continue on blocker findings and must have a loop cap;
- forbidden actions remain push, PR, merge, live activation, production write,
  external write, and destructive cleanup.

Acceptance:

- a coordinator can queue bounded background work without losing the main
  conversation;
- workers return structured handoff artifacts;
- `swarm check` catches missing or overlapping mutable surfaces.
- `swarm check` catches missing worker preflight and missing loop caps.

## Workstream D: Worker Preflight

Before any implementation worker starts, record a blocking preflight:

- task path and branch/worktree;
- context pack path;
- mutable and sealed surfaces;
- validation command availability;
- container/local-stack route for product validation;
- forbidden actions;
- budget and stop conditions.

Do not adopt host dependency installs from reference SDLC skills for product
repos. Product validation still goes through containers and local stacks.

## Workstream E: Pilot

Pilot targets:

1. one exploratory conversation promoted to product implementation;
2. one clear one-file implementation;
3. one cross-cutting UI/API implementation;
4. one workspace-control operating-model change.

Measure:

- time from "proceed" to approved brief;
- number of ambiguous edits prevented;
- whether background lanes reduce main-thread waiting;
- conflicts introduced by background workers;
- whether validation ledgers still require fresh pass entries.
- whether the scope bucket reduced unnecessary exploration.

## Workstream F: Activation Draft

Only after the pilot, draft a live activation update that says:

- agents may explore conversationally;
- before non-trivial product edits, agents must create or update an
  implementation brief;
- background agents are recommended for non-trivial implementation but must use
  the swarm contract;
- the coordinator remains responsible for final integration and validation.

Activation still requires explicit approval and rollback notes.

## Review Checkpoint

Before activation, review:

- does the gate reduce accidental implementation or just add paperwork?
- does the swarm contract reduce blocking time without increasing conflicts?
- are approval stops still explicit?
- can a fresh agent resume from `workflow.json`, the brief, and context pack?
- do simple tasks remain simple?
- did background workers reduce waiting without hiding important decisions from
  the coordinator?
