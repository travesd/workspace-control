# Codex History Review

Date: 2026-05-20
Reviewer: Codex
Scope: recent Codex history, active workspace artifacts, datasets, backups, investigations, and shared skills. This review summarizes patterns only; no transcript content, credentials, repo code, active task dirs, or Claude outputs were modified.

## Evidence

- Active work inventory: `/workspace/detection-platform-metal-work/ACTIVE.md`.
- Generated session index: `/workspace/detection-platform-metal-work/SESSIONS.md` reports 26 busy task dirs, 25 resume files, 11 recorded sessions, 12 live panes needing IDs, 1 busy dir missing `resume.md`, and 9 resume warnings.
- Missing active resume: `/workspace/detection-platform-metal-work/busy/autohunt-social-trace/`.
- Non-standard resume shapes found by local scan include 8 resume files without the standard `| Provider | Role | Session ID |` table, including `busy/brand-automation-expanded-workers/resume.md` and `busy/filter-service-social-identity-whitelist/resume.md`.
- Codex history sampled: `/home/user/.codex/history.jsonl` has 1,345 prompt records across 41 unique Codex session IDs. Only 5 of those session IDs are present in the current `SESSIONS.md`; not every historical session needs to be active, but several high-volume sessions are recoverable only through raw history.
- Recent Codex transcript inventory: 68 May 2026 JSONL files under `/home/user/.codex/sessions/2026/05/`. Large examples include `/home/user/.codex/sessions/2026/05/14/rollout-2026-05-14T13-26-01-019e26aa-64c3-7601-88d7-7fe31ceca6b7.jsonl` at about 173 MB and `/home/user/.codex/sessions/2026/05/07/rollout-2026-05-07T05-54-29-019e0100-7bed-7ed3-b304-0d9c9e8cd72f.jsonl` at about 150 MB.
- Session recovery precedent: `/workspace/detection-platform-metal-work/investigations/session-recovery-20260512/RECOVERY.md` reconstructed work from `ACTIVE.md`, busy dirs, worktrees, gateway state, Docker, tmux, and both provider transcript stores.
- Busy artifact size scan found very large active task dirs: `busy/image-similarity-research/` about 11 GB and 456,921 entries; `busy/llm-rethink-domain-llm-v2/` about 567 MB; `busy/autohunt-prompt-cache-followup/` about 215 MB.
- Done index health is relatively good: `/workspace/detection-platform-metal-work/done/INDEX.md` lists 16 completed task dirs, and each task dir has a `SUMMARY.md`. Recent day indexes exist under 9 day dirs.
- Dataset index drift: `/workspace/datasets/INDEX.md` lists the main durable entries, but a recursive manifest scan found 37 manifest/run records. Top-level durable datasets `/workspace/datasets/meritking-takedowns-30d-2026-05-14/` and `/workspace/datasets/tether-takedowns-30d-2026-05-14/` have manifests but are not currently described in `INDEX.md`.
- Backup organization is strong but the human index lags: `/workspace/backups/detection-platform/` has 7 backup dirs and all sampled dirs have both `MANIFEST.json` and `README.md`; `/workspace/backups/README.md` currently describes only 2 current captures.
- Shared skills inventory: `/workspace/agent-skills/skills/` has 9 canonical skills. Existing coverage is strong for DB, dataset export, UI browser review, Cloudflare Access observability, ground truth, and corpus coverage, but not for task intake, session hygiene, close-off, or learning capture.
- Provider-local memory gap: Claude memory files exist under `/home/user/.claude/projects/-workspace/memory/` with 28 files and an index. Codex has no comparable provider-neutral workspace memory store. `done/INDEX.md` and task notes reference memories such as prompt-iteration methodology, which means Codex may need to rediscover or search provider-local Claude files.

## Findings

### 1. Session recovery is the highest-friction area.

