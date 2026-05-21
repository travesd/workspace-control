# Claude And Codex Practices Review

Date: 2026-05-21

Status: review complete, workspace-control only, not activated live

## Question

Do the staged workspace-control changes follow current official practices for
both Claude Code and Codex/OpenAI agents?

## Official Sources Checked

- OpenAI Codex customization:
  <https://developers.openai.com/codex/concepts/customization>
- OpenAI Codex `AGENTS.md`:
  <https://developers.openai.com/codex/guides/agents-md>
- OpenAI Codex skills:
  <https://developers.openai.com/codex/skills>
- OpenAI Codex memories:
  <https://developers.openai.com/codex/memories>
- OpenAI Codex permissions:
  <https://developers.openai.com/codex/permissions>
- OpenAI Codex subagents:
  <https://developers.openai.com/codex/subagents>
- OpenAI Codex long-running work best practices:
  <https://developers.openai.com/codex/learn/best-practices>
- Claude Code memory / `CLAUDE.md`:
  <https://code.claude.com/docs/en/memory>
- Claude Code skills:
  <https://code.claude.com/docs/en/skills>
- Claude Code settings:
  <https://code.claude.com/docs/en/settings>
- Claude Code subagents:
  <https://code.claude.com/docs/en/sub-agents>

## Verdict

The staged workspace-control design is aligned with current provider guidance.
It is ready for a controlled live activation after the go-live checklist is run.

The shape is correct:

- `current-workspace/AGENTS.md` is the provider-neutral operating contract.
- `current-workspace/CLAUDE.md` imports `AGENTS.md` and keeps only
  Claude-specific guidance.
- Repeatable workflows live in shared skills instead of bloating startup
  instructions.
- Detailed procedures moved to references, tool READMEs, specs, and skills.
- Provider-local memory is treated as a recall layer, not the source of
  authoritative team rules.
- Task state and session records make long-running work resumable across
  providers.

## Evidence From Local State

Line and size checks:

| File | Lines | Bytes | Assessment |
|---|---:|---:|---|
| `current-workspace/AGENTS.md` | 175 | 7,678 | Fits Claude's under-200-line target and Codex's default project-doc budget. |
| `current-workspace/CLAUDE.md` | 8 | 291 | Correctly thin. |
| `docs/reference/live-workspace-details.md` | 270 | 9,217 | Acceptable because it is on-demand reference, not startup context. |
| `agent-skills/skills/classifier-corpus-coverage/SKILL.md` | 220 | 15,742 | Usable, but should be split when next touched. |

Provider mirrors in the live workspace currently contain only the older skill
set. This is expected until activation, but the activation checklist must run
`skillctl validate` and `skillctl sync` so new skills such as
`workspace-status`, `task-closeoff`, `session-hygiene`,
`durable-learning-capture`, `agents-md-review`, `research-to-knowledge`, and
`workspace-artifact-inventory` are discoverable by both providers.

## Provider Comparison

### Startup Instructions

Codex official guidance uses `AGENTS.md` for durable project instructions and
explicitly says to keep it small. Claude Code reads `CLAUDE.md`, not
`AGENTS.md`, and recommends creating a thin `CLAUDE.md` that imports
`AGENTS.md` when a repo already uses `AGENTS.md`.

Our staged state follows this:

- Codex gets `AGENTS.md` directly.
- Claude gets `CLAUDE.md` with `@AGENTS.md`.
- Shared rules are not duplicated.
- Always-loaded detail is below both providers' practical budgets.

No change needed.

### Skills

Both providers use skills as the right home for reusable procedures and richer
task workflows. Both load only skill metadata up front and load full skill
content when the skill is relevant or invoked.

Our staged state follows this:

- Canonical skills live under `agent-skills/skills/`.
- Provider mirrors are generated under `.claude/skills/` and `.agents/skills/`.
- Shared `SKILL.md` files use portable `name` and `description` frontmatter.
- Most skills are short and task-scoped.

One follow-up remains: split `classifier-corpus-coverage` into a shorter
`SKILL.md` plus reference files. It is below Claude's documented 500-line skill
ceiling, but it is long enough that both providers pay unnecessary context
once it is selected.

### Memory And Knowledge

Codex memories are a local recall layer and should not hold rules that must
always apply. Claude Code similarly distinguishes written `CLAUDE.md`
instructions from auto memory. Both providers treat these as context, not hard
enforcement.

Our staged state follows this:

- Required team guidance stays in `AGENTS.md`, specs, tool docs, and skills.
- Durable provider-neutral notes live in `knowledge/`.
- Provider-local memories remain optional and non-authoritative.
- Knowledge lookup is search-first rather than "load everything at startup."

No change needed.

### Long-Running Work

Codex recommends one coherent thread per unit of work, use of resume/fork/agent
controls, and bounded subagents for exploration, tests, or triage. Claude Code
subagent guidance is similar: delegate bounded work that would flood the main
context, keep subagents scoped by tool access, and use project/user definitions
only when the same role recurs.

Our staged state follows this:

- `resume.md` and generated `SESSIONS.md` preserve task recovery state.
- `sessionctl` standardizes Claude/Codex launch and recovery records.
- Review checkpoints define when to use second-agent critique.
- The repo does not create custom subagents prematurely; that is correct.

No change needed.

### Permissions And Secret Handling

This is the main hardening gap.

Claude Code official guidance distinguishes behavioral instructions from
enforced settings and recommends `permissions.deny` for sensitive files such as
env files and credentials. Codex official guidance similarly supports
permission profiles with narrower deny rules inside writable roots.

Our staged state has strong behavioral rules and a sensitivity checker, but
`current-workspace/config/claude.settings.json` is empty and
`current-workspace/config/codex.config.toml` currently only records the browser
MCP server. That is acceptable for documentation/go-live planning, but it is
not enforcement.

Recommendation before or shortly after live activation:

- Add tested Claude Code `permissions.deny` entries for `/workspace/*.env`,
  `.env*`, credential JSON files, and known auth-state files.
- Add a tested Codex permission profile that keeps intended workspace roots
  writable while denying env/credential file reads.
- Validate both in real provider sessions before relying on them. The current
  orchestration environment may still override provider-local settings.

This is not a blocker for activating the instruction layout, but it should be
treated as the next safety hardening item.

### Provider-Specific Files

Claude Code can use `.claude/rules/` for path-scoped instructions, and Codex can
use nested `AGENTS.md` files. We should not add provider-only rule trees unless
a rule is truly provider-specific. The provider-neutral design remains better
for this workspace because Claude imports `AGENTS.md` and Codex reads it
directly.

No change needed.

## Readiness

Ready to proceed with controlled live activation when approved, with these
activation checks:

1. Copy only the staged live files described in the go-live plan.
2. Run `skillctl validate` and `skillctl sync`.
3. Confirm both provider mirrors contain the same staged skill set.
4. Start fresh Claude and Codex sessions from `/workspace`.
5. Verify Claude loads `CLAUDE.md -> AGENTS.md`.
6. Verify Codex loads `AGENTS.md` and discovers `.agents/skills`.
7. Run `workspace-status --brief`.
8. Keep the previous live files backed up for rollback.

## Follow-Ups

- Split `classifier-corpus-coverage` into a concise skill plus references.
- Add and test provider-enforced secret-read deny rules.
- Consider custom subagents only after repeated tasks prove a stable role,
  such as read-only workspace auditor or review-only instruction drift checker.
