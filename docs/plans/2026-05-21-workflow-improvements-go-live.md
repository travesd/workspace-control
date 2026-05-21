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

Use this order:

1. Snapshot live workspace-control-relevant state.
2. Apply the thin-instructions gate before copying any always-loaded file.
3. Activate read-only helpers and knowledge lookup.
4. Activate shared skills.
5. Activate workspace rules from a thin `AGENTS.md`.
6. Create `parked/` and run a dry-run task audit.
7. Move only explicitly approved task directories.
8. Leave Pi pilot disabled until a separate harness decision.

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
- Any activation step would touch product repo code, datasets, backups, or
  production/staging services outside the approved slice.

## Recommended First Live Slice

For the lowest-risk rollout:

1. Create the activation task and rollback snapshot.
2. Review the thin `current-workspace/AGENTS.md` activation candidate.
3. Activate read-only helper/knowledge lookup by documenting repo-path commands.
4. Sync shared skills.
5. Copy reviewed thin `AGENTS.md`.
6. Create empty `parked/`.
7. Run the task audit and produce the movement table.
8. Pause for approval before moving any task directories.

This gives agents the improved workflow immediately while preserving a simple
rollback: restore `AGENTS.md`, restore skills, remove wrappers if any, and
leave task directories untouched.
