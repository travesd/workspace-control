# Workflow Improvements Go-Live Scope

Date: 2026-05-21

Status: proposed, not activated

## Objective

Promote the reviewed workspace workflow improvements from
`/workspace/workspace-control` into the live `/workspace` operating model in
small, auditable slices, with a clean rollback path for every live change.

This plan covers:

- workspace rules and activation boundary,
- provider-neutral knowledge lookup,
- shared Claude/Codex skills,
- status/inventory helper tools,
- task lifecycle states including `parked/`,
- incident scope-cache semantics,
- Pi pilot handoff boundaries.

Thin-instructions audit:

- `docs/reviews/2026-05-21-thin-instructions-audit.md`

Provider practices audit:

- `docs/reviews/2026-05-21-claude-codex-practices-review.md`

Latest tmux/session audit:

- Session `0` has 12 windows and 11 apparent agent chats: 8 Codex/node panes
  and 3 Claude panes.
- `/workspace/tools/agents/sessionctl index` reports 10 live agent panes that
  need explicit session IDs recorded, 11 recorded sessions not currently
  matched to live panes, and one busy task without `resume.md`
  (`brand-automation-corpus-llm-workers`).
- Treat active-chat reconciliation as migration preflight, not a post-activation
  cleanup. Do not move or archive task directories while current tmux panes
  cannot be mapped to owning task records.

## Current Source Boundary

`workspace-control` remains the reviewable source. Live runtime surfaces are
only updated through an explicit activation task.

| Surface | Proposed source | Live target | Risk |
|---|---|---|---|
| Workspace rules | `current-workspace/AGENTS.md` | `/workspace/AGENTS.md` and thin `/workspace/CLAUDE.md` import | Medium |
| Shared skills | `agent-skills/skills/` | `/workspace/agent-skills/skills/` plus generated provider mirrors | Medium |
| Knowledge notes | `knowledge/` | `/workspace/workspace-control/knowledge/` referenced by agents | Low |
| Helper tools | `tools/workspace-status`, `tools/workspace-artifact-inventory`, `tools/knowledgectl` | Called from repo path or installed under `/workspace/tools/workspace-control/` | Low |
| Task lifecycle dirs | `docs/specs/task-lifecycle.md` | `/workspace/detection-platform-metal-work/{parked,later,archived,...}` | Medium |
| Incident cache spec | `docs/specs/incident-scope-cache.md` | Future `/workspace/datasets/` behavior and dataset tooling | Medium |
| Pi pilot | `.pi/`, `pi-pilot/` | Not live | High if made runnable prematurely |

## Go-Live Principle

Activation should be read-mostly first. The first live slice should make the
new guidance discoverable and validate that agents use it correctly before any
large task-directory movement or dataset/cache behavior changes.

Use this order for the non-interrupting go-live:

1. Snapshot live workspace-control-relevant state.
2. Capture a passive active-chat inventory without sending input to any pane.
3. Apply the thin-instructions gate before copying any always-loaded file.
4. Activate read-only helpers and knowledge lookup.
5. Activate shared skills.
6. Activate workspace rules from a thin `AGENTS.md`.
7. Verify both providers from fresh sessions.
8. Create `parked/` and run a dry-run task audit.
9. Move only explicitly approved task directories.
10. Add provider-enforced secret-read denies as a separate hardening slice.
11. Leave Pi pilot disabled until a separate harness decision.

## Rescoped Migration Tracks

The migration is no longer a single "copy the new workspace model live" action.
It should run as four separable tracks:

| Track | Goal | Live mutation | Gate |
|---|---|---:|---|
| A. Recovery readiness | Make active chat/task state visible before changing instructions. | Passive inventory plus `SESSIONS.md` regeneration only | Active panes are inventoried without interruption; full per-task reconciliation may be deferred. |
| B. Source activation | Promote reviewed skills, helper usage, and thin instructions. | Yes | Rollback snapshot exists; validation passes. |
| C. Lifecycle adoption | Introduce `parked/` and classify stale work. | Directory creation first; moves only after approval | Movement table reviewed and approved. |
| D. Provider hardening | Convert secret-handling guidance into enforced provider settings. | Provider config only | Tested in fresh Claude and Codex sessions. |

