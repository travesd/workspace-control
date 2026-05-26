# workflowctl Five-Task Pilot

Date: 2026-05-26

Status: pilot complete; no live activation

## Pilot Targets

| Surface | Task Path | Kind | Final Result |
|---|---|---|---|
| Metal classifier-results browser | `/workspace/detection-platform-metal-work/busy/classifier-results-browser` | `implementation` | preflight passed; closeoff blocked correctly |
| Metal AI evaluator v1 | `/workspace/detection-platform-metal-work/busy/ai-evaluator-incidents-page-v1` | `implementation` | preflight passed; closeoff blocked correctly |
| Metal PR #34 review | `/workspace/detection-platform-metal-work/busy/review-pr-34-tlsh-minhash` | `review` | preflight passed; closeoff blocked on missing summary |
| Metal client threat-intel reports | `/workspace/detection-platform-metal-work/busy/client-threat-intel-reports` | `implementation` | preflight blocked on missing worktree |
| Agentic daily-result-review conversion | `/workspace/detection-agentic-workflows-work/busy/convert-evaluator-audit-to-agentic-workflows` | `implementation` | preflight passed; closeoff blocked correctly |

Command outputs were captured under:

```text
/workspace/workspace-control/docs/reviews/artifacts/2026-05-26-workflowctl-five-task-pilot/
```

Final context packs were generated at:

```text
/workspace/detection-platform-metal-work/busy/classifier-results-browser/artifacts/context-pack-20260526T211153Z.md
/workspace/detection-platform-metal-work/busy/ai-evaluator-incidents-page-v1/artifacts/context-pack-20260526T211153Z.md
/workspace/detection-platform-metal-work/busy/review-pr-34-tlsh-minhash/artifacts/context-pack-20260526T211153Z.md
/workspace/detection-platform-metal-work/busy/client-threat-intel-reports/artifacts/context-pack-20260526T211154Z.md
/workspace/detection-agentic-workflows-work/busy/convert-evaluator-audit-to-agentic-workflows/artifacts/context-pack-20260526T211154Z.md
```

## Commands Run

Initial pass for each target:

```text
workflowctl init --task-path <task> --repo <repo> --kind <kind>
workflowctl hydrate --task-path <task>
workflowctl preflight --task-path <task>
workflowctl validation import --task-path <task>
workflowctl validate --task-path <task>
workflowctl context-pack --task-path <task> --max-bytes 7000
workflowctl close-check --task-path <task>
```

The first pass exposed resume-shape gaps, so the pilot also patched and reran:

```text
workflowctl hydrate --task-path <task>
workflowctl validation import --task-path <task>
workflowctl preflight --task-path <task>
workflowctl validate --task-path <task>
workflowctl context-pack --task-path <task> --max-bytes 7000
workflowctl close-check --task-path <task>
```

Metrics were captured for both task roots after the final rerun.

## Results

### Hydration

Final hydrate results:

| Task | Branch | Worktree | PR |
|---|---|---|---|
| classifier-results browser | `feat/classifier-results-browser-pr` | `/workspace/detection-platform-metal.worktrees/feat-classifier-results-browser-pr` | PR #104 |
| AI evaluator v1 | `feat/ai-evaluator-incidents-page-v1` | `/workspace/detection-platform-metal.worktrees/feat-ai-evaluator-incidents-page-v1` | none |
| PR #34 review | `add-minhash-tlsh-hashing` | `/workspace/detection-platform-metal.worktrees/add-minhash-tlsh-hashing` | PR #34 |
| client threat-intel reports | none | none | none |
| agentic daily-result-review | `feat/daily-result-review` | `/workspace/detection-agentic-workflows.worktrees/feat-daily-result-review/` | none |

The rerun validated two fixes made during the pilot:

- bold labels such as `**Branch:**` and `**Worktree:**` are parsed;
- an extracted branch can infer an existing worktree from the workspace
  branch-directory convention.

### Validation Import

Final historical import results:

| Task | Evidence Items | Import Result |
|---|---:|---|
| classifier-results browser | 10 | `skipped`, historical |
| AI evaluator v1 | 4 | `skipped`, historical |
| client threat-intel reports | 4 | `skipped`, historical |
| agentic daily-result-review | 2 | already imported, historical |
| PR #34 review | 0 | no historical evidence found |

The rerun validated two more fixes:

- historical evidence can be imported from common resume sections such as
  `Current State`, `Status`, and plain `Current validation:`;
- importing the same source/package is idempotent.

`validate` still failed for every target because none had a fresh `pass` entry.
That is correct: imported historical evidence is handoff context, not closeoff
proof.

### Preflight And Close-Check

Four targets passed preflight after parser fixes:

- classifier-results browser;
- AI evaluator v1;
- PR #34 review;
- agentic daily-result-review conversion.

The client threat-intel report task remained blocked because it was initialized
as `implementation` but its resume has no branch or worktree. This is useful
signal: report/prototype tasks need either a declared worktree or a more accurate
task kind before implementation closeoff rules should apply.

Close-check results were appropriately conservative:

- implementation tasks with only historical evidence blocked on no passing
  validation entries;
- implementation tasks without `SUMMARY.md` also blocked on missing summary;
- the review task treated missing validation as a warning but blocked on missing
  `SUMMARY.md`.

## Metrics After Final Rerun

Metal task root:

```text
task_dirs: 45
with_workflow_json: 5
with_validation_jsonl: 5
with_validation_entries: 4
with_passing_validation: 0
with_context_pack: 5
```

Agentic-workflows task root:

```text
task_dirs: 2
with_workflow_json: 2
with_validation_jsonl: 2
with_validation_entries: 2
with_passing_validation: 0
with_context_pack: 2
```

## Assessment

The kernel is now useful as a task-orientation and closeoff guardrail:

- it can hydrate current branch/worktree/PR state from varied existing resumes;
- it creates compact context packs that a fresh agent can use without transcript
  lookup as the first step;
- it preserves historical validation evidence without weakening the fresh-pass
  gate;
- it surfaces stale or underspecified task metadata as actionable blockers.

Do not activate it into always-loaded live instructions yet. The next safe step
is a small activation draft that makes `workflowctl status`, `hydrate`,
`preflight`, and `context-pack` recommended for non-trivial resumed tasks, while
keeping `validation import`, `validate`, and `close-check` as explicit operator
or closeoff tools.
