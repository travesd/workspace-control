---
name: classifier-corpus-coverage
description: Drive snapshot-backed detection_data coverage for every active client across every deployed classifier. Diagnoses prod gaps, harvests Chrome-scraped snapshots, applies the candidate-quality gates, validates, promotes, and verifies the classifier-worker actually consumes the result. Includes the parallel brand_info / brand_logo_prompt workflow for the LLM evaluator.
---

# Classifier Corpus Coverage

A workflow skill for an agent operating an isolated detection-platform-metal sandbox. Goal: every active production client has high-quality, snapshot-backed detection_data for every classifier they're enrolled in, plus brand_info + brand_logo_prompt rows for the LLM evaluator.

This is a **strategic, repeatable** loop, not a one-off promote. Each cycle through it adds coverage; over time the corpus moves from legacy seed/backfill rows to fresh snapshot-backed rows.

## When to use this skill

- A new production client is onboarded -> seed their corpus
- A new classifier is deployed -> backfill coverage for existing clients
- Periodic refresh -> replace legacy `source_type='corpus'` / `'backfill-*'` rows with snapshot-backed equivalents
- Investigating a recurring FP / FN that traces back to thin or stale corpus
- Auditing whether internal detection clients (PhishFort's own brands) have parity with paying clients

## Prerequisites

- Local detection-platform-metal stack running (via `gatewayctl stack up`). Must include `detection-core`, `detection-ui-{api,frontend}`, and **`classifier-worker` + `redis-classifier-data`** - without classifier-worker the manifest endpoint 502s and the Classifier Data UI degrades to fallback mode.
- Read-only prod DB access via `/workspace/tools/db/dbctl` (`dbctl auth prod`, `dbctl start prod`).
- The client seed payload (`POST /api/v1/clients/import`) already loaded into the local stack so client IDs and canonical domains align with prod.
- Familiarity with: snapshot lifecycle, the classifier manifest contract shape, the `__system__` pseudo-client convention.

## Hard rules

1. **Snapshot-backed only.** Every promoted row sets `source.type = "snapshot"` with `source.ref` = the numeric local snapshot id. Non-numeric refs (e.g. legacy `"build:1"`, `"backfill-validated:..."`) silently break the favicon evidence helper.
2. **Chrome-only scrape.** Do not enable Oxylabs / scraper fallback for this initiative. Verify `SCRAPE_DEFAULT_METHOD=chrome`, `OXYLABS_DOMINFO_ENABLED=false`.
3. **Canonical domains only.** Use the client's `domains` field; do not snapshot misc / social URLs in this workflow.
4. **No staging or production writes.** All writes go to the local stack. Read-only prod access only.
5. **Test-client lineage stays out.** Drop rows whose client name contains `(test client)` before promotion; or, if you need to test classifier-worker on a pseudo-system row, use `client_id="__system__"`.
6. **No promotion without validation.** A two-pass LLM validation + reconciliation against negative controls is the gate.

## The cycle

### 1. Diagnose - what's the gap?

Query prod for the current `(client x classifier-data_type x source_type)` matrix. The question you're answering: *for each active client, which classifiers do they have **snapshot-backed** coverage for, vs legacy/manual coverage, vs nothing at all?*

Use `dbctl query` (read-only). Output one row per (client x target_type x data_type x source_type) with counts and distinct target IDs. Pivot in Python to produce a per-client coverage matrix.

What "good coverage" looks like, per classifier (from the manifest):

| Classifier | Required per client | Minimum |
|---|---|---|
| `domain_f0_typosquat[_fast]` | One `domain:domain_name` row per canonical domain | every canonical domain |
| `domain_f4_favicon_comparison` | Either `dom_favicon_md5` or `http_favicon_md5` per canonical domain (prefer `http_favicon_md5` as canonical when DOM and HTTP match) | one per canonical domain that has a meaningful favicon |
| `domain_f4_similar_html_text` | `domain:http_inner_text` from a substantive HTTP response | >=1 per client; richer is better |
| `domain_f5_similar_domhtml_inner_text` | `domain:dom_inner_text` from a Chrome scrape | >=1 per client |
| `domain_f5_similar_title` | `domain:dom_title` for a brand-specific (non-noisy) page title | >=1 per client |
| `domain_fN_similar_ssdeep_hash` | DOM ssdeep `hash_entry` for a substantive legitimate page | >=1 per client; multiple owned domains preferred |
| `unified_incident_evaluator` | `brand:brand_info` + `brand:brand_logo_prompt` | one of each per client |

A client with `source_type='snapshot'` rows for all seven is "covered". Anything less is a gap; record per (client, classifier) what's missing.

### 2. Plan - priority

Rank clients with no snapshot-backed coverage above those with partial. Prefer clients whose only coverage is legacy `source_type='corpus'` (the pre-snapshot backfill) since those rows are fingerprints from data the classifier no longer remembers having harvested.

Group target domains by client; batch <=10 snapshot jobs per cycle so Chrome doesn't thrash.

### 3. Snapshot generation

Use a workflow script modelled on the canonical pattern at `/workspace/detection-platform-metal-work/busy/local-brand-snapshot-harvest/snapshot_harvest.py`. The harness:

- Reads canonical-domain targets per client from `GET /api/clients/active`
- POSTs `/api/v1/snapshots/build/domain/{clientId}/{domain}` per target
- Records job results to a JSONL log
- Re-fetches each created snapshot via `GET /api/snapshots/{id}` and scores it

Quality scoring rules:

- Reject if HTTP status >= 400 or DOM scrape error present
- Reject if `text_length < 250`
- Reject if any of these regexes match the combined title+text (NON_CONTENT_PATTERNS):
  ```
  \bparked\b, \bdomain (is )?(for sale|available)\b, \bcoming soon\b, \bunder construction\b,
  \baccess denied\b, \b403 forbidden\b, \b404\b, \bnot found\b, \bprivacy error\b,
  \bsecurity check\b, \bchecking your browser\b, \btemporarily unavailable\b,
  \bjust a moment\b, \bperforming security verification\b, \bray id:?\b,
  ^\s*<style\b, ^\s*<!doctype\b, ^\s*<html\b
  ```
  The last three catch CSS-leak / raw-HTML pages (Notion default site frame, etc.) - discovered the hard way during snap 76 review.
- Otherwise mark quality `high` if it has at least one of: dom ssdeep, http ssdeep, screenshot pHash, favicon MD5, favicon pHash.

### 4. Candidate generation - the six quality gates

Use a generator modelled on `promotion_review.py` (same task dir). Six gates, all of which I added after the corresponding bug bit me in a real run:

**Gate 1 - Drop test clients.** Filter at the source: skip rows where `clientName` matches `\(\s*test\s+client\s*\)` (case-insensitive). The DB `test_client` flag is *not* reliable - PhishFort's own brand has `test_client=false` but name `phishfort (Test Client)`.

**Gate 2 - Dedupe ssdeep candidates by `targetId`.** When the same DOM ssdeep fingerprint exists across multiple owned domains (e.g. coinsbee.cn / .de / .fr all serving the same template), the first encounter wins as `promote`; the rest become `review` with a `duplicate ssdeep targetId - canonical row owned by snapshot N` note. Otherwise the second/third POSTs collide on the same target row.

**Gate 3 - Favicon DOM/HTTP canonicalisation.** When `dom_favicon_md5 == http_favicon_md5`, emit only the canonical `http_favicon_md5` row (the classifier reads HTTP first). When they differ, emit both. Maintain a deny-list of known platform-default favicon MD5s (`c36351f4817c6d4abfd93cb003b95b1d` = Notion default; extend as discovered) and reject promotion for any match.

**Gate 4 - Drop GTM-iframe `http_inner_text` rows.** The HTTPReq scraper sometimes leaks raw GTM noscript markup as inner_text (rows starting with `<iframe src="https?://www.googletagmanager`). These match any GTM-using site so they're false-positive bait. Drop unconditionally.

**Gate 5 - Tighten HQ gate at content level.** Even after upstream snapshot scoring, re-check `text_length >= 500` and re-apply NON_CONTENT_PATTERNS before emitting any text-derived candidate (`dom_title`, `dom_inner_text`, `http_inner_text`, etc.).

**Gate 6 - Brand-vs-surface-brand demotion.** If `brand_evidence` (domain tokens + client tokens found in title/innerText) is empty, demote text-derived candidates from `promote` to `review`. Catches snapshots where the surface brand differs from the configured brand (e.g. tymedigital.com renders GoTyme content; promotes would teach the classifier "tymedigital looks like GoTyme").

Each generated `hash_entry` value MUST include:
```json
{
  "brand": "<safe-domain>",
  "category": "brand_impersonation",
  "disposition": "malicious",
  "hash_type": "dom",
  "match_threshold": 0.85,
  "source": "snapshot-harvest-<date>",
  "notes": "Legitimate page fingerprint from <domain> snapshot <id> - matches indicate impersonation"
}
```

### 5. Validate

LLM-based two-pass validation:

1. Run an LLM (e.g. Claude) over the candidate set with a permissive prompt - produces an upper-bound report.
2. Run the same LLM with a stricter prompt that requires explicit brand evidence - produces a lower-bound report.
3. Reconcile: rows the strict pass demotes should override the permissive pass.
4. Include negative controls: snapshots that are Cloudflare challenges / Notion frames / parked domains should produce **zero** promote-tier rows. If they don't, the gates above need tightening.

Validation should produce a per-row disposition: `promote` / `review` / `reject` with reasoning. Persist as JSONL alongside the candidate file.

### 6. Promote

For each `tier=promote` row, group by `clientId` and per source snapshot:

```http
POST /api/detection-data/promote
{
  "clientId": "<actual id, never test-client>",
  "entries": [
    {"targetType": "...", "targetId": "...", "dataType": "...", "value": "..."}
  ],
  "source": {"type": "snapshot", "ref": "<numeric snapshot id>"},
  "promotedBy": "<workflow-and-date label>"
}
```

Important:
- `source.type` is `"snapshot"`, **not** `"corpus"`. The Go schema comment in `services/detection-core/src/interfaces/detection-data.interface.go` previously misled callers to use `"corpus"`; that string fails the favicon evidence helper's `sourceType === "snapshot"` filter. Use `"snapshot"`.
- `source.ref` must be the *numeric* local snapshot id. Non-numeric refs pass the API but fail the favicon-thumbnail helper's `Number.isInteger` guard.
- One POST per (clientId, snapshotId) - the source ref is scalar.
- Cluster-sourced rows (from classifier-worker's cluster promoter) use `source.type="ssdeep_cluster"` and `client_id="__system__"`; these are out of the snapshot-harvest workflow.

### 7. Verify

Three checks:

```bash
GW=http://<stack>.localhost:18000

# (a) Rows landed where expected
curl -s "$GW/api/detection-data?source_type=snapshot&active=true&limit=5000" | jq '.data | length'

# (b) Classifier-worker picked them up (the load cache must have refreshed since promotion)
curl -s "$GW/api/classifier-data/status" | jq '.sources'
# All sources should be status=ok with last_success_at recent.

# (c) Re-run the diagnosis from step 1 and compare: the (client x classifier) gap list should shrink.
```

If `(b)` shows stale `last_success_at`, force a refresh:
```bash
curl -s -X POST "$GW/api/classifier-data/refresh"
```

### 8. Brand info + brand_logo_prompt (parallel workflow for the LLM evaluator)

The `unified_incident_evaluator` classifier consumes two target_type=brand rows per client. These are not snapshot-derived - they're crafted brand profiles:

- `brand_info` - structured JSON: brand name, variations, description, sector, year founded, owned domains, social handles, etc.
- `brand_logo_prompt` - natural-language description of the brand's visual identity for an LLM vision model: logo shape, primary colours, signature elements.

Workflow:

1. For each client without a `brand_info` row: gather from canonical-domain DOM scrape (title, meta description, og:image), public sources (Wikipedia, Crunchbase) if approved, and structured prompts to an LLM. Persist as JSON.
2. For each client without `brand_logo_prompt`: load the favicon and any logo asset from the snapshot's storage path; describe via vision LLM. Persist as a prompt string.
3. Promote as `target_type="brand"`, `targetId=<clientId>`, `dataType="brand_info"` / `"brand_logo_prompt"`.

See `/workspace/detection-platform-metal-work/busy/brand-corpus-fill-*/` for a current-cycle pattern.

## Common traps (the ones that cost real time)

- **The schema-doc lie.** `PromoteSource.Type`'s comment lists `'corpus' | 'incident' | 'ssdeep_cluster' | 'manual'`. Running code writes `'snapshot'`. Always pass `"snapshot"`. (Fixed in the doc as of commit `4f4aa80f`, but the lesson sticks.)
- **Slim cluster `hash_entry` rows.** Cluster-promoted hashes carry only `{source_cluster_id, hash_type, match_threshold, source}` - no brand/disposition/category. The UI and the classifier are expected to look those up on the parent `cluster_metadata`. Don't expect rich payload on cluster-sourced hash rows.
- **The `__system__` pseudo-client.** Global filters (cluster non_content suppressors, etc.) live under this string. There's no corresponding row in `clients`; the FK is convention-only. Don't attach `__system__`-class rows to a real brand client - they pollute that client's grouped view in the UI.
- **classifier-worker manifest 502.** Without classifier-worker, the Classifier Data page falls back to per-(targetType, dataType) cards labelled by data-type name (not classifier name). Surface tell: cards say `dom_favicon_md5` instead of `f4-favicon-comparison`. Don't draw coverage conclusions from this view.
- **HQ-label drift.** `snapshot_harvest.py` may label a snapshot `quality=high` even when its content_ok flag is false (snap 79 Cloudflare challenge, snap 76 Notion default). The downstream candidate generator's `content_ok` gate catches the leak, but `snapshot_quality.jsonl` carries the wrong label. Either re-derive `quality` at promotion time or fix at source.
- **Server-side multi-data_type filter.** The detection-core list endpoint accepts `data_type=A,B,C` (comma-separated -> `IN (...)` clause) as of commit `db68ed3c`. Multi-data-type classifier views (favicon, unified_incident_evaluator, social_*) rely on this.

## Tools

- `/workspace/tools/db/dbctl` - read-only prod query, Cloudflared-tunnelled.
- `/workspace/tools/gateway/gatewayctl` - bring up / inspect local stacks.
- `snapshot_harvest.py` (task-local pattern) - Chrome scrape orchestration + scoring.
- `promotion_review.py` (task-local pattern) - six-gate candidate generator.
- `/api/detection-data/promote` - local POST endpoint.
- `/api/classifier-data/status` - classifier-worker load state.
- `/api/classifier-data/refresh` - force a cache refresh after a promotion batch.

## Provenance and follow-ups

After each cycle:

- Save the diagnosis report + new candidate file under `/workspace/datasets/adhoc/<task>-<date>/` (per workspace dataset conventions in `/workspace/AGENTS.md`).
- Update `/workspace/detection-platform-metal-work/busy/<task>/notes.md` with what cycle ran, what landed, what's deferred.
- Re-run diagnosis. Update the gap list. Identify next cycle's target clients.

Stop conditions for the loop:

- Every active client has snapshot-backed coverage for every classifier in their enrolled package.
- Every promoted row has been LLM-validated.
- classifier-worker `/api/classifier-data/status` reports all sources `ok`.
- Diagnosis shows zero gaps and zero non-snapshot-backed rows that haven't been intentionally retained (e.g. cluster `non_content` filters under `__system__`).

