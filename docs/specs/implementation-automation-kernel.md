# Implementation Automation Kernel

Status: draft in workspace-control; not activated

Date: 2026-05-26

## Purpose

This spec defines a provider-neutral control loop for turning user requests into
recoverable, validated implementation work. It extends the current task
lifecycle and resumability standards without replacing them.

The kernel is intentionally small:

- classify the work;
- choose the thinking and automation mode;
- create the minimum task artifacts;
- gate edits and writes behind explicit preflight checks;
- record validation evidence;
- close the task by extracting durable learnings.

## Scope

In scope:

- workspace-control operating-model work;
- detection-platform-metal implementation, review, investigation, and dataset
  workflows;
- detection-agentic-workflows deterministic JSON-envelope workflows;
- future Pi/agent harness adapters that consume the same contracts.

Out of scope:

- direct product repo execution on the host;
- live activation without approval;
- staging or production validation;
- raw provider transcript storage;
- autonomous push, PR creation, merge, or destructive cleanup.

## State Machine

| State | Purpose | Required Evidence | Exit Gate |
|---|---|---|---|
| `intake` | Capture the user's goal, repo/task scope, constraints, and known approvals. | `workflow.json` or resume packet fields. | Work kind and lifecycle home chosen. |
| `classify` | Determine complexity, risk, domain, and whether the task is clear, complicated, complex, or chaotic. | Classification block with reasons and source paths. | Thinking mode and automation mode selected. |
| `preflight` | Align task dir, worktree, session records, skills, local stack, and validation commands. | Workspace-status output, task path, branch/worktree, skill list, validation plan. | No guardrail violations or explicit blocker recorded. |
| `plan` | Break the work into implementation packages with acceptance gates. | Package list, write scopes, validation commands, rollback notes. | User-approved or agent-owned plan depending on task risk. |
| `execute` | Make scoped edits or run workflow steps. | Diff, run artifacts, command outputs, generated files. | Each package acceptance block green or blocked with evidence. |
| `verify` | Run the container/local-stack checks and review drift. | Validation ledger with commands, timestamps, results, and artifact paths. | Required checks pass or residual risk is explicit. |
| `review` | Evaluate scope, operator impact, missing tests, activation boundary, and durable-learning candidates. | Review checkpoint note. | Findings resolved, accepted, or deferred. |
| `closeoff` | Update resume/summary/session indexes and route learnings. | `SUMMARY.md`, updated `resume.md`, session index, knowledge/skill/ADR decisions. | Task is resumable and lifecycle state is correct. |

The state machine can be implemented as Markdown first, then as JSON-backed
tooling once the shape stabilizes.

## Work Classification

The classifier should be conservative. When unsure, choose the more deliberate
mode.

Fields:

```json
{
  "schema": "workspace-control.implementation-workflow.v0",
  "task": {
    "request": "short user-facing task statement",
    "repo": "workspace-control | detection-platform-metal | detection-agentic-workflows | cross-repo",
    "lifecycle_home": "/workspace/.../busy/<task> or /workspace/workspace-control/docs/..."
  },
  "classification": {
    "kind": "implementation | review | investigation | dataset | operating-model | llm-eval | closeoff",
    "complexity": "clear | complicated | complex | chaotic",
    "risk": ["product-code", "workspace-rules", "write-side", "data-product"],
    "reason": "why this routing was chosen"
  },
  "mode": {
    "thinking": ["recognition", "deliberate-engineering"],
    "automation": "checklist | deterministic-workflow | agent-loop",
    "human_checkpoints": ["before-push", "before-live-activation"]
  }
}
```

## Mode Router

| Situation | Thinking Mode | Automation Mode | Default Tooling |
|---|---|---|---|
| Known repeated workspace procedure | Recognition | Checklist | shared skill + current live tool |
| Normal code implementation | Deliberate engineering | Deterministic workflow | task plan + worktree + container validation |
| Vague product/design request | Divergent-convergent design | Deterministic workflow until scoped | research note + plan |
| LLM quality, rubric, classifier policy, corpus generation | Experimental complex-systems | Deterministic workflow plus evaluator loops | experiment log + fixtures + disagreement examples |
| Workspace operating-model change | Systems-leverage | Reviewable docs/specs first | workspace-control plan/spec + activation boundary |
| Unpredictable multi-step coding or search task | Governed agent | Agent loop with stop conditions | provider harness or Pi adapter, sandboxed |
| Broken/chaotic environment | Stabilization | Manual/operator-assisted checklist | status, blockers, rollback notes |

## Gate Types

