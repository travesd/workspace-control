---
name: Only promote ssdeep clusters with client domain brands
description: Non-client malicious ssdeep clusters cause false positives and can't route to gatekeeper — only promote clusters where brand matches an active client domain
type: feedback
---

SSDeep classifier sets `safeDomain = brand` field from the hash entry. The gatekeeper's `findClient()` matches safeDomain against client domain lists. If brand is a name (e.g., "OnlyFans", "MetaMask") instead of a client domain (e.g., "trezor.io"), gatekeeper routing fails.

**Why:** The OnlyFans cluster (sc_00005, low homogeneity) caused false positives on unrelated sites. Non-client brand hashes generate [CD8] tags and malicious disposition without enabling takedown.

**How to apply:**
- Only promote malicious clusters where `brand` matches an active client domain
- Non-content clusters are safe to promote broadly
- Before promoting, verify brand against `GET /api/v1/clients?active=true` domain lists
- The `brand` field must be a domain string (e.g., `trezor.io`), not a brand name (e.g., `Trezor`)