The workspace has the right artifacts, but they drift. `SESSIONS.md` is useful precisely because it exposes the mismatch: many panes need IDs, some resumes are non-standard, and one busy task has no resume. The 2026-05-12 recovery investigation shows the operational cost: recovery required correlating task dirs, worktrees, gateway routes, Docker state, tmux panes, and transcripts.

The most fragile pattern is long-running Codex work that accumulates huge transcripts and task state, then relies on raw transcript mining if a pane dies. The PR #2 resume explicitly records a 104 MB transcript; other recent Codex transcripts are larger. That is too much history for reliable recovery unless `resume.md` remains short, current, and parseable.

### 2. Durable learning is split between task notes and Claude-local memory.

Completed tasks do a good job preserving summaries, but reusable learning often lands in provider-local memory or buried task notes. Codex can grep Claude memory on this machine, but that is not a provider-neutral workspace contract. The problem is not that knowledge is missing; it is that agents do not have one stable lookup path for "what did we learn that should change future behavior?"

This especially affects rules cited during reviews, such as SSDeep promotion constraints, prompt-iteration methodology, or environment gotchas. Those are reusable workspace learnings and should not depend on one provider's memory implementation.

### 3. Task artifacts and data products are mostly well separated, but close-off is uneven.

The rules in `AGENTS.md` and `/workspace/datasets/MANAGEMENT.md` are clear. The recurring friction is enforcement at the end of long tasks. `busy/image-similarity-research/resume.md` already says some outputs should be harvested to `/workspace/datasets/` at close-off, and the directory size shows why this matters. Dataset manifests exist, but `datasets/INDEX.md` is not a complete discovery surface.

This is not a reason to move active data now. It is a reason to make close-off more mechanical and harder to forget.

### 4. Active work mapping is manually understandable but not machine-tight.

There are 26 busy dirs, 30 worktrees, and several gateway routes. Some worktrees are expected branch work, some are stale or follow-up contexts, and some are completed-but-retained references. Humans can work through this, but agents repeatedly rediscover the mapping.

A generated inventory that joins busy dirs, resume rows, worktrees, PRs, gateway routes, and dataset manifests would reduce uncertainty before cleanup, review, and handoff work.

### 5. Existing shared skills are useful, but the missing skills are about workspace mechanics.

The current 9 shared skills are mostly domain or tooling workflows. The repeated Codex friction is not "how do I query DB" or "how do I export incidents"; those now have skills. The repeated friction is starting work correctly, keeping recoverable state current, closing work cleanly, and promoting durable learning.

## Proposed Skills Or Updates

### `workspace-task-intake`

- Purpose: create or verify the task container for non-trivial work before implementation.
- Trigger: new feature, investigation, review, or multi-step task that needs a busy dir, investigation dir, worktree, plan, or resume.
- Source of truth: `/workspace/AGENTS.md`, `/workspace/tools/agents/sessionctl`, worktree rules, and the current task layout.
- Anti-staleness rule: keep this as a checklist plus commands that read live state; do not encode project-specific branch names, PR numbers, or gateway routes.

### `session-hygiene-recovery`

- Purpose: keep `resume.md`, `SESSIONS.md`, tmux panes, session IDs, transcripts, and next actions aligned.
- Trigger: starting or pausing agent sessions, crash recovery, "where are we", "what next", handoff, or before archiving.
- Source of truth: `/workspace/tools/agents/sessionctl`, `SESSIONS.md`, and task-local `resume.md`.
- Anti-staleness rule: require running `sessionctl index` or `reconcile`; never maintain a static pane list inside the skill.

### `task-closeoff-archive`

- Purpose: make close-off repeatable: verify PR/branch state, write `SUMMARY.md`, harvest datasets, update `DAY.md` and `done/INDEX.md`, regenerate session index, and only then remove worktrees when allowed.
- Trigger: user says a task is done, PR merged, review complete, or "close this task off".
- Source of truth: `AGENTS.md` Task Close-Off section, dataset management rules, and `ACTIVE.md`.
- Anti-staleness rule: the skill should cite the current close-off section instead of duplicating all rules; it should require reading `ACTIVE.md` before moving anything.

