# workflowctl Three-Task Pilot

Date: 2026-05-26

Status: pilot complete; no live activation

## Pilot Targets

| Surface | Task Path | Kind | Result |
|---|---|---|---|
| Workspace-control docs/research | `/workspace/workspace-control/docs/research/2026-05-26-implementation-automation-overhaul` | `investigation` | closeable with warnings |
| Detection-platform-metal active task | `/workspace/detection-platform-metal-work/busy/brand-automation-corpus-llm-workers` | `llm-eval` | closeoff blocked correctly |
| Detection-agentic-workflows active task | `/workspace/detection-agentic-workflows-work/busy/brand-automation-extraction` | `implementation` | closeoff blocked correctly |

Command outputs were captured under:

```text
/workspace/workspace-control/docs/reviews/artifacts/2026-05-26-workflowctl-three-task-pilot/
```

Context packs were generated at:

```text
/workspace/workspace-control/docs/research/2026-05-26-implementation-automation-overhaul/artifacts/context-pack-20260526T201558Z.md
/workspace/detection-platform-metal-work/busy/brand-automation-corpus-llm-workers/artifacts/context-pack-20260526T201558Z.md
/workspace/detection-agentic-workflows-work/busy/brand-automation-extraction/artifacts/context-pack-20260526T201558Z.md
```

## Commands Run

For each target:

```text
workflowctl init --task-path <task>
workflowctl preflight --task-path <task>
workflowctl context-pack --task-path <task> --max-bytes 5000
workflowctl close-check --task-path <task>
```

Additional metrics:

```text
workflowctl metrics --root /workspace/detection-platform-metal-work
workflowctl metrics --root /workspace/detection-agentic-workflows-work
```

## Results

### Workspace-Control Docs Task

`preflight` passed with one expected warning:

- `resume.md missing`

`close-check` passed with warnings:

- closeoff cleanup decision empty;
- docs-only path may intentionally omit `resume.md` and `SUMMARY.md`;
- no validation entries recorded for an investigation task.

This is the desired behavior for docs/research work. It avoids forcing task-dir
ceremony where the document set is itself the artifact.

### Metal Task

`preflight` passed with no warnings or blockers.

`close-check` blocked closeoff on:

- `SUMMARY.md missing`;
- no validation entries recorded.

This is the desired high-level behavior. The task `resume.md` contains a lot of
validation history, but `validation.jsonl` is empty because the pilot did not
import prior evidence. That makes the missing machine-readable ledger visible
without pretending the task is unvalidated.

### Agentic-Workflows Task

`preflight` passed with no warnings or blockers.

`close-check` blocked closeoff on:

- `SUMMARY.md missing`;
- no validation entries recorded.

This is also useful. The task has strong resume evidence, but the kernel
correctly distinguishes narrative validation from ledgered validation.

## Metrics After Pilot

Metal task root:

```text
task_dirs: 45
with_workflow_json: 1
with_validation_jsonl: 1
with_validation_entries: 0
with_context_pack: 1
```

Agentic-workflows task root:

```text
task_dirs: 2
with_workflow_json: 1
with_validation_jsonl: 1
with_validation_entries: 0
with_context_pack: 1
```

## What Worked

- Classification was accurate enough when kind/repo were explicit.
- Preflight produced low-noise results across all three surfaces.
- Context packs were compact enough to scan: 143 lines for docs, 295 for metal,
  and 238 for agentic-workflows.
- Close-check caught the right closeoff blockers for active implementation
  work.
- The sidecar model made the absence of machine-readable validation evidence
  visible without disturbing existing task notes.

## Friction And Follow-Up

1. `workflow.json` does not hydrate branch, worktree, validation history, or
   durable-learning route from `resume.md`.

   Recommended next slice: add `workflowctl hydrate --task-path <task>` or
   `workflowctl init --from-resume` to parse obvious resume fields and preserve
   the extracted values for review.

2. Historical validation remains narrative-only.

   Recommended next slice: add a conservative `workflowctl validation import`
   mode that can create `skipped` or `historical-evidence` ledger entries from
   explicit operator-selected resume sections, without claiming fresh pass
   status.

3. `closeoff.durable_learning_route` defaults to `none`.

   This is acceptable for small tasks, but for non-trivial implementation work
   `close-check` should probably warn when the route is still the default.

4. `context-pack` initially snapshotted `workflow.json` before recording the
   generated context-pack path.

   Fixed during the pilot: `workflowctl` now records `surfaces.context_pack`
   before rendering the pack, and the three packs were regenerated.

## Recommendation

Do not activate `workflowctl` into always-loaded instructions yet.

Proceed with a second pilot after two small improvements:

1. add resume hydration for branch/worktree and validation-plan fields;
2. add conservative validation import for historical evidence.

After that, pilot on five more active tasks and compare:

- commands before useful orientation;
- whether closeoff blockers are actionable;
- whether a fresh agent can resume from the context pack without transcript
  lookup.
