# Detection DB Utility Container

Use `/workspace/tools/db/dbctl` for database access from the host. It runs both
Cloudflare Access and PostgreSQL client tooling in containers, so it does not
depend on host-installed `cloudflared`/`psql` or on the VS Code devcontainer.

## Files

- `/workspace/db.env` — read-only DB credentials. Required keys:
  `psql_username`, `psql_password`. Optional keys: `DB_NAME`,
  `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`.
- `detection-db-cloudflared` Docker volume — cached Cloudflare Access browser
  tokens. This avoids devcontainer state and avoids host UID issues with the
  `cloudflared` image.
- `/workspace/tools/db/dbctl` — tunnel and psql wrapper.

## First-Time Auth

Authenticate Cloudflare Access into the workspace-owned token directory:

```bash
/workspace/tools/db/dbctl auth prod
```

This opens/prints the Cloudflare Access browser login flow and writes the token
to the `detection-db-cloudflared` Docker volume. Re-run when the Access session
expires. For unattended access, put `CF_ACCESS_CLIENT_ID` and
`CF_ACCESS_CLIENT_SECRET` in `/workspace/db.env` instead.

## Common Commands

```bash
# Start the tunnel container
/workspace/tools/db/dbctl start prod

# Run an interactive psql session from a postgres client container
/workspace/tools/db/dbctl psql

# Run a single query
/workspace/tools/db/dbctl query "select current_database(), current_user, now();"

# Run postgres client tooling with /workspace mounted
/workspace/tools/db/dbctl exec pg_dump --schema-only > /workspace/tmp/schema.sql

# Stop the tunnel
/workspace/tools/db/dbctl stop
```

`dbctl psql`, `dbctl query`, and `dbctl exec` mount `/workspace` into the client
container and use the current working directory when it is under `/workspace`.

## Notes

- `dbctl` repairs token volume ownership before starting or authenticating:
  files are owned by cloudflared UID/GID `65532:65532`, the directory is `0700`,
  and token files are `0600`. This keeps the shared token cache compatible with
  the non-root upstream `cloudflared` image.
- The tunnel container and client container share a private Docker network
  named `detection-db-access`; the database port is not published on the host.
- Tunnel startup is guarded by a workspace lock so multiple agent/tool commands
  do not race to create the same `detection-db-tunnel` container.
- The PostgreSQL client container mounts `/workspace`; the Cloudflare tunnel
  container does not need repo/workspace file access.
- Default target is `prod` (`db-prod.phishsonar.com`). Use `staging` explicitly
  when needed.
- The DB role should remain read-only for agent workflows. Do not run mutating
  queries unless the user explicitly asks and the credential permits it.
