# Cross-Review Synthesis

Date: 2026-05-20

Inputs:

- `reviews/codex-history-review.md`
- `reviews/claude-history-review.md`
- `reviews/codex-on-claude-cross-review.md`
- `reviews/claude-on-codex-cross-review.md`

## Strong Agreement

Both providers independently found the same three highest-value process gaps:

1. **Durable learning capture**: useful learnings are scattered across Claude-local memory, task notes, summaries, and datasets. Codex has no equivalent shared memory source, so the current setup is not provider-neutral.
2. **Session hygiene**: `resume.md` and `SESSIONS.md` drift. Current evidence includes 26 busy dirs, 25 resume files, one missing resume, and multiple non-standard or unparseable resume files.
3. **Task close-off**: the rules are already clear, but harvesting datasets, updating indexes, and closing sessions/worktrees are uneven at the end of long tasks.

This convergence is the strongest signal in the review. These should be implemented before broader workflow experiments.

## Corrections From Cross-Review

- Claude's memory store is more mature than Codex initially weighted: Claude-local workspace memory store has an indexed set of concise topic notes. The problem is not quality; it is that the store is provider-local.
- Codex quantified the harvest and recovery debt more sharply: active task dirs include very large artifacts, and recent Codex transcripts can exceed 100 MB. Recovery should rely on explicit `resume.md` metadata, not transcript mining.
- `workspace-status` and `workspace-artifact-inventory` should be distinct outputs even if they share implementation:
  - `workspace-status`: short daily orientation, hard-capped, suitable at session start.
  - `workspace-artifact-inventory`: full audit report for cleanup and investigations.
- `AGENTS.md` should stay authoritative for stable behavior rules, but factual claims in it need a lightweight verification convention. A stale high-precedence instruction can mislead both providers.
- `/insights` is useful as evidence when available, but should not become required infrastructure. It was not available in the live Claude session; prior HTML reports existed under Claude usage data.

## Disagreements Resolved

- **Knowledge layout**: use a flat `knowledge/*.md` layout with frontmatter tags first. Avoid premature subdirectories like `workspace/`, `project/`, `workflow/`, and `gotchas/` until the corpus is large enough to justify them.
- **Workspace task intake**: fold intake behavior into `workspace-status` for now. If the current cwd does not map to a task, the status output can show the intake checklist.
- **Session recording threshold**: a session should have a `resume.md` row when it owns or materially advances a `busy/<task>/` directory. Short one-off checks that do not create or own a task do not need durable session records.
- **AGENTS.md verification**: do not clutter the whole file with markers. Start with verification metadata for new or disputed factual claims and expand only if drift continues.

## Provider-Specific Blind Spots

- Codex cannot assume Claude-local memory or `/insights` outputs are part of the workspace contract.
- Claude cannot assume Codex can preassign session IDs or recover cheaply from raw transcripts.
- Shared skills should branch explicitly where provider capabilities differ, especially session recording.
- Transcript mining was acceptable for this investigation, but future workflows should use explicit workspace artifacts, not provider-private transcript formats.

## Final Priority Order

1. Provider-neutral `knowledge/` store plus `durable-learning-capture` skill.
2. `session-hygiene` skill and current resume/session drift cleanup.
3. `task-closeoff` skill with dataset harvest and large-artifact gates.
4. `workspace-status` tool/skill for daily orientation and task intake.
5. `workspace-artifact-inventory` audit report for cleanup and organization reviews.
6. Dataset and backup index generation from manifests.
7. Lightweight verification rules for factual claims in `AGENTS.md` and shared skills.

## External Research Position

Research should be bounded and comparative, not open-ended. The workspace already has enough evidence to act.

Useful conventions to borrow:

- Official Codex/Claude guidance: keep always-loaded instructions concise; use skills for repeatable workflows; use memories for recall but not mandatory team rules.
- ADR-style decision records: one decision, context, decision, consequences, and status.
- Zettelkasten/PARA only in a reduced form: atomic notes with tags and backlinks are useful; broad personal productivity taxonomies are not worth adopting wholesale.
