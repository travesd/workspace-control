---
title: "feedback ssdeep classifier refresh"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_ssdeep_classifier_refresh.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: SSDeep classifier refresh requires service restart
description: Selective refresh endpoints on classifier-worker don't send Redis PubSub notifications — classifier services keep stale in-memory cache until restarted or background cycle runs
type: feedback
originSessionId: b822048f-5ea0-4685-be40-ed454892fc03
---
The `/refresh/<source>` selective endpoint on classifier-worker writes to Redis but does NOT call `_publish_notification()`. Only `refresh_all()` (full refresh) sends the Redis PubSub notification that triggers classifier services to reload.

**Why:** Classifier services subscribe to `clsfr:v1:refresh-notification` via Redis PubSub. Redis PubSub is fire-and-forget — no message persistence. Without the notification, classifier processes hold stale in-memory state.

**How to apply:** After any detection_data change that needs immediate effect (deactivating hashes, threshold changes), trigger a rolling restart of the classifier service. In metal Docker Swarm: `docker service update --force <stack>_<service>` — verify the actual service name first with `docker service ls` before running. Don't rely on selective refresh endpoints alone. (Original GKE-era guidance was `kubectl rollout restart deployment/clsfr-domains-deployment -n detection-classifiers-production`; same concept, different orchestrator. Verify the Redis PubSub mechanics still match in metal source before asserting them as current.)
