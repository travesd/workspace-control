# workflowctl Reference

Status: MVP helper; workspace-control only; not live-activated

`tools/workflowctl` is the first implementation automation kernel helper. It
turns a task path into inspectable workflow state and reports missing gates
before an agent edits, validates, or closes work.

The tool is deliberately small and host-safe:

- write commands are limited to the selected task path;
- product tests are never run directly on the host;
- push, PR, live activation, destructive cleanup, production writes, and
  external writes are represented as approval stops, not actions.

## Commands

```text
tools/workflowctl init --task-path <path> [--kind <kind>] [--repo <repo>] [--request <text>] [--force]
tools/workflowctl classify --task-path <path>
tools/workflowctl hydrate --task-path <path> [--source <resume.md>]
tools/workflowctl preflight --task-path <path>
tools/workflowctl status --task-path <path>
tools/workflowctl validation add --task-path <path> --command <text> --result <result> [--package <id>] [--cwd <path>] [--evidence <text>] [--notes <text>]
tools/workflowctl validation import --task-path <path> [--source <resume.md>] [--package <id>]
tools/workflowctl validate --task-path <path>
tools/workflowctl context-pack --task-path <path> [--output <path>|-] [--max-bytes <n>]
tools/workflowctl gate init --task-path <path> [--scope-bucket trivial|standard|wide] [--decision continue-exploration|promote-to-implementation|stop]
tools/workflowctl gate check --task-path <path>
tools/workflowctl gate record --task-path <path> --decision <decision> [--scope-bucket trivial|standard|wide] [--brief <path>] [--prd <path>] [--goal <text>] [--problem <text>] [--write-scope <csv>] [--source-read <csv>] [--validation <csv>]
tools/workflowctl swarm init --task-path <path> --decision none|review-only|parallel-read|parallel-implement [--coordinator <text>] [--loop-cap <text>]
tools/workflowctl swarm check --task-path <path>
tools/workflowctl swarm assign --task-path <path> --lane <id> --role <role> --task <text> [--mutable <csv>] [--sealed <csv>] [--worktree <path>] [--budget <text>] [--preflight <text>] [--stop <csv>] [--handoff <path>]
tools/workflowctl swarm record --task-path <path> --lane <id> --status complete|blocked|discard [--handoff <path>] [--evidence <text>] [--notes <text>]
tools/workflowctl experiment init --task-path <path> --mutable <csv> --sealed-evaluator <csv> --budget <text> --metric <text> --keep-rule <text> [--complexity-delta <text>]
tools/workflowctl experiment check --task-path <path>
tools/workflowctl experiment record --task-path <path> --status keep|discard|crash [--candidate <id>] [--metric <text>] [--evidence <text>] [--complexity-delta <text>] [--notes <text>]
tools/workflowctl export --task-path <path> --format pi-workflow|agentic-runbook|swarm-runbook
tools/workflowctl metrics [--root <path>]
tools/workflowctl close-check --task-path <path>
```

Supported kinds:

```text
implementation, review, investigation, dataset, operating-model, llm-eval, closeoff
```

Supported repos:

```text
workspace-control, detection-platform-metal, detection-agentic-workflows, cross-repo
```

## Artifacts

`init` creates:

```text
<task-path>/workflow.json
<task-path>/validation.jsonl
```

`workflow.json` records the request, repo, task home, classification, mode,
preflight state, mutable/sealed surfaces, implementation gate, swarm routing
contract, stage artifacts, packages, approval stops, and closeoff state.

`validation.jsonl` starts with a header. Validation entries should be appended
by the agent or a future deterministic helper:

```json
{"type":"validation","time":"2026-05-26T00:00:00Z","package":"P0","command":"git diff --check","cwd":"/workspace/workspace-control","result":"pass","evidence":"command output in session","notes":""}
```

`experiment init` creates or preserves:

```text
<task-path>/experiment.jsonl
```

`context-pack` writes a filtered Markdown pack under:

```text
<task-path>/artifacts/context-pack-<timestamp>.md
```

## Command Behavior

`classify` is read-only. It uses `workflow.json` when present, otherwise infers
repo, kind, complexity, risk, thinking mode, automation mode, and approval
checkpoints from the path.

`hydrate` reads `resume.md` or an explicit source file and updates
`workflow.json` with obvious branch, worktree, PR, issue, and fenced validation
plan fields. It accepts common Markdown task labels such as `**Branch:**` and
`**Worktree:**`, and can infer an existing worktree path from an extracted
branch using the workspace branch-to-directory convention. It records the
source path in `preflight.hydrated_from`.

`status` is read-only. It reports whether the task dir, `workflow.json`,
`resume.md`, `SUMMARY.md`, and `validation.jsonl` exist, then summarizes
classification, packages, approval stops, and closeoff fields.

`preflight` is read-only. It checks for active workspace instructions, the
kernel spec, valid workflow JSON, repo/kind fields, a validation plan, declared
worktree existence, and product implementation work without a worktree. It
prints warnings separately from blockers.

`validation add` appends one JSONL validation entry. It records evidence for a
command that was already run by the agent or a safe workspace tool; it does not
execute the command.

`validation import` reads historical evidence from `resume.md` and appends one
conservative JSONL entry with `result="skipped"` and `historical=true`. This
improves handoff without claiming a fresh validation pass. The importer looks
for validation-looking bullets under common resume sections such as
`Validation Results`, `Current Validation`, `Current State`, `Status`, and
`Session Notes`. Re-importing the same source/package is idempotent. `validate`
and `close-check` still require a passing validation entry for implementation
closeoff.

