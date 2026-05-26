# workflowctl Kernel Completion Review

Date: 2026-05-26

Status: draft implementation complete in `workspace-control`; not live-activated

## Scope Reviewed

This review covers the implementation automation kernel draft and local helper
tooling added under `workspace-control`:

- `tools/workflowctl`
- `tools/workflowctl-selftest`
- `docs/specs/implementation-automation-kernel.md`
- `docs/reference/workflowctl.md`
- `docs/templates/workflow.json`
- `docs/templates/validation-ledger.jsonl.header`
- `docs/templates/implementation-package.md`
- `docs/plans/2026-05-26-workflow-control-implementation-automation.md`
- `docs/research/2026-05-26-implementation-automation-overhaul/`

## Findings

No blocking issues were found for the draft kernel staying inside
`workspace-control`.

Residual risks:

- `workflowctl` is a Bash/JQ MVP. It is intentionally small, but additional
  command surface will eventually need fixture-based tests if it becomes a
  live dependency.
- `context-pack` includes bounded excerpts from task files and git status/stat
  metadata. It skips sensitive-looking filenames, but it is not a full content
  classifier.
- `metrics` currently reports sidecar coverage. It does not yet grade workflow
  quality or validation depth.
- live task coverage is currently zero: existing task dirs do not yet have
  `workflow.json` sidecars. That is expected before activation.
- existing layered-source drift in `current-workspace/AGENTS.md` was resolved
  by updating `workspaces/detection-platform-metal/AGENTS.overlay.md` to
  preserve the current multi-repo Detection Platform ecosystem contract.

## Scope Drift Check

The implementation remains a control kernel, not a second task system.

It records:

- task classification;
- mode routing;
- validation evidence;
- context packs;
- bounded experiment contracts;
- provider export projections;
- closeoff blockers.

It does not:

- run product tests;
- mutate product repos;
- push branches;
- open PRs;
- publish datasets;
- activate live workspace files;
- perform destructive cleanup;
- run autonomous implementation loops.

## Safety Check

Approval boundaries are explicit in `workflow.json` and surfaced by
`workflowctl status`. Write commands only write under the selected task path.
External actions remain blocked by process, not hidden behind command flags.

## Operator Impact

The kernel directly targets the repeated chat-history patterns:

- classification before extended work;
- preflight before edits;
- validation ledger before completion claims;
- context pack before handoff;
- experiment contract before LLM/eval iteration;
- close-check before lifecycle movement.

This should reduce repeated instruction reminders once live task sidecars are
introduced.

## Portability Check

The source artifacts remain provider-neutral. `export --format pi-workflow` and
`export --format agentic-runbook` are projections from `workflow.json`; they do
not make Pi or agentic-workflows the source of truth.

## Validation Evidence

Commands run:

```text
bash -n tools/workflowctl tools/workflowctl-selftest
./tools/workflowctl-selftest
./tools/check-sensitive-content .
git diff --check
jq empty docs/templates/workflow.json
./tools/knowledgectl index --check
./tools/knowledgectl lint
./tools/workflowctl metrics --root /workspace/detection-platform-metal-work
./tools/renderctl dry-run
./tools/renderctl dry-run --out <tmp-generated-root>
SKILLCTL_CANONICAL_DIR=/workspace/workspace-control/agent-skills/skills /workspace/tools/skills/skillctl validate
SKILLCTL_CANONICAL_DIR=<generated-root>/agent-skills/skills /workspace/tools/skills/skillctl validate
```

Results:

- shell syntax: pass;
- `workflowctl-selftest`: pass;
- sensitive content check: pass;
- whitespace diff check: pass;
- workflow template JSON: pass;
- knowledge index check: pass;
- knowledge lint: pass with the existing 9 weak-provenance warnings;
- workflow metrics: pass and reports 45 metal task dirs, 0 workflow sidecars;
- render dry-run: pass;
- shared skill validation: pass for checked-in canonical skills and generated
  rendered skills.

## Completion Boundary

The draft implementation automation kernel is complete enough for review in
`workspace-control`.

Not complete without separate approval:

1. commit and push the workspace-control changes;
2. activate helper tooling into `/workspace/tools`;
3. pilot `workflowctl init` on a small number of live task dirs;
4. update live workspace instructions only after the pilot proves the overhead
   is acceptable.
