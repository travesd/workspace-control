# Provider Adapters

Provider adapters translate core plus workspace overlay source into the formats
needed by Claude, Codex, Pi, or future harnesses.

Adapters may contain:

- wrapper instructions,
- config examples,
- custom agent definitions,
- workflow translations,
- mirror maps,
- provider-specific command caveats.

Adapters must not become the source of truth for workspace policy. Put shared
rules in `core/` or `workspaces/<name>/`, then adapt them here.

Current dry-run coverage:

- Claude config examples in `providers/claude/config/`.
- Codex config examples in `providers/codex/config/`.
- Pi settings example in `providers/pi/config/`.

Run `tools/renderctl dry-run --mode providers` to compare generated provider
config outputs against the checked-in compatibility targets. This does not sync
provider mirrors or activate Pi.
