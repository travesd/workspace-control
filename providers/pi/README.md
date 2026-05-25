# Pi Adapter

Pi remains draft-only until the user explicitly starts the Pi migration path.

Current draft sources:

- `.pi/`
- `pi-pilot/`
- `providers/pi/config/settings.example.json`, rendered to
  `.pi/settings.example.json`

Future responsibilities:

- Translate core skills and detection-platform-metal overlays into Pi agents
  and workflows.
- Keep Pi agents/workflows referencing source layers instead of duplicating
  policy.
- Record package/schema decisions in an ADR before activation.
- Keep Pi activation separate from Claude/Codex workflow changes.

Boundary examples:

- `.pi/agents/*.md`, `.pi/workflows/*.json`, and `.pi/settings.example.json`
  are draft runnable configuration examples.
- Pi package/schema choices, adapter design notes, and mapping rationale belong
  here or in `docs/decisions/`, not inside runnable examples.
- `.pi/settings.json` remains a checked draft runtime file and is not rendered
  by `tools/renderctl`; do not treat it as live activation.

Validation:

```bash
tools/renderctl dry-run --mode providers
```

Future activation target:

- none yet
