# Incident Scope Cache Spec

Status: proposed, not active live behavior

Date: 2026-05-20

This spec describes the desired future shape for local detection incident exports. It is staged in `workspace-control` only. It does not change live `datasetctl`, `/workspace/tools`, `/workspace/datasets`, or any dataset payload.

## Goal

Keep exact investigation scope and provenance locally while treating full incident payloads as cacheable unless they are explicitly promoted to durable fixtures.

The local store should answer:

- which query selected which incidents,
- when and why the scope was created,
- which incident version/hash was seen,
- which task/issue/model/config used it,
- whether full payloads are currently cached,
- whether generated snapshot JSONL exists or can be regenerated.

## Terms

- **Scope index**: durable metadata for query runs, SQL/API filters, row counts, memberships, incident IDs, row hashes, and task references.
- **Projection index**: durable searchable summary fields copied from incident payloads or query rows, such as subject, type, client, source, judgement, outcome, created/updated time, and first/last seen run.
- **Payload cache**: full incident payloads, related table payloads, and generated snapshot JSONL. Cached by default, durable only when promoted.
- **Materialization**: command output generated from a run membership, such as IDs, incident JSONL, or snapshot JSONL.
- **Durable fixture**: payload data intentionally retained because future evals/tests need the payload itself.
- **Backup**: point-in-time platform recovery capture. Backups belong under `/workspace/backups/`, not `datasetctl`.

## Current Behavior To Preserve

- `run_id` is the query result set.
- Query rows are stored as memberships.
- Incident versions are deduplicated by source environment, incident ID, and row hash.
- Snapshot JSONL is for future API import shape only.
- No API import, DB writes, or `detection_data` promotion happen during export.

## Proposed Layers

| Layer | Retention | Contents |
|---|---|---|
| Scope index | durable | runs, exact SQL/API filters, query hash, memberships, row hashes, counts, task refs |
| Projection index | durable | searchable incident summary fields for local discovery |
| Payload cache | expiring by default | full payloads, related rows, generated materializations |

Never prune run metadata, query text/hash, memberships, row hashes, row counts, manifests, or eviction audit rows.

## Retention Classes

| Class | Meaning |
|---|---|
| `ephemeral` | Short-lived exploratory payload cache. Keep scope metadata. |
| `task-cache` | Payload cache for an active or recently completed task. Keep scope metadata. |
| `reusable-scope` | Keep membership indefinitely; payload cache may expire unless pinned. |
| `durable-fixture` | Preserve payloads with a manifest explaining why the payload is the reusable data product. |
| `backup` | Out of scope for `datasetctl`; use `/workspace/backups/`. |
| `legacy-retained` | Existing pre-retention exports kept unchanged until reviewed. |

## Proposed DuckDB Schema Extensions

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
  version TEXT PRIMARY KEY,
  applied_at TIMESTAMP NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
  tag_id TEXT PRIMARY KEY,
  namespace TEXT NOT NULL,
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  UNIQUE(namespace, key, value)
);

CREATE TABLE IF NOT EXISTS run_tags (
  run_id TEXT NOT NULL,
  tag_id TEXT NOT NULL,
  PRIMARY KEY (run_id, tag_id)
);

CREATE TABLE IF NOT EXISTS incident_tags (
  source_env TEXT NOT NULL,
  incident_id TEXT NOT NULL,
  row_hash TEXT NOT NULL,
  tag_id TEXT NOT NULL,
  assigned_by TEXT,
  assigned_at TIMESTAMP NOT NULL,
  reason TEXT,
  PRIMARY KEY (source_env, incident_id, row_hash, tag_id)
);

CREATE TABLE IF NOT EXISTS run_retention (
  run_id TEXT PRIMARY KEY,
  retention_class TEXT NOT NULL,
  expires_at TIMESTAMP,
  pinned BOOLEAN NOT NULL,
  reason TEXT,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS incident_projection (
  source_env TEXT NOT NULL,
  incident_id TEXT NOT NULL,
  row_hash TEXT NOT NULL,
  subject TEXT,
  type TEXT,
  source TEXT,
  client_id TEXT,
  judgement TEXT,
  outcome TEXT,
  source_created_at TIMESTAMP,
  source_updated_at TIMESTAMP,
  first_seen_run_id TEXT,
  last_seen_run_id TEXT,
  PRIMARY KEY (source_env, incident_id, row_hash)
);

CREATE TABLE IF NOT EXISTS payload_cache_entries (
  source_env TEXT NOT NULL,
  cache_key TEXT NOT NULL,
  incident_id TEXT,
  row_hash TEXT,
  artifact_kind TEXT NOT NULL,
  file_path TEXT,
  byte_count BIGINT,
  content_hash TEXT,
  cache_state TEXT NOT NULL,
  cached_at TIMESTAMP,
  expires_at TIMESTAMP,
  last_used_at TIMESTAMP,
  promoted_dataset_ref TEXT,
  PRIMARY KEY (source_env, cache_key)
);

CREATE TABLE IF NOT EXISTS cache_eviction_log (
  eviction_id TEXT PRIMARY KEY,
  created_at TIMESTAMP NOT NULL,
  dry_run BOOLEAN NOT NULL,
  retention_class TEXT,
  candidate_count BIGINT NOT NULL,
  candidate_bytes BIGINT NOT NULL,
  removed_count BIGINT NOT NULL,
  removed_bytes BIGINT NOT NULL,
  manifest_json TEXT NOT NULL
);
```

## Proposed CLI Surface

These commands are future target behavior, not active live commands:

```bash
datasetctl cache status
datasetctl runs tag <run_id> namespace:key=value
datasetctl runs retention <run_id> --class <retention-class> [--expires-at <date>] [--pin]
datasetctl export incidents --retention-class <class> --tag namespace:key=value ...
datasetctl cache prune --dry-run
```

Future pruning must start as dry-run only. Non-dry-run deletion requires a separate reviewed decision.

## Default Export Behavior

Future default retention:

- `task-cache` when `--task-path` is supplied.
- `reusable-scope` otherwise.

During compatibility rollout, snapshot JSONL generation should remain compatible with existing callers. Flipping to opt-in materialization requires a separate caller review.

## Migration Notes

1. Add migrations non-destructively.
2. Mark existing runs `legacy-retained`.
3. Backfill tags from run name, task path, query path, source environment, and manifest path.
4. Backfill projection rows from existing current/version payloads where available.
5. Report cache status before adding any prune behavior.

## Why Not Local Postgres Now

The current need is retention, discoverability, and exact scope provenance. DuckDB already fits the read-mostly catalog and Parquet inspection model. Local Postgres would add service lifecycle, volume, port, migration, and "second source of truth" risk without solving the immediate problem.

Postgres can be revisited only if there is measured writer-concurrency pressure or a local service must query a Postgres-compatible incident cache.
