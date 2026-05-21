# Task Lifecycle Update Plan

Date: 2026-05-21

Status: proposed, workspace-control only

## Objective

Make task state definitions unambiguous enough that Claude, Codex, and future
Pi workflows classify workspace tasks consistently. Current metal task
lifecycle state stays under `/workspace/detection-platform-metal-work/`; the
top-level `/workspace/archive/` remains legacy migration/provenance context.

The current lifecycle root for metal task state is:

```text
/workspace/detection-platform-metal-work/
```

Future task archives use:

```text
/workspace/detection-platform-metal-work/archived/YYYYMMDD-<reason>/<task>/
```

The top-level `/workspace/archive/` remains migration/provenance context for
old repos, old GKE-era work, historical datasets, loose migration files, and
compatibility symlink targets.

## Review Conclusions

- A new `parked/` state is justified. Existing `busy/` contains active work,
  deferred PRs, important prototypes, and paused critical work; those have
  different operational meanings.
- `archived/` and `parked/` must stay separate. `parked/` is paused but
  resumable or extractable. `archived/` is reference-only after useful material
  has been summarized or extracted.
- `later/` should remain lightweight. It is a backlog/reminder state, not a
  preservation state for branches, patches, prototypes, screenshots, or large
  analysis artifacts.
- Existing live `resume.md` files are mostly Markdown, not strict YAML. The
  standard should require lifecycle fields, not a mandatory serialization
  format.
- Activation must be separate from repo update. This plan updates
  `workspace-control`; moving live task directories should happen only after a
  targeted audit and explicit approval.

## Proposed Repo Updates

### 1. Formalize the Lifecycle Spec

Files:

- `docs/specs/task-lifecycle.md`

Changes:

- Define state as the single primary directory state.
- Define substate as metadata inside `resume.md` or `SUMMARY.md`.
- Add classification order for ambiguous tasks.
- Clarify `planned/`, `busy/`, `parked/`, `later/`, `done/`, `archived/`, and
  `investigations/`.
- State the positive archive destination under
  `/workspace/detection-platform-metal-work/archived/`.

Acceptance:

- An agent can decide whether a deferred PR belongs in `parked/`, `later/`, or
  `archived/` without chat-only context.
- The spec does not require editing live workspace files.

### 2. Add a Resume Lifecycle Template

Files:

- `docs/templates/task-lifecycle-block.md`

Changes:

- Provide a Markdown block for `resume.md` lifecycle metadata.
- Include state, substate, reason, restart condition, extraction requirement,
  branch/worktree status, artifact policy, and review trigger.
- Allow YAML frontmatter as an implementation option later, without making it
  mandatory now.

Acceptance:

- A parked task can be documented consistently in existing Markdown resumes.
- Agents can copy the block without changing the rest of a task's notes.

### 3. Align Workspace Instructions

Files:

- `current-workspace/AGENTS.md`

Changes:

- Add `parked/` to the work artifact layout.
- Make `/workspace/detection-platform-metal-work/` the explicit lifecycle root.
- Describe `/workspace/archive/` as legacy migration/provenance context.
- Update transition guidance to route valuable paused work to `parked/`.

Acceptance:

- The staged `AGENTS.md` copy gives positive destination rules.
- Existing migration references to `/workspace/archive/` remain intact.

### 4. Align Shared Skills

Files:

- `agent-skills/skills/task-closeoff/SKILL.md`
- `agent-skills/skills/workspace-status/SKILL.md`

Changes:

- Teach close-off to choose among `done/`, `parked/`, `later/`, and
  `archived/`.
- Require parked lifecycle metadata in clear Markdown labels or YAML
  frontmatter.
- Include task lifecycle counts in workspace status reports.

Acceptance:

- Skill frontmatter remains portable: only `name` and `description`.
- The skills do not assume Claude-only or Codex-only tooling.

### 5. Align Helper Tools

Files:

- `tools/workspace-status`
- `tools/workspace-artifact-inventory`

Changes:

- Include `parked/` in task-state counts.
- Count file-based `planned/*.md` specs as planned work.
- Keep output concise and read-only.

Acceptance:

- `bash -n` passes for updated shell tools.
- `tools/workspace-status --brief` reports `parked` count when the directory is
  present or `0` when absent.

## Activation Plan

Activation is not part of this repo update. When approved later:

1. Create `/workspace/detection-platform-metal-work/parked/`.
2. Run a read-only audit of `busy/`, `later/`, and existing work-dir
   `archived/` tasks.
3. Produce a proposed movement table with current path, proposed state,
   reason, branch/worktree/PR status, and required lifecycle metadata.
4. Move only approved tasks.
5. Update each moved task's `resume.md` or `SUMMARY.md`.
6. Regenerate session lookup with `/workspace/tools/agents/sessionctl index`.
7. Run workspace status and artifact inventory to confirm counts.

## Non-Goals

- Do not move live task directories as part of this repo change.
- Do not modify top-level `/workspace/archive/`.
- Do not remove any worktree as part of lifecycle classification.
- Do not introduce a full task database before the directory model has been
  activated and tested.

## Validation

For the workspace-control change:

```bash
bash -n tools/workspace-status tools/workspace-artifact-inventory
tools/check-sensitive-content /workspace/workspace-control
```

For future live activation:

```bash
/workspace/tools/agents/sessionctl index
/workspace/workspace-control/tools/workspace-status --brief
/workspace/workspace-control/tools/workspace-artifact-inventory
```

## Open Decisions

- Whether `parked/` should be activated immediately after review, or only after
  a complete movement table is approved.
- Whether to add a future `taskctl` helper for validating lifecycle metadata.
- Whether `planned/` should remain file-based, directory-based, or allow both
  during transition.