### `durable-learning-capture`

- Purpose: decide where a reusable learning belongs: `AGENTS.md`, shared skill, dataset manifest, done summary, or provider-neutral knowledge note.
- Trigger: "remember this", "methodology", repeated gotcha, postmortem learning, or review finding that should affect future agents.
- Source of truth: a new provider-neutral workspace knowledge index plus existing skill-maintainer rules.
- Anti-staleness rule: every note must include source artifact path, verification date, scope, and a "re-check before use" condition when the fact is code or environment dependent.

### `workspace-artifact-inventory`

- Purpose: produce the evidence table this investigation had to assemble manually: counts for busy/done/later/archived, resumes, sessions, worktrees, gateway routes, dataset manifests, backup manifests, and skill inventory.
- Trigger: workspace organization reviews, cleanup planning, or before large task archiving.
- Source of truth: live filesystem and tool output.
- Anti-staleness rule: no cached inventory; output should be regenerated each run and saved under the active investigation/task.

### Skill Updates

- Update or split `classifier-corpus-coverage` only after reviewing the draft skill work under `busy/local-brand-snapshot-harvest/repo-skill-drafts-20260519/`. The task review already argues for smaller workflows around seed/diagnose, snapshot harvest, promotion review, brand context generation, and transport.
- Extend `detection-dataset-export` or the proposed close-off skill to include `datasets/INDEX.md` maintenance when a durable dataset is created or promoted.
- Consider a backup index maintenance checklist, not a full skill yet. Backup manifests are good; the human README is just behind the actual 7 backup dirs.

## What Should Not Become A Skill

- PR-specific bugs such as the 2026-05-20 `migrate.sh` issues once fixed in code. The done summary correctly says the meta-lessons are already covered by existing memory.
- UI polish preferences from one page or one branch. Keep those in task notes until they repeat across pages.
- One-off client report content. The report pipeline may later deserve a skill if it becomes a repeatable product workflow, but the client-specific insights belong in datasets/reports, not a general workspace skill.
- Raw "refresh token" command snippets. DB and Access workflows already have `db-readonly-investigation` and `cloudflare-access-observability`.

## Proposed Knowledge Convention

Add a provider-neutral knowledge store under the workspace, for example:

```text
/workspace/detection-platform-metal-work/knowledge/
  INDEX.md
  workspace/
  project/
  workflow/
  gotchas/
```

Each note should have:

- title, tags, status, and verification date
- source task or investigation path
- the durable rule or learning in a few paragraphs
- when to re-verify
- whether it has been promoted to `AGENTS.md` or a shared skill

Suggested flow:

1. Task notes keep raw investigation detail.
2. `done/<date>/<task>/SUMMARY.md` captures what shipped and candidate learnings.
3. Reusable learnings move to `knowledge/` with provenance.
4. Procedural learnings that agents should actively invoke become shared skills.
5. Global rules with safety or workspace-wide impact move to `AGENTS.md`.

This gives Codex and Claude the same lookup path without depending on Claude-local memory or Codex transcript search.

## Claude Cross-Check Needed

- Whether Claude's `/insights` or memory workflow can export or mirror selected notes into a provider-neutral workspace store.
- Whether Claude relies on provider-local memory at session start in a way Codex cannot see.
- Whether the proposed session-hygiene skill should be a shared skill, a `sessionctl` command enhancement, or both.
- Whether any current Claude task dirs use resume formats that `sessionctl` cannot parse for provider-specific reasons.

## Risks And Open Questions

- More skills can become process bloat. The new skills should stay mechanical, short, and tied to live commands.
- Not every Codex session belongs in `SESSIONS.md`. The missing criterion is when a short PR review or one-off investigation becomes durable enough to need a task-local resume.
- Moving large active artifacts too early would break ongoing work. The close-off process should harvest only when the owning task is paused, done, or explicitly handed off.
- A provider-neutral knowledge store needs ownership. Without a small index-update habit, it will drift just like any other index.
