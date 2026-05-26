# Claude And Codex Chat-History Pattern Review

Date: 2026-05-26

Status: sanitized aggregate review; no raw transcripts preserved

## Purpose

This note maps local Claude and Codex chat-history patterns to the 2026-05-26
implementation automation research. The goal is not to archive chats. The goal
is to identify repeated workflow-control failures and turn them into reviewable
kernel requirements.

## Source And Guardrails

Reviewed local provider history metadata and session JSONL files under:

- `/home/user/.codex/history.jsonl`
- `/home/user/.codex/sessions/`
- `/home/user/.claude/history.jsonl`
- `/home/user/.claude/projects/`

Guardrails:

- no raw prompts, assistant responses, provider transcripts, secrets, or env
  values were copied into this document;
- counts are approximate signal, not audit-grade telemetry;
- provider-local history is evidence for patterns, not a source of truth for
  future workspace behavior;
- older history may include workflows that are now superseded by the 2026-05
  workspace-control changes.

## Corpus Shape

| Source | Aggregate Signal |
|---|---:|
| Codex history prompts | 2,076 |
| Claude history prompts | 7,733 |
| Combined prompt entries | 9,809 |
| Codex session JSONL files | 128 |
| Claude session JSONL files | 1,518 |
| Codex history/session footprint | 1.9G |
| Claude history/session footprint | 879M |

Large recent sessions and repeated context compaction events confirm the same
operational problem found in earlier workspace reviews: raw chat is too large,
provider-local, and lossy to be the durable control plane.

## Prompt Pattern Signals

Keyword counts from user-facing history entries:

| Pattern | Combined | Codex | Claude |
|---|---:|---:|---:|
| `implement/build/add/fix/patch` | 1,394 | 250 | 1,144 |
| `verify/validate/confirm/check` | 1,198 | 221 | 977 |
| `review/re-review/PR` | 1,183 | 288 | 895 |
| `prod/production/dbctl/database` | 669 | 118 | 551 |
| `research/investigate/audit/trace` | 504 | 77 | 427 |
| `resume/continue/status/where are we` | 460 | 120 | 340 |
| `codex/claude/agent/subagent/team` | 428 | 137 | 291 |
| `actual/real/source/evidence` | 395 | - | - |
| `browser/playwright/screenshot` | 296 | 56 | 240 |
| `wrong/incorrect/not right/nonsense/facepalm` | 160 | 33 | 127 |
| `closeoff/close off/done/archive` | 153 | 45 | 108 |
| `docker/container/local stack/compose` | 125 | 53 | 72 |
| `do not/don't/never/without approval` | 86 | - | - |
| `ultrathink` | 670 | 7 | 663 |

Rows with `-` were counted only in the combined pass.

Additional combined signals:

| Pattern | Count |
|---|---:|
| team/subagent/cross-review/second-opinion language | 63 |
| approval/no-push/no-PR/no external action language | 61 |
| durable memory/save learning/knowledge language | 45 |
| `resume.md`/`SESSIONS.md`/`ACTIVE.md`/worktree language | 217 |
| `dbctl`/read-only/query language | 87 |
| screenshots/browser-MCP/Playwright language | 254 |
| local-stack/staging/production/prod language | 1,057 |

The counts are directionally strong enough for design. They show a workspace
dominated by implementation, review, verification, investigation, DB/browser
inspection, and resumability work rather than simple Q&A.

## Session Tool Shape

Codex structured session events:

| Tool/Event | Count |
|---|---:|
| `exec_command` tool calls | 3,118 |
| `write_stdin` tool calls | 934 |
| `apply_patch` tool calls | 387 |
| `update_plan` tool calls | 16 |
| `token_count` events | 3,464 |
| `agent_message` events | 2,018 |
| `context_compacted` events | 28 |

Claude structured session events:

| Tool | Count |
|---|---:|
| `Bash` | 18,714 |
| `Read` | 15,656 |
| `Grep` | 2,816 |
| `Edit` | 2,167 |
| `Glob` | 1,862 |
| `Write` | 720 |
| `TaskUpdate` | 660 |
| `TaskCreate` | 322 |
| `Agent` | 102 |
| browser/Playwright screenshot and automation tools | 269+ |

The shape is implementation-heavy and artifact-heavy. A better workflow-control
system should therefore control execution state, validation, and closeoff
rather than only improving prompts.

## Emergent Patterns

### 1. The Default Unit Is A Task, Not A Chat

The combined history repeatedly asks agents to implement, review, investigate,
resume, continue, close off, and verify. The durable unit should be the task
artifact plus workflow state, not the provider conversation.

Kernel implication:

- initialize or locate task state early;
- classify the request before extended exploration;
- keep a short machine-readable `workflow.json` beside human `resume.md`;
- make `validation.jsonl` and closeoff summaries the durable completion record.

