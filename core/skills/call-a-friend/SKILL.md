---
name: call-a-friend
description: Invoke a fresh Claude or Codex perspective for bounded reviews, second opinions, or explicitly approved delegated implementation from a detailed plan.
---

# Call A Friend

Use this skill when the user asks to "call a friend", asks Claude to review
Codex work, asks Codex to review Claude work, wants a fresh cross-provider
second opinion, or explicitly approves offloading implementation from a detailed
plan.

## Modes

- `review`: default. Fresh agent reviews scope read-only and returns findings.
- `second-opinion`: fresh agent critiques an approach, plan, or decision.
- `implementation`: only after explicit approval, with a detailed plan and
  disjoint write scope.

## Workflow

1. Define the friend task: mode, goal, repo/path, branch/worktree, files in
   scope, out-of-scope areas, and expected output shape.
2. Send only the minimum useful context. Prefer paths, commands, diffs, and
   artifact references over broad chat summaries.
3. Do not include secrets, env values, raw provider transcripts, or unnecessary
   user-private context.
4. Use a fresh non-interactive session by default. Do not resume an old provider
   chat unless recovery of that chat is the task.
5. For review or second-opinion mode, make the friend read-only and ask for
   file/line findings, open questions, and suggested fixes.
6. For implementation mode, require explicit user approval, a detailed plan,
   a separate or clearly disjoint write scope, and post-run owner review before
   accepting changes.
7. Treat the friend output as evidence, not authority. The owning agent remains
   responsible for final judgment, edits, validation, and user-facing summary.
8. Record the call in task notes or `resume.md`: provider, model/effort if
   known, command shape, time, scope, outcome, and any limitations.

## Provider Commands

When an actual CLI invocation is needed, read
`references/provider-commands.md`. Keep provider-specific command details out
of this shared skill body unless the validator and skill policy are updated.

For implementation offload, use a write-capable mode only after approval and
only with the approved write scope. Do not let the friend push, merge, remove
worktrees, clean task artifacts, or activate live workspace changes unless the
user explicitly approved that exact action.

## Review Prompt Checklist

- What changed or is being proposed.
- Files, branch, task directory, or diff to inspect.
- Review lens: correctness, drift, validation, security, performance,
  maintainability, cost, or operator impact.
- Required output: findings first, ordered by severity, with file/line
  references where possible.
- Constraints: read-only, no secrets, no external systems unless approved, no
  live activation, no push/PR/merge.

## Guardrails

- Do not interrupt active tmux panes to call a friend.
- Do not use a friend to bypass approval gates or workspace guardrails.
- Do not ask a cheaper model to make broad architectural decisions from thin
  context.
- Prefer cheaper or lower-effort models only for bounded implementation,
  mechanical edits, formatting, fixture generation, or checklist execution from
  a high-quality plan.
- If the friend provider is unavailable, over quota, or lacks credentials,
  record that and continue with local review.
