---
name: cloudflare-access-observability
description: Use Cloudflare Access protected PhishSonar tunnel endpoints for read-only observability, dashboard, API, Loki, Prometheus, and DB reachability checks through workspace Docker tooling.
---

# Cloudflare Access Observability

Use this skill when investigating or validating Cloudflare Access protected
PhishSonar tunnel endpoints, including Grafana, detection-ui/dashboard,
detection-core API, Prometheus, Loki, or the read-only DB tunnel.

## Guardrails

- Treat prod and staging HTTP endpoints as read-only unless the user explicitly
  authorizes a mutating action.
- Prefer status, health, metadata, query, and log-read calls. Do not use POST,
  PUT, PATCH, or DELETE against prod/staging without explicit approval.
- Do not print Cloudflare Access JWTs, cookies, tunnel tokens, or token-cache
  file contents. Browser login URLs printed by `cloudflared` are expected during
  first-use CLI authentication; do not persist them in notes.
- Use workspace Docker tooling. Do not install host `cloudflared`, `curl`,
  `psql`, or provider CLIs for this workflow.
- For DB queries, prefer `/workspace/tools/db/dbctl` or dataset skills. Use
  `/workspace/tools/access/accessctl tcp` only for generic tunnel reachability
  or when building a new client wrapper.

## Workflow

1. Read the target registry:
   ```bash
   /workspace/tools/access/accessctl targets
   ```
2. Confirm public DNS/Cloudflare behavior without authenticating:
   ```bash
   /workspace/tools/access/accessctl public-probe all all
   ```
   Interpret 302 as Cloudflare Access login, 403 as Cloudflare boundary or
   origin/API auth refusal. This does not prove origin health behind Access.
3. For authenticated HTTP checks, use the persistent Docker Cloudflare token
   volume. If no token exists for that Access application, `cloudflared` prints
   a browser login URL; open it and leave the command running until the token is
   downloaded. Then the same command continues:
   ```bash
   /workspace/tools/access/accessctl health prod prometheus
   /workspace/tools/access/accessctl curl prod prometheus /api/v1/status/config -sf
   /workspace/tools/access/accessctl curl prod loki /ready -sf
   ```
   If the command times out while fetching `login.cloudflareaccess.org/transfer`,
   check the Access application's browser-login policy. In current Terraform,
   `db`, `prometheus`, and `loki` need `db_agent_allowed_emails` configured for
   browser SSO.
4. For DB work, use:
   ```bash
   /workspace/tools/db/dbctl auth prod
   /workspace/tools/db/dbctl query "select current_database(), current_user;"
   ```

## Targets

Current Terraform convention:

- `grafana-{env}.phishsonar.com` -> Grafana
- `dashboard-{env}.phishsonar.com` -> detection-ui frontend/API proxy
- `api-{env}.phishsonar.com` -> detection-core API
- `db-{env}.phishsonar.com` -> Postgres TCP tunnel
- `prometheus-{env}.phishsonar.com` -> Prometheus API
- `loki-{env}.phishsonar.com` -> Loki API

Use `prod` and `staging` as the environment names.