| Gate | Purpose | Examples |
|---|---|---|
| `source-read` | Prevent implementation from guesses. | Code paths read, docs read, schema inspected. |
| `scope` | Bound files, repos, and task artifacts. | Worktree path, write set, non-goals. |
| `safety` | Enforce workspace guardrails. | No host product tests, no secret printing, no production validation. |
| `approval` | Stop before operations requiring user authorization. | Push, PR, merge, live activation, destructive cleanup, external writes. |
| `validation` | Prove behavior. | Docker compose test, local stack check, render dry-run, browser review. |
| `artifact` | Preserve evidence. | Screenshots, JSONL outputs, run dirs, dataset manifests. |
| `learning` | Route reusable findings. | Knowledge note, skill draft, ADR, task summary only. |

## Experiment Contract

Autonomous or semi-autonomous iteration is allowed only when the task has a
small enough world to measure and reverse.

Required fields for experimental or agent-loop tasks:

| Field | Purpose |
|---|---|
| `mutable_surface` | Files, configs, prompts, or data products the agent may change. |
| `sealed_evaluator` | Code, fixture, metric, or validation path the agent must not modify. |
| `budget` | Time, cost, run count, token, API, or compute limit. |
| `metric` | The primary measurement that decides improvement. |
| `keep_rule` | The rule for keeping, reverting, or discarding a candidate. |
| `complexity_delta` | Qualitative cost of the change when the metric ties or improves only slightly. |

This mirrors the useful part of Karpathy-style autoresearch: shrink the
environment, fix the evaluator, measure every attempt, and keep or discard
based on the ledger. Do not copy destructive git-reset loops into this
workspace unless the task explicitly authorizes an isolated branch/worktree
experiment.

## Tool Shape

The initial helper should be `tools/workflowctl` in `workspace-control`.
Implement it incrementally and keep it host-safe.

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
workflowctl context-pack --task-path <path>
workflowctl experiment init --task-path <path>
workflowctl experiment check --task-path <path>
workflowctl experiment record --task-path <path> --status keep|discard|crash
workflowctl export --format pi-workflow --task-path <path>
workflowctl export --format agentic-runbook --task-path <path>
workflowctl metrics --root <work-root>
workflowctl close-check --task-path <path>
```

`hydrate` may infer an existing worktree path from a parsed branch name using
the workspace worktree directory convention. Historical validation imports are
conservative handoff evidence only: they use `skipped`/`historical=true`, are
idempotent for the same source/package, and must not satisfy fresh validation
gates.

Later commands can execute or integrate with adapters, after separate approval:

```text
workflowctl package run --task-path <path> --package <id>
workflowctl export --format pi-workflow --task-path <path> --output <path>
workflowctl export --format agentic-runbook --task-path <path> --output <path>
```

The tool should read live state and task artifacts. It should not execute
product tests directly on the host, mutate product repos, push branches, or
activate live workspace files.

`context-pack` should render a bounded task/worktree slice for human or LLM
review. It must apply the same secret and large-file filters as the rest of the
workspace-control tooling.

## Artifact Convention

For task dirs, add a machine-readable sidecar only when useful:

```text
busy/<task>/
  resume.md
  notes.md
  workflow.json
  validation.jsonl
  artifacts/
```

For workspace-control docs-only work, the plan/spec/research document can be
the canonical artifact until a task dir exists.

`workflow.json` should summarize current state, not duplicate all notes. Raw
tool output stays in task artifacts or generated run directories.

## Quality Attributes

The kernel should optimize for:

- recoverability: a fresh agent can resume without raw chat;
- verifiability: claims are backed by commands, paths, or source URLs;
- safety: prohibited actions are impossible or stopped at gates;
- portability: Claude, Codex, Pi, and future harnesses consume the same
  provider-neutral contract;
- low overhead: clear tasks should not require a ceremony-heavy process;
- evolvability: new workflows can add gates without rewriting the core loop.

## Metrics

Track during workspace hygiene reviews:

- percent of non-trivial tasks with `workflow.json` or equivalent classified
  resume packet;
- median commands before first useful implementation action;
- validation gates completed per implementation task;
- closeoff tasks with durable-learning routing recorded;
- stale busy tasks by age and missing next action;
- repeated user corrections by category;
- tasks that still require raw chat to resume.

Metrics are signals. If agents skip the contract, reduce friction. If resumed
tasks still require chat, strengthen the relevant gate.

## Relationship To Existing Specs

- `docs/specs/task-lifecycle.md` defines where task state lives.
- `docs/specs/task-resumability.md` defines how task state is recoverable.
- This spec defines how a task moves from request to implementation to verified
  closeoff.

The three specs should remain separate. Lifecycle is storage, resumability is
handoff, and implementation automation is execution control.