Track D follows official Claude Code and Codex guidance but is not required for
the first instruction-layout activation. It should be planned immediately after
Track B because instructions are advisory, while provider settings can enforce
deny rules for env and credential files.

## Non-Interrupting Active Chat Policy

The first live switch may proceed without interrupting existing Claude/Codex
chats if the user explicitly accepts that currently running chats keep their
already-loaded context until they are resumed, restarted, or naturally end.

Allowed during non-interrupting activation:

- Read tmux metadata with `tmux list-windows` and `tmux list-panes`.
- Regenerate `SESSIONS.md` with `/workspace/tools/agents/sessionctl index`.
- Record high-level active-chat counts and known pane targets in the activation
  task.
- Copy reviewed live instruction files.
- Sync shared skills.
- Start separate fresh verification sessions, then close only those verification
  sessions.

Not allowed during non-interrupting activation:

- No `tmux send-keys`, `/status`, `/memory`, `/skills`, `/quit`, or other input
  to existing active panes.
- No restarting, resuming, closing, or attaching to existing active chats.
- No editing active task `resume.md` files unless the owning chat is idle and
  the user explicitly asks for reconciliation.
- No moving `busy/` task directories, removing worktrees, rebasing branches, or
  changing product repo state.
- No full pane transcript capture by default; record metadata only unless a
  task explicitly needs transcript evidence.

Effect on running chats:

- Existing chats are not forced to reload `AGENTS.md`, `CLAUDE.md`, or skill
  metadata.
- New sessions and later resumed/restarted sessions should pick up the new live
  instructions and synced skill mirrors.
- Lifecycle directory moves remain blocked until the relevant panes are
  reconciled or explicitly waived.

## Preflight

Create a live activation task:

```text
/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521/
```

Required files:

- `plan.md` with this plan linked,
- `notes.md` with command output and decisions,
- `rollback/MANIFEST.md`,
- `rollback/file-list.txt`,
- `rollback/task-moves.tsv` once task movement is proposed.

Preflight checks:

```bash
cd /workspace/workspace-control
git status --short --branch
git rev-parse HEAD
tools/check-sensitive-content /workspace/workspace-control
bash -n tools/workspace-status tools/workspace-artifact-inventory tools/knowledgectl tools/check-sensitive-content
/workspace/tools/skills/skillctl inventory
/workspace/tools/skills/skillctl validate
```

Record:

- workspace-control commit,
- current `/workspace/AGENTS.md` checksum,
- current `/workspace/CLAUDE.md` checksum,
- live shared skill inventory,
- provider mirror inventory,
- task counts from current and proposed status tools.

## Active Chat Inventory Gate

Before changing live instructions or moving task directories, capture passive
metadata:

```bash
tmux list-windows -t 0 -F '#{window_index}:#{window_name} panes=#{window_panes}'
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} cmd=#{pane_current_command} path=#{pane_current_path} title=#{pane_title}'
/workspace/tools/agents/sessionctl index
sed -n '1,220p' /workspace/detection-platform-metal-work/SESSIONS.md
```

For a full reconciliation pass, after the user is ready to resume or retire
active chats, handle each Claude/Codex pane:

1. Identify the owning task directory.
2. Record the provider, tmux target, session ID when visible, transcript path
   when known, branch/worktree/PR context, status, and next action in that
   task's `resume.md`.
3. Regenerate `SESSIONS.md`.
4. If the session ID is unavailable, record the tmux target and recovery
   action instead of inventing an ID.
5. If a pane is stale and safe to abandon, get explicit approval before closing
   it.

Current known issues from the 2026-05-21 audit:

- `brand-automation-corpus-llm-workers` exists in `busy/` without `resume.md`.
- Long-lived Codex panes may have stale skill metadata loaded from before the
  workspace-control skill cleanup. Validate activation from fresh provider
  sessions, not from those already-running panes.
- Tmux pane `0:10` (`brand-corpus-llm`) is actively working from the
  `brand-automation-corpus-llm-workers` planned-task prompt.
- Tmux pane `0:12` (`workflow review`) is actively working on the workflow
  review/migration context.
- Tmux pane `0:9` (`PRs`) is mid-turn in a Claude PR/merge-conflict thread.

