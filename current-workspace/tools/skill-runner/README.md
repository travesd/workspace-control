# skill-runner

Workspace-side container for running upstream `<repo>/.claude/skills/<name>/`
skills that bake host tools (`cloudflared`, `psql`, `python+requests`, `claude`)
into subprocess calls.

This is one of the options described in `/workspace/AGENTS.md` §8c
("Repo-Level Skills vs Workspace Tooling"). The upstream skill runs unmodified
inside the container; outputs land on the shared `/workspace` mount.

## Build

```bash
docker build -t detection-skill-runner:latest /workspace/tools/skill-runner/
```

## Pre-flight (one time per browser-token expiry, ~24h)

```bash
/workspace/tools/db/dbctl auth prod
/workspace/tools/access/accessctl login prod dashboard
```

Both populate the `detection-db-cloudflared` Docker volume so the runner can
reuse the cached Cloudflare Access tokens for db-prod and dashboard-prod.

## Run

```bash
/workspace/tools/skill-runner/run-skill \
  /workspace/detection-platform-metal.worktrees/<worktree> \
  <skill-name> \
  [args...]
```

The container starts `cloudflared access tcp --hostname <DB_HOSTNAME>` to
`localhost:25432` so the upstream skill's hardcoded `host=127.0.0.1 port=25432`
works unmodified. Set `SKIP_DB_TUNNEL=1` to disable for non-DB workloads.

## Mounts

| Path inside container | Source | Mode |
|---|---|---|
| `/workspace` | `$WORKSPACE_ROOT` (default `/workspace`) | rw |
| `/usr/local/bin/claude` | host `$CLAUDE_BIN` | ro |
| `/home/nonroot/.cloudflared` | Docker volume `$CLOUDFLARED_VOLUME` | rw |
| `/root/.claude/.credentials.json` | host (minimal mode) | rw |
| `/root/.claude/settings.json` | host (minimal mode) | ro |
| `/root/.claude` | host (full mode) | rw |

`CLAUDE_MOUNT_MODE=minimal` (default) shares only OAuth credentials + user
settings. Switch to `full` if claude refuses to run because of a missing path.

## Configuration

Environment variables for `run-skill`:

- `WORKSPACE_ROOT` — workspace root (default `/workspace`)
- `SKILL_RUNNER_IMAGE` — image tag (default `detection-skill-runner:latest`)
- `CLOUDFLARED_VOLUME` — shared CF token volume (default `detection-db-cloudflared`)
- `CLAUDE_BIN` — host path to claude CLI
- `CLAUDE_HOME` — host path to claude state
- `CLAUDE_MOUNT_MODE` — `minimal` (default) or `full`
- `DB_ENV_FILE` — sources `psql_password` (default `/workspace/db.env`)
- `DB_HOSTNAME` — Access target (default `db-prod.phishsonar.com`)
- `SKIP_DB_TUNNEL` — set to `1` to skip the DB tunnel bootstrap
