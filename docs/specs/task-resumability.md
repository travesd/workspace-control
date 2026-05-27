# Task Resumability Spec

Status: draft in workspace-control; operating standard after approved live
activation

Date: 2026-05-21

This spec defines how task notes should make workspace work resumable without
depending on the original chat. Chat history remains useful forensic context,
but it should not be the primary source of task state.

## Goal

A fresh Claude, Codex, or future harness agent should be able to answer these
questions from task artifacts:

1. What is the task trying to achieve?
2. What changed so far?
3. What is the current exact state?
4. What is the next command or action?
5. What evidence supports the current state?
6. What must not be touched?

## Source Translation

This is a workspace-specific system. The external methods below inform the
shape, but none is adopted wholesale.

| Source | Borrow | Do Not Copy Wholesale | Workspace Mapping |
|---|---|---|---|
| Claude Code memory docs: https://docs.claude.com/en/docs/claude-code/memory | Keep always-loaded instructions concise; load detailed context on demand. | Do not put task history in provider memory or global instructions. | Thin `AGENTS.md`, task-local notes, searchable knowledge, compact resumes. |
| OpenAI AGENTS.md format: https://github.com/openai/agents.md and Codex intro: https://openai.com/index/introducing-codex/ | Treat agent docs like operational README files with verifiable commands and evidence. | Do not use chat-only claims as handoff evidence. | Record paths, commands, validation results, worktree/PR links, and artifacts. |
| Diataxis: https://diataxis.fr/start-here/ | Separate documentation by purpose. | Do not make one giant all-purpose task document. | `resume.md` for handoff, `notes.md` for working log, `SUMMARY.md` for closeoff, skills for procedures, knowledge notes for references. |
| Cornell note-taking: https://lsc.cornell.edu/how-to-study/taking-notes/cornell-note-taking-system/ | Condense raw notes into cues and summaries. | Do not copy an academic page layout. | Append compact ledger entries, then extract current truth into `resume.md`. |
| ADRs: https://adr.github.io/ and GOV.UK ADR example: https://docs.publishing.service.gov.uk/repos/govuk-infrastructure/architecture/decisions/0001-record-architecture-decisions.html | Capture consequential decisions with context and consequences. | Do not create ADRs for routine task details. | Use ADRs or decision notes only for reusable operating-model decisions. |
| PARA: https://fortelabs.com/our-best-free-resources/ | Organize by actionability and lifecycle. | Do not hide active work in topic buckets. | Use `busy/`, `parked/`, `later/`, `done/`, `archived/`, and `investigations/` by next action. |

## Artifact Roles

Use the smallest set that makes the task recoverable.

| Artifact | Purpose | Required When |
|---|---|---|
| `resume.md` | Current truth, next action, session pointers, state, constraints. | Any non-trivial `busy/` or `parked/` task. |
| `notes.md` | Append-only working ledger with evidence, decisions, risks, and cues. | Multi-step tasks, investigations, or tasks where chat context contains decisions. |
| `SUMMARY.md` | Closeoff result, validation, durable learnings, cleanup decision. | `done/` and `archived/` task moves. |
| ADR or decision note | Durable consequential decision with context and consequences. | The choice changes workspace or product operating policy. |
| Knowledge note | Reusable fact, gotcha, or method with source and re-verification rule. | The learning applies beyond one task. |
| Shared skill | Repeatable multi-step procedure. | The workflow should be invoked by future agents. |
| Dataset manifest | Data scope, provenance, retention, and regeneration instructions. | Data product is reusable beyond the task. |

## Resume Packet

Every non-trivial task `resume.md` should include or clearly point to these
fields:

```markdown
## Resume Packet

- Task path:
- Lifecycle state:
- Goal:
- Current state:
- Exact next action:
- Branch/worktree/PR:
- Related tasks:
- Sessions/transcripts:
- Validation done:
- Validation still needed:
- Important decisions:
- Constraints and guardrails:
- Artifacts and evidence:
- Open questions:
- Chat dependency: optional | useful-for-history | required
- Chat dependency reason:
```