`validate` is read-only. It summarizes validation ledger entries by result and
returns nonzero when entries are missing, no passing entry exists, or failed or
blocked entries are present.

`context-pack` writes or prints a filtered handoff pack containing workflow
summary, task notes, validation ledger, experiment ledger, and worktree status
metadata. It skips sensitive-looking files and records the pack path in
`workflow.json` when writing to disk. The written path is mirrored into
`stage_artifacts.context_pack` and `swarm.shared_context_pack` when the swarm
contract does not already name a pack.

`gate init` creates the `implementation_gate` block when needed. It can leave a
task in `continue-exploration`, or record an initial scope bucket and promotion
decision. If `workflow.json` is missing, it initializes the normal workflow
sidecars first.

`gate record` updates the promotion decision and implementation evidence:
brief/PRD paths, goal, problem statement, source-read evidence, write scope,
sealed surfaces, validation plan, non-goals, open questions, and approval
stops. It records state only; it does not grant approvals or edit product code.

`gate check` is read-only. It returns nonzero until a task is promoted to
implementation with a scope bucket, goal, source-read evidence, write scope,
validation plan, approval stops, and an existing implementation brief. It
prints warnings for suspicious scope/swarm combinations, such as a wide task
with no swarm decision or a trivial task routed to parallel implementation.

`swarm init` records the swarm routing decision. `none` is valid and keeps
`swarm.enabled=false`; `review-only`, `parallel-read`, and
`parallel-implement` require lane assignments before `swarm check` passes.

`swarm assign` upserts a bounded lane with role, task, mutable and sealed
surfaces, worktree, preflight note, stop conditions, budget, and handoff
artifact path. `swarm record` updates a lane status and optional handoff
evidence. Neither command spawns an agent.

`swarm check` is read-only. It validates the router decision, coordinator,
loop cap, lane shape, role/status values, required implementation lane
surfaces, and overlapping mutable surfaces for `parallel-implement`.

`experiment init` updates the workflow with mutable surfaces, sealed evaluator,
budget, metric, keep rule, and complexity-delta notes. `experiment check`
reports missing contract fields. `experiment record` appends keep/discard/crash
results to `experiment.jsonl` only after the contract check passes.

`export` prints a provider-neutral projection for a Pi-style JSON workflow, an
agentic-workflows runbook, or a swarm runbook. It does not write adapter files.

`metrics` summarizes workflow sidecar coverage under a task lifecycle root.

`close-check` is read-only. It checks for closeoff blockers such as missing
workflow state, missing task summary/resume files, missing session index for
task-root work, missing validation entries, and missing durable-learning route.
Docs-only workspace-control paths are allowed to omit task `resume.md` and
`SUMMARY.md`, but still need explicit validation evidence before close.

## Expected First Use

For a new task:

```bash
tools/workflowctl init --task-path /workspace/detection-platform-metal-work/busy/<task>
tools/workflowctl hydrate --task-path /workspace/detection-platform-metal-work/busy/<task>
tools/workflowctl preflight --task-path /workspace/detection-platform-metal-work/busy/<task>
tools/workflowctl status --task-path /workspace/detection-platform-metal-work/busy/<task>
```

For an existing task without sidecars:

```bash
tools/workflowctl classify --task-path /workspace/detection-platform-metal-work/busy/<task>
```

For closeoff:

```bash
tools/workflowctl validate --task-path /workspace/detection-platform-metal-work/busy/<task>
tools/workflowctl close-check --task-path /workspace/detection-platform-metal-work/busy/<task>
```

To preserve historical validation evidence without making it a fresh pass:

```bash
tools/workflowctl validation import --task-path /workspace/detection-platform-metal-work/busy/<task>
```

To promote exploration into implementation:

```bash
tools/workflowctl context-pack --task-path <task>
tools/workflowctl gate record --task-path <task> \
  --decision promote-to-implementation \
  --scope-bucket standard \
  --brief <task>/implementation-brief.md \
  --goal "ship the scoped behavior" \
  --source-read "path/to/source,path/to/test" \
  --write-scope "path/to/module" \
  --validation "container/local-stack validation command"
tools/workflowctl gate check --task-path <task>
```

To plan background work without blocking the coordinator thread:

```bash
tools/workflowctl swarm init --task-path <task> \
  --decision parallel-read \
  --loop-cap "2 blocker review loops"
tools/workflowctl swarm assign --task-path <task> \
  --lane A \
  --role source-read \
  --task "answer the bounded source question" \
  --sealed "path/to/repo-or-doc" \
  --preflight "context pack read" \
  --handoff "<task>/artifacts/swarm/A-handoff.md"
tools/workflowctl swarm check --task-path <task>
tools/workflowctl export --task-path <task> --format swarm-runbook
```

For bounded LLM/eval iteration:

```bash
tools/workflowctl experiment init --task-path <task> \
  --mutable prompts/program.md \
  --sealed-evaluator fixtures/eval.jsonl \
  --budget "3 runs" \
  --metric "accuracy" \
  --keep-rule "keep only if accuracy improves without increasing complexity"
tools/workflowctl experiment record --task-path <task> --status keep --metric "accuracy=0.91"
```

For tool validation:

```bash
tools/workflowctl-selftest
```

## Limits

This MVP does not execute implementation packages, run autonomous loops, mutate
product repos, run product validation commands, publish datasets, push branches,
open PRs, spawn agents, or activate live workspace files. It records and
exports control state so those actions can be performed deliberately by the
right operator or future adapter.
