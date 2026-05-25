# Layered Repo Organization Plan

Date: 2026-05-22

Status: first implementation slice proposed

## Objective

Restructure `workspace-control` around a layered source model:

- light core configuration and skills,
- detection-platform-metal overlays,
- provider adapters for Claude, Codex, and Pi,
- compatibility outputs for the current live workspace.

## Non-Goals

- Do not move live workspace files in this slice.
- Do not move canonical skills out of `agent-skills/skills/` yet.
- Do not activate Pi.
- Do not change product repos, task directories, or provider credentials.

## Slice 1: Scaffolding And Source Maps

Add:

- `docs/specs/repo-organization.md`,
- `core/README.md`,
- `core/skills/README.md`,
- `core/specs/README.md`,
- `core/templates/README.md`,
- `workspaces/README.md`,
- `workspaces/detection-platform-metal/README.md`,
- `workspaces/detection-platform-metal/skills/README.md`,
- `workspaces/detection-platform-metal/specs/README.md`,
- `workspaces/detection-platform-metal/profiles/README.md`,
- `workspaces/detection-platform-metal/tools/README.md`,
- `providers/README.md`,
- `providers/{claude,codex,pi}/README.md`.

Update:

- top-level `README.md`,
- `MAINTENANCE.md`,
- `ACTIVATION.md`.

No canonical source moves.

## Slice 2: Render/Sync Design

Design a deterministic render path. The first conservative command is
`tools/renderctl dry-run`, which proves the current compatibility outputs can
be regenerated from existing compatibility sources before any canonical moves.
It now also supports instruction composition from draft layered inputs.
Skill composition from draft layered inputs is also supported.

Target future render path:

```text
core + workspace overlay + activation references -> current-workspace/AGENTS.md
core skills + workspace skills -> agent-skills/skills
provider adapter -> provider mirrors/config examples
```

Before any move, build a dry-run command that reports:

- source files selected,
- generated target paths,
- diff against current checked-in outputs,
- validation commands to run.

## Slice 3: Skill Split

Current status: draft skill copies exist under `core/skills/` and
`workspaces/detection-platform-metal/skills/`, and `tools/renderctl dry-run
--mode skills` verifies that they generate the current compatibility tree.
The core copies are not all portable yet; see
`docs/reviews/2026-05-25-core-skill-portability-audit.md`.

Before activation:

1. Audit core-candidate skills for `/workspace` and detection assumptions.
2. Split or parameterize non-portable core skill content.
3. Generate `agent-skills/skills/` from both sources.
4. Confirm generated tree matches the current live-compatible tree.
5. Only then remove duplicated compatibility copies.

## Slice 4: Instruction Split

Split `current-workspace/AGENTS.md` into:

- core contract,
- detection-platform-metal overlay,
- activation reference block.

Render the combined output back to `current-workspace/AGENTS.md` and verify it
matches live `/workspace/AGENTS.md` before activation.

## Slice 5: Provider Adapters

Claude:

- keep `current-workspace/CLAUDE.md` as a thin wrapper,
- add provider-specific mapping in `providers/claude/`.

Codex:

- move project-local config examples to `providers/codex/`,
- add custom-agent profile mapping only after review.

Pi:

- keep `.pi/` and `pi-pilot/` draft-only,
- map Pi agents/workflows back to core/workspace source files,
- require separate package/schema ADR before activation.

## Validation

Each slice should run:

```bash
git diff --check
./tools/check-sensitive-content .
./tools/knowledgectl lint
SKILLCTL_CANONICAL_DIR=/workspace/workspace-control/agent-skills/skills /workspace/tools/skills/skillctl validate
```

If generated files are introduced, add dry-run diff checks before committing.