`Chat dependency` definitions:

- `optional`: task artifacts are sufficient; chat is not needed.
- `useful-for-history`: chat may explain how the task got here, but is not
  required to resume.
- `required`: task cannot be resumed safely without a specific chat or
  transcript. Record the missing state and the transcript path or session ID.

If `Chat dependency` is `required`, reduce it to `useful-for-history` or
`optional` before pausing when feasible.

## Notes Ledger

Use compact append-only entries in `notes.md`. Prefer one useful entry after a
meaningful event over raw transcript summaries.

```markdown
### 2026-05-21T12:00Z - short cue

- Type: decision | evidence | action | validation | risk | blocker | user-preference | learning | next
- Context:
- Entry:
- Evidence:
- Follow-up:
```

Keep entries factual:

- `Context`: why this note exists.
- `Entry`: the condensed point.
- `Evidence`: path, command, PR, dataset, screenshot, or source.
- `Follow-up`: next action or extraction target, if any.

Do not store secrets, raw provider transcripts, broad conversation summaries, or
large data dumps in task notes.

## Extraction Rules

At pause, handoff, closeoff, or parking:

| Finding | Durable Home |
|---|---|
| Current task state or next action | `resume.md` |
| Working evidence, commands, local observations | `notes.md` |
| Consequential decision | `resume.md` now, ADR or decision note if reusable |
| User preference | task notes first; promote to skill, knowledge, or `AGENTS.md` only after review |
| Repeatable procedure | shared skill |
| Reusable fact, gotcha, or method | `knowledge/*.md` |
| Reusable dataset or incident scope | `/workspace/datasets/` manifest |
| Completed outcome | `SUMMARY.md` |

## Resumability Score

Score a task 0-10. One point each:

1. Goal is explicit.
2. Lifecycle state and reason are explicit.
3. Exact next action is present.
4. Branch, worktree, PR, and session context are recorded when applicable.
5. Validation already done includes commands, results, or evidence paths.
6. Remaining validation, risks, or blockers are explicit.
7. Artifacts, datasets, screenshots, or generated outputs are linked.
8. Important decisions, preferences, and constraints are captured.
9. Chat dependency is classified and justified.
10. Durable extraction decision is recorded: none, done, or pending target.

Quality bands:

- `0-3`: not resumable; requires original chat or author.
- `4-6`: partially resumable; useful but still chat-dependent.
- `7-8`: task-artifact resumable; acceptable for normal pause or handoff.
- `9-10`: durable and extractive; preferred for parked, done, or archived work.

Targets:

- `busy/`: at least 7 before a planned handoff.
- `parked/`: at least 8, with restart or extraction condition.
- `done/`: at least 8, with `SUMMARY.md`.
- `archived/`: at least 9 or an explicit reason why no further recovery is
  needed.

## Metrics

Track these during workspace hygiene reviews:

- percentage of non-trivial tasks with a complete resume packet,
- percentage of parked tasks with a concrete restart or extraction condition,
- percentage of tasks where chat dependency is `required`,
- average time for a fresh agent to recover task state,
- stale `busy/` task count,
- durable learnings extracted to skills, knowledge, ADRs, or dataset manifests,
- resume drift findings found during closeoff.

These metrics are feedback signals, not bureaucracy. If agents skip the format,
reduce friction. If resumed tasks still need chat, strengthen the packet.

## Cadence

- Start: create or update `resume.md` when work becomes non-trivial.
- During work: add `notes.md` entries for decisions, evidence, validation,
  risks, user preferences, and next-action changes.
- Before pause or handoff: update the resume packet and session index.
- Before parking: score resumability and record restart or extraction condition.
- Before done/archive: write `SUMMARY.md`, capture durable learnings, and record
  cleanup or preservation decisions.
