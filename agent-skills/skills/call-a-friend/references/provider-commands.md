# Provider Commands

Use these command shapes only after the `call-a-friend` workflow has selected a
mode, scope, and output shape.

## Codex Calling Claude

For read-only review from Codex to Claude, put the prompt immediately after
`-p`; some Claude CLI tool flags are variadic and can otherwise consume the
prompt.

```bash
claude -p "<fresh review prompt>" \
  --effort max \
  --permission-mode dontAsk \
  --allowedTools 'Read,Grep,Bash(git *),Bash(rg *),Bash(sed *),Bash(find *),Bash(pwd),Bash(ls *)' \
  --disallowedTools 'Edit,Write,MultiEdit'
```

If Claude reports quota, credentials, or session-limit failure, record the
failed attempt in task notes and continue locally.

## Claude Calling Codex

For read-only review from Claude to Codex:

```bash
codex exec -C <repo-or-worktree> -s read-only -m <model> "<fresh review prompt>"
```

For bounded implementation after explicit approval:

```bash
codex exec -C <repo-or-worktree> -s workspace-write -m <model> "<detailed implementation prompt>"
```

The owner must review resulting diffs and run the relevant validation before
accepting the friend's output.

