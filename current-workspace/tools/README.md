# Workspace Tools Snapshot

Source: `/workspace/tools/`

Captured: 2026-05-20

This is a sanitized snapshot of the workspace helper tools. Runtime caches and bytecode were excluded.

## Tool Index

| Path | Purpose |
|---|---|
| `access/accessctl` | Cloudflare Access observability wrapper for dashboard/API/log/metric checks. |
| `agents/sessionctl` | Claude/Codex session tracking, resume metadata, transcript lookup, tmux launch helpers, and `SESSIONS.md` generation. |
| `browser-mcp/browser-mcp` | Wrapper for browser MCP sessions against local detection UI routes. |
| `datasets/datasetctl` | Managed detection incident export/materialization tool backed by DB utility containers and local dataset manifests. |
| `db/dbctl` | Read-only DB tunnel/client wrapper using workspace Docker containers. |
| `gateway/gatewayctl` | Local multi-worktree stack gateway for isolated detection-platform-metal instances. |
| `skill-runner/run-skill` | Containerized runner for upstream skills that expect laptop-style host tools. |
| `skills/skillctl` | Validates and syncs shared Agent Skills between canonical and provider mirror directories. |

## Guardrails

- Repo code still runs in containers.
- Do not source env files directly on the host.
- Do not print secrets from `/workspace/db.env` or Cloudflare Access state.
- Treat this snapshot as documentation and seed material; the live tools remain under `/workspace/tools/`.

## Proposed Tooling Specs

- `docs/specs/incident-scope-cache.md` describes a staged future direction for `datasetctl` retention/tag/cache semantics. It is not active live behavior.
