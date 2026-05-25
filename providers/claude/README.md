# Claude Adapter

Claude should consume the shared workspace contract through a thin wrapper.

Current live-compatible source:

- `current-workspace/CLAUDE.md`
- `providers/claude/config/claude.settings.json`, rendered to
  `current-workspace/config/claude.settings.json`
- `providers/claude/config/mcp.json`, rendered to
  `current-workspace/config/mcp.json`
- `/workspace/.claude/skills/` generated from canonical shared skills

Future responsibilities:

- Keep Claude-specific import/wrapper behavior here.
- Document Claude CLI command caveats that are not portable.
- Do not duplicate core or detection-platform-metal policy here.

Validation:

```bash
tools/renderctl dry-run --mode providers
```

Future activation target after approved sync:

- `/workspace/CLAUDE.md`
- `/workspace/.claude/skills/`
