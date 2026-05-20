# Workspace Organization and Efficiency Recommendations

Date: 2026-05-20

This investigation reviewed workspace artifacts, active tasks, shared skills, Claude and Codex histories, Claude's prior `/insights` output, and cross-provider reviews. It did not modify repo code or active task directories.

## Executive Summary

The workspace has strong foundations: clear top-level rules, explicit task/data/backup separation, managed dataset tooling, and useful shared skills. The recurring cost is not missing rules; it is that recovery metadata, human indexes, and reusable learnings drift under long-running multi-agent work.

The highest-value fix is a provider-neutral learning and status layer:

1. Put durable learnings in `/workspace/detection-platform-metal-work/knowledge/`, not only in Claude memory or task notes.
2. Make session hygiene and task close-off mechanical through shared skills.
3. Add a short generated workspace status command/report so agents stop rediscovering the same state at every session start.
4. Generate or reconcile human indexes from manifests instead of relying on agents to remember index edits.

## Key Evidence

- `busy/`: 26 task dirs, 25 resume files, one missing resume: `busy/autohunt-social-trace/`.
- `SESSIONS.md`: multiple live panes need IDs; several resume files are non-standard or unparseable.
- Claude memory: 28 markdown files under Claude-local workspace memory store, with a concise `MEMORY.md` index.
- Codex memory: no comparable populated workspace memory in Codex-local memory directory; visible config does not enable Codex memories.
- Codex history: 41 unique Codex session IDs sampled from history, only 5 present in current `SESSIONS.md`.
- Large active artifacts: `busy/image-similarity-research/` is about 11 GB / 457k entries.
- Dataset/backups: per-artifact manifests are strong, but human indexes lag manifest reality.
- `/insights`: not available in the live Claude session; prior static reports existed in Claude-local usage-report store and were useful evidence, but are provider-local.

## Recommended Changes

### 1. Add Provider-Neutral Knowledge

Create:

```text
/workspace/detection-platform-metal-work/knowledge/
  INDEX.md
  feedback_verify_before_asserting.md
  feedback_git_commit_identity.md
  project_curated_70_sample_dataset.md
  ...
```

Use a flat file layout with frontmatter:

```yaml
---
title: Verify before asserting
tags: [workspace, review, evidence]
status: active
verified: 2026-05-20
source: sanitized workspace memory migration, 2026-05-20
re_verify_when: "AGENTS.md verification rules or review workflow changes"
---
```

Seed it from the existing Claude memory files, but keep Claude's `MEMORY.md` as a pointer or generated mirror until the new store proves reliable. The workspace `knowledge/` tree should be canonical; provider-local memory should not become a second source of truth.

### 2. Create `durable-learning-capture`

Shared skill purpose: route a learning to the right durable home.

Decision rule:

- Safety/workspace rule used every session: `AGENTS.md`.
- Repeatable procedure: shared skill.
- Reusable fact/methodology/gotcha: `knowledge/`.
- Dataset-specific fact: dataset manifest.
- Task-specific detail: task `notes.md` or `SUMMARY.md`.

This is the place to handle "remember this" requests and `/insights` report promotion.

### 3. Create `session-hygiene`

Shared skill purpose: keep agent sessions recoverable.

Minimum behavior:

- Run `sessionctl index` / `reconcile`.
- Detect missing and non-standard `resume.md`.
- Record session ID, provider, role, transcript, tmux/window, and next step.
- Branch by provider because Claude can preassign session IDs and Codex currently discovers them after launch.

Rule of thumb: if a session owns or materially advances a `busy/<task>/` dir, it needs a standard `resume.md` row.

### 4. Create `task-closeoff`

Shared skill purpose: make task close-off hard to skip.

Minimum behavior:

- Read `ACTIVE.md` first.
- Verify PR/branch/worktree state.
- Write or update `SUMMARY.md`.
- Harvest data products to `/workspace/datasets/` and leave pointers.
- Update `DAY.md`, `done/INDEX.md`, dataset index, and session index.
- Warn on task dirs over 100 MB; require an explicit harvest/keep decision over 1 GB.

### 5. Add `workspace-status`

A short generated orientation report should replace the repeated session-start scout sequence.

Include:

- active critical tasks from `ACTIVE.md`,
- `SESSIONS.md` summary,
- current cwd mapping to task/worktree if any,
- open PRs relevant to current branch,
- worktree and gateway summary,
- missing resume or session-ID warnings,
- intake checklist when no task context is detected.

Hard-cap it around 200 lines. Prefer stdout-only or a clearly timestamped artifact to avoid stale `STATUS.md` becoming another source of truth.

### 6. Add `workspace-artifact-inventory`

Separate from `workspace-status`: this is the audit-grade version for cleanup and organization reviews.

It should regenerate counts for busy/done/later/archived, resumes, sessions, worktrees, gateway routes, datasets, backups, and shared skills, then save the output under the active task or investigation.

### 7. Generate Human Indexes From Manifests

The pattern is consistent: manifests are reliable; hand-maintained indexes drift.

First targets:

- `datasets/INDEX.md` from dataset manifests and managed detection run manifests.
- `/workspace/backups/README.md` from backup `MANIFEST.json` files.

Automation can draft rows while leaving human descriptions editable.

### 8. Add Lightweight Claim Verification

Do not make `AGENTS.md` longer by default. Instead:

- Add verification metadata only for concrete factual claims that can go stale.
- Require source path/date/re-check condition for new or disputed factual guidance.
- Run a periodic or on-demand `agents-md-review` after a user flags a claim as wrong.

Apply the same convention to shared skills where they cite current tool behavior.

## Skill Roadmap

Priority 1:

- `durable-learning-capture`
- `session-hygiene`
- `task-closeoff`

Priority 2:

- `workspace-status`
- `workspace-artifact-inventory`

Priority 3:

- `agents-md-review`
- dataset/backup index generation helpers

Defer:

- Splitting `classifier-corpus-coverage` until the current local-brand-snapshot task closes.
- Reimplementing `/insights`; preserve its outputs when available instead.
- Full Zettelkasten/PARA-style personal knowledge management. Use only the practical parts: atomic notes, tags, provenance, and backlinks.

## External References

- OpenAI Codex customization docs: `AGENTS.md`, memories, skills, MCP, and subagents are complementary layers: https://developers.openai.com/codex/concepts/customization
- OpenAI Codex memories docs: memories are local recall and not the only source for required rules: https://developers.openai.com/codex/memories
- Claude Code memory docs: concise instructions, topic files, and skills for multi-step procedures: https://code.claude.com/docs/en/memory
- MIT Libraries ADR guide: lightweight decision records with title, status, context, decision, and consequences: https://mitlibraries.github.io/guides/misc/adr.html
- ADR overview: decision records form a decision log with rationale and tradeoffs: https://adr.github.io/

## Suggested First Implementation Task

Create `knowledge/` and migrate the Claude memory files into it without deleting or changing the original Claude memory tree. Then add the `durable-learning-capture` shared skill and validate it with one real learning from a recent done task.

That first slice is small, reversible, and unlocks the biggest cross-provider efficiency gain.
