# Core Skill Portability Audit

Date: 2026-05-25

Scope: draft render-input skill copies under `core/skills/` after
`tools/renderctl dry-run --mode skills` was added.

Update: 2026-05-25 portability cleanup started for the near-portable review
and knowledge skills. See `core/templates/skill-parameter-map.md` and
`workspaces/detection-platform-metal/specs/core-skill-parameter-map.md`.

Update: 2026-05-25 provider command examples were split out of the portable
`call-a-friend` skill into provider adapter references under
`providers/claude/references/` and `providers/codex/references/`.

## Summary

The skill render path is mechanically clean: draft skill copies under
`core/skills/` and `workspaces/detection-platform-metal/skills/` generate the
current `agent-skills/skills/` tree exactly, and the generated tree validates.

That does not mean every `core/skills/` copy is portable. Most current "core"
copies are compatibility-preserving drafts that still mention live workspace
paths, Claude/Codex-specific behavior, task lifecycle details, or
workspace-control tooling.

Activation readiness:

- `agent-skills/skills/` remains the canonical live-compatible source.
- `core/skills/` and `workspaces/detection-platform-metal/skills/` are render
  inputs only.
- Do not remove compatibility copies or treat `core/skills/` as portable until
  the issues below are split or parameterized.

## Audit Method

Commands:

```bash
rg -n "/workspace|detection-platform|detection_|workspace-control|agent-skills|SESSIONS|ACTIVE|tmux|Codex|Claude|Cloudflare|dbctl|gatewayctl|datasetctl|skillctl|docker|production|local stack|worktree|AGENTS\.md|CLAUDE\.md" core/skills
tools/renderctl dry-run --mode skills
SKILLCTL_CANONICAL_DIR=<generated>/agent-skills/skills /workspace/tools/skills/skillctl validate
```

## Findings

| Skill | Current Portability | Notes |
|---|---|---|
| `agents-md-review` | Parameterized | Now uses local instruction, knowledge, and decision-record locations from the local parameter map or workspace instructions. |
| `call-a-friend` | Provider commands split | Core workflow is now provider-neutral; Claude/Codex command examples live in provider adapter references. |
| `durable-learning-capture` | Parameterized | Now routes by durable-home category and asks for the local parameter map before writing global files. |
| `research-to-knowledge` | Parameterized | Now references local guardrails and durable homes without embedding detection-platform-metal policy examples. |
| `session-hygiene` | Workspace overlay | Depends on `/workspace/detection-platform-metal-work/`, `/workspace/tools/agents/sessionctl`, tmux, Claude/Codex launch helpers, and task-resumability paths. The portable core should be a generic resume/session-record pattern. |
| `skill-maintainer` | Split required | Describes Claude/Codex shared skill layout, live `/workspace/agent-skills/`, provider mirrors, and `/workspace/tools/skills/skillctl`. Needs a portable skill schema plus workspace/provider adapter implementation. |
| `task-closeoff` | Workspace overlay | Depends on `/workspace/detection-platform-metal-work/`, `/workspace/datasets/`, sessionctl, worktrees, and detection archive policy. A portable core could define closeoff phases; this implementation belongs in the detection overlay. |
| `workspace-artifact-inventory` | Workspace overlay | Depends on `tools/workspace-artifact-inventory`, workspace tasks, sessions, worktrees, datasets, backups, and shared skill inventory. Keep as an overlay implementation unless generalized. |
| `workspace-status` | Workspace overlay | Depends on `tools/workspace-status`, live workspace state, task counts, PR/branch context, and intake checklist conventions. Keep as an overlay implementation unless generalized. |

## Recommended Split Order

1. Extract path/config maps:
   - instruction contract path,
   - knowledge note path,
   - task root path,
   - skill source path,
   - session index command,
   - provider mirror paths.
2. Convert near-portable skills first:
   - `agents-md-review` (done),
   - `durable-learning-capture` (done),
   - `research-to-knowledge` (done).
3. Split provider-specific command details:
   - move `call-a-friend` provider commands into `providers/claude/` and
     `providers/codex/` mappings or provider references (done).
4. Keep operational detection implementations under
   `workspaces/detection-platform-metal/skills/` until generalized:
   - `session-hygiene`,
   - `skill-maintainer`,
   - `task-closeoff`,
   - `workspace-artifact-inventory`,
   - `workspace-status`.
5. After each split, run:
   - `tools/renderctl dry-run --mode skills`,
   - generated-tree `skillctl validate`,
   - compatibility-tree `skillctl validate`.

## Decision

Keep the current exact render copies for now. Exact generated output is the
safety gate. Portability cleanup should happen as explicit follow-up commits
that preserve clean generated diffs or intentionally update the compatibility
tree with reviewed changes.