Instruction/skill activation may proceed after passive inventory if the user
accepts the non-interrupting mode. Do not start task lifecycle movement until
the full reconciliation gate is clean or explicitly waived.

## Thin-Instructions Gate

Goal: avoid activating a large always-loaded instruction file when the same
detail can live in linked references or scoped skills.

Before Slice 3, review:

```bash
wc -l /workspace/workspace-control/current-workspace/AGENTS.md
wc -l /workspace/workspace-control/current-workspace/CLAUDE.md
rg -n "^## |^### " /workspace/workspace-control/current-workspace/AGENTS.md
```

Activation target:

- `current-workspace/CLAUDE.md` stays thin and provider-specific only.
- `current-workspace/AGENTS.md` remains a compact operating contract before
  copying live.
- Detailed procedure text is moved to existing tool READMEs, shared skills,
  specs, or reference docs.
- Task lifecycle details stay in `docs/specs/task-lifecycle.md` and
  `task-closeoff`; `AGENTS.md` carries one-line state definitions only.

Long procedure details belong in `docs/reference/live-workspace-details.md`,
tool READMEs, shared skills, and specs rather than in the always-loaded file.

## Rollback Snapshot

Before changing any live file, copy the live surfaces into the task rollback
directory:

```bash
TASK=/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521
mkdir -p "$TASK/rollback/live-files"

cp -a /workspace/AGENTS.md "$TASK/rollback/live-files/AGENTS.md"
cp -a /workspace/CLAUDE.md "$TASK/rollback/live-files/CLAUDE.md"
cp -a /workspace/agent-skills "$TASK/rollback/live-files/agent-skills"
cp -a /workspace/.claude/skills "$TASK/rollback/live-files/claude-skills"
cp -a /workspace/.agents/skills "$TASK/rollback/live-files/openai-skills"
find /workspace/detection-platform-metal-work -maxdepth 1 -type d | sort > "$TASK/rollback/task-dirs.before.txt"
```

Also write checksums:

```bash
sha256sum \
  /workspace/AGENTS.md \
  /workspace/CLAUDE.md \
  > "$TASK/rollback/checksums.before.txt"
```

This is not a platform-state backup. It is task-local workflow rollback
evidence.

## Slice 1: Read-Only Tool And Knowledge Exposure

Goal: make lookup improvements available without changing live behavior.

Actions:

1. Keep `workspace-control` as the canonical location for knowledge notes.
2. Prefer calling helper tools from `/workspace/workspace-control/tools/`.
3. Optionally add a lightweight wrapper directory later:

   ```text
   /workspace/tools/workspace-control/
   ```

   Each wrapper should exec the repo tool, not duplicate implementation.

Validation:

```bash
/workspace/workspace-control/tools/knowledgectl lint
/workspace/workspace-control/tools/knowledgectl index --check
/workspace/workspace-control/tools/workspace-status --brief
/workspace/workspace-control/tools/workspace-artifact-inventory
```

Rollback:

- Remove only wrappers created under `/workspace/tools/workspace-control/`.
- No knowledge data rollback needed if the repo path remains canonical.

## Slice 2: Shared Skills Activation

Goal: make the new shared skills and updates available to both Claude and
Codex.

Actions:

1. Review `agent-skills/skills/` diff in `workspace-control`.
2. Copy reviewed canonical skills into `/workspace/agent-skills/skills/`.
3. Run:

   ```bash
   /workspace/tools/skills/skillctl validate
   /workspace/tools/skills/skillctl sync
   ```

4. Record the skill inventory before and after.

Validation:

```bash
/workspace/tools/skills/skillctl inventory
/workspace/tools/skills/skillctl validate
find /workspace/.claude/skills /workspace/.agents/skills -maxdepth 2 -name SKILL.md | sort
```

Rollback:

```bash
TASK=/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521
rm -rf /workspace/agent-skills
cp -a "$TASK/rollback/live-files/agent-skills" /workspace/agent-skills
/workspace/tools/skills/skillctl validate
/workspace/tools/skills/skillctl sync
```

If provider mirrors still look wrong, restore them directly:

