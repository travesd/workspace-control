# Thin Instructions Audit

Date: 2026-05-21

Status: review complete, implemented in workspace-control, not activated live

## Question

Do the updated workspace instructions and links follow the thin-instructions
pattern from the Karpathy follow-up: small always-loaded operating context,
scoped skills for repeatable procedures, and detailed references loaded only
when needed?

## Evidence Reviewed

- Local Karpathy follow-up:
  `/workspace/detection-platform-metal-work/investigations/notes-and-incident-cache-20260520/reviews/karpathy-followup.md`
- Workspace-control root instructions: `AGENTS.md`
- Staged live instructions: `current-workspace/AGENTS.md`
- Provider-specific import file: `current-workspace/CLAUDE.md`
- Shared skills under `agent-skills/skills/`
- Knowledge lookup docs under `knowledge/`
- New lifecycle and go-live plans under `docs/plans/` and `docs/specs/`

## Useful Karpathy Pattern

The relevant pattern is not a specific tool or provider setup. It is:

- keep the always-loaded operating contract small and close to the project,
- move repeatable procedures into scoped skills,
- keep detailed playbooks and experiment notes as references,
- give agents a narrow editable surface and a fixed validation path,
- avoid turning every task learning into a global instruction.

## Line Count Snapshot

Always-loaded or likely always-loaded surfaces:

| File | Lines | Audit |
|---|---:|---|
| `AGENTS.md` | 24 | Good. Thin workspace-control repo contract. |
| `current-workspace/CLAUDE.md` | 7 | Good. Thin provider-specific pointer. |
| `current-workspace/AGENTS.md` | 175 | Good. Thin live activation candidate. |

On-demand surfaces:

| File type | Audit |
|---|---|
| `docs/plans/*.md` | Acceptable. Long plans are linked, not session bootstrap. |
| `docs/specs/*.md` | Acceptable if linked from thin instructions. |
| `docs/reference/live-workspace-details.md` | Acceptable. Holds moved procedure detail and is loaded on demand. |
| `knowledge/*.md` | Acceptable. `knowledge/README.md` explicitly says not to load the tree at session start. |
| Most `agent-skills/skills/*/SKILL.md` | Acceptable; concise and scoped. |
| `agent-skills/skills/classifier-corpus-coverage/SKILL.md` | Too long for a skill body at 220 lines. It should be split into a short skill plus reference playbooks when next touched. |

## Findings

### 1. The staged `current-workspace/AGENTS.md` has been slimmed

The previous `current-workspace/AGENTS.md` was useful as a complete captured
operating model, but it was not thin. It combined:

- durable safety rules,
- detailed gateway usage,
- detailed DB usage,
- dataset management rules,
- platform backup layout,
- task lifecycle definitions,
- task close-off steps,
- PR migration instructions,
- archive pointers,
- backward-compatibility symlink details.

Those details were valid, but they were not all needed in the agent's first
context load. The current candidate keeps the always-loaded operating contract
thin and moves detailed procedure text to
`docs/reference/live-workspace-details.md`, tool READMEs, specs, and skills.

The thin live `AGENTS.md` now keeps:

- scope and source-of-truth boundary,
- hard execution/safety guardrails,
- primary directory map,
- short tool routing table,
- short task lifecycle state map,
- explicit links to detailed references and skills.

### 2. The lifecycle work is structurally good, but duplicated in too many surfaces

The detailed lifecycle belongs in `docs/specs/task-lifecycle.md` and the
close-off skill. `AGENTS.md` now carries only one-line state definitions and
the rule that current task state belongs under
`/workspace/detection-platform-metal-work/`.

Keep:

- `busy`: active or near-term action,
- `parked`: paused but resumable/extractable,
- `later`: lightweight backlog,
- `done`: completed,
- `archived`: reference-only after extraction/summarization,
- `investigations`: standalone research.

Detailed criteria, templates, and transition examples now live outside the
always-loaded file.

### 3. Tool instructions should link to tool READMEs

The thin live `AGENTS.md` now links rather than embedding most command examples
and operational notes. Continue to prefer:

- one-line rule in `AGENTS.md`,
- one command example only when it prevents a dangerous mistake,
- link to the tool README or relevant skill for full procedure.

Good targets:

- `/workspace/tools/gateway/README.md`
- `/workspace/tools/db/README.md`
- `/workspace/tools/datasets/README.md`
- `/workspace/datasets/MANAGEMENT.md`
- `/workspace/backups/README.md`
- `/workspace/archive/README.md`
- `/workspace/agent-skills/skills/<skill>/SKILL.md`

### 4. Shared skills mostly follow the thin pattern

Most skills are 20-70 lines and scoped. That is good because skills load only
when needed.

The exception is `classifier-corpus-coverage/SKILL.md`. It is a valuable
playbook, but the skill body is long enough that agents will pay context cost
for details before they know which slice they are doing. Split later into:

- `SKILL.md`: trigger conditions, hard rules, high-level cycle, stop
  conditions,
- `references/diagnosis.md`,
- `references/snapshot-quality-gates.md`,
- `references/promotion-validation.md`,
- `references/brand-info-logo-prompt.md`,
- `references/common-traps.md`.

This is not a blocker for workflow go-live unless that skill is part of the
first activation slice.

### 5. Knowledge lookup is aligned with thin instructions

`knowledge/README.md` already says:

- use `workspace-status` for compact orientation,
- search the generated index,
- open only specific relevant notes,
- do not load the whole knowledge tree at session start.

This matches the thin-instructions direction.

### 6. Plans and specs are appropriately long

The new go-live plan and task lifecycle spec are detailed, but they are linked
references. They should not be imported into every session. Their length is
acceptable if the live `AGENTS.md` points to them only for activation,
close-off, or lifecycle migration work.

## Recommended Thin Live Structure

Target live `AGENTS.md` budget: roughly 120-180 lines.

Proposed sections:

1. Scope and source of truth.
2. Non-negotiable guardrails:
   - verify before asserting,
   - Docker-only product execution,
   - no staging/prod validation except explicit read-only DB work,
   - no auto-push,
   - worktree rule,
   - data products go to datasets,
   - sessions/resume tracking for non-trivial work,
   - current task lifecycle root.
3. Directory map.
4. Tool routing table:
   - gateway,
   - db,
   - datasets,
   - access/observability,
   - skills,
   - sessionctl.
5. Task lifecycle one-line definitions.
6. Where details live.
7. Activation and rollback pointer.

## Go-Live Recommendation

Before live activation, keep the thin-instructions gate:

1. Review the thin `current-workspace/AGENTS.md`.
2. Keep detailed procedure text in reference docs or rely on existing tool
   READMEs/skills.
3. Run an instruction audit:

   ```bash
   wc -l current-workspace/AGENTS.md current-workspace/CLAUDE.md
   rg -n "###|^## " current-workspace/AGENTS.md
   ```

4. Confirm:
   - `current-workspace/AGENTS.md` is under 180 lines unless there is a
     deliberate exception,
   - `current-workspace/CLAUDE.md` stays thin,
   - long procedures are linked, not embedded,
   - skills remain scoped and provider-neutral.

Do not expand `current-workspace/AGENTS.md` with long procedure playbooks before
copying it live.

## Follow-Up

External provider research was completed after this audit and is recorded in
`docs/reviews/2026-05-21-claude-codex-practices-review.md`.

## Not Needed Now

- No Pi activation change is needed.
- No task-directory movement is needed.
