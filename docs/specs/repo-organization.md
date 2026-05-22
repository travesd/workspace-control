# Workspace-Control Repo Organization

Status: proposed source-layout standard; no canonical file moves until a render
or sync plan is approved

Date: 2026-05-22

This spec defines how `workspace-control` should separate small reusable core
instructions from workspace-specific overlays and provider adapters.

## Goal

Keep always-loaded context and reusable skills light while preserving the full
detection-platform-metal operating model and keeping a future Pi migration
straightforward.

The source model should let us answer:

1. What is portable across workspaces and providers?
2. What is specific to detection-platform-metal?
3. What is provider adapter logic for Claude, Codex, or Pi?
4. What is a generated or live activation target?
5. What can be migrated to Pi without changing the source of truth?

## Layer Model

| Layer | Purpose | Owns | Must Not Own |
|---|---|---|---|
| `core/` | Provider-neutral, workspace-neutral operating primitives. | Minimal shared instructions, portable skills, durable note conventions, generic task lifecycle/resumability specs. | Detection product paths, provider CLI commands, live-only state. |
| `workspaces/<name>/` | Workspace overlay for one concrete workspace. | Product-specific rules, tools, skills, profiles, specs, path conventions. | Provider auth, provider-local memory, generic reusable primitives. |
| `providers/<provider>/` | Adapter for a provider/harness. | Provider wrapper instructions, config examples, mirror maps, agent/workflow translations. | Source policy decisions or product-specific facts unless they are adapter examples. |
| `current-workspace/` | Compatibility source and activation target for the current live `/workspace`. | Rendered or manually maintained live instructions/tools until composition exists. | New durable policy that should live in `core/` or workspace overlays. |
| `agent-skills/` | Current live-compatible canonical shared skill tree. | The active skill source until split/mirror tooling is implemented. | Long-term mixed core and workspace ownership after migration completes. |
| `.pi/`, `pi-pilot/` | Pi draft adapter and migration research. | Experimental Pi agents/workflows/settings. | Live authority, canonical skills, or workspace policy. |

Top-level `AGENTS.md` is a repo-local instruction file for working inside
`workspace-control`; it is not a source for live `/workspace/AGENTS.md`.

## Classification Rules

Classify new content by the narrowest durable home:

- **Core**: applies to any repo or workspace using agents.
- **Workspace overlay**: depends on `/workspace`, detection-platform-metal,
  Docker Swarm, classifier data, task directories, or workspace tools.
- **Provider adapter**: exists only because Claude, Codex, or Pi needs a
  different file format, command, import style, config key, or agent wrapper.
- **Generated/live target**: output consumed by the current live workspace.
- **Research/plan/review**: analysis or proposal under `docs/`.

If content spans layers, split it:

- principle in `core/`,
- local application in `workspaces/detection-platform-metal/`,
- provider invocation in `providers/<provider>/`,
- activation output in `current-workspace/` or live `/workspace`.

## Initial Target Layout

This tree is the target organization, with currently known repo directories
listed to avoid treating omissions as deletion candidates.

```text
workspace-control/
  core/
    README.md
    skills/
    specs/
    templates/

  workspaces/
    detection-platform-metal/
      README.md
      skills/
      specs/
      profiles/
      tools/

  providers/
    claude/
    codex/
    pi/

  current-workspace/
    AGENTS.md
    CLAUDE.md
    README.md
    WORKSPACE-SNAPSHOT.md
    config/
    tools/

  agent-skills/
    skills/

  docs/
    decisions/
    plans/
    reference/
    research/
    reviews/
    specs/
    templates/

  .pi/
  pi-pilot/

  AGENTS.md
```

The first migration slice should add directories and source maps only. Moving
canonical files should wait for a render/sync plan that proves generated
outputs match the current live behavior.

## Skill Split

Current `agent-skills/skills/` remains the active canonical source until a split
is explicitly activated.

Proposed future split by concept:

| Core Skill Concepts | Detection Overlay Skills Or Implementations |
|---|---|
| `agents-md-review` | `autohunt-ground-truth-review` |
| `call-a-friend` | `classifier-corpus-coverage` |
| `durable-learning-capture` | `cloudflare-access-observability` |
| `research-to-knowledge` | `daily-submissions-metrics` |
| `session-hygiene` | `db-readonly-investigation` |
| `skill-maintainer` | `detection-dataset-export` |
| `task-closeoff` | `detection-ui-browser-review` |
| `workspace-artifact-inventory` | `validating-ground-truths` |
| `workspace-status` |  |

This table is not permission to move files as-is. Several core skill concepts
currently contain `/workspace` paths or detection-platform-metal assumptions.
Before moving them to `core/skills/`, either parameterize those paths or split
them into:

- a portable core skill,
- a detection-platform-metal reference or implementation under
  `workspaces/detection-platform-metal/skills/`.

## Instruction Split

The live `/workspace/AGENTS.md` should eventually be rendered from:

1. core operating contract,
2. detection-platform-metal overlay,
3. current live activation references.

`/workspace/CLAUDE.md` should remain a Claude-specific wrapper that imports the
shared contract and adds only Claude-specific behavior.

The top-level `workspace-control/AGENTS.md` should remain a separate thin
contract for editing this repo. If a rule needs to exist in both places, update
the repo-local file and the rendered live workspace source intentionally.

Codex should keep using `AGENTS.md` and project-scoped config where appropriate.
Project-scoped `.codex/config.toml` can hold non-secret project overrides and
custom agents, but machine-local auth/provider settings stay user-local.

Pi should consume the same core plus workspace overlay through adapter files
under `providers/pi/`, not by duplicating source policy in `.pi/`.

## Profiles

Profiles are task-oriented bundles that name the overlays, skills, and guardrails
expected for a class of work. They are not provider profiles by default.

Candidate profiles:

- `review`: read-only review, call-a-friend, findings-first output.
- `implementation`: worktree, Docker validation, scoped edits.
- `db-investigation`: DB read-only tooling and evidence capture.
- `ui-review`: browser MCP, screenshots in task artifacts.
- `dataset-export`: incident scope cache and dataset manifests.
- `workspace-maintenance`: skill sync, knowledge sync, session hygiene.

Provider adapters may translate these profiles into Claude agents, Codex custom
agents, or Pi workflows.

## Activation Principle

Do not make the layered layout live until:

1. every current live input has a mapped source layer,
2. generated or copied outputs diff cleanly against current live files,
3. skill validation passes from the generated skill tree,
4. rollback snapshot exists,
5. Pi remains excluded unless the user explicitly starts the Pi path.

## Provider Notes

Claude:

- Keep `CLAUDE.md` thin and import the shared contract.
- Keep detailed procedures in skills or references.
- Provider-local memory is not the source of truth.

Codex:

- Prefer `AGENTS.md` for project instructions.
- Use project `.codex/config.toml` only for allowed project-scoped overrides.
- Custom agents live under `.codex/agents/` or user-level config when adopted.
- Skills should stay portable and provider-neutral unless deliberately adapted.

Pi:

- Treat `.pi/` as adapter output or pilot config.
- Pi agents/workflows should reference core and workspace overlay material.
- Pi package/schema decisions need separate source review and activation.
