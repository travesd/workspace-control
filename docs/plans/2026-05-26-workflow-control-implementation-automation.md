# Workflow-Control Implementation Automation Plan

Date: 2026-05-26

Status: proposed; workspace-control only; not activated live

Related research:

- `docs/research/2026-05-26-implementation-automation-overhaul/README.md`
- `docs/research/2026-05-26-implementation-automation-overhaul/karpathy-github-review.md`
- `docs/research/2026-05-26-implementation-automation-overhaul/chat-history-patterns.md`

Related spec:

- `docs/specs/implementation-automation-kernel.md`

## Objective

Move workspace-control from "agents can resume work" to "agents can turn task
requests into classified, gated, validated implementation runs."

The desired end state is a provider-neutral implementation automation kernel
that can be consumed by Claude, Codex, Pi, and deterministic
`detection-agentic-workflows` tools.

## Non-Goals

- Do not activate new behavior into live `/workspace` without explicit
  approval.
- Do not modify product repos as part of this plan.
- Do not install or activate Pi packages as part of this plan.
- Do not create autonomous push, PR, merge, production, or destructive cleanup
  behavior.
- Do not mine or commit raw provider transcripts.
- Do not replace shared skills; route them through the kernel.

## Core Thesis

The last workspace-control pass solved source-of-truth and resumability. The
next pass should automate the control loop around implementation:

```text
intake -> classify -> preflight -> plan -> execute -> verify -> review -> closeoff
```

This is a systems-leverage change. The highest payoff is not another rule in
`AGENTS.md`; it is a typed state machine and helper tooling that make the right
agent behavior the path of least resistance.

## Workstream A: Casebook And Taxonomy

Goal: convert recent task history into an implementation taxonomy without raw
transcripts.

Inputs:

- `workspace-status --full`
- aggregate Claude/Codex history signals from
  `docs/research/2026-05-26-implementation-automation-overhaul/chat-history-patterns.md`
- recent `done/*/SUMMARY.md`
- active `busy/*/resume.md`
- `SESSIONS.md`
- prior history reviews under
  `docs/research/2026-05-20-workspace-organization/`
- `detection-agentic-workflows-work` task summaries and resumes

Output:

- `docs/research/2026-05-26-implementation-automation-overhaul/casebook.md`

Required fields per case:

- request class;
- repo/task surface;
- actual fulfillment shape;
- failure or friction pattern;
- validation evidence;
- durable learning extracted or missed;
- candidate automation gate.

Acceptance criteria:

- sample at least 15 recent tasks across implementation, review,
  investigation, operating-model, LLM/eval, and agentic-workflows work;
- no raw transcript content;
- each case recommends either "no automation", "checklist", "deterministic
  workflow", or "agent loop".

## Workstream B: Contract And Templates

Goal: make the kernel usable before writing substantial tooling.

Files:

- `docs/specs/implementation-automation-kernel.md`
- `docs/templates/workflow.json`
- `docs/templates/validation-ledger.jsonl.header`
- `docs/templates/implementation-package.md`
- optional update to `docs/templates/resume-packet.md`

Acceptance criteria:

- a new task can be started from the templates without reading this plan;
- each template states required and optional fields;
- approval gates are explicit for push, PR, live activation, destructive
  cleanup, production write, and external write actions;
- templates do not duplicate large instruction blocks from `AGENTS.md`.

Validation:

- `./tools/check-sensitive-content .`
- `./tools/renderctl dry-run`

## Workstream C: `workflowctl` MVP

Goal: add a small host-safe helper that reads artifacts and reports task state.

Files:

- `tools/workflowctl`
- `docs/reference/workflowctl.md` if inline help is not enough

MVP commands:

```text
workflowctl init --kind <kind> --repo <repo> --task-path <path>
workflowctl classify --task-path <path>
workflowctl hydrate --task-path <path>
workflowctl preflight --task-path <path>
workflowctl status --task-path <path>
workflowctl validation add --task-path <path> --command <text> --result <result>
workflowctl validation import --task-path <path>
workflowctl validate --task-path <path>
workflowctl close-check --task-path <path>
```

