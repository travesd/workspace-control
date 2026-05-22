# Pi Adapter

Pi remains draft-only until the user explicitly starts the Pi migration path.

Current draft sources:

- `.pi/`
- `pi-pilot/`

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

Future activation target:

- none yet
