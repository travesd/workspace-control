---
title: "feedback audit mirror production definition"
tags: [imported, claude-memory, feedback]
status: active
verified: 2026-05-20
source: /home/user/.claude/projects/-workspace/memory/feedback_audit_mirror_production_definition.md
re_verify_when: "Before promoting to AGENTS.md, shared skills, or operational automation"
---

---
name: feedback-audit-mirror-production-definition
description: When auditing a production filter/classifier, the audit verdict definition MUST mirror that component's own definition — not a broader "is it bad" notion.
metadata:
  type: feedback
---

When auditing whether a production decision component (e.g. the autohunt
`2a_impersonation_check_v8` seam) made the right call, the auditor's verdict
definition must be the **component's own definition**, read from its prompt —
not a broader notion.

**Why:** In the PR#64 audit I judged seam demotions with a broadened
"is this page malicious?" rubric (incl. credential-phishing on look-alike
domains). That produced "~55 clear-cut false negatives / severe recall
regression". The seam's actual definition is narrow: *does the page
positively portray itself AS the protected brand?* Credential-phish without
brand portrayal is `association`, which the seam **correctly** routes to
`suspicious` → a downstream workflow **by design**. Re-judged with the seam's
verbatim definition: ~2 genuine misses, not 55. The user caught this twice.

**How to apply:**
- Before auditing a component, read its prompt/spec and mirror its exact
  decision construct + disambiguators verbatim. Strip any analysis-specific
  broadening.
- A "downgrade/handoff" disposition (suspicious/monitor → another workflow)
  is *designed routing*, NOT a miss. Only the truly-dropped path (e.g.
  `safe`/no-monitoring) is a candidate false negative.
- Then apply the official-corpus / wrong-brand scrub before quoting a number
  (legit own-site and different-company-same-name inflate raw counts).
- Recurring root cause this session: corpus brand-identity gap for
  reseller/multi-brand clients (Total Cyber-Sec ↔ Banco Azteca) drove BOTH
  the FP inflation and the residual FN — fix corpus-side, not the component.
See [[feedback-verify-before-asserting]].