```bash
rm -rf /workspace/.claude/skills /workspace/.agents/skills
cp -a "$TASK/rollback/live-files/claude-skills" /workspace/.claude/skills
cp -a "$TASK/rollback/live-files/openai-skills" /workspace/.agents/skills
```

## Slice 3: Workspace Rules Activation

Goal: make the live agent instructions match the reviewed thin source.

Actions:

1. Confirm the thin-instructions gate passed.
2. Copy reviewed `current-workspace/AGENTS.md` to `/workspace/AGENTS.md`.
3. Keep `/workspace/CLAUDE.md` thin and importing `/workspace/AGENTS.md`.
4. Do not add provider-specific workflow rules to `AGENTS.md` unless required
   for tool differences.
5. Preserve live no-auto-push, Docker-only product execution, no staging/prod
   validation, session tracking, and activation-boundary rules.

Validation:

```bash
diff -u /workspace/workspace-control/current-workspace/AGENTS.md /workspace/AGENTS.md
sed -n '1,80p' /workspace/CLAUDE.md
/workspace/workspace-control/tools/workspace-status --brief
```

Rollback:

```bash
TASK=/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521
cp -a "$TASK/rollback/live-files/AGENTS.md" /workspace/AGENTS.md
cp -a "$TASK/rollback/live-files/CLAUDE.md" /workspace/CLAUDE.md
```

Then rerun:

```bash
/workspace/workspace-control/tools/workspace-status --brief
```

## Slice 4: Task Lifecycle Activation

Goal: add the `parked/` state and clarify `later/` vs `archived/` without
moving valuable work blindly.

Actions:

1. Create:

   ```bash
   mkdir -p /workspace/detection-platform-metal-work/parked
   ```

2. Run a read-only audit of:

   ```text
   /workspace/detection-platform-metal-work/busy/
   /workspace/detection-platform-metal-work/later/
   /workspace/detection-platform-metal-work/archived/
   ```

3. Produce a movement table before moving anything:

   ```tsv
   current_path	proposed_path	state	substate	reason	branch_or_pr	worktree_status	requires_user_approval
   ```

4. Move only approved tasks.
5. Add the lifecycle block from
   `docs/templates/task-lifecycle-block.md` to each moved task's `resume.md`.
6. Regenerate:

   ```bash
   /workspace/tools/agents/sessionctl index
   ```

Validation:

```bash
/workspace/workspace-control/tools/workspace-status --brief
/workspace/workspace-control/tools/workspace-artifact-inventory
find /workspace/detection-platform-metal-work/parked -maxdepth 2 -name resume.md -print
```

Rollback:

Use `rollback/task-moves.tsv` to reverse directory moves:

```bash
while IFS="$(printf '\t')" read -r before after _; do
  [ -z "$before" ] && continue
  [ -d "$after" ] && mv "$after" "$before"
done < "$TASK/rollback/task-moves.tsv"
/workspace/tools/agents/sessionctl index
```

If `parked/` is empty after reversal, it may remain harmlessly or be removed as
part of rollback notes.

## Slice 5: Incident Scope Cache Semantics

Goal: align future incident exports with the scope-cache model without pruning
existing payloads.

Actions:

1. Treat `docs/specs/incident-scope-cache.md` as the reference spec.
2. Keep current `/workspace/datasets/` manifests authoritative.
3. Do not delete or expire existing incident payloads in the first live slice.
4. Add future dataset-tooling changes only after a separate implementation plan.

Validation:

```bash
find /workspace/datasets -type f \( -name MANIFEST.json -o -name SNAPSHOT.md \) | wc -l
/workspace/tools/datasets/datasetctl --help
```

Rollback:

- No live data mutation in this slice.
- Revert only instruction/spec references if operators find them confusing.

## Slice 6: Pi Pilot Boundary

Goal: keep Pi available as a translation target without changing live Claude or
Codex workflows.

Actions:

1. Leave `.pi/` and `pi-pilot/` inactive.
2. Do not run Pi workflows as production coordination.
3. Use Pi artifacts only as design input until a package/schema/runtime is
   selected and validated.

Rollback:

- No live runtime rollback needed because Pi remains dark.

## Slice 7: Provider-Enforced Secret Handling

Goal: supplement behavioral rules with provider-level deny settings for obvious
secret-bearing files.

