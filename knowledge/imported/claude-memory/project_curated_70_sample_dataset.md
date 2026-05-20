---
name: curated-70-sample-dataset
description: Ground-truth labeled dataset for impersonation_check seam evaluation — 50 impersonation + 20 non-impersonation cases across 14+ brands
metadata: 
  node_type: memory
  type: project
  originSessionId: 28c3594c-205d-4fc9-b9e5-54a5fdd9ae29
---

Ground-truth labeled dataset for evaluating the autohunt impersonation_check seam (PR #64, MERGED 2026-05-15).

**Location (canonical, harvested 2026-05-15):** `/workspace/datasets/curated-impersonation-70sample/` — CSV + per-incident base assets + `MANIFEST.json`. The origin task dir (now `done/20260515-fri/.../audit-pushed-incidents-20260506/corpus-edits/filter/curated-70sample/`) retains the full iteration trace evidence and `_results_pre_*` snapshots (process evidence, not the reusable dataset).

**File:** `final_dataset_50imp_20noimp.csv` — 70 labeled rows.

**Schema:** `iid, brand, subject, source, category (impersonation | non_impersonation), label (impersonation | association | none), confidence (high | medium | low), notes, dashboard_url`

**Coverage:**
- 50 impersonation: Trezor=21, Meritking=16, Tether=2, brave=2, coingecko=2, Vinted=2, 1inch=1, pancakeswap=1, yellowcard=1, bitkub=1, Sky Money=1.
- 20 non-impersonation: 14 brands, 11 `association` (FLASH BY JO-style brand-themed scams, IdP tenants, composite-brand services, brand widgets) + 9 `none` (Cloudflare interstitials, unrelated content despite brand-confusable hostname).

**Assets:** `curated-70sample/incidents/<iid>_{screenshot.png, page.html, meta.json, dom_text.json}` for all 70 — usable as inputs to v13 / impersonation_check_v2 evals.

**Why:** Why each label landed where it did is in the `notes` column — was used during curation and is a quick way for future runs to know the deciding signal per case. The dataset reflects the 3-class framework: `impersonation = page wears the brand`; `association = touches brand, identity is something else`; `none = no meaningful brand presence`. Disclaimers don't change classification; brand variations (USDT for Tether, BAT for Brave) count as the brand.

**How to apply:** Use as a stable regression benchmark when iterating the impersonation_check seam prompt or v13 workflow. Run v13 against the 70 iids, compare verdict vs. ground-truth `label` column; expected mapping: `impersonation → takedown`, `association → suspicious`, `none → safe`. Above ~85% match is the realistic floor given seam non-determinism on boundary cases. Re-curate (refresh + add cases) when adding a new brand or when v13 architecture changes materially.

Relates to [[project-monitor-lifecycle-scope]] (downstream verdict semantics).
