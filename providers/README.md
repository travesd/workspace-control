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

