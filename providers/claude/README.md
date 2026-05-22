# Claude Adapter

Claude should consume the shared workspace contract through a thin wrapper.

Current live-compatible source:

- `current-workspace/CLAUDE.md`
- `current-workspace/config/claude.settings.json`
- `/workspace/.claude/skills/` generated from canonical shared skills

Future responsibilities:

- Keep Claude-specific import/wrapper behavior here.
- Document Claude CLI command caveats that are not portable.
- Do not duplicate core or detection-platform-metal policy here.

Future activation target after approved sync:

- `/workspace/CLAUDE.md`
- `/workspace/.claude/skills/`
