# Detection Agent Gateway

`gatewayctl` runs local detection-platform-metal Compose instances on separate
loopback addresses and exposes them through one host-based nginx gateway.

Use this when comparing multiple worktrees without changing repo Compose files:

```bash
/workspace/tools/gateway/gatewayctl stack up pr9 \
  /workspace/detection-platform-metal.worktrees/feat-stack-multi-instance \
  127.0.0.2 --tag latest --no-build
```

The command:

- generates a Compose override in `/workspace/.agent-gateway/instances/`
- binds published ports to the requested loopback IP
- removes the host bind for `filter-service` so it does not collide with the
  editor/code-server listener on host `:8080`
- starts `detection-ui-frontend` and its dependencies by default
- starts `detection-agent-gateway` on `127.0.0.1:18000`
- routes `http://<name>.localhost:18000/` to that instance

Common commands:

```bash
/workspace/tools/gateway/gatewayctl status
/workspace/tools/gateway/gatewayctl doctor
/workspace/tools/gateway/gatewayctl url pr9
/workspace/tools/gateway/gatewayctl stack down pr9
/workspace/tools/gateway/gatewayctl stop
```

## Local UI With Prod Dashboard API Proxy

For UI work that needs live production dashboard-backed API reads, keep the
frontend stack local and put the route into proxy mode:

```bash
/workspace/tools/access/accessctl login prod dashboard
/workspace/tools/gateway/gatewayctl proxy up pr9 \
  --local-api-prefix /api/ai-evaluator/
```

In this mode:

- local pages and assets are served from the local `detection-ui-frontend`
- configured local API prefixes are served from the local `detection-ui-api`
- every other `/api/*` request is proxied to
  `https://dashboard-prod.phishsonar.com` with Cloudflare Access auth
- mutating prod methods are blocked by default; use `--allow-mutate` only for an
  explicitly approved mutating test

Useful commands:

```bash
/workspace/tools/gateway/gatewayctl proxy list
/workspace/tools/gateway/gatewayctl proxy down pr9
```

Notes:

- `127.0.0.1` is reserved for the gateway; use `127.0.0.2`, `127.0.0.3`, etc.
  for instances.
- Use `--all` to start every Compose service instead of the UI app stack.
- Use `--extra-override <file>` for task-specific startup fixtures.
- The hostname route works through VS Code Remote when port `18000` is
  forwarded and the browser URL uses `<name>.localhost:18000`. Path-only
  code-server proxy URLs cannot select a host-based route by themselves.