Behavior:

- writes workflow sidecars only under the selected task path;
- reads `ACTIVE.md`, generated `SESSIONS.md`, task `resume.md`, worktree state,
  and relevant workspace-control specs;
- prints blockers instead of guessing;
- never runs product tests directly on the host;
- never pushes, opens PRs, activates live files, or removes worktrees.

Acceptance criteria:

- can initialize and classify a docs-only workspace-control task;
- can classify one active detection-platform-metal busy task read-only;
- `close-check` identifies missing summary/session/learning-routing fields;
- no secrets or env values are printed.

Validation:

- self-test fixtures under workspace-control, if added;
- `./tools/workflowctl-selftest`;
- `./tools/check-sensitive-content .`;
- `./tools/renderctl dry-run`.

## Workstream C2: Karpathy-Style Experiment Loop

Goal: support bounded autonomous iteration without creating an ungoverned agent.

Inputs:

- mutable surface;
- sealed evaluator;
- budget;
- metric;
- keep/discard rule;
- validation ledger.

Candidate commands:

```text
workflowctl context-pack --task-path <path>
workflowctl experiment init --task-path <path>
workflowctl experiment record --task-path <path> --status keep|discard|crash
```

Rules:

- no autonomous loop unless the evaluator and budget are explicit;
- no destructive keep/discard mechanism unless isolated worktree/branch use is
  explicitly authorized;
- keep `program.md` or workflow prompt changes reviewable as source;
- record complexity delta, not just metric movement.

Acceptance criteria:

- can produce a filtered context pack for one task;
- can append experiment results to a ledger without touching product code;
- can identify when a task is missing a sealed evaluator or keep rule.

## Workstream D: Agentic Workflow Adapter

Goal: let the kernel feed deterministic operator workflows without making Pi or
agentic-workflows the source of truth.

Candidate outputs:

- `workflowctl export --format pi-workflow`
- `workflowctl export --format agentic-runbook`
- `providers/pi/` mapping update
- `detection-agentic-workflows` runbook proposal, only after separate repo task
  setup

Acceptance criteria:

- exported workflow references the same source docs and gates;
- write-side and activation steps remain default-off;
- provider-specific adapters contain only adapter details, not canonical rules.

## Workstream E: Metrics And Feedback

Goal: make automation quality observable.

Metrics:

- median session-start scout commands before actionable work;
- percent of non-trivial tasks classified at intake;
- percent of implementation tasks with validation ledger entries;
- stale busy tasks with missing next action;
- closeoff tasks with durable-learning route recorded;
- repeated correction categories from task summaries and knowledge notes.
- tasks that still require raw provider chat to resume.

Output options:

- `workflowctl metrics --root <work-root>`
- extend `workspace-status --brief` with a tiny automation health section;
- extend `workspace-artifact-inventory` with full automation metrics;
- keep heavy reports in task/investigation artifacts.

## Initial Slice

Recommended first implementation task:

1. Create `casebook.md` from existing task artifacts.
2. Add the three templates in Workstream B.
3. Implement read-only `workflowctl classify` and `workflowctl status`.
4. Use it on one active task and one completed task.
5. Review whether the contract reduced ambiguity or just added paperwork.

This first slice is deliberately read-mostly. It proves the task taxonomy and
artifact shape before any implementation automation starts changing product
code.

## Review Checkpoint

Before live activation or provider adapter work, review:

- scope drift: are we automating task control, or accidentally building a
  second task system?
- safety: are approvals still explicit?
- operator impact: does this reduce repeated instructions and status scouting?
- validation: are gates tied to real commands and artifacts?
- portability: can Claude, Codex, Pi, and deterministic tools consume the same
  contract?
- overhead: does the process scale down for clear tasks?

## Activation Boundary

All work starts in `/workspace/workspace-control`. Live activation requires:

1. clean workspace-control checks;
2. review of repo diff;
3. commit and push only after approval;
4. explicit activation approval;
5. rollback notes;
6. post-activation `renderctl dry-run --mode live-check`.
