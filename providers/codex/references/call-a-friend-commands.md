# Call-A-Friend Commands

Codex uses the shared `call-a-friend` skill for scope, guardrails, output
shape, and acceptance criteria. This adapter reference only documents
Codex-side command examples for calling Claude as the friend provider.

## Codex Calling Claude

For read-only review from Codex to Claude, put the prompt immediately after
`-p`; some Claude CLI tool flags are variadic and can otherwise consume the
prompt. Prefer passing the relevant diff and file paths in the prompt so the
friend can work with `Read` and `Grep` only.

```bash
claude -p "<fresh review prompt>" \
  --effort max \
  --permission-mode dontAsk \
  --allowedTools 'Read,Grep' \
  --disallowedTools 'Edit,Write,MultiEdit,Bash'
```

If shell-backed inspection is essential, add only exact read-only command
patterns needed for the review. Do not allow broad patterns such as
`Bash(git *)`, `Bash(find *)`, or `Bash(sed *)`; those can mutate state.

If Claude reports quota, credentials, or session-limit failure, record the
failed attempt in task notes and continue locally.
