---
name: Verify before asserting — no inference as fact
description: Never claim how code works, what data shows, or how systems behave without verifying. Read the code, query the data, check the state — then assert. Sub-agent reports are inputs, not facts.
type: feedback
originSessionId: b822048f-5ea0-4685-be40-ed454892fc03
---
Never assert facts about code, data, or system state without verifying first. If you haven't read the actual source, queried the actual data, or checked the actual state, say "I haven't verified this" and go check.

**Why:** This has been called out repeatedly across distinct tasks — the recurring failure mode is: see data → construct plausible theory → state theory as fact → get caught. Past incidents:

1. **must-submit-force-with-judge** — speculated "LLM routes by source pattern" without reading the router code (called out 3+ times in the same task).
2. **autohunt SafeSubject** — claimed SafeSubject was "dropped" in the push handler based on an agent's report. 92.3% of incidents were resolving client_id correctly, directly contradicting the claim. Doubled down and proposed a "fix" for something that wasn't broken.
3. **Promoter cluster output** — claimed promoter "picked 1 representative hash"; was actually the algorithm's output for cohesive clusters.
4. **Audit-log search** — claimed "zero autohunt incidents hit autohunt workflows" while searching the wrong audit-log field.
5. **Pivot temp-content takedown bug (2026-04-08)** — asserted ssdeep hashes weren't generated based on API response fields without reading the enrichment code that clearly computes them; questioned a deliberate security policy baselessly.
6. **Social enrichment design (2026-04-13)** — built two design proposals around per-feeder toggles keyed on `feeder_settings.feeder_name`, trusting a sub-agent's report. Autohunt — the primary use case — has no `feeder_settings` row and submits via `/incident/push` with sources like `api-autohunt-v2-*` that never pass through `CheckFeeder`. Entire design was useless for the stated case.
7. **PromQL source filter sanitizer** — added a regex rejecting colons. Production source labels contain colons (`classifiers:api-manual-report`). Caused user-facing error on first prod use. Could have been caught with `group by (source) ({__name__=~"classifier_.*"})`.

**How to apply:**
- Before claiming X doesn't exist: query for it (DB, Redis, API, grep).
- Before claiming a system does/doesn't do Y: read the code path that would do Y.
- Before claiming something is misconfigured: look at the actual data, not the label.
- When data is surprising, say "I need to check why" and check — don't fill the gap with theory.
- Distinguish "the data shows X" from "I think Y explains X". Never use "the system picked", "it appears that", "this means" without having traced the actual code path.
- **Before writing input validation/allowlists**, query the live system for distinct values (`group by (label) (metric)`, `SELECT DISTINCT col FROM table LIMIT 100`). Don't guess what characters might appear.
- **Sub-agent reports are inputs, not facts.** When an Explore or research sub-agent returns findings, treat its claims as hypotheses until you personally verify the load-bearing premises — especially any premise that determines whether a design is viable.
- **Before designing, verify the domain objects named by the user.** If the user says "autohunt feeder", first check whether autohunt is actually modelled as a feeder.
- When the user challenges a claim: immediately go verify the code instead of defending or launching more speculative agents.
- In investigation documents: separate verified facts (with evidence) from speculation/hypotheses.
