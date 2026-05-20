---
title: "Block-size 96 ssdeep httpreq hashes are unreliable"
description: "ssdeep hashes at block size 96 (especially httpreq type) match HTTP boilerplate too broadly — set match_threshold=0.85 minimum and prefer DOM hashes"
tags: [feedback, memory-migration]
status: active
verified: 2026-05-20
source: "sanitized workspace memory migration, 2026-05-20"
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation."
---

Block size 96 captures ~6KB of structure. For httpreq hashes, this is dominated by HTTP headers/boilerplate shared across unrelated sites. The `96:1j9j...` Cloudflare hash family had a 4.7% false positive rate, matching crunchbase.com, luminor.lt, forum.mikro.com.tr at 88-96% similarity.

**Why:** The `lTkDa...` family at the same block size had only 0.2% FP rate — so the issue is hash-specific, not purely block-size. But low block sizes amplify the problem.

**How to apply:**
- All block-size-96 hashes should have `match_threshold >= 0.85`
- Deactivated the `96:1j9jwIjYj5jDK` family (4 hashes) — too broad
- Kept the `96:lTkDa/D+DMF` family — low FP rate
- When promoting new hashes, prefer DOM type over httpreq at low block sizes
