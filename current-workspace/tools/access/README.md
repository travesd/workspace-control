# Cloudflare Access Utility

`/workspace/tools/access/accessctl` is the shared Cloudflare Access entry point
for PhishSonar tunnel endpoints. It keeps endpoint naming, read-only probing,
browser-authenticated HTTP calls, and TCP tunnel startup in one place.

The target registry follows the metal Terraform convention:

```text
grafana-prod.phishsonar.com     -> http://grafana:3000
dashboard-prod.phishsonar.com   -> http://detection-ui-frontend:80
api-prod.phishsonar.com         -> http://detection-core:4200
db-prod.phishsonar.com          -> tcp://postgres:5432
prometheus-prod.phishsonar.com  -> http://prometheus:9090
loki-prod.phishsonar.com        -> http://loki:3100

grafana-staging.phishsonar.com     -> http://grafana:3000
dashboard-staging.phishsonar.com   -> http://detection-ui-frontend:80
api-staging.phishsonar.com         -> http://detection-core:4200
db-staging.phishsonar.com          -> tcp://postgres:5432
prometheus-staging.phishsonar.com  -> http://prometheus:9090
loki-staging.phishsonar.com        -> http://loki:3100
```

## Commands

```bash
/workspace/tools/access/accessctl targets
/workspace/tools/access/accessctl public-probe all all
/workspace/tools/access/accessctl health prod prometheus
/workspace/tools/access/accessctl curl prod prometheus /api/v1/status/config -sf
/workspace/tools/access/accessctl tcp start prod db 25432
```

`public-probe` is unauthenticated and only confirms DNS/Cloudflare/Access
boundary behavior. It does not prove origin health behind Access.

`curl` and `health` use `cloudflared access curl` in a container with the
persistent Cloudflare token volume mounted at `/home/nonroot/.cloudflared`.
On first access, `cloudflared` prints a browser login URL. Open it and leave the
command running; after the browser flow completes, the token is downloaded into
the Docker volume and reused by later commands.

`cloudflared access curl` shells out to `curl`, but the upstream Cloudflare
image does not include it. `accessctl` therefore builds a local image
`phishsonar-cloudflared-curl:local` from `/workspace/tools/access/Dockerfile`
that contains the Cloudflare binary plus Alpine `curl`.
The local image runs as cloudflared UID/GID `65532:65532`, matching the
official image used by `dbctl`.

Default token volume: `detection-db-cloudflared`. This intentionally matches
`dbctl` so the workspace has one Cloudflare Access cache. Override with
`ACCESS_CLOUDFLARED_VOLUME` only for isolated testing.
Before commands that write tokens, `accessctl` repairs the shared volume so all
token files are owned by `65532:65532` with private permissions.

## Browser Login Policy

The CLI login flow only succeeds if the Cloudflare Access application allows an
identity policy for your email. Current Terraform shape:

- `grafana` and `dashboard`: email-domain browser login.
- `db`, `prometheus`, and `loki`: browser login only when
  `db_agent_allowed_emails` is configured for the environment.
- `api`: tunnel route exists, but no Access application is defined in current
  Terraform.

If `cloudflared` prints a login URL and later times out while fetching
`https://login.cloudflareaccess.org/transfer/...`, the usual cause is that the
browser login was not completed or the Access application did not allow the
logged-in email.

## Notes

- HTTP endpoints use `cloudflared access curl`, not service-token headers.
- TCP endpoints use `cloudflared access tcp`.
- `dbctl` remains the preferred high-level DB wrapper for `psql`, one-off
  queries, and dataset exports.
