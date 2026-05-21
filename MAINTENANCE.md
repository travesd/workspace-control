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

## Live Instruction Sync

Keep always-loaded instructions thin.

- Edit `AGENTS.md` and `current-workspace/AGENTS.md` together when changing the
  shared workspace contract.
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

## Pi Boundary

`.pi/` and `pi-pilot/` are retained in this repo as draft translation material.
They are not live workspace activation inputs unless the user explicitly starts
the Pi migration path. Keep Pi changes separate from live Claude/Codex
workflow changes when possible.

## Closeout Reminder

Before closing a workspace-control task:

- run the routine checks,
- update any relevant docs or ADRs,
- record whether live activation happened,
- note the latest repo commit in the task summary,
- regenerate `/workspace/detection-platform-metal-work/SESSIONS.md` if task
  session records moved.
