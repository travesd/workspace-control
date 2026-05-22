# Workspace-Control Maintenance

This repo is the reviewable source for workspace operating-model changes. Keep
it current as the live workspace evolves, but do not let routine task artifacts
or provider-local state drift into Git.

## When To Update This Repo

Update `/workspace/workspace-control` when a change is meant to be reusable
beyond one task:

- workspace-wide rules or path conventions change,
- shared Agent Skills change,
- durable knowledge notes are added or corrected,
- helper scripts under `tools/` change,
- task lifecycle definitions or templates change,
- task resumability scoring or note templates change,
- layered source layout, overlays, provider adapters, or profile maps change,
- activation, rollback, or provider-practice docs change.

Do not update this repo for ordinary task notes, screenshots, datasets,
backups, product worktrees, provider transcripts, or one-off local stack output.

## Source-Of-Truth Direction

Use this direction unless a task explicitly says otherwise:

1. Draft operating-model changes in `/workspace/workspace-control`.
2. Review the repo diff and run the local checks below.
3. Commit and, after explicit approval, push the repo.
4. Activate deliberately into `/workspace` only after approval.

Live emergency fixes can happen in `/workspace` first. When that happens, copy
the durable part back into this repo before closing the task so the source repo
does not lag behind live practice.

## Layered Source Layout

The target organization is defined in `docs/specs/repo-organization.md`.

Until render/sync tooling exists:

- keep `current-workspace/` and `agent-skills/` as the live-compatible
  activation sources,
- use `core/`, `workspaces/`, and `providers/` for source maps and new layered
  proposals only,
- do not duplicate or move canonical skills into layered directories without a
  dry-run proving generated outputs match the current live-compatible tree,
- keep Pi adapter work separate from live Claude/Codex activation.

## Routine Checks

Run from `/workspace/workspace-control` before committing or pushing:

```bash
./tools/check-sensitive-content .
./tools/knowledgectl lint
./tools/knowledgectl index
git diff --stat
git status --short --branch
```

If generated knowledge indexes change, include them with the note changes that
caused them.

## Skill Sync

Shared skills should stay provider-neutral and should be edited in this repo
first when practical:

1. Edit `agent-skills/skills/<skill>/SKILL.md`.
2. Review and commit the repo change.
3. After explicit approval, sync to `/workspace/agent-skills/skills/`.
4. Run `/workspace/tools/skills/skillctl validate`.
5. Run `/workspace/tools/skills/skillctl sync`.

Provider mirrors under `/workspace/.claude/skills/` and
`/workspace/.agents/skills/` are generated copies, not canonical sources.

When the skill tree is split later, `agent-skills/skills/` should become a
generated compatibility tree composed from `core/skills/` and the selected
workspace overlay skills.

## Live Instruction Sync

Keep always-loaded instructions thin.

- Edit `AGENTS.md` and `current-workspace/AGENTS.md` together only when the
  same shared rule must apply to both this repo and the live workspace.
- Edit `current-workspace/AGENTS.md` for live `/workspace/AGENTS.md` changes.
- Edit top-level `AGENTS.md` only for workspace-control repo behavior.
- Edit `current-workspace/CLAUDE.md` only for Claude-specific import/wrapper
  behavior.
- Keep detailed procedures in skills, tool READMEs, or docs.
- After activation, verify `/workspace/AGENTS.md` and `/workspace/CLAUDE.md`
  match the intended repo copies.

## Knowledge Sync

Use durable knowledge for reusable facts and gotchas, not raw research dumps.

```bash
./tools/knowledgectl search <term>
./tools/knowledgectl lint
./tools/knowledgectl index
```

Set `re_verify_when` on notes whose facts can become stale, and prefer links to
task summaries, manifests, or source docs over pasted raw transcript content.

## Resumability Review

During workspace hygiene reviews, sample recent `busy/`, `parked/`, and `done/`
tasks against `docs/specs/task-resumability.md`.

Track:

- tasks with complete resume packets,
- parked tasks with concrete restart or extraction conditions,
- tasks where chat dependency remains `required`,
- stale `busy/` tasks,
- durable learnings extracted to skills, knowledge notes, ADRs, or manifests.

Use the results to simplify templates if agents skip them, or tighten fields if
fresh agents still need chat history to resume.

## Pi Boundary

`.pi/` and `pi-pilot/` are retained in this repo as draft translation material.
They are not live workspace activation inputs unless the user explicitly starts
the Pi migration path. Keep Pi changes separate from live Claude/Codex
workflow changes when possible.

Provider adapter notes belong under `providers/pi/`; runnable draft Pi files
remain under `.pi/` and `pi-pilot/` until a package/schema ADR is approved.
For example, a Pi package/schema decision or mapping rationale belongs under
`providers/pi/` or `docs/decisions/`, while `.pi/agents/*.md`,
`.pi/workflows/*.json`, and `.pi/settings.example.json` remain draft runnable
configuration examples.

## Closeout Reminder

Before closing a workspace-control task:

- run the routine checks,
- update any relevant docs or ADRs,
- record whether live activation happened,
- note the latest repo commit in the task summary,
- regenerate `/workspace/detection-platform-metal-work/SESSIONS.md` if task
  session records moved.
