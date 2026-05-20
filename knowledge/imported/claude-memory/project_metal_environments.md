---
name: Metal staging/prod exist alongside still-active legacy GKE
description: Metal has its own staging and prod environments; legacy non-metal staging/prod are still active in parallel. Distinguish via /workspace/classifiers.pipeline-*.env files.
type: project
originSessionId: 0a249e86-4b17-4516-81b9-13fcec4c780d
---
Metal has its own staging and prod environments. The legacy non-metal (GKE) staging and prod are **also still active**, serving traffic in parallel during migration.

**How to tell which is which** — `/workspace/classifiers.pipeline-*.env`:

| File | URL | Maps to |
|---|---|---|
| `classifiers.pipeline-staging-new.env` | `api-staging.phishsonar.com` | **metal staging** |
| `classifiers.pipeline-prod-new.env` | `api-prod.phishsonar.com` | **metal prod** |
| `classifiers.pipeline-staging.env` | `api-dev.detection.phishsonar.com` | legacy non-metal staging (still active) |
| `classifiers.pipeline-prod.env` | `api.detection.phishsonar.com` | legacy non-metal prod (still active) |

**Why:** during the GKE → metal migration both stacks run in parallel; cutover hasn't completed. The `-new` suffix marks the metal-side endpoints; the unsuffixed files are the legacy ones. Comment headers inside the `-new` files still say "GKE cluster" — those comments are stale; trust the URL not the comment.

**How to apply:**
- When asked about deployment topology, both metal and legacy GKE environments exist; don't claim "metal-only" or "no staging" based on CLAUDE.md alone — CLAUDE.md says staging/prod are off-limits *for this sandbox to validate against*, not that they don't exist.
- For proposals/rollout plans the team will execute outside the sandbox, metal staging is a real shadow/parity environment; legacy GKE prod can serve as a known-good baseline for parity checks since it still runs the existing Python classifiers.
- For sandbox-internal validation, still local-stack only (per CLAUDE.md).
- Read the URL inside the env file when uncertain, not the filename or header comment.
