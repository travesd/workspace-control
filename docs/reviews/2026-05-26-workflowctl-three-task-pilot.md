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
/workspace/detection-platform-metal-work/busy/brand-automation-corpus-llm-workers/artifacts/context-pack-20260526T204341Z.md
/workspace/detection-agentic-workflows-work/busy/brand-automation-extraction/artifacts/context-pack-20260526T204341Z.md
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

Second slice commands:

```text
workflowctl hydrate --task-path <task>
workflowctl validation import --task-path <task>
workflowctl validate --task-path <task>
workflowctl close-check --task-path <task>
workflowctl context-pack --task-path <task> --max-bytes 5000
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

Second slice result: `hydrate` failed as expected because this docs/research
directory intentionally has no `resume.md`.

### Metal Task

`preflight` passed with no warnings or blockers.

`close-check` blocked closeoff on:

- `SUMMARY.md missing`;
- no validation entries recorded.

This is the desired high-level behavior. The task `resume.md` contains a lot of
validation history, but `validation.jsonl` is empty because the pilot did not
import prior evidence. That makes the missing machine-readable ledger visible
without pretending the task is unvalidated.

Second slice result:

- `hydrate` extracted branch
  `feat/brand-automation-corpus-llm-workers` and worktree
  `/workspace/detection-platform-metal.worktrees/feat-brand-automation-corpus-llm-workers`.
- `hydrate` found no fenced validation plan entries in `resume.md`.
- `validation import` captured 12 historical evidence items as one
  `skipped` ledger entry with `historical=true`.
- `validate` still failed because there were zero passing entries.
- `close-check` still blocked closeoff on `SUMMARY.md missing` and no passing
  validation entries.

### Agentic-Workflows Task

`preflight` passed with no warnings or blockers.

`close-check` blocked closeoff on:

- `SUMMARY.md missing`;
- no validation entries recorded.

This is also useful. The task has strong resume evidence, but the kernel
correctly distinguishes narrative validation from ledgered validation.

Second slice result:

- `hydrate` extracted branch `main` and 6 fenced validation plan entries.
- `validation import` captured 10 historical evidence items as one
  `skipped` ledger entry with `historical=true`.
- `validate` still failed because there were zero passing entries.
- `close-check` still blocked closeoff on `SUMMARY.md missing` and no passing
  validation entries.

## Metrics After Pilot

Metal task root:

```text
task_dirs: 45
with_workflow_json: 1
with_validation_jsonl: 1
with_validation_entries: 1
with_passing_validation: 0
with_context_pack: 1
```

Agentic-workflows task root:

```text
task_dirs: 2
with_workflow_json: 1
with_validation_jsonl: 1
with_validation_entries: 1
with_passing_validation: 0
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
- Resume hydration extracted useful branch/worktree/validation-plan fields when
  `resume.md` had predictable headings.
- Historical validation import improved handoff while preserving a hard
  distinction between old narrative evidence and fresh passing validation.

## Friction And Follow-Up

1. Resume hydration is useful but intentionally syntax-dependent.

   It extracted fields from the two active task resumes, but the metal task had
   no fenced validation plan for the parser to preserve. This is acceptable for
   the kernel, and points to a future task-resume template improvement rather
   than broader parsing.

2. Historical validation import is conservative enough for pilot use.

   Imported entries use `result="skipped"` and `historical=true`; `validate` and
   `close-check` correctly require a separate `pass` entry before closeoff.

3. `closeoff.durable_learning_route` defaults to `none`.

   This is acceptable for small tasks, but for non-trivial implementation work
   `close-check` should probably warn when the route is still the default.

4. `context-pack` initially snapshotted `workflow.json` before recording the
   generated context-pack path.

   Fixed during the pilot: `workflowctl` now records `surfaces.context_pack`
   before rendering the pack, and the three packs were regenerated.

## Recommendation

Do not activate `workflowctl` into always-loaded instructions yet.

The two planned second-slice improvements are now implemented and passed this
pilot. Proceed with a broader five-task pilot before activation, and compare:

- commands before useful orientation;
- whether closeoff blockers are actionable;
- whether a fresh agent can resume from the context pack without transcript
  lookup.