Actions:

1. Draft deny rules in workspace-control first.
2. For Claude Code, use `permissions.deny` in project/user settings for env
   files, credential JSON, and auth-state paths.
3. For Codex, use a named permission profile or sandbox configuration with
   narrower deny rules inside writable workspace roots.
4. Test in fresh Claude and Codex sessions by confirming allowed workspace reads
   still work while known env/credential paths are denied.
5. Keep credentials themselves out of workspace-control.

Validation:

```bash
tools/check-sensitive-content /workspace/workspace-control
```

Record provider-specific validation evidence in the activation task. Do not
assume these settings apply if the orchestration environment overrides
provider-local config.

Rollback:

- Restore previous provider settings from the activation task rollback snapshot.
- Restart fresh provider sessions to confirm the old settings are active.

## Overall Revert Options

### Fast Instruction Revert

Use when agents are confused by new instructions but skills/tools are otherwise
fine:

```bash
TASK=/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521
cp -a "$TASK/rollback/live-files/AGENTS.md" /workspace/AGENTS.md
cp -a "$TASK/rollback/live-files/CLAUDE.md" /workspace/CLAUDE.md
```

### Full Skills Revert

Use when a shared skill sync causes incorrect skill availability or stale
provider mirrors:

```bash
TASK=/workspace/detection-platform-metal-work/busy/workflow-improvements-go-live-20260521
rm -rf /workspace/agent-skills /workspace/.claude/skills /workspace/.agents/skills
cp -a "$TASK/rollback/live-files/agent-skills" /workspace/agent-skills
cp -a "$TASK/rollback/live-files/claude-skills" /workspace/.claude/skills
cp -a "$TASK/rollback/live-files/openai-skills" /workspace/.agents/skills
/workspace/tools/skills/skillctl validate
```

### Task Movement Revert

Use when a task was incorrectly moved to `parked/`, `later/`, or `archived/`:

1. Read `rollback/task-moves.tsv`.
2. Move the task directory back to its previous path.
3. Restore the prior `resume.md` from task-local rollback if it was modified.
4. Run `/workspace/tools/agents/sessionctl index`.

### Workspace-Control Source Revert

Use when the repo source itself needs to roll back:

```bash
cd /workspace/workspace-control
git log --oneline -5
git revert <bad-commit>
tools/check-sensitive-content /workspace/workspace-control
```

Push only after approval.

## Stop Conditions

Stop activation and use the relevant rollback if any of these happen:

- `/workspace/tools/skills/skillctl validate` fails after skill sync.
- Provider mirrors differ from canonical skills in unexpected ways.
- Agents report conflicting task-state instructions between live `AGENTS.md`
  and skill text.
- The live `AGENTS.md` activation candidate still embeds long procedure
  playbooks that already exist in tool READMEs, specs, or skills.
- `workspace-status` or `workspace-artifact-inventory` gives misleading task
  counts.
- A proposed task move touches a dirty worktree, active session, or critical
  `ACTIVE.md` entry without explicit user approval.
- A non-interrupting activation step would require sending input to, restarting,
  closing, or editing state owned by an existing active chat.
- Any activation step would touch product repo code, datasets, backups, or
  production/staging services outside the approved slice.

## Recommended First Live Slice

For the lowest-risk rollout:

1. Create the activation task and rollback snapshot.
2. Capture passive tmux/session inventory without sending input to active
   panes.
3. Review the thin `current-workspace/AGENTS.md` activation candidate.
4. Activate read-only helper/knowledge lookup by documenting repo-path commands.
5. Sync shared skills.
6. Copy reviewed thin `AGENTS.md` and `CLAUDE.md`.
7. Start fresh Claude and Codex sessions from `/workspace` and verify they load
   the intended instructions and skill mirrors.
8. Create empty `parked/`.
9. Run the task audit and produce the movement table.
10. Pause for approval before moving any task directories or reconciling active
    chat task files.
11. When you resume or retire current chats, run the full reconciliation pass.
12. Plan provider-enforced secret-read denies as the next hardening slice.

This gives agents the improved workflow immediately while preserving a simple
rollback: restore `AGENTS.md`, restore skills, remove wrappers if any, and
leave task directories untouched.
