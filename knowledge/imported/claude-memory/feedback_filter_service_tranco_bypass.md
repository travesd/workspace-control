---
name: filter-service Tranco bypass for local-stack startup
description: When filter-service fails to start in a fresh local stack with "Initial refresh failed; starting with empty set: unzip: context deadline exceeded", point TRANCO_LIST_URL at a fast-fail address so FX OnStart returns before its deadline.
type: feedback
originSessionId: 8211f084-0b86-43f5-960a-285716976baa
---
When starting a fresh `gatewayctl` local stack and `filter-service` keeps restarting with logs like:

```
[TrancoService] Initial refresh failed; starting with empty set: unzip: context deadline exceeded
fx start failed, rolling back: context deadline exceeded
```

…the cause is that `tranco-list.eu/download/{id}/full` (the actual top-1m tar.gz, distinct from the fast `top-1m-id` URL) is too slow from this host to finish inside FX's OnStart deadline (15s by default). The OnStart hook is written to soft-fail and `return nil`, but the context has already expired by the time it returns, so FX records the start as failed and the container restart-loops.

**Bypass:** add a Compose override that points all three Tranco URLs at a connection-refused loopback so the HTTP client fails immediately and OnStart returns inside the deadline:

```yaml
services:
  filter-service:
    environment:
      TRANCO_LIST_URL: "http://127.0.0.255:1/"
      TRANCO_LATEST_ID_URL: "http://127.0.0.255:1/"
      TRANCO_DOWNLOAD_URL_TEMPLATE: "http://127.0.0.255:1/{id}"
```

Pass via `gatewayctl stack up ... --extra-override <path>`. The filter-service starts healthy with an empty Tranco set — fine for any local test that does not specifically need Tranco popular-domain matching.

**Why:** observed on 2026-05-12 bringing up `emit-features` stack on 127.0.0.2 for the configurable-classifier-features PR e2e test. Other long-running stacks on the host were healthy because they had started days earlier when the download URL was responsive; on a fresh start today the download URL timed out (`curl --max-time 20` returned exit 124) while the ID URL responded in ~0.5s. Reproducible.

**How to apply:** any time you spin up a new local stack via `/workspace/tools/gateway/gatewayctl stack up` and filter-service refuses to become healthy with the Tranco/unzip deadline pattern, include this override block. Do NOT change the upstream filter-service code or the canonical Compose file — this is a host-environment workaround.
