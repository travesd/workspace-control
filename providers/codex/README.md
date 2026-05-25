# Codex Adapter

Codex should consume the shared workspace contract through `AGENTS.md` and
project-scoped config where appropriate.

Current live-compatible Codex-specific source:

- `providers/codex/config/codex.config.toml`, rendered to
  `current-workspace/config/codex.config.toml`
- `/workspace/.agents/skills/` generated from canonical shared skills

Adapter references:

- `providers/codex/references/call-a-friend-commands.md`

Shared input:

- `current-workspace/AGENTS.md` is the provider-neutral workspace contract, not
  Codex-owned adapter source.

Future responsibilities:

- Map workspace profiles to Codex custom agents only after review.
- Keep project-scoped config free of machine-local auth/provider settings.
- Document Codex-side provider command or review modes.
- Do not duplicate core or detection-platform-metal policy here.

Validation:

```bash
tools/renderctl dry-run --mode providers
```

Future activation target after approved sync:

- `/workspace/AGENTS.md`
- `/workspace/.agents/skills/`
- optional future `.codex/` project config after approval