### 2. Verification Is A Primary User Intent

Validation, evidence, source, actual-state, and correction language appears
frequently. This is a sign that agents still over-infer from memory or stale
context.

Kernel implication:

- `source-read` and `validation` gates should be first-class;
- completion claims should cite files, commands, run IDs, or URLs;
- sealed evaluators are needed for LLM/workflow quality work;
- no workflow should mark itself complete from reasoning alone.

### 3. "Ultrathink" Is Manual Mode Routing

The high Claude-side `ultrathink` count is best interpreted as the user forcing
slower deliberate reasoning when the task was ambiguous, high impact, or likely
to suffer from shallow pattern matching.

Kernel implication:

- mode routing should be explicit and automatic;
- clear tasks use checklist mode;
- normal implementation uses deliberate engineering mode;
- ambiguous design work uses divergent-convergent mode;
- LLM/eval/classifier work uses experiment mode;
- chaotic environment work uses stabilization mode.

### 4. Environment Boundaries Are Repeated Failure Surfaces

Production, DB, local-stack, Docker, browser, and screenshot language appears
often. These are not incidental details; they are the places where a generic
agent can do the wrong thing if the workflow surface is unclear.

Kernel implication:

- preflight should identify the repo, worktree, local stack, DB access mode,
  browser artifact path, and prohibited surfaces;
- mutable surfaces and sealed evaluators should be explicit;
- approval gates must stop push, PR, live activation, destructive cleanup,
  production writes, and external writes.

### 5. Resumability Is Still A Live Pain

Resume/status/continue requests, context compaction, and large session files
show that chat history remains too central to recovering work.

Kernel implication:

- task `resume.md`, `SESSIONS.md`, `workflow.json`, and validation ledgers
  should be enough for a fresh provider to continue;
- `workflowctl status` should surface missing next actions and stale task
  state without requiring transcript review;
- closeoff should fail if durable-learning routing is not recorded.

### 6. Cross-Review Is Valuable But Too Ad Hoc

The history contains repeated team, subagent, cross-review, and second-opinion
signals. This aligns with the Karpathy `llm-council` lesson, but the workspace
needs typed review roles rather than free-form extra chats.

Kernel implication:

- add explicit review gates for high-impact plans, LLM/eval changes, and
  operating-model changes;
- review output should use findings, severity, evidence, and acceptance status;
- provider-specific subagents should consume the same task artifacts.

### 7. The User Repeatedly Enforces Approval Boundaries

No-push, no-PR, approval, and "without approval" language appears often enough
to be treated as a control-plane requirement.

Kernel implication:

- approval is a state transition, not a reminder;
- `workflowctl` should report blocked external actions rather than perform
  them;
- activation of workspace-control changes remains separate from drafting.

### 8. Durable Learning Exists But Needs Routing

The history contains recurring memory, knowledge, and learning language, and
earlier workspace reviews already found provider-local memory drift.

Kernel implication:

- every non-trivial closeoff should choose a durable home: task summary,
  workspace-control knowledge note, shared skill, ADR, dataset manifest, or
  no durable extraction;
- raw provider history should never be promoted directly into instructions;
- fresh evidence is required before turning a repeated lesson into automation.

## Relation To Karpathy Review

The chat-history patterns make the Karpathy review more concrete:

- `autoresearch` maps to bounded implementation automation: narrow mutable
  surface, sealed evaluator, budget, metric, keep/discard ledger.
- `program.md` maps to workflow prompts and rubrics as source-controlled
  programs, not hidden provider memory.
- `nanochat` maps to a small number of meaningful depth/mode profiles instead
  of many fragile flags.
- `llm-council` maps to typed cross-review gates with evidence and verdicts.
- `rendergit` and `reader3` map to context-pack generation: compress the right
  repo/task slice instead of asking the next agent to rediscover everything.
- the minimal reference implementation style maps to a small `workflowctl`
  kernel first, not a large orchestration platform.

## Design Requirements Added By History

The implementation automation kernel should prioritize:

1. `workflowctl status` and `workflowctl classify` before autonomous execution.
2. `source-read` and `validation` gates before write-heavy convenience tooling.
3. a validation ledger that records commands, artifacts, and residual risk.
4. a context-pack command that can safely summarize a task/worktree slice.
5. typed approval-stop states for push, PR, live activation, destructive
   cleanup, production writes, and external writes.
6. closeoff checks that require durable-learning routing.
7. history-derived metrics that track repeated corrections, stale task state,
   validation gaps, and tasks that still require raw chat to resume.

## Caveats

- Keyword counts are not semantic labels. They indicate recurring pressure, not
  exact task taxonomy.
- Provider histories include system prompts, tool metadata, and older operating
  models; only user-facing history entries and structured tool events were used
  for the primary signals above.
- No claim here should override current workspace-control specs without review,
  validation, and explicit activation approval.
