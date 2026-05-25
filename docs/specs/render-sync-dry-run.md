# Render/Sync Dry-Run

Status: conservative implementation; no canonical moves

Date: 2026-05-22

## Purpose

The layered repo layout should not become live until generated compatibility
outputs can be compared against the current checked-in sources. The dry-run
tool gives us that gate before moving skills, instructions, tools, or provider
adapter files.

## Current Behavior

`tools/renderctl dry-run` defaults to `--mode all`, which renders both the
compatibility tree and the draft instruction composition.

Compatibility mode:

| Selected Source | Generated Target | Mode |
|---|---|---|
| `current-workspace/` | `current-workspace/` | compatibility copy |
| `agent-skills/skills/` | `agent-skills/skills/` | compatibility copy |

Instruction mode:

| Selected Source | Generated Target | Mode |
|---|---|---|
| `core/AGENTS.contract.md` | `current-workspace/AGENTS.md` | instruction fragment |
| `workspaces/detection-platform-metal/AGENTS.overlay.md` | `current-workspace/AGENTS.md` | instruction fragment |
| `workspaces/detection-platform-metal/AGENTS.references.md` | `current-workspace/AGENTS.md` | instruction fragment |

The command prints:

- selected sources,
- selected source files,
- generated target root,
- manifest path,
- content and file-mode diffs against checked-in compatibility targets,
- follow-up validation commands, including working-tree, staged, commit, and
  outbound-range whitespace checks.

By default the generated tree is temporary and removed after a clean run. Use
`--keep` or `--out <dir>` when a diff artifact needs to be inspected.

## Non-Goals

- Do not treat draft render inputs as canonical until activation is approved.
- Do not write to live `/workspace`.
- Do not sync provider mirrors.
- Do not activate Pi.

## Promotion Gate

Before any canonical source move, the render path must prove:

1. every current live-compatible input has a mapped source,
2. generated outputs diff cleanly against `current-workspace/` and
   `agent-skills/skills/`,
3. skill validation passes against the generated or compatibility skill tree,
4. activation and rollback docs name the exact generated targets,
5. Pi remains excluded unless the user explicitly starts the Pi path.

## Future Render Modes

Implemented modes:

- `instructions`: `core` contract plus workspace overlay plus activation
  reference rendered into `current-workspace/AGENTS.md`.

The next implementation slices can add explicit modes such as:

- `skills`: portable core skills plus workspace overlay skills rendered into
  `agent-skills/skills/`,
- `provider`: provider adapters rendered into Claude/Codex/Pi config examples,
- `live-check`: read-only comparison between repo compatibility outputs and
  live `/workspace` targets.

Each new mode should be added behind a dry-run diff first. Write/sync behavior
requires separate approval and rollback notes.
