---
name: project-monitor-lifecycle-scope
description: Monitor judgement is reserved for brand-confusable hostnames currently showing no content; content-bearing non-impersonation pages do NOT belong in monitor
metadata: 
  node_type: memory
  type: project
  originSessionId: 28c3594c-205d-4fc9-b9e5-54a5fdd9ae29
---

Monitor judgement is reserved for **brand-confusable hostnames currently showing no content** (parked, Cloudflare interstitial, security challenge, sparse). Those domains might activate impersonation later, so the monitoring feeder re-queues them on the doubling-interval schedule.

A page that has clear content but isn't impersonating the protected brand (e.g. unrelated gambling content on `tetherzip.com`, or a "Flash USDT" service that exploits brand trust without claiming to BE Tether) does **NOT** belong in monitor — that misuses the monitoring schedule. Use suspicious (operator review) or safe (no action) instead.

**Why:** Monitoring is a scarce resource — every monitor row gets re-evaluated on the day-1/2/4/8/16/32 schedule. Filling it with content-bearing FPs that won't change state burns the schedule on incidents that should be definitively closed.

**How to apply:** When designing FP filters that downgrade takedown verdicts, split the downgrade target by page content:

- `relationship_type == brand_presenting_surface` → keep takedown
- `relationship_type != brand_presenting_surface` AND page is non-content / brand-confusable hostname → monitor
- `relationship_type != brand_presenting_surface` AND page has meaningful content → suspicious or safe (not monitor)

Relates to [[feedback-classification-review]] (judgement semantics in the metal stack).
