# Call-A-Friend Commands

Claude uses the shared `call-a-friend` skill for scope, guardrails, output
shape, and acceptance criteria. This adapter reference only documents
Claude-side command examples for calling Codex as the friend provider.

## Claude Calling Codex

For read-only review from Claude to Codex:

```bash
codex exec -C <repo-or-worktree> -s read-only -m <model> "<fresh review prompt>"
```

For bounded implementation after explicit approval:

```bash
codex exec -C <repo-or-worktree> -s workspace-write -m <model> "<detailed implementation prompt>"
```

The owning Claude session remains responsible for reviewing the resulting diff,
checking for scope drift, and running the relevant validation before accepting
the friend output.

`workspace-write` constrains filesystem access but does not prove the friend
stayed inside the intended logical scope. Give the friend an explicit write set
and review the diff before accepting any implementation output.
