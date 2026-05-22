# Detection Platform Metal Overlay

This overlay is for the live `/workspace` detection-platform-metal sandbox.

It should own workspace-specific material such as:

- Docker-only product execution rules,
- local stack and gateway tooling,
- database read-only investigation rules,
- classifier and dataset workflows,
- task lifecycle path conventions,
- browser MCP and Cloudflare Access observability workflows.

Current status: source map only. Canonical live-compatible files still live in:

- `current-workspace/AGENTS.md`,
- `current-workspace/tools/`,
- `agent-skills/skills/`,
- `docs/specs/`.

Future slices should move or render this material only after generated outputs
match the current live workspace.

## Source Map

| Current Source | Future Home |
|---|---|
| `current-workspace/AGENTS.md` provider-neutral operating contract sections | `core/AGENTS.contract.md` or equivalent render input |
| `current-workspace/AGENTS.md` detection-specific sections | `workspaces/detection-platform-metal/AGENTS.overlay.md` |
| `current-workspace/AGENTS.md` live activation references | render input under `current-workspace/` until activation tooling exists |
| `current-workspace/tools/` | `workspaces/detection-platform-metal/tools/` or rendered live tool bundle |
| `docs/specs/incident-scope-cache.md` | `workspaces/detection-platform-metal/specs/incident-scope-cache.md` |
| Detection-specific shared skills | `workspaces/detection-platform-metal/skills/` |
| Task-oriented workspace bundles | `workspaces/detection-platform-metal/profiles/` |
