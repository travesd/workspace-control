# Workspace Snapshot Seed

Captured: 2026-05-20

This directory is a sanitized seed snapshot of the current `/workspace` operating model.

## Included

- `AGENTS.md` and `CLAUDE.md` workspace instructions.
- `config/` sanitized MCP / provider project settings:
  - `mcp.json` copied from `/workspace/.mcp.json`
  - `codex.config.toml` copied from `/workspace/.codex/config.toml`
  - `claude.settings.json` copied from `/workspace/.claude/settings.json`
- `tools/` copied from `/workspace/tools/`, excluding `__pycache__` and `*.pyc`.

## Excluded

- Env files and credentials: `db.env`, `docker-swarm.env`, `pivoter.env`, `*.env`, service-account JSONs.
- Runtime state: `.agent-*`, `.playwright-mcp`, provider transcripts, telemetry, logs, SQLite files.
- Product repos and worktrees.
- Datasets, backups, archive data, screenshots, and raw task artifacts.

## Notes

This snapshot is historical source material. The active workspace remains `/workspace`; changes here do not automatically affect live tooling.

When a workflow becomes canonical, update the live workspace explicitly and record the decision in `docs/decisions/`.
