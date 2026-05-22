# Layered Repo Organization Review

Date: 2026-05-22

Scope: uncommitted `workspace-control` layered source-layout scaffold under
`core/`, `workspaces/`, `providers/`, plus related activation and maintenance
docs.

Method:

- local diff and source-map review,
- read-only Claude `call-a-friend` review with high reasoning,
- no live workspace activation,
- no Pi activation.

## Findings Fixed

1. `current-workspace/` and `agent-skills/` were described as activation
   outputs in one place and activation sources in another. They are now
   described consistently as the live-compatible sources until render/sync
   tooling exists.
2. The Codex adapter listed `current-workspace/AGENTS.md` as Codex-specific
   source. It now treats that file as shared provider-neutral input, not
   Codex-owned policy.
3. The first-slice plan listed fewer scaffold files than were actually created.
   The plan now enumerates all scaffold README files.
4. The repo-organization layout omitted existing tracked directories, which
   could make future cleanup look like deletion work. The layout now lists the
   known docs, current-workspace, Pi, and pilot areas.
5. The Pi boundary did not give a practical test for `.pi/` versus
   `providers/pi/`. It now gives examples for draft runnable files versus
   adapter design notes and ADR material.
6. Provider adapter docs used "Activation target" wording that could imply
   current live activation. They now say "Future activation target after
   approved sync."
7. `.gitignore` had unanchored workspace-state patterns that could hide future
   layered files. Root runtime-state patterns and product/task-state patterns
   are now anchored.
8. The detection workspace source map only covered the overlay part of
   `AGENTS.md`. It now also names the future core-contract and activation
   reference inputs.

## Validation

Passed:

```bash
git diff --check
./tools/check-sensitive-content .
SKILLCTL_CANONICAL_DIR=/workspace/workspace-control/agent-skills/skills /workspace/tools/skills/skillctl validate
git check-ignore -v workspaces/detection-platform-metal/README.md detection-platform-metal/foo detection-platform-metal-work/busy/foo logs/foo sessions/foo core/templates/logs/foo || true
```

`./tools/knowledgectl lint` returned `errors=0` with the existing legacy seed
note warnings.

## Residual Risks

- The layered directories are scaffold-only; adding real source content before
  render/sync tooling exists can still create drift.
- Live-compatible sources remain manual until render tooling proves clean diffs
  against `current-workspace/` and `agent-skills/`.
- Pi remains draft-only. `.pi/` and `pi-pilot/` must stay out of live
  Claude/Codex activation until a separate Pi package/schema decision is made.
